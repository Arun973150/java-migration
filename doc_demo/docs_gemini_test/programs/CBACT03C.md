# Program: CBACT03C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `CBACT03C` |
| Type | BATCH |
| Lines | 179 |
| Source | [CBACT03C.cbl](../carddemo/CBACT03C.cbl#L1) |
| Paragraphs | 5 |
| Statements | 34 |
| Impact Risk | **HIGH** — 13 programs affected |

> **View Source:** [Open CBACT03C.cbl](../carddemo/CBACT03C.cbl#L1)

## Source Grounding Facts

| Data Item | Literal Value |
|-----------|---------------|
| `END-OF-FILE` | `N` |

Status conditions found in source:
- `XREFFILE-STATUS = '00'`
- `XREFFILE-STATUS = '10'`


## Business Purpose

*Business purpose is not present in the extracted data. Run LLM enrichment to populate this section.*



## Dependency Context

> This section shows how **CBACT03C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call CBACT03C (Callers)

*No programs call CBACT03C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by CBACT03C (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| `UNKNOWN` | None | 169 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CVACT03Y` | CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C (+8 more) | 13 |

#### Shared Files

| File | Type | Access | Also Used By |
|------|------|--------|-------------|
| `XREFFILE-FILE` | VSAM | SEQUENTIAL |  |

## Legacy Data Contracts

> These tables are derived from FILE SECTION records and COPY-expanded data declarations. They preserve the legacy field names, COBOL storage type, inferred modern type, and status-code values needed for Java DTOs, SQL schemas, API contracts, and migration mapping.

### File Record Layouts

#### `XREFFILE-FILE` / `FD-XREFFILE-REC`
| Legacy Field | Meaning | COBOL Type | Modern Type | Notes |
|--------------|---------|------------|-------------|-------|
| `FD-XREFFILE-REC` | Fd Xreffile Record | `GROUP` | `OBJECT` |  |
| `FD-XREF-CARD-NUM` | Fd Xref Card Number | `PIC X(16)` | `STRING(16)` |  |
| `FD-XREF-DATA` | Fd Xref Data | `PIC X(34)` | `STRING(34)` |  |


### Copybook Segment Layouts

#### `CVACT03Y` as `CARD-XREF-RECORD`

| Legacy Field | Meaning | COBOL Type | Modern Type | Status / Format Notes |
|--------------|---------|------------|-------------|-----------------------|
| `CARD-XREF-RECORD` | Card Xref Record | `GROUP` | `OBJECT` |  |
| `XREF-CARD-NUM` | Xref Card Number | `PIC X(16)` | `STRING(16)` |  |
| `XREF-CUST-ID` | Xref Customer ID | `PIC 9(09)` | `INTEGER` |  |
| `XREF-ACCT-ID` | Xref Account ID | `PIC 9(11)` | `BIGINT` |  |
| `FILLER` | Filler | `PIC X(14)` | `STRING(14)` |  |


### Data Movement And Key Mapping

| Line | Source | Target | Meaning |
|------|--------|--------|---------|
| 108 | `'Y'` | `END-OF-FILE` | 'Y' populates END-OF-FILE |
| 111 | `XREFFILE-STATUS` | `IO-STATUS` | XREFFILE-STATUS populates IO-STATUS |
| 130 | `XREFFILE-STATUS` | `IO-STATUS` | XREFFILE-STATUS populates IO-STATUS |
| 148 | `XREFFILE-STATUS` | `IO-STATUS` | XREFFILE-STATUS populates IO-STATUS |
| 164 | `IO-STAT1` | `IO-STATUS-04(1:1)` | IO-STAT1 populates IO-STATUS-04(1:1) |
| 167 | `TWO-BYTES-BINARY` | `IO-STATUS-0403` | TWO-BYTES-BINARY populates IO-STATUS-0403 |
| 170 | `'0000'` | `IO-STATUS-04` | '0000' populates IO-STATUS-04 |
| 171 | `IO-STATUS` | `IO-STATUS-04(3:2)` | IO-STATUS populates IO-STATUS-04(3:2) |



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
| IF | 18 |
| EXIT | 4 |
| MOVE | 3 |
| READ | 2 |
| OPEN | 2 |
| CLOSE | 2 |
| DISPLAY | 1 |
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
| **Lines** | 92 - 117 |
| **View Code** | [Jump to Line 92](../carddemo/CBACT03C.cbl#L92) |



### 0000-XREFFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0000-XREFFILE-OPEN` |
| **Lines** | 118 - 135 |
| **View Code** | [Jump to Line 118](../carddemo/CBACT03C.cbl#L118) |



### 9000-XREFFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9000-XREFFILE-CLOSE` |
| **Lines** | 136 - 153 |
| **View Code** | [Jump to Line 136](../carddemo/CBACT03C.cbl#L136) |



### 9999-ABEND-PROGRAM

| | |
|---|---|
| **Paragraph** | `9999-ABEND-PROGRAM` |
| **Lines** | 154 - 160 |
| **View Code** | [Jump to Line 154](../carddemo/CBACT03C.cbl#L154) |



### 9910-DISPLAY-IO-STATUS

| | |
|---|---|
| **Paragraph** | `9910-DISPLAY-IO-STATUS` |
| **Lines** | 161 - 178 |
| **View Code** | [Jump to Line 161](../carddemo/CBACT03C.cbl#L161) |




## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
| [READXREF](../jcl/READXREF.md) | `STEP05` | *****************************************************************
Copyright Amaz... |




## Copybook Field Dictionaries

The following copybooks are included by this program. Each entry shows the actual fields
extracted from the copybook source file (`.cpy`).

### Copybook `CVACT03Y`

| Level | Field | PIC | USAGE | Parent | Notes |
|-------|-------|-----|-------|--------|-------|
| `01` | `CARD-XREF-RECORD` | `None` | None | None |  |
| `05` | `XREF-CARD-NUM` | `X(16)` | None | CARD-XREF-RECORD |  |
| `05` | `XREF-CUST-ID` | `9(09)` | None | CARD-XREF-RECORD |  |
| `05` | `XREF-ACCT-ID` | `9(11)` | None | CARD-XREF-RECORD |  |


## File Record Layouts (FD)

This program declares the following file records (data contracts for I/O):

### `FD XREFFILE-FILE` (record `FD-XREFFILE-REC`)

| Level | Field | PIC | USAGE | Parent |
|-------|-------|-----|-------|--------|
| `01` | `FD-XREFFILE-REC` | `None` | None | None |
| `05` | `FD-XREF-CARD-NUM` | `X(16)` | None | FD-XREFFILE-REC |
| `05` | `FD-XREF-DATA` | `X(34)` | None | FD-XREFFILE-REC |


## Data Lineage (MOVE Flow)

The following MOVE statements were extracted from the source. Each row is a `source → destination`
flow that the migration team can use to trace how data is reshaped and routed.

| Source | Destination | Paragraph | Line |
|--------|-------------|-----------|------|
| `'0'` | `APPL-RESULT` | 1000-XREFFILE-GET-NEXT | 95 |
| `'16'` | `APPL-RESULT` | 1000-XREFFILE-GET-NEXT | 99 |
| `'12'` | `APPL-RESULT` | 1000-XREFFILE-GET-NEXT | 101 |
| `'Y'` | `END-OF-FILE` | 1000-XREFFILE-GET-NEXT | 108 |
| `XREFFILE-STATUS` | `IO-STATUS` | 1000-XREFFILE-GET-NEXT | 111 |
| `'8'` | `APPL-RESULT` | 0000-XREFFILE-OPEN | 119 |
| `'0'` | `APPL-RESULT` | 0000-XREFFILE-OPEN | 122 |
| `'12'` | `APPL-RESULT` | 0000-XREFFILE-OPEN | 124 |
| `XREFFILE-STATUS` | `IO-STATUS` | 0000-XREFFILE-OPEN | 130 |
| `XREFFILE-STATUS` | `IO-STATUS` | 9000-XREFFILE-CLOSE | 148 |
| `'0'` | `TIMING` | 9999-ABEND-PROGRAM | 156 |
| `'999'` | `ABCODE` | 9999-ABEND-PROGRAM | 157 |
| `IO-STAT1` | `IO-STATUS-04` | 9910-DISPLAY-IO-STATUS | 164 |
| `'0'` | `TWO-BYTES-BINARY` | 9910-DISPLAY-IO-STATUS | 165 |
| `IO-STAT2` | `TWO-BYTES-RIGHT` | 9910-DISPLAY-IO-STATUS | 166 |
| `TWO-BYTES-BINARY` | `IO-STATUS-0403` | 9910-DISPLAY-IO-STATUS | 167 |
| `'0000'` | `IO-STATUS-04` | 9910-DISPLAY-IO-STATUS | 170 |
| `IO-STATUS` | `IO-STATUS-04` | 9910-DISPLAY-IO-STATUS | 171 |


## Known Issues & Code Anomalies

Static analysis flagged the following items in this program. Migration teams should
review each one before re-implementing in a modern stack.

| Severity | Category | Title | Paragraph | Line |
|----------|----------|-------|-----------|------|
| **NOTICE** | DEAD_CODE | Variable `FD-XREF-DATA` is declared but never referenced | None | 40 |
| **NOTICE** | DEAD_CODE | Variable `XREFFILE-STAT1` is declared but never referenced | None | 47 |
| **NOTICE** | DEAD_CODE | Variable `XREFFILE-STAT2` is declared but never referenced | None | 48 |
| **NOTICE** | DEAD_CODE | Variable `TWO-BYTES-LEFT` is declared but never referenced | None | 55 |
| **NOTICE** | DEAD_CODE | Variable `IO-STATUS-0401` is declared but never referenced | None | 58 |
| **NOTICE** | LOGIC | Paragraph `1000-XREFFILE-GET-NEXT` terminates the program on error | 1000-XREFFILE-GET-NEXT | 92 |
| **NOTICE** | LOGIC | Paragraph `0000-XREFFILE-OPEN` terminates the program on error | 0000-XREFFILE-OPEN | 118 |
| **NOTICE** | LOGIC | Paragraph `9000-XREFFILE-CLOSE` terminates the program on error | 9000-XREFFILE-CLOSE | 136 |
| **NOTICE** | DEPENDENCY | Static CALL to external `CEE3ABD` (not in this codebase) | None | 158 |

### NOTICE — Variable `FD-XREF-DATA` is declared but never referenced

`FD-XREF-DATA` is declared at line 40 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 40):
```cobol
05 FD-XREF-DATA                      PIC X(34).
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `XREFFILE-STAT1` is declared but never referenced

`XREFFILE-STAT1` is declared at line 47 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 47):
```cobol
05  XREFFILE-STAT1      PIC X.
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `XREFFILE-STAT2` is declared but never referenced

`XREFFILE-STAT2` is declared at line 48 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 48):
```cobol
05  XREFFILE-STAT2      PIC X.
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `TWO-BYTES-LEFT` is declared but never referenced

`TWO-BYTES-LEFT` is declared at line 55 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 55):
```cobol
05  TWO-BYTES-LEFT      PIC X.
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Variable `IO-STATUS-0401` is declared but never referenced

`IO-STATUS-0401` is declared at line 58 but no other statement reads or writes it. Likely a leftover from prior refactoring or an incomplete feature.
**Source excerpt** (line 58):
```cobol
05  IO-STATUS-0401      PIC 9   VALUE 0.
```

**Recommendation:** Remove the declaration or wire it into the logic that was originally intended.
---
### NOTICE — Paragraph `1000-XREFFILE-GET-NEXT` terminates the program on error

`1000-XREFFILE-GET-NEXT` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Paragraph `0000-XREFFILE-OPEN` terminates the program on error

`0000-XREFFILE-OPEN` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Paragraph `9000-XREFFILE-CLOSE` terminates the program on error

`9000-XREFFILE-CLOSE` calls an ABEND routine (or STOP RUN) on the failure path. This means an error here ENDS the entire program — it does NOT reject, skip, or log-and-continue. Documentation must use "abend" / "terminate" language, not "reject".

**Recommendation:** Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.
---
### NOTICE — Static CALL to external `CEE3ABD` (not in this codebase)

`CALL 'CEE3ABD'` appears in the source but `CEE3ABD` is not a program in the loaded codebase. IBM Language Environment ABEND service (forces program termination with a user code).
**Source excerpt** (line 158):
```cobol
CALL 'CEE3ABD' USING ABCODE, TIMING.
```

**Recommendation:** Document this external dependency in the Migration Notes — the modern equivalent must replicate its behaviour.
---


## File OPEN / CLOSE Operations

The exact OPEN mode (INPUT / OUTPUT / I-O / EXTEND) determines whether a file can be
read, written, or both — and whether REWRITE / DELETE are legal. This table is the
source of truth for migrators converting to modern storage layers.

| File | Operation | Mode | Paragraph | Line |
|------|-----------|------|-----------|------|
| `XREFFILE-FILE` | OPEN | INPUT | 0000-XREFFILE-OPEN | 120 |
| `XREFFILE-FILE` | CLOSE | None | 9000-XREFFILE-CLOSE | 138 |







## Modernization Review Findings

These are source-derived review notes that should be checked before translating this program into Java, Spring Boot, SQL, APIs, or batch jobs.

| Finding | Why It Matters |
|---------|----------------|
| Nested IF blocks need compiler-accurate validation | Nested conditional logic was detected. During migration, validate scope with the original compiler rules and explicit `END-IF`/period termination before translating to Java or SQL. |


## Business Rules

- **Cross-Reference File Read Error** `BR-069`  
  If there is a problem reading a record from the card cross-reference file, the system should display an error message indicating the file status.  
  [View Rule Details](../business-rules/BR-069.md)
- **End of Cross-Reference File Processing** `BR-070`  
  When the end of the card cross-reference file is reached, the system should close the file and proceed to the next step.  
  [View Rule Details](../business-rules/BR-070.md)
- **Cross-Reference File Open Successful** `BR-071`  
  The cross-reference file must open successfully before processing can continue.  
  [View Rule Details](../business-rules/BR-071.md)
- **Cross-Reference File Read Successful** `BR-072`  
  The cross-reference file must be read successfully.  
  [View Rule Details](../business-rules/BR-072.md)
- **Cross-Reference File Close Successful** `BR-073`  
  The cross-reference file should be closed successfully at the end of processing.  
  [View Rule Details](../business-rules/BR-073.md)
- **Handle Cross-Reference File Close Error** `BR-074`  
  If an error occurs while closing the cross-reference file, the program should handle the error.  
  [View Rule Details](../business-rules/BR-074.md)
- **Cross-Reference File Read Error** `BR-075`  
  If there is an issue reading the cross-reference file, the program will display an error message.  
  [View Rule Details](../business-rules/BR-075.md)
- **Cross-Reference File Write Error** `BR-076`  
  If there is an issue writing to the cross-reference file, the program will display an error message.  
  [View Rule Details](../business-rules/BR-076.md)

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

*Generated 2026-05-12 12:18*