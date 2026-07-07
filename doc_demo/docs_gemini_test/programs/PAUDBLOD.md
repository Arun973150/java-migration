# Program: PAUDBLOD


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `PAUDBLOD` |
| Type | BATCH |
| Lines | 370 |
| Source | [PAUDBLOD.CBL](../carddemo/PAUDBLOD.CBL#L1) |
| Paragraphs | 17 |
| Statements | 74 |
| Impact Risk | **MEDIUM** — 7 programs affected |

> **View Source:** [Open PAUDBLOD.CBL](../carddemo/PAUDBLOD.CBL#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-PGMNAME` | `IMSUNLOD` |
| `WS-ERR-FLG` | `N` |
| `WS-END-OF-AUTHDB-FLAG` | `N` |
| `WS-MORE-AUTHS-FLAG` | `N` |
| `END-OF-FILE` | `10` |

Status conditions found in source:
- `WS-INFIL1-STATUS = SPACES`
- `WS-INFIL2-STATUS = SPACES`
- `WS-INFIL1-STATUS = '10'`
- `PAUT-PCB-STATUS = SPACES`
- `PAUT-PCB-STATUS = 'II'`
- `PAUT-PCB-STATUS NOT EQUAL TO`
- `WS-INFIL2-STATUS = '10'`


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **PAUDBLOD** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call PAUDBLOD (Callers)

*No programs call PAUDBLOD — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by PAUDBLOD (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| `UNKNOWN` | None | 382 |  |
| `UNKNOWN` | None | 434 |  |
| `UNKNOWN` | None | 459 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CIPAUDTY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, COPAUS2C (+2 more) | 7 |
| `CIPAUSMY` | CBPAUP0C, COPAUA0C, COPAUS0C, COPAUS1C, DBUNLDGS (+1 more) | 6 |
| `IMSFUNCS` | DBUNLDGS, PAUDBUNL | 2 |
| `PAUTBPCB` | DBUNLDGS, PAUDBUNL | 2 |

#### Shared Files

| File | Type | Access | Also Used By |
|------|------|--------|-------------|
| `INFILE1` | SEQUENTIAL | SEQUENTIAL |  |
| `INFILE2` | SEQUENTIAL | SEQUENTIAL |  |

## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.

### File Record Layouts

#### `INFILE1` / `INFIL1-REC`
| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
| `INFIL1-REC` | Infil1 Record | `PIC X(100)` | `STRING(100)` |  |

#### `INFILE2` / `INFIL2-REC`
| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
| `INFIL2-REC` | Infil2 Record | `GROUP` | `OBJECT` |  |
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
| 229 | `INFIL1-REC` | `PENDING-AUTH-SUMMARY` | INFIL1-REC populates PENDING-AUTH-SUMMARY |
| 233 | `'Y'` | `END-ROOT-SEG-FILE` | 'Y' populates END-ROOT-SEG-FILE |
| 277 | `ROOT-SEG-KEY` | `QUAL-SSA-KEY-VALUE` | ROOT-SEG-KEY populates QUAL-SSA-KEY-VALUE |
| 280 | `CHILD-SEG-REC` | `PENDING-AUTH-DETAILS` | CHILD-SEG-REC populates PENDING-AUTH-DETAILS |
| 285 | `'Y'` | `END-CHILD-SEG-FILE` | 'Y' populates END-CHILD-SEG-FILE |



---

## Dependency Graph

```mermaid
flowchart TD
    PAUDBLOD["⬤ PAUDBLOD"]:::target
    UNKNOWN["UNKNOWN"]:::callee
    UNKNOWN["UNKNOWN"]:::callee
    UNKNOWN["UNKNOWN"]:::callee
    PAUDBLOD --> UNKNOWN
    PAUDBLOD --> UNKNOWN
    PAUDBLOD --> UNKNOWN
    CB_CIPAUDTY{{"CIPAUDTY"}}:::copybook
    PAUDBLOD -.- CB_CIPAUDTY
    CBPAUP0C["CBPAUP0C"]:::coupled
    CB_CIPAUDTY -.- CBPAUP0C
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CIPAUDTY -.- COPAUA0C
    COPAUS0C["COPAUS0C"]:::coupled
    CB_CIPAUDTY -.- COPAUS0C
    CB_CIPAUSMY{{"CIPAUSMY"}}:::copybook
    PAUDBLOD -.- CB_CIPAUSMY
    CBPAUP0C["CBPAUP0C"]:::coupled
    CB_CIPAUSMY -.- CBPAUP0C
    COPAUA0C["COPAUA0C"]:::coupled
    CB_CIPAUSMY -.- COPAUA0C
    COPAUS0C["COPAUS0C"]:::coupled
    CB_CIPAUSMY -.- COPAUS0C
    CB_IMSFUNCS{{"IMSFUNCS"}}:::copybook
    PAUDBLOD -.- CB_IMSFUNCS
    DBUNLDGS["DBUNLDGS"]:::coupled
    CB_IMSFUNCS -.- DBUNLDGS
    PAUDBUNL["PAUDBUNL"]:::coupled
    CB_IMSFUNCS -.- PAUDBUNL
    CB_PAUTBPCB{{"PAUTBPCB"}}:::copybook
    PAUDBLOD -.- CB_PAUTBPCB
    DBUNLDGS["DBUNLDGS"]:::coupled
    CB_PAUTBPCB -.- DBUNLDGS
    PAUDBUNL["PAUDBUNL"]:::coupled
    CB_PAUTBPCB -.- PAUDBUNL
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

> **If you change PAUDBLOD, what else could break?**

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
- `PAUDBUNL`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| IF | 30 |
| DISPLAY | 10 |
| EXIT | 8 |
| READ | 4 |
| PERFORM | 4 |
| OPEN | 4 |
| CLOSE | 4 |
| CALL | 3 |
| GOBACK | 2 |
| ACCEPT | 2 |
| MOVE | 1 |
| INITIALIZE | 1 |
| ENTRY | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN_PARA["MAIN-PARA"]
    1000_INITIALIZE["1000-INITIALIZE"]
    1000_EXIT["1000-EXIT"]
    2000_READ_ROOT_SEG_FILE["2000-READ-ROOT-SEG-FILE"]
    2000_EXIT["2000-EXIT"]
    2100_INSERT_ROOT_SEG["2100-INSERT-ROOT-SEG"]
    2100_EXIT["2100-EXIT"]
    3000_READ_CHILD_SEG_FILE["3000-READ-CHILD-SEG-FILE"]
    3000_EXIT["3000-EXIT"]
    3100_INSERT_CHILD_SEG["3100-INSERT-CHILD-SEG"]
    3100_EXIT["3100-EXIT"]
    3200_INSERT_IMS_CALL["3200-INSERT-IMS-CALL"]
    3200_EXIT["3200-EXIT"]
    4000_FILE_CLOSE["4000-FILE-CLOSE"]
    4000_EXIT["4000-EXIT"]
    START --> MAIN_PARA
    3100_INSERT_CHILD_SEG --> INLINE
    3100_EXIT --> INLINE
    3200_INSERT_IMS_CALL --> INLINE
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 169 - 189 |
| **View Code** | [Jump to Line 169](../carddemo/PAUDBLOD.CBL#L169) |



### 1000-INITIALIZE

| | |
|---|---|
| **Paragraph** | `1000-INITIALIZE` |
| **Lines** | 190 - 217 |
| **View Code** | [Jump to Line 190](../carddemo/PAUDBLOD.CBL#L190) |



### 1000-EXIT

| | |
|---|---|
| **Paragraph** | `1000-EXIT` |
| **Lines** | 218 - 221 |
| **View Code** | [Jump to Line 218](../carddemo/PAUDBLOD.CBL#L218) |



### 2000-READ-ROOT-SEG-FILE

| | |
|---|---|
| **Paragraph** | `2000-READ-ROOT-SEG-FILE` |
| **Lines** | 222 - 238 |
| **View Code** | [Jump to Line 222](../carddemo/PAUDBLOD.CBL#L222) |



### 2000-EXIT

| | |
|---|---|
| **Paragraph** | `2000-EXIT` |
| **Lines** | 239 - 241 |
| **View Code** | [Jump to Line 239](../carddemo/PAUDBLOD.CBL#L239) |



### 2100-INSERT-ROOT-SEG

| | |
|---|---|
| **Paragraph** | `2100-INSERT-ROOT-SEG` |
| **Lines** | 242 - 263 |
| **View Code** | [Jump to Line 242](../carddemo/PAUDBLOD.CBL#L242) |



### 2100-EXIT

| | |
|---|---|
| **Paragraph** | `2100-EXIT` |
| **Lines** | 264 - 268 |
| **View Code** | [Jump to Line 264](../carddemo/PAUDBLOD.CBL#L264) |



### 3000-READ-CHILD-SEG-FILE

| | |
|---|---|
| **Paragraph** | `3000-READ-CHILD-SEG-FILE` |
| **Lines** | 269 - 289 |
| **View Code** | [Jump to Line 269](../carddemo/PAUDBLOD.CBL#L269) |



### 3000-EXIT

| | |
|---|---|
| **Paragraph** | `3000-EXIT` |
| **Lines** | 290 - 291 |
| **View Code** | [Jump to Line 290](../carddemo/PAUDBLOD.CBL#L290) |



### 3100-INSERT-CHILD-SEG

| | |
|---|---|
| **Paragraph** | `3100-INSERT-CHILD-SEG` |
| **Lines** | 292 - 314 |
| **View Code** | [Jump to Line 292](../carddemo/PAUDBLOD.CBL#L292) |



### 3100-EXIT

| | |
|---|---|
| **Paragraph** | `3100-EXIT` |
| **Lines** | 315 - 317 |
| **View Code** | [Jump to Line 315](../carddemo/PAUDBLOD.CBL#L315) |



### 3200-INSERT-IMS-CALL

| | |
|---|---|
| **Paragraph** | `3200-INSERT-IMS-CALL` |
| **Lines** | 318 - 337 |
| **View Code** | [Jump to Line 318](../carddemo/PAUDBLOD.CBL#L318) |



### 3200-EXIT

| | |
|---|---|
| **Paragraph** | `3200-EXIT` |
| **Lines** | 338 - 340 |
| **View Code** | [Jump to Line 338](../carddemo/PAUDBLOD.CBL#L338) |



### 4000-FILE-CLOSE

| | |
|---|---|
| **Paragraph** | `4000-FILE-CLOSE` |
| **Lines** | 341 - 356 |
| **View Code** | [Jump to Line 341](../carddemo/PAUDBLOD.CBL#L341) |



### 4000-EXIT

| | |
|---|---|
| **Paragraph** | `4000-EXIT` |
| **Lines** | 357 - 359 |
| **View Code** | [Jump to Line 357](../carddemo/PAUDBLOD.CBL#L357) |



### 9999-ABEND

| | |
|---|---|
| **Paragraph** | `9999-ABEND` |
| **Lines** | 360 - 367 |
| **View Code** | [Jump to Line 360](../carddemo/PAUDBLOD.CBL#L360) |



### 9999-EXIT

| | |
|---|---|
| **Paragraph** | `9999-EXIT` |
| **Lines** | 368 - 369 |
| **View Code** | [Jump to Line 368](../carddemo/PAUDBLOD.CBL#L368) |






## IMS DL/I Calls

This program uses the following IMS DL/I calls:

| Function | Meaning | PCB | Segment Area | SSA | Qualifier | Paragraph | Line |
|----------|---------|-----|--------------|-----|-----------|-----------|------|
| `ENTRY` | IMS Batch Entry Point (DLITCBL) | None | None | None | None | MAIN-PARA | 171 |
| `ISRT` | Insert | PAUTBPCB | PENDING-AUTH-SUMMARY | ROOT-UNQUAL-SSA (segment: PAUTSUM0) | None | 2100-INSERT-ROOT-SEG | 244 |
| `GU` | Get Unique | PAUTBPCB | PENDING-AUTH-SUMMARY | ROOT-QUAL-SSA (segment: PAUTSUM0) | ACCNTID EQ QUAL-SSA-KEY-VALUE | 3100-INSERT-CHILD-SEG | 296 |
| `ISRT` | Insert | PAUTBPCB | PENDING-AUTH-DETAILS | CHILD-UNQUAL-SSA (segment: PAUTDTL1) | None | 3200-INSERT-IMS-CALL | 321 |


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

### `FD INFILE1` (record `INFIL1-REC`)

| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
| `01` | `INFIL1-REC` | `X(100)` | None | None |

### `FD INFILE2` (record `INFIL2-REC`)

| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
| `01` | `INFIL2-REC` | `None` | None | None |
| `05` | `ROOT-SEG-KEY` | `S9(11)` | COMP | INFIL2-REC |
| `05` | `CHILD-SEG-REC` | `X(200)` | None | INFIL2-REC |


## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
| `INFIL1-REC` | `PENDING-AUTH-SUMMARY` | 2000-READ-ROOT-SEG-FILE | 229 |
| `'Y'` | `END-ROOT-SEG-FILE` | 2000-READ-ROOT-SEG-FILE | 233 |
| `ROOT-SEG-KEY` | `QUAL-SSA-KEY-VALUE` | 3000-READ-CHILD-SEG-FILE | 277 |
| `CHILD-SEG-REC` | `PENDING-AUTH-DETAILS` | 3000-READ-CHILD-SEG-FILE | 280 |
| `'Y'` | `END-CHILD-SEG-FILE` | 3000-READ-CHILD-SEG-FILE | 285 |
| `'16'` | `RETURN-CODE` | 9999-ABEND | 365 |


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
| **NOTICE** | DEAD_CODE | Variable `WS-AUTH-SMRY-PROC-CNT` is declared but never referenced | None | 64 |
| **NOTICE** | DEAD_CODE | Variable `WS-TOT-REC-WRITTEN` is declared but never referenced | None | 65 |
| **NOTICE** | DEAD_CODE | Variable `WS-NO-SUMRY-READ` is declared but never referenced | None | 66 |
| **NOTICE** | LOGIC | Paragraph `1000-INITIALIZE` terminates the program on error | 1000-INITIALIZE | 190 |
| **NOTICE** | LOGIC | Paragraph `2100-INSERT-ROOT-SEG` terminates the program on error | 2100-INSERT-ROOT-SEG | 242 |
| **NOTICE** | DEPENDENCY | Static CALL to external `CBLTDLI` (not in this codebase) | None | 244 |
| **NOTICE** | LOGIC | Paragraph `3100-INSERT-CHILD-SEG` terminates the program on error | 3100-INSERT-CHILD-SEG | 292 |
| **NOTICE** | LOGIC | Paragraph `3200-INSERT-IMS-CALL` terminates the program on error | 3200-INSERT-IMS-CALL | 318 |

### WARNING — WS-PGMNAME literal does not match the actual PROGRAM-ID

The program identifier is `PAUDBLOD` but the source sets `WS-PGMNAME` to `'IMSUNLOD'`. This is misleading for debug traces, runtime logs, and audit records that key off WS-PGMNAME.
**Source excerpt** (line 54):
```cobol
05 WS-PGMNAME                 PIC X(08) VALUE 'IMSUNLOD'.
```

**Recommendation:** Update the literal to 'PAUDBLOD' or rename the program to 'IMSUNLOD' depending on which is canonical.
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
### NOTICE — Variable `WS-AUTH-SMRY-PROC-CNT` is declared but never referenced

`WS-AUTH-SMRY-PROC-CNT` is declared at line 64 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 64):
```cobol
05 WS-AUTH-SMRY-PROC-CNT      PIC  9(8) VALUE 0.               00380026
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
### NOTICE — Variable `WS-NO-SUMRY-READ` is declared but never referenced

`WS-NO-SUMRY-READ` is declared at line 66 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 66):
```cobol
05 WS-NO-SUMRY-READ           PIC S9(8) COMP VALUE 0.          00400026
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Paragraph `1000-INITIALIZE` terminates the program on error

`1000-INITIALIZE` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Paragraph `2100-INSERT-ROOT-SEG` terminates the program on error

`2100-INSERT-ROOT-SEG` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Static CALL to external `CBLTDLI` (not in this codebase)

`CALL 'CBLTDLI'` appears in the source but `CBLTDLI` is not a program in the loaded codebase. IMS DL/I database call interface.
**Source excerpt** (line 244):
```cobol
CALL 'CBLTDLI'       USING  FUNC-ISRT                       02070053
```

**Recommendation:** Document this external dependency in the Migration Notes — the modern equivalent must replicate its behaviour.
---
### NOTICE — Paragraph `3100-INSERT-CHILD-SEG` terminates the program on error

`3100-INSERT-CHILD-SEG` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Paragraph `3200-INSERT-IMS-CALL` terminates the program on error

`3200-INSERT-IMS-CALL` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---

## External Runtime Parameters

This program receives the following parameters at runtime (via `PROCEDURE DIVISION USING`
or `ENTRY USING`). Each parameter must be supplied by the caller — typically a JCL job
step (`PARM=`), CICS COMMAREA, or the IMS region controller. The migration target needs
an equivalent input wiring.

| # | Parameter | Source | Declared at line |
|---|-----------|--------|------------------|
| 0 | `PAUTBPCB` | ENTRY USING | 171 |
| 0 | `IO-PCB-MASK` | PROCEDURE DIVISION USING | 164 |
| 1 | `PAUTBPCB` | PROCEDURE DIVISION USING | 164 |

## File OPEN / CLOSE Operations

The exact OPEN mode (INPUT / OUTPUT / I-O / EXTEND) determines whether a file can be
read, written, or both — and whether REWRITE / DELETE are legal. This table is the
source of truth for migrators converting to modern storage layers.

| File | Operation | Mode | Paragraph | Line |
|------|-----------|------|-----------|------|
| `THRU` | CLOSE | None | MAIN-PARA | 183 |
| `INFILE1` | OPEN | INPUT | 1000-INITIALIZE | 201 |
| `INFILE2` | OPEN | INPUT | 1000-INITIALIZE | 209 |
| `INFILE1` | CLOSE | None | 4000-FILE-CLOSE | 343 |
| `INFILE2` | CLOSE | None | 4000-FILE-CLOSE | 350 |







## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Program name literal differs from PROGRAM-ID | `WS-PGMNAME` is `IMSUNLOD` while `PROGRAM-ID` is `PAUDBLOD`. Treat this as a migration review item; it may be copied template state or an intentional external name. |
| Checkpoint/restart fields without checkpoint calls | Checkpoint-style fields exist, but no IMS `CHKP` or `XRST` call was extracted. Confirm whether restart logic was abandoned or still expected operationally. |
| Template/debug fields require usage review | Fields such as `DEBUG-OFF`, `DEBUG-ON`, `P-DEBUG-FLAG`, `P-EXPIRY-DAYS`, `PA-CARD-EXPIRY-DATE`, `WK-CHKPT-ID`, `WK-CHKPT-ID-CTR`, `WS-DAY-DIFF` look like debug, checkpoint, or abandoned template state. Verify references before designing modern DTOs or database columns. |
| Numeric validation on a COBOL numeric field | `ROOT-SEG-KEY IS NUMERIC` was found in source. If the field is packed or binary numeric, this may be corruption detection rather than normal validation. |
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Root Segment Data Validation** `BR-010`  
  If the root segment data is invalid, the authorization data loading process will not proceed.  
  [View Rule Details](../business-rules/BR-010.md)
- **Child Segment Data Validation** `BR-011`  
  If the child segment data is invalid, the authorization data loading process for that specific child segment will not proceed.  
  [View Rule Details](../business-rules/BR-011.md)
- **Root Record Validation** `BR-012`  
  If a root segment record is invalid, the authorization data loading process will stop.  
  [View Rule Details](../business-rules/BR-012.md)
- **Root Segment Insert Failure** `BR-013`  
  If inserting a root segment into the database fails, the program should stop processing.  
  [View Rule Details](../business-rules/BR-013.md)
- **Child Record Validation** `BR-014`  
  If a child record is invalid, it will be rejected.  
  [View Rule Details](../business-rules/BR-014.md)
- **Child Segment Insertion** `BR-015`  
  Child segment data is added to the database to provide more details about the root segment.  
  [View Rule Details](../business-rules/BR-015.md)
- **Root Segment Insertion Success Check** `BR-016`  
  If the attempt to insert a root segment into the database is successful, proceed to the next step.  
  [View Rule Details](../business-rules/BR-016.md)
- **Child Segment Insertion Success Check** `BR-017`  
  If the attempt to insert a child segment into the database is successful, proceed to the next step.  
  [View Rule Details](../business-rules/BR-017.md)
- **Database Insertion Error Handling** `BR-018`  
  If an error occurs during the insertion of either a root or child segment into the database, the program should handle the error.  
  [View Rule Details](../business-rules/BR-018.md)
- **Input File Close Status Check** `BR-019`  
  If the input file close operation fails, the program should halt.  
  [View Rule Details](../business-rules/BR-019.md)
- **Output File Close Status Check** `BR-020`  
  If the output file close operation fails, the program should halt.  
  [View Rule Details](../business-rules/BR-020.md)

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
| `WS-END-OF-INFILE1` | 5 | `X(01)` | WORKING-STORAGE | None |
| `WS-END-OF-INFILE2` | 5 | `X(01)` | WORKING-STORAGE | None |
| `WS-INFILE-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-INFIL1-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-INFIL2-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `END-ROOT-SEG-FILE` | 5 | `X(01)` | WORKING-STORAGE | None |
| `END-CHILD-SEG-FILE` | 5 | `X(01)` | WORKING-STORAGE | None |
| `WS-CUSTID-STATUS` | 5 | `X(02)` | WORKING-STORAGE | None |
| `END-OF-FILE` | 88 | `None` | WORKING-STORAGE | None |
| `WK-CHKPT-ID` | 5 | `None` | WORKING-STORAGE | None |
| `FILLER` | 10 | `X(04)` | WORKING-STORAGE | None |
| `WK-CHKPT-ID-CTR` | 10 | `9(04)` | WORKING-STORAGE | None |
| `WS-IMS-VARIABLES` | 1 | `None` | WORKING-STORAGE | None |
| `IMS-RETURN-CODE` | 5 | `X(02)` | WORKING-STORAGE | None |
| `STATUS-OK` | 88 | `None` | WORKING-STORAGE | None |

*Showing 40 of 148 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-05-12 12:18*