# JCL English Documentation: TRANEXTR

## 1. Executive Summary

`TRANEXTR` is a standalone batch job defined in `TRANEXTR.jcl`. The extracted job description is: EXTRACT TRAN TYPE. It contains 5 execution step(s), reading 4 input dataset reference(s) and writing 4 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\app-transaction-type-db2\jcl\TRANEXTR.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IEBGENER, IEFBR14, IKJEFT01
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP10`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: Db2 Unload using DSNTIAUL utility STEP 10 : BACKUP THE PREVIOUS VERSION OF TRANTYPE FILE TO GDG
- Inputs: SYSIN, &HLQ..TRANTYPE.PS
- Outputs: &HLQ..TRANTYPE.BKUP(+1)

### Step 2: `STEP20`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: STEP 20 : BACKUP THE PREVIOUS VERSION OF TRANCATG FILE TO GDG
- Inputs: SYSIN, &HLQ..TRANCATG.PS
- Outputs: &HLQ..TRANCATG.PS.BKUP(+1)
- Conditional execution: `COND=0,NE`

### Step 3: `STEP30`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 2 DD statement(s).
Extracted step notes: STEP 30 : DELETE FILES FROM PREVIOUS RUN
- Inputs: None found in extracted data
- Outputs: &HLQ..TRANTYPE.PS, &HLQ..TRANCATG.PS
- Conditional execution: `COND=0,NE`

### Step 4: `STEP40`

This step executes `IKJEFT01` and runs TSO/DB2 command processing. It has 8 DD statement(s).
Extracted step notes: STEP 40 : EXTRACT DATA FROM TRANSACTION TYPE TABLE
- Inputs: inline control data, inline control data
- Outputs: &HLQ..TRANTYPE.PS
- Conditional execution: `COND=0,NE`
- Inline SYSIN: 13 control line(s) are supplied to the step.

### Step 5: `STEP50`

This step executes `IKJEFT01` and runs TSO/DB2 command processing. It has 8 DD statement(s).
Extracted step notes: STEP 50 : EXTRACT DATA FROM TRANSACTION TYPE TABLE
- Inputs: inline control data, inline control data
- Outputs: &HLQ..TRANCATG.PS
- Conditional execution: `COND=4,LT`
- Inline SYSIN: 14 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: SYSIN, &HLQ..TRANTYPE.PS, &HLQ..TRANCATG.PS, inline control data
- Output datasets: &HLQ..TRANTYPE.BKUP(+1), &HLQ..TRANCATG.PS.BKUP(+1), &HLQ..TRANTYPE.PS, &HLQ..TRANCATG.PS
- System/control DDs: SYSPRINT, OEM.DB2.DAZ1.RUNLIB.LOAD, SYSTSPRT, SYSUDUMP
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
- Peer/upstream references to the flat-file inputs: not present in extracted data

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
