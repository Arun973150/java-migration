# Artifact Documentation Agent Framework

> Generated 2026-05-12 12:20

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
