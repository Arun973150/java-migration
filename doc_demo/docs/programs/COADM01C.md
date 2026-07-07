# Program: COADM01C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COADM01C` |
| Type | ONLINE |
| Lines | 289 |
| Source | [COADM01C.cbl](../carddemo/COADM01C.cbl#L1) |
| Paragraphs | 8 |
| Statements | 44 |
| Impact Risk | **HIGH** — 20 programs affected |

> **View Source:** [Open COADM01C.cbl](../carddemo/COADM01C.cbl#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-PGMNAME` | `COADM01C` |
| `WS-TRANID` | `CA00` |
| `WS-USRSEC-FILE` | `USRSEC` |
| `WS-ERR-FLG` | `N` |


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **COADM01C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COADM01C (Callers)

*No programs call COADM01C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COADM01C (Callees)

*COADM01C does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `COADM01` |  | 0 |
| `COADM02Y` |  | 0 |
| `COCOM01Y` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |
| `COTTL01Y` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |
| `CSDAT01Y` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |
| `CSMSG01Y` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |
| `CSUSR01Y` | COACTUPC, COACTVWC, COCRDLIC, COCRDSLC, COCRDUPC (+8 more) | 13 |
| `DFHAID` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |
| `DFHBMSCA` | COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC (+15 more) | 20 |


## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.


### Copybook Segment Layouts

#### `COADM01` as `COADM1AI`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `COADM1AI` | Coadm1Ai | `GROUP` | `OBJECT` |  |
| `COADM1AO` | Coadm1Ao | `GROUP` | `OBJECT` |  |

#### `COADM02Y` as `CARDDEMO-ADMIN-MENU-OPTIONS`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CARDDEMO-ADMIN-MENU-OPTIONS` | Carddemo Admin Menu Options | `GROUP` | `OBJECT` |  |
| `CDEMO-ADMIN-OPT-COUNT` | Admin Opt Count | `PIC 9(02)` | `INTEGER` |  |
| `CDEMO-ADMIN-OPTIONS-DATA` | Admin Options Data | `GROUP` | `OBJECT` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `FILLER` | Filler | `PIC 9(02)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(35)` | `STRING(35)` |  |
| `FILLER` | Filler | `PIC X(08)` | `STRING(8)` |  |
| `CDEMO-ADMIN-OPTIONS` | Admin Options | `GROUP` | `OBJECT` |  |
| `CDEMO-ADMIN-OPT` | Admin Opt | `OCCURS 9` | `OBJECT` | Repeating field, 9 occurrences. |
| `CDEMO-ADMIN-OPT-NUM` | Admin Opt Number | `PIC 9(02)` | `INTEGER` |  |
| `CDEMO-ADMIN-OPT-NAME` | Admin Opt Name | `PIC X(35)` | `STRING(35)` |  |
| `CDEMO-ADMIN-OPT-PGMNAME` | Admin Opt Pgmname | `PIC X(08)` | `STRING(8)` |  |

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
| 83 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |
| 105 | `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | CCDA-MSG-INVALID-KEY populates WS-MESSAGE |
| 150 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |
| 180 | `WS-MESSAGE` | `ERRMSGO OF COADM1AO` | WS-MESSAGE populates ERRMSGO OF COADM1AO |
| 207 | `FUNCTION CURRENT-DATE` | `WS-CURDATE-DATA` | FUNCTION CURRENT-DATE populates WS-CURDATE-DATA |
| 214 | `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | WS-CURDATE-MONTH populates WS-CURDATE-MM |
| 215 | `WS-CURDATE-DAY` | `WS-CURDATE-DD` | WS-CURDATE-DAY populates WS-CURDATE-DD |
| 216 | `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | WS-CURDATE-YEAR(3:2) populates WS-CURDATE-YY |
| 218 | `WS-CURDATE-MM-DD-YY` | `CURDATEO OF COADM1AO` | WS-CURDATE-MM-DD-YY populates CURDATEO OF COADM1AO |
| 271 | `SPACES` | `WS-MESSAGE` | SPACES populates WS-MESSAGE |



---

## Dependency Graph

```mermaid
flowchart TD
    COADM01C["⬤ COADM01C"]:::target
    CB_COCOM01Y{{"COCOM01Y"}}:::copybook
    COADM01C -.- CB_COCOM01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COCOM01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COCOM01Y -.- COACTVWC
    COBIL00C["COBIL00C"]:::coupled
    CB_COCOM01Y -.- COBIL00C
    CB_COTTL01Y{{"COTTL01Y"}}:::copybook
    COADM01C -.- CB_COTTL01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COTTL01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COTTL01Y -.- COACTVWC
    COBIL00C["COBIL00C"]:::coupled
    CB_COTTL01Y -.- COBIL00C
    CB_CSDAT01Y{{"CSDAT01Y"}}:::copybook
    COADM01C -.- CB_CSDAT01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSDAT01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSDAT01Y -.- COACTVWC
    COBIL00C["COBIL00C"]:::coupled
    CB_CSDAT01Y -.- COBIL00C
    CB_CSMSG01Y{{"CSMSG01Y"}}:::copybook
    COADM01C -.- CB_CSMSG01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSMSG01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSMSG01Y -.- COACTVWC
    COBIL00C["COBIL00C"]:::coupled
    CB_CSMSG01Y -.- COBIL00C
    CB_CSUSR01Y{{"CSUSR01Y"}}:::copybook
    COADM01C -.- CB_CSUSR01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSUSR01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSUSR01Y -.- COACTVWC
    COCRDLIC["COCRDLIC"]:::coupled
    CB_CSUSR01Y -.- COCRDLIC
    CB_DFHAID{{"DFHAID"}}:::copybook
    COADM01C -.- CB_DFHAID
    COACTUPC["COACTUPC"]:::coupled
    CB_DFHAID -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_DFHAID -.- COACTVWC
    COBIL00C["COBIL00C"]:::coupled
    CB_DFHAID -.- COBIL00C
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

> **If you change COADM01C, what else could break?**

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
- `COUSR01C`
- `COUSR02C`
- `COUSR03C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| MOVE | 20 |
| IF | 10 |
| EXEC_CICS | 6 |
| PERFORM | 5 |
| STRING_OP | 1 |
| SET | 1 |
| INSPECT | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    MAIN_PARA["MAIN-PARA"]
    PROCESS_ENTER_KEY["PROCESS-ENTER-KEY"]
    RETURN_TO_SIGNON_SCREEN["RETURN-TO-SIGNON-SCREEN"]
    SEND_MENU_SCREEN["SEND-MENU-SCREEN"]
    RECEIVE_MENU_SCREEN["RECEIVE-MENU-SCREEN"]
    POPULATE_HEADER_INFO["POPULATE-HEADER-INFO"]
    BUILD_MENU_OPTIONS["BUILD-MENU-OPTIONS"]
    PGMIDERR_ERR_PARA["PGMIDERR-ERR-PARA"]
    START --> MAIN_PARA
    MAIN_PARA --> RETURN_TO_SIGNON_SCREEN
    MAIN_PARA --> SEND_MENU_SCREEN
    MAIN_PARA --> RECEIVE_MENU_SCREEN
    MAIN_PARA --> PROCESS_ENTER_KEY
    PROCESS_ENTER_KEY --> SEND_MENU_SCREEN
    SEND_MENU_SCREEN --> POPULATE_HEADER_INFO
    SEND_MENU_SCREEN --> BUILD_MENU_OPTIONS
    PGMIDERR_ERR_PARA --> SEND_MENU_SCREEN
    PROCESS_ENTER_KEY --> INLINE
    SEND_MENU_SCREEN --> INLINE
    BUILD_MENU_OPTIONS --> INLINE
    PGMIDERR_ERR_PARA --> INLINE
```

## Paragraphs

### MAIN-PARA

| | |
|---|---|
| **Paragraph** | `MAIN-PARA` |
| **Lines** | 75 - 118 |
| **View Code** | [Jump to Line 75](../carddemo/COADM01C.cbl#L75) |



### PROCESS-ENTER-KEY

| | |
|---|---|
| **Paragraph** | `PROCESS-ENTER-KEY` |
| **Lines** | 119 - 162 |
| **View Code** | [Jump to Line 119](../carddemo/COADM01C.cbl#L119) |



### RETURN-TO-SIGNON-SCREEN

| | |
|---|---|
| **Paragraph** | `RETURN-TO-SIGNON-SCREEN` |
| **Lines** | 163 - 174 |
| **View Code** | [Jump to Line 163](../carddemo/COADM01C.cbl#L163) |



### SEND-MENU-SCREEN

| | |
|---|---|
| **Paragraph** | `SEND-MENU-SCREEN` |
| **Lines** | 175 - 191 |
| **View Code** | [Jump to Line 175](../carddemo/COADM01C.cbl#L175) |



### RECEIVE-MENU-SCREEN

| | |
|---|---|
| **Paragraph** | `RECEIVE-MENU-SCREEN` |
| **Lines** | 192 - 204 |
| **View Code** | [Jump to Line 192](../carddemo/COADM01C.cbl#L192) |



### POPULATE-HEADER-INFO

| | |
|---|---|
| **Paragraph** | `POPULATE-HEADER-INFO` |
| **Lines** | 205 - 228 |
| **View Code** | [Jump to Line 205](../carddemo/COADM01C.cbl#L205) |



### BUILD-MENU-OPTIONS

| | |
|---|---|
| **Paragraph** | `BUILD-MENU-OPTIONS` |
| **Lines** | 229 - 269 |
| **View Code** | [Jump to Line 229](../carddemo/COADM01C.cbl#L229) |



### PGMIDERR-ERR-PARA

| | |
|---|---|
| **Paragraph** | `PGMIDERR-ERR-PARA` |
| **Lines** | 270 - 288 |
| **View Code** | [Jump to Line 270](../carddemo/COADM01C.cbl#L270) |







## Copybook Field Dictionaries

The following copybooks are included by this program. Each entry shows the actual fields
extracted from the copybook source file (`.cpy`).

### Copybook `COADM01`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `COADM1AI` | `None` | None | None |  |
| `02` | `TRNNAMEL` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `TRNNAMEF` | `X` | None | COADM1AI |  |
| `03` | `TRNNAMEA` | `X` | None | COADM1AI |  |
| `02` | `TRNNAMEI` | `X(4)` | None | COADM1AI |  |
| `02` | `TITLE01L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `TITLE01F` | `X` | None | COADM1AI |  |
| `03` | `TITLE01A` | `X` | None | COADM1AI |  |
| `02` | `TITLE01I` | `X(40)` | None | COADM1AI |  |
| `02` | `CURDATEL` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `CURDATEF` | `X` | None | COADM1AI |  |
| `03` | `CURDATEA` | `X` | None | COADM1AI |  |
| `02` | `CURDATEI` | `X(8)` | None | COADM1AI |  |
| `02` | `PGMNAMEL` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `PGMNAMEF` | `X` | None | COADM1AI |  |
| `03` | `PGMNAMEA` | `X` | None | COADM1AI |  |
| `02` | `PGMNAMEI` | `X(8)` | None | COADM1AI |  |
| `02` | `TITLE02L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `TITLE02F` | `X` | None | COADM1AI |  |
| `03` | `TITLE02A` | `X` | None | COADM1AI |  |
| `02` | `TITLE02I` | `X(40)` | None | COADM1AI |  |
| `02` | `CURTIMEL` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `CURTIMEF` | `X` | None | COADM1AI |  |
| `03` | `CURTIMEA` | `X` | None | COADM1AI |  |
| `02` | `CURTIMEI` | `X(8)` | None | COADM1AI |  |
| `02` | `OPTN001L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN001F` | `X` | None | COADM1AI |  |
| `03` | `OPTN001A` | `X` | None | COADM1AI |  |
| `02` | `OPTN001I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN002L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN002F` | `X` | None | COADM1AI |  |
| `03` | `OPTN002A` | `X` | None | COADM1AI |  |
| `02` | `OPTN002I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN003L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN003F` | `X` | None | COADM1AI |  |
| `03` | `OPTN003A` | `X` | None | COADM1AI |  |
| `02` | `OPTN003I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN004L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN004F` | `X` | None | COADM1AI |  |
| `03` | `OPTN004A` | `X` | None | COADM1AI |  |
| `02` | `OPTN004I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN005L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN005F` | `X` | None | COADM1AI |  |
| `03` | `OPTN005A` | `X` | None | COADM1AI |  |
| `02` | `OPTN005I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN006L` | `S9(4)` | COMP | COADM1AI |  |
| `02` | `OPTN006F` | `X` | None | COADM1AI |  |
| `03` | `OPTN006A` | `X` | None | COADM1AI |  |
| `02` | `OPTN006I` | `X(40)` | None | COADM1AI |  |
| `02` | `OPTN007L` | `S9(4)` | COMP | COADM1AI |  |
*+ 132 more fields*
### Copybook `COADM02Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CARDDEMO-ADMIN-MENU-OPTIONS` | `None` | None | None |  |
| `05` | `CDEMO-ADMIN-OPT-COUNT` | `9(02)` | None | CARDDEMO-ADMIN-MENU-OPTIONS |  |
| `05` | `CDEMO-ADMIN-OPTIONS-DATA` | `None` | None | CARDDEMO-ADMIN-MENU-OPTIONS |  |
| `05` | `CDEMO-ADMIN-OPTIONS` | `None` | None | CARDDEMO-ADMIN-MENU-OPTIONS |  REDEFINES CDEMO-ADMIN-OPTIONS-DATA |
| `10` | `CDEMO-ADMIN-OPT` | `None` | None | CDEMO-ADMIN-OPTIONS | OCCURS 9 |
| `15` | `CDEMO-ADMIN-OPT-NUM` | `9(02)` | None | CDEMO-ADMIN-OPT |  |
| `15` | `CDEMO-ADMIN-OPT-NAME` | `X(35)` | None | CDEMO-ADMIN-OPT |  |
| `15` | `CDEMO-ADMIN-OPT-PGMNAME` | `X(08)` | None | CDEMO-ADMIN-OPT |  |

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
| `SPACES` | `WS-MESSAGE` | MAIN-PARA | 83 |
| `'COSGN00C'` | `CDEMO-FROM-PROGRAM` | MAIN-PARA | 87 |
| `DFHCOMMAREA(1:EIBCALEN)` | `CARDDEMO-COMMAREA` | MAIN-PARA | 90 |
| `LOW-VALUES` | `COADM1AO` | MAIN-PARA | 93 |
| `'COSGN00C'` | `CDEMO-TO-PROGRAM` | MAIN-PARA | 101 |
| `'Y'` | `WS-ERR-FLG` | MAIN-PARA | 104 |
| `CCDA-MSG-INVALID-KEY` | `WS-MESSAGE` | MAIN-PARA | 105 |
| `WS-OPTION-X` | `WS-OPTION` | PROCESS-ENTER-KEY | 128 |
| `WS-OPTION` | `OPTIONO` | PROCESS-ENTER-KEY | 129 |
| `WS-OPTION` | `OF` | PROCESS-ENTER-KEY | 129 |
| `WS-OPTION` | `COADM1AO` | PROCESS-ENTER-KEY | 129 |
| `'Y'` | `WS-ERR-FLG` | PROCESS-ENTER-KEY | 134 |
| `WS-TRANID` | `CDEMO-FROM-TRANID` | PROCESS-ENTER-KEY | 142 |
| `WS-PGMNAME` | `CDEMO-FROM-PROGRAM` | PROCESS-ENTER-KEY | 143 |
| `ZEROS` | `CDEMO-PGM-CONTEXT` | PROCESS-ENTER-KEY | 144 |
| `SPACES` | `WS-MESSAGE` | PROCESS-ENTER-KEY | 150 |
| `DFHGREEN` | `ERRMSGC` | PROCESS-ENTER-KEY | 151 |
| `DFHGREEN` | `OF` | PROCESS-ENTER-KEY | 151 |
| `DFHGREEN` | `COADM1AO` | PROCESS-ENTER-KEY | 151 |
| `'COSGN00C'` | `CDEMO-TO-PROGRAM` | RETURN-TO-SIGNON-SCREEN | 166 |
| `WS-MESSAGE` | `ERRMSGO` | SEND-MENU-SCREEN | 180 |
| `WS-MESSAGE` | `OF` | SEND-MENU-SCREEN | 180 |
| `WS-MESSAGE` | `COADM1AO` | SEND-MENU-SCREEN | 180 |
| `CCDA-TITLE01` | `TITLE01O` | POPULATE-HEADER-INFO | 209 |
| `CCDA-TITLE01` | `OF` | POPULATE-HEADER-INFO | 209 |
| `CCDA-TITLE01` | `COADM1AO` | POPULATE-HEADER-INFO | 209 |
| `CCDA-TITLE02` | `TITLE02O` | POPULATE-HEADER-INFO | 210 |
| `CCDA-TITLE02` | `OF` | POPULATE-HEADER-INFO | 210 |
| `CCDA-TITLE02` | `COADM1AO` | POPULATE-HEADER-INFO | 210 |
| `WS-TRANID` | `TRNNAMEO` | POPULATE-HEADER-INFO | 211 |
| `WS-TRANID` | `OF` | POPULATE-HEADER-INFO | 211 |
| `WS-TRANID` | `COADM1AO` | POPULATE-HEADER-INFO | 211 |
| `WS-PGMNAME` | `PGMNAMEO` | POPULATE-HEADER-INFO | 212 |
| `WS-PGMNAME` | `OF` | POPULATE-HEADER-INFO | 212 |
| `WS-PGMNAME` | `COADM1AO` | POPULATE-HEADER-INFO | 212 |
| `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | POPULATE-HEADER-INFO | 214 |
| `WS-CURDATE-DAY` | `WS-CURDATE-DD` | POPULATE-HEADER-INFO | 215 |
| `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | POPULATE-HEADER-INFO | 216 |
| `WS-CURDATE-MM-DD-YY` | `CURDATEO` | POPULATE-HEADER-INFO | 218 |
| `WS-CURDATE-MM-DD-YY` | `OF` | POPULATE-HEADER-INFO | 218 |
| `WS-CURDATE-MM-DD-YY` | `COADM1AO` | POPULATE-HEADER-INFO | 218 |
| `WS-CURTIME-HOURS` | `WS-CURTIME-HH` | POPULATE-HEADER-INFO | 220 |
| `WS-CURTIME-MINUTE` | `WS-CURTIME-MM` | POPULATE-HEADER-INFO | 221 |
| `WS-CURTIME-SECOND` | `WS-CURTIME-SS` | POPULATE-HEADER-INFO | 222 |
| `WS-CURTIME-HH-MM-SS` | `CURTIMEO` | POPULATE-HEADER-INFO | 224 |
| `WS-CURTIME-HH-MM-SS` | `OF` | POPULATE-HEADER-INFO | 224 |
| `WS-CURTIME-HH-MM-SS` | `COADM1AO` | POPULATE-HEADER-INFO | 224 |
| `SPACES` | `WS-ADMIN-OPT-TXT` | BUILD-MENU-OPTIONS | 234 |
| `WS-ADMIN-OPT-TXT` | `OPTN001O` | BUILD-MENU-OPTIONS | 243 |
| `WS-ADMIN-OPT-TXT` | `OPTN002O` | BUILD-MENU-OPTIONS | 245 |
| `WS-ADMIN-OPT-TXT` | `OPTN003O` | BUILD-MENU-OPTIONS | 247 |
| `WS-ADMIN-OPT-TXT` | `OPTN004O` | BUILD-MENU-OPTIONS | 249 |
| `WS-ADMIN-OPT-TXT` | `OPTN005O` | BUILD-MENU-OPTIONS | 251 |
| `WS-ADMIN-OPT-TXT` | `OPTN006O` | BUILD-MENU-OPTIONS | 253 |
| `WS-ADMIN-OPT-TXT` | `OPTN007O` | BUILD-MENU-OPTIONS | 255 |
| `WS-ADMIN-OPT-TXT` | `OPTN008O` | BUILD-MENU-OPTIONS | 257 |
| `WS-ADMIN-OPT-TXT` | `OPTN009O` | BUILD-MENU-OPTIONS | 259 |
| `WS-ADMIN-OPT-TXT` | `OPTN010O` | BUILD-MENU-OPTIONS | 261 |
| `SPACES` | `WS-MESSAGE` | PGMIDERR-ERR-PARA | 271 |
| `DFHGREEN` | `ERRMSGC` | PGMIDERR-ERR-PARA | 272 |
*+ 2 more movements*

## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEAD_CODE | Variable `WS-USRSEC-FILE` is declared but never referenced | None | 39 |
| **NOTICE** | DEAD_CODE | Variable `LK-COMMAREA` is declared but never referenced | None | 68 |

### NOTICE — Variable `WS-USRSEC-FILE` is declared but never referenced

`WS-USRSEC-FILE` is declared at line 39 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 39):
```cobol
05 WS-USRSEC-FILE             PIC X(08) VALUE 'USRSEC  '.
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `LK-COMMAREA` is declared but never referenced

`LK-COMMAREA` is declared at line 68 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 68):
```cobol
05  LK-COMMAREA                           PIC X(01)
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---




## Decision Tables (EVALUATE / WHEN)

Captured from the source. Each EVALUATE block is a structured decision the
migration team should turn into either a switch / pattern-match or a rules table.

### EVALUATE `WS-IDX` — paragraph `BUILD-MENU-OPTIONS` (line 262)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | CONTINUE |
| `1` | MOVE WS-ADMIN-OPT-TXT TO OPTN001O |
| `2` | MOVE WS-ADMIN-OPT-TXT TO OPTN002O |
| `3` | MOVE WS-ADMIN-OPT-TXT TO OPTN003O |
| `4` | MOVE WS-ADMIN-OPT-TXT TO OPTN004O |
| `5` | MOVE WS-ADMIN-OPT-TXT TO OPTN005O |
| `6` | MOVE WS-ADMIN-OPT-TXT TO OPTN006O |
| `7` | MOVE WS-ADMIN-OPT-TXT TO OPTN007O |
| `8` | MOVE WS-ADMIN-OPT-TXT TO OPTN008O |
| `9` | MOVE WS-ADMIN-OPT-TXT TO OPTN009O |
| `10` | MOVE WS-ADMIN-OPT-TXT TO OPTN010O |

### EVALUATE `EIBAID` — paragraph `MAIN-PARA` (line 103)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE 'Y'                       TO WS-ERR-FLG |
| `DFHENTER` | PERFORM PROCESS-ENTER-KEY |
| `DFHPF3` | MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM |




## CICS Commands

This program uses the following EXEC CICS commands:

| Command | Paragraph | Line | Details |
|---------|-----------|------|---------|
| `HANDLE` | MAIN-PARA | 77 | {"details": {}} |
| `RETURN` | MAIN-PARA | 111 | {"details": {"transid": "WS-TRANID", "commarea": "CARDDEMO-COMMAREA"}} |
| `XCTL` | PROCESS-ENTER-KEY | 145 | {"details": {"program": "CDEMO-ADMIN-OPT-PGMNAME(WS-OPTION", "commarea": "CARDDE... |
| `XCTL` | RETURN-TO-SIGNON-SCREEN | 168 | {"details": {"program": "CDEMO-TO-PROGRAM"}} |
| `SEND` | SEND-MENU-SCREEN | 182 | {"details": {"map": "COADM1A", "mapset": "COADM01", "from": "COADM1AO"}} |
| `RECEIVE` | RECEIVE-MENU-SCREEN | 194 | {"details": {"map": "COADM1A", "mapset": "COADM01", "into": "COADM1AI", "resp": ... |
| `RETURN` | PGMIDERR-ERR-PARA | 280 | {"details": {"transid": "WS-TRANID", "commarea": "CARDDEMO-COMMAREA"}} |

**Summary:** 7 CICS command(s) — HANDLE (1), RETURN (2), XCTL (2), SEND (1), RECEIVE (1)

## CICS Screen Workflow Notes

These notes are derived directly from the COBOL source and BMS map usage. They are intended
to prevent migration errors where a PF key label is mistaken for the full transaction flow.

### Program transfers use XCTL, not a soft return

`EXEC CICS XCTL` transfers control to another program and does not return to the current program like a subroutine call. Document PF-key navigation that reaches this paragraph as a CICS transfer, not as an in-place screen redisplay.

Evidence:
- L145 in `PROCESS-ENTER-KEY`: EXEC CICS XCTL {"details": {"program": "CDEMO-ADMIN-OPT-PGMNAME(WS-OPTION", "commarea": "CARDDEMO-COMMAREA"}}
- L168 in `RETURN-TO-SIGNON-SCREEN`: EXEC CICS XCTL {"details": {"program": "CDEMO-TO-PROGRAM"}}

### Initial entry without COMMAREA transfers to sign-on

When `EIBCALEN = 0`, this program prepares `COSGN00C` as the target and follows the return/transfer path. It does not display its own BMS map on that entry path.

Evidence:
- L86: `IF EIBCALEN = 0`
- L101: `MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM`
- L166: `MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM`
- L145 in `PROCESS-ENTER-KEY`: EXEC CICS XCTL {"details": {"program": "CDEMO-ADMIN-OPT-PGMNAME(WS-OPTION", "commarea": "CARDDEMO-COMMAREA"}}

### PF3 navigation resolves through RETURN-TO-PREV-SCREEN

PF3 selects the `RETURN-TO-PREV-SCREEN` path. That paragraph ends in `EXEC CICS XCTL`, so PF3 is a transfer to the target program held in the COMMAREA routing fields.

Evidence:
- L100: `WHEN DFHPF3`
- L145 in `PROCESS-ENTER-KEY`: EXEC CICS XCTL {"details": {"program": "CDEMO-ADMIN-OPT-PGMNAME(WS-OPTION", "commarea": "CARDDEMO-COMMAREA"}}

### Error/message text is written to the BMS output field

`ERRMSGI` exists in the input copybook area, but this program displays messages by moving `WS-MESSAGE` to `ERRMSGO OF COUSR3AO`. Documentation should refer to `ERRMSGO` when describing rendered error or status messages.

Evidence:
- L180: `MOVE WS-MESSAGE TO ERRMSGO OF COADM1AO`

### ERR-FLG is reset at the start of each run

`ERR-FLG` starts each invocation on the off path via `SET ERR-FLG-OFF TO TRUE`. Validation and file-error branches set or test `ERR-FLG-ON` to stop later processing.

Evidence:
- L81: `SET ERR-FLG-OFF TO TRUE`
- L41: `88 ERR-FLG-ON                         VALUE 'Y'.`
- L140: `IF NOT ERR-FLG-ON`

### The BMS map can be sent from multiple paths

Screen output is centralized in the send paragraph, but several routines can perform it. If a read routine sends the map and its caller also sends the map, a modern UI migration must preserve or deliberately remove that duplicate response behavior.

Evidence:
- L94: `MAIN-PARA` performs `SEND-MENU-SCREEN`
- L106: `MAIN-PARA` performs `SEND-MENU-SCREEN`
- L137: `PROCESS-ENTER-KEY` performs `SEND-MENU-SCREEN`
- L157: `PROCESS-ENTER-KEY` performs `SEND-MENU-SCREEN`
- L279: `PGMIDERR-ERR-PARA` performs `SEND-MENU-SCREEN`
- L182 in `SEND-MENU-SCREEN`: EXEC CICS SEND {"details": {"map": "COADM1A", "mapset": "COADM01", "from": "COADM1AO"}}


## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Invalid Program ID Error** `BR-302`  
  If the user enters an invalid program ID, an error message is displayed.  
  [View Rule Details](../business-rules/BR-302.md)
- **Invalid Program ID Error Message** `BR-303`  
  If the user enters an invalid program ID, an error message is displayed on the screen.  
  [View Rule Details](../business-rules/BR-303.md)
- **Invalid Program ID Error Message** `BR-304`  
  If the user enters an invalid program ID, an error message is displayed on the screen.  
  [View Rule Details](../business-rules/BR-304.md)

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
| `WS-OPTION-X` | 5 | `X(02)` | WORKING-STORAGE | None |
| `WS-OPTION` | 5 | `9(02)` | WORKING-STORAGE | None |
| `WS-IDX` | 5 | `S9(04)` | WORKING-STORAGE | None |
| `WS-ADMIN-OPT-TXT` | 5 | `X(40)` | WORKING-STORAGE | None |
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

*Showing 40 of 438 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-05-12 12:31*