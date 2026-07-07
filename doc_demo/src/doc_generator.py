"""
Swimm-Style Documentation Generator - Complete 5-Layer Architecture
Generates interactive, business-first documentation from COBOL analysis.

Layers:
  1. Repository Overview (00-SYSTEM-OVERVIEW.md)
  2. Module Documentation (modules/MODULE-NAME.md)
  3. Program Walkthroughs (programs/PROGRAM-NAME.md)
  4. Business Rules Catalog (business-rules/INDEX.md + per-rule)
  5. Screen Catalog (screens/SCREEN-ID.md)

Plus:
  - Call Graph Diagram (diagrams/call-graph.md)
  - Data Dictionary (data-dictionary.md)
  - Copybook Reference (copybook-reference.md)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from jinja2 import Environment, BaseLoader, TemplateNotFound
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


# ============================================================
# Jinja2 Template Loader (inline templates)
# ============================================================

class InlineTemplateLoader(BaseLoader):
    """Loads templates from inline strings or optional template files."""

    def __init__(self, templates: Dict[str, str], templates_dir: str = None):
        self._templates = templates
        self._templates_dir = templates_dir

    def get_source(self, environment, template):
        if self._templates_dir:
            path = Path(self._templates_dir) / template
            if path.exists():
                return path.read_text(encoding="utf-8"), str(path), lambda: True
        if template in self._templates:
            return self._templates[template], template, lambda: True
        raise TemplateNotFound(template)


# ============================================================
# Templates
# ============================================================

TEMPLATES = {}

# ----- Layer 1: System Overview -----
TEMPLATES["system_overview.md.j2"] = '''\
# {{ system_name }} - System Overview

> **Auto-generated documentation** | {{ generated_date }}  
> Analyzed from {{ total_programs }} COBOL programs across {{ total_modules }} functional modules

---

## What is {{ system_name }}?

{{ system_name }} is a mainframe COBOL application composed of {{ total_programs }} programs
across {{ total_modules }} functional modules. It exposes {{ total_screens }} BMS screens for
online (CICS) interaction and is orchestrated by {{ total_jcl_jobs | default(0) }} JCL batch
jobs. The sections below summarize its structure, dependencies, and modernization-relevant
characteristics.

## System at a Glance

| Metric | Count |
|--------|-------|
| Programs | {{ total_programs }} |
| Functional Modules | {{ total_modules }} |
| BMS Screens | {{ total_screens }} |
| Data Items | {{ total_data_items }} |
| CICS Commands | {{ total_cics_commands }} |
| SQL Statements | {{ total_sql_statements }} |
| Inter-Program Calls | {{ total_calls }} |
| Business Rules | {{ total_rules }} |
| Copybooks | {{ total_copybooks }} |

## Architecture Overview

```mermaid
flowchart TB
    subgraph ONLINE["Online (CICS) Programs"]
{% for prog in online_programs[:12] %}
        {{ prog.program_id }}["{{ prog.program_id }}"]
{% endfor %}
    end

    subgraph BATCH["Batch Programs"]
{% for prog in batch_programs[:8] %}
        {{ prog.program_id }}["{{ prog.program_id }}"]
{% endfor %}
    end

{% for call in call_graph[:25] %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
    {{ call.caller_program }} --> {{ call.called_program }}
{% endif %}
{% endfor %}

    USER([User/CSR]) --> ONLINE
    SCHEDULER([Job Scheduler]) --> BATCH
```

## Functional Modules

{% for module in modules %}
### [{{ module.business_name }}](modules/{{ module.module_name }}.md)

{{ module.business_purpose | default(module.business_name ~ " operations") }}

| Programs | Type |
|----------|------|
{% for prog in module.programs[:5] %}
| [{{ prog.program_id }}](programs/{{ prog.program_id }}.md) | {{ prog.program_type | default("BATCH") }} |
{% endfor %}
{% if module.programs | length > 5 %}
| *...{{ module.programs | length - 5 }} more* | |
{% endif %}

{% endfor %}

## Entry Points

Programs that are not called by others -- these are likely user-facing entry points:

{% for prog in entry_points %}
- [{{ prog }}](programs/{{ prog }}.md)
{% endfor %}

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Program Documentation](programs/) | Detailed walkthrough for each COBOL program |
| [Linked Programs](clusters/INDEX.md) | Connected program clusters and dependency graphs |
| [Module Documentation](modules/) | Business-grouped program clusters |
| [Business Rules Catalog](business-rules/INDEX.md) | All extracted business rules |
| [Screen Catalog](screens/INDEX.md) | BMS screen definitions and layouts |
| [Call Graph](diagrams/call-graph.md) | Inter-program dependency diagram |
| [Data Dictionary](data-dictionary.md) | Complete variable listing |
| [Copybook Reference](copybook-reference.md) | Shared data structures |

---

*Generated by COBOL Documentation Pipeline*
'''

# ----- Layer 2: Module Documentation -----
TEMPLATES["module.md.j2"] = '''\
# Module: {{ business_name }}

> **Module ID:** `{{ module_name }}`  
> **Programs:** {{ programs | length }}

---

## Business Purpose

{{ business_purpose | default("This module groups related programs that share a common naming prefix and/or interact heavily through calls and shared copybooks.") }}

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
{% for prog in programs %}
| [{{ prog.program_id }}](../programs/{{ prog.program_id }}.md) | {{ prog.program_type | default("BATCH") }} | {{ prog.line_count | default(0) }} | {{ prog.business_purpose | default("-") | truncate(60) }} |
{% endfor %}

{% set valid_mod_calls = [] %}
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
{% set _ = valid_mod_calls.append(call) %}
{% endif %}
{% endfor %}
{% if valid_mod_calls %}
## Internal Call Flow

Programs in this module interact through the following call chain:

```mermaid
flowchart LR
{% set seen = {} %}
{% for call in valid_mod_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program }}["{{ call.caller_program }}"] --> {{ call.called_program }}["{{ call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

| Caller | Calls | Line |
|--------|-------|------|
{% set seen_mod_calls = {} %}
{% for call in valid_mod_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen_mod_calls %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | {{ call.called_program | program_link("../programs/") }} | {{ call.line_number | default("-") }} |
{% set _ = seen_mod_calls.update({key: true}) %}
{% endif %}
{% endfor %}
{% endif %}

{% if screens %}
## Associated Screens

| Screen | Map | Mapset | Program |
|--------|-----|--------|---------|
{% for s in screens %}
| [{{ s.screen_name }}](../screens/{{ s.screen_name }}.md) | {{ s.map_name }} | {{ s.mapset_name }} | [{{ s.associated_program }}](../programs/{{ s.associated_program }}.md) |
{% endfor %}
{% endif %}

{% if files %}
## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
{% for f in files %}
| `{{ f.file_name }}` | {{ f.file_type | default("SEQUENTIAL") }} | {{ f.access_mode | default("-") }} | {{ f.program_id }} |
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 3: Program Walkthrough -----
TEMPLATES["program.md.j2"] = '''\
# Program: {{ program_id }}

{% if business_name %}> **{{ business_name }}**{% endif %}

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `{{ program_id }}` |
| Type | {{ program_type | default("BATCH") }} |
| Lines | {{ line_count | default(0) }} |
| Source | {{ file_path | code_link(1, file_path | basename) }} |
| Paragraphs | {{ paragraphs | length }} |
| Statements | {{ statements | length }} |
| Impact Risk | **{{ impact.risk | default("LOW") }}** — {{ impact.total_impact | default(0) }} programs affected |

> **View Source:** {{ file_path | code_link(1, "Open " ~ (file_path | basename)) }}

{% if source_literals or source_statuses %}
## Source Grounding Facts

{% if source_literals %}
| Data Item | Literal Value |
|-----------|---------------|
{% for item in source_literals %}
| `{{ item.name }}` | `{{ item.value }}` |
{% endfor %}
{% endif %}
{% if source_statuses %}

Status conditions found in source:
{% for condition in source_statuses %}
- `{{ condition }}`
{% endfor %}
{% endif %}

{% endif %}

## Business Purpose

{% if business_purpose %}
{{ business_purpose }}
{% else %}
*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*
{% endif %}

{% if user_role %}**Used By:** {{ user_role }}{% endif %}
{% if business_process %}  |  **Process:** {{ business_process }}{% endif %}

{% if migration_complexity %}
## Migration Summary

| Attribute | Value |
|-----------|-------|
| Migration Complexity | **{{ migration_complexity }}/5** — {{ complexity_reason | default("-") }} |
| Modern Equivalent | {{ modern_equivalent | default("TBD") }} |
| Target Microservice | `{{ suggested_service | default("TBD") }}` |

{% if migration_approach %}
### How to Migrate This Program

{{ migration_approach }}
{% endif %}

{% if data_contracts %}
### Data Contracts (Input / Output)

{{ data_contracts }}
{% endif %}

{% if migration_risks %}
### Migration Risks

> ⚠️ {{ migration_risks }}
{% endif %}

{% if dependencies_to_migrate_first %}
### Migrate These First

The following programs should be migrated before this one:

{% for dep in dependencies_to_migrate_first %}
- [`{{ dep }}`]({{ dep }}.md)
{% endfor %}
{% endif %}

---
{% endif %}

## Dependency Context

> This section shows how **{{ program_id }}** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call {{ program_id }} (Callers)

{% if dep_callers %}
| Caller | Type | Line | Why |
|--------|------|------|-----|
{% for c in dep_callers %}
| [{{ c.caller_program }}]({{ c.caller_program }}.md) | {{ c.program_type | default("-") }} | {{ c.line_number | default("-") }} | {{ c.business_purpose | default(c.business_name | default("Calls " ~ program_id)) | truncate(80) }} |
{% endfor %}
{% else %}
*No programs call {{ program_id }} — this is likely a top-level entry point or CICS transaction starter.*
{% endif %}

### Programs Called by {{ program_id }} (Callees)

{% if dep_callees %}
| Called Program | Type | Line | Why |
|----------------|------|------|-----|
{% for c in dep_callees %}
| {{ c.called_program | program_link }} | {{ c.program_type | default("-") }} | {{ c.line_number | default("-") }} | {{ c.business_purpose | default(c.business_name | default("Called by " ~ program_id)) | truncate(80) }} |
{% endfor %}
{% else %}
*{{ program_id }} does not call any other programs (leaf program).*
{% endif %}

### Shared Data (Copybooks & Files)

{% if shared_copybooks %}
#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
{% for cb in shared_copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.co_users[:5] | map(attribute="program_id") | join(", ") }}{% if cb.co_user_count > 5 %} (+{{ cb.co_user_count - 5 }} more){% endif %} | {{ cb.co_user_count }} |
{% endfor %}
{% else %}
*No shared copybooks.*
{% endif %}

{% if shared_files %}
#### Shared Files

| File | Type | Access | Also Used By |
|------|------|--------|-------------|
{% for f in shared_files %}
| `{{ f.file_name }}` | {{ f.file_type | default("-") }} | {{ f.access_mode | default("-") }} | {{ f.co_users[:5] | map(attribute="program_id") | join(", ") }}{% if f.co_user_count > 5 %} (+{{ f.co_user_count - 5 }} more){% endif %} |
{% endfor %}
{% endif %}

## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.

{% if data_contracts_detail.file_records %}
### File Record Layouts

{% for rec in data_contracts_detail.file_records %}
#### `{{ rec.file_name }}`{% if rec.record_name %} / `{{ rec.record_name }}`{% endif %}

| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
{% for field in rec.fields %}
| `{{ field.name }}` | {{ field.meaning }} | `{{ field.cobol_type }}` | `{{ field.modern_type }}` | {{ field.format_note | default("-") }} |
{% endfor %}

{% endfor %}
{% endif %}

{% if data_contracts_detail.copybooks %}
### Copybook Segment Layouts

{% for cb in data_contracts_detail.copybooks %}
#### `{{ cb.copybook_name }}` as `{{ cb.record_name }}`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
{% for field in cb.fields %}
| `{{ field.name }}` | {{ field.meaning }} | `{{ field.cobol_type }}` | `{{ field.modern_type }}` | {{ field.format_note | default("-") }} |
{% endfor %}

{% endfor %}
{% endif %}

{% if data_contracts_detail.moves %}
### Data Movement And Key Mapping

| Line | Source | Target | Meaning |
|------|--------|--------|---------|
{% for move in data_contracts_detail.moves %}
| {{ move.line_number }} | `{{ move.source }}` | `{{ move.target }}` | {{ move.meaning }} |
{% endfor %}

{% endif %}

{% if not data_contracts_detail.file_records and not data_contracts_detail.copybooks %}
*No concrete file or copybook record layouts were found for this program.*
{% endif %}

---

## Dependency Graph

```mermaid
flowchart TD
{% for c in dep_callers %}
    {{ c.caller_program | mermaid_id }}["{{ c.caller_program }}"]:::caller
{% endfor %}
    {{ program_id | mermaid_id }}["⬤ {{ program_id }}"]:::target
{% for c in dep_callees %}
    {{ c.called_program | mermaid_id }}["{{ c.called_program }}"]:::callee
{% endfor %}
{% for c in dep_callers %}
    {{ c.caller_program | mermaid_id }} --> {{ program_id | mermaid_id }}
{% endfor %}
{% for c in dep_callees %}
    {{ program_id | mermaid_id }} --> {{ c.called_program | mermaid_id }}
{% endfor %}
{% for cb in shared_copybooks[:8] %}
{% if cb.co_user_count > 0 %}
    {{ cb.copybook_name | mermaid_cb_node }}
    {{ program_id | mermaid_id }} -.- CB_{{ cb.copybook_name | mermaid_id }}
{% for u in cb.co_users[:3] %}
    {{ u.program_id | mermaid_id }}["{{ u.program_id }}"]:::coupled
    CB_{{ cb.copybook_name | mermaid_id }} -.- {{ u.program_id | mermaid_id }}
{% endfor %}
{% endif %}
{% endfor %}
{% if impact.transitive_callers %}
{% for tc in impact.transitive_callers[:5] %}
{% if tc not in dep_callers | map(attribute="caller_program") | list %}
    {{ tc | mermaid_id }}["{{ tc }}"]:::transitive
    {{ tc | mermaid_id }} -.-> {{ program_id | mermaid_id }}
{% endif %}
{% endfor %}
{% endif %}
{% if impact.transitive_callees %}
{% for tc in impact.transitive_callees[:5] %}
{% if tc not in dep_callees | map(attribute="called_program") | list %}
    {{ tc | mermaid_id }}["{{ tc }}"]:::transitive
    {{ program_id | mermaid_id }} -.-> {{ tc | mermaid_id }}
{% endif %}
{% endfor %}
{% endif %}
    classDef target fill:#f85149,stroke:#da3633,color:#fff,stroke-width:3px
    classDef caller fill:#58a6ff,stroke:#1f6feb,color:#fff
    classDef callee fill:#3fb950,stroke:#238636,color:#fff
    classDef copybook fill:#d29922,stroke:#9e6a03,color:#fff
    classDef coupled fill:#d29922,stroke:#9e6a03,color:#fff,stroke-dasharray:5
    classDef transitive fill:#484f58,stroke:#8b949e,color:#c9d1d9,stroke-dasharray:5
```

> **Legend:** 🔴 Target program · 🔵 Direct callers · 🟢 Direct callees · 🟡 Copybook-coupled · ⚫ Transitive (indirect)

---

## Impact Ripple View

> **If you change {{ program_id }}, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | {{ impact.direct_callers | length }} |
| Transitive Callers (callers of callers) | {{ impact.transitive_callers | length }} |
| Direct Callees | {{ impact.direct_callees | length }} |
| Transitive Callees | {{ impact.transitive_callees | length }} |
| Copybook-Coupled Programs | {{ impact.copybook_coupling | length }} |
| **Total Impact** | **{{ impact.total_impact }}** |
| **Risk Rating** | **{{ impact.risk }}** |

{% if impact.transitive_callers %}
**Programs that would break (transitive callers):**
{% for p in impact.transitive_callers %}
- `{{ p }}`
{% endfor %}
{% endif %}

{% if impact.copybook_coupling %}
**Programs affected via shared copybooks:**
{% for p in impact.copybook_coupling %}
- `{{ p }}`
{% endfor %}
{% endif %}

---

## Statement Profile

{% if stmt_summary %}
| Statement Type | Count |
|---------------|-------|
{% for stype, count in stmt_summary.items() %}
| {{ stype }} | {{ count }} |
{% endfor %}
{% endif %}

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
{% for para in paragraphs[:15] %}
    {{ para.paragraph_name | mermaid_id }}["{{ para.paragraph_name }}"]
{% endfor %}
{% if paragraphs %}
    START --> {{ paragraphs[0].paragraph_name | mermaid_id }}
{% endif %}
{% set seen = {} %}
{% for perf in performs[:20] %}
{% set key = perf.source_paragraph ~ "->" ~ perf.target_paragraph %}
{% if key not in seen %}
    {{ perf.source_paragraph | mermaid_id }} --> {{ perf.target_paragraph | mermaid_id }}
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

## Paragraphs

{% for para in paragraphs %}
### {{ para.business_name if para.business_name else para.paragraph_name }}

| | |
|---|---|
| **Paragraph** | `{{ para.paragraph_name }}` |
| **Lines** | {{ para.line_start | default("?") }} - {{ para.line_end | default("?") }} |
| **View Code** | {{ file_path | code_link(para.line_start, "Jump to Line " ~ (para.line_start | string)) }} |

{% if para.narrative %}
{{ para.narrative }}
{% endif %}

{% if para.purpose %}
> **Purpose:** {{ para.purpose }}
{% endif %}

{% endfor %}

{% if jcl_jobs %}
## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
{% for j in jcl_jobs %}
| [{{ j.job_name }}](../jcl/{{ j.job_name }}.md) | `{{ j.step_name }}` | {{ j.step_comments | default("-") | truncate(80) }} |
{% endfor %}

{% endif %}

{% if exec_sql %}
## Database Operations (EXEC SQL / DB2)

This program uses the following SQL statements:

| Command | Table / Cursor | Paragraph | Line |
|---------|----------------|-----------|------|
{% for s in exec_sql %}
| `{{ s.command }}` | {{ s.table_name | default(s.cursor_name | default("-")) }} | {{ s.paragraph_name | default("-") }} | {{ s.line_number | default("-") }} |
{% endfor %}

{% set sql_summary = {} %}
{% for s in exec_sql %}
{% if s.command in sql_summary %}
{% set _ = sql_summary.update({s.command: sql_summary[s.command] + 1}) %}
{% else %}
{% set _ = sql_summary.update({s.command: 1}) %}
{% endif %}
{% endfor %}
**Summary:** {{ exec_sql | length }} SQL statement(s) — {% for cmd, cnt in sql_summary.items() %}{{ cmd }} ({{ cnt }}){% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}

{% if ims_calls %}
## IMS DL/I Calls

This program uses the following IMS DL/I calls:

| Function | Meaning | PCB | Segment Area | SSA | Qualifier | Paragraph | Line |
|----------|---------|-----|--------------|-----|-----------|-----------|------|
{% for im in ims_calls %}
| `{{ im.function_code }}` | {{ im.function_name | default("-") }} | {{ im.pcb_name | default("-") }} | {{ im.segment_area | default("-") }} | {{ im.ssa_name | default("-") }}{% if im.ssa_segment %} (segment: {{ im.ssa_segment }}){% endif %} | {{ im.ssa_qualifier | default("-") }} | {{ im.paragraph_name | default("-") }} | {{ im.line_number | default("-") }} |
{% endfor %}

{% endif %}

{% if copybook_dictionaries %}
## Copybook Field Dictionaries

The following copybooks are included by this program. Each entry shows the actual fields
extracted from the copybook source file (`.cpy`).

{% for cb in copybook_dictionaries %}
### Copybook `{{ cb.copybook_name }}`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
{% for f in cb.fields[:50] %}
| `{{ "%02d" | format(f.level_number or 0) }}` | `{{ f.field_name }}` | `{{ f.picture | default("-") }}` | {{ f.usage | default("-") }} | {{ f.parent_name | default("-") }} | {% if f.occurs_count %}OCCURS {{ f.occurs_count }}{% endif %}{% if f.redefines_target %} REDEFINES {{ f.redefines_target }}{% endif %} |
{% endfor %}
{% if cb.fields | length > 50 %}*+ {{ cb.fields | length - 50 }} more fields*{% endif %}

{% endfor %}
{% endif %}

{% if file_records %}
## File Record Layouts (FD)

This program declares the following file records (data contracts for I/O):

{% set fd_groups = {} %}
{% for r in file_records %}
{% if r.file_name not in fd_groups %}
{% set _ = fd_groups.update({r.file_name: []}) %}
{% endif %}
{% set _ = fd_groups[r.file_name].append(r) %}
{% endfor %}
{% for fname, items in fd_groups.items() %}
### `FD {{ fname }}`{% if items[0].record_name %} (record `{{ items[0].record_name }}`){% endif %}


| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
{% for it in items[:40] %}
| `{{ "%02d" | format(it.level_number or 0) }}` | `{{ it.field_name }}` | `{{ it.picture | default("-") }}` | {{ it.usage | default("-") }} | {{ it.parent_name | default("-") }} |
{% endfor %}
{% if items | length > 40 %}*+ {{ items | length - 40 }} more fields*{% endif %}

{% endfor %}
{% endif %}

{% if data_movements %}
## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
{% for m in data_movements[:60] %}
| {% if m.is_literal %}`'{{ m.source_field }}'`{% else %}`{{ m.source_field }}`{% endif %} | `{{ m.destination_field }}` | {{ m.paragraph_name | default("-") }} | {{ m.line_number | default("-") }} |
{% endfor %}
{% if data_movements | length > 60 %}*+ {{ data_movements | length - 60 }} more movements*{% endif %}

{% endif %}

{% if code_anomalies %}
## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
{% for a in code_anomalies %}
| **{{ a.severity }}** | {{ a.category }} | {{ a.title }} | {{ a.paragraph_name | default("-") }} | {{ a.line_number | default("-") }} |
{% endfor %}

{% for a in code_anomalies %}
### {{ a.severity }} — {{ a.title }}

{% if a.description %}{{ a.description }}{% endif %}

{% if a.snippet %}**Source excerpt** (line {{ a.line_number }}):
```cobol
{{ a.snippet }}
```
{% endif %}

{% if a.suggestion %}**Recommendation:** {{ a.suggestion }}{% endif %}

---
{% endfor %}
{% endif %}

{% if program_parameters %}
## External Runtime Parameters

This program receives the following parameters at runtime (via `PROCEDURE DIVISION USING`
or `ENTRY USING`). Each parameter must be supplied by the caller — typically a JCL job
step (`PARM=`), CICS COMMAREA, or the IMS region controller. The migration target needs
an equivalent input wiring.

| # | Parameter | Source | Declared at line |
|---|-----------|--------|------------------|
{% for p in program_parameters %}
| {{ p.position }} | `{{ p.parameter_name }}` | {{ p.source }} | {{ p.line_number }} |
{% endfor %}
{% endif %}

{% if file_operations %}
## File OPEN / CLOSE Operations

The exact OPEN mode (INPUT / OUTPUT / I-O / EXTEND) determines whether a file can be
read, written, or both — and whether REWRITE / DELETE are legal. This table is the
source of truth for migrators converting to modern storage layers.

| File | Operation | Mode | Paragraph | Line |
|------|-----------|------|-----------|------|
{% for op in file_operations %}
| `{{ op.file_name }}` | {{ op.operation }} | {{ op.mode | default("-") }} | {{ op.paragraph_name | default("-") }} | {{ op.line_number }} |
{% endfor %}
{% endif %}

{% if mq_calls %}
## IBM MQ Operations

This program calls the IBM MQ API. Each row is a queueing operation that must be
preserved (or migrated to Kafka/SQS topics) when modernising.

| Function | Description | Queue | Paragraph | Line |
|----------|-------------|-------|-----------|------|
{% for m in mq_calls %}
| `{{ m.function_code }}` | {{ m.function_name | default("-") }} | {{ m.queue_name | default("(not statically resolvable)") }} | {{ m.paragraph_name | default("-") }} | {{ m.line_number | default("-") }} |
{% endfor %}
{% endif %}

{% if evaluate_branches %}
## Decision Tables (EVALUATE / WHEN)

Captured from the source. Each EVALUATE block is a structured decision the
migration team should turn into either a switch / pattern-match or a rules table.

{% set ev_groups = {} %}
{% for b in evaluate_branches %}
{% if b.evaluate_id not in ev_groups %}
{% set _ = ev_groups.update({b.evaluate_id: []}) %}
{% endif %}
{% set _ = ev_groups[b.evaluate_id].append(b) %}
{% endfor %}
{% for eid, branches in ev_groups.items() %}
### EVALUATE `{{ branches[0].subject }}` — paragraph `{{ branches[0].paragraph_name | default("-") }}` (line {{ branches[0].line_number }})

| WHEN | Action |
|------|--------|
{% for b in branches %}
| {% if b.is_default %}**WHEN OTHER**{% else %}`{{ b.when_condition }}`{% endif %} | {{ b.action_summary | default("...") }} |
{% endfor %}

{% endfor %}
{% endif %}

{% if cics_handles %}
## CICS HANDLE Routing

Each entry shows where exceptional CICS conditions are routed. Migration to a
modern stack should map these to try / catch handlers or middleware filters.

| Type | Condition | Target Paragraph | Line |
|------|-----------|------------------|------|
{% for h in cics_handles %}
| {{ h.handle_type }} | `{{ h.condition_name }}` | {% if h.target_paragraph %}`{{ h.target_paragraph }}`{% else %}*(suspend / cancel prior handler)*{% endif %} | {{ h.line_number }} |
{% endfor %}
{% endif %}

{% if cursor_lifecycles %}
## SQL Cursor Lifecycles

Each cursor's full DECLARE → OPEN → FETCH → CLOSE chain. Use this when porting
to streaming queries or paginated REST endpoints.

{% for c in cursor_lifecycles %}
### Cursor `{{ c.cursor_name }}`{% if c.table_name %} (over table `{{ c.table_name }}`){% endif %}


| Phase | Paragraph | Line |
|-------|-----------|------|
| DECLARE | {{ c.declare.paragraph if c.declare else "-" }} | {{ c.declare.line if c.declare else "-" }} |
| OPEN | {{ c.open.paragraph if c.open else "-" }} | {{ c.open.line if c.open else "-" }} |
{% for fp in c.fetch_paragraphs[:4] %}
| FETCH | {{ fp }} | {{ c.fetch_lines[loop.index0] }} |
{% endfor %}
| CLOSE | {{ c.close.paragraph if c.close else "-" }} | {{ c.close.line if c.close else "-" }} |

{% endfor %}
{% endif %}

{% if exec_cics %}
## CICS Commands

This program uses the following EXEC CICS commands:

| Command | Paragraph | Line | Details |
|---------|-----------|------|---------|
{% for c in exec_cics %}
| `{{ c.command }}` | {{ c.paragraph_name | default("-") }} | {{ c.line_number | default("-") }} | {{ c.details_json | default("-") | truncate(80) }} |
{% endfor %}

{% set cics_commands = exec_cics | map(attribute="command") | list %}
{% set cics_summary = {} %}
{% for c in exec_cics %}
{% if c.command in cics_summary %}
{% set _ = cics_summary.update({c.command: cics_summary[c.command] + 1}) %}
{% else %}
{% set _ = cics_summary.update({c.command: 1}) %}
{% endif %}
{% endfor %}
**Summary:** {{ exec_cics | length }} CICS command(s) — {% for cmd, cnt in cics_summary.items() %}{{ cmd }} ({{ cnt }}){% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}

{% if cics_workflow_notes %}
## CICS Screen Workflow Notes

These notes are derived directly from the COBOL source and BMS map usage. They are intended
to prevent migration errors where a PF key label is mistaken for the full transaction flow.

{% for note in cics_workflow_notes %}
### {{ note.title }}

{{ note.detail }}

{% if note.evidence %}
Evidence:
{% for ev in note.evidence %}
- {{ ev }}
{% endfor %}
{% endif %}

{% endfor %}
{% endif %}

{% if modernization_findings %}
## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
{% for finding in modernization_findings %}
| {{ finding.title }} | {{ finding.detail }} |
{% endfor %}

{% endif %}

## Business Rules

{% if business_rules %}
{% for rule in business_rules %}
- **{{ rule.rule_name }}** `{{ rule.rule_id }}`  
  {{ rule.rule_statement }}  
  [View Rule Details](../business-rules/{{ rule.rule_id }}.md)
{% endfor %}
{% else %}
*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*
{% endif %}

## Key Data Items

{% if data_items %}
| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
{% for item in data_items[:40] %}
| `{{ item.name }}` | {{ item.level_number | default("-") }} | `{{ item.picture | default("-") }}` | {{ item.section | default("-") }} | {{ item.business_name | default("-") }} |
{% endfor %}
{% if data_items | length > 40 %}

*Showing 40 of {{ data_items | length }} data items. See [Data Dictionary](../data-dictionary.md).*
{% endif %}
{% else %}
*No data items found for this program.*
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 4: Business Rules -----
TEMPLATES["business_rule.md.j2"] = '''\
# Business Rule: {{ rule_name }}

| Attribute | Value |
|-----------|-------|
| Rule ID | `{{ rule_id }}` |
| Category | {{ category | default("GENERAL") }} |
| Program | [{{ program_id }}](../programs/{{ program_id }}.md) |
| Paragraph | `{{ paragraph_name | default("-") }}` |
{% if line_start %}| Lines | {{ line_start }} - {{ line_end | default("") }} |{% endif %}

## Rule Statement

> {{ rule_statement }}

## Condition

{{ condition_text | default(condition) | default("When specific business conditions are met") }}

## Action

{{ action_text | default(action) | default("System performs the defined business action") }}

{% if source_code %}
## Source Code

```cobol
{{ source_code }}
```
{% endif %}

---

*Generated {{ generated_date }}*
'''

TEMPLATES["business_rules_index.md.j2"] = '''\
# Business Rules Catalog

> **Total Rules:** {{ rules | length }}  
> **Categories:** {{ categories | length }}

---

{% for category, cat_rules in rules_by_category.items() %}
## {{ category }} ({{ cat_rules | length }} rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
{% for rule in cat_rules %}
| [{{ rule.rule_id }}]({{ rule.rule_id }}.md) | {{ rule.rule_name }} | {{ rule.rule_statement | truncate(60) }} | [{{ rule.program_id }}](../programs/{{ rule.program_id }}.md) |
{% endfor %}

{% endfor %}

{% if not rules %}
*No business rules have been extracted yet. Run the LLM enrichment step to extract rules from IF/EVALUATE statements.*
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 5: Screen Documentation -----
TEMPLATES["screen.md.j2"] = '''\
# Screen: {{ screen_name }}

| Attribute | Value |
|-----------|-------|
| Map Name | `{{ map_name }}` |
| Mapset | `{{ mapset_name }}` |
{% if associated_program %}| Program | [{{ associated_program }}](../programs/{{ associated_program }}.md) |{% endif %}
{% if transaction_id %}| Transaction ID | `{{ transaction_id }}` |{% endif %}

## Screen Layout

The following fields are defined in this BMS map:

{% if input_fields %}
### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
{% for f in input_fields %}
| `{{ f.field_name }}` | {{ f.row_position }} | {{ f.col_position }} | {{ f.length | default(0) }} | {{ f.attributes | default("-") }} |
{% endfor %}
{% endif %}

{% if output_fields %}
### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
{% for f in output_fields %}
| `{{ f.field_name }}` | {{ f.row_position }} | {{ f.col_position }} | {{ f.length | default(0) }} | {{ f.attributes | default("-") }} |
{% endfor %}
{% endif %}

{% if label_fields %}
### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
{% for f in label_fields %}
| {{ f.description | default(f.field_name) }} | {{ f.row_position }} | {{ f.col_position }} |
{% endfor %}
{% endif %}

## Visual Mockup

```
{% for row_num in range(1, max_row + 1) %}
{% set row_fields = fields_by_row.get(row_num, []) %}
{% if row_fields %}
Row {{ "%2d" | format(row_num) }}: {% for f in row_fields %}{{ f.description | default(f.field_name) | default("____") }}  {% endfor %}

{% endif %}
{% endfor %}
```

---

*Generated {{ generated_date }}*
'''

TEMPLATES["screens_index.md.j2"] = '''\
# Screen Catalog

> **Total Screens:** {{ screens | length }}

---

| Screen | Map | Mapset | Program | Fields |
|--------|-----|--------|---------|--------|
{% for s in screens %}
| [{{ s.screen_name }}]({{ s.screen_name }}.md) | `{{ s.map_name | default("-") }}` | `{{ s.mapset_name | default("-") }}` | {% if s.associated_program %}[{{ s.associated_program }}](../programs/{{ s.associated_program }}.md){% else %}-{% endif %} | {{ s.field_names | default("-") }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Call Graph -----
TEMPLATES["call_graph.md.j2"] = '''\
# Program Call Hierarchy

> Inter-program call relationships across the entire {{ system_name }} application.

## Visual Call Graph

```mermaid
graph LR
{% set seen = {} %}
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program }}["{{ call.caller_name if call.caller_name else call.caller_program }}"] --> {{ call.called_program }}["{{ call.called_name if call.called_name else call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endif %}
{% endfor %}
```

## Call Matrix

| Caller | Calls | Line |
|--------|-------|------|
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | {{ call.called_program | program_link("../programs/") }} | {{ call.line_number | default("-") }} |
{% endif %}
{% endfor %}

## Entry Points

Programs not called by any other program (likely top-level entry points or CICS transaction starters):

{% for prog in entry_points %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}

## Leaf Programs

Programs that don't call any other program (utility or terminal logic):

{% for prog in leaf_programs %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Data Dictionary -----
TEMPLATES["data_dictionary.md.j2"] = '''\
# Data Dictionary

> **Total Data Items:** {{ total_items }}  
> **Programs:** {{ programs_count }}

---

{% for section, items in items_by_section.items() %}
## {{ section }} Section ({{ items | length }} items)

| Name | Level | Picture | Program | Business Name |
|------|-------|---------|---------|---------------|
{% for item in items[:100] %}
| `{{ item.name }}` | {{ item.level_number | default("-") }} | `{{ item.picture | default("-") }}` | [{{ item.program_id }}](programs/{{ item.program_id }}.md) | {{ item.business_name | default("-") }} |
{% endfor %}
{% if items | length > 100 %}

*Showing 100 of {{ items | length }} items in {{ section }}.*
{% endif %}

{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- JCL Job Index -----
TEMPLATES["jcl_index.md.j2"] = '''\
# JCL Jobs Catalog

> **Total Jobs:** {{ jobs | length }}
> All batch JCL jobs found in the repository.

---

| Job Name | File | Description | Steps | Programs Called |
|----------|------|-------------|-------|----------------|
{% for job in jobs %}
| [{{ job.job_name }}]({{ job.job_name }}.md) | `{{ job.file_name }}` | {{ job.job_description | default("-") | truncate(50) }} | {{ job.step_count | default(0) }} | {{ job.programs_called | join(", ") if job.programs_called else "-" }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- JCL Job Detail -----
TEMPLATES["jcl_job.md.j2"] = '''\
# JCL Job: {{ job_name }}

| Attribute | Value |
|-----------|-------|
| File | `{{ file_name }}` |
| Description | {{ job_description | default("-") }} |
| Job Class | {{ job_class | default("-") }} |
| Msg Class | {{ msg_class | default("-") }} |
| Steps | {{ steps | length }} |

{% if header_comments %}
## Job Description (Comments)

```
{{ header_comments }}
```
{% endif %}

## Job Steps

{% for step in steps %}
### Step {{ loop.index }}: {{ step.step_name }}

| Attribute | Value |
|-----------|-------|
| Step Name | `{{ step.step_name }}` |
| Type | {{ step.step_type | default("-") }} |
{% if step.program %}| Program | {% if step.program_is_cobol %}[{{ step.program }}](../programs/{{ step.program }}.md){% else %}`{{ step.program }}`{% endif %} |{% endif %}
{% if step.proc %}| Procedure | `{{ step.proc }}` |{% endif %}
{% if step.cond %}| COND | `{{ step.cond }}` |{% endif %}

{% if step.step_comments %}
> {{ step.step_comments | replace("\n", "  \n> ") }}
{% endif %}

{% if step.datasets %}
#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
{% for ds in step.datasets %}
{% if not ds.is_inline %}
| `{{ ds.dd_name }}` | `{{ ds.dsn | default("-") }}` | {{ ds.disp | default("-") }} | {{ ds.direction | default("-") }} | {{ ds.recfm | default("-") }} | {{ ds.lrecl | default("-") }} |
{% endif %}
{% endfor %}
{% endif %}

{% if step.sysin_data %}
#### Inline SYSIN

```
{% for line in step.sysin_data %}
{{ line }}
{% endfor %}
```
{% endif %}

---
{% endfor %}

## Summary

{% if programs_called %}
### COBOL Programs Executed

{% for prog in programs_called %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}
{% endif %}

{% if input_datasets %}
### Input Datasets

{% for dsn in input_datasets %}
- `{{ dsn }}`
{% endfor %}
{% endif %}

{% if output_datasets %}
### Output Datasets

{% for dsn in output_datasets %}
- `{{ dsn }}`
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Copybook Reference -----
TEMPLATES["copybook_reference.md.j2"] = '''\
# Copybook Reference

> **Total Copybooks:** {{ copybooks | length }}

Copybooks are shared data structure definitions included (COPY) by multiple programs.

---

| Copybook | Used By Programs | Business Name |
|----------|-----------------|---------------|
{% for cb in copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.used_by | default("-") }} | {{ cb.business_name | default("-") }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 6: Linked Programs (Clusters) -----
TEMPLATES["cluster.md.j2"] = '''\
# Linked Programs: Cluster {{ cluster_id }}

> **{{ size }} interconnected programs** linked through call relationships and shared copybooks.

---

## Why These Programs Are Linked

These programs form a connected cluster because they either call each other directly,
share copybook data structures, or are transitively linked through intermediate programs.
A change to any one of them has the potential to affect the others.

## Programs in This Cluster

| Program | Type | Business Name |
|---------|------|---------------|
{% for m in member_details %}
| [{{ m.program_id }}](../programs/{{ m.program_id }}.md) | {{ m.program_type | default("-") }} | {{ m.business_name | default("-") }} |
{% endfor %}

## Internal Call Flow

{% if internal_calls %}
```mermaid
graph LR
{% set seen = {} %}
{% for call in internal_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program | mermaid_id }}["{{ call.caller_program }}"] --> {{ call.called_program | mermaid_id }}["{{ call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

| Caller | Calls | Line |
|--------|-------|------|
{% for call in internal_calls %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | {{ call.called_program | program_link("../programs/") }} | {{ call.line_number | default("-") }} |
{% endfor %}
{% else %}
*No direct call relationships between these programs — they are linked exclusively through shared copybooks.*
{% endif %}

{% if shared_copybooks %}
## Shared Copybooks (Data Coupling)

These copybooks are shared by 2+ programs in this cluster. Changing them affects multiple programs:

| Copybook | Shared By |
|----------|-----------|
{% for cb in shared_copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.programs }} |
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

TEMPLATES["clusters_index.md.j2"] = '''\
# Linked Programs Index

> **{{ clusters | length }} clusters** detected across the system.
> Programs are grouped by call relationships and shared copybook data coupling.

---

{% set connected = clusters | selectattr("is_standalone", "false") | list %}
{% set standalone = clusters | selectattr("is_standalone", "true") | list %}

## Connected Clusters ({{ connected | length }})

{% if connected %}
| Cluster | Programs | Internal Calls | Shared Copybooks |
|---------|----------|---------------|------------------|
{% for c in connected %}
| [Cluster {{ c.cluster_id }}](CLUSTER-{{ c.cluster_id }}.md) | {{ c.size }} | {{ c.internal_calls | length }} | {{ c.shared_copybooks | length }} |
{% endfor %}
{% else %}
*No multi-program clusters detected.*
{% endif %}

## Standalone Programs ({{ standalone | length }})

These programs have no call or copybook relationships with other programs:

{% for c in standalone %}
- [{{ c.members[0] }}](../programs/{{ c.members[0] }}.md)
{% endfor %}

---

*Generated {{ generated_date }}*
'''


# ============================================================
# Documentation Generator
# ============================================================

class DocGenerator:
    """Generates complete Swimm-style documentation from SQLite knowledge base."""

    def __init__(
        self,
        db_loader,
        output_dir: str = "docs",
        templates_dir: str = None,
        repo_path: str = None,
        system_name: str = "CardDemo",
    ):
        self.db = db_loader
        self.output_dir = Path(output_dir)
        self.repo_path = repo_path
        self.system_name = system_name

        self.env = Environment(
            loader=InlineTemplateLoader(TEMPLATES, templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Custom filters
        self.env.filters["basename"] = lambda x: Path(x).name if x else ""
        self.env.filters["truncate"] = lambda x, n: (x[:n] + "...") if x and len(str(x)) > n else (x or "")
        self.env.filters["mermaid_id"] = lambda x: (x or "UNKNOWN").replace("-", "_").replace(" ", "_")
        self.known_program_ids = {p["program_id"] for p in self.db.get_all_programs()}

        def program_link(program_id, prefix=""):
            """Link local COBOL programs; render external runtime calls as code."""
            if not program_id:
                return "-"
            pid = str(program_id)
            if pid in self.known_program_ids:
                return f"[{pid}]({prefix}{pid}.md)"
            return f"`{pid}`"

        self.env.filters["program_link"] = program_link

        def mermaid_cb_node(cb_name, node_id_prefix="CB_"):
            """Generate a full Mermaid copybook node line with hexagon shape.
            Uses {{ }} which is Mermaid hexagon syntax — this filter outputs it
            as a raw string to avoid Jinja2 clash."""
            safe_id = (cb_name or "UNKNOWN").replace("-", "_").replace(" ", "_")
            node_id = f"{node_id_prefix}{safe_id}"
            # Double curly braces in Python f-string become literal { }
            return f'{node_id}{{{{"{cb_name}"}}}}:::copybook'

        self.env.filters["mermaid_cb_node"] = mermaid_cb_node
        
        # Live code link filter - generates clickable source links
        def code_link(file_path, line=None, text=None):
            """Generate a clickable link to source code.
            
            Supports:
            - VS Code: Opens file at line when clicked in VS Code markdown preview
            - GitHub: #L{line} anchors work in GitHub
            - Relative paths for portability
            """
            if not file_path:
                return text or "source"
            
            # Make path relative to docs folder for portability
            try:
                rel_path = Path(file_path).as_posix()
                # Calculate relative path from docs to repo
                if repo_path:
                    rel_path = f"../{repo_path}/{Path(file_path).name}"
            except:
                rel_path = file_path
            
            display = text or Path(file_path).name
            
            if line and int(line) > 0:
                # GitHub-style line anchor + VS Code compatible
                return f"[{display}]({rel_path}#L{line})"
            else:
                return f"[{display}]({rel_path})"
        
        self.env.filters["code_link"] = code_link
        
        # Store repo_path for the filter
        self.env.globals["repo_path"] = repo_path

    # ================================================================
    # Source-level data contract helpers
    # ================================================================

    @staticmethod
    def _cobol_source_body(text: str) -> List[str]:
        """Return non-comment COBOL source text without sequence columns."""
        return [row["text"] for row in DocGenerator._cobol_source_rows(text)]

    @staticmethod
    def _cobol_source_rows(text: str) -> List[Dict[str, Any]]:
        """Return non-comment COBOL source rows with original line numbers."""
        rows = []
        for line_number, raw in enumerate(text.splitlines(), start=1):
            marker = raw[6:7] if len(raw) > 6 else ""
            if marker in ("*", "/", "D"):
                continue
            body = raw[6:72] if len(raw) > 6 else raw
            body = body.rstrip()
            if body.strip():
                rows.append({"line_number": line_number, "text": body})
        return rows

    @staticmethod
    def _logical_cobol_lines(lines: List[str]) -> List[str]:
        """Join simple continued COBOL declarations into logical statements."""
        logical = []
        current = ""
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^(01|05|10|15|20|25|30|49|66|77|88)\s+", stripped, re.IGNORECASE):
                if current:
                    logical.append(current.strip())
                current = stripped
            elif current:
                current = f"{current} {stripped}"
            else:
                current = stripped
            if stripped.endswith(".") and current:
                logical.append(current.strip())
                current = ""
        if current:
            logical.append(current.strip())
        return logical

    @staticmethod
    def _parse_cobol_data_declarations(lines: List[str]) -> List[Dict[str, Any]]:
        """Parse common COBOL data declarations into doc-friendly field rows."""
        fields = []
        last_field = None
        for stmt in DocGenerator._logical_cobol_lines(lines):
            m = re.match(r"^(01|05|10|15|20|25|30|49|66|77|88)\s+([A-Z0-9-]+|FILLER)\b(.*)$", stmt, re.IGNORECASE)
            if not m:
                continue

            level, name, rest = m.group(1), m.group(2).upper(), m.group(3).strip()
            pic_match = re.search(r"\bPIC(?:TURE)?\s+([A-Z0-9()V+\-,]+)", rest, re.IGNORECASE)
            value_match = re.search(r"\bVALUE\s+(.+?)(?:\.|$)", rest, re.IGNORECASE)
            occurs_match = re.search(r"\bOCCURS\s+([0-9]+)\s+TIMES", rest, re.IGNORECASE)
            usage_match = re.search(
                r"\b(COMP-3|COMP-5|COMP-4|COMP|BINARY|PACKED-DECIMAL|DISPLAY|INDEX)\b",
                rest,
                re.IGNORECASE,
            )

            value = value_match.group(1).strip() if value_match else ""
            value = re.sub(r"\s+", " ", value).rstrip(".")

            if level == "88":
                if last_field:
                    last_field.setdefault("status_values", []).append({
                        "name": name,
                        "value": value,
                    })
                continue

            field = {
                "level": level,
                "name": name,
                "picture": pic_match.group(1).upper().rstrip(".") if pic_match else "",
                "usage": usage_match.group(1).upper() if usage_match else "",
                "occurs": occurs_match.group(1) if occurs_match else "",
                "value": value,
                "meaning": DocGenerator._business_meaning(name),
                "modern_type": "",
                "status_values": [],
            }
            field["cobol_type"] = DocGenerator._format_cobol_type(field)
            field["modern_type"] = DocGenerator._modern_type(field)
            field["format_note"] = DocGenerator._format_note(field)
            fields.append(field)
            if name != "FILLER":
                last_field = field
        return fields

    @staticmethod
    def _format_cobol_type(field: Dict[str, Any]) -> str:
        parts = []
        if field.get("picture"):
            parts.append(f"PIC {field['picture']}")
        if field.get("usage"):
            parts.append(field["usage"])
        if field.get("occurs"):
            parts.append(f"OCCURS {field['occurs']}")
        return " ".join(parts) or "GROUP"

    @staticmethod
    def _pic_digits(pic: str) -> tuple[int, int]:
        """Return total digits and scale for a numeric PIC."""
        if not pic:
            return 0, 0
        pic = pic.upper().replace("S", "")

        def count_digits(part: str) -> int:
            total = 0
            for token, repeat in re.findall(r"([9X])(?:\((\d+)\))?", part):
                total += int(repeat or "1")
            return total

        if "V" in pic:
            left, right = pic.split("V", 1)
            scale = count_digits(right)
            return count_digits(left) + scale, scale
        return count_digits(pic), 0

    @staticmethod
    def _modern_type(field: Dict[str, Any]) -> str:
        pic = (field.get("picture") or "").upper()
        usage = (field.get("usage") or "").upper()
        total, scale = DocGenerator._pic_digits(pic)
        if not pic:
            return "OBJECT"
        if "X" in pic:
            length = DocGenerator._pic_digits(pic.replace("X", "9"))[0]
            return f"STRING({length})" if length else "STRING"
        if scale:
            return f"DECIMAL({total},{scale})"
        if "COMP-3" in usage and total > 9:
            return "BIGINT"
        if "COMP" in usage or "BINARY" in usage:
            return "INTEGER" if total <= 9 else "BIGINT"
        if total > 9:
            return "BIGINT"
        return "INTEGER"

    @staticmethod
    def _format_note(field: Dict[str, Any]) -> str:
        name = field.get("name", "")
        pic = field.get("picture", "")
        if re.search(r"(DATE|DT|YYDDD)", name) and re.search(r"9\(0?5\)|9\(0?6\)|X\(0?8\)|X\(10\)", pic, re.IGNORECASE):
            return "Date-like field; verify YYDDD, YYMMDD, or ISO format before migration."
        if field.get("occurs"):
            return f"Repeating field, {field['occurs']} occurrences."
        if field.get("status_values"):
            vals = ", ".join(f"{v['name']}={v['value']}" for v in field["status_values"][:4])
            return f"Status/code field: {vals}"
        return ""

    @staticmethod
    def _business_meaning(name: str) -> str:
        clean = re.sub(r"^(WS|WK|PA|CA|CDEMO|QUAL|SSA|P)-", "", name.upper())
        special = {
            "ACCT-ID": "Account ID",
            "ACCNTID": "Account ID",
            "CUST-ID": "Customer ID",
            "AUTH-DATE-9C": "Authorization Date",
            "AUTH-TIME-9C": "Authorization Time",
            "AUTH-RESP-CODE": "Authorization Response Code",
            "TRANSACTION-AMT": "Transaction Amount",
            "APPROVED-AMT": "Approved Amount",
            "ROOT-SEG-KEY": "Root Segment Key",
            "CHILD-SEG-REC": "Child Segment Record",
        }
        if clean in special:
            return special[clean]
        words = []
        dictionary = {
            "ACCT": "Account",
            "ACCNT": "Account",
            "CUST": "Customer",
            "AUTH": "Authorization",
            "AMT": "Amount",
            "DT": "Date",
            "DATE": "Date",
            "TIME": "Time",
            "RESP": "Response",
            "CODE": "Code",
            "STATUS": "Status",
            "CARD": "Card",
            "NUM": "Number",
            "MERCHANT": "Merchant",
            "ID": "ID",
            "KEY": "Key",
            "SEG": "Segment",
            "REC": "Record",
            "BALANCE": "Balance",
            "LIMIT": "Limit",
            "CNT": "Count",
            "FRAUD": "Fraud",
        }
        for token in clean.split("-"):
            words.append(dictionary.get(token, token.title()))
        return " ".join(words)

    def _find_copybook_path(self, copybook_name: str) -> Optional[Path]:
        roots = []
        if self.repo_path:
            roots.append(Path(self.repo_path))
        roots.append(Path("."))
        candidates = [f"{copybook_name}.cpy", f"{copybook_name}.CPY", copybook_name]
        for root in roots:
            if not root.exists():
                continue
            for candidate in candidates:
                matches = list(root.rglob(candidate))
                if matches:
                    return matches[0]
        return None

    @staticmethod
    def _copybook_contexts(lines: List[str]) -> Dict[str, Dict[str, Any]]:
        contexts = {}
        current_section = ""
        current_group = ""
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if re.search(r"\b(FILE|WORKING-STORAGE|LINKAGE)\s+SECTION\b", stripped, re.IGNORECASE):
                current_section = stripped.replace(".", "").title()
            group_match = re.match(r"^01\s+([A-Z0-9-]+)\b", stripped, re.IGNORECASE)
            if group_match:
                current_group = group_match.group(1).upper()
            copy_match = re.match(r"^COPY\s+([A-Z0-9-]+)", stripped, re.IGNORECASE)
            if copy_match:
                contexts[copy_match.group(1).upper()] = {
                    "record_name": current_group,
                    "section": current_section,
                    "line_number": idx,
                }
        return contexts

    @staticmethod
    def _file_record_contracts(lines: List[str]) -> List[Dict[str, Any]]:
        contracts = []
        current_file = None
        current_fields = []
        for line in lines:
            stripped = line.strip()
            fd_match = re.match(r"^FD\s+([A-Z0-9-]+)\b", stripped, re.IGNORECASE)
            if fd_match:
                if current_file:
                    contracts.append(current_file | {"fields": current_fields})
                current_file = {
                    "file_name": fd_match.group(1).upper(),
                    "record_name": "",
                }
                current_fields = []
                continue
            if not current_file:
                continue
            if re.search(r"\b(WORKING-STORAGE|LINKAGE)\s+SECTION\b", stripped, re.IGNORECASE):
                contracts.append(current_file | {"fields": current_fields})
                current_file = None
                current_fields = []
                continue
            if re.match(r"^01\s+", stripped, re.IGNORECASE) and not current_file.get("record_name"):
                m = re.match(r"^01\s+([A-Z0-9-]+)\b", stripped, re.IGNORECASE)
                if m:
                    current_file["record_name"] = m.group(1).upper()
            parsed = DocGenerator._parse_cobol_data_declarations([stripped])
            current_fields.extend(parsed)
        if current_file:
            contracts.append(current_file | {"fields": current_fields})
        return [c for c in contracts if c.get("fields")]

    def _build_data_contracts(self, details: Dict[str, Any]) -> Dict[str, Any]:
        source_path = Path(details.get("file_path") or "")
        source_lines = []
        source_rows = []
        if source_path.exists():
            try:
                source_text = source_path.read_text(encoding="utf-8", errors="ignore")
                source_rows = self._cobol_source_rows(source_text)
                source_lines = [row["text"] for row in source_rows]
            except Exception:
                source_lines = []
                source_rows = []

        copy_contexts = self._copybook_contexts(source_lines)
        copybook_contracts = []
        for cb in details.get("copybooks", []):
            cb_name = (cb.get("copybook_name") or "").upper()
            cb_path = self._find_copybook_path(cb_name)
            if not cb_path:
                continue
            try:
                cb_lines = self._cobol_source_body(cb_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            fields = self._parse_cobol_data_declarations(cb_lines)
            if not fields:
                continue
            ctx = copy_contexts.get(cb_name, {})
            embedded_group = next(
                (field["name"] for field in fields if field.get("level") == "01" and field.get("name") != "FILLER"),
                None,
            )
            copybook_contracts.append({
                "copybook_name": cb_name,
                "record_name": embedded_group or ctx.get("record_name") or cb_name,
                "section": ctx.get("section") or "-",
                "line_number": ctx.get("line_number"),
                "fields": fields,
            })

        return {
            "file_records": self._file_record_contracts(source_lines),
            "copybooks": copybook_contracts,
            "moves": self._data_contract_moves(source_rows or source_lines),
        }

    @staticmethod
    def _data_contract_moves(lines: List[Any]) -> List[Dict[str, Any]]:
        moves = []
        interesting = re.compile(
            r"(REC|RECORD|SEG|SEGMENT|KEY|SSA|FILE|AUTH|ACCT|CUST|AMT|DATE|STATUS)",
            re.IGNORECASE,
        )
        for idx, line in enumerate(lines, start=1):
            if isinstance(line, dict):
                line_number = line.get("line_number") or idx
                line = line.get("text") or ""
            else:
                line_number = idx
            stripped = line.strip()
            m = re.match(r"^MOVE\s+(.+?)\s+TO\s+(.+?)(?:\.|$)", stripped, re.IGNORECASE)
            if not m:
                continue
            source = re.sub(r"\s+", " ", m.group(1).strip())
            target = re.sub(r"\s+", " ", m.group(2).strip())
            if not (interesting.search(source) or interesting.search(target)):
                continue
            moves.append({
                "line_number": line_number,
                "source": source,
                "target": target,
                "meaning": f"{source} populates {target}",
            })
        return moves[:30]

    @staticmethod
    def _find_paragraph_for_line(details: Dict[str, Any], line_number: int) -> Optional[str]:
        for para in details.get("paragraphs", []) or []:
            start = para.get("line_start") or 0
            end = para.get("line_end") or 0
            if start and end and start <= line_number <= end:
                return para.get("paragraph_name") or para.get("name")
        return None

    @staticmethod
    def _extract_performs_from_source(details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract simple PERFORM paragraph edges directly from source."""
        source_path = Path(details.get("file_path") or "")
        if not source_path.exists():
            return []
        try:
            rows = DocGenerator._cobol_source_rows(source_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            return []

        paragraph_names = {
            (p.get("paragraph_name") or p.get("name") or "").upper()
            for p in details.get("paragraphs", []) or []
            if p.get("paragraph_name") or p.get("name")
        }
        if not paragraph_names:
            return []

        reserved = {"UNTIL", "VARYING", "TIMES", "WITH", "AFTER", "BEFORE", "TEST"}
        performs = []
        for row in rows:
            text = row["text"].strip()
            if "PERFORM" not in text.upper():
                continue
            for match in re.finditer(r"\bPERFORM\s+([A-Z][A-Z0-9-]+)\b", text, re.IGNORECASE):
                target = match.group(1).upper()
                if target in reserved or target not in paragraph_names:
                    continue
                source = DocGenerator._find_paragraph_for_line(details, row["line_number"])
                if not source:
                    continue
                performs.append({
                    "program_id": details.get("program_id"),
                    "source_paragraph": source,
                    "target_paragraph": target,
                    "perform_type": "SIMPLE",
                    "line_number": row["line_number"],
                    "condition": None,
                })
        return performs

    @staticmethod
    def _merge_performs(existing: List[Dict[str, Any]], source_performs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        merged = []
        seen = set()
        for perf in (existing or []) + (source_performs or []):
            key = (
                perf.get("source_paragraph"),
                perf.get("target_paragraph"),
                perf.get("line_number"),
            )
            if key in seen:
                continue
            seen.add(key)
            merged.append(perf)
        return sorted(merged, key=lambda p: p.get("line_number") or 0)

    @staticmethod
    def _build_cics_workflow_notes(details: Dict[str, Any], performs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build deterministic CICS workflow notes for screen-driven programs."""
        exec_cics = details.get("exec_cics") or []
        if not exec_cics:
            return []

        source_path = Path(details.get("file_path") or "")
        rows = []
        if source_path.exists():
            try:
                rows = DocGenerator._cobol_source_rows(source_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                rows = []

        def source_hits(pattern: str, limit: int = 6) -> List[str]:
            hits = []
            regex = re.compile(pattern, re.IGNORECASE)
            for row in rows:
                if regex.search(row["text"]):
                    hits.append(f"L{row['line_number']}: `{row['text'].strip()}`")
                    if len(hits) >= limit:
                        break
            return hits

        def cics_hits(command: str) -> List[str]:
            hits = []
            for c in exec_cics:
                if (c.get("command") or "").upper() == command:
                    para = c.get("paragraph_name") or "-"
                    line = c.get("line_number") or "-"
                    details_json = c.get("details_json") or "-"
                    hits.append(f"L{line} in `{para}`: EXEC CICS {command} {details_json}")
            return hits

        notes = []
        commands = {(c.get("command") or "").upper() for c in exec_cics}

        if "XCTL" in commands:
            notes.append({
                "title": "Program transfers use XCTL, not a soft return",
                "detail": (
                    "`EXEC CICS XCTL` transfers control to another program and does not return to the "
                    "current program like a subroutine call. Document PF-key navigation that reaches this "
                    "paragraph as a CICS transfer, not as an in-place screen redisplay."
                ),
                "evidence": cics_hits("XCTL"),
            })

        no_commarea_evidence = source_hits(r"\bIF\s+EIBCALEN\s*=\s*0\b") + source_hits(r"\bMOVE\s+'COSGN00C'\s+TO\s+CDEMO-TO-PROGRAM\b")
        if no_commarea_evidence and "XCTL" in commands:
            notes.append({
                "title": "Initial entry without COMMAREA transfers to sign-on",
                "detail": (
                    "When `EIBCALEN = 0`, this program prepares `COSGN00C` as the target and follows "
                    "the return/transfer path. It does not display its own BMS map on that entry path."
                ),
                "evidence": no_commarea_evidence + cics_hits("XCTL")[:1],
            })

        pf3_evidence = source_hits(r"\bWHEN\s+DFHPF3\b") + source_hits(r"\bPERFORM\s+RETURN-TO-PREV-SCREEN\b")
        if pf3_evidence and "XCTL" in commands:
            notes.append({
                "title": "PF3 navigation resolves through RETURN-TO-PREV-SCREEN",
                "detail": (
                    "PF3 selects the `RETURN-TO-PREV-SCREEN` path. That paragraph ends in `EXEC CICS XCTL`, "
                    "so PF3 is a transfer to the target program held in the COMMAREA routing fields."
                ),
                "evidence": pf3_evidence[:5] + cics_hits("XCTL")[:1],
            })

        pf5_evidence = source_hits(r"\bWHEN\s+DFHPF5\b") + source_hits(r"\bPERFORM\s+DELETE-USER-INFO\b")
        fetch_prompt = source_hits(r"Press\s+PF5\s+key\s+to\s+delete", limit=2)
        if pf5_evidence or fetch_prompt:
            notes.append({
                "title": "PF5 delete is a two-step user flow",
                "detail": (
                    "The screen label says `F5=Delete`, but the COBOL flow first validates/fetches the user "
                    "record. On a successful read, the program displays a message telling the user to press PF5. "
                    "The actual delete is then executed through `DELETE-USER-INFO` and `DELETE-USER-SEC-FILE`."
                ),
                "evidence": pf5_evidence[:4] + fetch_prompt + cics_hits("READ")[:1] + cics_hits("DELETE")[:1],
            })

        msg_evidence = source_hits(r"\bMOVE\s+.+\s+TO\s+ERRMSGO\b") + source_hits(r"\bERRMSGI\b", limit=2)
        if msg_evidence:
            notes.append({
                "title": "Error/message text is written to the BMS output field",
                "detail": (
                    "`ERRMSGI` exists in the input copybook area, but this program displays messages by moving "
                    "`WS-MESSAGE` to `ERRMSGO OF COUSR3AO`. Documentation should refer to `ERRMSGO` when "
                    "describing rendered error or status messages."
                ),
                "evidence": msg_evidence[:5],
            })

        err_flag_evidence = source_hits(r"\bSET\s+ERR-FLG-OFF\s+TO\s+TRUE\b") + source_hits(r"\bERR-FLG-ON\b", limit=4)
        if err_flag_evidence:
            notes.append({
                "title": "ERR-FLG is reset at the start of each run",
                "detail": (
                    "`ERR-FLG` starts each invocation on the off path via `SET ERR-FLG-OFF TO TRUE`. "
                    "Validation and file-error branches set or test `ERR-FLG-ON` to stop later processing."
                ),
                "evidence": err_flag_evidence[:6],
            })

        send_edges = [
            f"L{p.get('line_number')}: `{p.get('source_paragraph')}` performs `{p.get('target_paragraph')}`"
            for p in performs
            if (p.get("target_paragraph") or "").upper().startswith("SEND-")
        ]
        read_sends = [edge for edge in send_edges if "READ-" in edge.upper()]
        if len(send_edges) > 1 and "SEND" in commands:
            notes.append({
                "title": "The BMS map can be sent from multiple paths",
                "detail": (
                    "Screen output is centralized in the send paragraph, but several routines can perform it. "
                    "If a read routine sends the map and its caller also sends the map, a modern UI migration "
                    "must preserve or deliberately remove that duplicate response behavior."
                ),
                "evidence": (read_sends or send_edges)[:8] + cics_hits("SEND")[:1],
            })

        return notes

    def _build_modernization_findings(
        self,
        details: Dict[str, Any],
        data_contracts: Dict[str, Any],
        source_literals: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        findings = []
        pid = details.get("program_id")
        for lit in source_literals:
            if lit.get("name") == "WS-PGMNAME" and lit.get("value") and lit["value"].upper() != pid:
                findings.append({
                    "title": "Program name literal differs from PROGRAM-ID",
                    "detail": f"`WS-PGMNAME` is `{lit['value']}` while `PROGRAM-ID` is `{pid}`. Treat this as a migration review item; it may be copied template state or an intentional external name.",
                })

        field_names = {
            field["name"]
            for contract in data_contracts.get("file_records", []) + data_contracts.get("copybooks", [])
            for field in contract.get("fields", [])
        }
        field_names.update((item.get("name") or "") for item in details.get("data_items", []))
        if {"WS-CHKPT-ID", "WK-CHKPT-ID", "WS-NO-CHKP", "P-CHKP-FREQ"} & field_names:
            ims_checkpoint_calls = [
                im for im in details.get("ims_calls", [])
                if (im.get("function_code") or "").upper() in {"CHKP", "XRST"}
            ]
            if not ims_checkpoint_calls:
                findings.append({
                    "title": "Checkpoint/restart fields without checkpoint calls",
                    "detail": "Checkpoint-style fields exist, but no IMS `CHKP` or `XRST` call was extracted. Confirm whether restart logic was abandoned or still expected operationally.",
                })

        unused_candidates = sorted(
            name for name in field_names
            if re.search(r"(DEBUG|EXPIRY|DAY-DIFF|NO-CHKP|CHKPT)", name)
        )
        if unused_candidates:
            findings.append({
                "title": "Template/debug fields require usage review",
                "detail": "Fields such as " + ", ".join(f"`{n}`" for n in unused_candidates[:8]) + " look like debug, checkpoint, or abandoned template state. Verify references before designing modern DTOs or database columns.",
            })

        source_path = Path(details.get("file_path") or "")
        if source_path.exists():
            try:
                body = "\n".join(self._cobol_source_body(source_path.read_text(encoding="utf-8", errors="ignore")))
                numeric_match = re.search(r"\b([A-Z0-9-]+)\s+IS\s+NUMERIC\b", body, re.IGNORECASE)
                if numeric_match:
                    findings.append({
                        "title": "Numeric validation on a COBOL numeric field",
                        "detail": f"`{numeric_match.group(1).upper()} IS NUMERIC` was found in source. If the field is packed or binary numeric, this may be corruption detection rather than normal validation.",
                    })
                if re.search(r"\bIF\b[\s\S]{0,500}\bIF\b[\s\S]{0,500}\.", body, re.IGNORECASE):
                    findings.append({
                        "title": "Nested IF blocks need compiler-accurate validation",
                        "detail": "Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL.",
                    })
            except Exception:
                pass

        return findings

    def generate_all(self):
        """Generate all 6 documentation layers plus supporting docs."""
        console.print("[cyan]Generating Swimm-style documentation...[/cyan]")

        # Create output directories
        for subdir in ["programs", "modules", "business-rules", "screens", "diagrams", "clusters", "jcl"]:
            dir_path = self.output_dir / subdir
            dir_path.mkdir(parents=True, exist_ok=True)

        generated = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Layer 1: System Overview
        self._generate_system_overview(generated)

        # Layer 2: Linked Programs (Clusters)
        self._generate_linked_clusters(generated)

        # Layer 3: Module Documentation
        self._generate_module_docs(generated)

        # Layer 4: Program Walkthroughs (with dependency + impact)
        self._generate_program_docs(generated)

        # Layer 5: Business Rules Catalog
        self._generate_business_rules(generated)

        # Layer 6: Screen Catalog
        self._generate_screen_docs(generated)

        # Supporting: Call Graph, Data Dictionary, Copybook Reference, JCL
        self._generate_call_graph(generated)
        self._generate_data_dictionary(generated)
        self._generate_copybook_reference(generated)
        self._generate_jcl_docs(generated)
        self._generate_data_flow_chains_doc(generated)

        total = len(list(self.output_dir.rglob("*.md")))
        console.print(f"[green]OK - Generated {total} documentation files in {self.output_dir}[/green]")

    # ================================================================
    # Layer 1: System Overview
    # ================================================================

    def _generate_data_flow_chains_doc(self, generated_date: str):
        """Render docs/diagrams/data-flow-chains.md from get_data_flow_chains()."""
        try:
            chains = self.db.get_data_flow_chains(max_hops=4)
        except Exception:
            chains = []
        if not chains:
            return
        lines = [
            f"# End-to-End Data Flow Chains",
            "",
            f"> Auto-generated {generated_date}",
            "",
            "Each chain traces how data flows: a JCL job triggers a program, which writes "
            "a file/dataset, which is then read by another program, and so on. Use this to "
            "decide migration units that must move together.",
            "",
            f"**Chains discovered:** {len(chains)}",
            "",
        ]
        for i, c in enumerate(chains, 1):
            chain = c["chain"]
            kind = "JCL-rooted" if c.get("starts_with_jcl") else "Program-rooted"
            lines.append(f"## Chain {i} — {kind}")
            lines.append("")
            steps = []
            for step in chain:
                if step.get("job"):
                    steps.append(f"`JCL {step['job']}`")
                elif step.get("program"):
                    steps.append(f"[{step['program']}](../programs/{step['program']}.md)")
                if step.get("file"):
                    steps.append(f"`file {step['file']}`")
            lines.append(" → ".join(steps))
            lines.append("")
        out_path = self.output_dir / "diagrams" / "data-flow-chains.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines), encoding="utf-8")
        console.print(f"  [green]OK - Generated {out_path.name} ({len(chains)} chains)[/green]")

    def _generate_system_overview(self, generated_date: str):
        console.print("  [cyan]Layer 1: System Overview[/cyan]")

        programs = self.db.get_all_programs()
        call_graph = self.db.get_call_graph()
        modules = self.db.get_all_modules()
        rules = self.db.get_all_business_rules()
        screens = self.db.get_all_screens()
        copybooks = self.db.get_copybooks()

        # Compute stats
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data_items")
        total_data_items = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM exec_cics")
        total_cics_commands = cursor.fetchone()[0]
        try:
            cursor.execute("SELECT COUNT(*) FROM exec_sql")
            total_sql_statements = cursor.fetchone()[0]
        except Exception:
            total_sql_statements = 0

        online = [p for p in programs if (p.get("program_type") or "").upper() == "ONLINE"]
        batch = [p for p in programs if (p.get("program_type") or "").upper() != "ONLINE"]

        # Entry points
        called_set = set(c["called_program"] for c in call_graph)
        all_set = set(p["program_id"] for p in programs)
        entry_points = sorted(all_set - called_set)

        # JCL job count for overview narrative
        try:
            cursor.execute("SELECT COUNT(*) FROM jcl_jobs")
            total_jcl_jobs = cursor.fetchone()[0]
        except Exception:
            total_jcl_jobs = 0

        template = self.env.get_template("system_overview.md.j2")
        content = template.render(
            system_name=self.system_name,
            total_programs=len(programs),
            total_modules=len(modules),
            total_screens=len(screens),
            total_data_items=total_data_items,
            total_cics_commands=total_cics_commands,
            total_sql_statements=total_sql_statements,
            total_calls=len(call_graph),
            total_rules=len(rules),
            total_copybooks=len(copybooks),
            total_jcl_jobs=total_jcl_jobs,
            online_programs=online,
            batch_programs=batch,
            call_graph=call_graph,
            modules=modules,
            entry_points=entry_points,
            generated_date=generated_date,
        )
        (self.output_dir / "00-SYSTEM-OVERVIEW.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Layer 2: Linked Programs (Clusters)
    # ================================================================

    def _generate_linked_clusters(self, generated_date: str):
        console.print("  [cyan]Layer 2: Linked Programs (Clusters)[/cyan]")

        clusters = self.db.get_linked_clusters()

        # Generate individual cluster files
        cluster_template = self.env.get_template("cluster.md.j2")
        for cluster in clusters:
            if cluster["is_standalone"]:
                continue  # Don't generate individual files for standalone programs
            content = cluster_template.render(
                **cluster,
                generated_date=generated_date,
            )
            (self.output_dir / "clusters" / f"CLUSTER-{cluster['cluster_id']}.md").write_text(
                content, encoding="utf-8"
            )

        # Generate index
        index_template = self.env.get_template("clusters_index.md.j2")
        content = index_template.render(
            clusters=clusters,
            generated_date=generated_date,
        )
        (self.output_dir / "clusters" / "INDEX.md").write_text(content, encoding="utf-8")

        connected = [c for c in clusters if not c["is_standalone"]]
        standalone = [c for c in clusters if c["is_standalone"]]
        console.print(f"[green]OK - {len(connected)} connected clusters, "
                      f"{len(standalone)} standalone programs[/green]")

    # ================================================================
    # Layer 3: Module Documentation
    # ================================================================

    def _generate_module_docs(self, generated_date: str):
        console.print("  [cyan]Layer 2: Module Documentation[/cyan]")

        modules = self.db.get_all_modules()

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Modules...", total=len(modules))

            for mod in modules:
                details = self.db.get_module_details(mod["id"])
                if details:
                    template = self.env.get_template("module.md.j2")
                    content = template.render(
                        **details,
                        generated_date=generated_date,
                    )
                    fname = details["module_name"].replace(" ", "_").upper()
                    (self.output_dir / "modules" / f"{fname}.md").write_text(content, encoding="utf-8")

                progress.advance(task)

    # ================================================================
    # Layer 3: Program Walkthroughs
    # ================================================================

    def _generate_program_docs(self, generated_date: str):
        console.print("  [cyan]Layer 4: Program Walkthroughs (with dependencies + impact)[/cyan]")

        programs = self.db.get_all_programs()
        template = self.env.get_template("program.md.j2")

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Programs...", total=len(programs))

            for prog_summary in programs:
                pid = prog_summary["program_id"]
                details = self.db.get_program_details(pid)

                if details:
                    stmt_summary = self.db.get_statement_summary(pid)

                    # Fetch dependency context
                    deps = self.db.get_program_dependencies(pid)
                    shared = self.db.get_shared_data_context(pid)
                    impact = self.db.get_impact_analysis(pid)

                    # Parse JSON list field back to a Python list for the template
                    deps_raw = details.pop("dependencies_to_migrate_first", None) or "[]"
                    try:
                        deps_list = json.loads(deps_raw) if isinstance(deps_raw, str) else (deps_raw or [])
                    except Exception:
                        deps_list = []

                    jcl_jobs_for_prog = self.db.get_program_jcl_jobs(pid)
                    source_literals = []
                    source_statuses = []
                    source_path = Path(details.get("file_path") or "")
                    if source_path.exists():
                        try:
                            text = source_path.read_text(encoding="utf-8", errors="ignore")
                            body_lines = []
                            for raw_line in text.splitlines():
                                if len(raw_line) > 6 and raw_line[6] == "*":
                                    continue
                                body = raw_line[6:] if len(raw_line) > 6 else raw_line
                                body_lines.append(body[:66] if len(body) > 66 else body)
                            body = "\n".join(body_lines)
                            # Generic: extract any WS-*-NAME / PROGRAM-* / *-FILE / *-DSN
                            # literal value paired with its VALUE clause within the
                            # same period-terminated declaration. Forbidding '.'
                            # in the gap prevents one field's VALUE leaking onto
                            # another field's name.
                            for m in re.finditer(
                                r"\b(WS-[A-Z][A-Z0-9-]{0,28}|PGM[A-Z0-9-]{0,15}|[A-Z][A-Z0-9-]{0,28}-FILE-?(?:NAME)?|[A-Z][A-Z0-9-]{0,28}-DSN)\b"
                                r"[^.\n]{0,200}?\bVALUE\s+(?:IS\s+)?['\"]([^'\"]+)['\"]",
                                body, re.IGNORECASE | re.DOTALL,
                            ):
                                nm = m.group(1).upper()
                                val = m.group(2).strip()
                                if not any(s["name"] == nm for s in source_literals):
                                    source_literals.append({"name": nm, "value": val})
                                if len(source_literals) >= 16:
                                    break
                            # Generic: any *-STATUS reference inside an IF condition
                            for m in re.finditer(
                                r"\bIF\s+([A-Z][A-Z0-9-]*-STATUS)\s*("
                                r"=|<>|NOT\s*EQUAL|EQUAL|NOT\s*=|>|<|>=|<=)"
                                r"\s*([A-Z0-9'\"-]+)",
                                body, re.IGNORECASE,
                            ):
                                cond = f"{m.group(1)} {m.group(2).upper()} {m.group(3)}"
                                if cond not in source_statuses:
                                    source_statuses.append(cond)
                                if len(source_statuses) >= 12:
                                    break
                        except Exception:
                            pass

                    data_contracts_detail = self._build_data_contracts(details)
                    source_performs = self._extract_performs_from_source(details)
                    details["performs"] = self._merge_performs(details.get("performs", []), source_performs)
                    cics_workflow_notes = self._build_cics_workflow_notes(details, details.get("performs", []))
                    modernization_findings = self._build_modernization_findings(
                        details,
                        data_contracts_detail,
                        source_literals,
                    )

                    # Per-program copybook field dictionaries (from copybook_fields)
                    cb_dicts = []
                    for cb in (details.get("copybooks") or []):
                        cb_name = cb.get("copybook_name") if isinstance(cb, dict) else cb
                        if not cb_name:
                            continue
                        try:
                            fields = self.db.get_copybook_fields(cb_name)
                        except Exception:
                            fields = []
                        if fields:
                            cb_dicts.append({"copybook_name": cb_name, "fields": fields})

                    # FD record layouts for this program
                    try:
                        file_records = self.db.get_program_file_records(pid)
                    except Exception:
                        file_records = []

                    # Data lineage
                    try:
                        movements = self.db.get_program_data_movements(pid, limit=100)
                    except Exception:
                        movements = []

                    # Static-analysis anomalies (bugs, dead code, naming issues)
                    try:
                        anomalies = self.db.get_program_anomalies(pid)
                    except Exception:
                        anomalies = []

                    # New extractions: MQ, EVALUATE, CICS HANDLE, cursor lifecycles
                    try:    mq_calls = self.db.get_program_mq_calls(pid)
                    except Exception: mq_calls = []
                    try:    evaluate_branches = self.db.get_program_evaluates(pid)
                    except Exception: evaluate_branches = []
                    try:    cics_handles = self.db.get_program_cics_handles(pid)
                    except Exception: cics_handles = []
                    try:    cursor_lifecycles = self.db.get_program_cursor_lifecycles(pid)
                    except Exception: cursor_lifecycles = []
                    try:    program_parameters = self.db.get_program_parameters(pid)
                    except Exception: program_parameters = []
                    try:    file_operations = self.db.get_program_file_operations(pid)
                    except Exception: file_operations = []

                    content = template.render(
                        **details,
                        stmt_summary=stmt_summary,
                        dep_callers=deps["callers"],
                        dep_callees=deps["callees"],
                        shared_copybooks=shared["shared_copybooks"],
                        shared_files=shared["shared_files"],
                        impact=impact,
                        dependencies_to_migrate_first=deps_list,
                        jcl_jobs=jcl_jobs_for_prog,
                        source_literals=source_literals,
                        source_statuses=source_statuses,
                        data_contracts_detail=data_contracts_detail,
                        modernization_findings=modernization_findings,
                        copybook_dictionaries=cb_dicts,
                        file_records=file_records,
                        data_movements=movements,
                        code_anomalies=anomalies,
                        cics_workflow_notes=cics_workflow_notes,
                        mq_calls=mq_calls,
                        evaluate_branches=evaluate_branches,
                        cics_handles=cics_handles,
                        cursor_lifecycles=cursor_lifecycles,
                        program_parameters=program_parameters,
                        file_operations=file_operations,
                        generated_date=generated_date,
                    )
                    (self.output_dir / "programs" / f"{pid}.md").write_text(content, encoding="utf-8")

                progress.advance(task)

    # ================================================================
    # Layer 4: Business Rules Catalog
    # ================================================================

    def _generate_business_rules(self, generated_date: str):
        console.print("  [cyan]Layer 4: Business Rules Catalog[/cyan]")

        rules = self.db.get_all_business_rules()

        # Generate individual rule files
        if rules:
            rule_template = self.env.get_template("business_rule.md.j2")
            for rule in rules:
                content = rule_template.render(**rule, generated_date=generated_date)
                safe_id = (rule["rule_id"] or "UNKNOWN").replace("/", "_")
                (self.output_dir / "business-rules" / f"{safe_id}.md").write_text(content, encoding="utf-8")

        # Generate index
        rules_by_category = defaultdict(list)
        for rule in rules:
            cat = rule.get("category") or "GENERAL"
            rules_by_category[cat].append(rule)

        index_template = self.env.get_template("business_rules_index.md.j2")
        content = index_template.render(
            rules=rules,
            rules_by_category=dict(rules_by_category),
            categories=dict(rules_by_category),
            generated_date=generated_date,
        )
        (self.output_dir / "business-rules" / "INDEX.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Layer 5: Screen Catalog
    # ================================================================

    def _generate_screen_docs(self, generated_date: str):
        console.print("  [cyan]Layer 5: Screen Catalog[/cyan]")

        screens = self.db.get_all_screens()

        for screen_summary in screens:
            sid = screen_summary.get("id")
            details = self.db.get_screen_details(sid)
            if not details:
                continue

            fields = details.get("fields", [])

            # Separate field types
            input_fields = [f for f in fields if (f.get("field_type") or "").upper() == "INPUT"]
            output_fields = [f for f in fields if (f.get("field_type") or "").upper() == "OUTPUT"]
            label_fields = [f for f in fields if (f.get("field_type") or "").upper() == "LABEL"]

            # Group by row for visual mockup
            fields_by_row = defaultdict(list)
            max_row = 0
            for f in fields:
                row = f.get("row_position") or 0
                if row > 0:
                    fields_by_row[row].append(f)
                    max_row = max(max_row, row)

            template = self.env.get_template("screen.md.j2")
            content = template.render(
                **details,
                input_fields=input_fields,
                output_fields=output_fields,
                label_fields=label_fields,
                fields_by_row=dict(fields_by_row),
                max_row=max_row,
                generated_date=generated_date,
            )
            screen_name = details.get("screen_name") or f"SCREEN_{sid}"
            (self.output_dir / "screens" / f"{screen_name}.md").write_text(content, encoding="utf-8")

        # Index
        index_template = self.env.get_template("screens_index.md.j2")
        content = index_template.render(screens=screens, generated_date=generated_date)
        (self.output_dir / "screens" / "INDEX.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Call Graph
    # ================================================================

    def _generate_call_graph(self, generated_date: str):
        console.print("  [cyan]Diagram: Call Graph[/cyan]")

        calls = self.db.get_call_graph()
        programs = self.db.get_all_programs()

        called_set = set(c["called_program"] for c in calls)
        caller_set = set(c["caller_program"] for c in calls)
        all_set = set(p["program_id"] for p in programs)

        entry_points = sorted(all_set - called_set)
        leaf_programs = sorted(all_set - caller_set)

        template = self.env.get_template("call_graph.md.j2")
        content = template.render(
            system_name=self.system_name,
            calls=calls,
            entry_points=entry_points,
            leaf_programs=leaf_programs,
            generated_date=generated_date,
        )
        (self.output_dir / "diagrams" / "call-graph.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Data Dictionary
    # ================================================================

    def _generate_data_dictionary(self, generated_date: str):
        console.print("  [cyan]Reference: Data Dictionary[/cyan]")

        items = self.db.get_data_dictionary()
        programs = self.db.get_all_programs()

        # Group by section
        items_by_section = defaultdict(list)
        for item in items:
            section = item.get("section") or "OTHER"
            items_by_section[section].append(item)

        template = self.env.get_template("data_dictionary.md.j2")
        content = template.render(
            total_items=len(items),
            programs_count=len(programs),
            items_by_section=dict(items_by_section),
            generated_date=generated_date,
        )
        (self.output_dir / "data-dictionary.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Copybook Reference
    # ================================================================

    def _generate_copybook_reference(self, generated_date: str):
        console.print("  [cyan]Reference: Copybook Reference[/cyan]")

        copybooks = self.db.get_copybooks()

        template = self.env.get_template("copybook_reference.md.j2")
        content = template.render(
            copybooks=copybooks,
            generated_date=generated_date,
        )
        (self.output_dir / "copybook-reference.md").write_text(content, encoding="utf-8")

    # ================================================================
    # JCL Documentation
    # ================================================================

    def _generate_jcl_docs(self, generated_date: str):
        console.print("  [cyan]JCL: Job Catalog[/cyan]")

        jobs = self.db.get_all_jcl_jobs()
        if not jobs:
            console.print("  [yellow]  No JCL jobs in database — skipping JCL docs[/yellow]")
            return

        # Set of known COBOL program IDs for linking
        known_programs = {p["program_id"] for p in self.db.get_all_programs()}

        # Generate index
        idx_template = self.env.get_template("jcl_index.md.j2")
        idx_content = idx_template.render(jobs=jobs, generated_date=generated_date)
        (self.output_dir / "jcl" / "INDEX.md").write_text(idx_content, encoding="utf-8")

        # Generate one page per job
        job_template = self.env.get_template("jcl_job.md.j2")
        for job in jobs:
            details = self.db.get_jcl_job_details(job["job_name"])
            if not details:
                continue
            details["programs_called"] = [
                p for p in (details.get("programs_called") or [])
                if str(p).upper() in known_programs
            ]
            # Mark which step programs are known COBOL programs
            for step in details.get("steps") or []:
                step["program_is_cobol"] = (step.get("program") or "").upper() in known_programs
            content = job_template.render(**details, generated_date=generated_date)
            safe_name = details["job_name"].replace("/", "_")
            (self.output_dir / "jcl" / f"{safe_name}.md").write_text(content, encoding="utf-8")

        console.print(f"  [green]OK - Generated {len(jobs)} JCL job docs in docs/jcl/[/green]")

        # Also annotate program docs: which JCL jobs call them
        # (stored in program details page via get_program_jcl_jobs)


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    import argparse
    from sqlite_loader import SQLiteLoader

    parser = argparse.ArgumentParser(description="Generate Swimm-style COBOL documentation")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="Database path")
    parser.add_argument("--output", "-o", default="docs", help="Output directory")
    parser.add_argument("--templates", help="Custom templates directory")
    parser.add_argument("--repo", help="Source repository path")
    parser.add_argument("--name", default="CardDemo", help="System name")

    args = parser.parse_args()

    loader = SQLiteLoader(args.db)
    loader.connect()

    generator = DocGenerator(
        db_loader=loader,
        output_dir=args.output,
        templates_dir=args.templates,
        repo_path=args.repo,
        system_name=args.name,
    )
    generator.generate_all()

    loader.close()
