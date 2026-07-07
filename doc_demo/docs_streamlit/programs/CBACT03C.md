# Program: CBACT03C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `CBACT03C` |
| Type | BATCH |
| Lines | 179 |
| Source | [CBACT03C.cbl](../carddemo\app/CBACT03C.cbl#L1) |
| Paragraphs | 5 |
| Statements | 20 |
| Impact Risk | **HIGH** — 13 programs affected |

> **View Source:** [Open CBACT03C.cbl](../carddemo\app/CBACT03C.cbl#L1)



## Dependency Context

> This section shows how **CBACT03C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call CBACT03C (Callers)

*No programs call CBACT03C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by CBACT03C (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| [UNKNOWN](UNKNOWN.md) | None | 169 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CVACT03Y` | CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C (+8 more) | 13 |


---

## Dependency Graph

```mermaid
flowchart TD
    CBACT03C["⬤ CBACT03C"]:::target
    UNKNOWN["UNKNOWN"]:::callee
    CBACT03C --> UNKNOWN
    CB_CVACT03Y{{"CVACT03Y"}}:::copybook
    CBACT03C -.- CB_CVACT03Y
    CBACT04C["CBACT04C"]:::coupled
    CB_CVACT03Y -.- CBACT04C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT03Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVACT03Y -.- CBIMPORT

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

> **If you change CBACT03C, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 13 |
| **Total Impact** | **13** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `CBACT04C`
- `CBEXPORT`
- `CBIMPORT`
- `CBSTM03A`
- `CBTRN01C`
- `CBTRN02C`
- `CBTRN03C`
- `COACTUPC`
- `COACTVWC`
- `COBIL00C`
- `COPAUA0C`
- `COPAUS0C`
- `COTRN02C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| IF | 7 |
| EXIT | 4 |
| MOVE | 3 |
| READ | 1 |
| OPEN | 1 |
| DISPLAY | 1 |
| CLOSE | 1 |
| CALL | 1 |
| ARITHMETIC | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    1000_XREFFILE_GET_NEXT["1000-XREFFILE-GET-NEXT"]
    0000_XREFFILE_OPEN["0000-XREFFILE-OPEN"]
    9000_XREFFILE_CLOSE["9000-XREFFILE-CLOSE"]
    9999_ABEND_PROGRAM["9999-ABEND-PROGRAM"]
    9910_DISPLAY_IO_STATUS["9910-DISPLAY-IO-STATUS"]
    START --> 1000_XREFFILE_GET_NEXT
```

## Paragraphs

### 1000-XREFFILE-GET-NEXT

| | |
|---|---|
| **Paragraph** | `1000-XREFFILE-GET-NEXT` |
| **Lines** | 103 - 127 |
| **View Code** | [Jump to Line 103](../carddemo\app/CBACT03C.cbl#L103) |



### 0000-XREFFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0000-XREFFILE-OPEN` |
| **Lines** | 129 - 145 |
| **View Code** | [Jump to Line 129](../carddemo\app/CBACT03C.cbl#L129) |



### 9000-XREFFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9000-XREFFILE-CLOSE` |
| **Lines** | 147 - 163 |
| **View Code** | [Jump to Line 147](../carddemo\app/CBACT03C.cbl#L147) |



### 9999-ABEND-PROGRAM

| | |
|---|---|
| **Paragraph** | `9999-ABEND-PROGRAM` |
| **Lines** | 165 - 169 |
| **View Code** | [Jump to Line 165](../carddemo\app/CBACT03C.cbl#L165) |



### 9910-DISPLAY-IO-STATUS

| | |
|---|---|
| **Paragraph** | `9910-DISPLAY-IO-STATUS` |
| **Lines** | 172 - 185 |
| **View Code** | [Jump to Line 172](../carddemo\app/CBACT03C.cbl#L172) |




## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
| [READXREF](../jcl/READXREF.md) | `STEP05` | *****************************************************************
Copyright Amaz... |


## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `CARD-XREF-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `XREF-CARD-NUM` | 5 | `X(16)` | WORKING-STORAGE | None |
| `XREF-CUST-ID` | 5 | `9(09)` | WORKING-STORAGE | None |
| `XREF-ACCT-ID` | 5 | `9(11)` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(14)` | WORKING-STORAGE | None |
| `XREFFILE-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `XREFFILE-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `XREFFILE-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `IO-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `IO-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `IO-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `TWO-BYTES-BINARY` | 1 | `9(4)` | WORKING-STORAGE | None |
| `TWO-BYTES-ALPHA` | 1 | `None` | WORKING-STORAGE | None |
| `TWO-BYTES-LEFT` | 5 | `X` | WORKING-STORAGE | None |
| `TWO-BYTES-RIGHT` | 5 | `X` | WORKING-STORAGE | None |
| `IO-STATUS-04` | 1 | `None` | WORKING-STORAGE | None |
| `IO-STATUS-0401` | 5 | `9` | WORKING-STORAGE | None |
| `IO-STATUS-0403` | 5 | `999` | WORKING-STORAGE | None |
| `APPL-RESULT` | 1 | `S9(9)` | WORKING-STORAGE | None |
| `APPL-AOK` | 88 | `None` | WORKING-STORAGE | None |
| `APPL-EOF` | 88 | `None` | WORKING-STORAGE | None |
| `END-OF-FILE` | 1 | `X(01)` | WORKING-STORAGE | None |
| `ABCODE` | 1 | `S9(9)` | WORKING-STORAGE | None |
| `TIMING` | 1 | `S9(9)` | WORKING-STORAGE | None |

---

*Generated 2026-03-16 19:39*