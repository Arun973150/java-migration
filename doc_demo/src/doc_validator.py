"""
Documentation Validator
Runs three validation checks against the generated docs:

  1. Structural — every program has a doc, required sections present, links resolve
  2. Factual    — every program ID / copybook / paragraph / line in docs exists in SQLite
  3. Coverage   — every CALL / COPY / CICS XCTL / JCL EXEC in source appears in the doc

Usage (standalone):
    python -m src.doc_validator --db data/cobol_knowledge.db --docs docs/

Usage (programmatic):
    from doc_validator import validate_docs
    report = validate_docs(db_path, docs_dir)
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from rich.console import Console
from rich.table import Table

console = Console(force_terminal=True, highlight=False, legacy_windows=False)

REQUIRED_PROGRAM_SECTIONS = [
    "## Business Purpose",
    "## Dependency Context",
    "## Statement Profile",
    "## Control Flow",
    "## Paragraphs",
]


@dataclass
class ValidationReport:
    structural_errors: List[str] = field(default_factory=list)
    structural_warnings: List[str] = field(default_factory=list)
    factual_errors: List[str] = field(default_factory=list)
    coverage_gaps: List[str] = field(default_factory=list)
    prompt_coverage_warnings: List[str] = field(default_factory=list)
    citation_errors: List[str] = field(default_factory=list)
    citation_warnings: List[str] = field(default_factory=list)
    stats: Dict[str, object] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not (self.structural_errors or self.factual_errors
                    or self.coverage_gaps or self.citation_errors)

    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "stats": self.stats,
            "structural_errors": self.structural_errors,
            "structural_warnings": self.structural_warnings,
            "factual_errors": self.factual_errors,
            "coverage_gaps": self.coverage_gaps,
            "prompt_coverage_warnings": self.prompt_coverage_warnings,
            "citation_errors": self.citation_errors,
            "citation_warnings": self.citation_warnings,
        }


# ───────────────────────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────────────────────

def _load_sqlite_facts(db_path: str) -> Dict[str, Set[str]]:
    """Pull ground-truth identifiers from SQLite for the factual check."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    facts: Dict[str, Set[str]] = {
        "programs": set(),
        "copybooks": set(),
        "paragraphs": set(),         # plain paragraph names
        "screens": set(),
        "jcl_jobs": set(),
        "modules": set(),
        "business_rules": set(),
        "data_items": set(),
        "files": set(),
    }

    cur.execute("SELECT program_id FROM programs")
    facts["programs"] = {r["program_id"] for r in cur.fetchall()}

    cur.execute("SELECT copybook_name FROM copybooks")
    facts["copybooks"] = {r["copybook_name"] for r in cur.fetchall()}

    cur.execute("SELECT paragraph_name FROM paragraphs")
    facts["paragraphs"] = {r["paragraph_name"] for r in cur.fetchall()}

    try:
        cur.execute("SELECT screen_name, map_name, mapset_name FROM screens")
        for r in cur.fetchall():
            for v in (r["screen_name"], r["map_name"], r["mapset_name"]):
                if v:
                    facts["screens"].add(v)
    except Exception:
        pass

    try:
        cur.execute("SELECT job_name FROM jcl_jobs")
        facts["jcl_jobs"] = {r["job_name"] for r in cur.fetchall()}
    except Exception:
        pass

    try:
        cur.execute("SELECT DISTINCT step_name FROM jcl_steps")
        for r in cur.fetchall():
            if r["step_name"]:
                facts["jcl_jobs"].add(r["step_name"])
    except Exception:
        pass

    cur.execute("SELECT module_name FROM modules")
    facts["modules"] = {r["module_name"] for r in cur.fetchall()}

    try:
        cur.execute("SELECT rule_id FROM business_rules")
        facts["business_rules"] = {r["rule_id"] for r in cur.fetchall() if r["rule_id"]}
    except Exception:
        pass

    cur.execute("SELECT DISTINCT name FROM data_items")
    facts["data_items"] = {r["name"] for r in cur.fetchall() if r["name"]}

    # Add copybook field names, FD record fields, and MOVE-touched fields
    # so the factual check doesn't flag valid extracted identifiers.
    try:
        cur.execute("SELECT DISTINCT field_name FROM copybook_fields")
        for r in cur.fetchall():
            if r["field_name"]:
                facts["data_items"].add(r["field_name"])
    except Exception:
        pass
    try:
        cur.execute("SELECT DISTINCT field_name FROM file_records UNION SELECT DISTINCT record_name FROM file_records UNION SELECT DISTINCT file_name FROM file_records")
        for r in cur.fetchall():
            if r[0]:
                facts["data_items"].add(r[0])
    except Exception:
        pass
    try:
        cur.execute("SELECT DISTINCT source_field FROM data_movements UNION SELECT DISTINCT destination_field FROM data_movements")
        for r in cur.fetchall():
            if r[0]:
                facts["data_items"].add(r[0])
    except Exception:
        pass

    # Source-file scan: pull every COBOL data declaration and every identifier
    # that is the target of a MOVE / IF / READ / WRITE / SET clause. Catches
    # working-storage fields that ProLeap missed (e.g. WS-PFK-FLAG).
    try:
        cur.execute("SELECT DISTINCT file_path FROM programs WHERE file_path IS NOT NULL")
        prog_paths = [r["file_path"] for r in cur.fetchall()]
    except Exception:
        prog_paths = []

    decl_re = re.compile(
        r"^\s*\d{2}\s+([A-Z][A-Z0-9-]{1,30})(?:\s+|\.)",
        re.IGNORECASE | re.MULTILINE,
    )
    move_to_re = re.compile(
        r"\b(?:MOVE\s+\S+\s+TO|TO|INTO|FROM|RIDFLD|MAP|MAPSET|PROGRAM|FILE|DATASET|TRANSID|"
        r"COMMAREA|LENGTH|RESP|CURSOR)\s*\(?\s*([A-Z][A-Z0-9-]{2,30})",
        re.IGNORECASE,
    )

    # Also scan all .cpy/.CPY files (catches copybook fields that aren't in data_items)
    try:
        cur.execute("SELECT DISTINCT file_path FROM copybooks WHERE file_path IS NOT NULL")
        prog_paths += [r["file_path"] for r in cur.fetchall() if r["file_path"]]
    except Exception:
        pass

    for fp in prog_paths:
        try:
            from pathlib import Path as _P
            p = _P(fp)
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            # Strip column 1-6 sequence area + column 73-80 area + comments
            cleaned = []
            for line in text.split("\n"):
                if len(line) > 6 and line[6] == "*":
                    continue
                body = line[6:] if len(line) > 6 else line
                cleaned.append(body[:66] if len(body) > 66 else body)
            joined = "\n".join(cleaned)
            for m in decl_re.finditer(joined):
                facts["data_items"].add(m.group(1).upper())
            for m in move_to_re.finditer(joined):
                facts["data_items"].add(m.group(1).upper())
        except Exception:
            continue

    try:
        cur.execute("SELECT DISTINCT file_name FROM files")
        facts["files"] = {r["file_name"] for r in cur.fetchall() if r["file_name"]}
    except Exception:
        pass

    try:
        cur.execute("SELECT file_path FROM programs WHERE file_path IS NOT NULL")
        for r in cur.fetchall():
            path = Path(r["file_path"] or "")
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"\bWS-PGMNAME\b[\s\S]{0,90}?\bVALUE\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
            if m:
                facts["data_items"].add(m.group(1))
    except Exception:
        pass

    conn.close()
    return facts


def _load_expected_relations(db_path: str) -> Dict[str, Dict[str, Set[str]]]:
    """For coverage check: what each program SHOULD reference."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    relations: Dict[str, Dict[str, Set[str]]] = {}

    cur.execute("SELECT program_id, file_path FROM programs")
    program_paths = {}
    for r in cur.fetchall():
        relations[r["program_id"]] = {
            "calls": set(),
            "copybooks": set(),
            "cics_xctl": set(),
            "jcl_jobs": set(),
            "source_copybooks": set(),
            "ims_functions": set(),
        }
        if r["file_path"]:
            program_paths[r["program_id"]] = r["file_path"]

    cur.execute("SELECT caller_program, called_program FROM program_calls")
    for r in cur.fetchall():
        if r["caller_program"] in relations and r["called_program"] not in (None, "UNKNOWN"):
            relations[r["caller_program"]]["calls"].add(r["called_program"])

    cur.execute("SELECT program_id, copybook_name FROM copybook_usage")
    for r in cur.fetchall():
        if r["program_id"] in relations:
            relations[r["program_id"]]["copybooks"].add(r["copybook_name"])

    try:
        cur.execute("SELECT program_id, command, details_json FROM exec_cics WHERE command IN ('XCTL','LINK')")
        for r in cur.fetchall():
            if r["program_id"] not in relations:
                continue
            try:
                d = json.loads(r["details_json"] or "{}")
                inner = d.get("details", d) or {}
                target = inner.get("program")
                if target:
                    relations[r["program_id"]]["cics_xctl"].add(target)
            except Exception:
                pass
    except Exception:
        pass

    try:
        cur.execute("SELECT program, job_name FROM jcl_steps WHERE program IS NOT NULL")
        for r in cur.fetchall():
            if r["program"] in relations:
                relations[r["program"]]["jcl_jobs"].add(r["job_name"])
    except Exception:
        pass

    # Read source files to extract expected COPY and IMS references
    import re
    copy_pat = re.compile(r"COPY\s+([A-Z0-9_-]+)", re.IGNORECASE)
    ims_pat = re.compile(r"CALL\s+['\"]CBLTDLI['\"]\s+USING\s+['\"]?([A-Z0-9]+)['\"]?", re.IGNORECASE)
    
    for pid, fpath in program_paths.items():
        src = Path(fpath)
        if not src.exists():
            continue
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
            # Strip sequence areas
            lines = content.split("\n")
            cleaned_lines = []
            for l in lines:
                if len(l) > 6 and l[6] == "*":
                    continue
                body = l[6:] if len(l) > 6 else l
                cleaned_lines.append(body[:66] if len(body) > 66 else body)
            cleaned_content = " ".join(cleaned_lines)
            
            # Find standalone COPY words followed by something
            for m in re.finditer(r"\bCOPY\s+([A-Z0-9_-]+)", cleaned_content, re.IGNORECASE):
                cb_name = m.group(1).upper()
                if cb_name not in ("REPLACING", "PERFORM", "MOVE", "ADD", "COMPUTE"):
                    relations[pid]["source_copybooks"].add(cb_name)
                
            for m in ims_pat.finditer(cleaned_content):
                fn_code = m.group(1).upper()
                if fn_code.startswith("FUNC-"):
                    fn_code = fn_code[5:]
                if fn_code not in ("BY", "REFERENCE", "CONTENT", "VALUE"):
                    relations[pid]["ims_functions"].add(fn_code)
        except Exception:
            pass

    conn.close()
    return relations


# ───────────────────────────────────────────────────────────────────────────────
# Check 1: Structural
# ───────────────────────────────────────────────────────────────────────────────

def _check_structural(facts: Dict[str, Set[str]], docs_dir: Path,
                       report: ValidationReport) -> None:
    programs_dir = docs_dir / "programs"

    # Every program must have a doc file
    missing_docs = []
    for pid in facts["programs"]:
        doc = programs_dir / f"{pid}.md"
        if not doc.exists():
            missing_docs.append(pid)
    if missing_docs:
        report.structural_errors.append(
            f"Missing program docs ({len(missing_docs)}): {', '.join(sorted(missing_docs)[:10])}"
            + ("..." if len(missing_docs) > 10 else "")
        )

    # Required sections present + non-empty
    empty_section_count = 0
    missing_section_count = 0
    for pid in facts["programs"]:
        doc = programs_dir / f"{pid}.md"
        if not doc.exists():
            continue
        content = doc.read_text(encoding="utf-8", errors="ignore")
        for section in REQUIRED_PROGRAM_SECTIONS:
            if section not in content:
                report.structural_warnings.append(f"{pid}: missing section '{section}'")
                missing_section_count += 1
                continue
            # Check the section has at least 30 chars of content after its heading
            idx = content.find(section)
            tail = content[idx + len(section): idx + len(section) + 200]
            if len(tail.strip()) < 30:
                report.structural_warnings.append(f"{pid}: section '{section}' appears empty")
                empty_section_count += 1

    # Internal markdown links resolve
    broken_links = 0
    link_pat = re.compile(r"\]\(([^)]+\.md)(?:#[^)]*)?\)")
    for md_file in docs_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in link_pat.finditer(content):
            link = m.group(1)
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            target = (md_file.parent / link).resolve()
            if not target.exists():
                broken_links += 1
                if broken_links <= 20:  # cap noise
                    report.structural_warnings.append(
                        f"Broken link in {md_file.relative_to(docs_dir)}: -> {link}"
                    )

    report.stats["program_docs_expected"] = len(facts["programs"])
    report.stats["program_docs_missing"] = len(missing_docs)
    report.stats["empty_sections"] = empty_section_count
    report.stats["missing_sections"] = missing_section_count
    report.stats["broken_links"] = broken_links


# ───────────────────────────────────────────────────────────────────────────────
# Check 2: Factual cross-check
# ───────────────────────────────────────────────────────────────────────────────

# Identifier pattern: allow upper/digit + dash, 3-12 chars (typical COBOL names)
ID_PAT = re.compile(r"`([A-Z][A-Z0-9-]{2,11})`")

# Skip these common false positives — keywords that look like identifiers
NOISE = {
    # COBOL keywords
    "COBOL", "CICS", "JCL", "BMS", "VSAM", "SQL", "DB2", "IMS", "ONLINE", "BATCH",
    "MAIN", "ENTRY", "EXIT", "END", "TRUE", "FALSE", "NULL", "UNKNOWN",
    "INPUT", "OUTPUT", "READ", "WRITE", "OPEN", "CLOSE", "CALL", "PERFORM",
    "MOVE", "IF", "ELSE", "EVALUATE", "WHEN", "GOTO", "STOP", "GOBACK",
    "WORKING-STORAGE", "LINKAGE", "FILE",
    # CICS commands
    "SEND", "RECEIVE", "XCTL", "LINK", "RETURN", "ASKTIME", "SYNCPOINT",
    "FORMATTIME", "STARTBR", "READNEXT", "READPREV", "ENDBR", "REWRITE", "DELETE",
    "HANDLE", "ASSIGN", "INQUIRE", "WRITEQ", "READQ", "DELETEQ", "ABEND",
    "RETRIEVE", "ENQ", "DEQ", "CONVERSE", "ISSUE", "SUSPEND", "RESUME",
    # External MQ runtime routines used as CALL targets, not local COBOL program IDs
    "MQOPEN", "MQGET", "MQPUT", "MQPUT1", "MQCLOSE",
    # SQL/DB2 keywords
    "SELECT", "INSERT", "UPDATE", "DECLARE", "FETCH", "COMMIT", "ROLLBACK",
    "INCLUDE", "BEGIN", "EXEC", "WHENEVER", "MERGE",
    # IMS DL/I functions
    "GU", "GHN", "GHU", "GN", "GNP", "GHNP", "ISRT", "REPL", "DLET", "CHKP",
    "XRST", "STAT", "TERM", "PCB", "SYNC", "LOG", "GMSG", "ICMD",
    # Common report/util tokens
    "XXXX", "XXX", "TBD", "TODO", "FIXME",
    # Logical operators / quantifiers
    "AND", "OR", "NOT", "TRUE", "FALSE", "ANY", "ALL", "EACH", "EVERY",
    # COBOL data types / report headers / SQL types
    "BIGINT", "INTEGER", "INT", "SMALLINT", "DECIMAL", "DEC", "NUMERIC",
    "VARCHAR", "CHAR", "DATE", "TIME", "TIMESTAMP", "FLOAT", "DOUBLE",
    "GROUP", "ELEMENTARY", "OBJECT", "FIELD", "RECORD", "LEVEL", "PARENT",
    "END-IF", "END-EVALUATE", "END-PERFORM", "END-READ", "END-WRITE",
    "END-CALL", "END-SEARCH", "END-START", "END-STRING", "END-UNSTRING",
    "END-COMPUTE", "END-ADD", "END-SUBTRACT", "END-MULTIPLY", "END-DIVIDE",
    "PIC", "PICTURE", "USAGE", "VALUE", "OCCURS", "REDEFINES", "FILLER",
    "JCL_JOB", "JCL_STEP", "DD", "DSN", "LRECL", "RECFM", "DISP", "SPACE", "UNIT",
    # CICS HANDLE clauses + system fields (EIB*)
    "CANCEL", "LABEL", "PROGRAM", "RESET", "PUSH", "POP", "SUSPEND",
    "EIBAID", "EIBCALEN", "EIBRESP", "EIBRESP2", "EIBFN", "EIBRCODE",
    "EIBTRNID", "EIBTRMID", "EIBSYSID", "EIBDATE", "EIBTIME", "EIBTASKN",
    # MQ standard completion codes / reason codes
    "MQCC-OK", "MQCC-WARNING", "MQCC-FAILED",
    "MQRC-NONE", "MQRC-NO-MSG-AVAILABLE", "MQRC-Q-FULL",
    "MQOO-INPUT-AS-Q-DEF", "MQOO-OUTPUT", "MQOO-BROWSE",
    "MQGMO-WAIT", "MQGMO-NO-WAIT", "MQPMO-NO-SYNCPOINT", "MQPMO-SYNCPOINT",
    # IMS PSB / DBD identifiers (often referenced generically)
    "PSB-NAME", "DBD-NAME", "DBA", "PCB", "AIB",
}


def _check_factual(facts: Dict[str, Set[str]], docs_dir: Path,
                    report: ValidationReport) -> None:
    programs_dir = docs_dir / "programs"
    if not programs_dir.exists():
        return

    known_ids = (
        facts["programs"]
        | facts["copybooks"]
        | facts["modules"]
        | facts["jcl_jobs"]
        | facts["screens"]
        | facts["business_rules"]
        | facts["data_items"]
        | facts["paragraphs"]
        | facts["files"]
    )

    unknown_refs: Dict[str, Set[str]] = {}  # doc_file -> set of unknown identifiers

    for doc in programs_dir.glob("*.md"):
        content = doc.read_text(encoding="utf-8", errors="ignore")
        for m in ID_PAT.finditer(content):
            ident = m.group(1)
            if ident in NOISE or ident in known_ids:
                continue
            # Strip trailing dash artifacts and re-test
            cleaned = ident.rstrip("-")
            if cleaned in known_ids or cleaned in NOISE:
                continue
            unknown_refs.setdefault(doc.stem, set()).add(ident)

    bad_count = sum(len(v) for v in unknown_refs.values())
    if bad_count:
        # Report top offenders
        for doc_stem, refs in list(unknown_refs.items())[:15]:
            sample = sorted(refs)[:8]
            report.factual_errors.append(
                f"{doc_stem}.md references unknown identifiers: {', '.join(sample)}"
                + (f" (+{len(refs) - 8} more)" if len(refs) > 8 else "")
            )

    report.stats["unknown_identifier_refs"] = bad_count


# ───────────────────────────────────────────────────────────────────────────────
# Check 3: Coverage
# ───────────────────────────────────────────────────────────────────────────────

def _check_coverage(relations: Dict[str, Dict[str, Set[str]]], docs_dir: Path,
                     report: ValidationReport) -> None:
    programs_dir = docs_dir / "programs"
    if not programs_dir.exists():
        return

    total_expected = 0
    total_missing = 0

    for pid, expected in relations.items():
        doc = programs_dir / f"{pid}.md"
        if not doc.exists():
            continue  # missing doc already flagged in structural check
        content = doc.read_text(encoding="utf-8", errors="ignore")

        # Each expected reference: just check substring presence
        for kind, ids in expected.items():
            for ident in ids:
                total_expected += 1
                if ident not in content:
                    total_missing += 1
                    report.coverage_gaps.append(
                        f"{pid}.md does not reference {kind}: {ident}"
                    )

    report.stats["coverage_expected_refs"] = total_expected
    report.stats["coverage_missing_refs"] = total_missing


def _check_prompt_coverage(db_path: str, report: ValidationReport) -> None:
    """Inspect saved prompt / document coverage ledgers when available."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        cur.execute("SELECT mode, subject, coverage_ledger_json FROM generated_docs")
    except Exception:
        conn.close()
        return

    docs_checked = 0
    expected_total = 0
    prompt_total = 0
    document_total = 0

    for row in cur.fetchall():
        raw = row["coverage_ledger_json"]
        if not raw:
            continue
        try:
            ledger = json.loads(raw)
        except Exception:
            continue

        docs_checked += 1
        expected = int(ledger.get("expected_count", 0) or 0)
        prompt = int(ledger.get("prompt_count", 0) or 0)
        document = int(ledger.get("document_count", 0) or 0)
        expected_total += expected
        prompt_total += prompt
        document_total += document

        prompt_missing = ledger.get("prompt_missing_fact_ids") or []
        doc_missing = ledger.get("document_missing_fact_ids") or []
        if prompt_missing:
            report.prompt_coverage_warnings.append(
                f"{row['mode']} / {row['subject']}: {len(prompt_missing)} fact(s) omitted from prompt assembly"
            )
        if doc_missing:
            report.prompt_coverage_warnings.append(
                f"{row['mode']} / {row['subject']}: {len(doc_missing)} fact(s) still not referenced in generated document"
            )

    conn.close()
    report.stats["prompt_ledgers_checked"] = docs_checked
    report.stats["prompt_expected_facts"] = expected_total
    report.stats["prompt_facts_in_context"] = prompt_total
    report.stats["prompt_facts_in_document"] = document_total


# ───────────────────────────────────────────────────────────────────────────────
# Check 4: Paragraph citation check (LLM-generated docs only)
# ───────────────────────────────────────────────────────────────────────────────

# Match `PARAGRAPH-NAME` style: backticks, uppercase + digits + dash, 5-40 chars,
# must contain at least one dash so we don't match plain words.
PARA_CITE_PAT = re.compile(r"`([A-Z][A-Z0-9]{2,}-[A-Z0-9-]{2,30})`")

MIN_CITATIONS = {"Program": 3, "Module": 2, "Application": 0}


def _check_citations(db_path: str, report: ValidationReport) -> None:
    """For LLM-generated docs in generated_docs table:
       (a) every cited paragraph must exist in the paragraphs table for the relevant program;
       (b) Program-mode docs must cite >= 3 paragraphs from the subject program."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Skip if the cache table doesn't exist yet (no agentic docs generated)
    try:
        cur.execute("SELECT mode, subject, document_text FROM generated_docs")
        rows = cur.fetchall()
    except Exception:
        report.stats["citations_docs_checked"] = 0
        report.stats["citations_invalid"] = 0
        report.stats["citations_below_min"] = 0
        conn.close()
        return

    if not rows:
        report.stats["citations_docs_checked"] = 0
        report.stats["citations_invalid"] = 0
        report.stats["citations_below_min"] = 0
        conn.close()
        return

    # Pull paragraphs grouped by program for fast lookup
    cur.execute("SELECT program_id, paragraph_name FROM paragraphs")
    paras_by_program: Dict[str, Set[str]] = {}
    for r in cur.fetchall():
        paras_by_program.setdefault(r["program_id"], set()).add(r["paragraph_name"])
    all_paragraphs: Set[str] = {p for ps in paras_by_program.values() for p in ps}

    # Backticks are also used for data items/copybooks in generated docs. Do not
    # misclassify those grounded identifiers as hallucinated paragraph citations.
    cur.execute("SELECT DISTINCT name FROM data_items WHERE name IS NOT NULL")
    all_data_items: Set[str] = {r["name"] for r in cur.fetchall()}
    cur.execute("SELECT DISTINCT copybook_name FROM copybook_usage WHERE copybook_name IS NOT NULL")
    all_copybook_refs: Set[str] = {r["copybook_name"] for r in cur.fetchall()}
    non_paragraph_ids = all_data_items | all_copybook_refs

    # Pull module → programs for Module-mode lookups
    cur.execute("SELECT id, module_name FROM modules")
    mod_id_by_name = {r["module_name"]: r["id"] for r in cur.fetchall()}
    cur.execute("SELECT id, business_name FROM modules")
    mod_id_by_business = {r["business_name"]: r["id"] for r in cur.fetchall() if r["business_name"]}
    cur.execute("SELECT module_id, program_id FROM module_programs")
    progs_by_module_id: Dict[int, Set[str]] = {}
    for r in cur.fetchall():
        progs_by_module_id.setdefault(r["module_id"], set()).add(r["program_id"])

    cur.execute("SELECT program_id, copybook_name FROM copybook_usage")
    copybooks_by_program: Dict[str, Set[str]] = {}
    for r in cur.fetchall():
        copybooks_by_program.setdefault(r["program_id"], set()).add(r["copybook_name"])

    ims_by_program: Dict[str, Dict[str, Set[str]]] = {}
    ims_call_pairs_by_program: Dict[str, List[Tuple[str, str]]] = {}
    try:
        cur.execute("""
            SELECT program_id, function_code, ssa_name, paragraph_name
            FROM ims_calls
            ORDER BY line_number
        """)
        for r in cur.fetchall():
            ims = ims_by_program.setdefault(
                r["program_id"],
                {"functions": set(), "ssas": set(), "paragraphs": set(), "entry": set()},
            )
            fn = r["function_code"]
            if fn:
                if fn == "ENTRY":
                    ims["entry"].add("DLITCBL")
                else:
                    ims["functions"].add(fn)
            if r["ssa_name"]:
                ims["ssas"].add(r["ssa_name"])
            if r["paragraph_name"]:
                ims["paragraphs"].add(r["paragraph_name"])
            if fn and fn != "ENTRY" and r["paragraph_name"]:
                ims_call_pairs_by_program.setdefault(r["program_id"], []).append((fn, r["paragraph_name"]))
    except Exception:
        pass

    source_literals_by_program: Dict[str, Set[str]] = {}
    source_status_by_program: Dict[str, Set[str]] = {}
    try:
        cur.execute("SELECT program_id, file_path FROM programs")
        for r in cur.fetchall():
            path = Path(r["file_path"] or "")
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            body_lines = []
            for raw_line in text.splitlines():
                if len(raw_line) > 6 and raw_line[6] == "*":
                    continue
                body = raw_line[6:] if len(raw_line) > 6 else raw_line
                body_lines.append(body[:66] if len(body) > 66 else body)
            body = "\n".join(body_lines)
            m = re.search(r"\bWS-PGMNAME\b[\s\S]{0,90}?\bVALUE\s+['\"]([^'\"]+)['\"]", body, re.IGNORECASE)
            if m:
                source_literals_by_program.setdefault(r["program_id"], set()).add(f"WS-PGMNAME={m.group(1)}")
            statuses = set()
            if re.search(r"\bPAUT-PCB-STATUS\s*=\s*SPACES\b", body, re.IGNORECASE):
                statuses.add("PAUT-PCB-STATUS = SPACES")
            if re.search(r"\bPAUT-PCB-STATUS\s*=\s*['\"]II['\"]", body, re.IGNORECASE):
                statuses.add("PAUT-PCB-STATUS = 'II'")
            if re.search(r"\bWS-INFIL1-STATUS\b", body, re.IGNORECASE):
                statuses.add("WS-INFIL1-STATUS")
            if re.search(r"\bWS-INFIL2-STATUS\b", body, re.IGNORECASE):
                statuses.add("WS-INFIL2-STATUS")
            if statuses:
                source_status_by_program[r["program_id"]] = statuses
    except Exception:
        pass

    invalid = 0
    below_min = 0
    docs_checked = 0

    for row in rows:
        mode = row["mode"]
        subject = row["subject"]
        text = row["document_text"] or ""
        if mode not in ("Program", "Module", "Application"):
            continue
        docs_checked += 1
        text_upper = text.upper()

        cites = set(PARA_CITE_PAT.findall(text))
        if not cites and mode == "Application":
            continue  # Application mode doesn't require citations

        # Build the set of valid paragraphs for this subject's scope
        if mode == "Program":
            scope = paras_by_program.get(subject, set())
        elif mode == "Module":
            mod_id = mod_id_by_business.get(subject) or mod_id_by_name.get(subject)
            scope = set()
            if mod_id is not None:
                for pid in progs_by_module_id.get(mod_id, set()):
                    scope |= paras_by_program.get(pid, set())
        else:
            scope = all_paragraphs

        # (a) Hallucinated citations — cited paragraph not in scope
        paragraph_cites = cites - non_paragraph_ids
        bad = paragraph_cites - scope - all_paragraphs  # not in this scope AND not in any program
        # We forgive citations that match any real paragraph (LLM might cite a related program's
        # paragraph). Hard error only when the name doesn't exist anywhere in the codebase.
        truly_bad = paragraph_cites - all_paragraphs
        if truly_bad:
            invalid += len(truly_bad)
            report.citation_errors.append(
                f"{mode}/{subject}: {len(truly_bad)} hallucinated paragraph(s): "
                + ", ".join(sorted(truly_bad)[:5])
                + (" ..." if len(truly_bad) > 5 else "")
            )
        elif bad:
            # In-scope check is a softer warning
            report.citation_warnings.append(
                f"{mode}/{subject}: cited paragraphs not in subject scope: "
                + ", ".join(sorted(bad)[:5])
            )

        # (b) Minimum count check
        in_scope_cites = paragraph_cites & scope
        min_required = MIN_CITATIONS.get(mode, 0)
        if mode == "Program":
            available = len(paras_by_program.get(subject, set()))
            min_required = min(min_required, max(1, available))
        if mode in ("Program", "Module") and len(in_scope_cites) < min_required:
            below_min += 1
            report.citation_warnings.append(
                f"{mode}/{subject}: only {len(in_scope_cites)} paragraph citation(s); expected >= {min_required}"
            )

        # (c) Source-grounding checks for cached generated Program docs.
        if mode == "Program":
            expected_copybooks = copybooks_by_program.get(subject, set())
            if expected_copybooks:
                if re.search(r"DOES\s+NOT\s+COPY\s+ANY\s+COPYBOOKS|NO\s+COPYBOOKS", text_upper):
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: contradicts source by saying no copybooks; expected {', '.join(sorted(expected_copybooks))}"
                    )
                missing = sorted(cb for cb in expected_copybooks if cb.upper() not in text_upper)
                if missing:
                    invalid += len(missing)
                    report.citation_errors.append(
                        f"Program/{subject}: missing source COPY/copybook(s): {', '.join(missing)}"
                    )

            ims_expected = ims_by_program.get(subject, {})
            if ims_expected.get("entry") and "DLITCBL" not in text_upper:
                invalid += 1
                report.citation_errors.append(
                    f"Program/{subject}: missing IMS ENTRY 'DLITCBL' documentation"
                )
            for fn in sorted(ims_expected.get("functions", set())):
                if fn.upper() not in text_upper:
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: missing IMS CBLTDLI function {fn}"
                    )
            for ssa in sorted(ims_expected.get("ssas", set())):
                if ssa.upper() not in text_upper:
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: missing IMS SSA {ssa}"
                    )
            for para in sorted(ims_expected.get("paragraphs", set())):
                if para.upper() not in text_upper:
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: missing IMS call paragraph {para}"
                    )
            known_paras = paras_by_program.get(subject, set())
            sentences = re.split(r"(?<=[.!?])\s+", text_upper)
            fn_counts = {}
            for fn, _para in ims_call_pairs_by_program.get(subject, []):
                fn_counts[fn] = fn_counts.get(fn, 0) + 1
            for fn, correct_para in ims_call_pairs_by_program.get(subject, []):
                if fn_counts.get(fn, 0) != 1:
                    continue
                fn_upper = fn.upper()
                correct_upper = correct_para.upper()
                wrong_paras = [p.upper() for p in known_paras if p.upper() != correct_upper]
                for sentence in sentences:
                    if fn_upper not in sentence:
                        continue
                    for wrong_para in wrong_paras:
                        if wrong_para in sentence and correct_upper not in sentence:
                            invalid += 1
                            report.citation_errors.append(
                                f"Program/{subject}: misattributes IMS function {fn} to {wrong_para}; source shows {correct_para}"
                            )
                            break

            for literal in sorted(source_literals_by_program.get(subject, set())):
                name, value = literal.split("=", 1)
                if name.upper() not in text_upper or value.upper() not in text_upper:
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: missing source literal {name}='{value}'"
                    )

            for condition in sorted(source_status_by_program.get(subject, set())):
                if condition.upper() not in text_upper:
                    invalid += 1
                    report.citation_errors.append(
                        f"Program/{subject}: missing source status condition {condition}"
                    )

    report.stats["citations_docs_checked"] = docs_checked
    report.stats["citations_invalid"] = invalid
    report.stats["citations_below_min"] = below_min
    conn.close()


# ───────────────────────────────────────────────────────────────────────────────
# Public API
# ───────────────────────────────────────────────────────────────────────────────

def validate_docs(db_path: str, docs_dir: str) -> ValidationReport:
    """Run all three validation checks and return a report."""
    report = ValidationReport()
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        report.structural_errors.append(f"Docs directory does not exist: {docs_dir}")
        return report

    facts = _load_sqlite_facts(db_path)
    relations = _load_expected_relations(db_path)

    console.print("[cyan]Running structural check...[/cyan]")
    _check_structural(facts, docs_path, report)

    console.print("[cyan]Running factual cross-check...[/cyan]")
    _check_factual(facts, docs_path, report)

    console.print("[cyan]Running paragraph-citation check (LLM docs)...[/cyan]")
    _check_citations(db_path, report)

    console.print("[cyan]Running coverage check...[/cyan]")
    _check_coverage(relations, docs_path, report)

    console.print("[cyan]Running prompt coverage check...[/cyan]")
    _check_prompt_coverage(db_path, report)

    return report


def print_report(report: ValidationReport) -> None:
    """Pretty-print a validation report to console."""
    table = Table(title="Documentation Validation Report")
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    s_status = "PASS" if not report.structural_errors else "FAIL"
    table.add_row(
        "Structural",
        f"[green]{s_status}[/green]" if s_status == "PASS" else f"[red]{s_status}[/red]",
        f"missing docs: {report.stats.get('program_docs_missing', 0)}, "
        f"broken links: {report.stats.get('broken_links', 0)}, "
        f"empty/missing sections: "
        f"{report.stats.get('empty_sections', 0) + report.stats.get('missing_sections', 0)}",
    )

    f_status = "PASS" if not report.factual_errors else "FAIL"
    table.add_row(
        "Factual",
        f"[green]{f_status}[/green]" if f_status == "PASS" else f"[red]{f_status}[/red]",
        f"unknown identifier refs: {report.stats.get('unknown_identifier_refs', 0)}",
    )

    expected = report.stats.get("coverage_expected_refs", 0)
    missing = report.stats.get("coverage_missing_refs", 0)
    pct = 100.0 * (expected - missing) / expected if expected else 100.0
    c_status = "PASS" if missing == 0 else "FAIL"
    table.add_row(
        "Coverage",
        f"[green]{c_status}[/green]" if c_status == "PASS" else f"[red]{c_status}[/red]",
        f"{expected - missing}/{expected} references covered ({pct:.1f}%)",
    )

    prompt_docs = int(report.stats.get("prompt_ledgers_checked", 0) or 0)
    prompt_expected = int(report.stats.get("prompt_expected_facts", 0) or 0)
    prompt_in_context = int(report.stats.get("prompt_facts_in_context", 0) or 0)
    prompt_in_doc = int(report.stats.get("prompt_facts_in_document", 0) or 0)
    if prompt_docs == 0:
        prompt_status = "SKIP"
        prompt_color = "yellow"
        prompt_detail = "no saved prompt coverage ledgers yet"
    else:
        prompt_status = "WARN" if report.prompt_coverage_warnings else "PASS"
        prompt_color = "yellow" if report.prompt_coverage_warnings else "green"
        prompt_detail = (
            f"{prompt_docs} doc(s) · context {prompt_in_context}/{prompt_expected} facts · "
            f"document {prompt_in_doc}/{prompt_expected} facts"
        )
    table.add_row(
        "Prompt Coverage",
        f"[{prompt_color}]{prompt_status}[/{prompt_color}]",
        prompt_detail,
    )

    cit_checked = report.stats.get("citations_docs_checked", 0)
    cit_invalid = report.stats.get("citations_invalid", 0)
    cit_low = report.stats.get("citations_below_min", 0)
    if cit_checked == 0:
        cit_status = "SKIP"
        cit_color = "yellow"
        cit_detail = "no LLM-generated docs in cache yet"
    elif cit_invalid > 0:
        cit_status = "FAIL"
        cit_color = "red"
        cit_detail = f"{cit_checked} docs · {cit_invalid} citation/grounding issue(s) · {cit_low} below-min"
    else:
        cit_status = "PASS"
        cit_color = "green"
        cit_detail = f"{cit_checked} docs · 0 citation/grounding issues · {cit_low} below-min"
    table.add_row(
        "Citations",
        f"[{cit_color}]{cit_status}[/{cit_color}]",
        cit_detail,
    )

    console.print(table)

    # Show first 10 issues per category
    if report.structural_errors:
        console.print("\n[red]Structural Errors:[/red]")
        for e in report.structural_errors[:10]:
            console.print(f"  - {e}")
    if report.structural_warnings:
        console.print(f"\n[yellow]Structural Warnings ({len(report.structural_warnings)}):[/yellow]")
        for w in report.structural_warnings[:10]:
            console.print(f"  - {w}")
    if report.factual_errors:
        console.print(f"\n[red]Factual Errors ({len(report.factual_errors)}):[/red]")
        for e in report.factual_errors[:10]:
            console.print(f"  - {e}")
    if report.coverage_gaps:
        console.print(f"\n[yellow]Coverage Gaps ({len(report.coverage_gaps)}):[/yellow]")
        for g in report.coverage_gaps[:10]:
            console.print(f"  - {g}")
    if report.prompt_coverage_warnings:
        console.print(f"\n[yellow]Prompt Coverage Warnings ({len(report.prompt_coverage_warnings)}):[/yellow]")
        for w in report.prompt_coverage_warnings[:10]:
            console.print(f"  - {w}")
    if report.citation_errors:
        console.print(f"\n[red]Citation Errors ({len(report.citation_errors)}):[/red]")
        for e in report.citation_errors[:10]:
            console.print(f"  - {e}")
    if report.citation_warnings:
        console.print(f"\n[yellow]Citation Warnings ({len(report.citation_warnings)}):[/yellow]")
        for w in report.citation_warnings[:10]:
            console.print(f"  - {w}")


def write_report(report: ValidationReport, output_path: str) -> None:
    """Write the validation report as JSON."""
    Path(output_path).write_text(
        json.dumps(report.to_dict(), indent=2),
        encoding="utf-8",
    )
    console.print(f"[green]Report written to {output_path}[/green]")


# ───────────────────────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate generated COBOL docs")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="SQLite DB path")
    parser.add_argument("--docs", default="docs", help="Generated docs directory")
    parser.add_argument("--out", default="docs/validation_report.json", help="JSON report output")
    args = parser.parse_args()

    report = validate_docs(args.db, args.docs)
    print_report(report)
    write_report(report, args.out)

    raise SystemExit(0 if report.passed else 1)
