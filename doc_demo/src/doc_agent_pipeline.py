"""
Agentic Documentation Pipeline
LangGraph state machine: Writer → Critique → Formatter → Grounding → Save

Works for all three modes: Program, Module, Application.
"""

import os
import json
import re
import functools
import sqlite3
from pathlib import Path
from typing import Any, Dict, Literal, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from context_engine import apply_document_coverage


class SafeConsole:
    def print(self, *args, **kwargs):
        try:
            print(*[str(arg) for arg in args])
        except Exception:
            pass


console = SafeConsole()


def _sqlite_connect(db_path: str):
    if os.name == "nt":
        return sqlite3.connect(Path(db_path).resolve().as_uri(), uri=True)
    return sqlite3.connect(db_path)


# ── State ──────────────────────────────────────────────────────────────────────

class DocAgentState(TypedDict):
    mode:             str   # "Program", "Module", "Application"
    subject:          str   # program ID, module name, or "Full Application"
    context:          str   # pre-built context string from app.py helpers
    draft:            str   # document produced by Writer
    critique_feedback:str   # issues found by Critique
    critique_passed:  bool  # True when Critique is satisfied
    formatted_doc:    str   # final cleaned document
    grounding_passed: bool  # True when deterministic grounding checks pass
    grounding_feedback:str  # source-grounding issues, if any
    context_metadata: Dict[str, Any]
    coverage_ledger:  Dict[str, Any]
    iteration:        int   # how many write→critique loops have run
    max_iterations:   int   # cap — default 3
    saved:            bool


# ── LLM factory ───────────────────────────────────────────────────────────────

class DocRunRequest(BaseModel):
    """Validated public input for the agentic documentation pipeline."""

    model_config = ConfigDict(extra="forbid")

    mode: Literal["Program", "Module", "Application"]
    subject: str = Field(min_length=1)
    context: str = Field(min_length=20)
    db_path: str = Field(min_length=1)
    max_iterations: int = Field(default=3, ge=1, le=5)
    context_metadata: Dict[str, Any] = Field(default_factory=dict)
    coverage_ledger: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("subject", "context", "db_path")
    @classmethod
    def _strip_text(cls, value: str) -> str:
        return value.strip()


class CritiqueResult(BaseModel):
    """Strict shape expected from the critique LLM JSON."""

    model_config = ConfigDict(extra="ignore")

    passed: bool = True
    issues: list[str] = Field(default_factory=list)

    @field_validator("issues", mode="before")
    @classmethod
    def _normalise_issues(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        return [str(value)]


class GroundingReport(BaseModel):
    """Deterministic save gate for source-grounded generated docs."""

    passed: bool
    issues: list[str] = Field(default_factory=list)


class GeneratedDocRecord(BaseModel):
    """Validated shape for generated_docs cache writes."""

    model_config = ConfigDict(extra="forbid")

    mode: Literal["Program", "Module", "Application"]
    subject: str = Field(min_length=1)
    document_text: str = Field(min_length=100)
    context_metadata: Dict[str, Any] = Field(default_factory=dict)
    coverage_ledger: Dict[str, Any] = Field(default_factory=dict)


def _get_llm():
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        val = os.environ.get(key, "")
        if "127.0.0.1:9" in val or "localhost:9" in val:
            os.environ.pop(key, None)

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.environ.get("GEMINI_API_KEY"),
        temperature=0.3,
        max_output_tokens=65536,
    )


# ── Prompts ────────────────────────────────────────────────────────────────────

GROUNDING_RULES = """
GROUNDING RULES (mandatory — violations are treated as errors):
- Do NOT infer access technology. If SYSTEM DATA does not explicitly state the
  program uses VSAM, DB2, IMS, or DL/I, do not claim it does.
- Copybook names: only reference copybooks that appear verbatim in
  "Shared Data (Copybooks)" in SYSTEM DATA. Never substitute or invent names.
- If "Shared Data (Copybooks)" or "Source COPY statements" lists copybooks,
  never write that the program has no COPY statements or no copybooks.
- File and dataset names: only reference names that appear in
  "Files Accessed" or "Input/Output Datasets" in SYSTEM DATA.
- IMS DL/I calls: only reference IMS functions (GU, GHN, ISRT, REPL, DLET) that
  appear in the "IMS DL/I Calls" section of SYSTEM DATA. Do not infer IMS usage.
- For IMS programs, explicitly document ENTRY 'DLITCBL' when present, every
  CBLTDLI function, the PCB, segment area, SSA name, SSA segment, SSA qualifier,
  and the exact paragraph where the call appears.
- For IMS parent/child flows, describe the exact sequence from SYSTEM DATA:
  input record read, key move to SSA key value, parent GU using the qualified SSA,
  then child ISRT only when the PCB status condition allows it.
- Business rules must tie each rule to concrete source conditions and actions
  from SYSTEM DATA, such as file status fields and PCB status values. Do not
  split one condition into repetitive generic rules.
- If a fact is missing from SYSTEM DATA, write "(not present in extracted data)"
  rather than guessing.
- If SYSTEM DATA includes a "Code Anomalies / Known Issues" block, you MUST
  add a dedicated "Known Issues / Code Anomalies" subsection before Migration
  Notes. List every flagged item with severity, location, description, and
  recommendation verbatim from SYSTEM DATA. Do not invent or omit anomalies.

- If a `BUSINESS_FORMULA` anomaly is present, you MUST quote the exact formula
  (including the literal divisor) in the Business Rules section and explain its
  business meaning using the "interpretation" line provided. NEVER write
  "specific formula not detailed" — the formula is right there in SYSTEM DATA.

- If an `ABEND_TERMINATION` anomaly is present for a paragraph, describe the
  error path of that paragraph using the words "abend" or "terminates the
  program" — never "rejects the record" or "skips the record" or "logs and
  continues". The program ENDS on that error.

- If a `CONTROL_BREAK_PATTERN` anomaly is present, you MUST add a paragraph in
  the Program Description section (or Section 6 Business Rules) describing the
  control break: which key field changes, which holder field stores the prior
  value, which paragraph is invoked to flush the previous group, and the fact
  that the same paragraph is called once more after the loop to flush the
  final group. This is the architectural backbone — never omit it.

- If `program_parameters` lists external parameters, document each one
  explicitly in Section 5 (JCL Batch Context) AND wherever it is consumed.
  Use the "usage_sites" list verbatim — say which paragraphs MOVE/READ from
  the parameter. Never write "the specific content and usage are not detailed".

- If a `STUB_PARAGRAPH` anomaly says a paragraph is a stub, document it as
  "[NOTICE] UNIMPLEMENTED FEATURE: <paragraph-name> is a placeholder and
  contains no executable logic". Never describe the stub's behaviour as
  "the specific formula is not detailed" — it has no behaviour.

- ANTI-SPECULATION RULE (mandatory): never use the words "implied", "likely
  occurs", "may be handled", "might exist", "presumably", "could be" when
  describing program behaviour. If something is not in SYSTEM DATA, write
  "(not present in extracted data)" — do NOT speculate that it happens
  "in a preceding program" or "via CICS transaction security" unless SYSTEM
  DATA explicitly says so.

- ANTI-COMPRESSION RULE (mandatory): when SYSTEM DATA shows a MOVE statement
  or assignment guarded by an IF condition, document BOTH the guard AND the
  action. Do not summarise "X is set to Y" when the source actually says
  "IF condition THEN X is set to Y" — that strips the conditional logic.

- ARRAY / TABLE RULE: if SYSTEM DATA shows multiple MOVE statements writing
  different values to the same array (e.g. ARR(1), ARR(2), ARR(3)...), you
  MUST list ALL slots and their values. Do not stop after the first two.

- LITERAL FILE NAMES: if `Source literal/status facts` lists items like
  `WS-USRSEC-FILE VALUE 'USRSEC'`, the dataset / VSAM file name IS 'USRSEC'.
  Document it. Never say "the file name is not present" when a VALUE clause
  is shown.

- CICS RIDFLD / DATASET parameters: when documenting EXEC CICS READ / WRITE /
  DELETE commands, quote the exact parameter values from SYSTEM DATA's
  "Details" column (e.g. "RIDFLD(SEC-USR-ID)" not "RIDFLD(USRIDINI)" — they
  are different fields). If a command has no RIDFLD, do NOT add one to the
  description; the absence is significant (it means token-based locking).

- EXTERNAL CALLS: if `STATIC_CALL_EXTERNAL` anomalies are present, list every
  external program that is CALLed (CEE3ABD, COBDATFT, etc.) under
  Section 3 (Program Connectivity). Do NOT write "this program calls no
  external subroutines" if any STATIC_CALL_EXTERNAL appears in SYSTEM DATA.

- OPEN_WITHOUT_CLOSE: if any file is OPENed but not CLOSEd, document it
  explicitly under "File Lifecycle" or in Migration Notes — do NOT write
  "all files are closed" when the data shows otherwise.
"""

WRITER_SYSTEM = (
    "You are a chief software architect writing technical documentation "
    "for a legacy COBOL mainframe modernisation team. "
    "Write clearly, specifically, and completely. Never truncate sections."
)

CRITIQUE_SYSTEM = """You are a senior technical editor reviewing COBOL documentation for a modernisation team.
Your job is to find gaps, vague statements, and missing sections — not to rewrite, just to flag issues.
Respond ONLY with JSON: {"passed": true/false, "issues": ["issue 1", "issue 2"]}
If the document is complete respond with {"passed": true, "issues": []}"""

FORMATTER_SYSTEM = (
    "You are a technical documentation formatter. "
    "Fix heading levels, remove duplicate sections, ensure consistent formatting. "
    "Do NOT remove or summarise any content — only clean structure. "
    "Return the complete cleaned document."
)


def _writer_prompt(mode: str, subject: str, context: str, feedback: str = "") -> str:
    feedback_block = (
        f"\n\nPREVIOUS CRITIQUE FEEDBACK — address every point below:\n{feedback}"
        "\n\nRewrite the full document addressing all issues above."
    ) if feedback else ""

    if mode == "Program":
        instructions = f"""Write a comprehensive technical documentation document for "{subject}" and all its connected programs.

The document must contain these numbered sections:
1. Executive Summary — what this program does, who triggers it, business importance
2. Program Descriptions — each program in execution order: what it does, data read/written, business decisions, output produced
3. Program Connectivity and Data Flow — which program calls which, shared data structures, data flow between programs
4. BMS Screen & CICS Interaction (for ONLINE programs) — describe the BMS screen layout (input/output fields, user interaction flow), CICS commands used (SEND MAP, RECEIVE MAP, READ, WRITE, XCTL, LINK, RETURN), and the screen navigation pattern
5. JCL Batch Context (for batch programs) — describe which JCL jobs execute this program, the job steps, input/output datasets, and how the program fits into the batch processing chain
6. Critical Business Rules and Validation Logic — list specific rules with conditions and actions
7. Migration Notes — complexity rating, modern equivalent, recommended microservice boundary. For CICS programs suggest REST API + modern UI. For batch programs suggest cloud-native batch alternatives.

Write in flowing prose with clear numbered headings. Reference actual program IDs, paragraph names, copybook names, screen names, and file names throughout.

CITATION REQUIREMENT (mandatory):
For each program covered, you MUST cite at least 3 specific paragraph names from the program's
paragraph list provided in SYSTEM DATA below. Format citations as `paragraph PARA-NAME` so the
reader can locate the source code. Example: "Card validation runs in `1500-VALIDATE-CARD` before
the transaction is committed by `2000-PROCESS-TRANSACTION`." Only cite paragraphs that actually
appear in SYSTEM DATA — never invent paragraph names. If the program has fewer than 3 paragraphs,
cite all of them.

{GROUNDING_RULES}"""

    elif mode == "Module":
        instructions = f"""Write a comprehensive module specification document for the "{subject}" module.

The document must contain these numbered sections:
1. Module Overview — business capability this module provides, who uses it, its role in the overall system
2. Programs in This Module — each program with a clear one-paragraph description of its purpose
3. Internal Flow — how programs within this module interact, the sequence of operations end-to-end
4. Data Architecture — files, datasets, and shared copybooks this module uses
5. BMS Screens & CICS Interaction (for ONLINE programs) — describe BMS screen layouts (input/output fields), CICS commands, and user interaction flows for each screen-driven program in the module
6. JCL Batch Context (for batch programs) — describe JCL jobs that execute module programs, datasets flowing in/out, batch execution dependencies
7. Key Business Rules and Validations — enforced by programs in this module
8. External Dependencies — what other modules/programs this module depends on and what depends on it
9. Migration Strategy — recommended service boundary, suggested modern architecture (REST APIs for CICS screens, cloud batch for JCL jobs), migration order for programs

Write in flowing prose with numbered headings. Reference specific program IDs, screen names, copybook names, and file names.

CITATION REQUIREMENT (mandatory):
For every program in the Internal Flow section, cite at least 2 paragraph names per program in
the format `paragraph PARA-NAME`. Use only paragraph names that appear in SYSTEM DATA. Never
invent paragraph names — fabricated citations will fail validation.

{GROUNDING_RULES}"""

    else:  # Application
        instructions = """Write a comprehensive Application Architecture Document.

CRITICAL FORMATTING RULES:
- Do NOT use markdown tables anywhere. Use numbered lists and prose instead.
- Write every module subsection in full — do not skip any module.
- Do not truncate any section.

The document must contain these numbered sections:
1. Executive Summary — what the application does, who uses it, business criticality, case for modernisation (2-3 paragraphs)
2. System Architecture Overview — online CICS tier vs batch tier, entry points, schedulers, user touchpoints
3. Module Breakdown — one numbered subsection per module containing: business domain, list of programs with one-sentence roles, how programs interact internally
4. CICS Online Tier & BMS Screens — describe the online programs and their BMS screen maps: what fields users see, input/output fields, CICS commands driving screen navigation (SEND MAP, RECEIVE MAP, XCTL, LINK), and how screens chain together
5. Batch Processing Tier & JCL Jobs — describe JCL batch jobs: what each job does, programs executed, input/output datasets, batch processing flow and dependencies between online and batch tiers
6. Inter-Module Data Flow — which modules depend on which, shared files/copybooks coupling modules, 3-4 critical data paths as step-by-step numbered flows
7. Business Rule Inventory — rule categories with counts, top 5 highest-density programs and what kinds of rules they contain
8. Migration Roadmap — for EACH module write: target microservice name, for CICS screens suggest REST API + modern UI (React/Angular), for batch JCL suggest cloud-native batch (AWS Batch/Step Functions), migration order (1=first) with justification, key technical risks, suggested tech stack. End with an overall ordered migration sequence.
9. Risk Register — top 7 highest-risk components as a numbered list, each with: why it is high risk, concrete mitigation strategy

{GROUNDING_RULES}"""

    return f"""{instructions}{feedback_block}

SYSTEM DATA:
{context}

Write the complete document now:"""


def _critique_prompt(mode: str, subject: str, draft: str) -> str:
    required = {
        "Program":     ["Executive Summary", "Program Descriptions", "Data Flow", "Business Rules", "Migration Notes"],
        "Module":      ["Module Overview", "Programs in This Module", "Internal Flow", "Data Architecture", "BMS Screens", "JCL Batch", "Business Rules", "External Dependencies", "Migration Strategy"],
        "Application": ["Executive Summary", "System Architecture", "Module Breakdown", "CICS Online Tier", "Batch Processing", "Inter-Module Data Flow", "Business Rule Inventory", "Migration Roadmap", "Risk Register"],
    }
    sections = ", ".join(required.get(mode, []))

    citation_check = ""
    if mode == "Program":
        citation_check = "\n6. Does each covered program cite at least 3 specific paragraph names (using `PARA-NAME` backticks)? Flag if missing."
    elif mode == "Module":
        citation_check = "\n6. Does the Internal Flow section cite at least 2 paragraph names per program (using `PARA-NAME` backticks)? Flag if missing."

    return f"""Review this {mode}-level COBOL documentation for "{subject}".

Check for ALL of the following:
1. Are ALL required sections present and complete? Required sections: {sections}
2. Are there any vague, generic, or placeholder statements ("TBD", "not available", "various programs")?
3. Are specific program IDs, module names, file names referenced throughout — not just in the data section?
4. For Application mode: does the Migration Roadmap cover EVERY module individually? Does the Risk Register have exactly 7 entries?
5. Is any section truncated, cut off mid-sentence, or significantly shorter than expected?{citation_check}

DOCUMENT TO REVIEW:
{draft[:9000]}{"...[truncated for review]" if len(draft) > 9000 else ""}

Respond with JSON only: {{"passed": true/false, "issues": ["specific issue 1", "specific issue 2"]}}"""


# ── Node functions ─────────────────────────────────────────────────────────────

def _program_context_block(context: str, subject: str) -> str:
    """Return the SYSTEM DATA block for one program when present."""
    marker = f"## Program: {subject}"
    start = context.find(marker)
    if start < 0:
        return context
    next_prog = context.find("\n## Program:", start + len(marker))
    return context[start:] if next_prog < 0 else context[start:next_prog]


def _csv_tokens_after_colon(line: str) -> list[str]:
    if ":" not in line:
        return []
    return [
        token.strip().strip("`.")
        for token in line.split(":", 1)[1].split(",")
        if token.strip()
    ]


def _ground_document(mode: str, subject: str, context: str, document: str) -> GroundingReport:
    """Check high-risk source facts before caching LLM documentation."""
    if mode != "Program":
        return GroundingReport(passed=True)

    block = _program_context_block(context, subject)
    text_upper = document.upper()
    issues: list[str] = []

    expected_copybooks: set[str] = set()
    ims_fn_counts: dict[str, int] = {}
    for call_line in block.splitlines():
        call_upper = call_line.upper()
        fn_match = re.search(r"CALL\s+'CBLTDLI'\s+([A-Z0-9-]+)", call_upper)
        if fn_match:
            fn = fn_match.group(1)
            ims_fn_counts[fn] = ims_fn_counts.get(fn, 0) + 1

    for line in block.splitlines():
        upper = line.upper()
        if "SHARED DATA (COPYBOOKS)" in upper and "NONE" not in upper:
            expected_copybooks.update(cb.upper() for cb in _csv_tokens_after_colon(line))
        if "SOURCE COPY STATEMENTS" in upper:
            expected_copybooks.update(cb.upper() for cb in _csv_tokens_after_colon(line))
    expected_copybooks.discard("")
    if expected_copybooks:
        if re.search(r"DOES\s+NOT\s+COPY\s+ANY\s+COPYBOOKS|NO\s+COPYBOOKS", text_upper):
            issues.append("Document contradicts source by saying the program has no copybooks.")
        missing = sorted(cb for cb in expected_copybooks if cb not in text_upper)
        if missing:
            issues.append(f"Missing required copybook name(s): {', '.join(missing)}")

    if "ENTRY 'DLITCBL'" in block.upper() and "DLITCBL" not in text_upper:
        issues.append("Missing IMS ENTRY 'DLITCBL' entry point.")

    for line in block.splitlines():
        stripped = line.strip()
        upper = stripped.upper()
        if "CALL 'CBLTDLI'" in upper:
            for token in re.findall(r"\b(GU|GHN|GHU|GN|GNP|GHNP|ISRT|REPL|DLET|CHKP|ENTRY)\b", upper):
                if token not in text_upper:
                    issues.append(f"Missing IMS function {token}.")
            for key in ("PCB=", "AREA=", "SSA="):
                if key in upper:
                    value = upper.split(key, 1)[1].split(",", 1)[0].split()[0].strip("()[]")
                    if value and value not in text_upper:
                        issues.append(f"Missing IMS {key.rstrip('=')} {value}.")
            m_para = re.search(r"\[IN\s+([A-Z0-9-]+),\s+LINE", upper)
            if m_para and m_para.group(1) not in text_upper:
                issues.append(f"Missing IMS call paragraph {m_para.group(1)}.")
            fn_match = re.search(r"CALL\s+'CBLTDLI'\s+([A-Z0-9-]+)", upper)
            if fn_match and m_para and ims_fn_counts.get(fn_match.group(1), 0) == 1:
                fn = fn_match.group(1)
                correct_para = m_para.group(1)
                known_paras = set(re.findall(r"`([A-Z0-9][A-Z0-9-]+)`", block.upper()))
                known_paras.update(re.findall(r"PARAGRAPH\s+([A-Z0-9][A-Z0-9-]+)", block.upper()))
                known_paras.add("MAIN-PARA")
                wrong_paras = sorted(p for p in known_paras if p != correct_para and "-" in p)
                sentences = re.split(r"(?<=[.!?])\s+", text_upper)
                for sentence in sentences:
                    if fn not in sentence:
                        continue
                    for wrong_para in wrong_paras:
                        if wrong_para in sentence and correct_para not in sentence:
                            issues.append(
                                f"Misattributes IMS function {fn} to {wrong_para}; source shows {correct_para}."
                            )
        if re.match(r"-\s*SOURCE LITERAL/STATUS FACTS:", upper):
            for name, value in re.findall(r"([A-Z0-9-]+)\s+VALUE\s+'([^']+)'", upper):
                if name not in text_upper or value not in text_upper:
                    issues.append(f"Missing source literal {name}='{value}'.")
        if re.match(r"-\s*([A-Z0-9-]+):\s+SEGMENT=", upper):
            ssa = upper.split(":", 1)[0].lstrip("- ").strip()
            if ssa and ssa not in text_upper:
                issues.append(f"Missing IMS SSA {ssa}.")
            seg_match = re.search(r"SEGMENT=([^;]+)", upper)
            if seg_match:
                segment = seg_match.group(1).strip()
                if segment and not segment.startswith("(") and segment not in text_upper:
                    issues.append(f"Missing IMS SSA segment {segment}.")
            qual_match = re.search(r"QUALIFIER=([^;]+)", upper)
            if qual_match:
                qualifier = qual_match.group(1).strip()
                if qualifier and not qualifier.startswith("("):
                    for part in qualifier.split():
                        if part and part not in text_upper:
                            issues.append(f"Missing IMS SSA qualifier token {part}.")

    deduped = list(dict.fromkeys(issues))
    return GroundingReport(passed=not deduped, issues=deduped)


def _write_node(state: DocAgentState) -> dict:
    iteration = state.get("iteration", 0)
    feedback  = state.get("critique_feedback", "")

    if iteration == 0:
        console.print(f"[cyan]  Writer: generating {state['mode']}-level doc for '{state['subject']}'...[/cyan]")
    else:
        console.print(f"[cyan]  Writer: revision {iteration} — addressing critique feedback...[/cyan]")

    llm      = _get_llm()
    prompt   = _writer_prompt(state["mode"], state["subject"], state["context"], feedback)
    response = llm.invoke([SystemMessage(content=WRITER_SYSTEM), HumanMessage(content=prompt)])

    return {"draft": response.content, "iteration": iteration + 1}


def _critique_node(state: DocAgentState) -> dict:
    console.print(f"[cyan]  Critique: reviewing draft (iteration {state['iteration']})...[/cyan]")

    llm      = _get_llm()
    prompt   = _critique_prompt(state["mode"], state["subject"], state["draft"])
    response = llm.invoke([SystemMessage(content=CRITIQUE_SYSTEM), HumanMessage(content=prompt)])

    content = response.content.strip()
    try:
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        result = CritiqueResult.model_validate(json.loads(content))
    except Exception:
        m = re.search(r'\{[\s\S]*\}', content)
        try:
            result = CritiqueResult.model_validate(json.loads(m.group())) if m else CritiqueResult()
        except Exception:
            result = CritiqueResult(passed=False, issues=["Critique response was not valid JSON."])

    passed = result.passed
    issues = result.issues

    if passed:
        console.print("[green]  Critique: document passed quality check.[/green]")
    else:
        console.print(f"[yellow]  Critique: {len(issues)} issue(s) found — requesting revision.[/yellow]")
        for iss in issues:
            console.print(f"[yellow]    · {iss}[/yellow]")

    return {
        "critique_passed":   passed,
        "critique_feedback": "\n".join(f"- {i}" for i in issues),
    }


def _format_node(state: DocAgentState) -> dict:
    console.print("[cyan]  Formatter: cleaning document structure...[/cyan]")
    llm      = _get_llm()
    response = llm.invoke([
        SystemMessage(content=FORMATTER_SYSTEM),
        HumanMessage(content=f"Clean and format this document. Return the complete document:\n\n{state['draft']}"),
    ])
    return {"formatted_doc": response.content}


def _grounding_node(state: DocAgentState) -> dict:
    ledger = apply_document_coverage(
        state.get("coverage_ledger", {}) or {},
        state.get("formatted_doc") or state.get("draft", ""),
    )
    report = _ground_document(
        state["mode"],
        state["subject"],
        state["context"],
        state.get("formatted_doc") or state.get("draft", ""),
    )
    if report.passed:
        console.print("[green]  Grounding: source-fact checks passed.[/green]")
    else:
        console.print(f"[yellow]  Grounding: {len(report.issues)} issue(s) found.[/yellow]")
        for issue in report.issues[:8]:
            console.print(f"[yellow]    · {issue}[/yellow]")
    return {
        "grounding_passed": report.passed,
        "grounding_feedback": "\n".join(f"- {issue}" for issue in report.issues),
        "critique_passed": report.passed,
        "critique_feedback": "\n".join(f"- {issue}" for issue in report.issues),
        "coverage_ledger": ledger,
    }


def _save_node(state: DocAgentState, db_path: str) -> dict:
    if not state.get("grounding_passed", True):
        console.print("[yellow]  Save: skipped because source-grounding checks failed.[/yellow]")
        return {"saved": False}
    try:
        record = GeneratedDocRecord(
            mode=state["mode"],
            subject=state["subject"],
            document_text=state["formatted_doc"],
            context_metadata=state.get("context_metadata", {}) or {},
            coverage_ledger=state.get("coverage_ledger", {}) or {},
        )
        conn = _sqlite_connect(db_path)
        try:
            conn.execute("ALTER TABLE generated_docs ADD COLUMN context_metadata_json TEXT")
        except Exception:
            pass
        try:
            conn.execute("ALTER TABLE generated_docs ADD COLUMN coverage_ledger_json TEXT")
        except Exception:
            pass
        conn.execute("""
            INSERT OR REPLACE INTO generated_docs (
                mode, subject, document_text, context_metadata_json, coverage_ledger_json, generated_at
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            record.mode,
            record.subject,
            record.document_text,
            json.dumps(record.context_metadata, default=str),
            json.dumps(record.coverage_ledger, default=str),
        ))
        conn.commit()
        conn.close()
        console.print(f"[green]  Save: stored in DB ({state['mode']} / {state['subject']})[/green]")
        return {"saved": True}
    except Exception as e:
        console.print(f"[yellow]  Save: warning — could not save to DB: {e}[/yellow]")
        return {"saved": False}


def _should_revise(state: DocAgentState) -> str:
    if not state.get("critique_passed", False) and state.get("iteration", 0) < state.get("max_iterations", 2):
        return "revise"
    return "format"


def _should_save_or_revise(state: DocAgentState) -> str:
    if not state.get("grounding_passed", True) and state.get("iteration", 0) < state.get("max_iterations", 2):
        return "revise"
    return "save"


# ── Graph builder ──────────────────────────────────────────────────────────────

def _build_pipeline(db_path: str):
    workflow = StateGraph(DocAgentState)

    workflow.add_node("write",    _write_node)
    workflow.add_node("critique", _critique_node)
    workflow.add_node("format",   _format_node)
    workflow.add_node("ground",   _grounding_node)
    workflow.add_node("save",     functools.partial(_save_node, db_path=db_path))

    workflow.add_edge(START,      "write")
    workflow.add_edge("write",    "critique")
    workflow.add_conditional_edges("critique", _should_revise, {
        "revise": "write",
        "format": "format",
    })
    workflow.add_edge("format",   "ground")
    workflow.add_conditional_edges("ground", _should_save_or_revise, {
        "revise": "write",
        "save": "save",
    })
    workflow.add_edge("save",     END)

    return workflow.compile()


# ── Public API ─────────────────────────────────────────────────────────────────

def run_doc_pipeline(
    mode: str,
    subject: str,
    context: str,
    db_path: str,
    context_metadata: Dict[str, Any] | None = None,
    coverage_ledger: Dict[str, Any] | None = None,
) -> str:
    """
    Run Writer → Critique → Formatter → Grounding → Save.
    Returns the final formatted document text.
    """
    try:
        request = DocRunRequest(
            mode=mode,
            subject=subject,
            context=context,
            db_path=db_path,
            context_metadata=context_metadata or {},
            coverage_ledger=coverage_ledger or {},
        )
    except ValidationError as exc:
        raise ValueError(f"Invalid documentation pipeline request: {exc}") from exc

    console.print(f"[cyan]Doc Pipeline: {request.mode} / {request.subject}[/cyan]")

    pipeline = _build_pipeline(request.db_path)

    initial: DocAgentState = {
        "mode":             request.mode,
        "subject":          request.subject,
        "context":          request.context,
        "draft":            "",
        "critique_feedback":"",
        "critique_passed":  False,
        "formatted_doc":    "",
        "grounding_passed": True,
        "grounding_feedback":"",
        "context_metadata": request.context_metadata,
        "coverage_ledger":  request.coverage_ledger,
        "iteration":        0,
        "max_iterations":   request.max_iterations,
        "saved":            False,
    }

    final = pipeline.invoke(initial)
    doc   = final.get("formatted_doc") or final.get("draft", "")
    console.print(
        f"[green]Doc Pipeline: done — {final.get('iteration')} iteration(s), "
        f"saved={final.get('saved')}[/green]"
    )
    return doc
