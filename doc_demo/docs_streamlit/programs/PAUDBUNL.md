# Program: PAUDBUNL


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `PAUDBUNL` |
| Type | BATCH |
| Lines | 318 |
| Source | [PAUDBUNL.CBL](../carddemo\app/PAUDBUNL.CBL#L1) |
| Paragraphs | 11 |
| Statements | 38 |
| Impact Risk | **MEDIUM** — 7 programs affected |

> **View Source:** [Open PAUDBUNL.CBL](../carddemo\app/PAUDBUNL.CBL#L1)



## Dependency Context

> This section shows how **PAUDBUNL** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call PAUDBUNL (Callers)

*No programs call PAUDBUNL — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by PAUDBUNL (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| [UNKNOWN](UNKNOWN.md) | None | 351 |  |
| [UNKNOWN](UNKNOWN.md) | None | 395 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CIPAUDTY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, COPAUS2C (+2 more) | 7 |
| `CIPAUSMY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, DBUNLDGS (+1 more) | 6 |
| `IMSFUNCS` | DBUNLDGS, PAUDBLOD | 2 |
| `PAUTBPCB` | DBUNLDGS, PAUDBLOD | 2 |


---

## Dependency Graph

```mermaid
flowchart TD
    PAUDBUNL["⬤ PAUDBUNL"]:::target
    UNKNOWN["UNKNOWN"]:::callee
    UNKNOWN["UNKNOWN"]:::callee
    PAUDBUNL --> UNKNOWN
    PAUDBUNL --> UNKNOWN
    CB_CIPAUDTY{{"CIPAUDTY"}}:::copybook
    PAUDBUNL -.- CB_CIPAUDTY
    CBPAUP0C["CBPAUP0C"]:::coupled
    CB_CIPAUDTY -.- CBPAUP0C
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CIPAUDTY -.- COPAUA0C
    COPAUS0C["COPAUS0C"]:::coupled
    CB_CIPAUDTY -.- COPAUS0C
    CB_CIPAUSMY{{"CIPAUSMY"}}:::copybook
    PAUDBUNL -.- CB_CIPAUSMY
    CBPAUP0C["CBPAUP0C"]:::coupled
    CB_CIPAUSMY -.- CBPAUP0C
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CIPAUSMY -.- COPAUA0C
    COPAUS0C["COPAUS0C"]:::coupled
    CB_CIPAUSMY -.- COPAUS0C
    CB_IMSFUNCS{{"IMSFUNCS"}}:::copybook
    PAUDBUNL -.- CB_IMSFUNCS
    DBUNLDGS["DBUNLDGS"]:::coupled
    CB_IMSFUNCS -.- DBUNLDGS
    PAUDBLOD["PAUDBLOD"]:::coupled
    CB_IMSFUNCS -.- PAUDBLOD
    CB_PAUTBPCB{{"PAUTBPCB"}}:::copybook
    PAUDBUNL -.- CB_PAUTBPCB
    DBUNLDGS["DBUNLDGS"]:::coupled
    CB_PAUTBPCB -.- DBUNLDGS
    PAUDBLOD["PAUDBLOD"]:::coupled
    CB_PAUTBPCB -.- PAUDBLOD

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

> **If you change PAUDBUNL, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 7 |
| **Total Impact** | **7** |
| **Risk Rating** | **MEDIUM** |


**Programs affected via shared copybooks:**
- `CBPAUP0C`
- `COPAUA0C`
- `COPAUS0C`
- `COPAUS1C`
- `COPAUS2C`
- `DBUNLDGS`
- `PAUDBLOD`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| IF | 10 |
| DISPLAY | 6 |
| EXIT | 5 |
| PERFORM | 3 |
| OPEN | 2 |
| INITIALIZE | 2 |
| GOBACK | 2 |
| CLOSE | 2 |
| CALL | 2 |
| ACCEPT | 2 |
| MOVE | 1 |
| ENTRY | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN_PARA["MAIN-PARA"]
    1000_INITIALIZE["1000-INITIALIZE"]
    1000_EXIT["1000-EXIT"]
    2000_FIND_NEXT_AUTH_SUMMARY["2000-FIND-NEXT-AUTH-SUMMARY"]
    2000_EXIT["2000-EXIT"]
    3000_FIND_NEXT_AUTH_DTL["3000-FIND-NEXT-AUTH-DTL"]
    3000_EXIT["3000-EXIT"]
    4000_FILE_CLOSE["4000-FILE-CLOSE"]
    4000_EXIT["4000-EXIT"]
    9999_ABEND["9999-ABEND"]
    9999_EXIT["9999-EXIT"]
    START --> MAIN_PARA
    MAIN_PARA --> INLINE
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 295 - 308 |
| **View Code** | [Jump to Line 295](../carddemo\app/PAUDBUNL.CBL#L295) |



### 1000-INITIALIZE

| | |
|---|---|
| **Paragraph** | `1000-INITIALIZE` |
| **Lines** | 311 - 338 |
| **View Code** | [Jump to Line 311](../carddemo\app/PAUDBUNL.CBL#L311) |



### 1000-EXIT

| | |
|---|---|
| **Paragraph** | `1000-EXIT` |
| **Lines** | 341 - 342 |
| **View Code** | [Jump to Line 341](../carddemo\app/PAUDBUNL.CBL#L341) |



### 2000-FIND-NEXT-AUTH-SUMMARY

| | |
|---|---|
| **Paragraph** | `2000-FIND-NEXT-AUTH-SUMMARY` |
| **Lines** | 345 - 385 |
| **View Code** | [Jump to Line 345](../carddemo\app/PAUDBUNL.CBL#L345) |



### 2000-EXIT

| | |
|---|---|
| **Paragraph** | `2000-EXIT` |
| **Lines** | 386 - 387 |
| **View Code** | [Jump to Line 386](../carddemo\app/PAUDBUNL.CBL#L386) |



### 3000-FIND-NEXT-AUTH-DTL

| | |
|---|---|
| **Paragraph** | `3000-FIND-NEXT-AUTH-DTL` |
| **Lines** | 391 - 422 |
| **View Code** | [Jump to Line 391](../carddemo\app/PAUDBUNL.CBL#L391) |



### 3000-EXIT

| | |
|---|---|
| **Paragraph** | `3000-EXIT` |
| **Lines** | 423 - 424 |
| **View Code** | [Jump to Line 423](../carddemo\app/PAUDBUNL.CBL#L423) |



### 4000-FILE-CLOSE

| | |
|---|---|
| **Paragraph** | `4000-FILE-CLOSE` |
| **Lines** | 427 - 442 |
| **View Code** | [Jump to Line 427](../carddemo\app/PAUDBUNL.CBL#L427) |



### 4000-EXIT

| | |
|---|---|
| **Paragraph** | `4000-EXIT` |
| **Lines** | 443 - 444 |
| **View Code** | [Jump to Line 443](../carddemo\app/PAUDBUNL.CBL#L443) |



### 9999-ABEND

| | |
|---|---|
| **Paragraph** | `9999-ABEND` |
| **Lines** | 446 - 452 |
| **View Code** | [Jump to Line 446](../carddemo\app/PAUDBUNL.CBL#L446) |



### 9999-EXIT

| | |
|---|---|
| **Paragraph** | `9999-EXIT` |
| **Lines** | 454 - 455 |
| **View Code** | [Jump to Line 454](../carddemo\app/PAUDBUNL.CBL#L454) |





## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `WS-VARIABLES` | 1 | `None` | WORKING-STORAGE | None |
| `WS-PGMNAME` | 5 | `X(08)` | WORKING-STORAGE | None |
| `CURRENT-DATE` | 5 | `9(06)` | WORKING-STORAGE | None |
| `CURRENT-YYDDD` | 5 | `9(05)` | WORKING-STORAGE | None |
| `WS-AUTH-DATE` | 5 | `9(05)` | WORKING-STORAGE | None |
| `WS-EXPIRY-DAYS` | 5 | `S9(4)` | WORKING-STORAGE | None |
| `WS-DAY-DIFF` | 5 | `S9(4)` | WORKING-STORAGE | None |
| `IDX` | 5 | `S9(4)` | WORKING-STORAGE | None |
| `WS-CURR-APP-ID` | 5 | `9(11)` | WORKING-STORAGE | None |
| `WS-NO-CHKP` | 5 | `9(8)` | WORKING-STORAGE | None |
| `WS-AUTH-SMRY-PROC-CNT` | 5 | `9(8)` | WORKING-STORAGE | None |
| `WS-TOT-REC-WRITTEN` | 5 | `S9(8)` | WORKING-STORAGE | None |
| `WS-NO-SUMRY-READ` | 5 | `S9(8)` | WORKING-STORAGE | None |
| `WS-NO-SUMRY-DELETED` | 5 | `S9(8)` | WORKING-STORAGE | None |
| `WS-NO-DTL-READ` | 5 | `S9(8)` | WORKING-STORAGE | None |
| `WS-NO-DTL-DELETED` | 5 | `S9(8)` | WORKING-STORAGE | None |
| `WS-ERR-FLG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `ERR-FLG-ON` | 88 | `None` | WORKING-STORAGE | None |
| `ERR-FLG-OFF` | 88 | `None` | WORKING-STORAGE | None |
| `WS-END-OF-AUTHDB-FLAG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `END-OF-AUTHDB` | 88 | `None` | WORKING-STORAGE | None |
| `NOT-END-OF-AUTHDB` | 88 | `None` | WORKING-STORAGE | None |
| `WS-MORE-AUTHS-FLAG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `MORE-AUTHS` | 88 | `None` | WORKING-STORAGE | None |
| `NO-MORE-AUTHS` | 88 | `None` | WORKING-STORAGE | None |
| `WS-END-OF-ROOT-SEG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `WS-END-OF-CHILD-SEG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `WS-INFILE-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-OUTFL1-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-OUTFL2-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-CUSTID-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `END-OF-FILE` | 88 | `None` | WORKING-STORAGE | None |
| `WK-CHKPT-ID` | 5 | `None` | WORKING-STORAGE | None |
| `FILLER` | 10 | `X(04)` | WORKING-STORAGE | None |
| `WK-CHKPT-ID-CTR` | 10 | `9(04)` | WORKING-STORAGE | None |
| `WS-IMS-VARIABLES` | 1 | `None` | WORKING-STORAGE | None |
| `IMS-RETURN-CODE` | 5 | `X(02)` | WORKING-STORAGE | None |
| `STATUS-OK` | 88 | `None` | WORKING-STORAGE | None |
| `SEGMENT-NOT-FOUND` | 88 | `None` | WORKING-STORAGE | None |
| `DUPLICATE-SEGMENT-FOUND` | 88 | `None` | WORKING-STORAGE | None |

*Showing 40 of 138 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-03-16 19:39*