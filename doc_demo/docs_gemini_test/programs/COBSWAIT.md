# Program: COBSWAIT


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COBSWAIT` |
| Type | BATCH |
| Lines | 42 |
| Source | [COBSWAIT.cbl](../carddemo/COBSWAIT.cbl#L1) |
| Paragraphs | 0 |
| Statements | 0 |
| Impact Risk | **LOW** — 0 programs affected |

> **View Source:** [Open COBSWAIT.cbl](../carddemo/COBSWAIT.cbl#L1)


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **COBSWAIT** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COBSWAIT (Callers)

*No programs call COBSWAIT — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COBSWAIT (Callees)

*COBSWAIT does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

*No shared copybooks.*


## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.




*No concrete file or copybook record layouts were found for this program.*

---

## Dependency Graph

```mermaid
flowchart TD
    COBSWAIT["⬤ COBSWAIT"]:::target
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

> **If you change COBSWAIT, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 0 |
| **Total Impact** | **0** |
| **Risk Rating** | **LOW** |



---

## Statement Profile


## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
```

## Paragraphs


## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
| [WAITSTEP](../jcl/WAITSTEP.md) | `WAIT` | *****************************************************************
Copyright Amaz... |






## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
| `PARM-VALUE` | `MVSWAIT-TIME` | None | 37 |


## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEPENDENCY | Static CALL to external `MVSWAIT` (not in this codebase) | None | 38 |

### NOTICE — Static CALL to external `MVSWAIT` (not in this codebase)

`CALL 'MVSWAIT'` appears in the source but `MVSWAIT` is not a program in the loaded codebase. Custom MVS wait subroutine.
**Source excerpt** (line 38):
```cobol
CALL 'MVSWAIT'       USING MVSWAIT-TIME.
```

**Recommendation:** Document this external dependency in the Migration Notes — the modern equivalent must replicate its behaviour.
---










## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `MVSWAIT-TIME` | 1 | `9(8)` | WORKING-STORAGE | None |
| `PARM-VALUE` | 1 | `X(8)` | WORKING-STORAGE | None |

---

*Generated 2026-05-12 12:18*