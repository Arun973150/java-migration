# Program: COCRDUPC


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COCRDUPC` |
| Type | ONLINE |
| Lines | 1561 |
| Source | [COCRDUPC.cbl](../carddemo/COCRDUPC.cbl#L1) |
| Paragraphs | 45 |
| Statements | 73 |
| Impact Risk | **HIGH** — 26 programs affected |

> **View Source:** [Open COCRDUPC.cbl](../carddemo/COCRDUPC.cbl#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `WS-RETURN-FLAG-ON` | `1` |
| `WS-EXIT-MESSAGE` | `PF03 pressed.Exiting` |
| `WS-PROMPT-FOR-ACCT` | `Account number not provided` |
| `WS-PROMPT-FOR-CARD` | `Card number not provided` |
| `WS-PROMPT-FOR-NAME` | `Card name not provided` |
| `WS-NAME-MUST-BE-ALPHA` | `Card name can only contain alphabets and spaces` |


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **COCRDUPC** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COCRDUPC (Callers)

*No programs call COCRDUPC — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COCRDUPC (Callees)

*COCRDUPC does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `COCOM01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `COCRDUP` |  | 0 |
| `COTTL01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `CSDAT01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `CSMSG01Y` | COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC (+15 more) | 20 |
| `CSMSG02Y` | COACTUPC, COACTVWC, COCRDSLC, COPAUS0C, COPAUS1C (+1 more) | 6 |
| `CSUSR01Y` | COACTUPC, COACTVWC, COADM01C, COCRDLIC, COCRDSLC (+8 more) | 13 |
| `CVACT02Y` | CBACT02C, CBEXPORT, CBIMPORT, CBTRN01C, COACTVWC (+4 more) | 9 |
| `CVCRD01Y` | COACTUPC, COACTVWC, COCRDLIC, COCRDSLC, COTRTLIC (+1 more) | 6 |
| `CVCUS01Y` | CBCUS01C, CBEXPORT, CBIMPORT, CBTRN01C, COACTUPC (+4 more) | 9 |
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

#### `COCRDUP` as `CCRDUPAI`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CCRDUPAI` | Ccrdupai | `GROUP` | `OBJECT` |  |
| `CCRDUPAO` | Ccrdupao | `GROUP` | `OBJECT` |  |

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

#### `CSMSG02Y` as `ABEND-DATA`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `ABEND-DATA` | Abend Data | `GROUP` | `OBJECT` |  |
| `ABEND-CODE` | Abend Code | `PIC X(4)` | `STRING(4)` |  |
| `ABEND-CULPRIT` | Abend Culprit | `PIC X(8)` | `STRING(8)` |  |
| `ABEND-REASON` | Abend Reason | `PIC X(50)` | `STRING(50)` |  |
| `ABEND-MSG` | Abend Msg | `PIC X(72)` | `STRING(72)` |  |

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

#### `CVACT02Y` as `CARD-RECORD`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CARD-RECORD` | Card Record | `GROUP` | `OBJECT` |  |
| `CARD-NUM` | Card Number | `PIC X(16)` | `STRING(16)` |  |
| `CARD-ACCT-ID` | Card Account ID | `PIC 9(11)` | `BIGINT` |  |
| `CARD-CVV-CD` | Card Cvv Cd | `PIC 9(03)` | `INTEGER` |  |
| `CARD-EMBOSSED-NAME` | Card Embossed Name | `PIC X(50)` | `STRING(50)` |  |
| `CARD-EXPIRAION-DATE` | Card Expiraion Date | `PIC X(10)` | `STRING(10)` | Date-like field; verify YYDDD, YYMMDD, or ISO format before migration. |
| `CARD-ACTIVE-STATUS` | Card Active Status | `PIC X(01)` | `STRING(1)` |  |
| `FILLER` | Filler | `PIC X(59)` | `STRING(59)` |  |

#### `CVCRD01Y` as `CC-WORK-AREAS`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CC-WORK-AREAS` | Cc Work Areas | `GROUP` | `OBJECT` |  |
| `CC-WORK-AREA` | Cc Work Area | `GROUP` | `OBJECT` |  |
| `CCARD-AID` | Ccard Aid | `PIC X(5)` | `STRING(5)` |  |
| `CCARD-NEXT-PROG` | Ccard Next Prog | `PIC X(8)` | `STRING(8)` |  |
| `CCARD-NEXT-MAPSET` | Ccard Next Mapset | `PIC X(7)` | `STRING(7)` |  |
| `CCARD-NEXT-MAP` | Ccard Next Map | `PIC X(7)` | `STRING(7)` |  |
| `CCARD-ERROR-MSG` | Ccard Error Msg | `PIC X(75)` | `STRING(75)` |  |
| `CCARD-RETURN-MSG` | Ccard Return Msg | `PIC X(75)` | `STRING(75)` |  |
| `CC-ACCT-ID` | Cc Account ID | `PIC X(11)` | `STRING(11)` |  |
| `CC-ACCT-ID-N` | Cc Account ID N | `PIC 9(11)` | `BIGINT` |  |
| `CC-CARD-NUM` | Cc Card Number | `PIC X(16)` | `STRING(16)` |  |
| `CC-CARD-NUM-N` | Cc Card Number N | `PIC 9(16)` | `BIGINT` |  |
| `CC-CUST-ID` | Cc Customer ID | `PIC X(09)` | `STRING(9)` |  |
| `CC-CUST-ID-N` | Cc Customer ID N | `PIC 9(9)` | `INTEGER` |  |

#### `CVCUS01Y` as `CUSTOMER-RECORD`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CUSTOMER-RECORD` | Customer Record | `GROUP` | `OBJECT` |  |
| `CUST-ID` | Customer ID | `PIC 9(09)` | `INTEGER` |  |
| `CUST-FIRST-NAME` | Customer First Name | `PIC X(25)` | `STRING(25)` |  |
| `CUST-MIDDLE-NAME` | Customer Middle Name | `PIC X(25)` | `STRING(25)` |  |
| `CUST-LAST-NAME` | Customer Last Name | `PIC X(25)` | `STRING(25)` |  |
| `CUST-ADDR-LINE-1` | Customer Addr Line 1 | `PIC X(50)` | `STRING(50)` |  |
| `CUST-ADDR-LINE-2` | Customer Addr Line 2 | `PIC X(50)` | `STRING(50)` |  |
| `CUST-ADDR-LINE-3` | Customer Addr Line 3 | `PIC X(50)` | `STRING(50)` |  |
| `CUST-ADDR-STATE-CD` | Customer Addr State Cd | `PIC X(02)` | `STRING(2)` |  |
| `CUST-ADDR-COUNTRY-CD` | Customer Addr Country Cd | `PIC X(03)` | `STRING(3)` |  |
| `CUST-ADDR-ZIP` | Customer Addr Zip | `PIC X(10)` | `STRING(10)` |  |
| `CUST-PHONE-NUM-1` | Customer Phone Number 1 | `PIC X(15)` | `STRING(15)` |  |
| `CUST-PHONE-NUM-2` | Customer Phone Number 2 | `PIC X(15)` | `STRING(15)` |  |
| `CUST-SSN` | Customer Ssn | `PIC 9(09)` | `INTEGER` |  |
| `CUST-GOVT-ISSUED-ID` | Customer Govt Issued ID | `PIC X(20)` | `STRING(20)` |  |
| `CUST-DOB-YYYY-MM-DD` | Customer Dob Yyyy Mm Dd | `PIC X(10)` | `STRING(10)` |  |
| `CUST-EFT-ACCOUNT-ID` | Customer Eft Account ID | `PIC X(10)` | `STRING(10)` |  |
| `CUST-PRI-CARD-HOLDER-IND` | Customer Pri Card Holder Ind | `PIC X(01)` | `STRING(1)` |  |
| `CUST-FICO-CREDIT-SCORE` | Customer Fico Credit Score | `PIC 9(03)` | `INTEGER` |  |
| `FILLER` | Filler | `PIC X(168)` | `STRING(168)` |  |

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
| 460 | `ZEROS` | `CDEMO-ACCT-ID` | ZEROS populates CDEMO-ACCT-ID |
| 490 | `CDEMO-ACCT-ID` | `CC-ACCT-ID-N` | CDEMO-ACCT-ID populates CC-ACCT-ID-N |
| 591 | `LOW-VALUES` | `CC-ACCT-ID` | LOW-VALUES populates CC-ACCT-ID |
| 594 | `ACCTSIDI OF CCRDUPAI` | `CC-ACCT-ID` | ACCTSIDI OF CCRDUPAI populates CC-ACCT-ID |
| 671 | `CCUP-OLD-ACCTID` | `CDEMO-ACCT-ID` | CCUP-OLD-ACCTID populates CDEMO-ACCT-ID |
| 674 | `CCUP-OLD-CRDSTCD` | `CARD-ACTIVE-STATUS` | CCUP-OLD-CRDSTCD populates CARD-ACTIVE-STATUS |
| 733 | `ZEROES` | `CDEMO-ACCT-ID` | ZEROES populates CDEMO-ACCT-ID |
| 734 | `LOW-VALUES` | `CCUP-NEW-ACCTID` | LOW-VALUES populates CCUP-NEW-ACCTID |
| 748 | `ZERO` | `CDEMO-ACCT-ID` | ZERO populates CDEMO-ACCT-ID |
| 749 | `LOW-VALUES` | `CCUP-NEW-ACCTID` | LOW-VALUES populates CCUP-NEW-ACCTID |
| 752 | `CC-ACCT-ID` | `CDEMO-ACCT-ID` | CC-ACCT-ID populates CDEMO-ACCT-ID |
| 1015 | `ZEROES` | `CDEMO-ACCT-ID` | ZEROES populates CDEMO-ACCT-ID |
| 1017 | `LOW-VALUES` | `CDEMO-ACCT-STATUS` | LOW-VALUES populates CDEMO-ACCT-STATUS |
| 1055 | `FUNCTION CURRENT-DATE` | `WS-CURDATE-DATA` | FUNCTION CURRENT-DATE populates WS-CURDATE-DATA |
| 1062 | `FUNCTION CURRENT-DATE` | `WS-CURDATE-DATA` | FUNCTION CURRENT-DATE populates WS-CURDATE-DATA |
| 1064 | `WS-CURDATE-MONTH` | `WS-CURDATE-MM` | WS-CURDATE-MONTH populates WS-CURDATE-MM |
| 1065 | `WS-CURDATE-DAY` | `WS-CURDATE-DD` | WS-CURDATE-DAY populates WS-CURDATE-DD |
| 1066 | `WS-CURDATE-YEAR(3:2)` | `WS-CURDATE-YY` | WS-CURDATE-YEAR(3:2) populates WS-CURDATE-YY |
| 1068 | `WS-CURDATE-MM-DD-YY` | `CURDATEO OF CCRDUPAO` | WS-CURDATE-MM-DD-YY populates CURDATEO OF CCRDUPAO |
| 1088 | `LOW-VALUES` | `ACCTSIDO OF CCRDUPAO` | LOW-VALUES populates ACCTSIDO OF CCRDUPAO |
| 1090 | `CC-ACCT-ID` | `ACCTSIDO OF CCRDUPAO` | CC-ACCT-ID populates ACCTSIDO OF CCRDUPAO |
| 1174 | `DFHBMFSE` | `ACCTSIDA OF CCRDUPAI` | DFHBMFSE populates ACCTSIDA OF CCRDUPAI |
| 1183 | `DFHBMPRF` | `ACCTSIDA OF CCRDUPAI` | DFHBMPRF populates ACCTSIDA OF CCRDUPAI |
| 1193 | `DFHBMPRF` | `ACCTSIDA OF CCRDUPAI` | DFHBMPRF populates ACCTSIDA OF CCRDUPAI |
| 1201 | `DFHBMFSE` | `ACCTSIDA OF CCRDUPAI` | DFHBMFSE populates ACCTSIDA OF CCRDUPAI |
| 1217 | `-1` | `ACCTSIDL OF CCRDUPAI` | -1 populates ACCTSIDL OF CCRDUPAI |
| 1234 | `-1` | `ACCTSIDL OF CCRDUPAI` | -1 populates ACCTSIDL OF CCRDUPAI |
| 1239 | `DFHDFCOL` | `ACCTSIDC OF CCRDUPAO` | DFHDFCOL populates ACCTSIDC OF CCRDUPAO |
| 1244 | `DFHRED` | `ACCTSIDC OF CCRDUPAO` | DFHRED populates ACCTSIDC OF CCRDUPAO |
| 1249 | `'*'` | `ACCTSIDO OF CCRDUPAO` | '*' populates ACCTSIDO OF CCRDUPAO |



---

## Dependency Graph

```mermaid
flowchart TD
    COCRDUPC["⬤ COCRDUPC"]:::target
    CB_COCOM01Y{{"COCOM01Y"}}:::copybook
    COCRDUPC -.- CB_COCOM01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COCOM01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COCOM01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COCOM01Y -.- COADM01C
    CB_COTTL01Y{{"COTTL01Y"}}:::copybook
    COCRDUPC -.- CB_COTTL01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_COTTL01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_COTTL01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_COTTL01Y -.- COADM01C
    CB_CSDAT01Y{{"CSDAT01Y"}}:::copybook
    COCRDUPC -.- CB_CSDAT01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSDAT01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSDAT01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSDAT01Y -.- COADM01C
    CB_CSMSG01Y{{"CSMSG01Y"}}:::copybook
    COCRDUPC -.- CB_CSMSG01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSMSG01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSMSG01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSMSG01Y -.- COADM01C
    CB_CSMSG02Y{{"CSMSG02Y"}}:::copybook
    COCRDUPC -.- CB_CSMSG02Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSMSG02Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSMSG02Y -.- COACTVWC
    COCRDSLC["COCRDSLC"]:::coupled
    CB_CSMSG02Y -.- COCRDSLC
    CB_CSUSR01Y{{"CSUSR01Y"}}:::copybook
    COCRDUPC -.- CB_CSUSR01Y
    COACTUPC["COACTUPC"]:::coupled
    CB_CSUSR01Y -.- COACTUPC
    COACTVWC["COACTVWC"]:::coupled
    CB_CSUSR01Y -.- COACTVWC
    COADM01C["COADM01C"]:::coupled
    CB_CSUSR01Y -.- COADM01C
    CB_CVACT02Y{{"CVACT02Y"}}:::copybook
    COCRDUPC -.- CB_CVACT02Y
    CBACT02C["CBACT02C"]:::coupled
    CB_CVACT02Y -.- CBACT02C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT02Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVACT02Y -.- CBIMPORT
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

> **If you change COCRDUPC, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 26 |
| **Total Impact** | **26** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `CBACT02C`
- `CBCUS01C`
- `CBEXPORT`
- `CBIMPORT`
- `CBTRN01C`
- `COACTUPC`
- `COACTVWC`
- `COADM01C`
- `COBIL00C`
- `COCRDLIC`
- `COCRDSLC`
- `COMEN01C`
- `COPAUA0C`
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
| IF | 72 |
| REWRITE | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    0000_MAIN["0000-MAIN"]
    COMMON_RETURN["COMMON-RETURN"]
    0000_MAIN_EXIT["0000-MAIN-EXIT"]
    1000_PROCESS_INPUTS["1000-PROCESS-INPUTS"]
    1000_PROCESS_INPUTS_EXIT["1000-PROCESS-INPUTS-EXIT"]
    1100_RECEIVE_MAP["1100-RECEIVE-MAP"]
    1100_RECEIVE_MAP_EXIT["1100-RECEIVE-MAP-EXIT"]
    1200_EDIT_MAP_INPUTS["1200-EDIT-MAP-INPUTS"]
    1200_EDIT_MAP_INPUTS_EXIT["1200-EDIT-MAP-INPUTS-EXIT"]
    1210_EDIT_ACCOUNT["1210-EDIT-ACCOUNT"]
    1210_EDIT_ACCOUNT_EXIT["1210-EDIT-ACCOUNT-EXIT"]
    1220_EDIT_CARD["1220-EDIT-CARD"]
    1220_EDIT_CARD_EXIT["1220-EDIT-CARD-EXIT"]
    1230_EDIT_NAME["1230-EDIT-NAME"]
    1230_EDIT_NAME_EXIT["1230-EDIT-NAME-EXIT"]
    START --> 0000_MAIN
    0000_MAIN --> YYYY_STORE_PFKEY
    0000_MAIN --> 9000_READ_DATA
    0000_MAIN --> 3000_SEND_MAP
    0000_MAIN --> 1000_PROCESS_INPUTS
    0000_MAIN --> 2000_DECIDE_ACTION
    1000_PROCESS_INPUTS --> 1100_RECEIVE_MAP
    1000_PROCESS_INPUTS --> 1200_EDIT_MAP_INPUTS
    1200_EDIT_MAP_INPUTS --> 1210_EDIT_ACCOUNT
    1200_EDIT_MAP_INPUTS --> 1220_EDIT_CARD
    1200_EDIT_MAP_INPUTS --> 1230_EDIT_NAME
    1200_EDIT_MAP_INPUTS --> 1240_EDIT_CARDSTATUS
    1200_EDIT_MAP_INPUTS --> 1250_EDIT_EXPIRY_MON
    1200_EDIT_MAP_INPUTS --> 1260_EDIT_EXPIRY_YEAR
    2000_DECIDE_ACTION --> 9000_READ_DATA
    2000_DECIDE_ACTION --> 9200_WRITE_PROCESSING
    2000_DECIDE_ACTION --> ABEND_ROUTINE
    3000_SEND_MAP --> 3100_SCREEN_INIT
```

## Paragraphs

### 0000-MAIN

| | |
|---|---|
| **Paragraph** | `0000-MAIN` |
| **Lines** | 367 - 545 |
| **View Code** | [Jump to Line 367](../carddemo/COCRDUPC.cbl#L367) |



### COMMON-RETURN

| | |
|---|---|
| **Paragraph** | `COMMON-RETURN` |
| **Lines** | 546 - 559 |
| **View Code** | [Jump to Line 546](../carddemo/COCRDUPC.cbl#L546) |



### 0000-MAIN-EXIT

| | |
|---|---|
| **Paragraph** | `0000-MAIN-EXIT` |
| **Lines** | 560 - 563 |
| **View Code** | [Jump to Line 560](../carddemo/COCRDUPC.cbl#L560) |



### 1000-PROCESS-INPUTS

| | |
|---|---|
| **Paragraph** | `1000-PROCESS-INPUTS` |
| **Lines** | 564 - 574 |
| **View Code** | [Jump to Line 564](../carddemo/COCRDUPC.cbl#L564) |



### 1000-PROCESS-INPUTS-EXIT

| | |
|---|---|
| **Paragraph** | `1000-PROCESS-INPUTS-EXIT` |
| **Lines** | 575 - 577 |
| **View Code** | [Jump to Line 575](../carddemo/COCRDUPC.cbl#L575) |



### 1100-RECEIVE-MAP

| | |
|---|---|
| **Paragraph** | `1100-RECEIVE-MAP` |
| **Lines** | 578 - 637 |
| **View Code** | [Jump to Line 578](../carddemo/COCRDUPC.cbl#L578) |



### 1100-RECEIVE-MAP-EXIT

| | |
|---|---|
| **Paragraph** | `1100-RECEIVE-MAP-EXIT` |
| **Lines** | 638 - 640 |
| **View Code** | [Jump to Line 638](../carddemo/COCRDUPC.cbl#L638) |



### 1200-EDIT-MAP-INPUTS

| | |
|---|---|
| **Paragraph** | `1200-EDIT-MAP-INPUTS` |
| **Lines** | 641 - 716 |
| **View Code** | [Jump to Line 641](../carddemo/COCRDUPC.cbl#L641) |



### 1200-EDIT-MAP-INPUTS-EXIT

| | |
|---|---|
| **Paragraph** | `1200-EDIT-MAP-INPUTS-EXIT` |
| **Lines** | 717 - 720 |
| **View Code** | [Jump to Line 717](../carddemo/COCRDUPC.cbl#L717) |



### 1210-EDIT-ACCOUNT

| | |
|---|---|
| **Paragraph** | `1210-EDIT-ACCOUNT` |
| **Lines** | 721 - 757 |
| **View Code** | [Jump to Line 721](../carddemo/COCRDUPC.cbl#L721) |



### 1210-EDIT-ACCOUNT-EXIT

| | |
|---|---|
| **Paragraph** | `1210-EDIT-ACCOUNT-EXIT` |
| **Lines** | 758 - 761 |
| **View Code** | [Jump to Line 758](../carddemo/COCRDUPC.cbl#L758) |



### 1220-EDIT-CARD

| | |
|---|---|
| **Paragraph** | `1220-EDIT-CARD` |
| **Lines** | 762 - 801 |
| **View Code** | [Jump to Line 762](../carddemo/COCRDUPC.cbl#L762) |



### 1220-EDIT-CARD-EXIT

| | |
|---|---|
| **Paragraph** | `1220-EDIT-CARD-EXIT` |
| **Lines** | 802 - 805 |
| **View Code** | [Jump to Line 802](../carddemo/COCRDUPC.cbl#L802) |



### 1230-EDIT-NAME

| | |
|---|---|
| **Paragraph** | `1230-EDIT-NAME` |
| **Lines** | 806 - 840 |
| **View Code** | [Jump to Line 806](../carddemo/COCRDUPC.cbl#L806) |



### 1230-EDIT-NAME-EXIT

| | |
|---|---|
| **Paragraph** | `1230-EDIT-NAME-EXIT` |
| **Lines** | 841 - 844 |
| **View Code** | [Jump to Line 841](../carddemo/COCRDUPC.cbl#L841) |



### 1240-EDIT-CARDSTATUS

| | |
|---|---|
| **Paragraph** | `1240-EDIT-CARDSTATUS` |
| **Lines** | 845 - 873 |
| **View Code** | [Jump to Line 845](../carddemo/COCRDUPC.cbl#L845) |



### 1240-EDIT-CARDSTATUS-EXIT

| | |
|---|---|
| **Paragraph** | `1240-EDIT-CARDSTATUS-EXIT` |
| **Lines** | 874 - 876 |
| **View Code** | [Jump to Line 874](../carddemo/COCRDUPC.cbl#L874) |



### 1250-EDIT-EXPIRY-MON

| | |
|---|---|
| **Paragraph** | `1250-EDIT-EXPIRY-MON` |
| **Lines** | 877 - 909 |
| **View Code** | [Jump to Line 877](../carddemo/COCRDUPC.cbl#L877) |



### 1250-EDIT-EXPIRY-MON-EXIT

| | |
|---|---|
| **Paragraph** | `1250-EDIT-EXPIRY-MON-EXIT` |
| **Lines** | 910 - 912 |
| **View Code** | [Jump to Line 910](../carddemo/COCRDUPC.cbl#L910) |



### 1260-EDIT-EXPIRY-YEAR

| | |
|---|---|
| **Paragraph** | `1260-EDIT-EXPIRY-YEAR` |
| **Lines** | 913 - 944 |
| **View Code** | [Jump to Line 913](../carddemo/COCRDUPC.cbl#L913) |



### 1260-EDIT-EXPIRY-YEAR-EXIT

| | |
|---|---|
| **Paragraph** | `1260-EDIT-EXPIRY-YEAR-EXIT` |
| **Lines** | 945 - 947 |
| **View Code** | [Jump to Line 945](../carddemo/COCRDUPC.cbl#L945) |



### 2000-DECIDE-ACTION

| | |
|---|---|
| **Paragraph** | `2000-DECIDE-ACTION` |
| **Lines** | 948 - 1028 |
| **View Code** | [Jump to Line 948](../carddemo/COCRDUPC.cbl#L948) |



### 2000-DECIDE-ACTION-EXIT

| | |
|---|---|
| **Paragraph** | `2000-DECIDE-ACTION-EXIT` |
| **Lines** | 1029 - 1034 |
| **View Code** | [Jump to Line 1029](../carddemo/COCRDUPC.cbl#L1029) |



### 3000-SEND-MAP

| | |
|---|---|
| **Paragraph** | `3000-SEND-MAP` |
| **Lines** | 1035 - 1047 |
| **View Code** | [Jump to Line 1035](../carddemo/COCRDUPC.cbl#L1035) |



### 3000-SEND-MAP-EXIT

| | |
|---|---|
| **Paragraph** | `3000-SEND-MAP-EXIT` |
| **Lines** | 1048 - 1051 |
| **View Code** | [Jump to Line 1048](../carddemo/COCRDUPC.cbl#L1048) |



### 3100-SCREEN-INIT

| | |
|---|---|
| **Paragraph** | `3100-SCREEN-INIT` |
| **Lines** | 1052 - 1077 |
| **View Code** | [Jump to Line 1052](../carddemo/COCRDUPC.cbl#L1052) |



### 3100-SCREEN-INIT-EXIT

| | |
|---|---|
| **Paragraph** | `3100-SCREEN-INIT-EXIT` |
| **Lines** | 1078 - 1081 |
| **View Code** | [Jump to Line 1078](../carddemo/COCRDUPC.cbl#L1078) |



### 3200-SETUP-SCREEN-VARS

| | |
|---|---|
| **Paragraph** | `3200-SETUP-SCREEN-VARS` |
| **Lines** | 1082 - 1134 |
| **View Code** | [Jump to Line 1082](../carddemo/COCRDUPC.cbl#L1082) |



### 3200-SETUP-SCREEN-VARS-EXIT

| | |
|---|---|
| **Paragraph** | `3200-SETUP-SCREEN-VARS-EXIT` |
| **Lines** | 1135 - 1137 |
| **View Code** | [Jump to Line 1135](../carddemo/COCRDUPC.cbl#L1135) |



### 3250-SETUP-INFOMSG

| | |
|---|---|
| **Paragraph** | `3250-SETUP-INFOMSG` |
| **Lines** | 1138 - 1164 |
| **View Code** | [Jump to Line 1138](../carddemo/COCRDUPC.cbl#L1138) |



### 3250-SETUP-INFOMSG-EXIT

| | |
|---|---|
| **Paragraph** | `3250-SETUP-INFOMSG-EXIT` |
| **Lines** | 1165 - 1167 |
| **View Code** | [Jump to Line 1165](../carddemo/COCRDUPC.cbl#L1165) |



### 3300-SETUP-SCREEN-ATTRS

| | |
|---|---|
| **Paragraph** | `3300-SETUP-SCREEN-ATTRS` |
| **Lines** | 1168 - 1318 |
| **View Code** | [Jump to Line 1168](../carddemo/COCRDUPC.cbl#L1168) |



### 3300-SETUP-SCREEN-ATTRS-EXIT

| | |
|---|---|
| **Paragraph** | `3300-SETUP-SCREEN-ATTRS-EXIT` |
| **Lines** | 1319 - 1323 |
| **View Code** | [Jump to Line 1319](../carddemo/COCRDUPC.cbl#L1319) |



### 3400-SEND-SCREEN

| | |
|---|---|
| **Paragraph** | `3400-SEND-SCREEN` |
| **Lines** | 1324 - 1337 |
| **View Code** | [Jump to Line 1324](../carddemo/COCRDUPC.cbl#L1324) |



### 3400-SEND-SCREEN-EXIT

| | |
|---|---|
| **Paragraph** | `3400-SEND-SCREEN-EXIT` |
| **Lines** | 1338 - 1342 |
| **View Code** | [Jump to Line 1338](../carddemo/COCRDUPC.cbl#L1338) |



### 9000-READ-DATA

| | |
|---|---|
| **Paragraph** | `9000-READ-DATA` |
| **Lines** | 1343 - 1371 |
| **View Code** | [Jump to Line 1343](../carddemo/COCRDUPC.cbl#L1343) |



### 9000-READ-DATA-EXIT

| | |
|---|---|
| **Paragraph** | `9000-READ-DATA-EXIT` |
| **Lines** | 1372 - 1375 |
| **View Code** | [Jump to Line 1372](../carddemo/COCRDUPC.cbl#L1372) |



### 9100-GETCARD-BYACCTCARD

| | |
|---|---|
| **Paragraph** | `9100-GETCARD-BYACCTCARD` |
| **Lines** | 1376 - 1414 |
| **View Code** | [Jump to Line 1376](../carddemo/COCRDUPC.cbl#L1376) |



### 9100-GETCARD-BYACCTCARD-EXIT

| | |
|---|---|
| **Paragraph** | `9100-GETCARD-BYACCTCARD-EXIT` |
| **Lines** | 1415 - 1419 |
| **View Code** | [Jump to Line 1415](../carddemo/COCRDUPC.cbl#L1415) |



### 9200-WRITE-PROCESSING

| | |
|---|---|
| **Paragraph** | `9200-WRITE-PROCESSING` |
| **Lines** | 1420 - 1493 |
| **View Code** | [Jump to Line 1420](../carddemo/COCRDUPC.cbl#L1420) |



### 9200-WRITE-PROCESSING-EXIT

| | |
|---|---|
| **Paragraph** | `9200-WRITE-PROCESSING-EXIT` |
| **Lines** | 1494 - 1497 |
| **View Code** | [Jump to Line 1494](../carddemo/COCRDUPC.cbl#L1494) |



### 9300-CHECK-CHANGE-IN-REC

| | |
|---|---|
| **Paragraph** | `9300-CHECK-CHANGE-IN-REC` |
| **Lines** | 1498 - 1520 |
| **View Code** | [Jump to Line 1498](../carddemo/COCRDUPC.cbl#L1498) |



### 9300-CHECK-CHANGE-IN-REC-EXIT

| | |
|---|---|
| **Paragraph** | `9300-CHECK-CHANGE-IN-REC-EXIT` |
| **Lines** | 1521 - 1530 |
| **View Code** | [Jump to Line 1521](../carddemo/COCRDUPC.cbl#L1521) |



### ABEND-ROUTINE

| | |
|---|---|
| **Paragraph** | `ABEND-ROUTINE` |
| **Lines** | 1531 - 1553 |
| **View Code** | [Jump to Line 1531](../carddemo/COCRDUPC.cbl#L1531) |



### ABEND-ROUTINE-EXIT

| | |
|---|---|
| **Paragraph** | `ABEND-ROUTINE-EXIT` |
| **Lines** | 1554 - 1560 |
| **View Code** | [Jump to Line 1554](../carddemo/COCRDUPC.cbl#L1554) |







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

### Copybook `COCRDUP`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CCRDUPAI` | `None` | None | None |  |
| `02` | `TRNNAMEL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `TRNNAMEF` | `X` | None | CCRDUPAI |  |
| `03` | `TRNNAMEA` | `X` | None | CCRDUPAI |  |
| `02` | `TRNNAMEI` | `X(4)` | None | CCRDUPAI |  |
| `02` | `TITLE01L` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `TITLE01F` | `X` | None | CCRDUPAI |  |
| `03` | `TITLE01A` | `X` | None | CCRDUPAI |  |
| `02` | `TITLE01I` | `X(40)` | None | CCRDUPAI |  |
| `02` | `CURDATEL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `CURDATEF` | `X` | None | CCRDUPAI |  |
| `03` | `CURDATEA` | `X` | None | CCRDUPAI |  |
| `02` | `CURDATEI` | `X(8)` | None | CCRDUPAI |  |
| `02` | `PGMNAMEL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `PGMNAMEF` | `X` | None | CCRDUPAI |  |
| `03` | `PGMNAMEA` | `X` | None | CCRDUPAI |  |
| `02` | `PGMNAMEI` | `X(8)` | None | CCRDUPAI |  |
| `02` | `TITLE02L` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `TITLE02F` | `X` | None | CCRDUPAI |  |
| `03` | `TITLE02A` | `X` | None | CCRDUPAI |  |
| `02` | `TITLE02I` | `X(40)` | None | CCRDUPAI |  |
| `02` | `CURTIMEL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `CURTIMEF` | `X` | None | CCRDUPAI |  |
| `03` | `CURTIMEA` | `X` | None | CCRDUPAI |  |
| `02` | `CURTIMEI` | `X(8)` | None | CCRDUPAI |  |
| `02` | `ACCTSIDL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `ACCTSIDF` | `X` | None | CCRDUPAI |  |
| `03` | `ACCTSIDA` | `X` | None | CCRDUPAI |  |
| `02` | `ACCTSIDI` | `X(11)` | None | CCRDUPAI |  |
| `02` | `CARDSIDL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `CARDSIDF` | `X` | None | CCRDUPAI |  |
| `03` | `CARDSIDA` | `X` | None | CCRDUPAI |  |
| `02` | `CARDSIDI` | `X(16)` | None | CCRDUPAI |  |
| `02` | `CRDNAMEL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `CRDNAMEF` | `X` | None | CCRDUPAI |  |
| `03` | `CRDNAMEA` | `X` | None | CCRDUPAI |  |
| `02` | `CRDNAMEI` | `X(50)` | None | CCRDUPAI |  |
| `02` | `CRDSTCDL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `CRDSTCDF` | `X` | None | CCRDUPAI |  |
| `03` | `CRDSTCDA` | `X` | None | CCRDUPAI |  |
| `02` | `CRDSTCDI` | `X(1)` | None | CCRDUPAI |  |
| `02` | `EXPMONL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `EXPMONF` | `X` | None | CCRDUPAI |  |
| `03` | `EXPMONA` | `X` | None | CCRDUPAI |  |
| `02` | `EXPMONI` | `X(2)` | None | CCRDUPAI |  |
| `02` | `EXPYEARL` | `S9(4)` | COMP | CCRDUPAI |  |
| `02` | `EXPYEARF` | `X` | None | CCRDUPAI |  |
| `03` | `EXPYEARA` | `X` | None | CCRDUPAI |  |
| `02` | `EXPYEARI` | `X(4)` | None | CCRDUPAI |  |
| `02` | `EXPDAYL` | `S9(4)` | COMP | CCRDUPAI |  |
*+ 105 more fields*
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

### Copybook `CSMSG02Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `ABEND-DATA` | `None` | None | None |  |
| `05` | `ABEND-CODE` | `X(4)` | None | ABEND-DATA |  |
| `05` | `ABEND-CULPRIT` | `X(8)` | None | ABEND-DATA |  |
| `05` | `ABEND-REASON` | `X(50)` | None | ABEND-DATA |  |
| `05` | `ABEND-MSG` | `X(72)` | None | ABEND-DATA |  |

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

### Copybook `CVACT02Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CARD-RECORD` | `None` | None | None |  |
| `05` | `CARD-NUM` | `X(16)` | None | CARD-RECORD |  |
| `05` | `CARD-ACCT-ID` | `9(11)` | None | CARD-RECORD |  |
| `05` | `CARD-CVV-CD` | `9(03)` | None | CARD-RECORD |  |
| `05` | `CARD-EMBOSSED-NAME` | `X(50)` | None | CARD-RECORD |  |
| `05` | `CARD-EXPIRAION-DATE` | `X(10)` | None | CARD-RECORD |  |
| `05` | `CARD-ACTIVE-STATUS` | `X(01)` | None | CARD-RECORD |  |

### Copybook `CVCRD01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CC-WORK-AREAS` | `None` | None | None |  |
| `05` | `CC-WORK-AREA` | `None` | None | CC-WORK-AREAS |  |
| `10` | `CCARD-AID` | `X(5)` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-ENTER` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-CLEAR` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PA1` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PA2` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK01` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK02` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK03` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK04` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK05` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK06` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK07` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK08` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK09` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK10` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK11` | `None` | None | CC-WORK-AREA |  |
| `88` | `CCARD-AID-PFK12` | `None` | None | CC-WORK-AREA |  |
| `10` | `CCARD-NEXT-PROG` | `X(8)` | None | CC-WORK-AREA |  |
| `10` | `CCARD-NEXT-MAPSET` | `X(7)` | None | CC-WORK-AREA |  |
| `10` | `CCARD-NEXT-MAP` | `X(7)` | None | CC-WORK-AREA |  |
| `10` | `CCARD-ERROR-MSG` | `X(75)` | None | CC-WORK-AREA |  |
| `10` | `CCARD-RETURN-MSG` | `X(75)` | None | CC-WORK-AREA |  |
| `88` | `CCARD-RETURN-MSG-OFF` | `None` | None | CC-WORK-AREA |  |
| `10` | `CC-ACCT-ID` | `X(11)` | None | CC-WORK-AREA |  |
| `10` | `CC-ACCT-ID-N` | `9(11)` | None | CC-WORK-AREA |  REDEFINES CC-ACCT-ID |
| `10` | `CC-CARD-NUM` | `X(16)` | None | CC-WORK-AREA |  |
| `10` | `CC-CARD-NUM-N` | `9(16)` | None | CC-WORK-AREA |  REDEFINES CC-CARD-NUM |
| `10` | `CC-CUST-ID` | `X(09)` | None | CC-WORK-AREA |  |
| `10` | `CC-CUST-ID-N` | `9(9)` | None | CC-WORK-AREA |  REDEFINES CC-CUST-ID |

### Copybook `CVCUS01Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CUSTOMER-RECORD` | `None` | None | None |  |
| `05` | `CUST-ID` | `9(09)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-FIRST-NAME` | `X(25)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-MIDDLE-NAME` | `X(25)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-LAST-NAME` | `X(25)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-LINE-1` | `X(50)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-LINE-2` | `X(50)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-LINE-3` | `X(50)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-STATE-CD` | `X(02)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-COUNTRY-CD` | `X(03)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-ADDR-ZIP` | `X(10)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-PHONE-NUM-1` | `X(15)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-PHONE-NUM-2` | `X(15)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-SSN` | `9(09)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-GOVT-ISSUED-ID` | `X(20)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-DOB-YYYY-MM-DD` | `X(10)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-EFT-ACCOUNT-ID` | `X(10)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-PRI-CARD-HOLDER-IND` | `X(01)` | None | CUSTOMER-RECORD |  |
| `05` | `CUST-FICO-CREDIT-SCORE` | `9(03)` | None | CUSTOMER-RECORD |  |

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
| `LIT-THISTRANID` | `WS-TRANID` | 0000-MAIN | 380 |
| `LIT-MENUTRANID` | `CDEMO-TO-TRANID` | 0000-MAIN | 444 |
| `CDEMO-FROM-TRANID` | `CDEMO-TO-TRANID` | 0000-MAIN | 446 |
| `LIT-MENUPGM` | `CDEMO-TO-PROGRAM` | 0000-MAIN | 451 |
| `CDEMO-FROM-PROGRAM` | `CDEMO-TO-PROGRAM` | 0000-MAIN | 453 |
| `LIT-THISTRANID` | `CDEMO-FROM-TRANID` | 0000-MAIN | 456 |
| `LIT-THISPGM` | `CDEMO-FROM-PROGRAM` | 0000-MAIN | 457 |
| `ZEROS` | `CDEMO-ACCT-ID` | 0000-MAIN | 460 |
| `LIT-THISMAPSET` | `CDEMO-LAST-MAPSET` | 0000-MAIN | 466 |
| `LIT-THISMAP` | `CDEMO-LAST-MAP` | 0000-MAIN | 467 |
| `CDEMO-ACCT-ID` | `CC-ACCT-ID-N` | 0000-MAIN | 490 |
| `CDEMO-CARD-NUM` | `CC-CARD-NUM-N` | 0000-MAIN | 491 |
| `WS-RETURN-MSG` | `CCARD-ERROR-MSG` | COMMON-RETURN | 547 |
| `CARDDEMO-COMMAREA` | `WS-COMMAREA` | COMMON-RETURN | 549 |
| `WS-RETURN-MSG` | `CCARD-ERROR-MSG` | 1000-PROCESS-INPUTS | 569 |
| `LIT-THISPGM` | `CCARD-NEXT-PROG` | 1000-PROCESS-INPUTS | 570 |
| `LIT-THISMAPSET` | `CCARD-NEXT-MAPSET` | 1000-PROCESS-INPUTS | 571 |
| `LIT-THISMAP` | `CCARD-NEXT-MAP` | 1000-PROCESS-INPUTS | 572 |
| `LOW-VALUES` | `CC-ACCT-ID` | 1100-RECEIVE-MAP | 591 |
| `LOW-VALUES` | `CC-CARD-NUM` | 1100-RECEIVE-MAP | 600 |
| `LOW-VALUES` | `CCUP-NEW-CRDNAME` | 1100-RECEIVE-MAP | 609 |
| `LOW-VALUES` | `CCUP-NEW-CRDSTCD` | 1100-RECEIVE-MAP | 616 |
| `LOW-VALUES` | `CCUP-NEW-EXPMON` | 1100-RECEIVE-MAP | 625 |
| `LOW-VALUES` | `CCUP-NEW-EXPYEAR` | 1100-RECEIVE-MAP | 632 |
| `LOW-VALUES` | `CCUP-NEW-CARDDATA` | 1200-EDIT-MAP-INPUTS | 653 |
| `CCUP-OLD-ACCTID` | `CDEMO-ACCT-ID` | 1200-EDIT-MAP-INPUTS | 671 |
| `CCUP-OLD-CARDID` | `CDEMO-CARD-NUM` | 1200-EDIT-MAP-INPUTS | 672 |
| `CCUP-OLD-CRDNAME` | `CARD-EMBOSSED-NAME` | 1200-EDIT-MAP-INPUTS | 673 |
| `CCUP-OLD-CRDSTCD` | `CARD-ACTIVE-STATUS` | 1200-EDIT-MAP-INPUTS | 674 |
| `CCUP-OLD-EXPDAY` | `CARD-EXPIRY-DAY` | 1200-EDIT-MAP-INPUTS | 675 |
| `CCUP-OLD-EXPMON` | `CARD-EXPIRY-MONTH` | 1200-EDIT-MAP-INPUTS | 676 |
| `CCUP-OLD-EXPYEAR` | `CARD-EXPIRY-YEAR` | 1200-EDIT-MAP-INPUTS | 677 |
| `ZEROES` | `CDEMO-ACCT-ID` | 1210-EDIT-ACCOUNT | 733 |
| `LOW-VALUES` | `CCUP-NEW-ACCTID` | 1210-EDIT-ACCOUNT | 734 |
| `ZERO` | `CDEMO-ACCT-ID` | 1210-EDIT-ACCOUNT | 748 |
| `LOW-VALUES` | `CCUP-NEW-ACCTID` | 1210-EDIT-ACCOUNT | 749 |
| `CC-ACCT-ID` | `CDEMO-ACCT-ID` | 1210-EDIT-ACCOUNT | 752 |
| `ZEROES` | `CDEMO-CARD-NUM` | 1220-EDIT-CARD | 777 |
| `ZERO` | `CDEMO-CARD-NUM` | 1220-EDIT-CARD | 792 |
| `LOW-VALUES` | `CCUP-NEW-CARDID` | 1220-EDIT-CARD | 793 |
| `CC-CARD-NUM-N` | `CDEMO-CARD-NUM` | 1220-EDIT-CARD | 796 |
| `CC-CARD-NUM` | `CCUP-NEW-CARDID` | 1220-EDIT-CARD | 797 |
| `CCUP-NEW-CRDNAME` | `CARD-NAME-CHECK` | 1230-EDIT-NAME | 823 |
| `CCUP-NEW-CRDSTCD` | `FLG-YES-NO-CHECK` | 1240-EDIT-CARDSTATUS | 861 |
| `CCUP-NEW-EXPMON` | `CARD-MONTH-CHECK` | 1250-EDIT-EXPIRY-MON | 896 |
| `CCUP-NEW-EXPYEAR` | `CARD-YEAR-CHECK` | 1260-EDIT-EXPIRY-YEAR | 932 |
| `ZEROES` | `CDEMO-ACCT-ID` | 2000-DECIDE-ACTION | 1015 |
| `LOW-VALUES` | `CDEMO-ACCT-STATUS` | 2000-DECIDE-ACTION | 1017 |
| `LIT-THISPGM` | `ABEND-CULPRIT` | 2000-DECIDE-ACTION | 1020 |
| `'0001'` | `ABEND-CODE` | 2000-DECIDE-ACTION | 1021 |
| `SPACES` | `ABEND-REASON` | 2000-DECIDE-ACTION | 1022 |
| `LOW-VALUES` | `CCRDUPAO` | 3100-SCREEN-INIT | 1053 |
| `CCDA-TITLE01` | `TITLE01O` | 3100-SCREEN-INIT | 1057 |
| `CCDA-TITLE01` | `OF` | 3100-SCREEN-INIT | 1057 |
| `CCDA-TITLE01` | `CCRDUPAO` | 3100-SCREEN-INIT | 1057 |
| `CCDA-TITLE02` | `TITLE02O` | 3100-SCREEN-INIT | 1058 |
| `CCDA-TITLE02` | `OF` | 3100-SCREEN-INIT | 1058 |
| `CCDA-TITLE02` | `CCRDUPAO` | 3100-SCREEN-INIT | 1058 |
| `LIT-THISTRANID` | `TRNNAMEO` | 3100-SCREEN-INIT | 1059 |
| `LIT-THISTRANID` | `OF` | 3100-SCREEN-INIT | 1059 |
*+ 40 more movements*

## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEAD_CODE | Variable `WS-INPUT-FLAG` is declared but never referenced | None | 53 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-ACCT-FLAG` is declared but never referenced | None | 57 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-CARD-FLAG` is declared but never referenced | None | 61 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-CARDNAME-FLAG` is declared but never referenced | None | 65 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-CARDSTATUS-FLAG` is declared but never referenced | None | 69 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-CARDEXPMON-FLAG` is declared but never referenced | None | 73 |
| **NOTICE** | DEAD_CODE | Variable `WS-EDIT-CARDEXPYEAR-FLAG` is declared but never referenced | None | 77 |
| **NOTICE** | DEAD_CODE | Variable `WS-PFK-FLAG` is declared but never referenced | None | 84 |
| **NOTICE** | DEAD_CODE | Variable `WS-LONG-MSG` is declared but never referenced | None | 156 |
| **NOTICE** | DEAD_CODE | Variable `LIT-CCLISTTRANID` is declared but never referenced | None | 229 |

### NOTICE — Variable `WS-INPUT-FLAG` is declared but never referenced

`WS-INPUT-FLAG` is declared at line 53 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 53):
```cobol
05  WS-INPUT-FLAG                         PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-ACCT-FLAG` is declared but never referenced

`WS-EDIT-ACCT-FLAG` is declared at line 57 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 57):
```cobol
05  WS-EDIT-ACCT-FLAG                     PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-CARD-FLAG` is declared but never referenced

`WS-EDIT-CARD-FLAG` is declared at line 61 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 61):
```cobol
05  WS-EDIT-CARD-FLAG                     PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-CARDNAME-FLAG` is declared but never referenced

`WS-EDIT-CARDNAME-FLAG` is declared at line 65 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 65):
```cobol
05  WS-EDIT-CARDNAME-FLAG                 PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-CARDSTATUS-FLAG` is declared but never referenced

`WS-EDIT-CARDSTATUS-FLAG` is declared at line 69 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 69):
```cobol
05  WS-EDIT-CARDSTATUS-FLAG              PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-CARDEXPMON-FLAG` is declared but never referenced

`WS-EDIT-CARDEXPMON-FLAG` is declared at line 73 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 73):
```cobol
05  WS-EDIT-CARDEXPMON-FLAG              PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-EDIT-CARDEXPYEAR-FLAG` is declared but never referenced

`WS-EDIT-CARDEXPYEAR-FLAG` is declared at line 77 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 77):
```cobol
05  WS-EDIT-CARDEXPYEAR-FLAG             PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-PFK-FLAG` is declared but never referenced

`WS-PFK-FLAG` is declared at line 84 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 84):
```cobol
05  WS-PFK-FLAG                           PIC X(1).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `WS-LONG-MSG` is declared but never referenced

`WS-LONG-MSG` is declared at line 156 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 156):
```cobol
05  WS-LONG-MSG                           PIC X(500).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `LIT-CCLISTTRANID` is declared but never referenced

`LIT-CCLISTTRANID` is declared at line 229 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 229):
```cobol
05 LIT-CCLISTTRANID                      PIC X(4)
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---




## Decision Tables (EVALUATE / WHEN)

Captured from the source. Each EVALUATE block is a structured decision the
migration team should turn into either a switch / pattern-match or a rules table.

### EVALUATE `TRUE` — paragraph `3200-SETUP-SCREEN-VARS` (line 1124)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE CCUP-OLD-CRDNAME    TO CRDNAMEO OF CCRDUPAO |
| `CCUP-DETAILS-NOT-FETCHED` | MOVE LOW-VALUES         TO CRDNAMEO OF CCRDUPAO |
| `CCUP-SHOW-DETAILS` | MOVE CCUP-OLD-CRDNAME    TO CRDNAMEO OF CCRDUPAO |
| `CCUP-CHANGES-MADE` | MOVE CCUP-NEW-CRDNAME    TO CRDNAMEO OF CCRDUPAO |

### EVALUATE `TRUE` — paragraph `3250-SETUP-INFOMSG` (line 1141)

| WHEN | Action |
|------|--------|
| `CDEMO-PGM-ENTER` | SET  PROMPT-FOR-SEARCH-KEYS TO TRUE |
| `CCUP-DETAILS-NOT-FETCHED` | SET PROMPT-FOR-SEARCH-KEYS      TO TRUE |
| `CCUP-SHOW-DETAILS` | SET FOUND-CARDS-FOR-ACCOUNT    TO TRUE |
| `CCUP-CHANGES-NOT-OK` | SET PROMPT-FOR-CHANGES         TO TRUE |
| `CCUP-CHANGES-OK-NOT-CONFIRMED` | SET PROMPT-FOR-CONFIRMATION    TO TRUE |
| `CCUP-CHANGES-OKAYED-AND-DONE` | SET CONFIRM-UPDATE-SUCCESS     TO TRUE |
| `CCUP-CHANGES-OKAYED-LOCK-ERROR` | SET INFORM-FAILURE             TO TRUE |
| `CCUP-CHANGES-OKAYED-BUT-FAILED` | SET INFORM-FAILURE             TO TRUE |
| `WS-NO-INFO-MESSAGE` | SET PROMPT-FOR-SEARCH-KEYS      TO TRUE |

### EVALUATE `TRUE` — paragraph `3300-SETUP-SCREEN-ATTRS` (line 1200)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE DFHBMFSE      TO ACCTSIDA OF CCRDUPAI |
| `CCUP-DETAILS-NOT-FETCHED` | MOVE DFHBMFSE      TO ACCTSIDA OF CCRDUPAI |
| `CCUP-SHOW-DETAILS` |  |
| `CCUP-CHANGES-NOT-OK` | MOVE DFHBMPRF      TO ACCTSIDA OF CCRDUPAI |
| `CCUP-CHANGES-OK-NOT-CONFIRMED` |  |
| `CCUP-CHANGES-OKAYED-AND-DONE` | MOVE DFHBMPRF      TO ACCTSIDA OF CCRDUPAI |

### EVALUATE `TRUE` — paragraph `3300-SETUP-SCREEN-ATTRS` (line 1233)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE -1              TO ACCTSIDL OF CCRDUPAI |
| `FOUND-CARDS-FOR-ACCOUNT` |  |
| `NO-CHANGES-DETECTED` | MOVE -1              TO CRDNAMEL OF CCRDUPAI |
| `FLG-ACCTFILTER-NOT-OK` |  |
| `FLG-ACCTFILTER-BLANK` | MOVE -1             TO ACCTSIDL OF CCRDUPAI |
| `FLG-CARDFILTER-NOT-OK` |  |
| `FLG-CARDFILTER-BLANK` | MOVE -1             TO CARDSIDL OF CCRDUPAI |
| `FLG-CARDNAME-NOT-OK` |  |
| `FLG-CARDNAME-BLANK` | MOVE -1              TO CRDNAMEL OF  CCRDUPAI |
| `FLG-CARDSTATUS-NOT-OK` |  |
| `FLG-CARDSTATUS-BLANK` | MOVE -1              TO CRDSTCDL OF  CCRDUPAI |
| `FLG-CARDEXPMON-NOT-OK` |  |
| `FLG-CARDEXPMON-BLANK` | MOVE -1              TO EXPMONL  OF  CCRDUPAI |
| `FLG-CARDEXPYEAR-NOT-OK` |  |
| `FLG-CARDEXPYEAR-BLANK` | MOVE -1              TO EXPYEARL OF  CCRDUPAI |

### EVALUATE `WS-RESP-CD` — paragraph `9100-GETCARD-BYACCTCARD` (line 1402)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | SET INPUT-ERROR                    TO TRUE |
| `DFHRESP(NORMAL)` | SET FOUND-CARDS-FOR-ACCOUNT TO TRUE |
| `DFHRESP(NOTFND)` | SET INPUT-ERROR                    TO TRUE |

### EVALUATE `TRUE` — paragraph `0000-MAIN` (line 535)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | PERFORM 1000-PROCESS-INPUTS |
| `CCARD-AID-PFK03` |  |
| `(CCUP-CHANGES-OKAYED-AND-DONE` | AND  CDEMO-LAST-MAPSET   EQUAL LIT-CCLISTMAPSET) |
| `(CCUP-CHANGES-FAILED` | AND  CDEMO-LAST-MAPSET   EQUAL LIT-CCLISTMAPSET) |
| `CDEMO-PGM-ENTER` | AND CDEMO-FROM-PROGRAM  EQUAL LIT-CCLISTPGM |
| `CCARD-AID-PFK12` | AND CDEMO-FROM-PROGRAM  EQUAL LIT-CCLISTPGM |
| `CCUP-DETAILS-NOT-FETCHED` | AND CDEMO-PGM-ENTER |
| `CDEMO-FROM-PROGRAM   EQUAL LIT-MENUPGM` | AND NOT CDEMO-PGM-REENTER |
| `CCUP-CHANGES-OKAYED-AND-DONE` |  |
| `CCUP-CHANGES-FAILED` | INITIALIZE WS-THIS-PROGCOMMAREA |

### EVALUATE `TRUE` — paragraph `2000-DECIDE-ACTION` (line 1019)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | MOVE LIT-THISPGM    TO ABEND-CULPRIT |
| `CCUP-DETAILS-NOT-FETCHED` |  |
| `CCARD-AID-PFK12` | IF  FLG-ACCTFILTER-ISVALID |
| `CCUP-SHOW-DETAILS` | IF INPUT-ERROR |
| `CCUP-CHANGES-NOT-OK` | CONTINUE |
| `CCUP-CHANGES-OK-NOT-CONFIRMED` | AND CCARD-AID-PFK05 |
| `CCUP-CHANGES-OK-NOT-CONFIRMED` | CONTINUE |
| `CCUP-CHANGES-OKAYED-AND-DONE` | SET CCUP-SHOW-DETAILS TO TRUE |

### EVALUATE `TRUE` — paragraph `2000-DECIDE-ACTION` (line 999)

| WHEN | Action |
|------|--------|
| **WHEN OTHER** | SET CCUP-CHANGES-OKAYED-AND-DONE   TO TRUE |
| `COULD-NOT-LOCK-FOR-UPDATE` | SET CCUP-CHANGES-OKAYED-LOCK-ERROR TO TRUE |
| `LOCKED-BUT-UPDATE-FAILED` | SET CCUP-CHANGES-OKAYED-BUT-FAILED TO TRUE |
| `DATA-WAS-CHANGED-BEFORE-UPDATE` | SET CCUP-SHOW-DETAILS            TO TRUE |


## CICS HANDLE Routing

Each entry shows where exceptional CICS conditions are routed. Migration to a
modern stack should map these to try / catch handlers or middleware filters.

| Type | Condition | Target Paragraph | Line |
|------|-----------|------------------|------|
| ABEND | `LABEL` | `ABEND-ROUTINE` | 370 |
| ABEND | `ABEND-ROUTINE` | *(suspend / cancel prior handler)* | 370 |
| ABEND | `CANCEL` | *(suspend / cancel prior handler)* | 1546 |




## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*

## Key Data Items

*No data items found for this program.*

---

*Generated 2026-05-12 12:18*