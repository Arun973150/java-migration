"""
Run the COBOL Documentation Pipeline

Usage:
  python run_pipeline.py                    # Full pipeline (parse + load + docs)
  python run_pipeline.py --skip-parse       # Skip parsing (use existing parsed_output/)
  python run_pipeline.py --skip-jcl         # Skip JCL parsing
  python run_pipeline.py --enrich           # Enable LLM enrichment

Output:
  docs/00-SYSTEM-OVERVIEW.md       # Layer 1: System overview
  docs/modules/*.md                # Layer 2: Module documentation
  docs/programs/*.md               # Layer 3: Program walkthroughs
  docs/business-rules/*.md         # Layer 4: Business rules catalog
  docs/screens/*.md                # Layer 5: Screen catalog
  docs/diagrams/call-graph.md      # Call graph diagram
  docs/data-dictionary.md          # Data dictionary
  docs/copybook-reference.md       # Copybook reference
"""
import argparse
import os
import sys

# Force UTF-8 console on Windows so Rich's spinner does not crash cp1252.
if sys.platform.startswith("win"):
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, "src")

from orchestrator import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run the COBOL documentation pipeline on any codebase")
    parser.add_argument("--repo", default="carddemo", help="COBOL repository path")
    parser.add_argument("--output", default="docs", help="Documentation output directory")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="SQLite database path")
    parser.add_argument("--schema", default="schemas/cobol_knowledge.sql", help="SQLite schema path")
    parser.add_argument("--format", default=None,
                        help="COBOL source format (FIXED or FREE). If omitted, auto-detected by sampling source files.")
    parser.add_argument("--model", default="gemini-2.0-flash", help="LLM model name")
    parser.add_argument("--system-name", default=None,
                        help="Display name for the application (defaults to repo basename)")
    parser.add_argument("--skip-parse", action="store_true", help="Reuse existing parsed_output files")
    parser.add_argument("--skip-jcl", action="store_true", help="Reuse cached JCL JSON or omit JCL parsing")
    parser.add_argument("--enrich", action="store_true", help="Enable LLM enrichment")
    parser.add_argument("--neo4j", action="store_true", help="Enable Neo4j export")
    args = parser.parse_args()

    return run_pipeline(
        repo_path=args.repo,
        output_dir=args.output,
        db_path=args.db,
        schema_path=args.schema,
        skip_parse=args.skip_parse,
        skip_jcl=args.skip_jcl,
        skip_enrich=not args.enrich,
        skip_neo4j=not args.neo4j,
        cobol_format=args.format,
        groq_model=args.model,
        system_name=args.system_name,
    )


if __name__ == "__main__":
    main()
