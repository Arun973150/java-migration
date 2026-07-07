# JCL English Documentation: CARDFILE

## 1. Executive Summary

`CARDFILE` is a standalone batch job defined in `CARDFILE.jcl`. The extracted job description is: Delete define card data. It contains 8 execution step(s), reading 3 input dataset reference(s) and writing 2 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\CARDFILE.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: SDSF
- Main utilities: IDCAMS
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `CLCIFIL`

This step executes `SDSF` and runs application processing. It has 3 DD statement(s).
Extracted step notes: Close files in CICS region
- Inputs: inline control data
- Outputs: ISFOUT, CMDOUT
- Inline SYSIN: 2 control line(s) are supplied to the step.

### Step 2: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DELETE CARD DATA VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 6 control line(s) are supplied to the step.

### Step 3: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE CARD DATA VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 14 control line(s) are supplied to the step.

### Step 4: `STEP15`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: COPY DATA FROM FLAT FILE TO VSAM FILE
- Inputs: AWS.M2.CARDDEMO.CARDDATA.PS, AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 5: `STEP40`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- CREATE ALTERNATE INDEX ON ACCT ID
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 10 control line(s) are supplied to the step.

### Step 6: `STEP50`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- DEFINE PATH IS USED TO RELATE THE ALTERNATE INDEX TO BASE CLUSTER
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 7: `STEP60`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: ------------------------------------------------------------------ BUILD ALTERNATE INDEX CLUSTER -------------------------------------------------------------------
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 8: `OPCIFIL`

This step executes `SDSF` and runs application processing. It has 3 DD statement(s).
Extracted step notes: Open files in CICS region
- Inputs: inline control data
- Outputs: ISFOUT, CMDOUT
- Inline SYSIN: 2 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.CARDDATA.PS, AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS
- Output datasets: ISFOUT, CMDOUT
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, READCARD/STEP05
- Peer/upstream references to the flat-file inputs: not present in extracted data

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBACT02C` / `CARDFILE-FILE` / `FD-CARDFILE-REC`: `FD-CARDFILE-REC` PIC `-`
- `CBACT02C` / `CARDFILE-FILE` / `FD-CARDFILE-REC`: `FD-CARD-NUM` PIC `X(16)`
- `CBACT02C` / `CARDFILE-FILE` / `FD-CARDFILE-REC`: `FD-CARD-DATA` PIC `X(134)`
- `CBACT03C` / `XREFFILE-FILE` / `FD-XREFFILE-REC`: `FD-XREF-CARD-NUM` PIC `X(16)`
- `CBACT04C` / `XREF-FILE` / `FD-XREFFILE-REC`: `FD-XREF-CARD-NUM` PIC `X(16)`
- `CBSTM03B` / `TRNX-FILE` / `FD-TRNXFILE-REC`: `FD-TRNX-CARD` PIC `X(16)`
- `CBSTM03B` / `XREF-FILE` / `FD-XREFFILE-REC`: `FD-XREF-CARD-NUM` PIC `X(16)`
- `CBTRN01C` / `CARD-FILE` / `FD-CARDFILE-REC`: `FD-CARDFILE-REC` PIC `-`
- `CBTRN01C` / `CARD-FILE` / `FD-CARDFILE-REC`: `FD-CARD-NUM` PIC `X(16)`
- `CBTRN01C` / `CARD-FILE` / `FD-CARDFILE-REC`: `FD-CARD-DATA` PIC `X(134)`
Copybook field evidence suggests the logical account record layout is:
- Copybook `CCPAURLY` field `PA-RL-CARD-NUM` PIC `X(16)`
- Copybook `CCPAURQY` field `PA-RQ-CARD-NUM` PIC `X(16)`
- Copybook `CCPAURQY` field `PA-RQ-CARD-EXPIRY-DATE` PIC `X(04)`
- Copybook `CIPAUDTY` field `PA-CARD-NUM` PIC `X(16)`
- Copybook `CIPAUDTY` field `PA-CARD-EXPIRY-DATE` PIC `X(04)`
- Copybook `COADM02Y` field `CARDDEMO-ADMIN-MENU-OPTIONS` PIC `-`
- Copybook `COADM02Y` field `CDEMO-ADMIN-OPT-COUNT` PIC `9(02)`
- Copybook `COADM02Y` field `CDEMO-ADMIN-OPTIONS-DATA` PIC `-`
- Copybook `COADM02Y` field `CDEMO-ADMIN-OPTIONS` PIC `-`
- Copybook `COCOM01Y` field `CARDDEMO-COMMAREA` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-GENERAL-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-CUSTOMER-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-ACCOUNT-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-CARD-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-CARD-NUM` PIC `9(16)`
- Copybook `COCOM01Y` field `CDEMO-MORE-INFO` PIC `-`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
