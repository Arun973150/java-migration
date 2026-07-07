# Program: COUSR01C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COUSR01C` |
| Type | ONLINE |
| Lines | 300 |
| Source | [COUSR01C.cbl](../carddemo/COUSR01C.cbl#L1) |
| Paragraphs | 9 |
| Statements | 38 |
| Impact Risk | **HIGH** — 20 programs affected |

> **View Source:** [Open COUSR01C.cbl](../carddemo/COUSR01C.cbl#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-PGMNAME` | `COUSR01C` |
| `WS-TRANID` | `CU01` |
| `WS-USRSEC-FILE` | `USRSEC` |
| `WS-ERR-FLG` | `N` |


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **COUSR01C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COUSR01C (Callers)

*No programs call COUSR01C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COUSR01C (Callees)

*COUSR01C does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `COCOM01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `COTTL01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `COUSR01` |  | 0 |
| `CSDAT01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `CSMSG01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `CSUSR01Y` | COACTUPC, COACTVWC, COADM01C, COCRDLIC, COCRDSLC (+8 more) | 13 |
| `DFHAID` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `DFHBMSCA` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |


## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.


### Copybook Segment Layouts

#### `COCOM01Y` as `CARDDEMO-COMMAREA`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CARDDEMO-COMMAREA` | Carddemo Commarea | `GROUP` | `OBJECT` |  |
| `CDEMO-GENERAL-INFO` | General Info | `GROUP` | `OBJECT` |  |
| `CDEMO-FROM-TRANID` | From Tranid | `PIC X(04)` | `STRING(4)` |  |
| `CDEMO-FROM-PROGRAM` | From Program | `PIC X(08)` | `STRING(8)` |  |
| `CDEMO-TO-TRANID` | To Tranid | `PIC X(04)` | `STRING(4)` |  |
| `CDEMO-TO-PROGRAM` | To Program | `PIC X(08)` | `STRING(8)` |  |
| `CDEMO-USER-ID` | User ID | `PIC X(08)` | `STRING(8)` |  |
| `CDEMO-USER-TYPE` | User Type | `PIC X(01)` | `STRING(1)` |  |
| `CDEMO-PGM-CONTEXT` | Pgm Context | `PIC 9(01)` | `INTEGER` |  |
| `CDEMO-CUSTOMER-INFO` | Customer Info | `GROUP` | `OBJECT` |  |
| `CDEMO-CUST-ID` | Customer ID | `PIC 9(09)` | `INTEGER` |  |
| `CDEMO-CUST-FNAME` | Customer Fname | `PIC X(25)` | `STRING(25)` |  |
| `CDEMO-CUST-MNAME` | Customer Mname | `PIC X(25)` | `STRING(25)` |  |
| `CDEMO-CUST-LNAME` | Customer Lname | `PIC X(25)` | `STRING(25)` |  |
| `CDEMO-ACCOUNT-INFO` | Account Info | `GROUP` | `OBJECT` |  |
| `CDEMO-ACCT-ID` | Account ID | `PIC 9(11)` | `BIGINT` |  |
| `CDEMO-ACCT-STATUS` | Account Status | `PIC X(01)` | `STRING(1)` |  |
| `CDEMO-CARD-INFO` | Card Info | `GROUP` | `OBJECT` |  |
| `CDEMO-CARD-NUM` | Card Number | `PIC 9(16)` | `BIGINT` |  |
| `CDEMO-MORE-INFO` | More Info | `GROUP` | `OBJECT` |  |
| `CDEMO-LAST-MAP` | Last Map | `PIC X(7)` | `STRING(7)` |  |
| `CDEMO-LAST-MAPSET` | Last Mapset | `PIC X(7)` | `STRING(7)` |  |

#### `COTTL01Y` as `CCDA-SCREEN-TITLE`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CCDA-SCREEN-TITLE` | Ccda Screen Title | `GROUP` | `OBJECT` |  |
| `CCDA-TITLE01` | Ccda Title01 | `PIC X(40)` | `STRING(40)` |  |
| `CCDA-TITLE02` | Ccda Title02 | `PIC X(40)` | `STRING(40)` |  |
| `CCDA-THANK-YOU` | Ccda Thank You | `PIC X(40)` | `STRING(40)` |  |

#### `COUSR01` as `COUSR1AI`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `COUSR1AI` | Cousr1Ai | `GROUP` | `OBJECT` |  |
| `COUSR1AO` | Cousr1Ao | `GROUP` | `OBJECT` |  |

#### `CSDAT01Y` as `WS-DATE-TIME`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `WS-DATE-TIME` | Date Time | `GROUP` | `OBJECT` |  |
| `WS-CURDATE-DATA` | Curdate Data | `GROUP` | `OBJECT` |  |
| `WS-CURDATE` | Curdate | `GROUP` | `OBJECT` |  |
| `WS-CURDATE-YEAR` | Curdate Year | `PIC 9(04)` | `INTEGER` |  |
| `WS-CURDATE-MONTH` | Curdate Month | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURDATE-DAY` | Curdate Day | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURDATE-N` | Curdate N | `PIC 9(08)` | `INTEGER` |  |
| `WS-CURTIME` | Curtime | `GROUP` | `OBJECT` |  |
| `WS-CURTIME-HOURS` | Curtime Hours | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURTIME-MINUTE` | Curtime Minute | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURTIME-SECOND` | Curtime Second | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURTIME-MILSEC` | Curtime Milsec | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURTIME-N` | Curtime N | `PIC 9(08)` | `INTEGER` |  |
| `WS-CURDATE-MM-DD-YY` | Curdate Mm Dd Yy | `GROUP` | `OBJECT` |  |
| `WS-CURDATE-MM` | Curdate Mm | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-CURDATE-DD` | Curdate Dd | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-CURDATE-YY` | Curdate Yy | `PIC 9(02)` | `INTEGER` |  |
| `WS-CURTIME-HH-MM-SS` | Curtime Hh Mm Ss | `GROUP` | `OBJECT` |  |
| `WS-CURTIME-HH` | Curtime Hh | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-CURTIME-MM` | Curtime Mm | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-CURTIME-SS` | Curtime Ss | `PIC 9(02)` | `INTEGER` |  |
| `WS-TIMESTAMP` | Timestamp | `GROUP` | `OBJECT` |  |
| `WS-TIMESTAMP-DT-YYYY` | Timestamp Date Yyyy | `PIC 9(04)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-DT-MM` | Timestamp Date Mm | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-DT-DD` | Timestamp Date Dd | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-TM-HH` | Timestamp Tm Hh | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-TM-MM` | Timestamp Tm Mm | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-TM-SS` | Timestamp Tm Ss | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(01)` | `STRING(1)` |  |
| `WS-TIMESTAMP-TM-MS6` | Timestamp Tm Ms6 | `PIC 9(06)` | `INTEGER` |  |

#### `CSMSG01Y` as `CCDA-COMMON-MESSAGES`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CCDA-COMMON-MESSAGES` | Ccda Common Messages | `GROUP` | `OBJECT` |  |
| `CCDA-MSG-THANK-YOU` | Ccda Msg Thank You | `PIC X(50)` | `STRING(50)` |  |
| `CCDA-MSG-INVALID-KEY` | Ccda Msg Invalid Key | `PIC X(50)` | `STRING(50)` |  |

#### `CSUSR01Y` as `SEC-USER-DATA`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `SEC-USER-DATA` | Sec User Data | `GROUP` | `OBJECT` |  |
| `SEC-USR-ID` | Sec Usr ID | `PIC X(08)` | `STRING(8)` |  |
| `SEC-USR-FNAME` | Sec Usr Fname | `PIC X(20)` | `STRING(20)` |  |
| `SEC-USR-LNAME` | Sec Usr Lname | `PIC X(20)` | `STRING(20)` |  |
| `SEC-USR-PWD` | Sec Usr Pwd | `PIC X(08)` | `STRING(8)` |  |
| `SEC-USR-TYPE` | Sec Usr Type | `PIC X(01)` | `STRING(1)` |  |
| `SEC-USR-FILLER` | Sec Usr Filler | `PIC X(23)` | `STRING(23)` |  |

#### `DFHAID` as `DFHAID`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `DFHAID` | Dfhaid | `GROUP` | `OBJECT` |  |

#### `DFHBMSCA` as `DFHBMSCA`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `DFHBMSCA` | Dfhbmsca | `GROUP` | `OBJECT` |  |


### Data Movement And Key Mapping

| Line | Source | Target | Meaning |
|------|--------|--------|---------|
| 75 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |
| 101 | `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | CCDA-MSG-INVALID-KEY populates WS-MESSAGE |
| 188 | `WS-MESSAGE` | `ERRMSGO OF COUSR1AO` | WS-MESSAGE populates ERRMSGO OF COUSR1AO |
| 216 | `FUNCTION CURRENT-DATE` | `WS-CURDATE-DATA` | FUNCTION CURRENT-DATE populates WS-CURDATE-DATA |
| 223 | `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | WS-CURDATE-MONTH populates WS-CURDATE-MM |
| 224 | `WS-CURDATE-DAY` | `WS-CURDATE-DD` | WS-CURDATE-DAY populates WS-CURDATE-DD |
| 225 | `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | WS-CURDATE-YEAR(3:2) populates WS-CURDATE-YY |
| 227 | `WS-CURDATE-MM-DD-YY` | `CURDATEO OF COUSR1AO` | WS-CURDATE-MM-DD-YY populates CURDATEO OF COUSR1AO |
| 253 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |



---

## Dependency Graph

```mermaid
flowchart TD
    COUSR01C["⬤ COUSR01C"]:::target
    CB_COCOM01Y{{"COCOM01Y"}}:::copybook
    COUSR01C -.- CB_COCOM01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COCOM01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COCOM01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COCOM01Y -.- COADM01C
    CB_COTTL01Y{{"COTTL01Y"}}:::copybook
    COUSR01C -.- CB_COTTL01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COTTL01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COTTL01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COTTL01Y -.- COADM01C
    CB_CSDAT01Y{{"CSDAT01Y"}}:::copybook
    COUSR01C -.- CB_CSDAT01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSDAT01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSDAT01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSDAT01Y -.- COADM01C
    CB_CSMSG01Y{{"CSMSG01Y"}}:::copybook
    COUSR01C -.- CB_CSMSG01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSMSG01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSMSG01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSMSG01Y -.- COADM01C
    CB_CSUSR01Y{{"CSUSR01Y"}}:::copybook
    COUSR01C -.- CB_CSUSR01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSUSR01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSUSR01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSUSR01Y -.- COADM01C
    CB_DFHAID{{"DFHAID"}}:::copybook
    COUSR01C -.- CB_DFHAID
    COACTUPC["COACTUPC"]:::coupled
    CB_DFHAID -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_DFHAID -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_DFHAID -.- COADM01C
    CB_DFHBMSCA{{"DFHBMSCA"}}:::copybook
    COUSR01C -.- CB_DFHBMSCA
    COACTUPC["COACTUPC"]:::coupled
    CB_DFHBMSCA -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_DFHBMSCA -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_DFHBMSCA -.- COADM01C
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

> **If you change COUSR01C, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 20 |
| **Total Impact** | **20** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `COACTUPC`
- `COACTVWC`
- `COADM01C`
- `COBIL00C`
- `COCRDLIC`
- `COCRDSLC`
- `COCRDUPC`
- `COMEN01C`
- `COPAUS0C`
- `COPAUS1C`
- `CORPT00C`
- `COSGN00C`
- `COTRN00C`
- `COTRN01C`
- `COTRN02C`
- `COTRTLIC`
- `COTRTUPC`
- `COUSR00C`
- `COUSR02C`
- `COUSR03C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| MOVE | 20 |
| IF | 7 |
| EXEC_CICS | 5 |
| PERFORM | 3 |
| EVALUATE | 2 |
| SET | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN_PARA["MAIN-PARA"]
    PROCESS_ENTER_KEY["PROCESS-ENTER-KEY"]
    RETURN_TO_PREV_SCREEN["RETURN-TO-PREV-SCREEN"]
    SEND_USRADD_SCREEN["SEND-USRADD-SCREEN"]
    RECEIVE_USRADD_SCREEN["RECEIVE-USRADD-SCREEN"]
    POPULATE_HEADER_INFO["POPULATE-HEADER-INFO"]
    WRITE_USER_SEC_FILE["WRITE-USER-SEC-FILE"]
    CLEAR_CURRENT_SCREEN["CLEAR-CURRENT-SCREEN"]
    INITIALIZE_ALL_FIELDS["INITIALIZE-ALL-FIELDS"]
    START --> MAIN_PARA
    MAIN_PARA --> RETURN_TO_PREV_SCREEN
    MAIN_PARA --> SEND_USRADD_SCREEN
    MAIN_PARA --> RECEIVE_USRADD_SCREEN
    MAIN_PARA --> PROCESS_ENTER_KEY
    MAIN_PARA --> CLEAR_CURRENT_SCREEN
    PROCESS_ENTER_KEY --> SEND_USRADD_SCREEN
    PROCESS_ENTER_KEY --> WRITE_USER_SEC_FILE
    SEND_USRADD_SCREEN --> POPULATE_HEADER_INFO
    WRITE_USER_SEC_FILE --> INITIALIZE_ALL_FIELDS
    WRITE_USER_SEC_FILE --> SEND_USRADD_SCREEN
    CLEAR_CURRENT_SCREEN --> INITIALIZE_ALL_FIELDS
    CLEAR_CURRENT_SCREEN --> SEND_USRADD_SCREEN
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 71 - 114 |
| **View Code** | [Jump to Line 71](../carddemo/COUSR01C.cbl#L71) |



### PROCESS-ENTER-KEY

| | |
|---|---|
| **Paragraph** | `PROCESS-ENTER-KEY` |
| **Lines** | 115 - 164 |
| **View Code** | [Jump to Line 115](../carddemo/COUSR01C.cbl#L115) |



### RETURN-TO-PREV-SCREEN

| | |
|---|---|
| **Paragraph** | `RETURN-TO-PREV-SCREEN` |
| **Lines** | 165 - 183 |
| **View Code** | [Jump to Line 165](../carddemo/COUSR01C.cbl#L165) |



### SEND-USRADD-SCREEN

| | |
|---|---|
| **Paragraph** | `SEND-USRADD-SCREEN` |
| **Lines** | 184 - 200 |
| **View Code** | [Jump to Line 184](../carddemo/COUSR01C.cbl#L184) |



### RECEIVE-USRADD-SCREEN

| | |
|---|---|
| **Paragraph** | `RECEIVE-USRADD-SCREEN` |
| **Lines** | 201 - 213 |
| **View Code** | [Jump to Line 201](../carddemo/COUSR01C.cbl#L201) |



### POPULATE-HEADER-INFO

| | |
|---|---|
| **Paragraph** | `POPULATE-HEADER-INFO` |
| **Lines** | 214 - 237 |
| **View Code** | [Jump to Line 214](../carddemo/COUSR01C.cbl#L214) |



### WRITE-USER-SEC-FILE

| | |
|---|---|
| **Paragraph** | `WRITE-USER-SEC-FILE` |
| **Lines** | 238 - 278 |
| **View Code** | [Jump to Line 238](../carddemo/COUSR01C.cbl#L238) |



### CLEAR-CURRENT-SCREEN

| | |
|---|---|
| **Paragraph** | `CLEAR-CURRENT-SCREEN` |
| **Lines** | 279 - 286 |
| **View Code** | [Jump to Line 279](../carddemo/COUSR01C.cbl#L279) |



### INITIALIZE-ALL-FIELDS

| | |
|---|---|
| **Paragraph** | `INITIALIZE-ALL-FIELDS` |
| **Lines** | 287 - 299 |
| **View Code** | [Jump to Line 287](../carddemo/COUSR01C.cbl#L287) |







## Copybook Field Dictionaries

The following copybooks are included by this program. Each entry shows the actual fields
extracted from the copybook source file (`.cpy`).

### Copybook `COCOM01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CARDDEMO-COMMAREA` | `None` | None | None |  |
| `05` | `CDEMO-GENERAL-INFO` | `None` | None | CARDDEMO-COMMAREA |  |
| `10` | `CDEMO-FROM-TRANID` | `X(04)` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-FROM-PROGRAM` | `X(08)` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-TO-TRANID` | `X(04)` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-TO-PROGRAM` | `X(08)` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-USER-ID` | `X(08)` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-USER-TYPE` | `X(01)` | None | CDEMO-GENERAL-INFO |  |
| `88` | `CDEMO-USRTYP-ADMIN` | `None` | None | CDEMO-GENERAL-INFO |  |
| `88` | `CDEMO-USRTYP-USER` | `None` | None | CDEMO-GENERAL-INFO |  |
| `10` | `CDEMO-PGM-CONTEXT` | `9(01)` | None | CDEMO-GENERAL-INFO |  |
| `88` | `CDEMO-PGM-ENTER` | `None` | None | CDEMO-GENERAL-INFO |  |
| `88` | `CDEMO-PGM-REENTER` | `None` | None | CDEMO-GENERAL-INFO |  |
| `05` | `CDEMO-CUSTOMER-INFO` | `None` | None | CARDDEMO-COMMAREA |  |
| `10` | `CDEMO-CUST-ID` | `9(09)` | None | CDEMO-CUSTOMER-INFO |  |
| `10` | `CDEMO-CUST-FNAME` | `X(25)` | None | CDEMO-CUSTOMER-INFO |  |
| `10` | `CDEMO-CUST-MNAME` | `X(25)` | None | CDEMO-CUSTOMER-INFO |  |
| `10` | `CDEMO-CUST-LNAME` | `X(25)` | None | CDEMO-CUSTOMER-INFO |  |
| `05` | `CDEMO-ACCOUNT-INFO` | `None` | None | CARDDEMO-COMMAREA |  |
| `10` | `CDEMO-ACCT-ID` | `9(11)` | None | CDEMO-ACCOUNT-INFO |  |
| `10` | `CDEMO-ACCT-STATUS` | `X(01)` | None | CDEMO-ACCOUNT-INFO |  |
| `05` | `CDEMO-CARD-INFO` | `None` | None | CARDDEMO-COMMAREA |  |
| `10` | `CDEMO-CARD-NUM` | `9(16)` | None | CDEMO-CARD-INFO |  |
| `05` | `CDEMO-MORE-INFO` | `None` | None | CARDDEMO-COMMAREA |  |
| `10` | `CDEMO-LAST-MAP` | `X(7)` | None | CDEMO-MORE-INFO |  |
| `10` | `CDEMO-LAST-MAPSET` | `X(7)` | None | CDEMO-MORE-INFO |  |

### Copybook `COTTL01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CCDA-SCREEN-TITLE` | `None` | None | None |  |
| `05` | `CCDA-TITLE01` | `X(40)` | None | CCDA-SCREEN-TITLE |  |
| `05` | `CCDA-TITLE02` | `X(40)` | None | CCDA-SCREEN-TITLE |  |
| `05` | `CCDA-THANK-YOU` | `X(40)` | None | CCDA-SCREEN-TITLE |  |

### Copybook `COUSR01`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `COUSR1AI` | `None` | None | None |  |
| `02` | `TRNNAMEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `TRNNAMEF` | `X` | None | COUSR1AI |  |
| `03` | `TRNNAMEA` | `X` | None | COUSR1AI |  |
| `02` | `TRNNAMEI` | `X(4)` | None | COUSR1AI |  |
| `02` | `TITLE01L` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `TITLE01F` | `X` | None | COUSR1AI |  |
| `03` | `TITLE01A` | `X` | None | COUSR1AI |  |
| `02` | `TITLE01I` | `X(40)` | None | COUSR1AI |  |
| `02` | `CURDATEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `CURDATEF` | `X` | None | COUSR1AI |  |
| `03` | `CURDATEA` | `X` | None | COUSR1AI |  |
| `02` | `CURDATEI` | `X(8)` | None | COUSR1AI |  |
| `02` | `PGMNAMEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `PGMNAMEF` | `X` | None | COUSR1AI |  |
| `03` | `PGMNAMEA` | `X` | None | COUSR1AI |  |
| `02` | `PGMNAMEI` | `X(8)` | None | COUSR1AI |  |
| `02` | `TITLE02L` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `TITLE02F` | `X` | None | COUSR1AI |  |
| `03` | `TITLE02A` | `X` | None | COUSR1AI |  |
| `02` | `TITLE02I` | `X(40)` | None | COUSR1AI |  |
| `02` | `CURTIMEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `CURTIMEF` | `X` | None | COUSR1AI |  |
| `03` | `CURTIMEA` | `X` | None | COUSR1AI |  |
| `02` | `CURTIMEI` | `X(8)` | None | COUSR1AI |  |
| `02` | `FNAMEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `FNAMEF` | `X` | None | COUSR1AI |  |
| `03` | `FNAMEA` | `X` | None | COUSR1AI |  |
| `02` | `FNAMEI` | `X(20)` | None | COUSR1AI |  |
| `02` | `LNAMEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `LNAMEF` | `X` | None | COUSR1AI |  |
| `03` | `LNAMEA` | `X` | None | COUSR1AI |  |
| `02` | `LNAMEI` | `X(20)` | None | COUSR1AI |  |
| `02` | `USERIDL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `USERIDF` | `X` | None | COUSR1AI |  |
| `03` | `USERIDA` | `X` | None | COUSR1AI |  |
| `02` | `USERIDI` | `X(8)` | None | COUSR1AI |  |
| `02` | `PASSWDL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `PASSWDF` | `X` | None | COUSR1AI |  |
| `03` | `PASSWDA` | `X` | None | COUSR1AI |  |
| `02` | `PASSWDI` | `X(8)` | None | COUSR1AI |  |
| `02` | `USRTYPEL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `USRTYPEF` | `X` | None | COUSR1AI |  |
| `03` | `USRTYPEA` | `X` | None | COUSR1AI |  |
| `02` | `USRTYPEI` | `X(1)` | None | COUSR1AI |  |
| `02` | `ERRMSGL` | `S9(4)` | COMP | COUSR1AI |  |
| `02` | `ERRMSGF` | `X` | None | COUSR1AI |  |
| `03` | `ERRMSGA` | `X` | None | COUSR1AI |  |
| `02` | `ERRMSGI` | `X(78)` | None | COUSR1AI |  |
| `01` | `COUSR1AO` | `None` | None | None |  REDEFINES COUSR1AI |
*+ 60 more fields*
### Copybook `CSDAT01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `WS-DATE-TIME` | `None` | None | None |  |
| `05` | `WS-CURDATE-DATA` | `None` | None | WS-DATE-TIME |  |
| `10` | `WS-CURDATE` | `None` | None | WS-CURDATE-DATA |  |
| `15` | `WS-CURDATE-YEAR` | `9(04)` | None | WS-CURDATE |  |
| `15` | `WS-CURDATE-MONTH` | `9(02)` | None | WS-CURDATE |  |
| `15` | `WS-CURDATE-DAY` | `9(02)` | None | WS-CURDATE |  |
| `10` | `WS-CURDATE-N` | `9(08)` | None | WS-CURDATE-DATA |  REDEFINES WS-CURDATE |
| `10` | `WS-CURTIME` | `None` | None | WS-CURDATE-DATA |  |
| `15` | `WS-CURTIME-HOURS` | `9(02)` | None | WS-CURTIME |  |
| `15` | `WS-CURTIME-MINUTE` | `9(02)` | None | WS-CURTIME |  |
| `15` | `WS-CURTIME-SECOND` | `9(02)` | None | WS-CURTIME |  |
| `15` | `WS-CURTIME-MILSEC` | `9(02)` | None | WS-CURTIME |  |
| `10` | `WS-CURTIME-N` | `9(08)` | None | WS-CURDATE-DATA |  REDEFINES WS-CURTIME |
| `05` | `WS-CURDATE-MM-DD-YY` | `None` | None | WS-DATE-TIME |  |
| `10` | `WS-CURDATE-MM` | `9(02)` | None | WS-CURDATE-MM-DD-YY |  |
| `10` | `WS-CURDATE-DD` | `9(02)` | None | WS-CURDATE-MM-DD-YY |  |
| `10` | `WS-CURDATE-YY` | `9(02)` | None | WS-CURDATE-MM-DD-YY |  |
| `05` | `WS-CURTIME-HH-MM-SS` | `None` | None | WS-DATE-TIME |  |
| `10` | `WS-CURTIME-HH` | `9(02)` | None | WS-CURTIME-HH-MM-SS |  |
| `10` | `WS-CURTIME-MM` | `9(02)` | None | WS-CURTIME-HH-MM-SS |  |
| `10` | `WS-CURTIME-SS` | `9(02)` | None | WS-CURTIME-HH-MM-SS |  |
| `05` | `WS-TIMESTAMP` | `None` | None | WS-DATE-TIME |  |
| `10` | `WS-TIMESTAMP-DT-YYYY` | `9(04)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-DT-MM` | `9(02)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-DT-DD` | `9(02)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-TM-HH` | `9(02)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-TM-MM` | `9(02)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-TM-SS` | `9(02)` | None | WS-TIMESTAMP |  |
| `10` | `WS-TIMESTAMP-TM-MS6` | `9(06)` | None | WS-TIMESTAMP |  |

### Copybook `CSMSG01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CCDA-COMMON-MESSAGES` | `None` | None | None |  |
| `05` | `CCDA-MSG-THANK-YOU` | `X(50)` | None | CCDA-COMMON-MESSAGES |  |
| `05` | `CCDA-MSG-INVALID-KEY` | `X(50)` | None | CCDA-COMMON-MESSAGES |  |

### Copybook `CSUSR01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `SEC-USER-DATA` | `None` | None | None |  |
| `05` | `SEC-USR-ID` | `X(08)` | None | SEC-USER-DATA |  |
| `05` | `SEC-USR-FNAME` | `X(20)` | None | SEC-USER-DATA |  |
| `05` | `SEC-USR-LNAME` | `X(20)` | None | SEC-USER-DATA |  |
| `05` | `SEC-USR-PWD` | `X(08)` | None | SEC-USER-DATA |  |
| `05` | `SEC-USR-TYPE` | `X(01)` | None | SEC-USER-DATA |  |
| `05` | `SEC-USR-FILLER` | `X(23)` | None | SEC-USER-DATA |  |

### Copybook `DFHAID`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `DFHAID` | `None` | None | None |  |
| `02` | `DFHENTER` | `X` | None | DFHAID |  |
| `02` | `DFHCLEAR` | `X` | None | DFHAID |  |
| `02` | `DFHCLRP` | `X` | None | DFHAID |  |
| `02` | `DFHPA1` | `X` | None | DFHAID |  |
| `02` | `DFHPA2` | `X` | None | DFHAID |  |
| `02` | `DFHPA3` | `X` | None | DFHAID |  |
| `02` | `DFHPF1` | `X` | None | DFHAID |  |
| `02` | `DFHPF2` | `X` | None | DFHAID |  |
| `02` | `DFHPF3` | `X` | None | DFHAID |  |
| `02` | `DFHPF4` | `X` | None | DFHAID |  |
| `02` | `DFHPF5` | `X` | None | DFHAID |  |
| `02` | `DFHPF6` | `X` | None | DFHAID |  |
| `02` | `DFHPF7` | `X` | None | DFHAID |  |
| `02` | `DFHPF8` | `X` | None | DFHAID |  |
| `02` | `DFHPF9` | `X` | None | DFHAID |  |
| `02` | `DFHPF10` | `X` | None | DFHAID |  |
| `02` | `DFHPF11` | `X` | None | DFHAID |  |
| `02` | `DFHPF12` | `X` | None | DFHAID |  |
| `02` | `DFHPF13` | `X` | None | DFHAID |  |
| `02` | `DFHPF14` | `X` | None | DFHAID |  |
| `02` | `DFHPF15` | `X` | None | DFHAID |  |
| `02` | `DFHPF16` | `X` | None | DFHAID |  |
| `02` | `DFHPF17` | `X` | None | DFHAID |  |
| `02` | `DFHPF18` | `X` | None | DFHAID |  |
| `02` | `DFHPF19` | `X` | None | DFHAID |  |
| `02` | `DFHPF20` | `X` | None | DFHAID |  |
| `02` | `DFHPF21` | `X` | None | DFHAID |  |
| `02` | `DFHPF22` | `X` | None | DFHAID |  |
| `02` | `DFHPF23` | `X` | None | DFHAID |  |
| `02` | `DFHPF24` | `X` | None | DFHAID |  |
| `02` | `DFHPEN` | `X` | None | DFHAID |  |
| `02` | `DFHOPID` | `X` | None | DFHAID |  |
| `02` | `DFHMSRE` | `X` | None | DFHAID |  |
| `02` | `DFHSTRF` | `X` | None | DFHAID |  |
| `02` | `DFHTRIG` | `X` | None | DFHAID |  |

### Copybook `DFHBMSCA`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `DFHBMSCA` | `None` | None | None |  |
| `02` | `DFHBMPEM` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMPNL` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMASK` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMUNP` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMUNN` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMPRO` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMBRY` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMDAR` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMFSE` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMPRF` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMASF` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMASB` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMEOF` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBMEC` | `X` | None | DFHBMSCA |  |
| `02` | `DFHSA` | `X` | None | DFHBMSCA |  |
| `02` | `DFHCOLOR` | `X` | None | DFHBMSCA |  |
| `02` | `DFHPS` | `X` | None | DFHBMSCA |  |
| `02` | `DFHHLT` | `X` | None | DFHBMSCA |  |
| `02` | `DFHVAL` | `X` | None | DFHBMSCA |  |
| `02` | `DFHOUTLN` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBKTRN` | `X` | None | DFHBMSCA |  |
| `02` | `DFHALL` | `X` | None | DFHBMSCA |  |
| `02` | `DFHERROR` | `X` | None | DFHBMSCA |  |
| `02` | `DFHDFT` | `X` | None | DFHBMSCA |  |
| `02` | `DFHDFCOL` | `X` | None | DFHBMSCA |  |
| `02` | `DFHBLUE` | `X` | None | DFHBMSCA |  |
| `02` | `DFHRED` | `X` | None | DFHBMSCA |  |
| `02` | `DFHPINK` | `X` | None | DFHBMSCA |  |
| `02` | `DFHGREEN` | `X` | None | DFHBMSCA |  |
| `02` | `DFHTURQ` | `X` | None | DFHBMSCA |  |
| `02` | `DFHYELLO` | `X` | None | DFHBMSCA |  |
| `02` | `DFHWHTE` | `X` | None | DFHBMSCA |  |
| `02` | `CATTR-H-UNPROT` | `X` | None | DFHBMSCA |  |
| `02` | `CATTR-H-UNPROT-FSET` | `X` | None | DFHBMSCA |  |
| `02` | `CATTR-H-UNPROT-NUM` | `X` | None | DFHBMSCA |  |
| `02` | `CATTR-H-ASKIP` | `X` | None | DFHBMSCA |  |



## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
| `SPACES` | `WS-MESSAGE` | MAIN-PARA | 75 |
| `'COSGN00C'` | `CDEMO-TO-PROGRAM` | MAIN-PARA | 79 |
| `DFHCOMMAREA(1:EIBCALEN)` | `CARDDEMO-COMMAREA` | MAIN-PARA | 82 |
| `LOW-VALUES` | `COUSR1AO` | MAIN-PARA | 85 |
| `'-1'` | `FNAMEL` | MAIN-PARA | 86 |
| `'-1'` | `OF` | MAIN-PARA | 86 |
| `'-1'` | `COUSR1AI` | MAIN-PARA | 86 |
| `'COADM01C'` | `CDEMO-TO-PROGRAM` | MAIN-PARA | 94 |
| `'Y'` | `WS-ERR-FLG` | MAIN-PARA | 99 |
| `'-1'` | `FNAMEL` | MAIN-PARA | 100 |
| `'-1'` | `OF` | MAIN-PARA | 100 |
| `'-1'` | `COUSR1AI` | MAIN-PARA | 100 |
| `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | MAIN-PARA | 101 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 119 |
| `'-1'` | `FNAMEL` | PROCESS-ENTER-KEY | 122 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 122 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 122 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 125 |
| `'-1'` | `LNAMEL` | PROCESS-ENTER-KEY | 128 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 128 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 128 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 131 |
| `'-1'` | `USERIDL` | PROCESS-ENTER-KEY | 134 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 134 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 134 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 137 |
| `'-1'` | `PASSWDL` | PROCESS-ENTER-KEY | 140 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 140 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 140 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 143 |
| `'-1'` | `USRTYPEL` | PROCESS-ENTER-KEY | 146 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 146 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 146 |
| `'-1'` | `FNAMEL` | PROCESS-ENTER-KEY | 149 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 149 |
| `'-1'` | `COUSR1AI` | PROCESS-ENTER-KEY | 149 |
| `'COSGN00C'` | `CDEMO-TO-PROGRAM` | RETURN-TO-PREV-SCREEN | 168 |
| `WS-TRANID` | `CDEMO-FROM-TRANID` | RETURN-TO-PREV-SCREEN | 170 |
| `WS-PGMNAME` | `CDEMO-FROM-PROGRAM` | RETURN-TO-PREV-SCREEN | 171 |
| `ZEROS` | `CDEMO-PGM-CONTEXT` | RETURN-TO-PREV-SCREEN | 174 |
| `WS-MESSAGE` | `ERRMSGO` | SEND-USRADD-SCREEN | 188 |
| `WS-MESSAGE` | `OF` | SEND-USRADD-SCREEN | 188 |
| `WS-MESSAGE` | `COUSR1AO` | SEND-USRADD-SCREEN | 188 |
| `CCDA-TITLE01` | `TITLE01O` | POPULATE-HEADER-INFO | 218 |
| `CCDA-TITLE01` | `OF` | POPULATE-HEADER-INFO | 218 |
| `CCDA-TITLE01` | `COUSR1AO` | POPULATE-HEADER-INFO | 218 |
| `CCDA-TITLE02` | `TITLE02O` | POPULATE-HEADER-INFO | 219 |
| `CCDA-TITLE02` | `OF` | POPULATE-HEADER-INFO | 219 |
| `CCDA-TITLE02` | `COUSR1AO` | POPULATE-HEADER-INFO | 219 |
| `WS-TRANID` | `TRNNAMEO` | POPULATE-HEADER-INFO | 220 |
| `WS-TRANID` | `OF` | POPULATE-HEADER-INFO | 220 |
| `WS-TRANID` | `COUSR1AO` | POPULATE-HEADER-INFO | 220 |
| `WS-PGMNAME` | `PGMNAMEO` | POPULATE-HEADER-INFO | 221 |
| `WS-PGMNAME` | `OF` | POPULATE-HEADER-INFO | 221 |
| `WS-PGMNAME` | `COUSR1AO` | POPULATE-HEADER-INFO | 221 |
| `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | POPULATE-HEADER-INFO | 223 |
| `WS-CURDATE-DAY` | `WS-CURDATE-DD` | POPULATE-HEADER-INFO | 224 |
| `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | POPULATE-HEADER-INFO | 225 |
| `WS-CURDATE-MM-DD-YY` | `CURDATEO` | POPULATE-HEADER-INFO | 227 |
| `WS-CURDATE-MM-DD-YY` | `OF` | POPULATE-HEADER-INFO | 227 |
*+ 25 more movements*

## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEAD_CODE | Variable `LK-COMMAREA` is declared but never referenced | None | 64 |

### NOTICE — Variable `LK-COMMAREA` is declared but never referenced

`LK-COMMAREA` is declared at line 64 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 64):
```cobol
05  LK-COMMAREA                           PIC X(01)
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---




## Decision Tables (EVALUATE / WHEN)

Captured from the source. Each EVALUATE block is a structured decision the
migration team should turn into either a switch / pattern-match or a rules table.

### EVALUATE `TRUE` — paragraph `PROCESS-ENTER-KEY` (line 148)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE -1       TO FNAMEL OF COUSR1AI |
| `FNAMEI OF COUSR1AI = SPACES OR LOW-VALUES` | MOVE 'Y'     TO WS-ERR-FLG |
| `LNAMEI OF COUSR1AI = SPACES OR LOW-VALUES` | MOVE 'Y'     TO WS-ERR-FLG |
| `USERIDI OF COUSR1AI = SPACES OR LOW-VALUES` | MOVE 'Y'     TO WS-ERR-FLG |
| `PASSWDI OF COUSR1AI = SPACES OR LOW-VALUES` | MOVE 'Y'     TO WS-ERR-FLG |
| `USRTYPEI OF COUSR1AI = SPACES OR LOW-VALUES` | MOVE 'Y'     TO WS-ERR-FLG |

### EVALUATE `WS-RESP-CD` — paragraph `WRITE-USER-SEC-FILE` (line 267)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE 'Y'     TO WS-ERR-FLG |
| `DFHRESP(NORMAL)` | PERFORM INITIALIZE-ALL-FIELDS |
| `DFHRESP(DUPKEY)` |  |
| `DFHRESP(DUPREC)` | MOVE 'Y'     TO WS-ERR-FLG |

### EVALUATE `EIBAID` — paragraph `MAIN-PARA` (line 98)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE 'Y'                       TO WS-ERR-FLG |
| `DFHENTER` | PERFORM PROCESS-ENTER-KEY |
| `DFHPF3` | MOVE 'COADM01C' TO CDEMO-TO-PROGRAM |
| `DFHPF4` | PERFORM CLEAR-CURRENT-SCREEN |




## CICS Commands

This program uses the following EXEC CICS commands:

| Command | Paragraph | Line | Details |
|---------|-----------|------|---------|
| `RETURN` | MAIN-PARA | 107 | {"details": {"transid": "WS-TRANID", "commarea": "CARDDEMO-COMMAREA"}} |
| `XCTL` | RETURN-TO-PREV-SCREEN | 175 | {"details": {"program": "CDEMO-TO-PROGRAM", "commarea": "CARDDEMO-COMMAREA"}} |
| `SEND` | SEND-USRADD-SCREEN | 190 | {"details": {"map": "COUSR1A", "mapset": "COUSR01", "from": "COUSR1AO"}} |
| `RECEIVE` | RECEIVE-USRADD-SCREEN | 203 | {"details": {"map": "COUSR1A", "mapset": "COUSR01", "into": "COUSR1AI", "resp": ... |
| `WRITE` | WRITE-USER-SEC-FILE | 240 | {"details": {"dataset": "WS-USRSEC-FILE", "from": "SEC-USER-DATA", "length": "LE... |

**Summary:** 5 CICS command(s) — RETURN (1), XCTL (1), SEND (1), RECEIVE (1), WRITE (1)

## CICS Screen Workflow Notes

These notes are derived directly from the COBOL source and BMS map usage. They are intended
to prevent migration errors where a PF key label is mistaken for the full transaction flow.

### Program transfers use XCTL, not a soft return

`EXEC CICS XCTL` transfers control to another program and does not return to the current program like a subroutine call. Document PF-key navigation that reaches this paragraph as a CICS transfer, not as an in-place screen redisplay.

Evidence:
- L175 in `RETURN-TO-PREV-SCREEN`: EXEC CICS XCTL {"details": {"program": "CDEMO-TO-PROGRAM", "commarea": "CARDDEMO-COMMAREA"}}

### Initial entry without COMMAREA transfers to sign-on

When `EIBCALEN = 0`, this program prepares `COSGN00C` as the target and follows the return/transfer path. It does not display its own BMS map on that entry path.

Evidence:
- L78: `IF EIBCALEN = 0`
- L79: `MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM`
- L168: `MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM`
- L175 in `RETURN-TO-PREV-SCREEN`: EXEC CICS XCTL {"details": {"program": "CDEMO-TO-PROGRAM", "commarea": "CARDDEMO-COMMAREA"}}

### PF3 navigation resolves through RETURN-TO-PREV-SCREEN

PF3 selects the `RETURN-TO-PREV-SCREEN` path. That paragraph ends in `EXEC CICS XCTL`, so PF3 is a transfer to the target program held in the COMMAREA routing fields.

Evidence:
- L93: `WHEN DFHPF3`
- L80: `PERFORM RETURN-TO-PREV-SCREEN`
- L95: `PERFORM RETURN-TO-PREV-SCREEN`
- L175 in `RETURN-TO-PREV-SCREEN`: EXEC CICS XCTL {"details": {"program": "CDEMO-TO-PROGRAM", "commarea": "CARDDEMO-COMMAREA"}}

### Error/message text is written to the BMS output field

`ERRMSGI` exists in the input copybook area, but this program displays messages by moving `WS-MESSAGE` to `ERRMSGO OF COUSR3AO`. Documentation should refer to `ERRMSGO` when describing rendered error or status messages.

Evidence:
- L188: `MOVE WS-MESSAGE TO ERRMSGO OF COUSR1AO`

### ERR-FLG is reset at the start of each run

`ERR-FLG` starts each invocation on the off path via `SET ERR-FLG-OFF TO TRUE`. Validation and file-error branches set or test `ERR-FLG-ON` to stop later processing.

Evidence:
- L73: `SET ERR-FLG-OFF TO TRUE`
- L41: `88 ERR-FLG-ON                         VALUE 'Y'.`
- L153: `IF NOT ERR-FLG-ON`

### The BMS map can be sent from multiple paths

Screen output is centralized in the send paragraph, but several routines can perform it. If a read routine sends the map and its caller also sends the map, a modern UI migration must preserve or deliberately remove that duplicate response behavior.

Evidence:
- L87: `MAIN-PARA` performs `SEND-USRADD-SCREEN`
- L102: `MAIN-PARA` performs `SEND-USRADD-SCREEN`
- L123: `PROCESS-ENTER-KEY` performs `SEND-USRADD-SCREEN`
- L129: `PROCESS-ENTER-KEY` performs `SEND-USRADD-SCREEN`
- L135: `PROCESS-ENTER-KEY` performs `SEND-USRADD-SCREEN`
- L141: `PROCESS-ENTER-KEY` performs `SEND-USRADD-SCREEN`
- L147: `PROCESS-ENTER-KEY` performs `SEND-USRADD-SCREEN`
- L259: `WRITE-USER-SEC-FILE` performs `SEND-USRADD-SCREEN`
- L190 in `SEND-USRADD-SCREEN`: EXEC CICS SEND {"details": {"map": "COUSR1A", "mapset": "COUSR01", "from": "COUSR1AO"}}


## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Invalid Security Level** `BR-414`  
  If the entered security level is not valid, the user will be notified and must re-enter a valid security level.  
  [View Rule Details](../business-rules/BR-414.md)
- **Invalid User ID** `BR-415`  
  If the entered User ID is invalid, the user will be notified and must re-enter a valid User ID.  
  [View Rule Details](../business-rules/BR-415.md)
- **User ID Format Check** `BR-416`  
  The system validates the format of the entered User ID.  
  [View Rule Details](../business-rules/BR-416.md)
- **Password Complexity Check** `BR-417`  
  The system enforces password complexity rules when a new password is created.  
  [View Rule Details](../business-rules/BR-417.md)
- **Security Profile Authorization** `BR-418`  
  The system verifies if the user initiating the creation of a new user has the necessary permissions.  
  [View Rule Details](../business-rules/BR-418.md)
- **Clear Screen and Return** `BR-419`  
  After processing, the system clears the input screen and returns the user to the previous screen.  
  [View Rule Details](../business-rules/BR-419.md)
- **Invalid Security Level** `BR-420`  
  If the entered security level is not valid, display an error message.  
  [View Rule Details](../business-rules/BR-420.md)

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `WS-VARIABLES` | 1 | `None` | WORKING-STORAGE | None |
| `WS-PGMNAME` | 5 | `X(08)` | WORKING-STORAGE | None |
| `WS-TRANID` | 5 | `X(04)` | WORKING-STORAGE | None |
| `WS-MESSAGE` | 5 | `X(80)` | WORKING-STORAGE | None |
| `WS-USRSEC-FILE` | 5 | `X(08)` | WORKING-STORAGE | None |
| `WS-ERR-FLG` | 5 | `X(01)` | WORKING-STORAGE | None |
| `ERR-FLG-ON` | 88 | `None` | WORKING-STORAGE | None |
| `ERR-FLG-OFF` | 88 | `None` | WORKING-STORAGE | None |
| `WS-RESP-CD` | 5 | `S9(09)` | WORKING-STORAGE | None |
| `WS-REAS-CD` | 5 | `S9(09)` | WORKING-STORAGE | None |
| `CARDDEMO-COMMAREA` | 1 | `None` | WORKING-STORAGE | None |
| `CDEMO-GENERAL-INFO` | 5 | `None` | WORKING-STORAGE | None |
| `CDEMO-FROM-TRANID` | 10 | `X(04)` | WORKING-STORAGE | None |
| `CDEMO-FROM-PROGRAM` | 10 | `X(08)` | WORKING-STORAGE | None |
| `CDEMO-TO-TRANID` | 10 | `X(04)` | WORKING-STORAGE | None |
| `CDEMO-TO-PROGRAM` | 10 | `X(08)` | WORKING-STORAGE | None |
| `CDEMO-USER-ID` | 10 | `X(08)` | WORKING-STORAGE | None |
| `CDEMO-USER-TYPE` | 10 | `X(01)` | WORKING-STORAGE | None |
| `CDEMO-USRTYP-ADMIN` | 88 | `None` | WORKING-STORAGE | None |
| `CDEMO-USRTYP-USER` | 88 | `None` | WORKING-STORAGE | None |
| `CDEMO-PGM-CONTEXT` | 10 | `9(01)` | WORKING-STORAGE | None |
| `CDEMO-PGM-ENTER` | 88 | `None` | WORKING-STORAGE | None |
| `CDEMO-PGM-REENTER` | 88 | `None` | WORKING-STORAGE | None |
| `CDEMO-CUSTOMER-INFO` | 5 | `None` | WORKING-STORAGE | None |
| `CDEMO-CUST-ID` | 10 | `9(09)` | WORKING-STORAGE | None |
| `CDEMO-CUST-FNAME` | 10 | `X(25)` | WORKING-STORAGE | None |
| `CDEMO-CUST-MNAME` | 10 | `X(25)` | WORKING-STORAGE | None |
| `CDEMO-CUST-LNAME` | 10 | `X(25)` | WORKING-STORAGE | None |
| `CDEMO-ACCOUNT-INFO` | 5 | `None` | WORKING-STORAGE | None |
| `CDEMO-ACCT-ID` | 10 | `9(11)` | WORKING-STORAGE | None |
| `CDEMO-ACCT-STATUS` | 10 | `X(01)` | WORKING-STORAGE | None |
| `CDEMO-CARD-INFO` | 5 | `None` | WORKING-STORAGE | None |
| `CDEMO-CARD-NUM` | 10 | `9(16)` | WORKING-STORAGE | None |
| `CDEMO-MORE-INFO` | 5 | `None` | WORKING-STORAGE | None |
| `CDEMO-LAST-MAP` | 10 | `X(7)` | WORKING-STORAGE | None |
| `CDEMO-LAST-MAPSET` | 10 | `X(7)` | WORKING-STORAGE | None |
| `COUSR1AI` | 1 | `None` | WORKING-STORAGE | None |
| `FILLER` | 2 | `X(12)` | WORKING-STORAGE | None |
| `TRNNAMEL` | 2 | `S9(4)` | WORKING-STORAGE | None |
| `TRNNAMEF` | 2 | `X` | WORKING-STORAGE | None |

*Showing 40 of 312 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-05-12 12:18*