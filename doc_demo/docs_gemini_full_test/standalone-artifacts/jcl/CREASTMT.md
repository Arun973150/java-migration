# JCL English Documentation: CREASTMT

## 1. Executive Summary

`CREASTMT` is a standalone batch job defined in `CREASTMT.JCL`. The extracted job description is: Create Statement. It contains 5 execution step(s), reading 7 input dataset reference(s) and writing 3 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\CREASTMT.JCL`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: CBSTM03A
- Main utilities: IDCAMS, IEFBR14, SORT
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `DELDEF01`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: This JCL will create statement for each CARD present in the XREF file
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 15 control line(s) are supplied to the step.

### Step 2: `STEP010`

This step executes `SORT` and sorts, filters, or reformats records. It has 5 DD statement(s).
Extracted step notes: CREATE COPY OF TRANSACT FILE WITH CARD NUMBER AND TRAN ID AS KEY
- Inputs: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, inline control data
- Outputs: AWS.M2.CARDDEMO.TRXFL.SEQ
- Inline SYSIN: 2 control line(s) are supplied to the step.

### Step 3: `STEP020`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
- Inputs: AWS.M2.CARDDEMO.TRXFL.SEQ, AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Conditional execution: `COND=0,NE`
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 4: `STEP030`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 2 DD statement(s).
Extracted step notes: DELETE TRANSACTION REPORTS FROM PREVIOUS RUN
- Inputs: None found in extracted data
- Outputs: AWS.M2.CARDDEMO.STATEMNT.HTML, AWS.M2.CARDDEMO.STATEMNT.PS
- Conditional execution: `COND=0,NE`

### Step 5: `STEP040`

This step executes `CBSTM03A` and runs application processing. It has 9 DD statement(s).
Extracted step notes: PRODUCING REPORT IN TEXT AND HTML - DEMONSTRATES CALLED SUBROUTINE
- Inputs: AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.STATEMNT.PS, AWS.M2.CARDDEMO.STATEMNT.HTML
- Conditional execution: `COND=0,NE`

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.TRXFL.SEQ, AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS
- Output datasets: AWS.M2.CARDDEMO.TRXFL.SEQ, AWS.M2.CARDDEMO.STATEMNT.HTML, AWS.M2.CARDDEMO.STATEMNT.PS
- System/control DDs: SYSPRINT, SYSOUT, AWS.M2.CARDDEMO.LOADLIB
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, COMBTRAN/STEP10, POSTTRAN/STEP15, REPRTEST/STEP05, TRANBKP/STEP05R, TRANFILE/STEP15, TRANREPT/STEP05R, INTCALC/STEP15, READXREF/STEP05, TRANREPT/STEP10R, XREFFILE/STEP15, ACCTFILE/STEP15, READACCT/STEP05, CUSTFILE/STEP15, READCUST/STEP05
- Peer/upstream references to the flat-file inputs: TXT2PDF1/TXT2PDF

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
