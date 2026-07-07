# JCL English Documentation: TRANCATG

## 1. Executive Summary

`TRANCATG` is a standalone batch job defined in `TRANCATG.jcl`. The extracted job description is: DEFINE TRAN CATEGORY. It contains 3 execution step(s), reading 3 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\TRANCATG.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DELETE TRANSACTION CATEGORY TYPE VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 2: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE TRANSACTION CATEGORY TYPE VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 14 control line(s) are supplied to the step.

### Step 3: `STEP15`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: COPY DATA FROM FLAT FILE TO VSAM FILE
- Inputs: AWS.M2.CARDDEMO.TRANCATG.PS, AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.TRANCATG.PS, AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS
- Output datasets: None found in extracted data
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: TRANREPT/STEP10R
- Peer/upstream references to the flat-file inputs: DEFGDGD/STEP40

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBTRN03C` / `TRANCATG-FILE` / `FD-TRAN-CAT-RECORD`: `FD-TRAN-CAT-RECORD` PIC `-`
- `CBTRN03C` / `TRANCATG-FILE` / `FD-TRAN-CAT-RECORD`: `FD-TRAN-CAT-KEY` PIC `-`
- `CBTRN03C` / `TRANCATG-FILE` / `FD-TRAN-CAT-RECORD`: `FD-TRAN-TYPE-CD` PIC `X(02)`
- `CBTRN03C` / `TRANCATG-FILE` / `FD-TRAN-CAT-RECORD`: `FD-TRAN-CAT-CD` PIC `9(04)`
- `CBTRN03C` / `TRANCATG-FILE` / `FD-TRAN-CAT-RECORD`: `FD-TRAN-CAT-DATA` PIC `X(54)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-TYPE-CD` PIC `X(02)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-CAT-CD` PIC `9(04)`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRAN-CAT-BAL-RECORD` PIC `-`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRAN-CAT-KEY` PIC `-`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRANCAT-ACCT-ID` PIC `9(11)`
Copybook field evidence suggests the logical account record layout is:
- Copybook `CCPAURLY` field `PA-RL-TRANSACTION-ID` PIC `X(15)`
- Copybook `CCPAURQY` field `PA-RQ-TRANSACTION-AMT` PIC `+9(10)`
- Copybook `CCPAURQY` field `PA-RQ-TRANSACTION-ID` PIC `X(15)`
- Copybook `CIPAUDTY` field `PA-TRANSACTION-AMT` PIC `S9(10)V99`
- Copybook `CIPAUDTY` field `PA-TRANSACTION-ID` PIC `X(15)`
- Copybook `CIPAUDTY` field `PA-MATCHED-WITH-TRAN` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-FROM-TRANID` PIC `X(04)`
- Copybook `COCOM01Y` field `CDEMO-TO-TRANID` PIC `X(04)`
- Copybook `CVEXPORT` field `EXPORT-TRANSACTION-DATA` PIC `-`
- Copybook `CVEXPORT` field `EXP-TRAN-ID` PIC `X(16)`
- Copybook `CVEXPORT` field `EXP-TRAN-TYPE-CD` PIC `X(02)`
- Copybook `CVEXPORT` field `EXP-TRAN-CAT-CD` PIC `9(04)`
- Copybook `CVEXPORT` field `EXP-TRAN-SOURCE` PIC `X(10)`
- Copybook `CVEXPORT` field `EXP-TRAN-DESC` PIC `X(100)`
- Copybook `CVEXPORT` field `EXP-TRAN-AMT` PIC `S9(09)V99`
- Copybook `CVEXPORT` field `EXP-TRAN-MERCHANT-ID` PIC `9(09)`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
