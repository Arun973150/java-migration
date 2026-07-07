# JCL English Documentation: DISCGRP

## 1. Executive Summary

`DISCGRP` is a standalone batch job defined in `DISCGRP.jcl`. The extracted job description is: DEFINE DISCLOSURE GROUP FILE. It contains 3 execution step(s), reading 3 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\DISCGRP.jcl`
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
Extracted step notes: DELETE DISCLOSURE GROUP VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 2: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE DISCLOSURE GROUP VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 14 control line(s) are supplied to the step.

### Step 3: `STEP15`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: COPY DATA FROM FLAT FILE TO VSAM FILE
- Inputs: AWS.M2.CARDDEMO.DISCGRP.PS, AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.DISCGRP.PS, AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS
- Output datasets: None found in extracted data
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: INTCALC/STEP15
- Peer/upstream references to the flat-file inputs: DEFGDGD/STEP60

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DISCGRP-REC` PIC `-`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DISCGRP-KEY` PIC `-`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-ACCT-GROUP-ID` PIC `X(10)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-TYPE-CD` PIC `X(02)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DIS-TRAN-CAT-CD` PIC `9(04)`
- `CBACT04C` / `DISCGRP-FILE` / `FD-DISCGRP-REC`: `FD-DISCGRP-DATA` PIC `X(34)`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
