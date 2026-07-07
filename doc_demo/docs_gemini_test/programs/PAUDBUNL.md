# Program: PAUDBUNL


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `PAUDBUNL` |
| Type | BATCH |
| Lines | 318 |
| Source | [PAUDBUNL.CBL](../carddemo/PAUDBUNL.CBL#L1) |
| Paragraphs | 11 |
| Statements | 55 |
| Impact Risk | **MEDIUM** — 7 programs affected |

> **View Source:** [Open PAUDBUNL.CBL](../carddemo/PAUDBUNL.CBL#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-PGMNAME` | `IMSUNLOD` |
| `WS-ERR-FLG` | `N` |
| `WS-END-OF-AUTHDB-FLAG` | `N` |
| `WS-MORE-AUTHS-FLAG` | `N` |
| `END-OF-FILE` | `10` |

Status conditions found in source:
- `WS-OUTFL1-STATUS = SPACES`
- `WS-OUTFL2-STATUS = SPACES`
- `PAUT-PCB-STATUS = SPACES`
- `PAUT-PCB-STATUS = 'GB'`
- `PAUT-PCB-STATUS NOT EQUAL TO`
- `PAUT-PCB-STATUS = 'GE'`


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **PAUDBUNL** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call PAUDBUNL (Callers)

*No programs call PAUDBUNL — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by PAUDBUNL (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| `UNKNOWN` | None | 351 |  |
| `UNKNOWN` | None | 395 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CIPAUDTY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, COPAUS2C (+2 more) | 7 |
| `CIPAUSMY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, DBUNLDGS (+1 more) | 6 |
| `IMSFUNCS` | DBUNLDGS, PAUDBLOD | 2 |
| `PAUTBPCB` | DBUNLDGS, PAUDBLOD | 2 |

#### Shared Files

| File | Type | Access | Also Used By |
|------|------|--------|-------------|
| `OPFILE1` | SEQUENTIAL | SEQUENTIAL |  |
| `OPFILE2` | SEQUENTIAL | SEQUENTIAL |  |

## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.

### File Record Layouts

#### `OPFILE1` / `OPFIL1-REC`
| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
| `OPFIL1-REC` | Opfil1 Record | `PIC X(100)` | `STRING(100)` |  |

#### `OPFILE2` / `OPFIL2-REC`
| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
| `OPFIL2-REC` | Opfil2 Record | `GROUP` | `OBJECT` |  |
| `ROOT-SEG-KEY` | Root Segment Key | `PIC S9(11) COMP-3` | `BIGINT` |  |
| `CHILD-SEG-REC` | Child Segment Record | `PIC X(200)` | `STRING(200)` |  |


### Copybook Segment Layouts

#### `CIPAUDTY` as `PENDING-AUTH-DETAILS`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `PA-AUTHORIZATION-KEY` | Authorization Key | `GROUP` | `OBJECT` |  |
| `PA-AUTH-DATE-9C` | Authorization Date | `PIC S9(05) COMP-3` | `INTEGER` | Date-like field; verify YYDDD, YYMMDD, or ISO format before migration. |
| `PA-AUTH-TIME-9C` | Authorization Time | `PIC S9(09) COMP-3` | `INTEGER` |  |
| `PA-AUTH-ORIG-DATE` | Authorization Orig Date | `PIC X(06)` | `STRING(6)` |  |
| `PA-AUTH-ORIG-TIME` | Authorization Orig Time | `PIC X(06)` | `STRING(6)` |  |
| `PA-CARD-NUM` | Card Number | `PIC X(16)` | `STRING(16)` |  |
| `PA-AUTH-TYPE` | Authorization Type | `PIC X(04)` | `STRING(4)` |  |
| `PA-CARD-EXPIRY-DATE` | Card Expiry Date | `PIC X(04)` | `STRING(4)` |  |
| `PA-MESSAGE-TYPE` | Message Type | `PIC X(06)` | `STRING(6)` |  |
| `PA-MESSAGE-SOURCE` | Message Source | `PIC X(06)` | `STRING(6)` |  |
| `PA-AUTH-ID-CODE` | Authorization ID Code | `PIC X(06)` | `STRING(6)` |  |
| `PA-AUTH-RESP-CODE` | Authorization Response Code | `PIC X(02)` | `STRING(2)` |  |
| `PA-AUTH-RESP-REASON` | Authorization Response Reason | `PIC X(04)` | `STRING(4)` |  |
| `PA-PROCESSING-CODE` | Processing Code | `PIC 9(06)` | `INTEGER` |  |
| `PA-TRANSACTION-AMT` | Transaction Amount | `PIC S9(10)V99 COMP-3` | `DECIMAL(12,2)` |  |
| `PA-APPROVED-AMT` | Approved Amount | `PIC S9(10)V99 COMP-3` | `DECIMAL(12,2)` |  |
| `PA-MERCHANT-CATAGORY-CODE` | Merchant Catagory Code | `PIC X(04)` | `STRING(4)` |  |
| `PA-ACQR-COUNTRY-CODE` | Acqr Country Code | `PIC X(03)` | `STRING(3)` |  |
| `PA-POS-ENTRY-MODE` | Pos Entry Mode | `PIC 9(02)` | `INTEGER` |  |
| `PA-MERCHANT-ID` | Merchant ID | `PIC X(15)` | `STRING(15)` |  |
| `PA-MERCHANT-NAME` | Merchant Name | `PIC X(22)` | `STRING(22)` |  |
| `PA-MERCHANT-CITY` | Merchant City | `PIC X(13)` | `STRING(13)` |  |
| `PA-MERCHANT-STATE` | Merchant State | `PIC X(02)` | `STRING(2)` |  |
| `PA-MERCHANT-ZIP` | Merchant Zip | `PIC X(09)` | `STRING(9)` |  |
| `PA-TRANSACTION-ID` | Transaction ID | `PIC X(15)` | `STRING(15)` |  |
| `PA-MATCH-STATUS` | Match Status | `PIC X(01)` | `STRING(1)` |  |
| `PA-AUTH-FRAUD` | Authorization Fraud | `PIC X(01)` | `STRING(1)` |  |
| `PA-FRAUD-RPT-DATE` | Fraud Rpt Date | `PIC X(08)` | `STRING(8)` | Date-like field; verify YYDDD, YYMMDD, or ISO format before migration. |
| `FILLER` | Filler | `PIC X(17)` | `STRING(17)` |  |

#### `CIPAUSMY` as `PENDING-AUTH-SUMMARY`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `PA-ACCT-ID` | Account ID | `PIC S9(11) COMP-3` | `BIGINT` |  |
| `PA-CUST-ID` | Customer ID | `PIC 9(09)` | `INTEGER` |  |
| `PA-AUTH-STATUS` | Authorization Status | `PIC X(01)` | `STRING(1)` |  |
| `PA-ACCOUNT-STATUS` | Account Status | `PIC X(02) OCCURS 5` | `STRING(2)` | Repeating field, 5 occurrences. |
| `PA-CREDIT-LIMIT` | Credit Limit | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `PA-CASH-LIMIT` | Cash Limit | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `PA-CREDIT-BALANCE` | Credit Balance | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `PA-CASH-BALANCE` | Cash Balance | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `PA-APPROVED-AUTH-CNT` | Approved Authorization Count | `PIC S9(04) COMP` | `INTEGER` |  |
| `PA-DECLINED-AUTH-CNT` | Declined Authorization Count | `PIC S9(04) COMP` | `INTEGER` |  |
| `PA-APPROVED-AUTH-AMT` | Approved Authorization Amount | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `PA-DECLINED-AUTH-AMT` | Declined Authorization Amount | `PIC S9(09)V99 COMP-3` | `DECIMAL(11,2)` |  |
| `FILLER` | Filler | `PIC X(34)` | `STRING(34)` |  |

#### `IMSFUNCS` as `FUNC-CODES`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `FUNC-CODES` | Func Codes | `GROUP` | `OBJECT` |  |
| `FUNC-GU` | Func Gu | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-GHU` | Func Ghu | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-GN` | Func Gn | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-GHN` | Func Ghn | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-GNP` | Func Gnp | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-GHNP` | Func Ghnp | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-REPL` | Func Repl | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-ISRT` | Func Isrt | `PIC X(04)` | `STRING(4)` |  |
| `FUNC-DLET` | Func Dlet | `PIC X(04)` | `STRING(4)` |  |
| `PARMCOUNT` | Parmcount | `PIC S9(05) COMP-5` | `INTEGER` |  |

#### `PAUTBPCB` as `PAUTBPCB`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `PAUTBPCB` | Pautbpcb | `GROUP` | `OBJECT` |  |
| `PAUT-DBDNAME` | Paut Dbdname | `PIC X(08)` | `STRING(8)` |  |
| `PAUT-SEG-LEVEL` | Paut Segment Level | `PIC X(02)` | `STRING(2)` |  |
| `PAUT-PCB-STATUS` | Paut Pcb Status | `PIC X(02)` | `STRING(2)` |  |
| `PAUT-PCB-PROCOPT` | Paut Pcb Procopt | `PIC X(04)` | `STRING(4)` |  |
| `FILLER` | Filler | `PIC S9(05) COMP` | `INTEGER` |  |
| `PAUT-SEG-NAME` | Paut Segment Name | `PIC X(08)` | `STRING(8)` |  |
| `PAUT-KEYFB-NAME` | Paut Keyfb Name | `PIC S9(05) COMP` | `INTEGER` |  |
| `PAUT-NUM-SENSEGS` | Paut Number Sensegs | `PIC S9(05) COMP` | `INTEGER` |  |
| `PAUT-KEYFB` | Paut Keyfb | `PIC X(255)` | `STRING(255)` |  |


### Data Movement And Key Mapping

| Line | Source | Target | Meaning |
|------|--------|--------|---------|
| 227 | `PENDING-AUTH-SUMMARY` | `OPFIL1-REC` | PENDING-AUTH-SUMMARY populates OPFIL1-REC |
| 230 | `PA-ACCT-ID` | `ROOT-SEG-KEY` | PA-ACCT-ID populates ROOT-SEG-KEY |
| 241 | `'Y'` | `WS-END-OF-ROOT-SEG` | 'Y' populates WS-END-OF-ROOT-SEG |
| 270 | `PENDING-AUTH-DETAILS` | `CHILD-SEG-REC` | PENDING-AUTH-DETAILS populates CHILD-SEG-REC |
| 275 | `'Y'` | `WS-END-OF-CHILD-SEG` | 'Y' populates WS-END-OF-CHILD-SEG |



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
| IF | 21 |
| DISPLAY | 6 |
| EXIT | 5 |
| OPEN | 4 |
| CLOSE | 4 |
| PERFORM | 3 |
| WRITE | 2 |
| INITIALIZE | 2 |
| GOBACK | 2 |
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
    4000_FILE_CLOSE --> INLINE
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 157 - 172 |
| **View Code** | [Jump to Line 157](../carddemo/PAUDBUNL.CBL#L157) |



### 1000-INITIALIZE

| | |
|---|---|
| **Paragraph** | `1000-INITIALIZE` |
| **Lines** | 173 - 202 |
| **View Code** | [Jump to Line 173](../carddemo/PAUDBUNL.CBL#L173) |



### 1000-EXIT

| | |
|---|---|
| **Paragraph** | `1000-EXIT` |
| **Lines** | 203 - 206 |
| **View Code** | [Jump to Line 203](../carddemo/PAUDBUNL.CBL#L203) |



### 2000-FIND-NEXT-AUTH-SUMMARY

| | |
|---|---|
| **Paragraph** | `2000-FIND-NEXT-AUTH-SUMMARY` |
| **Lines** | 207 - 247 |
| **View Code** | [Jump to Line 207](../carddemo/PAUDBUNL.CBL#L207) |



### 2000-EXIT

| | |
|---|---|
| **Paragraph** | `2000-EXIT` |
| **Lines** | 248 - 252 |
| **View Code** | [Jump to Line 248](../carddemo/PAUDBUNL.CBL#L248) |



### 3000-FIND-NEXT-AUTH-DTL

| | |
|---|---|
| **Paragraph** | `3000-FIND-NEXT-AUTH-DTL` |
| **Lines** | 253 - 284 |
| **View Code** | [Jump to Line 253](../carddemo/PAUDBUNL.CBL#L253) |



### 3000-EXIT

| | |
|---|---|
| **Paragraph** | `3000-EXIT` |
| **Lines** | 285 - 288 |
| **View Code** | [Jump to Line 285](../carddemo/PAUDBUNL.CBL#L285) |



### 4000-FILE-CLOSE

| | |
|---|---|
| **Paragraph** | `4000-FILE-CLOSE` |
| **Lines** | 289 - 304 |
| **View Code** | [Jump to Line 289](../carddemo/PAUDBUNL.CBL#L289) |



### 4000-EXIT

| | |
|---|---|
| **Paragraph** | `4000-EXIT` |
| **Lines** | 305 - 307 |
| **View Code** | [Jump to Line 305](../carddemo/PAUDBUNL.CBL#L305) |



### 9999-ABEND

| | |
|---|---|
| **Paragraph** | `9999-ABEND` |
| **Lines** | 308 - 315 |
| **View Code** | [Jump to Line 308](../carddemo/PAUDBUNL.CBL#L308) |



### 9999-EXIT

| | |
|---|---|
| **Paragraph** | `9999-EXIT` |
| **Lines** | 316 - 317 |
| **View Code** | [Jump to Line 316](../carddemo/PAUDBUNL.CBL#L316) |






## IMS DL/I Calls

This program uses the following IMS DL/I calls:

| Function | Meaning | PCB | Segment Area | SSA | Qualifier | Paragraph | Line |
|----------|---------|-----|--------------|-----|-----------|-----------|------|
| `ENTRY` | IMS Batch Entry Point (DLITCBL) | None | None | None | None | MAIN-PARA | 158 |
| `GN` | Get Next | PAUTBPCB | PENDING-AUTH-SUMMARY | ROOT-UNQUAL-SSA (segment: PAUTSUM0) | None | 2000-FIND-NEXT-AUTH-SUMMARY | 213 |
| `GNP` | Get Next in Parent | PAUTBPCB | PENDING-AUTH-DETAILS | CHILD-UNQUAL-SSA (segment: PAUTDTL1) | None | 3000-FIND-NEXT-AUTH-DTL | 257 |


## Copybook Field Dictionaries

The following copybooks are included by this program. Each entry shows the actual fields
extracted from the copybook source file (`.cpy`).

### Copybook `CIPAUDTY`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `05` | `PA-AUTHORIZATION-KEY` | `None` | None | None |  |
| `10` | `PA-AUTH-DATE-9C` | `S9(05)` | COMP | PA-AUTHORIZATION-KEY |  |
| `10` | `PA-AUTH-TIME-9C` | `S9(09)` | COMP | PA-AUTHORIZATION-KEY |  |
| `05` | `PA-AUTH-ORIG-DATE` | `X(06)` | None | None |  |
| `05` | `PA-AUTH-ORIG-TIME` | `X(06)` | None | None |  |
| `05` | `PA-CARD-NUM` | `X(16)` | None | None |  |
| `05` | `PA-AUTH-TYPE` | `X(04)` | None | None |  |
| `05` | `PA-CARD-EXPIRY-DATE` | `X(04)` | None | None |  |
| `05` | `PA-MESSAGE-TYPE` | `X(06)` | None | None |  |
| `05` | `PA-MESSAGE-SOURCE` | `X(06)` | None | None |  |
| `05` | `PA-AUTH-ID-CODE` | `X(06)` | None | None |  |
| `05` | `PA-AUTH-RESP-CODE` | `X(02)` | None | None |  |
| `88` | `PA-AUTH-APPROVED` | `None` | None | None |  |
| `05` | `PA-AUTH-RESP-REASON` | `X(04)` | None | None |  |
| `05` | `PA-PROCESSING-CODE` | `9(06)` | None | None |  |
| `05` | `PA-TRANSACTION-AMT` | `S9(10)V99` | COMP | None |  |
| `05` | `PA-APPROVED-AMT` | `S9(10)V99` | COMP | None |  |
| `05` | `PA-MERCHANT-CATAGORY-CODE` | `X(04)` | None | None |  |
| `05` | `PA-ACQR-COUNTRY-CODE` | `X(03)` | None | None |  |
| `05` | `PA-POS-ENTRY-MODE` | `9(02)` | None | None |  |
| `05` | `PA-MERCHANT-ID` | `X(15)` | None | None |  |
| `05` | `PA-MERCHANT-NAME` | `X(22)` | None | None |  |
| `05` | `PA-MERCHANT-CITY` | `X(13)` | None | None |  |
| `05` | `PA-MERCHANT-STATE` | `X(02)` | None | None |  |
| `05` | `PA-MERCHANT-ZIP` | `X(09)` | None | None |  |
| `05` | `PA-TRANSACTION-ID` | `X(15)` | None | None |  |
| `05` | `PA-MATCH-STATUS` | `X(01)` | None | None |  |
| `88` | `PA-MATCH-PENDING` | `None` | None | None |  |
| `88` | `PA-MATCH-AUTH-DECLINED` | `None` | None | None |  |
| `88` | `PA-MATCH-PENDING-EXPIRED` | `None` | None | None |  |
| `88` | `PA-MATCHED-WITH-TRAN` | `None` | None | None |  |
| `05` | `PA-AUTH-FRAUD` | `X(01)` | None | None |  |
| `88` | `PA-FRAUD-CONFIRMED` | `None` | None | None |  |
| `88` | `PA-FRAUD-REMOVED` | `None` | None | None |  |
| `05` | `PA-FRAUD-RPT-DATE` | `X(08)` | None | None |  |

### Copybook `CIPAUSMY`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `05` | `PA-ACCT-ID` | `S9(11)` | COMP | None |  |
| `05` | `PA-CUST-ID` | `9(09)` | None | None |  |
| `05` | `PA-AUTH-STATUS` | `X(01)` | None | None |  |
| `05` | `PA-ACCOUNT-STATUS` | `X(02)` | None | None | OCCURS 5 |
| `05` | `PA-CREDIT-LIMIT` | `S9(09)V99` | COMP | None |  |
| `05` | `PA-CASH-LIMIT` | `S9(09)V99` | COMP | None |  |
| `05` | `PA-CREDIT-BALANCE` | `S9(09)V99` | COMP | None |  |
| `05` | `PA-CASH-BALANCE` | `S9(09)V99` | COMP | None |  |
| `05` | `PA-APPROVED-AUTH-CNT` | `S9(04)` | COMP | None |  |
| `05` | `PA-DECLINED-AUTH-CNT` | `S9(04)` | COMP | None |  |
| `05` | `PA-APPROVED-AUTH-AMT` | `S9(09)V99` | COMP | None |  |
| `05` | `PA-DECLINED-AUTH-AMT` | `S9(09)V99` | COMP | None |  |

### Copybook `IMSFUNCS`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `FUNC-CODES` | `None` | None | None |  |
| `05` | `FUNC-GU` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-GHU` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-GN` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-GHN` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-GNP` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-GHNP` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-REPL` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-ISRT` | `X(04)` | None | FUNC-CODES |  |
| `05` | `FUNC-DLET` | `X(04)` | None | FUNC-CODES |  |
| `05` | `PARMCOUNT` | `S9(05)` | COMP | FUNC-CODES |  |

### Copybook `PAUTBPCB`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `PAUTBPCB` | `None` | None | None |  |
| `05` | `PAUT-DBDNAME` | `X(08)` | None | PAUTBPCB |  |
| `05` | `PAUT-SEG-LEVEL` | `X(02)` | None | PAUTBPCB |  |
| `05` | `PAUT-PCB-STATUS` | `X(02)` | None | PAUTBPCB |  |
| `05` | `PAUT-PCB-PROCOPT` | `X(04)` | None | PAUTBPCB |  |
| `05` | `PAUT-SEG-NAME` | `X(08)` | None | PAUTBPCB |  |
| `05` | `PAUT-KEYFB-NAME` | `S9(05)` | COMP | PAUTBPCB |  |
| `05` | `PAUT-NUM-SENSEGS` | `S9(05)` | COMP | PAUTBPCB |  |
| `05` | `PAUT-KEYFB` | `X(255)` | None | PAUTBPCB |  |


## File Record Layouts (FD)

This program declares the following file records (data contracts for I/O):

### `FD OPFILE1` (record `OPFIL1-REC`)

| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
| `01` | `OPFIL1-REC` | `X(100)` | None | None |

### `FD OPFILE2` (record `OPFIL2-REC`)

| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
| `01` | `OPFIL2-REC` | `None` | None | None |
| `05` | `ROOT-SEG-KEY` | `S9(11)` | COMP | OPFIL2-REC |
| `05` | `CHILD-SEG-REC` | `X(200)` | None | OPFIL2-REC |


## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
| `PENDING-AUTH-SUMMARY` | `OPFIL1-REC` | 2000-FIND-NEXT-AUTH-SUMMARY | 227 |
| `PA-ACCT-ID` | `ROOT-SEG-KEY` | 2000-FIND-NEXT-AUTH-SUMMARY | 230 |
| `'Y'` | `WS-END-OF-ROOT-SEG` | 2000-FIND-NEXT-AUTH-SUMMARY | 241 |
| `PENDING-AUTH-DETAILS` | `CHILD-SEG-REC` | 3000-FIND-NEXT-AUTH-DTL | 270 |
| `'Y'` | `WS-END-OF-CHILD-SEG` | 3000-FIND-NEXT-AUTH-DTL | 275 |
| `'16'` | `RETURN-CODE` | 9999-ABEND | 313 |


## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **WARNING** | NAMING | WS-PGMNAME literal does not match the actual PROGRAM-ID | None | 54 |
| **NOTICE** | DEAD_CODE | Variable `WS-PGMNAME` is declared but never referenced | None | 54 |
| **NOTICE** | DEAD_CODE | Variable `WS-AUTH-DATE` is declared but never referenced | None | 57 |
| **NOTICE** | DEAD_CODE | Variable `WS-EXPIRY-DAYS` is declared but never referenced | None | 58 |
| **NOTICE** | DEAD_CODE | Variable `WS-DAY-DIFF` is declared but never referenced | None | 59 |
| **NOTICE** | DEAD_CODE | Variable `IDX` is declared but never referenced | None | 60 |
| **NOTICE** | DEAD_CODE | Variable `WS-CURR-APP-ID` is declared but never referenced | None | 61 |
| **NOTICE** | DEAD_CODE | Variable `WS-NO-CHKP` is declared but never referenced | None | 63 |
| **NOTICE** | DEAD_CODE | Variable `WS-TOT-REC-WRITTEN` is declared but never referenced | None | 65 |
| **NOTICE** | DEAD_CODE | Variable `WS-NO-SUMRY-DELETED` is declared but never referenced | None | 67 |
| **NOTICE** | DEAD_CODE | Variable `WS-NO-DTL-READ` is declared but never referenced | None | 68 |
| **NOTICE** | LOGIC | Paragraph `1000-INITIALIZE` terminates the program on error | 1000-INITIALIZE | 173 |
| **NOTICE** | LOGIC | Paragraph `2000-FIND-NEXT-AUTH-SUMMARY` terminates the program on error | 2000-FIND-NEXT-AUTH-SUMMARY | 207 |
| **NOTICE** | DEPENDENCY | Static CALL to external `CBLTDLI` (not in this codebase) | None | 213 |
| **NOTICE** | LOGIC | Paragraph `3000-FIND-NEXT-AUTH-DTL` terminates the program on error | 3000-FIND-NEXT-AUTH-DTL | 253 |

### WARNING — WS-PGMNAME literal does not match the actual PROGRAM-ID

The program identifier is `PAUDBUNL` but the source sets `WS-PGMNAME` to `'IMSUNLOD'`. This is misleading for debug traces, runtime logs, and audit records that key off WS-PGMNAME.
**Source excerpt** (line 54):
```cobol
05 WS-PGMNAME                 PIC X(08) VALUE 'IMSUNLOD'.
```

**Recommendation:** Update the literal to 'PAUDBUNL' or rename the program to 'IMSUNLOD' depending on which is canonical.
---
### NOTICE — Variable `WS-PGMNAME` is declared but never referenced

`WS-PGMNAME` is declared at line 54 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 54):
```cobol
05 WS-PGMNAME                 PIC X(08) VALUE 'IMSUNLOD'.      00280026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-AUTH-DATE` is declared but never referenced

`WS-AUTH-DATE` is declared at line 57 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 57):
```cobol
05 WS-AUTH-DATE               PIC 9(05).                       00310026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EXPIRY-DAYS` is declared but never referenced

`WS-EXPIRY-DAYS` is declared at line 58 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 58):
```cobol
05 WS-EXPIRY-DAYS             PIC S9(4) COMP.                  00320026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-DAY-DIFF` is declared but never referenced

`WS-DAY-DIFF` is declared at line 59 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 59):
```cobol
05 WS-DAY-DIFF                PIC S9(4) COMP.                  00330026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `IDX` is declared but never referenced

`IDX` is declared at line 60 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 60):
```cobol
05 IDX                        PIC S9(4) COMP.                  00340026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-CURR-APP-ID` is declared but never referenced

`WS-CURR-APP-ID` is declared at line 61 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 61):
```cobol
05 WS-CURR-APP-ID             PIC 9(11).                       00350026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-NO-CHKP` is declared but never referenced

`WS-NO-CHKP` is declared at line 63 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 63):
```cobol
05 WS-NO-CHKP                 PIC  9(8) VALUE 0.               00370026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-TOT-REC-WRITTEN` is declared but never referenced

`WS-TOT-REC-WRITTEN` is declared at line 65 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 65):
```cobol
05 WS-TOT-REC-WRITTEN         PIC S9(8) COMP VALUE 0.          00390026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-NO-SUMRY-DELETED` is declared but never referenced

`WS-NO-SUMRY-DELETED` is declared at line 67 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 67):
```cobol
05 WS-NO-SUMRY-DELETED        PIC S9(8) COMP VALUE 0.          00410026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-NO-DTL-READ` is declared but never referenced

`WS-NO-DTL-READ` is declared at line 68 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 68):
```cobol
05 WS-NO-DTL-READ             PIC S9(8) COMP VALUE 0.          00420026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Paragraph `1000-INITIALIZE` terminates the program on error

`1000-INITIALIZE` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Paragraph `2000-FIND-NEXT-AUTH-SUMMARY` terminates the program on error

`2000-FIND-NEXT-AUTH-SUMMARY` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Static CALL to external `CBLTDLI` (not in this codebase)

`CALL 'CBLTDLI'` appears in the source but `CBLTDLI` is not a program in the loaded codebase. IMS DL/I database call interface.
**Source excerpt** (line 213):
```cobol
CALL 'CBLTDLI'            USING  FUNC-GN                    02070034
```

**Recommendation:** Document this external dependency in the Migration Notes — the modern equivalent must replicate its behaviour.
---
### NOTICE — Paragraph `3000-FIND-NEXT-AUTH-DTL` terminates the program on error

`3000-FIND-NEXT-AUTH-DTL` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---

## External Runtime Parameters

This program receives the following parameters at runtime (via `PROCEDURE DIVISION USING`
or `ENTRY USING`). Each parameter must be supplied by the caller — typically a JCL job
step (`PARM=`), CICS COMMAREA, or the IMS region controller. The migration target needs
an equivalent input wiring.

| # | Parameter | Source | Declared at line |
|---|-----------|--------|------------------|
| 0 | `PAUTBPCB` | ENTRY USING | 158 |
| 0 | `PAUTBPCB` | PROCEDURE DIVISION USING | 153 |

## File OPEN / CLOSE Operations

The exact OPEN mode (INPUT / OUTPUT / I-O / EXTEND) determines whether a file can be
read, written, or both — and whether REWRITE / DELETE are legal. This table is the
source of truth for migrators converting to modern storage layers.

| File | Operation | Mode | Paragraph | Line |
|------|-----------|------|-----------|------|
| `THRU` | CLOSE | None | MAIN-PARA | 166 |
| `OPFILE1` | OPEN | OUTPUT | 1000-INITIALIZE | 186 |
| `OPFILE2` | OPEN | OUTPUT | 1000-INITIALIZE | 194 |
| `OPFILE1` | CLOSE | None | 4000-FILE-CLOSE | 291 |
| `OPFILE2` | CLOSE | None | 4000-FILE-CLOSE | 298 |







## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Program name literal differs from PROGRAM-ID | `WS-PGMNAME` is `IMSUNLOD` while `PROGRAM-ID` is `PAUDBUNL`. Treat this as a migration review item; it may be copied template state or an intentional external name. |
| Checkpoint/restart fields without checkpoint calls | Checkpoint-style fields exist, but no IMS `CHKP` or `XRST` call was extracted. Confirm whether restart logic was abandoned or still expected operationally. |
| Template/debug fields require usage review | Fields such as `DEBUG-OFF`, `DEBUG-ON`, `P-DEBUG-FLAG`, `P-EXPIRY-DAYS`, `PA-CARD-EXPIRY-DATE`, `WK-CHKPT-ID`, `WK-CHKPT-ID-CTR`, `WS-DAY-DIFF` look like debug, checkpoint, or abandoned template state. Verify references before designing modern DTOs or database columns. |
| Numeric validation on a COBOL numeric field | `PA-ACCT-ID IS NUMERIC` was found in source. If the field is packed or binary numeric, this may be corruption detection rather than normal validation. |
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Authorization Expiry Date Validation** `BR-021`  
  If the authorization expiry date is in the past, the authorization record is flagged for review.  
  [View Rule Details](../business-rules/BR-021.md)
- **Authorization Grace Period Handling** `BR-022`  
  Authorizations are granted a grace period after their expiry date. Authorizations within this grace period are handled differently.  
  [View Rule Details](../business-rules/BR-022.md)
- **Authorization Expiry Date Validation** `BR-023`  
  If the authorization expiry date is in the past, the authorization record may be flagged for review or deletion.  
  [View Rule Details](../business-rules/BR-023.md)
- **Authorization Period Calculation** `BR-024`  
  The program calculates the duration of an authorization, possibly to identify authorizations nearing expiry or exceeding a maximum allowed duration.  
  [View Rule Details](../business-rules/BR-024.md)
- **Authorization Record Processing** `BR-025`  
  Authorization summary and detail records are passed to external programs for further processing, such as validation, enrichment, or transfer to other systems.  
  [View Rule Details](../business-rules/BR-025.md)
- **Authorization Expiry Date Validation** `BR-026`  
  If the authorization expiry date is in the past, the authorization record may be flagged for review or deletion.  
  [View Rule Details](../business-rules/BR-026.md)
- **Authorization Period Calculation** `BR-027`  
  The program calculates the duration of an authorization, likely to determine if it falls within acceptable limits.  
  [View Rule Details](../business-rules/BR-027.md)
- **Authorization Record Flagging** `BR-028`  
  Authorization records are flagged based on the calculated authorization period, potentially indicating anomalies or requiring special handling.  
  [View Rule Details](../business-rules/BR-028.md)
- **Authorization Record Flagging Based on Expiry Date Difference** `BR-029`  
  If the difference between the authorization expiry date and the current date exceeds a certain threshold, the authorization record is flagged for review.  
  [View Rule Details](../business-rules/BR-029.md)
- **Authorization Record Deletion Based on Expiry Date** `BR-030`  
  Authorization records are automatically deleted if the expiry date is in the past by a certain amount of time.  
  [View Rule Details](../business-rules/BR-030.md)

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

*Generated 2026-05-12 12:18*