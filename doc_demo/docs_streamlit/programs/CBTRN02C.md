# Program: CBTRN02C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `CBTRN02C` |
| Type | BATCH |
| Lines | 732 |
| Source | [CBTRN02C.cbl](../carddemo\app/CBTRN02C.cbl#L1) |
| Paragraphs | 26 |
| Statements | 146 |
| Impact Risk | **HIGH** — 18 programs affected |

> **View Source:** [Open CBTRN02C.cbl](../carddemo\app/CBTRN02C.cbl#L1)



## Dependency Context

> This section shows how **CBTRN02C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call CBTRN02C (Callers)

*No programs call CBTRN02C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by CBTRN02C (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| [UNKNOWN](UNKNOWN.md) | None | 797 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CVACT01Y` | CBACT01C, CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A (+8 more) | 13 |
| `CVACT03Y` | CBACT03C, CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A (+8 more) | 13 |
| `CVTRA01Y` | CBACT04C | 1 |
| `CVTRA05Y` | CBACT04C, CBEXPORT, CBIMPORT, CBTRN01C, CBTRN03C (+5 more) | 10 |
| `CVTRA06Y` | CBTRN01C | 1 |


---

## Dependency Graph

```mermaid
flowchart TD
    CBTRN02C["⬤ CBTRN02C"]:::target
    UNKNOWN["UNKNOWN"]:::callee
    CBTRN02C --> UNKNOWN
    CB_CVACT01Y{{"CVACT01Y"}}:::copybook
    CBTRN02C -.- CB_CVACT01Y
    CBACT01C["CBACT01C"]:::coupled
    CB_CVACT01Y -.- CBACT01C
    CBACT04C["CBACT04C"]:::coupled
    CB_CVACT01Y -.- CBACT04C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT01Y -.- CBEXPORT
    CB_CVACT03Y{{"CVACT03Y"}}:::copybook
    CBTRN02C -.- CB_CVACT03Y
    CBACT03C["CBACT03C"]:::coupled
    CB_CVACT03Y -.- CBACT03C
    CBACT04C["CBACT04C"]:::coupled
    CB_CVACT03Y -.- CBACT04C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT03Y -.- CBEXPORT
    CB_CVTRA01Y{{"CVTRA01Y"}}:::copybook
    CBTRN02C -.- CB_CVTRA01Y
    CBACT04C["CBACT04C"]:::coupled
    CB_CVTRA01Y -.- CBACT04C
    CB_CVTRA05Y{{"CVTRA05Y"}}:::copybook
    CBTRN02C -.- CB_CVTRA05Y
    CBACT04C["CBACT04C"]:::coupled
    CB_CVTRA05Y -.- CBACT04C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVTRA05Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVTRA05Y -.- CBIMPORT
    CB_CVTRA06Y{{"CVTRA06Y"}}:::copybook
    CBTRN02C -.- CB_CVTRA06Y
    CBTRN01C["CBTRN01C"]:::coupled
    CB_CVTRA06Y -.- CBTRN01C

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

> **If you change CBTRN02C, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 18 |
| **Total Impact** | **18** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `CBACT01C`
- `CBACT03C`
- `CBACT04C`
- `CBEXPORT`
- `CBIMPORT`
- `CBSTM03A`
- `CBTRN01C`
- `CBTRN03C`
- `COACCT01`
- `COACTUPC`
- `COACTVWC`
- `COBIL00C`
- `COPAUA0C`
- `COPAUS0C`
- `CORPT00C`
- `COTRN00C`
- `COTRN01C`
- `COTRN02C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| MOVE | 51 |
| IF | 40 |
| EXIT | 23 |
| OPEN | 6 |
| CLOSE | 6 |
| PERFORM | 5 |
| READ | 4 |
| WRITE | 3 |
| ARITHMETIC | 3 |
| REWRITE | 2 |
| INITIALIZE | 1 |
| DISPLAY | 1 |
| CALL | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    0000_DALYTRAN_OPEN["0000-DALYTRAN-OPEN"]
    0100_TRANFILE_OPEN["0100-TRANFILE-OPEN"]
    0200_XREFFILE_OPEN["0200-XREFFILE-OPEN"]
    0300_DALYREJS_OPEN["0300-DALYREJS-OPEN"]
    0400_ACCTFILE_OPEN["0400-ACCTFILE-OPEN"]
    0500_TCATBALF_OPEN["0500-TCATBALF-OPEN"]
    1000_DALYTRAN_GET_NEXT["1000-DALYTRAN-GET-NEXT"]
    1500_VALIDATE_TRAN["1500-VALIDATE-TRAN"]
    1500_A_LOOKUP_XREF["1500-A-LOOKUP-XREF"]
    1500_B_LOOKUP_ACCT["1500-B-LOOKUP-ACCT"]
    2000_POST_TRANSACTION["2000-POST-TRANSACTION"]
    2500_WRITE_REJECT_REC["2500-WRITE-REJECT-REC"]
    2700_UPDATE_TCATBAL["2700-UPDATE-TCATBAL"]
    2700_A_CREATE_TCATBAL_REC["2700-A-CREATE-TCATBAL-REC"]
    2700_B_UPDATE_TCATBAL_REC["2700-B-UPDATE-TCATBAL-REC"]
    START --> 0000_DALYTRAN_OPEN
    1500_VALIDATE_TRAN --> INLINE
    2000_POST_TRANSACTION --> INLINE
```

## Paragraphs

### 0000-DALYTRAN-OPEN

| | |
|---|---|
| **Paragraph** | `0000-DALYTRAN-OPEN` |
| **Lines** | 322 - 338 |
| **View Code** | [Jump to Line 322](../carddemo\app/CBTRN02C.cbl#L322) |



### 0100-TRANFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0100-TRANFILE-OPEN` |
| **Lines** | 340 - 356 |
| **View Code** | [Jump to Line 340](../carddemo\app/CBTRN02C.cbl#L340) |



### 0200-XREFFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0200-XREFFILE-OPEN` |
| **Lines** | 359 - 375 |
| **View Code** | [Jump to Line 359](../carddemo\app/CBTRN02C.cbl#L359) |



### 0300-DALYREJS-OPEN

| | |
|---|---|
| **Paragraph** | `0300-DALYREJS-OPEN` |
| **Lines** | 377 - 393 |
| **View Code** | [Jump to Line 377](../carddemo\app/CBTRN02C.cbl#L377) |



### 0400-ACCTFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0400-ACCTFILE-OPEN` |
| **Lines** | 395 - 411 |
| **View Code** | [Jump to Line 395](../carddemo\app/CBTRN02C.cbl#L395) |



### 0500-TCATBALF-OPEN

| | |
|---|---|
| **Paragraph** | `0500-TCATBALF-OPEN` |
| **Lines** | 413 - 429 |
| **View Code** | [Jump to Line 413](../carddemo\app/CBTRN02C.cbl#L413) |



### 1000-DALYTRAN-GET-NEXT

| | |
|---|---|
| **Paragraph** | `1000-DALYTRAN-GET-NEXT` |
| **Lines** | 431 - 455 |
| **View Code** | [Jump to Line 431](../carddemo\app/CBTRN02C.cbl#L431) |



### 1500-VALIDATE-TRAN

| | |
|---|---|
| **Paragraph** | `1500-VALIDATE-TRAN` |
| **Lines** | 456 - 464 |
| **View Code** | [Jump to Line 456](../carddemo\app/CBTRN02C.cbl#L456) |



### 1500-A-LOOKUP-XREF

| | |
|---|---|
| **Paragraph** | `1500-A-LOOKUP-XREF` |
| **Lines** | 466 - 478 |
| **View Code** | [Jump to Line 466](../carddemo\app/CBTRN02C.cbl#L466) |



### 1500-B-LOOKUP-ACCT

| | |
|---|---|
| **Paragraph** | `1500-B-LOOKUP-ACCT` |
| **Lines** | 479 - 508 |
| **View Code** | [Jump to Line 479](../carddemo\app/CBTRN02C.cbl#L479) |



### 2000-POST-TRANSACTION

| | |
|---|---|
| **Paragraph** | `2000-POST-TRANSACTION` |
| **Lines** | 510 - 530 |
| **View Code** | [Jump to Line 510](../carddemo\app/CBTRN02C.cbl#L510) |



### 2500-WRITE-REJECT-REC

| | |
|---|---|
| **Paragraph** | `2500-WRITE-REJECT-REC` |
| **Lines** | 532 - 551 |
| **View Code** | [Jump to Line 532](../carddemo\app/CBTRN02C.cbl#L532) |



### 2700-UPDATE-TCATBAL

| | |
|---|---|
| **Paragraph** | `2700-UPDATE-TCATBAL` |
| **Lines** | 553 - 587 |
| **View Code** | [Jump to Line 553](../carddemo\app/CBTRN02C.cbl#L553) |



### 2700-A-CREATE-TCATBAL-REC

| | |
|---|---|
| **Paragraph** | `2700-A-CREATE-TCATBAL-REC` |
| **Lines** | 589 - 610 |
| **View Code** | [Jump to Line 589](../carddemo\app/CBTRN02C.cbl#L589) |



### 2700-B-UPDATE-TCATBAL-REC

| | |
|---|---|
| **Paragraph** | `2700-B-UPDATE-TCATBAL-REC` |
| **Lines** | 612 - 628 |
| **View Code** | [Jump to Line 612](../carddemo\app/CBTRN02C.cbl#L612) |



### 2800-UPDATE-ACCOUNT-REC

| | |
|---|---|
| **Paragraph** | `2800-UPDATE-ACCOUNT-REC` |
| **Lines** | 631 - 646 |
| **View Code** | [Jump to Line 631](../carddemo\app/CBTRN02C.cbl#L631) |



### 2900-WRITE-TRANSACTION-FILE

| | |
|---|---|
| **Paragraph** | `2900-WRITE-TRANSACTION-FILE` |
| **Lines** | 648 - 665 |
| **View Code** | [Jump to Line 648](../carddemo\app/CBTRN02C.cbl#L648) |



### 9000-DALYTRAN-CLOSE

| | |
|---|---|
| **Paragraph** | `9000-DALYTRAN-CLOSE` |
| **Lines** | 668 - 684 |
| **View Code** | [Jump to Line 668](../carddemo\app/CBTRN02C.cbl#L668) |



### 9100-TRANFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9100-TRANFILE-CLOSE` |
| **Lines** | 686 - 702 |
| **View Code** | [Jump to Line 686](../carddemo\app/CBTRN02C.cbl#L686) |



### 9200-XREFFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9200-XREFFILE-CLOSE` |
| **Lines** | 705 - 721 |
| **View Code** | [Jump to Line 705](../carddemo\app/CBTRN02C.cbl#L705) |



### 9300-DALYREJS-CLOSE

| | |
|---|---|
| **Paragraph** | `9300-DALYREJS-CLOSE` |
| **Lines** | 723 - 739 |
| **View Code** | [Jump to Line 723](../carddemo\app/CBTRN02C.cbl#L723) |



### 9400-ACCTFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9400-ACCTFILE-CLOSE` |
| **Lines** | 741 - 757 |
| **View Code** | [Jump to Line 741](../carddemo\app/CBTRN02C.cbl#L741) |



### 9500-TCATBALF-CLOSE

| | |
|---|---|
| **Paragraph** | `9500-TCATBALF-CLOSE` |
| **Lines** | 760 - 776 |
| **View Code** | [Jump to Line 760](../carddemo\app/CBTRN02C.cbl#L760) |



### Z-GET-DB2-FORMAT-TIMESTAMP

| | |
|---|---|
| **Paragraph** | `Z-GET-DB2-FORMAT-TIMESTAMP` |
| **Lines** | 778 - 791 |
| **View Code** | [Jump to Line 778](../carddemo\app/CBTRN02C.cbl#L778) |



### 9999-ABEND-PROGRAM

| | |
|---|---|
| **Paragraph** | `9999-ABEND-PROGRAM` |
| **Lines** | 793 - 797 |
| **View Code** | [Jump to Line 793](../carddemo\app/CBTRN02C.cbl#L793) |



### 9910-DISPLAY-IO-STATUS

| | |
|---|---|
| **Paragraph** | `9910-DISPLAY-IO-STATUS` |
| **Lines** | 800 - 813 |
| **View Code** | [Jump to Line 800](../carddemo\app/CBTRN02C.cbl#L800) |




## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
| [POSTTRAN](../jcl/POSTTRAN.md) | `STEP15` | *****************************************************************
Copyright Amaz... |


## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `DALYTRAN-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `DALYTRAN-ID` | 5 | `X(16)` | WORKING-STORAGE | None |
| `DALYTRAN-TYPE-CD` | 5 | `X(02)` | WORKING-STORAGE | None |
| `DALYTRAN-CAT-CD` | 5 | `9(04)` | WORKING-STORAGE | None |
| `DALYTRAN-SOURCE` | 5 | `X(10)` | WORKING-STORAGE | None |
| `DALYTRAN-DESC` | 5 | `X(100)` | WORKING-STORAGE | None |
| `DALYTRAN-AMT` | 5 | `S9(09)V99` | WORKING-STORAGE | None |
| `DALYTRAN-MERCHANT-ID` | 5 | `9(09)` | WORKING-STORAGE | None |
| `DALYTRAN-MERCHANT-NAME` | 5 | `X(50)` | WORKING-STORAGE | None |
| `DALYTRAN-MERCHANT-CITY` | 5 | `X(50)` | WORKING-STORAGE | None |
| `DALYTRAN-MERCHANT-ZIP` | 5 | `X(10)` | WORKING-STORAGE | None |
| `DALYTRAN-CARD-NUM` | 5 | `X(16)` | WORKING-STORAGE | None |
| `DALYTRAN-ORIG-TS` | 5 | `X(26)` | WORKING-STORAGE | None |
| `DALYTRAN-PROC-TS` | 5 | `X(26)` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(20)` | WORKING-STORAGE | None |
| `DALYTRAN-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `DALYTRAN-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `DALYTRAN-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `TRAN-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `TRAN-ID` | 5 | `X(16)` | WORKING-STORAGE | None |
| `TRAN-TYPE-CD` | 5 | `X(02)` | WORKING-STORAGE | None |
| `TRAN-CAT-CD` | 5 | `9(04)` | WORKING-STORAGE | None |
| `TRAN-SOURCE` | 5 | `X(10)` | WORKING-STORAGE | None |
| `TRAN-DESC` | 5 | `X(100)` | WORKING-STORAGE | None |
| `TRAN-AMT` | 5 | `S9(09)V99` | WORKING-STORAGE | None |
| `TRAN-MERCHANT-ID` | 5 | `9(09)` | WORKING-STORAGE | None |
| `TRAN-MERCHANT-NAME` | 5 | `X(50)` | WORKING-STORAGE | None |
| `TRAN-MERCHANT-CITY` | 5 | `X(50)` | WORKING-STORAGE | None |
| `TRAN-MERCHANT-ZIP` | 5 | `X(10)` | WORKING-STORAGE | None |
| `TRAN-CARD-NUM` | 5 | `X(16)` | WORKING-STORAGE | None |
| `TRAN-ORIG-TS` | 5 | `X(26)` | WORKING-STORAGE | None |
| `TRAN-PROC-TS` | 5 | `X(26)` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(20)` | WORKING-STORAGE | None |
| `TRANFILE-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `TRANFILE-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `TRANFILE-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `CARD-XREF-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `XREF-CARD-NUM` | 5 | `X(16)` | WORKING-STORAGE | None |
| `XREF-CUST-ID` | 5 | `9(09)` | WORKING-STORAGE | None |
| `XREF-ACCT-ID` | 5 | `9(11)` | WORKING-STORAGE | None |

*Showing 40 of 127 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-03-16 19:39*