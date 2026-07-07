# JCL English Documentation: DEFGDGD

## 1. Executive Summary

`DEFGDGD` is a standalone batch job defined in `DEFGDGD.jcl`. The extracted job description is: DEF DB2 GDG. It contains 6 execution step(s), reading 5 input dataset reference(s) and writing 3 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\DEFGDGD.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS, IEBGENER
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: RESTART=STEP30                                                     JOB05067 This jcl will create GDGs and load first generation for Transaction reference data Define GDG for Transaction Type
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 5 control line(s) are supplied to the step.

### Step 2: `STEP20`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: Create the first generation of GDG Transaction Type
- Inputs: SYSIN, AWS.M2.CARDDEMO.TRANTYPE.PS
- Outputs: AWS.M2.CARDDEMO.TRANTYPE.BKUP(+1)
- Conditional execution: `COND=0,NE`

### Step 3: `STEP30`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: Transaction Category type
- Inputs: inline control data
- Outputs: None found in extracted data
- Conditional execution: `COND=0,NE`
- Inline SYSIN: 5 control line(s) are supplied to the step.

### Step 4: `STEP40`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: Create the first generation of GDG Transaction Category Type
- Inputs: SYSIN, AWS.M2.CARDDEMO.TRANCATG.PS
- Outputs: AWS.M2.CARDDEMO.TRANCATG.PS.BKUP(+1)
- Conditional execution: `COND=0,NE`

### Step 5: `STEP50`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: Disclosure Group
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 5 control line(s) are supplied to the step.

### Step 6: `STEP60`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: Create the first generation of GDG disclosure group
- Inputs: SYSIN, AWS.M2.CARDDEMO.DISCGRP.PS
- Outputs: AWS.M2.CARDDEMO.DISCGRP.BKUP(+1)
- Conditional execution: `COND=0,NE`

## 4. Dataset and Dependency Context

- Input datasets: inline control data, SYSIN, AWS.M2.CARDDEMO.TRANTYPE.PS, AWS.M2.CARDDEMO.TRANCATG.PS, AWS.M2.CARDDEMO.DISCGRP.PS
- Output datasets: AWS.M2.CARDDEMO.TRANTYPE.BKUP(+1), AWS.M2.CARDDEMO.TRANCATG.PS.BKUP(+1), AWS.M2.CARDDEMO.DISCGRP.BKUP(+1)
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
- Peer/upstream references to the flat-file inputs: TRANTYPE/STEP15, TRANCATG/STEP15, DISCGRP/STEP15

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBTRN03C` / `TRANTYPE-FILE` / `FD-TRANTYPE-REC`: `FD-TRANTYPE-REC` PIC `-`
- `CBTRN03C` / `TRANTYPE-FILE` / `FD-TRANTYPE-REC`: `FD-TRAN-TYPE` PIC `X(02)`
- `CBTRN03C` / `TRANTYPE-FILE` / `FD-TRANTYPE-REC`: `FD-TRAN-DATA` PIC `X(58)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-TYPE-CD` PIC `X(02)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-CAT-CD` PIC `9(04)`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRAN-CAT-BAL-RECORD` PIC `-`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRAN-CAT-KEY` PIC `-`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRANCAT-ACCT-ID` PIC `9(11)`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRANCAT-TYPE-CD` PIC `X(02)`
- `CBACT04C` / `TCATBAL-FILE` / `FD-TRAN-CAT-BAL-RECORD`: `FD-TRANCAT-CD` PIC `9(04)`
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
