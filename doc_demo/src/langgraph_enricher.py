"""
LangGraph + Groq Enrichment Agent
Enhances parsed COBOL data with business context using LLM.

Feeds actual code context (IF/EVALUATE conditions, CALL targets,
data items, EXEC CICS commands) to the LLM for accurate enrichment.
"""

import os
import json
import re
from typing import TypedDict, List, Dict, Any, Optional
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


# ============================================
# State Definition
# ============================================

class EnrichmentState(TypedDict):
    """State passed through the LangGraph enrichment pipeline."""
    raw_programs: List[Dict]
    raw_copybooks: List[Dict]
    current_program_index: int
    current_program: Optional[Dict]
    enriched_programs: List[Dict]
    enriched_copybooks: List[Dict]
    business_rules: List[Dict]
    errors: List[str]
    total_enriched: int
    rule_counter: int


# ============================================
# Prompts
# ============================================

SYSTEM_PROMPT = """You are a COBOL mainframe business analyst specializing in legacy system documentation.
You translate technical COBOL constructs into clear business language.
Always respond with valid JSON only. No markdown, no explanations outside the JSON."""

PROGRAM_PURPOSE_PROMPT = """Analyze this COBOL program and explain it in plain English for a developer who will migrate it to a modern system. Avoid COBOL jargon — write as if describing a business function.

Program ID: {program_id}
Program Type: {program_type} (ONLINE = CICS 3270 terminal screen program, BATCH = background job run by scheduler)
Line Count: {line_count}

Paragraphs ({para_count} total):
{paragraphs}

Files Used:
{files}

Programs Called:
{calls}

EXEC CICS Commands (if ONLINE):
{cics_commands}

Key Data Items (first 20):
{data_items}

Copybooks Included:
{copybooks}

Respond with JSON:
{{
  "business_name": "Short plain English name (e.g. 'User Sign-On Handler', 'Monthly Statement Generator')",
  "business_purpose": "3-5 sentence description: what triggers this program, what it does step by step, what data it reads/writes, and what it produces. Write for a developer who will rewrite this in Java or Python.",
  "user_role": "Who initiates this (e.g., Customer Service Representative, Batch Scheduler, System Administrator)",
  "business_process": "Which business process this belongs to (e.g., Authentication, Account Management, Transaction Processing, Reporting)"
}}"""

PARAGRAPH_NARRATIVE_PROMPT = """Create plain English narrative descriptions for these COBOL paragraphs. Write for a developer who has never seen COBOL — they need to understand WHAT the paragraph does, WHY, and HOW, so they can rewrite it in a modern language.

Program: {program_id} ({program_purpose})
Program Type: {program_type}

Paragraphs to describe:
{paragraphs_detail}

For each paragraph write:
- business_name: A readable function name (e.g. "Validate User Credentials", "Calculate Interest Charges")
- narrative: A step-by-step description. Start with what triggers this paragraph, then describe each main action in order. Mention what data it reads, what decisions it makes (IF conditions), what it writes or updates, and what it returns or signals. Use plain English, no COBOL jargon. Aim for 4-6 sentences.
- purpose: One sentence on its role in the overall program flow.

Respond with a JSON array:
[
  {{
    "paragraph_name": "original COBOL name",
    "business_name": "Plain English function name",
    "narrative": "Step-by-step plain English description (4-6 sentences)",
    "purpose": "Its role in the overall program flow (1 sentence)"
  }}
]"""

NAME_TRANSLATION_PROMPT = """Translate these COBOL data item names into plain English business terminology.

Program: {program_id}
Context: {context}

Data Items:
{data_items}

Respond with a JSON array:
[
  {{
    "original_name": "WS-ACCT-BAL-AMT",
    "business_name": "Account Balance Amount",
    "description": "Current account balance in dollars and cents",
    "data_type": "Numeric (11 digits, 2 decimal places)"
  }}
]"""

BUSINESS_RULE_PROMPT = """Extract business rules from these conditional statements in a COBOL program.

Program: {program_id} ({program_purpose})
Paragraph: {paragraph_name}

Conditional Statements:
{conditions}

Data Items Referenced:
{data_items_context}

For each meaningful business rule, create:
{{
  "rule_name": "Short descriptive name",
  "rule_statement": "Plain English rule (non-technical)",
  "category": "VALIDATION | CALCULATION | WORKFLOW | COMPLIANCE",
  "condition": "When this rule applies",
  "action": "What happens when rule fires"
}}

Respond with a JSON array of rules. Only extract genuine business rules, skip trivial logic like null checks."""

MIGRATION_PERSPECTIVE_PROMPT = """You are a senior software architect helping migrate a legacy COBOL mainframe application to modern cloud services.

Analyze this COBOL program and provide a migration perspective.

Program ID: {program_id}
Business Name: {business_name}
Business Purpose: {business_purpose}
Program Type: {program_type} (ONLINE = CICS terminal program, BATCH = background job)
Lines of Code: {line_count}
Paragraphs: {para_count}

Files/Databases accessed:
{files}

Programs it calls:
{calls}

Called by:
{called_by}

CICS Commands (if ONLINE):
{cics_commands}

Key data items:
{data_items}

Respond with JSON:
{{
  "migration_complexity": 1-5 integer (1=trivial, 5=very complex),
  "complexity_reason": "One sentence explaining the complexity rating",
  "modern_equivalent": "What modern component replaces this (e.g., REST API endpoint, Kafka consumer, scheduled batch job, database stored procedure)",
  "suggested_service": "Which microservice this belongs to (e.g., account-service, auth-service, transaction-service)",
  "migration_approach": "Step-by-step plain English description of how to migrate this program (3-5 steps)",
  "data_contracts": "What input/output data this program consumes and produces, in plain English",
  "risks": "Key migration risks or things to watch out for",
  "dependencies_to_migrate_first": ["list of program IDs that should be migrated before this one"]
}}"""


# ============================================
# Enricher
# ============================================

class CobolEnricher:
    """LangGraph-based COBOL enrichment agent using Vertex AI LLM."""

    def __init__(self, groq_api_key: str = None, model: str = "gemini-2.5-flash",max_programs: int = 50,vertex_project: str = None, vertex_location: str = "us-central1"):
        model_name = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=os.environ.get("GEMINI_API_KEY"),
            temperature=0.1,
            max_output_tokens=4096,
        )
        self.max_programs = max_programs
        self.graph = self._build_graph()
        console.print(f"[green]OK - Gemini API initialized: {model_name}[/green]")


    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(EnrichmentState)

        workflow.add_node("initialize", self._initialize)
        workflow.add_node("load_program", self._load_program)
        workflow.add_node("infer_purpose", self._infer_purpose)
        workflow.add_node("translate_names", self._translate_names)
        workflow.add_node("generate_narratives", self._generate_narratives)
        workflow.add_node("extract_rules", self._extract_rules)
        workflow.add_node("add_migration_context", self._add_migration_context)
        workflow.add_node("save_and_next", self._save_and_next)
        workflow.add_node("finalize", self._finalize)

        workflow.add_edge(START, "initialize")
        workflow.add_edge("initialize", "load_program")
        workflow.add_edge("load_program", "infer_purpose")
        workflow.add_edge("infer_purpose", "translate_names")
        workflow.add_edge("translate_names", "generate_narratives")
        workflow.add_edge("generate_narratives", "extract_rules")
        workflow.add_edge("extract_rules", "add_migration_context")
        workflow.add_edge("add_migration_context", "save_and_next")

        workflow.add_conditional_edges(
            "save_and_next",
            self._should_continue,
            {"continue": "load_program", "end": "finalize"},
        )
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def _should_continue(self, state: EnrichmentState) -> str:
        if state["current_program_index"] < len(state["raw_programs"]):
            return "continue"
        return "end"

    # ================================================================
    # Nodes
    # ================================================================

    def _initialize(self, state: EnrichmentState) -> dict:
        console.print("[cyan]Starting LLM enrichment pipeline...[/cyan]")
        return {
            "current_program_index": 0,
            "current_program": None,
            "enriched_programs": [],
            "enriched_copybooks": list(state.get("raw_copybooks", [])),
            "business_rules": [],
            "errors": [],
            "total_enriched": 0,
            "rule_counter": 0,
        }

    def _load_program(self, state: EnrichmentState) -> dict:
        idx = state["current_program_index"]
        programs = state["raw_programs"]
        if idx < len(programs):
            prog = programs[idx]
            pid = prog.get("program_id", "UNKNOWN")
            console.print(f"[cyan]  [{idx+1}/{len(programs)}] Enriching: {pid}[/cyan]")
            return {"current_program": prog}
        return {}

    def _infer_purpose(self, state: EnrichmentState) -> dict:
        """Infer business purpose using actual program structure."""
        prog = state.get("current_program")
        if not prog:
            return {}

        try:
            # Build context from actual parsed data
            paragraphs = prog.get("paragraphs", [])
            para_summary = "\n".join(
                f"  - {p.get('name', '?')} (lines {p.get('line_start', '?')}-{p.get('line_end', '?')}, "
                f"{p.get('statement_count', 0)} statements)"
                for p in paragraphs[:15]
            )

            calls = prog.get("calls", [])
            call_summary = "\n".join(
                f"  - CALL '{c.get('called_program', '?')}' at line {c.get('line_number', '?')}"
                for c in calls
            ) or "  None"

            files = prog.get("files", [])
            file_summary = "\n".join(
                f"  - {f.get('file_name', '?')} ({f.get('file_type', '?')}, {f.get('access_mode', '?')})"
                for f in files
            ) or "  None"

            exec_cics = prog.get("exec_cics", [])
            cics_summary = "\n".join(
                f"  - EXEC CICS {c.get('command', '?')}"
                + (f" MAP({c.get('details', {}).get('map', '')})" if c.get('details', {}).get('map') else "")
                + (f" PROGRAM({c.get('details', {}).get('program', '')})" if c.get('details', {}).get('program') else "")
                for c in exec_cics[:10]
            ) or "  None"

            data_items = prog.get("data_items", [])
            di_summary = "\n".join(
                f"  - {d.get('name', '?')} PIC {d.get('picture', '?')} ({d.get('section', '?')})"
                for d in data_items[:20]
                if d.get("name") != "FILLER"
            ) or "  None"

            copybooks = prog.get("copybooks", [])
            cb_summary = ", ".join(copybooks[:10]) or "None"

            prompt = PROGRAM_PURPOSE_PROMPT.format(
                program_id=prog.get("program_id", "UNKNOWN"),
                program_type=prog.get("program_type", "UNKNOWN"),
                line_count=prog.get("line_count", 0),
                para_count=len(paragraphs),
                paragraphs=para_summary,
                files=file_summary,
                calls=call_summary,
                cics_commands=cics_summary,
                data_items=di_summary,
                copybooks=cb_summary,
            )

            response = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ])

            result = self._parse_json(response.content)
            if isinstance(result, dict):
                prog["business_name"] = result.get("business_name", prog.get("program_id"))
                prog["business_purpose"] = result.get("business_purpose", "")
                prog["user_role"] = result.get("user_role", "")
                prog["business_process"] = result.get("business_process", "")

        except Exception as e:
            state.get("errors", []).append(f"Purpose inference failed for {prog.get('program_id')}: {e}")
            console.print(f"[yellow]    Warning: Purpose inference failed: {e}[/yellow]")

        return {"current_program": prog}

    def _translate_names(self, state: EnrichmentState) -> dict:
        """Translate COBOL data item names to business English."""
        prog = state.get("current_program")
        if not prog:
            return {}

        data_items = prog.get("data_items", [])
        if not data_items:
            return {}

        # Process in batches of 25
        batch_size = 25
        translated = []

        for i in range(0, len(data_items), batch_size):
            batch = data_items[i:i + batch_size]
            # Skip FILLER entries
            meaningful = [d for d in batch if d.get("name") != "FILLER"]

            if not meaningful:
                translated.extend(batch)
                continue

            try:
                di_text = "\n".join(
                    f"  - {d.get('name')} (Level {d.get('level_number', '?')}, "
                    f"PIC {d.get('picture', '?')}, Section: {d.get('section', '?')})"
                    for d in meaningful
                )

                prompt = NAME_TRANSLATION_PROMPT.format(
                    program_id=prog.get("program_id", "UNKNOWN"),
                    context=prog.get("business_purpose", "business processing"),
                    data_items=di_text,
                )

                response = self.llm.invoke([
                    SystemMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=prompt),
                ])

                translations = self._parse_json(response.content)
                if isinstance(translations, list):
                    trans_map = {}
                    for t in translations:
                        orig = t.get("original_name", "")
                        trans_map[orig] = t

                    for d in batch:
                        t = trans_map.get(d.get("name"), {})
                        d["business_name"] = t.get("business_name", d.get("business_name"))
                        d["description"] = t.get("description", d.get("description"))
                        d["data_type_description"] = t.get("data_type", d.get("data_type_description"))
                        translated.append(d)
                else:
                    translated.extend(batch)

            except Exception as e:
                console.print(f"[yellow]    Warning: Name translation batch failed: {e}[/yellow]")
                translated.extend(batch)

        prog["data_items"] = translated
        return {"current_program": prog}

    def _generate_narratives(self, state: EnrichmentState) -> dict:
        """Generate narrative descriptions using actual statement data."""
        prog = state.get("current_program")
        if not prog:
            return {}

        paragraphs = prog.get("paragraphs", [])
        if not paragraphs:
            return {}

        # Process up to 10 paragraphs at a time
        batch_size = 10
        for i in range(0, min(len(paragraphs), 20), batch_size):
            batch = paragraphs[i:i + batch_size]

            try:
                para_details = []
                for p in batch:
                    stmts = p.get("statements", [])
                    stmt_types = [s.get("type", "?") for s in stmts]
                    stmt_summary = ", ".join(f"{t}({stmt_types.count(t)})" for t in set(stmt_types)) if stmt_types else "None"

                    calls_in_para = [c.get("called_program", "?") for c in p.get("calls", [])]
                    performs_in_para = [pf.get("target_paragraph", "?") for pf in p.get("performs", [])]
                    cics_in_para = [c.get("command", "?") for c in p.get("exec_cics", [])]

                    detail = (
                        f"Paragraph: {p.get('name', '?')}\n"
                        f"  Lines: {p.get('line_start', '?')}-{p.get('line_end', '?')}\n"
                        f"  Statement types: {stmt_summary}\n"
                        f"  CALL targets: {', '.join(calls_in_para) or 'None'}\n"
                        f"  PERFORM targets: {', '.join(performs_in_para) or 'None'}\n"
                        f"  CICS commands: {', '.join(cics_in_para) or 'None'}"
                    )
                    para_details.append(detail)

                prompt = PARAGRAPH_NARRATIVE_PROMPT.format(
                    program_id=prog.get("program_id", "UNKNOWN"),
                    program_purpose=prog.get("business_purpose", "business processing"),
                    program_type=prog.get("program_type", "UNKNOWN"),
                    paragraphs_detail="\n\n".join(para_details),
                )

                response = self.llm.invoke([
                    SystemMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=prompt),
                ])

                narratives = self._parse_json(response.content)
                if isinstance(narratives, list):
                    narr_map = {n.get("paragraph_name", ""): n for n in narratives}
                    for p in batch:
                        n = narr_map.get(p.get("name"), {})
                        p["business_name"] = n.get("business_name", p.get("business_name"))
                        p["narrative"] = n.get("narrative", p.get("narrative"))
                        p["purpose"] = n.get("purpose", p.get("purpose"))

            except Exception as e:
                console.print(f"[yellow]    Warning: Narrative generation failed: {e}[/yellow]")

        prog["paragraphs"] = paragraphs
        return {"current_program": prog}

    def _extract_rules(self, state: EnrichmentState) -> dict:
        """Extract business rules from actual IF/EVALUATE statements."""
        prog = state.get("current_program")
        if not prog:
            return {}

        program_id = prog.get("program_id", "UNKNOWN")
        new_rules = []
        rule_counter = state.get("rule_counter", 0)

        # Collect IF and EVALUATE statements with actual conditions
        statements = prog.get("statements", [])
        conditionals = [s for s in statements if s.get("type") in ("IF", "EVALUATE")]

        if not conditionals:
            return {"business_rules": state.get("business_rules", []) + new_rules}

        # Group by paragraph
        by_para = {}
        for s in conditionals:
            para = s.get("paragraph", "UNKNOWN")
            if para not in by_para:
                by_para[para] = []
            by_para[para].append(s)

        # Process each paragraph's conditions
        for para_name, conds in by_para.items():
            if not conds:
                continue

            try:
                cond_text = "\n".join(
                    f"  - {c.get('type')} at line {c.get('line', '?')}: "
                    f"{c.get('condition', c.get('subject', ''))}"
                    + (f"\n    Branches: {', '.join(c.get('whens', [])[:5])}" if c.get('whens') else "")
                    for c in conds[:8]
                )

                # Gather data items in this paragraph for context
                para_data = prog.get("paragraphs", [])
                di_context = ""
                for p in para_data:
                    if p.get("name") == para_name:
                        stmt_list = p.get("statements", [])
                        # Get MOVE targets and sources as context
                        moves = [s for s in stmt_list if s.get("type") == "MOVE"]
                        if moves:
                            di_context = "\n".join(
                                f"  - MOVE {m.get('source', '?')} TO {m.get('destination', '?')}"
                                for m in moves[:5]
                            )
                        break

                if not di_context:
                    di_context = "  (no additional data context)"

                prompt = BUSINESS_RULE_PROMPT.format(
                    program_id=program_id,
                    program_purpose=prog.get("business_purpose", "business processing"),
                    paragraph_name=para_name,
                    conditions=cond_text,
                    data_items_context=di_context,
                )

                response = self.llm.invoke([
                    SystemMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=prompt),
                ])

                rules = self._parse_json(response.content)
                if isinstance(rules, dict):
                    rules = [rules]
                if isinstance(rules, list):
                    for r in rules:
                        rule_counter += 1
                        r["rule_id"] = r.get("rule_id", f"BR-{rule_counter:03d}")
                        r["program_id"] = program_id
                        r["paragraph_name"] = para_name
                        # Find line numbers from the condition
                        if conds:
                            r["line_start"] = conds[0].get("line", 0)
                            r["line_end"] = conds[-1].get("line_end", conds[-1].get("line", 0))
                        new_rules.append(r)

            except Exception as e:
                console.print(f"[yellow]    Warning: Rule extraction failed for {para_name}: {e}[/yellow]")

        existing_rules = state.get("business_rules", [])
        return {
            "business_rules": existing_rules + new_rules,
            "rule_counter": rule_counter,
        }

    def _add_migration_context(self, state: EnrichmentState) -> dict:
        """Generate migration perspective for the current program."""
        prog = state.get("current_program")
        if not prog:
            return {}

        try:
            paragraphs = prog.get("paragraphs", [])
            calls      = prog.get("calls", [])
            called_by  = prog.get("called_by", [])
            files      = prog.get("files", [])
            exec_cics  = prog.get("exec_cics", [])
            data_items = prog.get("data_items", [])

            files_text = "\n".join(
                f"  - {f.get('file_name','?')} ({f.get('file_type','?')}, {f.get('access_mode','?')})"
                for f in files
            ) or "  None"

            calls_text = "\n".join(
                f"  - {c.get('called_program','?')}"
                for c in calls
            ) or "  None"

            called_by_text = "\n".join(
                f"  - {c.get('caller_program','?')}"
                for c in (called_by or [])[:10]
            ) or "  None"

            cics_text = "\n".join(
                f"  - EXEC CICS {c.get('command','?')}"
                for c in exec_cics[:8]
            ) or "  None"

            di_text = "\n".join(
                f"  - {d.get('name','?')} ({d.get('business_name') or d.get('picture','?')})"
                for d in data_items[:15]
                if d.get("name") != "FILLER"
            ) or "  None"

            prompt = MIGRATION_PERSPECTIVE_PROMPT.format(
                program_id=prog.get("program_id", "UNKNOWN"),
                business_name=prog.get("business_name", ""),
                business_purpose=prog.get("business_purpose", ""),
                program_type=prog.get("program_type", "UNKNOWN"),
                line_count=prog.get("line_count", 0),
                para_count=len(paragraphs),
                files=files_text,
                calls=calls_text,
                called_by=called_by_text,
                cics_commands=cics_text,
                data_items=di_text,
            )

            response = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ])

            result = self._parse_json(response.content)
            if isinstance(result, dict):
                prog["migration_complexity"]  = result.get("migration_complexity", 0)
                prog["complexity_reason"]     = result.get("complexity_reason", "")
                prog["modern_equivalent"]     = result.get("modern_equivalent", "")
                prog["suggested_service"]     = result.get("suggested_service", "")
                prog["migration_approach"]    = result.get("migration_approach", "")
                prog["data_contracts"]        = result.get("data_contracts", "")
                prog["migration_risks"]       = result.get("risks", "")
                prog["dependencies_to_migrate_first"] = result.get("dependencies_to_migrate_first", [])

        except Exception as e:
            console.print(f"[yellow]    Warning: Migration context failed for {prog.get('program_id')}: {e}[/yellow]")

        return {"current_program": prog}

    def _save_and_next(self, state: EnrichmentState) -> dict:
        prog = state.get("current_program")
        enriched = list(state.get("enriched_programs", []))
        if prog:
            enriched.append(prog)

        idx = state["current_program_index"] + 1
        console.print(f"[green]    OK - Enriched ({idx}/{len(state['raw_programs'])})[/green]")

        return {
            "enriched_programs": enriched,
            "current_program_index": idx,
            "current_program": None,
            "total_enriched": len(enriched),
        }

    def _finalize(self, state: EnrichmentState) -> dict:
        total = state.get("total_enriched", 0)
        rules = len(state.get("business_rules", []))
        errors = len(state.get("errors", []))
        console.print(f"[green]OK - Enrichment complete: {total} programs, {rules} rules, {errors} errors[/green]")
        return {}

    # ================================================================
    # Helpers
    # ================================================================

    @staticmethod
    def _parse_json(content: str) -> Any:
        """Parse JSON from LLM response, handling markdown code blocks."""
        content = content.strip()

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                content = parts[1]

        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            # Try finding embedded JSON
            for pattern in [r'\[[\s\S]*\]', r'\{[\s\S]*\}']:
                m = re.search(pattern, content)
                if m:
                    try:
                        return json.loads(m.group())
                    except:
                        continue
            return {}

    # ================================================================
    # Public API
    # ================================================================

    def enrich(self, programs: List[Dict], copybooks: List[Dict] = None) -> Dict[str, Any]:
        """Run enrichment pipeline on parsed COBOL data."""
        # Limit programs for API budget
        limited = programs[:self.max_programs]
        console.print(f"[cyan]Enriching {len(limited)} of {len(programs)} programs...[/cyan]")

        initial_state: EnrichmentState = {
            "raw_programs": limited,
            "raw_copybooks": copybooks or [],
            "current_program_index": 0,
            "current_program": None,
            "enriched_programs": [],
            "enriched_copybooks": [],
            "business_rules": [],
            "errors": [],
            "total_enriched": 0,
            "rule_counter": 0,
        }

        final = self.graph.invoke(initial_state)

        # Merge enriched with any unenriched programs
        enriched_ids = {p.get("program_id") for p in final["enriched_programs"]}
        remaining = [p for p in programs if p.get("program_id") not in enriched_ids]

        return {
            "programs": final["enriched_programs"] + remaining,
            "copybooks": final.get("enriched_copybooks", copybooks or []),
            "business_rules": final["business_rules"],
            "errors": final.get("errors", []),
        }

    def enrich_from_file(self, programs_json: str, copybooks_json: str = None) -> Dict[str, Any]:
        """Load parsed JSON and run enrichment."""
        with open(programs_json, "r") as f:
            programs = json.load(f)

        # Deduplicate by program_id — keep the entry with more content (more paragraphs)
        seen: Dict[str, Dict] = {}
        for p in programs:
            pid = p.get("program_id", "")
            if pid not in seen or len(p.get("paragraphs", [])) > len(seen[pid].get("paragraphs", [])):
                seen[pid] = p
        programs = list(seen.values())
        console.print(f"[cyan]Deduped to {len(programs)} unique programs[/cyan]")

        copybooks = []
        if copybooks_json and Path(copybooks_json).exists():
            with open(copybooks_json, "r") as f:
                copybooks = json.load(f)

        return self.enrich(programs, copybooks)

    def save_results(self, results: Dict, output_dir: str):
        """Save enriched results to JSON files."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        with open(out / "enriched_programs.json", "w") as f:
            json.dump(results["programs"], f, indent=2, default=str)

        with open(out / "business_rules.json", "w") as f:
            json.dump(results["business_rules"], f, indent=2, default=str)

        if results.get("errors"):
            with open(out / "enrichment_errors.json", "w") as f:
                json.dump(results["errors"], f, indent=2)

        console.print(f"[green]OK - Saved enriched results to {out}[/green]")


# ============================================
# CLI
# ============================================

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description="Enrich parsed COBOL with Groq LLM")
    parser.add_argument("programs_json", help="Path to programs.json")
    parser.add_argument("--copybooks", help="Path to copybooks.json")
    parser.add_argument("--output", "-o", default="enriched_output")
    parser.add_argument("--api-key", help="Groq API key (or GROQ_API_KEY env)")
    parser.add_argument("--model", default="llama-3.3-70b-versatile")
    parser.add_argument("--max-programs", type=int, default=50,
                        help="Max programs to enrich (API budget)")

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[red]Error: Groq API key required. Set GROQ_API_KEY or use --api-key[/red]")
        exit(1)

    enricher = CobolEnricher(groq_api_key=api_key, model=args.model,
                              max_programs=args.max_programs)
    results = enricher.enrich_from_file(args.programs_json, args.copybooks)
    enricher.save_results(results, args.output)
