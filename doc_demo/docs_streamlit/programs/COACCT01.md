# Program: COACCT01


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COACCT01` |
| Type | ONLINE |
| Lines | 621 |
| Source | [COACCT01.cbl](../carddemo\app/COACCT01.cbl#L1) |
| Paragraphs | 0 |
| Statements | 0 |
| Impact Risk | **HIGH** — 14 programs affected |

> **View Source:** [Open COACCT01.cbl](../carddemo\app/COACCT01.cbl#L1)



## Dependency Context

> This section shows how **COACCT01** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COACCT01 (Callers)

*No programs call COACCT01 — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COACCT01 (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| [MQCLOSE](MQCLOSE.md) | None | 557 |  |
| [MQCLOSE](MQCLOSE.md) | None | 579 |  |
| [MQCLOSE](MQCLOSE.md) | None | 602 |  |
| [MQGET](MQGET.md) | None | 352 |  |
| [MQOPEN](MQOPEN.md) | None | 233 |  |
| [MQOPEN](MQOPEN.md) | None | 267 |  |
| [MQOPEN](MQOPEN.md) | None | 302 |  |
| [MQPUT](MQPUT.md) | None | 479 |  |
| [MQPUT](MQPUT.md) | None | 516 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `03500000` |  | 0 |
| `CMQGMOV` | CODATE01, COPAUA0C | 2 |
| `CMQMDV` | CODATE01, COPAUA0C | 2 |
| `CMQODV` | CODATE01, COPAUA0C | 2 |
| `CMQPMOV` | CODATE01, COPAUA0C | 2 |
| `CMQTML` | CODATE01, COPAUA0C | 2 |
| `CMQV` | CODATE01, COPAUA0C | 2 |
| `CVACT01Y` | CBACT01C, CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A (+8 more) | 13 |
| `REPLACING` | CODATE01 | 1 |


---

## Dependency Graph

```mermaid
flowchart TD
    COACCT01["⬤ COACCT01"]:::target
    MQCLOSE["MQCLOSE"]:::callee
    MQCLOSE["MQCLOSE"]:::callee
    MQCLOSE["MQCLOSE"]:::callee
    MQGET["MQGET"]:::callee
    MQOPEN["MQOPEN"]:::callee
    MQOPEN["MQOPEN"]:::callee
    MQOPEN["MQOPEN"]:::callee
    MQPUT["MQPUT"]:::callee
    MQPUT["MQPUT"]:::callee
    COACCT01 --> MQCLOSE
    COACCT01 --> MQCLOSE
    COACCT01 --> MQCLOSE
    COACCT01 --> MQGET
    COACCT01 --> MQOPEN
    COACCT01 --> MQOPEN
    COACCT01 --> MQOPEN
    COACCT01 --> MQPUT
    COACCT01 --> MQPUT
    CB_CMQGMOV{{"CMQGMOV"}}:::copybook
    COACCT01 -.- CB_CMQGMOV
    CODATE01["CODATE01"]:::coupled
    CB_CMQGMOV -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQGMOV -.- COPAUA0C
    CB_CMQMDV{{"CMQMDV"}}:::copybook
    COACCT01 -.- CB_CMQMDV
    CODATE01["CODATE01"]:::coupled
    CB_CMQMDV -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQMDV -.- COPAUA0C
    CB_CMQODV{{"CMQODV"}}:::copybook
    COACCT01 -.- CB_CMQODV
    CODATE01["CODATE01"]:::coupled
    CB_CMQODV -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQODV -.- COPAUA0C
    CB_CMQPMOV{{"CMQPMOV"}}:::copybook
    COACCT01 -.- CB_CMQPMOV
    CODATE01["CODATE01"]:::coupled
    CB_CMQPMOV -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQPMOV -.- COPAUA0C
    CB_CMQTML{{"CMQTML"}}:::copybook
    COACCT01 -.- CB_CMQTML
    CODATE01["CODATE01"]:::coupled
    CB_CMQTML -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQTML -.- COPAUA0C
    CB_CMQV{{"CMQV"}}:::copybook
    COACCT01 -.- CB_CMQV
    CODATE01["CODATE01"]:::coupled
    CB_CMQV -.- CODATE01
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CMQV -.- COPAUA0C
    CB_CVACT01Y{{"CVACT01Y"}}:::copybook
    COACCT01 -.- CB_CVACT01Y
    CBACT01C["CBACT01C"]:::coupled
    CB_CVACT01Y -.- CBACT01C
    CBACT04C["CBACT04C"]:::coupled
    CB_CVACT01Y -.- CBACT04C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT01Y -.- CBEXPORT

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

> **If you change COACCT01, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 14 |
| **Total Impact** | **14** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `CBACT01C`
- `CBACT04C`
- `CBEXPORT`
- `CBIMPORT`
- `CBSTM03A`
- `CBTRN01C`
- `CBTRN02C`
- `COACTUPC`
- `COACTVWC`
- `COBIL00C`
- `CODATE01`
- `COPAUA0C`
- `COPAUS0C`
- `COTRN02C`

---

## Statement Profile


## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN --> 2100_OPEN_ERROR_QUEUE
    MAIN --> 9000_ERROR
    MAIN --> 8000_TERMINATION
    MAIN --> 2300_OPEN_INPUT_QUEUE
    MAIN --> 2400_OPEN_OUTPUT_QUEUE
    MAIN --> 3000_GET_REQUEST
    MAIN --> 4000_MAIN_PROCESS
    MAIN --> 4000_PROCESS_REQUEST_REPLY
    MAIN --> 4100_PUT_REPLY
```

## Paragraphs



## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

*No data items found for this program.*

---

*Generated 2026-03-16 19:39*