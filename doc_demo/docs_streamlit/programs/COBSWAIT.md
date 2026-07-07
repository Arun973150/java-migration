# Program: COBSWAIT


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COBSWAIT` |
| Type | BATCH |
| Lines | 42 |
| Source | [COBSWAIT.cbl](../carddemo\app/COBSWAIT.cbl#L1) |
| Paragraphs | 0 |
| Statements | 0 |
| Impact Risk | **LOW** — 0 programs affected |

> **View Source:** [Open COBSWAIT.cbl](../carddemo\app/COBSWAIT.cbl#L1)



## Dependency Context

> This section shows how **COBSWAIT** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COBSWAIT (Callers)

*No programs call COBSWAIT — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COBSWAIT (Callees)

*COBSWAIT does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

*No shared copybooks.*


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


## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `MVSWAIT-TIME` | 1 | `9(8)` | WORKING-STORAGE | None |
| `PARM-VALUE` | 1 | `X(8)` | WORKING-STORAGE | None |

---

*Generated 2026-03-16 19:39*