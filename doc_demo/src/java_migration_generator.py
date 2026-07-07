"""Java migration generator — Program/Module/Application level, Neo4j-backed."""

from __future__ import annotations
import json, os, re, time
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


# ── Neo4j context builders ──────────────────────────────────────────────

def _neo4j_driver():
    from neo4j import GraphDatabase
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    pwd = os.getenv("NEO4J_PASSWORD", "password")
    return GraphDatabase.driver(uri, auth=(user, pwd))


def _program_node_context(session, program_id: str) -> Dict[str, Any]:
    rec = session.run("MATCH (p:Program {id:$id}) RETURN p", id=program_id).single()
    prog = dict(rec["p"]) if rec else {}

    paragraphs = [dict(r["para"]) for r in session.run(
        "MATCH (p:Program {id:$id})-[:CONTAINS]->(para:Paragraph) RETURN para",
        id=program_id)]

    calls = [r["c.id"] for r in session.run(
        "MATCH (p:Program {id:$id})-[:CALLS]->(c:Program) RETURN c.id AS `c.id`",
        id=program_id)]
    called_by = [r["c.id"] for r in session.run(
        "MATCH (c:Program)-[:CALLS]->(p:Program {id:$id}) RETURN c.id AS `c.id`",
        id=program_id)]

    files = [dict(r) for r in session.run("""
        MATCH (p:Program {id:$id})-[rel:READS|WRITES]->(f:File)
        RETURN f.name AS name, type(rel) AS access""", id=program_id)]

    copybooks = [r["cb.name"] for r in session.run(
        "MATCH (p:Program {id:$id})-[:INCLUDES]->(cb:Copybook) RETURN cb.name AS `cb.name`",
        id=program_id)]

    rules = [dict(r["r"]) for r in session.run(
        "MATCH (p:Program {id:$id})-[:APPLIES]->(r:BusinessRule) RETURN r LIMIT 30",
        id=program_id)]

    screens = [dict(r["s"]) for r in session.run(
        "MATCH (p:Program {id:$id})-[:USES_SCREEN]->(s:Screen) RETURN s",
        id=program_id)]

    cics = session.run(
        "MATCH (p:Program {id:$id})-[:USES_CICS]->(cp:CicsProfile) RETURN cp",
        id=program_id).single()
    cics_profile = dict(cics["cp"]) if cics else {}

    db_tables = [dict(r) for r in session.run("""
        MATCH (p:Program {id:$id})-[rel:READS_TABLE|WRITES_TABLE]->(t:DbTable)
        RETURN t.name AS table_name, type(rel) AS access, rel.command AS command""",
        id=program_id)]

    ims_segments = [dict(r) for r in session.run("""
        MATCH (p:Program {id:$id})-[rel:READS_IMS_SEGMENT|WRITES_IMS_SEGMENT]->(s:ImsSegment)
        RETURN s.name AS segment, type(rel) AS access, rel.functionCode AS functionCode""",
        id=program_id)]

    jcl_jobs = [dict(r) for r in session.run("""
        MATCH (j:JclJob)-[:EXECUTES]->(p:Program {id:$id})
        RETURN j.name AS job_name, j.description AS description""",
        id=program_id)]

    anomalies = [dict(r["a"]) for r in session.run(
        "MATCH (p:Program {id:$id})-[:HAS_ANOMALY]->(a:CodeAnomaly) RETURN a LIMIT 20",
        id=program_id)]

    fields = [dict(r["field"]) for r in session.run(
        "MATCH (p:Program {id:$id})-[:DECLARES_FIELD]->(field:DataField) RETURN field LIMIT 60",
        id=program_id)]

    return {
        "program": prog,
        "paragraphs": paragraphs,
        "calls": calls,
        "called_by": called_by,
        "files": files,
        "copybooks": copybooks,
        "business_rules": rules,
        "screens": screens,
        "cics_profile": cics_profile,
        "db_tables": db_tables,
        "ims_segments": ims_segments,
        "jcl_jobs": jcl_jobs,
        "anomalies": anomalies,
        "fields": fields,
    }


def build_program_java_context(program_id: str, project_root: str | Path) -> Dict[str, Any]:
    """Single-program context, sourced from Neo4j."""
    project_root = Path(project_root)
    driver = _neo4j_driver()
    try:
        with driver.session() as session:
            ctx = _program_node_context(session, program_id)
    finally:
        driver.close()

    file_path = ctx["program"].get("filePath")
    source = ""
    if file_path:
        p = Path(file_path)
        if not p.is_absolute():
            p = project_root / p
        if p.exists():
            source = p.read_text(encoding="utf-8", errors="ignore")[:18000]

    ctx["source_excerpt"] = source
    ctx["source_line_count"] = len(source.splitlines())
    ctx["evidence_source"] = "Neo4j graph (Program/Paragraph/File/Copybook/BusinessRule/Screen/CicsProfile/DbTable/ImsSegment/JclJob/CodeAnomaly nodes)"
    return ctx


def build_module_java_context(module_name: str, project_root: str | Path) -> Dict[str, Any]:
    """Module-level context: all programs in the module + their interconnections."""
    driver = _neo4j_driver()
    try:
        with driver.session() as session:
            rec = session.run("""
                MATCH (m:Module {name:$name})-[:CONTAINS]->(p:Program)
                RETURN p.id AS id""", name=module_name).data()
            program_ids = [r["id"] for r in rec]

            programs = []
            for pid in program_ids:
                programs.append(_program_node_context(session, pid))

            # internal call edges
            internal_calls = session.run("""
                MATCH (m:Module {name:$name})-[:CONTAINS]->(a:Program)
                MATCH (m)-[:CONTAINS]->(b:Program)
                MATCH (a)-[:CALLS]->(b)
                RETURN a.id AS caller, b.id AS callee""", name=module_name).data()

            shared_copybooks = session.run("""
                MATCH (m:Module {name:$name})-[:CONTAINS]->(p:Program)-[:INCLUDES]->(cb:Copybook)
                WITH cb, collect(DISTINCT p.id) AS users
                WHERE size(users) > 1
                RETURN cb.name AS copybook, users""", name=module_name).data()
    finally:
        driver.close()

    return {
        "module_name": module_name,
        "programs": programs,
        "internal_calls": internal_calls,
        "shared_copybooks": shared_copybooks,
        "evidence_source": "Neo4j graph — Module/Program/Copybook nodes and CALLS relationships",
    }


def build_application_java_context() -> Dict[str, Any]:
    """Application-level: module summaries + cross-module calls + JCL + screens."""
    driver = _neo4j_driver()
    try:
        with driver.session() as session:
            modules = session.run("""
                MATCH (m:Module)-[:CONTAINS]->(p:Program)
                RETURN m.name AS module, collect(p.id) AS programs""").data()

            cross_module_calls = session.run("""
                MATCH (m1:Module)-[:CONTAINS]->(a:Program)-[:CALLS]->(b:Program)<-[:CONTAINS]-(m2:Module)
                WHERE m1 <> m2
                RETURN DISTINCT m1.name AS from_module, m2.name AS to_module,
                       a.id AS caller, b.id AS callee""").data()

            jcl_jobs = session.run("""
                MATCH (j:JclJob)-[:EXECUTES]->(p:Program)
                RETURN j.name AS job, collect(p.id) AS programs""").data()

            screens = session.run("""
                MATCH (p:Program)-[:USES_SCREEN]->(s:Screen)
                RETURN p.id AS program, s.name AS screen, s.mapsetName AS mapset""").data()

            db_tables = session.run("""
                MATCH (p:Program)-[rel:READS_TABLE|WRITES_TABLE]->(t:DbTable)
                RETURN p.id AS program, t.name AS table_name, type(rel) AS access""").data()

            rule_counts = session.run("""
                MATCH (p:Program)-[:APPLIES]->(r:BusinessRule)
                RETURN r.category AS category, count(r) AS cnt""").data()
    finally:
        driver.close()

    return {
        "modules": modules,
        "cross_module_calls": cross_module_calls,
        "jcl_jobs": jcl_jobs,
        "screens": screens,
        "db_tables": db_tables,
        "rule_counts": rule_counts,
        "evidence_source": "Neo4j graph — full application: Module/Program/JclJob/Screen/DbTable/BusinessRule nodes",
    }


# ── LLM prompts ─────────────────────────────────────────────────────────

def _extract_code(text: str) -> str:
    m = re.search(r"```(?:java)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else text.strip()


def _llm():
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.environ.get("GEMINI_API_KEY"),
        temperature=0.1,
        max_output_tokens=24000,
    )


def _llm_metrics(response, start_time, model_name):
    usage = getattr(response, "usage_metadata", None) or {}
    meta = getattr(response, "response_metadata", None) or {}
    tok = meta.get("token_usage") or meta.get("usage_metadata") or {}
    def _m(*keys):
        for src in (usage, tok):
            for k in keys:
                if src.get(k) is not None:
                    return int(src[k])
        return None
    return {
        "llm_duration_seconds": time.perf_counter() - start_time,
        "prompt_tokens": _m("input_tokens", "prompt_token_count", "prompt_tokens"),
        "output_tokens": _m("output_tokens", "candidates_token_count", "completion_tokens"),
        "total_tokens": _m("total_tokens", "total_token_count"),
        "model_name": meta.get("model_name") or model_name,
    }


# ── Fallback (no-LLM) skeletons ───────────────────────────────────────────

def _java_class_name(program_id: str) -> str:
    return program_id.title().replace("_", "").replace("-", "") + "Migration"


def _fallback_program_java(ctx: Dict[str, Any]) -> str:
    pid = ctx["program"].get("id", "Program")
    paragraphs = [p.get("name") for p in ctx["paragraphs"] if p.get("name")]
    methods = "\n\n".join(
        f"""    private void {re.sub(r'[^A-Za-z0-9]', '', n.title())}() {{
        // Migrated from COBOL paragraph {n}
    }}""" for n in paragraphs[:10]
    )
    return f"""package com.unisys.migration.carddemo;

/**
 * Demo Java migration skeleton for COBOL program {pid}.
 * Evidence source: {ctx.get('evidence_source')}
 */
public final class {_java_class_name(pid)} {{
{methods}
}}
"""


def _fallback_module_java(ctx: Dict[str, Any]) -> str:
    mod = ctx["module_name"]
    classes = "\n\n".join(_fallback_program_java(p) for p in ctx["programs"])
    return f"// Module: {mod}\n// Evidence: {ctx['evidence_source']}\n\n" + classes


def _fallback_application_java(ctx: Dict[str, Any]) -> str:
    lines = [f"// Application — {len(ctx['modules'])} modules",
             f"// Evidence: {ctx['evidence_source']}"]
    for m in ctx["modules"]:
        lines.append(f"// Module {m['module']}: programs {', '.join(m['programs'])}")
    return "\n".join(lines)


# ── Public generation entry points ────────────────────────────────────────

def generate_java_for_program(loader, program_id: str, project_root: str | Path,
                                use_llm: bool = True) -> Dict[str, Any]:
    context = build_program_java_context(program_id, project_root)

    if not use_llm or not os.environ.get("GEMINI_API_KEY"):
        return {"java_code": _fallback_program_java(context), "context": context,
                "used_llm": False, "llm_metrics": {}}

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    llm = _llm()
    prompt = f"""Convert COBOL program {program_id} into Java for a modernization demo.

Use the Neo4j graph evidence and COBOL source excerpt below. Generate one cohesive
Java class plus small nested records/interfaces where useful.

Requirements:
- Name the class {_java_class_name(program_id)}.
- Map important methods back to COBOL paragraphs in comments.
- If business rules are present, encode them as validation/branch logic with comments citing rule IDs.
- If db_tables are present, generate a repository interface for those tables.
- If ims_segments are present, generate accessor methods named after the segments.
- If screens are present, generate a DTO record matching the screen's input/output fields.
- Use only facts from this context. Do not invent databases, queues, or APIs.
- Return Java code only, no markdown explanation.

CONTEXT JSON:
{json.dumps(context, indent=2, default=str)}

SOURCE EXCERPT:
{context.get('source_excerpt','')[:8000]}
"""
    start = time.perf_counter()
    response = llm.invoke([
        SystemMessage(content="You are a senior Java modernization engineer. Return Java code only."),
        HumanMessage(content=prompt),
    ])
    return {
        "java_code": _extract_code(response.content),
        "context": context,
        "used_llm": True,
        "llm_metrics": _llm_metrics(response, start, model_name),
    }


def generate_java_for_module(module_name: str, project_root: str | Path,
                               use_llm: bool = True) -> Dict[str, Any]:
    context = build_module_java_context(module_name, project_root)

    if not use_llm or not os.environ.get("GEMINI_API_KEY"):
        return {"java_code": _fallback_module_java(context), "context": context,
                "used_llm": False, "llm_metrics": {}}

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    llm = _llm()
    prog_ids = [p["program"].get("id") for p in context["programs"]]
    prompt = f"""Convert the COBOL module "{module_name}" into a cohesive Java package for a
modernization demo.

The module contains these programs: {', '.join(prog_ids)}.

Use the Neo4j graph evidence below (internal call relationships, shared copybooks,
business rules, screens, CICS profiles, DB tables, IMS segments, JCL jobs).

Requirements:
- Generate ONE Java file containing: a package declaration, one class per program
  (named after the program ID, e.g. {_java_class_name(prog_ids[0]) if prog_ids else 'ProgramMigration'}),
  plus shared DTOs/records for any shared copybooks.
- Reflect the internal_calls as method calls between the generated classes
  (caller class invokes callee class's main method).
- For shared copybooks, generate ONE shared record/class used by all programs that reference it.
- Return Java code only, no markdown explanation. Do not truncate.

CONTEXT JSON:
{json.dumps(context, indent=2, default=str)}
"""
    start = time.perf_counter()
    response = llm.invoke([
        SystemMessage(content="You are a senior Java modernization engineer. Return Java code only."),
        HumanMessage(content=prompt),
    ])
    return {
        "java_code": _extract_code(response.content),
        "context": context,
        "used_llm": True,
        "llm_metrics": _llm_metrics(response, start, model_name),
    }


def generate_java_for_application(project_root: str | Path,
                                     use_llm: bool = True) -> Dict[str, Any]:
    context = build_application_java_context()

    if not use_llm or not os.environ.get("GEMINI_API_KEY"):
        return {"java_code": _fallback_application_java(context), "context": context,
                "used_llm": False, "llm_metrics": {}}

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    llm = _llm()
    prompt = f"""Produce a high-level Java package architecture (skeleton classes/interfaces only,
not full method bodies) for modernizing this entire COBOL application.

Use the Neo4j graph evidence below covering all modules, cross-module calls, JCL batch
jobs, BMS screens, and DB2 tables.

Requirements:
- One package per module (com.unisys.migration.carddemo.<module_lowercase>).
- For each module, list the classes that will represent its programs (class names only,
  with a one-line Javadoc comment describing responsibility).
- For cross-module calls, generate a small "ports" interface in the calling module's
  package that the target module's package implements.
- For JCL jobs, generate a @Scheduled batch job class skeleton per job (Spring Batch style),
  with a comment listing the COBOL programs it orchestrates.
- For BMS screens, generate a DTO record per screen (fields as String/BigDecimal placeholders).
- Return Java code only (multiple classes/files concatenated with // ===== FILE: <path> ===== separators),
  no markdown explanation. Do not truncate.

CONTEXT JSON:
{json.dumps(context, indent=2, default=str)}
"""
    start = time.perf_counter()
    response = llm.invoke([
        SystemMessage(content="You are a senior Java modernization engineer. Return Java code only."),
        HumanMessage(content=prompt),
    ])
    return {
        "java_code": _extract_code(response.content),
        "context": context,
        "used_llm": True,
        "llm_metrics": _llm_metrics(response, start, model_name),
    }