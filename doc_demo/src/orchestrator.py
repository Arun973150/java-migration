"""
COBOL Documentation Pipeline Orchestrator

Two enrichment modes:
  [Mode A - Default] Step 1a→1b → Step 2 (JSON enrichment) → Step 3 (SQLite) → Step 5 (Neo4j) → Step 4 (Docs)
  [Mode B - Graph Enrichment] Step 1a→1b → Step 3 (SQLite) → Step 5 (Neo4j) → Step 5b (Neo4j enrichment) → Step 4 (Docs)

Step 1a: Parse JCL files
Step 1b: Parse COBOL with ProLeap -> parsed_output/
Step 2:  Optional LLM Enrichment on JSON (langgraph_enricher) -> enriched_output/ [skipped in Mode B]
Step 3:  Load into SQLite Knowledge Base
Step 4:  Generate Markdown Docs + Streamlit Dashboard
Step 5:  Neo4j Export (Optional)
Step 5b: Neo4j Graph-Based LLM Enrichment [Mode B only]
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Force UTF-8 for stdout/stderr on Windows so Rich's spinner braille characters
# (e.g. ⠋) don't crash cp1252 consoles. Safe no-op on POSIX.
if sys.platform.startswith("win"):
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent))

from proleap_wrapper import ProLeapWrapper
from sqlite_loader import SQLiteLoader
from doc_generator import DocGenerator

# legacy_windows=False keeps Rich on the modern renderer that supports UTF-8 spinners.
console = Console(force_terminal=True, highlight=False, legacy_windows=False)


def detect_cobol_format(repo_path) -> str:
    """Sample a few COBOL files to guess FIXED vs FREE format.
    FIXED format has 6-digit sequence numbers in cols 1-6 and `*` comments
    in col 7. FREE format has no such column rules. Returns 'FIXED' or 'FREE'."""
    import re
    repo = Path(repo_path)
    samples = []
    for ext in (".cbl", ".CBL", ".cob", ".COB"):
        samples.extend(list(repo.rglob(f"*{ext}"))[:5])
        if len(samples) >= 5:
            break
    if not samples:
        return "FIXED"
    fixed_signals = 0
    free_signals = 0
    seq_pat = re.compile(r"^\d{6}")
    for fp in samples[:5]:
        try:
            with open(fp, encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh):
                    if i > 80:
                        break
                    if not line.strip():
                        continue
                    if seq_pat.match(line):
                        fixed_signals += 1
                    elif len(line) > 6 and line[6] == "*":
                        fixed_signals += 1
                    elif line.lstrip().startswith("*>"):
                        free_signals += 1
                    elif len(line) > 0 and line[0] not in (" ", "\t") and not line[0].isdigit():
                        free_signals += 1
        except Exception:
            continue
    return "FIXED" if fixed_signals >= free_signals else "FREE"


def ensure_env():
    if not Path(".env").exists() and Path(".env.example").exists():
        with open(".env.example", "r") as f_in, open(".env", "w") as f_out:
            f_out.write(f_in.read())
    load_dotenv()


def print_banner():
    banner = """
  COBOL Documentation Pipeline (Swimm-Style)
  ProLeap Parser -> SQLite KB -> LLM Enrichment -> Markdown Docs
    """
    console.print(Panel(banner, style="cyan"))


def run_pipeline(
    repo_path: str,
    output_dir: str = "docs",
    groq_api_key: str = None,
    groq_model: str = "llama-3.3-70b-versatile",
    db_path: str = "data/cobol_knowledge.db",
    schema_path: str = "schemas/cobol_knowledge.sql",
    skip_parse: bool = False,
    skip_enrich: bool = False,
    skip_neo4j: bool = True,
    skip_jcl: bool = False,
    neo4j_uri: str = None,
    neo4j_user: str = None,
    neo4j_password: str = None,
    cobol_format: str = None,        # auto-detected if None
    system_name: str = None,
    graph_enrich_after_neo4j: bool = False,  # NEW: Use Neo4j-based enrichment instead of JSON
):
    ensure_env()
    print_banner()

    start_time = datetime.now()
    repo_path = Path(repo_path)
    parsed_dir  = Path("parsed_output")
    enriched_dir = Path("enriched_output")
    jcl_jobs = []
    
    # If using graph-based enrichment, always skip JSON enrichment
    if graph_enrich_after_neo4j:
        skip_enrich = True
        skip_neo4j = False  # Must export to Neo4j to enrich

    # Auto-detect COBOL format if caller didn't specify
    if not cobol_format:
        cobol_format = detect_cobol_format(repo_path)
        console.print(f"[cyan]Auto-detected COBOL format: {cobol_format}[/cyan]")

    console.print(f"[cyan]Repository: {repo_path}[/cyan]")
    console.print(f"[cyan]Output: {output_dir}[/cyan]")
    console.print()

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # ========================================
    # Step 1a: Parse JCL files
    # ========================================
    if not skip_jcl:
        console.print(Panel("[bold]Step 1a: Parsing JCL Files[/bold]", style="blue"))
        try:
            from jcl_parser import JclParser
            jcl_parser = JclParser()
            jcl_jobs_obj = jcl_parser.parse_repository(str(repo_path))
            if jcl_jobs_obj:
                jcl_parser.save_results(jcl_jobs_obj, str(parsed_dir))
                jcl_jobs = [j.to_dict() if hasattr(j, "to_dict") else j for j in jcl_jobs_obj]
                console.print(f"[green]OK - Parsed {len(jcl_jobs)} JCL jobs[/green]")
            else:
                console.print("[yellow]  No JCL files found in repository[/yellow]")
        except Exception as e:
            console.print(f"[yellow]  Warning: JCL parsing failed: {e}. Continuing.[/yellow]")
    else:
        # Try to load from previously saved JSON
        jcl_json = parsed_dir / "jcl_jobs.json"
        if jcl_json.exists():
            import json as _json
            with open(jcl_json) as f:
                jcl_jobs = _json.load(f)
            console.print(f"[yellow]>> Using cached JCL: {len(jcl_jobs)} jobs[/yellow]")
        else:
            console.print("[yellow]>> Skipping JCL parse (no cached data found)[/yellow]")
    console.print()

    # ========================================
    # Step 1b: Parse COBOL with ProLeap (incremental)
    # ========================================
    if not skip_parse:
        console.print(Panel("[bold]Step 1b: Parsing COBOL Repository with ProLeap[/bold]", style="blue"))

        # Load existing file hashes from DB for incremental parsing
        existing_hashes: Dict[str, str] = {}
        try:
            _tmp_loader = SQLiteLoader(db_path, schema_path)
            _tmp_loader.connect()
            _cur = _tmp_loader.conn.cursor()
            _cur.execute("SELECT file_path, file_hash FROM programs WHERE file_hash IS NOT NULL")
            existing_hashes = {row[0]: row[1] for row in _cur.fetchall()}
            _tmp_loader.close()
            if existing_hashes:
                console.print(f"[cyan]  Incremental mode: {len(existing_hashes)} programs already in DB[/cyan]")
        except Exception:
            pass  # Fresh DB — parse everything

        wrapper = ProLeapWrapper(cobol_format=cobol_format)
        parse_results = wrapper.parse_repository(str(repo_path), existing_hashes=existing_hashes)
        wrapper.save_results(parse_results, str(parsed_dir))
        skipped = parse_results.get("skipped", 0)
        console.print(f"[green]OK - Parsed {len(parse_results['programs'])} programs "
                       f"({skipped} skipped unchanged), "
                       f"{len(parse_results['copybooks'])} copybooks, "
                       f"{len(parse_results.get('screens', []))} screens[/green]")
        console.print()
    else:
        console.print("[yellow]>> Skipping parse step (using existing data)[/yellow]")

    # ========================================
    # Step 2: Enrich with LLM (Optional)
    # ========================================
    if not skip_enrich:
        console.print(Panel(f"[bold]Step 2: LLM Enrichment (LangGraph + Gemini API)[/bold]", style="blue"))
        try:
            from langgraph_enricher import CobolEnricher
            enricher = CobolEnricher(
                model=groq_model,
            )
            enrich_results = enricher.enrich_from_file(
                str(parsed_dir / "programs.json"),
                str(parsed_dir / "copybooks.json")
            )
            enricher.save_results(enrich_results, str(enriched_dir))
            console.print(f"[green]OK - Enriched {len(enrich_results['programs'])} programs, "
                           f"extracted {len(enrich_results['business_rules'])} rules[/green]")
        except Exception as e:
            console.print(f"[yellow]Warning: Enrichment failed: {e}. Continuing without.[/yellow]")
            skip_enrich = True
        console.print()
    else:
        if graph_enrich_after_neo4j:
            console.print("[cyan]>> Skipping JSON enrichment (will use Neo4j-based enrichment after export)[/cyan]")
        else:
            console.print("[yellow]>> Skipping enrichment step[/yellow]")
        console.print()

    # ========================================
    # Step 3: Load into SQLite
    # ========================================
    console.print(Panel("[bold]Step 3: Loading into SQLite Knowledge Base[/bold]", style="blue"))

    loader = SQLiteLoader(db_path, schema_path)
    loader.connect()

    if not skip_enrich and enriched_dir.exists():
        loader.load_from_json(enriched_json=str(enriched_dir),
                              screens_json=str(parsed_dir / "screens.json"))
    else:
        loader.load_from_json(
            programs_json=str(parsed_dir / "programs.json"),
            screens_json=str(parsed_dir / "screens.json")
        )

    # Load JCL jobs
    if jcl_jobs:
        loader.load_jcl(jcl_jobs)

    # Load copybook field dictionaries from .cpy files in the repo
    try:
        loader.load_copybook_fields(str(repo_path))
    except Exception as e:
        console.print(f"[yellow]Warning: copybook field load skipped: {e}[/yellow]")

    # Detect modules
    modules = loader.detect_modules()
    console.print(f"[green]OK - Detected {len(modules)} functional modules[/green]")

    # Print stats
    programs = loader.get_all_programs()
    rules = loader.get_all_business_rules()
    screens = loader.get_all_screens()
    console.print(f"[green]OK - DB: {len(programs)} programs, {len(rules)} rules, {len(screens)} screens[/green]")
    console.print()

    # ========================================
    # Step 4/5 routing: Doc generation vs Neo4j export
    # ========================================
    # If graph-enriching, export to Neo4j BEFORE generating docs so enrichment feeds into doc generation
    if graph_enrich_after_neo4j:
        # Move Neo4j export here (before doc generation)
        console.print(Panel("[bold]Step 5: Exporting to Neo4j (for graph enrichment)[/bold]", style="blue"))
        neo4j_driver = None
        try:
            from neo4j_exporter import Neo4jExporter
            exporter = Neo4jExporter(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
            exporter.connect()
            exporter.export_from_sqlite(loader)
            neo4j_driver = exporter.driver
            # Don't close yet — we need it for enrichment
            console.print("[green]OK - Exported to Neo4j[/green]")
        except Exception as e:
            console.print(f"[red]Neo4j export failed: {e}. Aborting graph enrichment.[/red]")
            graph_enrich_after_neo4j = False
        console.print()
        
        # Run Neo4j enrichment
        if graph_enrich_after_neo4j and neo4j_driver:
            console.print(Panel("[bold]Step 5b: LLM Enrichment via Neo4j Graph[/bold]", style="blue"))
            try:
                from neo4j_enricher import Neo4jEnricher
                graph_enricher = Neo4jEnricher(neo4j_driver=neo4j_driver, model=groq_model)
                enrich_results = graph_enricher.enrich_from_neo4j()
                graph_enricher.save_enrichment_to_neo4j()
                console.print(f"[green]OK - Enriched {enrich_results['total_enriched']} programs from graph[/green]")
                if enrich_results['errors']:
                    console.print(f"[yellow]  {len(enrich_results['errors'])} errors during enrichment[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Warning: Neo4j enrichment failed: {e}. Continuing.[/yellow]")
            console.print()
            
            # Close exporter driver
            if neo4j_driver:
                neo4j_driver.close()
    
    # ========================================
    # Step 4: Generate Documentation
    # ========================================
    console.print(Panel("[bold]Step 4: Generating Swimm-Style Documentation[/bold]", style="blue"))
    artifact_doc_counts = {"jcl": 0, "bms": 0}

    # Derive system name from repo path basename if not explicitly provided.
    # Falls back to "Application" if the basename is empty.
    derived_name = system_name or os.environ.get("SYSTEM_NAME") or repo_path.name.title() or "Application"
    generator = DocGenerator(
        db_loader=loader,
        output_dir=output_dir,
        repo_path=str(repo_path),
        system_name=derived_name,
    )
    generator.generate_all()

    # ========================================
    # Step 4a: Generate standalone JCL/BMS English docs
    # ========================================
    console.print(Panel("[bold]Step 4a: Generating Standalone JCL/BMS English Documentation[/bold]", style="blue"))
    try:
        from artifact_doc_agent import StandaloneArtifactDocGenerator
        artifact_generator = StandaloneArtifactDocGenerator(
            db_loader=loader,
            output_dir=Path(output_dir) / "standalone-artifacts",
        )
        artifact_doc_counts = artifact_generator.generate_all()
    except Exception as e:
        console.print(f"[yellow]Standalone JCL/BMS documentation skipped: {e}[/yellow]")

    doc_files = list(Path(output_dir).rglob("*.md"))
    console.print(f"[green]OK - Generated {len(doc_files)} documentation files[/green]")
    console.print()

    # ========================================
    # Step 4b: Validate Generated Documentation
    # ========================================
    console.print(Panel("[bold]Step 4b: Validating Documentation[/bold]", style="blue"))
    try:
        from doc_validator import validate_docs, print_report, write_report
        report = validate_docs(db_path, output_dir)
        print_report(report)
        write_report(report, str(Path(output_dir) / "validation_report.json"))
        if not report.passed:
            console.print("[yellow]Documentation validation found issues — see report above.[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Validation skipped: {e}[/yellow]")
    console.print()

    # ========================================
    # Step 5: Neo4j Export (if not already done above)
    # ========================================
    if not skip_neo4j and not graph_enrich_after_neo4j:
        console.print(Panel("[bold]Step 5: Exporting to Neo4j[/bold]", style="blue"))
        try:
            from neo4j_exporter import Neo4jExporter
            exporter = Neo4jExporter(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
            exporter.connect()
            exporter.export_from_sqlite(loader)
            exporter.close()
        except Exception as e:
            console.print(f"[yellow]Neo4j export failed: {e}[/yellow]")
    elif not graph_enrich_after_neo4j:
        console.print("[yellow]>> Skipping Neo4j export[/yellow]")

    loader.close()

    # Summary
    elapsed = datetime.now() - start_time
    console.print()
    console.print(Panel(f"""
Pipeline Complete!

Documentation: {output_dir}/
  Entry point: {output_dir}/00-SYSTEM-OVERVIEW.md
  Programs: {output_dir}/programs/
  Business Rules: {output_dir}/business-rules/
  Screens: {output_dir}/screens/
  Standalone JCL/BMS: {output_dir}/standalone-artifacts/
  Diagrams: {output_dir}/diagrams/

Database: {db_path}
  {len(programs)} programs | {len(rules)} rules | {len(screens)} screens | {len(modules)} modules
  Standalone artifact docs: {artifact_doc_counts.get("jcl", 0)} JCL | {artifact_doc_counts.get("bms", 0)} BMS

Total time: {elapsed.total_seconds():.1f}s
    """, style="green"))

    return {
        "programs": len(programs), "rules": len(rules),
        "screens": len(screens), "modules": len(modules),
        "artifact_jcl_docs": artifact_doc_counts.get("jcl", 0),
        "artifact_bms_docs": artifact_doc_counts.get("bms", 0),
        "doc_files": len(doc_files), "elapsed": elapsed.total_seconds()
    }


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="COBOL Documentation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("repo_path", help="Path to COBOL repository")
    parser.add_argument("--output", "-o", default="docs")
    parser.add_argument("--api-key", help="Groq API key")
    parser.add_argument("--model", default="llama-3.3-70b-versatile")
    parser.add_argument("--db", default="data/cobol_knowledge.db")
    parser.add_argument("--schema", default="schemas/cobol_knowledge.sql")
    parser.add_argument("--skip-parse", action="store_true")
    parser.add_argument("--skip-jcl", action="store_true", help="Skip JCL parsing step")
    parser.add_argument("--skip-enrich", action="store_true")
    parser.add_argument("--neo4j", action="store_true", help="Enable Neo4j export")
    parser.add_argument("--graph-enrich-after-neo4j", action="store_true", 
                        help="Use Neo4j graph-based enrichment after export (requires --neo4j)")
    parser.add_argument("--neo4j-uri", default=None)
    parser.add_argument("--neo4j-user", default=None)
    parser.add_argument("--neo4j-password", default=None)
    parser.add_argument("--format", default="FIXED", help="COBOL format (FIXED, TANDEM)")
    args = parser.parse_args()

    run_pipeline(
        repo_path=args.repo_path, output_dir=args.output,
        groq_api_key=args.api_key, groq_model=args.model,
        db_path=args.db, schema_path=args.schema,
        skip_parse=args.skip_parse, skip_enrich=args.skip_enrich,
        skip_jcl=args.skip_jcl, skip_neo4j=not args.neo4j,
        neo4j_uri=args.neo4j_uri, neo4j_user=args.neo4j_user,
        neo4j_password=args.neo4j_password,
        cobol_format=args.format,
        graph_enrich_after_neo4j=args.graph_enrich_after_neo4j,
    )


if __name__ == "__main__":
    main()
