# COBOL Migration Documentation Hub

`doc_demo` is a documentation and migration-analysis pipeline for the AWS CardDemo COBOL sample. It parses COBOL, copybooks, BMS screens, and JCL; loads the facts into SQLite; enriches the codebase with business and migration context; generates cross-linked Markdown documentation; and serves an interactive Streamlit dashboard for exploration.

The folder already contains a local `carddemo/` source tree plus cached parser, enrichment, database, and generated documentation outputs, so you can inspect the system immediately or regenerate the docs when the source changes.

## What This Project Contains

- A parser pipeline for COBOL programs, copybooks, BMS screen maps, and JCL jobs.
- A SQLite knowledge base with full-text search and relational tables for programs, paragraphs, statements, data items, calls, screens, jobs, modules, and business rules.
- LLM-assisted enrichment for business purpose, plain-English names, migration complexity, data contracts, risks, and business rules.
- A Markdown documentation generator for system, module, program, screen, JCL, business-rule, cluster, data-dictionary, copybook, and diagram docs.
- A Streamlit dashboard named **COBOL Migration Hub** with exploration, search, graph, SQL, CICS, migration, and doc-generation pages.
- Optional Neo4j export for graph impact analysis.

## Current Generated Snapshot

The checked-in generated artifacts currently describe:

| Artifact | Count |
| --- | ---: |
| COBOL programs | 44 |
| Copybooks | 68 |
| Copybook usages | 301 |
| Paragraphs | 739 |
| Statements | 2,079 |
| Data items | 7,383 |
| Program calls | 59 |
| PERFORM relationships | 586 |
| BMS screens | 21 |
| Screen fields | 1,164 |
| JCL jobs | 55 |
| Functional modules | 19 |
| Business rules | 447 |
| Generated Markdown docs | 595 |

`docs/validation_report.json` currently reports validation as passing, with no missing program docs, broken links, or coverage gaps.

## Architecture

Two enrichment modes are available:

### Mode A (Default): JSON-based Enrichment → SQLite → Neo4j
```text
AWS CardDemo source
  ↓
Step 1: Parse with ProLeap + custom parsers
  ├─ parsed_output/programs.json
  ├─ parsed_output/copybooks.json
  ├─ parsed_output/screens.json
  └─ parsed_output/jcl_jobs.json
  ↓
Step 2: LLM enrichment on parsed JSON (langgraph_enricher)
  ├─ enriched_output/enriched_programs.json
  └─ enriched_output/business_rules.json
  ↓
Step 3: Load enriched data into SQLite
  └─ data/cobol_knowledge.db
  ↓
Step 4: Generate Markdown docs
  └─ docs/
  ↓
Step 5: Optional Neo4j export (no further enrichment)
  └─ Neo4j graph
```

### Mode B (New): SQLite → Neo4j → Graph-based LLM Enrichment
Use this when you want LLM to consider program dependencies and data flow relationships.

```text
AWS CardDemo source
  ↓
Step 1: Parse with ProLeap + custom parsers (as-is, no enrichment)
  ├─ parsed_output/programs.json
  ├─ parsed_output/copybooks.json
  ├─ parsed_output/screens.json
  └─ parsed_output/jcl_jobs.json
  ↓
Step 2: [SKIPPED] No JSON enrichment
  ↓
Step 3: Load raw parsed data into SQLite
  └─ data/cobol_knowledge.db
  ↓
Step 5: Export to Neo4j (builds call graph, data flow)
  └─ Neo4j graph
  ↓
Step 5b: LLM enrichment using graph structure (neo4j_enricher)
         Enricher reads: call graph, data dependencies, relationships
         LLM analyzes: integration points, migration complexity, risks
         Writes back to Neo4j: enriched program metadata
  ↓
Step 4: Generate Markdown docs (using graph-enriched metadata)
  └─ docs/ [with richer graph-based context]
```

### Which mode should I use?

- **Mode A (JSON)**: Fast, works offline, enrichment based on code syntax alone
- **Mode B (Graph)**: Slower, needs Neo4j, enrichment considers architectural relationships

Enable Mode B by passing `graph_enrich_after_neo4j=True` to the pipeline:
```python
run_pipeline(
    repo_path="./carddemo",
    graph_enrich_after_neo4j=True,
    skip_neo4j=False,
)
```


## Folder Guide

```text
doc_demo/
  carddemo/                 Local AWS CardDemo source copy used by the pipeline
  data/                     SQLite database and exported English JSON
  docs/                     Generated Markdown documentation
  docs_streamlit/           Supporting docs for dashboard content
  enriched_output/          LLM-enriched program and rule JSON
  lib/                      JavaScript/CSS assets and parser JAR dependencies
  parsed_output/            Parser outputs for programs, copybooks, screens, and JCL
  proleap-cobol-parser/     Vendored ProLeap parser source
  schemas/                  SQLite schema
  src/                      Python pipeline, dashboard, parsers, loaders, validators
  export_english.py         Merges parsed and enriched JSON into data/programs_english.json
  run_pipeline.py           Main one-command pipeline runner
  requirements.txt          Python dependencies
```

Important source files:

| File | Purpose |
| --- | --- |
| `src/proleap_wrapper.py` | COBOL, copybook, and BMS parsing through ProLeap plus fallback extraction |
| `src/jcl_parser.py` | JCL job, step, program, and dataset parsing |
| `src/sqlite_loader.py` | SQLite loading, module detection, search, and query helpers |
| `src/doc_generator.py` | Markdown documentation generation |
| `src/doc_validator.py` | Generated documentation validation |
| `src/langgraph_enricher.py` | Vertex AI Gemini enrichment pipeline |
| `src/doc_agent_pipeline.py` | LLM-backed dashboard document generation and critique flow |
| `src/neo4j_exporter.py` | Optional graph export from SQLite to Neo4j |
| `src/app.py` | Streamlit dashboard |
| `src/chat_cli.py` | CLI assistant over the knowledge base |

## Requirements

- Python 3.10+
- Java 11+ or 17+ for ProLeap parsing
- `pip`
- Optional: Google Cloud credentials for Vertex AI Gemini enrichment and document generation
- Optional: Groq API key for the chat CLI paths that use Groq
- Optional: Neo4j Desktop or server for graph export

Install Python dependencies:

```powershell
cd doc_demo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment

Create `doc_demo/.env` when you need non-default settings:

```ini
DB_PATH=data/cobol_knowledge.db

# Optional, used by Vertex AI Gemini enrichment and dashboard doc generation
GOOGLE_CLOUD_PROJECT=your-gcp-project
VERTEX_PROJECT=your-gcp-project
VERTEX_LOCATION=us-central1
VERTEX_MODEL=gemini-2.5-flash
VERTEX_MAX_OUTPUT_TOKENS=8192

# Optional, used by chat_cli.py and some dashboard chat paths
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# Optional Neo4j export
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

For parsing, make sure Java is available:

```powershell
java -version
```

## Quick Start

Run the dashboard against the existing database and generated artifacts:

```powershell
cd doc_demo
streamlit run src/app.py
```

Then open:

```text
http://localhost:8501
```

The dashboard pages include Overview, Call Graph, Dependency Matrix, Data Flow, Modules, Explorer, Doc Generator, JCL Jobs, CICS Commands, SQL Operations, Migration, Rules, and Search.

## Regenerate The Knowledge Base And Docs

The simplest path is:

```powershell
cd doc_demo
python run_pipeline.py
```

`run_pipeline.py` currently runs against `carddemo/`, reparses COBOL/BMS/copybook and JCL sources, skips LLM enrichment by default, loads SQLite, regenerates Markdown docs, validates the output, and skips Neo4j export.

For CLI-driven control, call the orchestrator directly:

```powershell
python src/orchestrator.py carddemo --output docs --skip-enrich --format FIXED
```

Useful options:

| Option | Effect |
| --- | --- |
| `--skip-parse` | Reuse existing `parsed_output/` files |
| `--skip-jcl` | Reuse existing JCL JSON or omit JCL parsing |
| `--skip-enrich` | Skip LLM enrichment |
| `--neo4j` | Export the loaded graph to Neo4j |
| `--db <path>` | Use a different SQLite DB path |
| `--schema <path>` | Use a different schema file |
| `--format FIXED` | Parse fixed-format COBOL source |
| `--format TANDEM` | Parse Tandem-format COBOL source |

## Run Individual Tools

Parse COBOL, copybooks, and BMS screens:

```powershell
python src/proleap_wrapper.py carddemo --output parsed_output --format FIXED
```

Load parsed data into SQLite:

```powershell
python src/sqlite_loader.py --db data/cobol_knowledge.db --programs parsed_output/programs.json --screens parsed_output/screens.json
```

Generate documentation only:

```powershell
python src/doc_generator.py --db data/cobol_knowledge.db --output docs
```

Validate generated documentation:

```powershell
python src/doc_validator.py --db data/cobol_knowledge.db --docs docs --out docs/validation_report.json
```

Export merged parsed and enriched program explanations:

```powershell
python export_english.py
```

Run the CLI knowledge-base assistant:

```powershell
python src/chat_cli.py
```

Export to Neo4j:

```powershell
python src/neo4j_exporter.py --db data/cobol_knowledge.db --uri bolt://localhost:7687
```

## Generated Documentation

The `docs/` folder is generated from the SQLite knowledge base and contains:

```text
docs/
  00-SYSTEM-OVERVIEW.md
  business-rules/
  clusters/
  diagrams/
  jcl/
  modules/
  programs/
  screens/
  copybook-reference.md
  data-dictionary.md
  validation_report.json
```

Start with `docs/00-SYSTEM-OVERVIEW.md`, then move into module, program, screen, JCL, or business-rule pages as needed.

## Docker

From the repository root, the provided `Dockerfile` creates a Maven/Java/Python utility image and installs the Python requirements:

```powershell
docker build -t cobol-doc-demo .
docker run --rm -it -v ${PWD}:/workspace cobol-doc-demo
```

Inside the container:

```bash
cd doc_demo
python3 run_pipeline.py
```

## Notes And Caveats

- `run_pipeline.py` is a convenience script with fixed defaults. Use `src/orchestrator.py` when you need command-line switches.
- LLM enrichment requires cloud credentials and can take several minutes depending on model and quota.
- Some names in the code still mention Groq because earlier versions used Groq for enrichment; the current enrichment and dashboard document-generation path uses Vertex AI Gemini.
- The generated docs and SQLite DB are derived artifacts. Regenerating them may change many files at once.
- The top-level `aws-mainframe-modernization-carddemo/` folder is another copy of the AWS sample source. The pipeline defaults to `doc_demo/carddemo/`.

## License

This documentation pipeline is provided under the repository license. The bundled AWS CardDemo sample keeps its own license and notices in the CardDemo source folders.
