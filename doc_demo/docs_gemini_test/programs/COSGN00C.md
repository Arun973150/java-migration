# Program: COSGN00C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COSGN00C` |
| Type | ONLINE |
| Lines | 261 |
| Source | [COSGN00C.cbl](../carddemo/COSGN00C.cbl#L1) |
| Paragraphs | 6 |
| Statements | 34 |
| Impact Risk | **HIGH** — 20 programs affected |

> **View Source:** [Open COSGN00C.cbl](../carddemo/COSGN00C.cbl#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-PGMNAME` | `COSGN00C` |
| `WS-TRANID` | `CC00` |
| `WS-USRSEC-FILE` | `USRSEC` |
| `WS-ERR-FLG` | `N` |


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **COSGN00C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COSGN00C (Callers)

*No programs call COSGN00C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COSGN00C (Callees)

*COSGN00C does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `COCOM01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `COSGN00` |  | 0 |
| `COTTL01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
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

#### `COSGN00` as `COSGN0AI`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `COSGN0AI` | Cosgn0Ai | `GROUP` | `OBJECT` |  |
| `COSGN0AO` | Cosgn0Ao | `GROUP` | `OBJECT` |  |

#### `COTTL01Y` as `CCDA-SCREEN-TITLE`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CCDA-SCREEN-TITLE` | Ccda Screen Title | `GROUP` | `OBJECT` |  |
| `CCDA-TITLE01` | Ccda Title01 | `PIC X(40)` | `STRING(40)` |  |
| `CCDA-TITLE02` | Ccda Title02 | `PIC X(40)` | `STRING(40)` |  |
| `CCDA-THANK-YOU` | Ccda Thank You | `PIC X(40)` | `STRING(40)` |  |

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
| 77 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |
| 89 | `CCDA-MSG-THANK-YOU` | `WS-MESSAGE` | CCDA-MSG-THANK-YOU populates WS-MESSAGE |
| 93 | `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | CCDA-MSG-INVALID-KEY populates WS-MESSAGE |
| 120 | `'Please enter User ID ...'` | `WS-MESSAGE` | 'Please enter User ID ...' populates WS-MESSAGE |
| 125 | `'Please enter Password ...'` | `WS-MESSAGE` | 'Please enter Password ...' populates WS-MESSAGE |
| 149 | `WS-MESSAGE` | `ERRMSGO OF COSGN0AO` | WS-MESSAGE populates ERRMSGO OF COSGN0AO |
| 179 | `FUNCTION CURRENT-DATE` | `WS-CURDATE-DATA` | FUNCTION CURRENT-DATE populates WS-CURDATE-DATA |
| 186 | `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | WS-CURDATE-MONTH populates WS-CURDATE-MM |
| 187 | `WS-CURDATE-DAY` | `WS-CURDATE-DD` | WS-CURDATE-DAY populates WS-CURDATE-DD |
| 188 | `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | WS-CURDATE-YEAR(3:2) populates WS-CURDATE-YY |
| 190 | `WS-CURDATE-MM-DD-YY` | `CURDATEO OF COSGN0AO` | WS-CURDATE-MM-DD-YY populates CURDATEO OF COSGN0AO |
| 249 | `'User not found. Try again ...'` | `WS-MESSAGE` | 'User not found. Try again ...' populates WS-MESSAGE |



---

## Dependency Graph

```mermaid
flowchart TD
    COSGN00C["⬤ COSGN00C"]:::target
    CB_COCOM01Y{{"COCOM01Y"}}:::copybook
    COSGN00C -.- CB_COCOM01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COCOM01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COCOM01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COCOM01Y -.- COADM01C
    CB_COTTL01Y{{"COTTL01Y"}}:::copybook
    COSGN00C -.- CB_COTTL01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COTTL01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COTTL01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COTTL01Y -.- COADM01C
    CB_CSDAT01Y{{"CSDAT01Y"}}:::copybook
    COSGN00C -.- CB_CSDAT01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSDAT01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSDAT01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSDAT01Y -.- COADM01C
    CB_CSMSG01Y{{"CSMSG01Y"}}:::copybook
    COSGN00C -.- CB_CSMSG01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSMSG01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSMSG01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSMSG01Y -.- COADM01C
    CB_CSUSR01Y{{"CSUSR01Y"}}:::copybook
    COSGN00C -.- CB_CSUSR01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSUSR01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSUSR01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSUSR01Y -.- COADM01C
    CB_DFHAID{{"DFHAID"}}:::copybook
    COSGN00C -.- CB_DFHAID
    COACTUPC["COACTUPC"]:::coupled
    CB_DFHAID -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_DFHAID -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_DFHAID -.- COADM01C
    CB_DFHBMSCA{{"DFHBMSCA"}}:::copybook
    COSGN00C -.- CB_DFHBMSCA
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

> **If you change COSGN00C, what else could break?**

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
- `COTRN00C`
- `COTRN01C`
- `COTRN02C`
- `COTRTLIC`
- `COTRTUPC`
- `COUSR00C`
- `COUSR01C`
- `COUSR02C`
- `COUSR03C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| MOVE | 17 |
| EXEC_CICS | 7 |
| IF | 6 |
| EVALUATE | 2 |
| SET | 1 |
| PERFORM | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN_PARA["MAIN-PARA"]
    PROCESS_ENTER_KEY["PROCESS-ENTER-KEY"]
    SEND_SIGNON_SCREEN["SEND-SIGNON-SCREEN"]
    SEND_PLAIN_TEXT["SEND-PLAIN-TEXT"]
    POPULATE_HEADER_INFO["POPULATE-HEADER-INFO"]
    READ_USER_SEC_FILE["READ-USER-SEC-FILE"]
    START --> MAIN_PARA
    MAIN_PARA --> SEND_SIGNON_SCREEN
    MAIN_PARA --> PROCESS_ENTER_KEY
    MAIN_PARA --> SEND_PLAIN_TEXT
    PROCESS_ENTER_KEY --> SEND_SIGNON_SCREEN
    PROCESS_ENTER_KEY --> READ_USER_SEC_FILE
    SEND_SIGNON_SCREEN --> POPULATE_HEADER_INFO
    READ_USER_SEC_FILE --> SEND_SIGNON_SCREEN
    SEND_SIGNON_SCREEN --> INLINE
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 73 - 107 |
| **View Code** | [Jump to Line 73](../carddemo/COSGN00C.cbl#L73) |



### PROCESS-ENTER-KEY

| | |
|---|---|
| **Paragraph** | `PROCESS-ENTER-KEY` |
| **Lines** | 108 - 144 |
| **View Code** | [Jump to Line 108](../carddemo/COSGN00C.cbl#L108) |



### SEND-SIGNON-SCREEN

| | |
|---|---|
| **Paragraph** | `SEND-SIGNON-SCREEN` |
| **Lines** | 145 - 161 |
| **View Code** | [Jump to Line 145](../carddemo/COSGN00C.cbl#L145) |



### SEND-PLAIN-TEXT

| | |
|---|---|
| **Paragraph** | `SEND-PLAIN-TEXT` |
| **Lines** | 162 - 176 |
| **View Code** | [Jump to Line 162](../carddemo/COSGN00C.cbl#L162) |



### POPULATE-HEADER-INFO

| | |
|---|---|
| **Paragraph** | `POPULATE-HEADER-INFO` |
| **Lines** | 177 - 208 |
| **View Code** | [Jump to Line 177](../carddemo/COSGN00C.cbl#L177) |



### READ-USER-SEC-FILE

| | |
|---|---|
| **Paragraph** | `READ-USER-SEC-FILE` |
| **Lines** | 209 - 260 |
| **View Code** | [Jump to Line 209](../carddemo/COSGN00C.cbl#L209) |







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

### Copybook `COSGN00`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `COSGN0AI` | `None` | None | None |  |
| `02` | `TRNNAMEL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `TRNNAMEF` | `X` | None | COSGN0AI |  |
| `03` | `TRNNAMEA` | `X` | None | COSGN0AI |  |
| `02` | `TRNNAMEI` | `X(4)` | None | COSGN0AI |  |
| `02` | `TITLE01L` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `TITLE01F` | `X` | None | COSGN0AI |  |
| `03` | `TITLE01A` | `X` | None | COSGN0AI |  |
| `02` | `TITLE01I` | `X(40)` | None | COSGN0AI |  |
| `02` | `CURDATEL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `CURDATEF` | `X` | None | COSGN0AI |  |
| `03` | `CURDATEA` | `X` | None | COSGN0AI |  |
| `02` | `CURDATEI` | `X(8)` | None | COSGN0AI |  |
| `02` | `PGMNAMEL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `PGMNAMEF` | `X` | None | COSGN0AI |  |
| `03` | `PGMNAMEA` | `X` | None | COSGN0AI |  |
| `02` | `PGMNAMEI` | `X(8)` | None | COSGN0AI |  |
| `02` | `TITLE02L` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `TITLE02F` | `X` | None | COSGN0AI |  |
| `03` | `TITLE02A` | `X` | None | COSGN0AI |  |
| `02` | `TITLE02I` | `X(40)` | None | COSGN0AI |  |
| `02` | `CURTIMEL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `CURTIMEF` | `X` | None | COSGN0AI |  |
| `03` | `CURTIMEA` | `X` | None | COSGN0AI |  |
| `02` | `CURTIMEI` | `X(9)` | None | COSGN0AI |  |
| `02` | `APPLIDL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `APPLIDF` | `X` | None | COSGN0AI |  |
| `03` | `APPLIDA` | `X` | None | COSGN0AI |  |
| `02` | `APPLIDI` | `X(8)` | None | COSGN0AI |  |
| `02` | `SYSIDL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `SYSIDF` | `X` | None | COSGN0AI |  |
| `03` | `SYSIDA` | `X` | None | COSGN0AI |  |
| `02` | `SYSIDI` | `X(8)` | None | COSGN0AI |  |
| `02` | `USERIDL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `USERIDF` | `X` | None | COSGN0AI |  |
| `03` | `USERIDA` | `X` | None | COSGN0AI |  |
| `02` | `USERIDI` | `X(8)` | None | COSGN0AI |  |
| `02` | `PASSWDL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `PASSWDF` | `X` | None | COSGN0AI |  |
| `03` | `PASSWDA` | `X` | None | COSGN0AI |  |
| `02` | `PASSWDI` | `X(8)` | None | COSGN0AI |  |
| `02` | `ERRMSGL` | `S9(4)` | COMP | COSGN0AI |  |
| `02` | `ERRMSGF` | `X` | None | COSGN0AI |  |
| `03` | `ERRMSGA` | `X` | None | COSGN0AI |  |
| `02` | `ERRMSGI` | `X(78)` | None | COSGN0AI |  |
| `01` | `COSGN0AO` | `None` | None | None |  REDEFINES COSGN0AI |
| `02` | `TRNNAMEC` | `X` | None | COSGN0AO |  |
| `02` | `TRNNAMEP` | `X` | None | COSGN0AO |  |
| `02` | `TRNNAMEH` | `X` | None | COSGN0AO |  |
| `02` | `TRNNAMEV` | `X` | None | COSGN0AO |  |
*+ 51 more fields*
### Copybook `COTTL01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CCDA-SCREEN-TITLE` | `None` | None | None |  |
| `05` | `CCDA-TITLE01` | `X(40)` | None | CCDA-SCREEN-TITLE |  |
| `05` | `CCDA-TITLE02` | `X(40)` | None | CCDA-SCREEN-TITLE |  |
| `05` | `CCDA-THANK-YOU` | `X(40)` | None | CCDA-SCREEN-TITLE |  |

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
| `SPACES` | `WS-MESSAGE` | MAIN-PARA | 77 |
| `LOW-VALUES` | `COSGN0AO` | MAIN-PARA | 81 |
| `'-1'` | `USERIDL` | MAIN-PARA | 82 |
| `'-1'` | `OF` | MAIN-PARA | 82 |
| `'-1'` | `COSGN0AI` | MAIN-PARA | 82 |
| `CCDA-MSG-THANK-YOU` | `WS-MESSAGE` | MAIN-PARA | 89 |
| `'Y'` | `WS-ERR-FLG` | MAIN-PARA | 92 |
| `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | MAIN-PARA | 93 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 119 |
| `'Please enter User ID ...'` | `WS-MESSAGE` | PROCESS-ENTER-KEY | 120 |
| `'-1'` | `USERIDL` | PROCESS-ENTER-KEY | 121 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 121 |
| `'-1'` | `COSGN0AI` | PROCESS-ENTER-KEY | 121 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 124 |
| `'Please enter Password ...'` | `WS-MESSAGE` | PROCESS-ENTER-KEY | 125 |
| `'-1'` | `PASSWDL` | PROCESS-ENTER-KEY | 126 |
| `'-1'` | `OF` | PROCESS-ENTER-KEY | 126 |
| `'-1'` | `COSGN0AI` | PROCESS-ENTER-KEY | 126 |
| `WS-MESSAGE` | `ERRMSGO` | SEND-SIGNON-SCREEN | 149 |
| `WS-MESSAGE` | `OF` | SEND-SIGNON-SCREEN | 149 |
| `WS-MESSAGE` | `COSGN0AO` | SEND-SIGNON-SCREEN | 149 |
| `CCDA-TITLE01` | `TITLE01O` | POPULATE-HEADER-INFO | 181 |
| `CCDA-TITLE01` | `OF` | POPULATE-HEADER-INFO | 181 |
| `CCDA-TITLE01` | `COSGN0AO` | POPULATE-HEADER-INFO | 181 |
| `CCDA-TITLE02` | `TITLE02O` | POPULATE-HEADER-INFO | 182 |
| `CCDA-TITLE02` | `OF` | POPULATE-HEADER-INFO | 182 |
| `CCDA-TITLE02` | `COSGN0AO` | POPULATE-HEADER-INFO | 182 |
| `WS-TRANID` | `TRNNAMEO` | POPULATE-HEADER-INFO | 183 |
| `WS-TRANID` | `OF` | POPULATE-HEADER-INFO | 183 |
| `WS-TRANID` | `COSGN0AO` | POPULATE-HEADER-INFO | 183 |
| `WS-PGMNAME` | `PGMNAMEO` | POPULATE-HEADER-INFO | 184 |
| `WS-PGMNAME` | `OF` | POPULATE-HEADER-INFO | 184 |
| `WS-PGMNAME` | `COSGN0AO` | POPULATE-HEADER-INFO | 184 |
| `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | POPULATE-HEADER-INFO | 186 |
| `WS-CURDATE-DAY` | `WS-CURDATE-DD` | POPULATE-HEADER-INFO | 187 |
| `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | POPULATE-HEADER-INFO | 188 |
| `WS-CURDATE-MM-DD-YY` | `CURDATEO` | POPULATE-HEADER-INFO | 190 |
| `WS-CURDATE-MM-DD-YY` | `OF` | POPULATE-HEADER-INFO | 190 |
| `WS-CURDATE-MM-DD-YY` | `COSGN0AO` | POPULATE-HEADER-INFO | 190 |
| `WS-CURTIME-HOURS` | `WS-CURTIME-HH` | POPULATE-HEADER-INFO | 192 |
| `WS-CURTIME-MINUTE` | `WS-CURTIME-MM` | POPULATE-HEADER-INFO | 193 |
| `WS-CURTIME-SECOND` | `WS-CURTIME-SS` | POPULATE-HEADER-INFO | 194 |
| `WS-CURTIME-HH-MM-SS` | `CURTIMEO` | POPULATE-HEADER-INFO | 196 |
| `WS-CURTIME-HH-MM-SS` | `OF` | POPULATE-HEADER-INFO | 196 |
| `WS-CURTIME-HH-MM-SS` | `COSGN0AO` | POPULATE-HEADER-INFO | 196 |
| `WS-TRANID` | `CDEMO-FROM-TRANID` | READ-USER-SEC-FILE | 224 |
| `WS-PGMNAME` | `CDEMO-FROM-PROGRAM` | READ-USER-SEC-FILE | 225 |
| `WS-USER-ID` | `CDEMO-USER-ID` | READ-USER-SEC-FILE | 226 |
| `SEC-USR-TYPE` | `CDEMO-USER-TYPE` | READ-USER-SEC-FILE | 227 |
| `ZEROS` | `CDEMO-PGM-CONTEXT` | READ-USER-SEC-FILE | 228 |
| `'-1'` | `PASSWDL` | READ-USER-SEC-FILE | 244 |
| `'-1'` | `OF` | READ-USER-SEC-FILE | 244 |
| `'-1'` | `COSGN0AI` | READ-USER-SEC-FILE | 244 |
| `'Y'` | `WS-ERR-FLG` | READ-USER-SEC-FILE | 248 |
| `'User not found. Try again ...'` | `WS-MESSAGE` | READ-USER-SEC-FILE | 249 |
| `'-1'` | `USERIDL` | READ-USER-SEC-FILE | 250 |
| `'-1'` | `OF` | READ-USER-SEC-FILE | 250 |
| `'-1'` | `COSGN0AI` | READ-USER-SEC-FILE | 250 |
| `'Y'` | `WS-ERR-FLG` | READ-USER-SEC-FILE | 253 |
| `'Unable to verify the User ...'` | `WS-MESSAGE` | READ-USER-SEC-FILE | 254 |
*+ 3 more movements*

## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEAD_CODE | Variable `LK-COMMAREA` is declared but never referenced | None | 66 |

### NOTICE — Variable `LK-COMMAREA` is declared but never referenced

`LK-COMMAREA` is declared at line 66 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 66):
```cobol
05  LK-COMMAREA                           PIC X(01)
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---




## Decision Tables (EVALUATE / WHEN)

Captured from the source. Each EVALUATE block is a structured decision the
migration team should turn into either a switch / pattern-match or a rules table.

### EVALUATE `TRUE` — paragraph `PROCESS-ENTER-KEY` (line 128)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | CONTINUE |
| `USERIDI OF COSGN0AI = SPACES OR LOW-VALUES` | MOVE 'Y'      TO WS-ERR-FLG |
| `PASSWDI OF COSGN0AI = SPACES OR LOW-VALUES` | MOVE 'Y'      TO WS-ERR-FLG |

### EVALUATE `WS-RESP-CD` — paragraph `READ-USER-SEC-FILE` (line 252)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE 'Y'      TO WS-ERR-FLG |
| `0` | IF SEC-USR-PWD = WS-USER-PWD |
| `13` | MOVE 'Y'      TO WS-ERR-FLG |

### EVALUATE `EIBAID` — paragraph `MAIN-PARA` (line 91)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE 'Y'                       TO WS-ERR-FLG |
| `DFHENTER` | PERFORM PROCESS-ENTER-KEY |
| `DFHPF3` | MOVE CCDA-MSG-THANK-YOU        TO WS-MESSAGE |




## CICS Commands

This program uses the following EXEC CICS commands:

| Command | Paragraph | Line | Details |
|---------|-----------|------|---------|
| `RETURN` | MAIN-PARA | 98 | {"details": {"transid": "WS-TRANID", "length": "LENGTH OF CARDDEMO-COMMAREA", "c... |
| `RECEIVE` | PROCESS-ENTER-KEY | 110 | {"details": {"map": "COSGN0A", "mapset": "COSGN00", "resp": "WS-RESP-CD"}} |
| `SEND` | SEND-SIGNON-SCREEN | 151 | {"details": {"map": "COSGN0A", "mapset": "COSGN00", "from": "COSGN0AO"}} |
| `SEND` | SEND-PLAIN-TEXT | 164 | {"details": {"from": "WS-MESSAGE", "length": "LENGTH OF WS-MESSAGE"}} |
| `RETURN` | SEND-PLAIN-TEXT | 171 | {"details": {}} |
| `ASSIGN` | POPULATE-HEADER-INFO | 198 | {"details": {}} |
| `ASSIGN` | POPULATE-HEADER-INFO | 202 | {"details": {}} |
| `READ` | READ-USER-SEC-FILE | 211 | {"details": {"dataset": "WS-USRSEC-FILE", "into": "SEC-USER-DATA", "length": "LE... |
| `XCTL` | READ-USER-SEC-FILE | 231 | {"details": {"program": "COADM01C", "commarea": "CARDDEMO-COMMAREA"}} |
| `XCTL` | READ-USER-SEC-FILE | 236 | {"details": {"program": "COMEN01C", "commarea": "CARDDEMO-COMMAREA"}} |

**Summary:** 10 CICS command(s) — RETURN (2), RECEIVE (1), SEND (2), ASSIGN (2), READ (1), XCTL (2)

## CICS Screen Workflow Notes

These notes are derived directly from the COBOL source and BMS map usage. They are intended
to prevent migration errors where a PF key label is mistaken for the full transaction flow.

### Program transfers use XCTL, not a soft return

`EXEC CICS XCTL` transfers control to another program and does not return to the current program like a subroutine call. Document PF-key navigation that reaches this paragraph as a CICS transfer, not as an in-place screen redisplay.

Evidence:
- L231 in `READ-USER-SEC-FILE`: EXEC CICS XCTL {"details": {"program": "COADM01C", "commarea": "CARDDEMO-COMMAREA"}}
- L236 in `READ-USER-SEC-FILE`: EXEC CICS XCTL {"details": {"program": "COMEN01C", "commarea": "CARDDEMO-COMMAREA"}}

### Initial entry without COMMAREA transfers to sign-on

When `EIBCALEN = 0`, this program prepares `COSGN00C` as the target and follows the return/transfer path. It does not display its own BMS map on that entry path.

Evidence:
- L80: `IF EIBCALEN = 0`
- L231 in `READ-USER-SEC-FILE`: EXEC CICS XCTL {"details": {"program": "COADM01C", "commarea": "CARDDEMO-COMMAREA"}}

### PF3 navigation resolves through RETURN-TO-PREV-SCREEN

PF3 selects the `RETURN-TO-PREV-SCREEN` path. That paragraph ends in `EXEC CICS XCTL`, so PF3 is a transfer to the target program held in the COMMAREA routing fields.

Evidence:
- L88: `WHEN DFHPF3`
- L231 in `READ-USER-SEC-FILE`: EXEC CICS XCTL {"details": {"program": "COADM01C", "commarea": "CARDDEMO-COMMAREA"}}

### Error/message text is written to the BMS output field

`ERRMSGI` exists in the input copybook area, but this program displays messages by moving `WS-MESSAGE` to `ERRMSGO OF COUSR3AO`. Documentation should refer to `ERRMSGO` when describing rendered error or status messages.

Evidence:
- L149: `MOVE WS-MESSAGE TO ERRMSGO OF COSGN0AO`

### ERR-FLG is reset at the start of each run

`ERR-FLG` starts each invocation on the off path via `SET ERR-FLG-OFF TO TRUE`. Validation and file-error branches set or test `ERR-FLG-ON` to stop later processing.

Evidence:
- L75: `SET ERR-FLG-OFF TO TRUE`
- L41: `88 ERR-FLG-ON                         VALUE 'Y'.`
- L138: `IF NOT ERR-FLG-ON`

### The BMS map can be sent from multiple paths

Screen output is centralized in the send paragraph, but several routines can perform it. If a read routine sends the map and its caller also sends the map, a modern UI migration must preserve or deliberately remove that duplicate response behavior.

Evidence:
- L245: `READ-USER-SEC-FILE` performs `SEND-SIGNON-SCREEN`
- L251: `READ-USER-SEC-FILE` performs `SEND-SIGNON-SCREEN`
- L256: `READ-USER-SEC-FILE` performs `SEND-SIGNON-SCREEN`
- L151 in `SEND-SIGNON-SCREEN`: EXEC CICS SEND {"details": {"map": "COSGN0A", "mapset": "COSGN00", "from": "COSGN0AO"}}


## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Invalid Login Attempt** `BR-332`  
  If the provided User ID and Password combination does not match the credentials stored in the user security file, the system will display an error message to the user.  
  [View Rule Details](../business-rules/BR-332.md)
- **Invalid User ID Message** `BR-333`  
  If the entered User ID is invalid, display an error message to the user.  
  [View Rule Details](../business-rules/BR-333.md)
- **Invalid Password Message** `BR-334`  
  If the entered Password does not match the Password associated with the User ID, display an error message to the user.  
  [View Rule Details](../business-rules/BR-334.md)
- **Successful Login - Populate Header** `BR-335`  
  Upon successful validation of User ID and Password, populate the header information for the user's session.  
  [View Rule Details](../business-rules/BR-335.md)
- **Successful Login - Proceed to Next Transaction** `BR-336`  
  After successful login and header population, direct the user to the next appropriate transaction.  
  [View Rule Details](../business-rules/BR-336.md)
- **Invalid User ID** `BR-337`  
  If the provided User ID does not exist in the user security file, the system should display an error message.  
  [View Rule Details](../business-rules/BR-337.md)
- **Inactive User Account** `BR-338`  
  If the user account associated with the provided User ID is inactive, the system should display an error message.  
  [View Rule Details](../business-rules/BR-338.md)
- **Password Mismatch** `BR-339`  
  If the provided password does not match the password stored in the user security file for the given User ID, the system should display an error message.  
  [View Rule Details](../business-rules/BR-339.md)
- **Successful Authentication** `BR-340`  
  If the User ID and Password are valid, the system should populate header information and proceed to the next appropriate transaction.  
  [View Rule Details](../business-rules/BR-340.md)

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
| `WS-USER-ID` | 5 | `X(08)` | WORKING-STORAGE | None |
| `WS-USER-PWD` | 5 | `X(08)` | WORKING-STORAGE | None |
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
| `COSGN0AI` | 1 | `None` | WORKING-STORAGE | None |
| `FILLER` | 2 | `X(12)` | WORKING-STORAGE | None |

*Showing 40 of 302 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-05-12 12:18*