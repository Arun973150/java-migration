"""
Standalone JCL/BMS English documentation pipeline.

This module is intentionally separate from doc_generator.py. It creates
first-class English documentation for non-COBOL artifacts:
  - JCL batch jobs
  - BMS screen maps
  - BMS source files / mapsets

The pipeline mirrors the agent framework used elsewhere in the application:
Context Builder -> Writer -> Critique -> Formatter -> Grounding -> Publisher.
When LangGraph is installed the stages are wired as a StateGraph; otherwise the
same stages run sequentially so local deterministic generation still works.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import os
from typing import Any, Dict, List, Optional, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

try:
    from langgraph.graph import END, START, StateGraph
except Exception:  # pragma: no cover - fallback keeps CLI usable without LangGraph
    END = START = None
    StateGraph = None

from sqlite_loader import SQLiteLoader
from doc_agent_pipeline import _get_llm


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


class ArtifactDocState(TypedDict, total=False):
    artifact_type: str
    subject: str
    raw: Dict[str, Any]
    context: Dict[str, Any]
    draft: str
    critique_passed: bool
    critique_feedback: str
    formatted_doc: str
    grounding_passed: bool
    grounding_feedback: str
    db_path: str
    output_path: str
    iteration: int
    max_iterations: int
    saved: bool


class ArtifactCritiqueResult(BaseModel):
    passed: bool = True
    issues: List[str] = Field(default_factory=list)


ARTIFACT_WRITER_SYSTEM = (
    "You are a senior mainframe modernization documentation architect. "
    "Write source-grounded English documentation for JCL and BMS artifacts. "
    "Use only facts from SYSTEM DATA. If a fact is missing, say it is not present "
    "in extracted data."
)

ARTIFACT_CRITIQUE_SYSTEM = """You are a technical editor reviewing standalone JCL/BMS documentation.
Respond only with JSON: {"passed": true/false, "issues": ["issue 1", "issue 2"]}"""

ARTIFACT_FORMATTER_SYSTEM = (
    "You are a documentation formatter. Clean markdown structure without removing details. "
    "Return the complete document."
)


def _safe_name(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name.strip())
    return safe or "UNKNOWN"


def _clean_comment_lines(lines: Any, limit: int = 8) -> List[str]:
    if isinstance(lines, str):
        lines = [ln.strip() for ln in lines.splitlines()]
    cleaned: List[str] = []
    boilerplate_terms = (
        "copyright",
        "all rights reserved",
        "licensed under",
        "apache license",
        "you may not",
        "you may obtain",
        "http://",
        "https://",
        "unless required",
        "software distributed",
        "either express",
        "as is",
        "warranties or conditions",
        "language governing",
        "limitations under the license",
    )
    for line in lines or []:
        text = str(line).strip(" *")
        if not text:
            continue
        low = text.lower()
        if any(term in low for term in boilerplate_terms):
            continue
        if text not in cleaned:
            cleaned.append(text)
        if len(cleaned) >= limit:
            break
    return cleaned


def _join_or_none(items: List[str], limit: int = 12) -> str:
    items = [str(i) for i in items if str(i).strip()]
    if not items:
        return "None found in extracted data"
    if len(items) > limit:
        return ", ".join(items[:limit]) + f", and {len(items) - limit} more"
    return ", ".join(items)


def _dataset_name(ds: Dict[str, Any]) -> str:
    dsn = (ds.get("dsn") or "").strip()
    if dsn:
        return dsn
    if ds.get("is_inline"):
        return "inline control data"
    return ds.get("dd_name") or "unnamed DD"


def _dataset_base_tokens(dsn: str) -> List[str]:
    raw = (dsn or "").upper().strip()
    if not raw:
        return []
    parts = [p for p in raw.replace("-", ".").split(".") if p]
    candidates = []
    for part in parts:
        if part in {"AWS", "M2", "CARDDEMO", "PS", "KSDS", "DATA", "INDEX", "VSAM"}:
            continue
        candidates.append(part)
    if not candidates and parts:
        candidates.append(parts[-1])
    return candidates


def _dataset_search_terms(dsn: str) -> List[str]:
    synonyms = {
        "ACCT": ["ACCOUNT", "ACCT"],
        "ACCOUNT": ["ACCOUNT", "ACCT"],
        "CUST": ["CUSTOMER", "CUST"],
        "CARD": ["CARD"],
        "TRAN": ["TRAN", "TRN", "TRANSACTION"],
        "XREF": ["XREF", "CROSS", "REF"],
    }
    terms: List[str] = []
    for token in _dataset_base_tokens(dsn):
        terms.append(token)
        for key, vals in synonyms.items():
            if token.startswith(key) or key.startswith(token):
                terms.extend(vals)
    seen = []
    for term in terms:
        if term not in seen:
            seen.append(term)
    return seen


def _ownership_clues(job: Dict[str, Any]) -> Dict[str, str]:
    all_comments = "\n".join(str(line) for line in (job.get("comment_lines") or []))
    owner = "not present in extracted data"
    maintainer = "not present in extracted data"
    if "amazon.com" in all_comments.lower():
        owner = "Copyright header names Amazon.com, Inc. or its affiliates"
    notify = ""
    raw_header = "\n".join(str(line) for line in (job.get("header_comments") or []))
    if "&SYSUID" in str(job).upper() or "&SYSUID" in raw_header.upper():
        notify = "JOB card includes NOTIFY=&SYSUID"
    if notify and maintainer == "not present in extracted data":
        maintainer = f"batch completion notice is routed to {notify}"
    return {"owner": owner, "maintainer": maintainer, "notify": notify or "not present in extracted data"}


def _find_dataset_job_dependencies(loader: SQLiteLoader, dsn: str, current_job: str) -> Dict[str, List[Dict[str, Any]]]:
    if not dsn or not getattr(loader, "conn", None):
        return {"references": [], "other_jobs": []}
    cur = loader.conn.cursor()
    try:
        cur.execute("""
            SELECT DISTINCT job_name, step_name, direction
            FROM jcl_datasets
            WHERE UPPER(dsn) = UPPER(?)
            ORDER BY job_name, step_name
        """, (dsn,))
        rows = [dict(r) for r in cur.fetchall()]
    except Exception:
        rows = []
    references = rows
    other_jobs = [r for r in rows if (r.get("job_name") or "").upper() != current_job.upper()]
    return {"references": references, "other_jobs": other_jobs}


def _find_dataset_program_evidence(loader: SQLiteLoader, dsn: str) -> Dict[str, Any]:
    if not dsn or not getattr(loader, "conn", None):
        return {"file_records": [], "copybook_fields": [], "matched_terms": []}
    terms = _dataset_search_terms(dsn)
    if not terms:
        return {"file_records": [], "copybook_fields": [], "matched_terms": []}

    cur = loader.conn.cursor()
    file_rows: List[Dict[str, Any]] = []
    for term in terms[:6]:
        try:
            cur.execute("""
                SELECT program_id, file_name, record_name, field_name, level_number, picture, usage, line_number
                FROM file_records
                WHERE UPPER(file_name) LIKE ? OR UPPER(record_name) LIKE ? OR UPPER(field_name) LIKE ?
                ORDER BY program_id, file_name, line_number
            """, (f"%{term}%", f"%{term}%", f"%{term}%"))
            file_rows.extend(dict(r) for r in cur.fetchall())
        except Exception:
            pass

    copy_rows: List[Dict[str, Any]] = []
    for term in terms[:6]:
        try:
            cur.execute("""
                SELECT copybook_name, field_name, level_number, picture, usage, parent_name, line_number
                FROM copybook_fields
                WHERE UPPER(field_name) LIKE ? OR UPPER(parent_name) LIKE ? OR UPPER(copybook_name) LIKE ?
                ORDER BY copybook_name, line_number
            """, (f"%{term}%", f"%{term}%", f"%{term}%"))
            copy_rows.extend(dict(r) for r in cur.fetchall())
        except Exception:
            pass

    def _dedupe(rows: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
        seen = set()
        out = []
        for row in rows:
            marker = tuple(row.get(k) for k in keys)
            if marker in seen:
                continue
            seen.add(marker)
            out.append(row)
        return out

    file_rows = _dedupe(file_rows, ["program_id", "file_name", "record_name", "field_name", "line_number"])
    copy_rows = _dedupe(copy_rows, ["copybook_name", "field_name", "parent_name", "line_number"])
    return {"file_records": file_rows, "copybook_fields": copy_rows, "matched_terms": terms}


def _doc_demo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _normalize_relpath(path: str) -> str:
    return str(path or "").replace("/", "\\").strip().lower()


def _resolve_existing_path(relative_path: str) -> Optional[Path]:
    rel = str(relative_path or "").replace("\\", os.sep).replace("/", os.sep)
    candidates = [
        _doc_demo_root() / rel,
        _doc_demo_root().parent / rel,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _load_parsed_bms_file(file_path: str) -> Optional[Dict[str, Any]]:
    parsed_path = _doc_demo_root() / "parsed_output" / "screens.json"
    if not parsed_path.exists():
        return None
    try:
        data = json.loads(parsed_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    normalized = _normalize_relpath(file_path)
    for item in data:
        if _normalize_relpath(item.get("file_path") or "") == normalized:
            return item
    return None


def _parse_readme_bms_mapping(mapset: str) -> Dict[str, str]:
    readme = _doc_demo_root() / "carddemo" / "README.md"
    if not readme.exists():
        return {}
    try:
        lines = readme.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return {}
    target = (mapset or "").strip().upper()
    for line in lines:
        if "|" not in line:
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 6:
            continue
        if len(parts) > 2 and parts[2].upper() == target:
            return {
                "transaction_id": parts[1] if len(parts) > 1 else "",
                "mapset_name": parts[2] if len(parts) > 2 else "",
                "associated_program": parts[3] if len(parts) > 3 else "",
                "business_name": parts[4] if len(parts) > 4 else "",
                "description": parts[5] if len(parts) > 5 else "",
            }
    return {}


def _infer_bms_programs_from_repo(mapset: str, map_names: List[str]) -> List[Dict[str, str]]:
    root = _doc_demo_root() / "carddemo"
    if not root.exists():
        return []
    programs: List[Dict[str, str]] = []
    seen = set()
    mapset_up = (mapset or "").upper()
    map_names_up = [m.upper() for m in map_names if m]
    for path in root.rglob("*"):
        if path.suffix.lower() not in {".cbl", ".cob"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        upper = text.upper()
        reasons = []
        if mapset_up and (f"COPY {mapset_up}." in upper or f"MAPSET('{mapset_up}')" in upper):
            reasons.append(f"references mapset {mapset_up}")
        for map_name in map_names_up:
            if f"MAP('{map_name}')" in upper:
                reasons.append(f"references map {map_name}")
                break
        if not reasons:
            continue
        program_id = path.stem.upper()
        if program_id in seen:
            continue
        seen.add(program_id)
        programs.append({
            "program_id": program_id,
            "file_path": str(path),
            "evidence": "; ".join(reasons),
        })
    return programs


def _extract_bms_source_metadata(file_path: str) -> Dict[str, Any]:
    source_path = _resolve_existing_path(file_path)
    if not source_path:
        return {
            "source_path": file_path,
            "header_comments": [],
            "title": "",
            "dfhmsd_controls": {},
            "map_definitions": [],
            "command_key_hints": [],
        }
    try:
        lines = source_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return {
            "source_path": str(source_path),
            "header_comments": [],
            "title": "",
            "dfhmsd_controls": {},
            "map_definitions": [],
            "command_key_hints": [],
        }

    header_comments = []
    before_mapset = True
    for raw in lines:
        stripped = raw.strip()
        if before_mapset and " DFHMSD " in stripped:
            before_mapset = False
        if before_mapset and stripped.startswith("*"):
            header_comments.append(stripped.strip("* ").strip())

    title = ""
    for line in header_comments:
        low = line.lower()
        if line and "copyright" not in low and "licensed under" not in low and "all rights reserved" not in low:
            title = line
            break

    controls: Dict[str, str] = {}
    block = []
    capture = False
    for raw in lines:
        stripped = raw.rstrip()
        if " DFHMSD " in stripped:
            capture = True
        if capture:
            block.append(stripped)
            if not stripped.endswith("-"):
                break
    control_text = " ".join(part.replace("-", " ") for part in block)
    for key in ["CTRL", "EXTATT", "LANG", "MODE", "STORAGE", "TIOAPFX", "TYPE"]:
        match = re.search(rf"{key}\s*=\s*(\([^)]*\)|[^,\s]+)", control_text, re.IGNORECASE)
        if match:
            controls[key.upper()] = match.group(1).strip()

    map_definitions = []
    for idx, raw in enumerate(lines):
        match = re.match(r"^\s*([A-Z0-9#@$]+)\s+DFHMDI\b", raw, re.IGNORECASE)
        if not match:
            continue
        collected = [raw.rstrip()]
        pointer = idx + 1
        while pointer < len(lines):
            nxt = lines[pointer].rstrip()
            if "DFHMDF" in nxt or "DFHMDI" in nxt or "DFHMSD TYPE=FINAL" in nxt or " END" == nxt.strip():
                break
            collected.append(nxt)
            if not nxt.endswith("-"):
                break
            pointer += 1
        joined = " ".join(part.replace("-", " ") for part in collected)
        md = {"map_name": match.group(1).upper()}
        for key in ["COLUMN", "LINE", "SIZE"]:
            m = re.search(rf"{key}\s*=\s*(\([^)]*\)|[^,\s]+)", joined, re.IGNORECASE)
            if m:
                md[key.lower()] = m.group(1).strip()
        map_definitions.append(md)

    command_hints: List[str] = []
    idx = 0
    while idx < len(lines):
        text = lines[idx].strip()
        if "INITIAL='" not in text.upper():
            idx += 1
            continue
        combined = text
        while combined.count("'") % 2 != 0 and idx + 1 < len(lines):
            idx += 1
            combined += lines[idx].strip()
        parts = re.findall(r"'([^']*)'", combined)
        for part in parts:
            cleaned = part.replace("-", "").strip()
            if re.search(r"\bENTER=", cleaned, re.IGNORECASE) or re.search(r"\bF\d+=", cleaned, re.IGNORECASE):
                cleaned = re.sub(r"\s{2,}", " ", cleaned)
                if cleaned not in command_hints:
                    command_hints.append(cleaned)
        idx += 1

    return {
        "source_path": str(source_path),
        "header_comments": _clean_comment_lines(header_comments, limit=12),
        "title": title,
        "dfhmsd_controls": controls,
        "map_definitions": map_definitions,
        "command_key_hints": command_hints,
    }


def build_jcl_agent_context(job: Dict[str, Any], loader: Optional[SQLiteLoader] = None) -> str:
    """Build the source-grounded context sent to the JCL writer agent."""
    ctx = _build_jcl_context(job)
    ownership = _ownership_clues(job)
    upstream = []
    downstream = []
    layout_notes = []
    for dsn in ctx["input_datasets"] + ctx["output_datasets"]:
        if loader:
            dep = _find_dataset_job_dependencies(loader, dsn, job.get("job_name") or "")
            others = dep["other_jobs"]
            if others:
                target = downstream if dsn.endswith(".KSDS") or ".VSAM." in dsn.upper() else upstream
                target.extend([f"{dsn} <- {r['job_name']}/{r['step_name']} ({r.get('direction') or '-'})" for r in others])
        if loader and dsn.endswith(".PS"):
            evidence = _find_dataset_program_evidence(loader, dsn)
            if evidence["file_records"]:
                sample = evidence["file_records"][:10]
                layout_notes.append(f"Program FD evidence for {dsn}:")
                for row in sample:
                    layout_notes.append(
                        f"- Program={row.get('program_id')}; File={row.get('file_name')}; Record={row.get('record_name')}; "
                        f"Field={row.get('field_name')}; PIC={row.get('picture') or '-'}; Usage={row.get('usage') or '-'}"
                    )
            if evidence["copybook_fields"]:
                sample = [r for r in evidence["copybook_fields"] if r.get("level_number") in (1, 5)][:16]
                layout_notes.append(f"Copybook evidence for {dsn}:")
                for row in sample:
                    layout_notes.append(
                        f"- Copybook={row.get('copybook_name')}; Parent={row.get('parent_name') or '-'}; "
                        f"Field={row.get('field_name')}; PIC={row.get('picture') or '-'}; Usage={row.get('usage') or '-'}"
                    )

    lines = [
        "# JCL Artifact Context",
        f"Job Name: {job.get('job_name') or 'UNKNOWN'}",
        f"Source File: {job.get('file_path') or job.get('file_name') or '-'}",
        f"Job Description: {job.get('job_description') or '(not present in extracted data)'}",
        f"Job Class: {job.get('job_class') or '(not present in extracted data)'}",
        f"Message Class: {job.get('msg_class') or '(not present in extracted data)'}",
        f"Ownership Clue: {ownership['owner']}",
        f"Maintainer Clue: {ownership['maintainer']}",
        f"Notify Routing: {ownership['notify']}",
        f"Step Count: {ctx['step_count']}",
        f"Programs Called: {_join_or_none(job.get('programs_called') or [])}",
        f"Input Datasets: {_join_or_none(ctx['input_datasets'], limit=40)}",
        f"Output Datasets: {_join_or_none(ctx['output_datasets'], limit=40)}",
        "Trigger Evidence: no scheduler chain, predecessor job, or explicit submit relationship found in extracted JCL metadata unless listed below.",
        "Downstream Job Dependencies: " + (_join_or_none(downstream, limit=40) if downstream else "not present in extracted data"),
        "Related Upstream/Peer References: " + (_join_or_none(upstream, limit=40) if upstream else "not present in extracted data"),
        "",
        "## Steps",
    ]
    for index, step in enumerate(job.get("steps") or [], 1):
        lines.extend([
            f"### Step {index}: {step.get('step_name') or '-'}",
            f"Program: {step.get('program') or '(not present in extracted data)'}",
            f"Procedure: {step.get('proc') or '(not present in extracted data)'}",
            f"Step Type: {step.get('step_type') or '-'}",
            f"COND: {step.get('cond') or '(not present in extracted data)'}",
            f"Line Number: {step.get('line_number') or '-'}",
        ])
        comments = _clean_comment_lines(step.get("step_comments") or [], limit=12)
        lines.append("Step Comments: " + (_join_or_none(comments, limit=12)))
        datasets = step.get("datasets") or []
        if datasets:
            lines.append("DD Datasets:")
            for ds in datasets:
                lines.append(
                    f"- DD={ds.get('dd_name') or '-'}; DSN={ds.get('dsn') or '(none)'}; "
                    f"DISP={ds.get('disp') or '(none)'}; Direction={ds.get('direction') or '-'}; "
                    f"RECFM={ds.get('recfm') or '-'}; LRECL={ds.get('lrecl') or '-'}; "
                    f"Inline={bool(ds.get('is_inline'))}"
                )
        else:
            lines.append("DD Datasets: None found in extracted data")
        if step.get("sysin_data"):
            lines.append("Inline SYSIN:")
            for sysin in step.get("sysin_data") or []:
                lines.append(f"  {sysin.rstrip()}")
        lines.append("")
    if layout_notes:
        lines.extend(["## Source Record Layout Evidence", *layout_notes, ""])
    else:
        lines.extend(["## Source Record Layout Evidence", "No physical or logical record layout evidence was matched for the flat-file datasets.", ""])
    return "\n".join(lines)


def build_bms_agent_context(screen: Dict[str, Any]) -> str:
    """Build the source-grounded context sent to the BMS writer agent."""
    ctx = _build_bms_context(screen)
    lines = [
        "# BMS Artifact Context",
        f"Screen Name: {screen.get('screen_name') or 'UNKNOWN'}",
        f"Map Name: {screen.get('map_name') or '-'}",
        f"Mapset Name: {screen.get('mapset_name') or '-'}",
        f"Source File: {screen.get('file_path') or '-'}",
        f"Associated Program: {screen.get('associated_program') or '(not present in extracted data)'}",
        f"Transaction ID: {screen.get('transaction_id') or '(not present in extracted data)'}",
        f"Total Fields: {ctx['field_count']}",
        f"Input Fields: {len(ctx['input_fields'])}",
        f"Output Fields: {len(ctx['output_fields'])}",
        f"Label Fields: {len(ctx['label_fields'])}",
        "",
        "## Fields",
    ]
    for field in screen.get("fields") or []:
        label = _field_label(field) or "(no label text)"
        lines.append(
            f"- Name={field.get('field_name')}; Type={field.get('field_type')}; "
            f"Row={field.get('row_position')}; Col={field.get('col_position')}; "
            f"Length={field.get('length')}; Attributes={field.get('attributes') or '-'}; "
            f"Color={field.get('color') or '-'}; Initial={field.get('initial_value') or ''}; "
            f"Label={label}"
        )
    return "\n".join(lines)


def build_bms_file_artifact(loader: SQLiteLoader, file_path: str) -> Optional[Dict[str, Any]]:
    """Group all extracted screens/maps that belong to one BMS source file."""
    normalized = (file_path or "").strip().lower()
    if not normalized:
        return None

    screens = loader.get_all_screens()
    matching = [
        screen for screen in screens
        if (screen.get("file_path") or "").strip().lower() == normalized
    ]
    if not matching:
        return None

    detailed_screens: List[Dict[str, Any]] = []
    details_by_name: Dict[str, Dict[str, Any]] = {}
    for screen in matching:
        screen_id = screen.get("id")
        if screen_id is None:
            continue
        details = loader.get_screen_details(screen_id)
        if details:
            detailed_screens.append(details)
            details_by_name[(details.get("map_name") or details.get("screen_name") or "").upper()] = details

    if not detailed_screens:
        return None

    parsed = _load_parsed_bms_file(file_path)
    source_meta = _extract_bms_source_metadata(file_path)

    screen_records: List[Dict[str, Any]] = []
    if parsed and parsed.get("maps"):
        for map_info in parsed.get("maps") or []:
            map_name = str(map_info.get("map_name") or "").upper()
            db_row = details_by_name.get(map_name, {})
            screen_records.append({
                "screen_name": db_row.get("screen_name") or map_info.get("map_name") or "UNKNOWN",
                "map_name": map_info.get("map_name") or db_row.get("map_name") or "-",
                "mapset_name": parsed.get("mapset_name") or db_row.get("mapset_name") or "-",
                "file_path": parsed.get("file_path") or file_path,
                "associated_program": db_row.get("associated_program"),
                "transaction_id": db_row.get("transaction_id"),
                "fields": map_info.get("fields") or [],
                "size": map_info.get("size"),
                "line": map_info.get("line"),
                "column": map_info.get("column"),
            })
    else:
        screen_records = detailed_screens[:]

    screen_records.sort(
        key=lambda item: (
            str(item.get("mapset_name") or ""),
            str(item.get("map_name") or ""),
            str(item.get("screen_name") or ""),
        )
    )

    mapset_name = (
        (parsed or {}).get("mapset_name")
        or next((item.get("mapset_name") for item in screen_records if item.get("mapset_name")), "")
    )
    map_names = [str(item.get("map_name") or item.get("screen_name") or "").upper() for item in screen_records]
    readme_mapping = _parse_readme_bms_mapping(str(mapset_name or ""))
    repo_programs = _infer_bms_programs_from_repo(str(mapset_name or ""), map_names)

    programs = sorted({
        str(item.get("associated_program")).strip()
        for item in screen_records
        if str(item.get("associated_program") or "").strip()
    })
    if readme_mapping.get("associated_program"):
        programs.append(readme_mapping["associated_program"])
    programs.extend([row["program_id"] for row in repo_programs if row.get("program_id")])
    programs = sorted({program for program in programs if str(program).strip()})

    transactions = sorted({
        str(item.get("transaction_id")).strip()
        for item in screen_records
        if str(item.get("transaction_id") or "").strip()
    })
    if readme_mapping.get("transaction_id"):
        transactions.append(readme_mapping["transaction_id"])
    transactions = sorted({tran for tran in transactions if str(tran).strip()})

    primary_program = programs[0] if programs else None
    primary_transaction = transactions[0] if transactions else None
    for record in screen_records:
        if not record.get("associated_program") and primary_program:
            record["associated_program"] = primary_program
        if not record.get("transaction_id") and primary_transaction:
            record["transaction_id"] = primary_transaction

    mapsets = sorted({
        str(item.get("mapset_name")).strip()
        for item in screen_records
        if str(item.get("mapset_name") or "").strip()
    })

    return {
        "file_name": Path(file_path).name,
        "file_path": file_path,
        "mapset_names": mapsets,
        "associated_programs": programs,
        "transaction_ids": transactions,
        "screens": screen_records,
        "source_metadata": source_meta,
        "readme_mapping": readme_mapping,
        "program_evidence": repo_programs,
    }


def _build_bms_file_context(bms_file: Dict[str, Any]) -> Dict[str, Any]:
    screens = bms_file.get("screens") or []
    all_fields = [
        field
        for screen in screens
        for field in (screen.get("fields") or [])
    ]
    by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for field in all_fields:
        by_type[(field.get("field_type") or "UNKNOWN").upper()].append(field)

    map_summaries = []
    colors = Counter((field.get("color") or "").upper() for field in all_fields if field.get("color"))
    command_hints = list(bms_file.get("source_metadata", {}).get("command_key_hints") or [])
    if not command_hints:
        for field in all_fields:
            text = (field.get("description") or field.get("initial_value") or "").strip()
            if text and (re.search(r"\bENTER=", text, re.IGNORECASE) or re.search(r"\bF\d+=", text, re.IGNORECASE)):
                if text not in command_hints:
                    command_hints.append(text)

    repeated_groups = []
    group_rows: Dict[str, List[int]] = defaultdict(list)
    group_suffixes: Dict[str, List[str]] = defaultdict(list)
    for field in all_fields:
        name = str(field.get("field_name") or "")
        if not name or name.startswith("_LABEL_"):
            continue
        match = re.match(r"^(.*?)(\d+)$", name)
        if not match:
            continue
        prefix, suffix = match.groups()
        group_rows[prefix].append(int(field.get("row_position") or 0))
        group_suffixes[prefix].append(suffix)
    for prefix, suffixes in group_suffixes.items():
        distinct = sorted(set(suffixes))
        if len(distinct) < 2:
            continue
        rows = [row for row in group_rows[prefix] if row]
        repeated_groups.append({
            "prefix": prefix,
            "occurrences": len(distinct),
            "row_span": f"{min(rows)}-{max(rows)}" if rows else "not present",
            "suffixes": distinct[:8],
        })
    repeated_groups.sort(key=lambda item: (-item["occurrences"], item["prefix"]))

    for screen in screens:
        fields = screen.get("fields") or []
        rows = sorted({field.get("row_position") for field in fields if field.get("row_position")})
        row_span = f"{min(rows)}-{max(rows)}" if rows else "not present"
        map_summaries.append({
            "screen_name": screen.get("screen_name") or "UNKNOWN",
            "map_name": screen.get("map_name") or "-",
            "mapset_name": screen.get("mapset_name") or "-",
            "associated_program": screen.get("associated_program") or "not present in extracted data",
            "transaction_id": screen.get("transaction_id") or "not present in extracted data",
            "field_count": len(fields),
            "input_count": sum(1 for field in fields if (field.get("field_type") or "").upper() == "INPUT"),
            "output_count": sum(1 for field in fields if (field.get("field_type") or "").upper() == "OUTPUT"),
            "label_count": sum(1 for field in fields if (field.get("field_type") or "").upper() == "LABEL"),
            "row_span": row_span,
            "size": screen.get("size") or "not present in extracted data",
        })

    return {
        "screen_count": len(screens),
        "field_count": len(all_fields),
        "input_fields": by_type.get("INPUT", []),
        "output_fields": by_type.get("OUTPUT", []),
        "label_fields": by_type.get("LABEL", []),
        "colors": colors,
        "map_summaries": map_summaries,
        "command_hints": command_hints,
        "repeated_groups": repeated_groups,
    }


def build_bms_file_agent_context(bms_file: Dict[str, Any]) -> str:
    """Build the source-grounded context sent to the BMS-file writer agent."""
    ctx = _build_bms_file_context(bms_file)
    source_meta = bms_file.get("source_metadata") or {}
    readme_mapping = bms_file.get("readme_mapping") or {}
    lines = [
        "# BMS File Artifact Context",
        f"BMS File: {bms_file.get('file_name') or 'UNKNOWN'}",
        f"Source File: {bms_file.get('file_path') or '-'}",
        f"Mapset Names: {_join_or_none(bms_file.get('mapset_names') or [])}",
        f"Associated Programs: {_join_or_none(bms_file.get('associated_programs') or [])}",
        f"Transaction IDs: {_join_or_none(bms_file.get('transaction_ids') or [])}",
        f"Business Name: {readme_mapping.get('business_name') or source_meta.get('title') or 'not present in extracted data'}",
        f"Business Description: {readme_mapping.get('description') or 'not present in extracted data'}",
        f"Total Maps/Screens: {ctx['screen_count']}",
        f"Total Fields: {ctx['field_count']}",
        f"Input Fields: {len(ctx['input_fields'])}",
        f"Output Fields: {len(ctx['output_fields'])}",
        f"Label Fields: {len(ctx['label_fields'])}",
        "",
        "## Source Metadata",
        f"- Title/Comment: {source_meta.get('title') or 'not present in extracted data'}",
        f"- Header comments: {_join_or_none(source_meta.get('header_comments') or [], limit=12)}",
        f"- DFHMSD controls: {_join_or_none([f'{k}={v}' for k, v in (source_meta.get('dfhmsd_controls') or {}).items()], limit=20)}",
        f"- Command key hints: {_join_or_none(ctx.get('command_hints') or [], limit=12)}",
        "",
        "## Map Summaries",
    ]
    for item in ctx["map_summaries"]:
        lines.append(
            f"- Screen={item['screen_name']}; Map={item['map_name']}; Mapset={item['mapset_name']}; "
            f"Program={item['associated_program']}; Tran={item['transaction_id']}; "
            f"Fields={item['field_count']}; Inputs={item['input_count']}; "
            f"Outputs={item['output_count']}; Labels={item['label_count']}; Rows={item['row_span']}; Size={item['size']}"
        )

    lines.extend(["", "## Linked Program Evidence"])
    for row in bms_file.get("program_evidence") or []:
        lines.append(
            f"- Program={row.get('program_id')}; Evidence={row.get('evidence')}; Source={row.get('file_path')}"
        )
    if not (bms_file.get("program_evidence") or []):
        lines.append("- No repository scan evidence found beyond extracted screen metadata.")

    lines.extend(["", "## Repeating Field Groups"])
    for group in ctx.get("repeated_groups") or []:
        lines.append(
            f"- Prefix={group['prefix']}; Occurrences={group['occurrences']}; "
            f"Suffixes={','.join(group['suffixes'])}; Rows={group['row_span']}"
        )
    if not (ctx.get("repeated_groups") or []):
        lines.append("- No repeating numbered field groups detected.")

    lines.extend(["", "## Fields By Map"])
    for screen in bms_file.get("screens") or []:
        lines.append(
            f"### Map {screen.get('map_name') or '-'} / Screen {screen.get('screen_name') or 'UNKNOWN'}"
        )
        for field in screen.get("fields") or []:
            label = _field_label(field) or "(no label text)"
            lines.append(
                f"- Name={field.get('field_name')}; Type={field.get('field_type')}; "
                f"Row={field.get('row_position')}; Col={field.get('col_position')}; "
                f"Length={field.get('length')}; Attributes={field.get('attributes') or '-'}; "
                f"Color={field.get('color') or '-'}; Initial={field.get('initial_value') or ''}; "
                f"Label={label}"
            )
        lines.append("")
    return "\n".join(lines).strip()


def _program_role(program: str, step_type: str) -> str:
    p = (program or "").upper()
    if p in {"IDCAMS"}:
        return "manages VSAM/catalog resources"
    if p in {"SORT", "DFSORT", "SYNCSORT"}:
        return "sorts, filters, or reformats records"
    if p == "IEBGENER":
        return "copies sequential data or submits generated control cards"
    if p == "IEFBR14":
        return "performs allocation or cleanup through DD statements"
    if p in {"IKJEFT01", "IKJEFT1B"}:
        return "runs TSO/DB2 command processing"
    if p == "DFSRRC00":
        return "runs an IMS dependent region program"
    if step_type == "PROC":
        return "expands and runs a cataloged procedure"
    if p:
        return "runs application processing"
    return "executes a procedure or utility"


def _field_label(field: Dict[str, Any]) -> str:
    label = (field.get("description") or field.get("initial_value") or "").strip()
    if label:
        return label
    name = field.get("field_name") or ""
    if name.startswith("_LABEL_"):
        return ""
    return name or "unnamed field"


def _build_jcl_context(job: Dict[str, Any], loader: Optional[SQLiteLoader] = None) -> Dict[str, Any]:
    steps = job.get("steps") or []
    input_datasets = []
    output_datasets = []
    system_datasets = []
    for step in steps:
        for ds in step.get("datasets") or []:
            direction = (ds.get("direction") or "").upper()
            name = _dataset_name(ds)
            if direction == "INPUT" and name not in input_datasets:
                input_datasets.append(name)
            elif direction == "OUTPUT" and name not in output_datasets:
                output_datasets.append(name)
            elif direction == "SYSTEM" and name not in system_datasets:
                system_datasets.append(name)

    programs = []
    utilities = []
    for step in steps:
        program = (step.get("program") or step.get("proc") or "").strip()
        if not program:
            continue
        if (step.get("step_type") or "").upper() in {"UTIL", "SORT", "IDCAMS"}:
            utilities.append(program)
        else:
            programs.append(program)

    ownership = _ownership_clues(job)
    downstream_jobs: List[Dict[str, Any]] = []
    peer_references: List[Dict[str, Any]] = []
    layout_evidence: Dict[str, Any] = {"file_records": [], "copybook_fields": []}
    if loader:
        for dsn in input_datasets + output_datasets:
            dep = _find_dataset_job_dependencies(loader, dsn, job.get("job_name") or "")
            others = dep["other_jobs"]
            if others:
                if dsn.endswith(".KSDS") or ".VSAM." in dsn.upper():
                    downstream_jobs.extend(others)
                else:
                    peer_references.extend(others)
            if dsn.endswith(".PS"):
                evidence = _find_dataset_program_evidence(loader, dsn)
                layout_evidence["file_records"].extend(evidence.get("file_records") or [])
                layout_evidence["copybook_fields"].extend(evidence.get("copybook_fields") or [])

    def _dedupe_refs(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        out = []
        for row in rows:
            marker = (row.get("job_name"), row.get("step_name"), row.get("direction"))
            if marker in seen:
                continue
            seen.add(marker)
            out.append(row)
        return out

    return {
        "step_count": len(steps),
        "input_datasets": input_datasets,
        "output_datasets": output_datasets,
        "system_datasets": system_datasets,
        "programs": sorted(set(programs)),
        "utilities": sorted(set(utilities)),
        "header_notes": _clean_comment_lines(job.get("header_comments") or []),
        "ownership": ownership,
        "downstream_jobs": _dedupe_refs(downstream_jobs),
        "peer_references": _dedupe_refs(peer_references),
        "layout_evidence": layout_evidence,
    }


def _write_jcl_doc(job: Dict[str, Any], ctx: Dict[str, Any]) -> str:
    job_name = job.get("job_name") or "UNKNOWN"
    description = job.get("job_description") or "No job-card description was extracted."
    ownership = ctx.get("ownership") or {}
    downstream_jobs = ctx.get("downstream_jobs") or []
    peer_references = ctx.get("peer_references") or []
    layout_evidence = ctx.get("layout_evidence") or {}
    lines = [
        f"# JCL English Documentation: {job_name}",
        "",
        "## 1. Executive Summary",
        "",
        (
            f"`{job_name}` is a standalone batch job defined in `{job.get('file_name', '-')}`. "
            f"The extracted job description is: {description}. "
            f"It contains {ctx['step_count']} execution step(s), reading "
            f"{len(ctx['input_datasets'])} input dataset reference(s) and writing "
            f"{len(ctx['output_datasets'])} output dataset reference(s)."
        ),
        "",
        "## 2. Batch Runtime Context",
        "",
        f"- Source file: `{job.get('file_path') or job.get('file_name') or '-'}`",
        f"- Job class: `{job.get('job_class') or '-'}`",
        f"- Message class: `{job.get('msg_class') or '-'}`",
        f"- Application programs/procedures: {_join_or_none(ctx['programs'])}",
        f"- Main utilities: {_join_or_none(ctx['utilities'])}",
        f"- Ownership clue: {ownership.get('owner') or 'not present in extracted data'}",
        f"- Maintainer clue: {ownership.get('maintainer') or 'not present in extracted data'}",
        f"- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file",
        "",
        "## 3. Step-by-Step Job Flow",
        "",
    ]

    for index, step in enumerate(job.get("steps") or [], 1):
        step_name = step.get("step_name") or f"STEP{index}"
        program = step.get("program") or step.get("proc") or "not present in extracted data"
        role = _program_role(step.get("program") or "", step.get("step_type") or "")
        comments = _clean_comment_lines(step.get("step_comments") or [])
        datasets = step.get("datasets") or []
        inputs = [_dataset_name(ds) for ds in datasets if (ds.get("direction") or "").upper() == "INPUT"]
        outputs = [_dataset_name(ds) for ds in datasets if (ds.get("direction") or "").upper() == "OUTPUT"]

        lines.extend([
            f"### Step {index}: `{step_name}`",
            "",
            (
                f"This step executes `{program}` and {role}. "
                f"It has {len(datasets)} DD statement(s)."
            ),
        ])
        if comments:
            lines.append("Extracted step notes: " + " ".join(comments))
        lines.extend([
            f"- Inputs: {_join_or_none(inputs)}",
            f"- Outputs: {_join_or_none(outputs)}",
        ])
        if step.get("cond"):
            lines.append(f"- Conditional execution: `COND={step.get('cond')}`")
        if step.get("sysin_data"):
            lines.append(
                f"- Inline SYSIN: {len(step.get('sysin_data') or [])} control line(s) are supplied to the step."
            )
        lines.append("")

    lines.extend([
        "## 4. Dataset and Dependency Context",
        "",
        f"- Input datasets: {_join_or_none(ctx['input_datasets'], limit=20)}",
        f"- Output datasets: {_join_or_none(ctx['output_datasets'], limit=20)}",
        f"- System/control DDs: {_join_or_none(ctx['system_datasets'], limit=20)}",
        (
            "- Downstream jobs that also reference the created/managed VSAM dataset: "
            + (_join_or_none([f"{r['job_name']}/{r['step_name']}" for r in downstream_jobs], limit=20)
               if downstream_jobs else "not present in extracted data")
        ),
        (
            "- Peer/upstream references to the flat-file inputs: "
            + (_join_or_none([f"{r['job_name']}/{r['step_name']}" for r in peer_references], limit=20)
               if peer_references else "not present in extracted data")
        ),
        "",
        "## 5. Source Record Layout",
        "",
    ])
    if layout_evidence.get("file_records"):
        lines.append("Program FD evidence suggests the physical account file contract is:")
        for row in layout_evidence["file_records"][:10]:
            lines.append(
                f"- `{row.get('program_id')}` / `{row.get('file_name')}` / `{row.get('record_name')}`: "
                f"`{row.get('field_name')}` PIC `{row.get('picture') or '-'}`"
            )
    if layout_evidence.get("copybook_fields"):
        lines.append("Copybook field evidence suggests the logical account record layout is:")
        for row in layout_evidence["copybook_fields"][:16]:
            if row.get("field_name") == "ACCOUNT-RECORD":
                continue
            lines.append(
                f"- Copybook `{row.get('copybook_name')}` field `{row.get('field_name')}` "
                f"PIC `{row.get('picture') or '-'}`"
            )
    if not layout_evidence.get("file_records") and not layout_evidence.get("copybook_fields"):
        lines.append("No record-layout evidence was matched for the flat-file datasets.")
    lines.extend([
        "- Encoding/charset: not present in extracted data.",
        "",
        "## 6. Operational Meaning",
        "",
        (
            "For migration planning, treat this JCL file as an independently schedulable "
            "batch workflow. Each EXEC step becomes either an application batch task, a "
            "managed utility operation, or a data-preparation step. Preserve the dataset "
            "ordering and inline SYSIN content because those values define the job's "
            "runtime contract."
        ),
        "",
        "## 7. Migration Notes",
        "",
        "- Modern equivalent: scheduler workflow with one task per JCL step.",
        "- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.",
        "- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.",
        "",
    ])
    return "\n".join(lines)


def _build_bms_context(screen: Dict[str, Any]) -> Dict[str, Any]:
    fields = screen.get("fields") or []
    by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for field in fields:
        by_type[(field.get("field_type") or "UNKNOWN").upper()].append(field)

    rows = sorted({f.get("row_position") for f in fields if f.get("row_position")})
    colors = Counter((f.get("color") or "").upper() for f in fields if f.get("color"))
    editable = by_type.get("INPUT", [])
    display = by_type.get("OUTPUT", [])
    labels = by_type.get("LABEL", [])

    return {
        "field_count": len(fields),
        "input_fields": editable,
        "output_fields": display,
        "label_fields": labels,
        "rows": rows,
        "colors": colors,
    }


def _write_bms_doc(screen: Dict[str, Any], ctx: Dict[str, Any]) -> str:
    screen_name = screen.get("screen_name") or "UNKNOWN"
    associated_program = screen.get("associated_program") or "not present in extracted data"
    rows = ctx["rows"]
    row_span = f"rows {min(rows)} through {max(rows)}" if rows else "no row positions extracted"

    lines = [
        f"# BMS English Documentation: {screen_name}",
        "",
        "## 1. Screen Purpose",
        "",
        (
            f"`{screen_name}` is a BMS screen map in mapset `{screen.get('mapset_name') or '-'}` "
            f"with map name `{screen.get('map_name') or '-'}`. It is associated with program "
            f"`{associated_program}` and contains {ctx['field_count']} extracted field(s) across {row_span}."
        ),
        "",
        "## 2. User Interaction Model",
        "",
        (
            f"The screen exposes {len(ctx['input_fields'])} editable input field(s), "
            f"{len(ctx['output_fields'])} output/display field(s), and "
            f"{len(ctx['label_fields'])} label/decorative field(s). "
            "Input fields represent values the terminal user can provide. Output fields "
            "represent values the backing CICS program prepares and sends to the terminal."
        ),
        "",
        "## 3. Input Fields",
        "",
    ]

    if ctx["input_fields"]:
        for field in ctx["input_fields"]:
            lines.append(
                f"- `{field.get('field_name')}` at row {field.get('row_position')}, "
                f"column {field.get('col_position')}, length {field.get('length')}: "
                f"terminal input field with attributes `{field.get('attributes') or '-'}`."
            )
    else:
        lines.append("- No editable input fields were extracted for this map.")

    lines.extend(["", "## 4. Display Fields", ""])
    if ctx["output_fields"]:
        for field in ctx["output_fields"][:40]:
            lines.append(
                f"- `{field.get('field_name')}` at row {field.get('row_position')}, "
                f"column {field.get('col_position')}, length {field.get('length')}: "
                f"display value initialized as `{field.get('initial_value') or ''}`."
            )
        if len(ctx["output_fields"]) > 40:
            lines.append(f"- {len(ctx['output_fields']) - 40} additional display fields are present.")
    else:
        lines.append("- No output/display fields were extracted for this map.")

    label_samples = [label for label in (_field_label(f) for f in ctx["label_fields"]) if label][:25]
    colors = [f"{color} ({count})" for color, count in ctx["colors"].most_common()]
    lines.extend([
        "",
        "## 5. Labels and Layout",
        "",
        f"- Layout labels sampled from the map: {_join_or_none(label_samples, limit=25)}",
        f"- Color usage: {_join_or_none(colors)}",
        "",
        "## 6. Program and Navigation Context",
        "",
        (
            f"The extracted program link is `{associated_program}`. In a CICS migration, this "
            "screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands "
            "to determine submit, validation, and navigation behavior."
        ),
        "",
        "## 7. Migration Notes",
        "",
        "- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.",
        "- Preserve field lengths and row/column grouping as validation and layout hints.",
        "- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.",
        "- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.",
        "",
    ])
    return "\n".join(lines)


def _write_bms_file_doc(bms_file: Dict[str, Any], ctx: Dict[str, Any]) -> str:
    file_name = bms_file.get("file_name") or "UNKNOWN"
    mapsets = bms_file.get("mapset_names") or []
    programs = bms_file.get("associated_programs") or []
    transactions = bms_file.get("transaction_ids") or []
    source_meta = bms_file.get("source_metadata") or {}
    readme_mapping = bms_file.get("readme_mapping") or {}
    program_evidence = bms_file.get("program_evidence") or []
    business_name = readme_mapping.get("business_name") or source_meta.get("title") or "not present in extracted data"
    business_description = readme_mapping.get("description") or "not present in extracted data"
    lines = [
        f"# BMS File English Documentation: {file_name}",
        "",
        "## 1. Executive Summary",
        "",
        (
            f"`{file_name}` is a BMS source file that defines {ctx['screen_count']} extracted map(s)/screen(s) "
            f"across mapset(s) {_join_or_none(mapsets)}. The extracted data links this file to "
            f"{_join_or_none(programs)} and transaction id(s) {_join_or_none(transactions)}. "
            f"The business-facing title is {business_name}."
        ),
        "",
        "## 2. File and Mapset Context",
        "",
        f"- Source file: `{bms_file.get('file_path') or '-'}`",
        f"- Mapset names: {_join_or_none(mapsets)}",
        f"- Associated programs: {_join_or_none(programs)}",
        f"- Transaction ids: {_join_or_none(transactions)}",
        f"- Business name/title: {business_name}",
        f"- Business description: {business_description}",
        f"- DFHMSD controls: {_join_or_none([f'{k}={v}' for k, v in (source_meta.get('dfhmsd_controls') or {}).items()], limit=20)}",
        "",
        "## 3. Map-by-Map Structure",
        "",
    ]
    for item in ctx["map_summaries"]:
        lines.append(
            f"- `{item['screen_name']}` / map `{item['map_name']}`: "
            f"{item['field_count']} total field(s), {item['input_count']} input, "
            f"{item['output_count']} output, {item['label_count']} label, rows {item['row_span']}, size {item['size']}."
        )

    label_samples: List[str] = []
    for screen in bms_file.get("screens") or []:
        for field in screen.get("fields") or []:
            if (field.get("field_type") or "").upper() == "LABEL":
                text = _field_label(field)
                if text and text not in label_samples:
                    label_samples.append(text)
            if len(label_samples) >= 20:
                break
        if len(label_samples) >= 20:
            break

    colors = [f"{color} ({count})" for color, count in ctx["colors"].most_common()]
    lines.extend([
        "",
        "## 4. User Interaction Flow",
        "",
        (
            f"Across the file, the extracted maps expose {len(ctx['input_fields'])} editable field occurrence(s) "
            f"and {len(ctx['output_fields'])} display field occurrence(s). This indicates the file supports "
            "interactive CICS-style terminal flows where users enter values into unprotected fields and receive "
            "program-populated output fields on the returned map."
        ),
        "",
        (
            "Repository evidence should be used to confirm the live terminal flow. "
            + (
                f"Linked COBOL programs include {_join_or_none([row.get('program_id') for row in program_evidence], limit=8)}."
                if program_evidence else
                "No additional repository linkage was inferred beyond extracted metadata."
            )
        ),
        "",
        "## 5. Shared Field and Layout Patterns",
        "",
        f"- Representative labels: {_join_or_none(label_samples, limit=20)}",
        f"- Color usage: {_join_or_none(colors)}",
        "- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.",
        "- Command-key/footer hints: " + _join_or_none(ctx.get("command_hints") or [], limit=12),
    ])
    repeated_groups = ctx.get("repeated_groups") or []
    if repeated_groups:
        lines.extend([
            "",
            "### Repeating Regions",
            "",
        ])
        for group in repeated_groups[:12]:
            lines.append(
                f"- Field family `{group['prefix']}` repeats {group['occurrences']} time(s) "
                f"with suffixes {', '.join(group['suffixes'])} across rows {group['row_span']}."
            )
    lines.extend([
        "",
        "## 6. Validation and Navigation Considerations",
        "",
        (
            "The BMS file alone describes screen structure, not the full navigation logic. Confirm SEND MAP, "
            "RECEIVE MAP, PF-key handling, and validation behavior in the associated CICS programs before migration."
        ),
        "- Review COPY-book usage and SEND/RECEIVE MAP statements in the linked COBOL programs to validate field direction and paging behavior.",
        "",
        "## 7. Modernization Guidance",
        "",
        "- Treat this BMS file as a UI contract for one terminal interaction area or flow segment.",
        "- Map input fields to modern form controls and output fields to read-only display elements.",
        "- Preserve repeated row groups as table or list components rather than flattening them into unrelated fields.",
        "- Preserve screen grouping, command-key prompts, and labels when designing the replacement web or API-driven UI.",
        "- Validate transaction routing, per-map behavior, paging/navigation, and error-message handling in the linked programs.",
        "",
    ])
    return "\n".join(lines)


def _context_node(state: ArtifactDocState) -> Dict[str, Any]:
    if state["artifact_type"] == "JCL":
        return {"context": _build_jcl_context(state["raw"])}
    if state["artifact_type"] == "BMS_FILE":
        return {"context": _build_bms_file_context(state["raw"])}
    return {"context": _build_bms_context(state["raw"])}


def _writer_node(state: ArtifactDocState) -> Dict[str, Any]:
    if state["artifact_type"] == "JCL":
        draft = _write_jcl_doc(state["raw"], state["context"])
    elif state["artifact_type"] == "BMS_FILE":
        draft = _write_bms_file_doc(state["raw"], state["context"])
    else:
        draft = _write_bms_doc(state["raw"], state["context"])
    return {"draft": draft}


def _critique_node(state: ArtifactDocState) -> Dict[str, Any]:
    required = ["Business Purpose" if state["artifact_type"] == "JCL" else "Executive Summary"]
    if state["artifact_type"] == "JCL":
        required.extend(["Step-by-Step Flow", "Data Movement", "Migration Notes"])
    elif state["artifact_type"] == "BMS_FILE":
        required.extend(["File and Mapset Context", "Map-by-Map Structure", "User Interaction Flow", "Modernization Guidance"])
    else:
        required.extend(["User Interaction Model", "Input Fields", "Display Fields", "Migration Notes"])

    issues = [f"Missing section: {section}" for section in required if section not in state.get("draft", "")]
    return {
        "critique_passed": not issues,
        "critique_feedback": "\n".join(issues),
    }


def _format_node(state: ArtifactDocState) -> Dict[str, Any]:
    text = state.get("draft", "").strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return {"formatted_doc": text}


def _ground_node(state: ArtifactDocState) -> Dict[str, Any]:
    doc = state.get("formatted_doc") or state.get("draft", "")
    subject = state.get("subject") or ""
    issues = []
    if subject and subject not in doc:
        issues.append(f"Document does not mention source artifact {subject}.")
    banned = ["presumably", "likely", "might", "could be inferred"]
    found = [word for word in banned if word in doc.lower()]
    if found:
        issues.append("Speculative wording found: " + ", ".join(found))
    return {
        "grounding_passed": not issues,
        "grounding_feedback": "\n".join(issues),
    }


def _artifact_writer_prompt(artifact_type: str, subject: str, context: str, feedback: str = "") -> str:
    if artifact_type == "JCL":
        sections = """1. Executive Summary - what this JCL job does and why it exists
2. Batch Runtime Context - owner/maintainer clues, notify routing, scheduler/trigger evidence, job class/message class, invoked programs/utilities
3. Step-by-Step Job Flow - every EXEC step in order, what it does, inputs, outputs, SYSIN
4. Dataset and Dependency Context - datasets read/written, downstream jobs that reference the managed dataset, and any peer/upstream references found
5. Source Record Layout - describe the flat-file source layout evidence, including physical record structure, logical field layout, and explicitly note encoding when absent
6. Operational Controls - return-code/COND behavior, restart considerations, utility dependencies
7. Modernization Guidance - modern workflow equivalent, target services, migration risks"""
    elif artifact_type == "BMS_FILE":
        sections = """1. Executive Summary - what this BMS source file represents and the user/business task it supports
2. File and Mapset Context - file path, mapset names, DFHMSD controls, associated programs, transaction ids
3. Map-by-Map Structure - every map/screen in the file, field counts, role, size, and layout observations
4. User Interaction Flow - what users see, enter, page through, confirm, and receive back across the file
5. Shared Field and Layout Patterns - important input/output fields, labels, attributes, colors, field lengths, repeating rows or grid patterns, command-key hints
6. Validation and Navigation Considerations - what must be confirmed from linked CICS programs and COPY/SEND/RECEIVE usage
7. Modernization Guidance - modern UI equivalent, API boundary, migration risks"""
    else:
        sections = """1. Executive Summary - what this BMS screen represents and the business task it supports
2. Screen and Program Context - map, mapset, transaction/program relationship
3. User Interaction Flow - what the user sees, enters, submits, and receives back
4. Field-Level Behavior - input fields, output fields, labels, field lengths, attributes
5. Validation and Navigation Considerations - what must be confirmed from the CICS program
6. Modernization Guidance - modern UI equivalent, API boundary, migration risks"""

    feedback_block = (
        f"\n\nPREVIOUS CRITIQUE FEEDBACK - address every issue:\n{feedback}\n"
        "Rewrite the complete document."
    ) if feedback else ""

    return f"""Write standalone English documentation for {artifact_type} artifact "{subject}".

This is NOT COBOL program documentation. It is a first-class artifact document for a modernization team.

Required sections:
{sections}

Rules:
- Use the concrete names, steps, fields, datasets, programs, and values from SYSTEM DATA.
- Do not invent missing facts.
- If a fact is missing, write "(not present in extracted data)".
- Write in clear flowing prose with concise bullets where useful.
- End with migration guidance specific to this artifact.

{feedback_block}

SYSTEM DATA:
{context}

Write the complete document now."""


def _artifact_critique_prompt(artifact_type: str, subject: str, draft: str) -> str:
    if artifact_type == "JCL":
        required = "Executive Summary, Batch Runtime Context, Step-by-Step Job Flow, Dataset and Dependency Context, Source Record Layout, Operational Controls, Modernization Guidance"
    elif artifact_type == "BMS_FILE":
        required = "Executive Summary, File and Mapset Context, Map-by-Map Structure, User Interaction Flow, Shared Field and Layout Patterns, Validation and Navigation Considerations, Modernization Guidance"
    else:
        required = "Executive Summary, Screen and Program Context, User Interaction Flow, Field-Level Behavior, Validation and Navigation Considerations, Modernization Guidance"
    return f"""Review this standalone {artifact_type} documentation for "{subject}".

Check:
1. Are all required sections present? Required: {required}
2. Does the document use concrete extracted names rather than generic language?
3. Does it avoid invented behavior and speculation?
4. Is the migration guidance specific to the artifact?

DOCUMENT:
{draft[:9000]}{"...[truncated]" if len(draft) > 9000 else ""}

Respond with JSON only: {{"passed": true/false, "issues": ["specific issue"]}}"""


def _artifact_agent_write_node(state: ArtifactDocState) -> Dict[str, Any]:
    iteration = state.get("iteration", 0)
    feedback = state.get("critique_feedback", "")
    console.print(
        f"[cyan]  Artifact Writer: {state['artifact_type']} / {state['subject']} "
        f"(iteration {iteration + 1})[/cyan]"
    )
    llm = _get_llm()
    prompt = _artifact_writer_prompt(
        state["artifact_type"],
        state["subject"],
        state["context"],  # type: ignore[arg-type]
        feedback,
    )
    response = llm.invoke([
        SystemMessage(content=ARTIFACT_WRITER_SYSTEM),
        HumanMessage(content=prompt),
    ])
    return {"draft": response.content, "iteration": iteration + 1}


def _artifact_agent_critique_node(state: ArtifactDocState) -> Dict[str, Any]:
    console.print("[cyan]  Artifact Critique: reviewing draft...[/cyan]")
    llm = _get_llm()
    prompt = _artifact_critique_prompt(state["artifact_type"], state["subject"], state.get("draft", ""))
    response = llm.invoke([
        SystemMessage(content=ARTIFACT_CRITIQUE_SYSTEM),
        HumanMessage(content=prompt),
    ])
    content = response.content.strip()
    try:
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        result = ArtifactCritiqueResult.model_validate(json.loads(content))
    except Exception:
        match = re.search(r"\{[\s\S]*\}", content)
        try:
            result = ArtifactCritiqueResult.model_validate(json.loads(match.group())) if match else ArtifactCritiqueResult()
        except Exception:
            result = ArtifactCritiqueResult(passed=False, issues=["Critique response was not valid JSON."])
    return {
        "critique_passed": result.passed,
        "critique_feedback": "\n".join(f"- {issue}" for issue in result.issues),
    }


def _artifact_agent_format_node(state: ArtifactDocState) -> Dict[str, Any]:
    console.print("[cyan]  Artifact Formatter: cleaning document...[/cyan]")
    llm = _get_llm()
    response = llm.invoke([
        SystemMessage(content=ARTIFACT_FORMATTER_SYSTEM),
        HumanMessage(content=f"Clean and format this markdown document. Return the complete document:\n\n{state.get('draft', '')}"),
    ])
    return {"formatted_doc": response.content}


def _artifact_agent_ground_node(state: ArtifactDocState) -> Dict[str, Any]:
    doc = state.get("formatted_doc") or state.get("draft", "")
    context = str(state.get("context") or "")
    subject = state.get("subject") or ""
    issues = []
    if subject.upper() not in doc.upper():
        issues.append(f"Document does not mention artifact {subject}.")
    for token in ["likely", "presumably", "might", "may be handled", "could be"]:
        if token in doc.lower():
            issues.append(f"Speculative wording found: {token}")
    if state["artifact_type"] == "JCL":
        for line in context.splitlines():
            if line.startswith("### Step "):
                step = line.split(":", 1)[1].strip()
                if step and step.upper() not in doc.upper():
                    issues.append(f"Missing JCL step {step}.")
    elif state["artifact_type"] == "BMS_FILE":
        for key in ("BMS File:", "Mapset Names:", "Associated Programs:"):
            match = re.search(rf"^{re.escape(key)}\s*(.+)$", context, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                if value and "not present in extracted data" not in value.lower() and value.upper() not in doc.upper():
                    issues.append(f"Missing BMS file fact {key} {value}.")
    else:
        for key in ("Screen Name:", "Map Name:", "Mapset Name:"):
            match = re.search(rf"^{re.escape(key)}\s*(.+)$", context, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                if value and value != "-" and value.upper() not in doc.upper():
                    issues.append(f"Missing BMS fact {key} {value}.")
    issues = list(dict.fromkeys(issues))
    return {
        "grounding_passed": not issues,
        "grounding_feedback": "\n".join(f"- {issue}" for issue in issues),
        "critique_passed": not issues,
        "critique_feedback": "\n".join(f"- {issue}" for issue in issues),
    }


def _artifact_agent_save_node(state: ArtifactDocState) -> Dict[str, Any]:
    if not state.get("grounding_passed", True):
        return {"saved": False}
    doc = state.get("formatted_doc") or state.get("draft", "")
    mode = state["artifact_type"]
    subject = state["subject"]
    try:
        conn = _sqlite_connect(state["db_path"])
        conn.execute("""
            CREATE TABLE IF NOT EXISTS generated_docs (
                mode TEXT NOT NULL,
                subject TEXT NOT NULL,
                document_text TEXT NOT NULL,
                context_metadata_json TEXT,
                coverage_ledger_json TEXT,
                generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (mode, subject)
            )
        """)
        conn.execute("""
            INSERT OR REPLACE INTO generated_docs (
                mode, subject, document_text, context_metadata_json, coverage_ledger_json, generated_at
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            mode,
            subject,
            doc,
            json.dumps({"artifact_type": mode, "source": "artifact_doc_agent"}),
            json.dumps({}),
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        console.print(f"[yellow]  Artifact Save: DB save failed: {e}[/yellow]")

    output_path = state.get("output_path")
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(doc, encoding="utf-8")
    return {"saved": True}


def _artifact_should_revise(state: ArtifactDocState) -> str:
    if not state.get("critique_passed", False) and state.get("iteration", 0) < state.get("max_iterations", 2):
        return "revise"
    return "format"


def _artifact_should_save_or_revise(state: ArtifactDocState) -> str:
    if not state.get("grounding_passed", True) and state.get("iteration", 0) < state.get("max_iterations", 2):
        return "revise"
    return "save"


def run_artifact_doc_pipeline(
    artifact_type: str,
    subject: str,
    context: str,
    db_path: str,
    output_path: str | Path | None = None,
    max_iterations: int = 3,
) -> str:
    """Run Writer -> Critique -> Formatter -> Grounding -> Save for one JCL/BMS artifact."""
    artifact_type = artifact_type.upper()
    if artifact_type not in {"JCL", "BMS", "BMS_FILE"}:
        raise ValueError("artifact_type must be JCL, BMS, or BMS_FILE")

    initial: ArtifactDocState = {
        "artifact_type": artifact_type,
        "subject": subject,
        "context": context,
        "draft": "",
        "critique_passed": False,
        "critique_feedback": "",
        "formatted_doc": "",
        "grounding_passed": True,
        "grounding_feedback": "",
        "db_path": db_path,
        "output_path": str(output_path) if output_path else "",
        "iteration": 0,
        "max_iterations": max_iterations,
        "saved": False,
    }

    workflow = StateGraph(ArtifactDocState)
    workflow.add_node("write", _artifact_agent_write_node)
    workflow.add_node("critique", _artifact_agent_critique_node)
    workflow.add_node("format", _artifact_agent_format_node)
    workflow.add_node("ground", _artifact_agent_ground_node)
    workflow.add_node("save", _artifact_agent_save_node)
    workflow.add_edge(START, "write")
    workflow.add_edge("write", "critique")
    workflow.add_conditional_edges("critique", _artifact_should_revise, {"revise": "write", "format": "format"})
    workflow.add_edge("format", "ground")
    workflow.add_conditional_edges("ground", _artifact_should_save_or_revise, {"revise": "write", "save": "save"})
    workflow.add_edge("save", END)
    final = workflow.compile().invoke(initial)
    return final.get("formatted_doc") or final.get("draft", "")


def _run_artifact_agent(artifact_type: str, subject: str, raw: Dict[str, Any]) -> ArtifactDocState:
    initial: ArtifactDocState = {
        "artifact_type": artifact_type,
        "subject": subject,
        "raw": raw,
        "context": {},
        "draft": "",
        "critique_passed": False,
        "critique_feedback": "",
        "formatted_doc": "",
        "grounding_passed": False,
        "grounding_feedback": "",
    }

    if StateGraph is None:
        state = dict(initial)
        for node in (_context_node, _writer_node, _critique_node, _format_node, _ground_node):
            state.update(node(state))  # type: ignore[arg-type]
        return state  # type: ignore[return-value]

    workflow = StateGraph(ArtifactDocState)
    workflow.add_node("context", _context_node)
    workflow.add_node("writer", _writer_node)
    workflow.add_node("critique", _critique_node)
    workflow.add_node("formatter", _format_node)
    workflow.add_node("grounding", _ground_node)
    workflow.add_edge(START, "context")
    workflow.add_edge("context", "writer")
    workflow.add_edge("writer", "critique")
    workflow.add_edge("critique", "formatter")
    workflow.add_edge("formatter", "grounding")
    workflow.add_edge("grounding", END)
    return workflow.compile().invoke(initial)


class StandaloneArtifactDocGenerator:
    """Generate standalone English docs for JCL and BMS artifacts."""

    def __init__(self, db_loader: SQLiteLoader, output_dir: str | Path = "docs/standalone-artifacts"):
        self.db = db_loader
        self.output_dir = Path(output_dir)
        self.jcl_dir = self.output_dir / "jcl"
        self.bms_dir = self.output_dir / "bms"

    def generate_all(self) -> Dict[str, int]:
        generated = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.jcl_dir.mkdir(parents=True, exist_ok=True)
        self.bms_dir.mkdir(parents=True, exist_ok=True)

        jcl_count = self._generate_jcl_docs(generated)
        bms_count = self._generate_bms_docs(generated)
        self._generate_root_index(jcl_count, bms_count, generated)
        self._generate_agent_framework_doc(generated)

        console.print(
            f"[green]OK - Standalone artifact docs: {jcl_count} JCL, {bms_count} BMS[/green]"
        )
        return {"jcl": jcl_count, "bms": bms_count}

    def _generate_jcl_docs(self, generated: str) -> int:
        jobs = self.db.get_all_jcl_jobs()
        index_rows = [
            "# Standalone JCL English Documentation",
            "",
            f"> Generated {generated}",
            "",
            "| Job | Source File | Steps | Programs |",
            "|-----|-------------|-------|----------|",
        ]

        count = 0
        for job in jobs:
            job_name = job.get("job_name") or "UNKNOWN"
            details = self.db.get_jcl_job_details(job_name)
            if not details:
                continue
            doc = _write_jcl_doc(details, _build_jcl_context(details, self.db))
            path = self.jcl_dir / f"{_safe_name(job_name)}.md"
            path.write_text(doc, encoding="utf-8")
            programs = details.get("programs_called") or []
            index_rows.append(
                f"| [{job_name}]({_safe_name(job_name)}.md) | "
                f"`{details.get('file_name') or '-'}` | {len(details.get('steps') or [])} | "
                f"{_join_or_none(programs, limit=8)} |"
            )
            count += 1

        index_rows.append("")
        (self.jcl_dir / "INDEX.md").write_text("\n".join(index_rows), encoding="utf-8")
        return count

    def _generate_bms_docs(self, generated: str) -> int:
        screens = self.db.get_all_screens()
        file_paths = sorted({s.get("file_path") for s in screens if s.get("file_path")}, key=lambda p: str(p).lower())
        self.bms_dir.mkdir(parents=True, exist_ok=True)
        index_rows = [
            "# Standalone BMS English Documentation",
            "",
            f"> Generated {generated}",
            "",
            "| BMS File | Mapsets | Programs | Transactions | Maps |",
            "|----------|---------|----------|--------------|------|",
        ]

        count = 0
        for file_path in file_paths:
            details = build_bms_file_artifact(self.db, file_path)
            if not details:
                continue
            file_name = details.get("file_name") or Path(str(file_path)).name
            final = _run_artifact_agent("BMS_FILE", file_name, details)
            doc = final.get("formatted_doc") or final.get("draft") or ""
            safe_subject = str(file_path).replace("\\", "_").replace("/", "_").replace(":", "_")
            path = self.bms_dir / f"{safe_subject}.md"
            path.write_text(doc, encoding="utf-8")
            index_rows.append(
                f"| [{file_name}]({safe_subject}.md) | "
                f"`{_join_or_none(details.get('mapset_names') or [])}` | "
                f"`{_join_or_none(details.get('associated_programs') or [], limit=6)}` | "
                f"`{_join_or_none(details.get('transaction_ids') or [], limit=6)}` | "
                f"{len(details.get('screens') or [])} |"
            )
            count += 1

        index_rows.append("")
        (self.bms_dir / "INDEX.md").write_text("\n".join(index_rows), encoding="utf-8")
        return count

    def _generate_root_index(self, jcl_count: int, bms_count: int, generated: str) -> None:
        content = f"""# Standalone Artifact English Documentation

> Generated {generated}

This section is separate from the COBOL program documentation generator. It
documents non-COBOL mainframe artifacts as first-class migration inputs.

## Sections

| Section | Purpose | Count |
|---------|---------|-------|
| [JCL Jobs](jcl/INDEX.md) | English explanations of batch jobs, steps, datasets, utilities, and migration notes | {jcl_count} |
| [BMS Screens](bms/INDEX.md) | English explanations of screen purpose, fields, interaction model, and migration notes | {bms_count} |
| [Agent Framework](AGENT-FRAMEWORK.md) | The artifact documentation agent workflow used to create this section | - |
"""
        (self.output_dir / "INDEX.md").write_text(content, encoding="utf-8")

    def _generate_agent_framework_doc(self, generated: str) -> None:
        content = f"""# Artifact Documentation Agent Framework

> Generated {generated}

The standalone JCL/BMS documentation section uses a dedicated artifact agent
pipeline, separate from the COBOL `DocGenerator`.

## Workflow

1. Context Builder: reads normalized JCL or BMS records from SQLite.
2. Writer: produces a source-grounded English document for one artifact.
3. Critique: checks that the artifact-specific required sections are present.
4. Formatter: normalizes Markdown spacing and structure.
5. Grounding: verifies the document names the source artifact and avoids speculative wording.
6. Publisher: writes the standalone Markdown file and updates the artifact index.

## Artifact Types

- JCL jobs are documented as schedulable batch workflows with job purpose, step flow, DD datasets, utility usage, and migration notes.
- BMS screens are documented as user-interface artifacts with screen purpose, field behavior, layout, associated program, and migration notes.

## Implementation

The implementation lives in `doc_demo/src/artifact_doc_agent.py`. If LangGraph
is available, the stages are wired as a `StateGraph`. If LangGraph is not
available, the same stages run sequentially so deterministic documentation can
still be generated locally.
"""
        (self.output_dir / "AGENT-FRAMEWORK.md").write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate standalone JCL/BMS English documentation")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="SQLite database path")
    parser.add_argument("--schema", default="schemas/cobol_knowledge.sql", help="SQLite schema path")
    parser.add_argument("--output", default="docs/standalone-artifacts", help="Output documentation directory")
    args = parser.parse_args()

    loader = SQLiteLoader(args.db, args.schema)
    loader.connect()
    try:
        StandaloneArtifactDocGenerator(loader, args.output).generate_all()
    finally:
        loader.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
