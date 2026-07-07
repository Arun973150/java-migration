# JCL English Documentation: CUSTFILE

## 1. Executive Summary

`CUSTFILE` is a standalone batch job defined in `CUSTFILE.jcl`. The extracted job description is: DEFINE CUSTOMER FILE. It contains 5 execution step(s), reading 3 input dataset reference(s) and writing 2 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\CUSTFILE.jcl`
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
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 2: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DELETE CUSTOMER VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 3: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE CUSTOMER VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 14 control line(s) are supplied to the step.

### Step 4: `STEP15`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: COPY DATA FROM FLAT FILE TO VSAM FILE
- Inputs: AWS.M2.CARDDEMO.CUSTDATA.PS, AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 5: `OPCIFIL`

This step executes `SDSF` and runs application processing. It has 3 DD statement(s).
Extracted step notes: Open files in CICS region
- Inputs: inline control data
- Outputs: ISFOUT, CMDOUT
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.CUSTDATA.PS, AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS
- Output datasets: ISFOUT, CMDOUT
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, CREASTMT/STEP040, READCUST/STEP05
- Peer/upstream references to the flat-file inputs: not present in extracted data

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBTRN01C` / `CUSTOMER-FILE` / `FD-CUSTFILE-REC`: `FD-CUSTFILE-REC` PIC `-`
- `CBTRN01C` / `CUSTOMER-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-ID` PIC `9(09)`
- `CBTRN01C` / `CUSTOMER-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-DATA` PIC `X(491)`
- `CBACT04C` / `XREF-FILE` / `FD-XREFFILE-REC`: `FD-XREF-CUST-NUM` PIC `9(09)`
- `CBCUS01C` / `CUSTFILE-FILE` / `FD-CUSTFILE-REC`: `FD-CUSTFILE-REC` PIC `-`
- `CBCUS01C` / `CUSTFILE-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-ID` PIC `9(09)`
- `CBCUS01C` / `CUSTFILE-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-DATA` PIC `X(491)`
- `CBSTM03B` / `CUST-FILE` / `FD-CUSTFILE-REC`: `FD-CUSTFILE-REC` PIC `-`
- `CBSTM03B` / `CUST-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-ID` PIC `X(09)`
- `CBSTM03B` / `CUST-FILE` / `FD-CUSTFILE-REC`: `FD-CUST-DATA` PIC `X(491)`
Copybook field evidence suggests the logical account record layout is:
- Copybook `COCOM01Y` field `CDEMO-CUSTOMER-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-CUST-ID` PIC `9(09)`
- Copybook `COCOM01Y` field `CDEMO-CUST-FNAME` PIC `X(25)`
- Copybook `COCOM01Y` field `CDEMO-CUST-MNAME` PIC `X(25)`
- Copybook `COCOM01Y` field `CDEMO-CUST-LNAME` PIC `X(25)`
- Copybook `CUSTREC` field `CUSTOMER-RECORD` PIC `-`
- Copybook `CUSTREC` field `CUST-ID` PIC `9(09)`
- Copybook `CUSTREC` field `CUST-FIRST-NAME` PIC `X(25)`
- Copybook `CUSTREC` field `CUST-MIDDLE-NAME` PIC `X(25)`
- Copybook `CUSTREC` field `CUST-LAST-NAME` PIC `X(25)`
- Copybook `CUSTREC` field `CUST-ADDR-LINE-1` PIC `X(50)`
- Copybook `CUSTREC` field `CUST-ADDR-LINE-2` PIC `X(50)`
- Copybook `CUSTREC` field `CUST-ADDR-LINE-3` PIC `X(50)`
- Copybook `CUSTREC` field `CUST-ADDR-STATE-CD` PIC `X(02)`
- Copybook `CUSTREC` field `CUST-ADDR-COUNTRY-CD` PIC `X(03)`
- Copybook `CUSTREC` field `CUST-ADDR-ZIP` PIC `X(10)`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
