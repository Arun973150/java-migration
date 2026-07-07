# JCL English Documentation: TRANBKP

## 1. Executive Summary

`TRANBKP` is a standalone batch job defined in `TRANBKP.jcl`. The extracted job description is: REPRO and Delete Transaction Master. It contains 3 execution step(s), reading 2 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\TRANBKP.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: REPROC
- Main utilities: IDCAMS
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05R`

This step executes `REPROC` and expands and runs a cataloged procedure. It has 2 DD statement(s).
Extracted step notes: Repro the processed transaction file
- Inputs: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)

### Step 2: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DELETE TRANSACATION MASTER VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 6 control line(s) are supplied to the step.

### Step 3: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE TRANSACATION MASTER VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Conditional execution: `COND=4,LT`
- Inline SYSIN: 14 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, inline control data
- Output datasets: AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, COMBTRAN/STEP10, CREASTMT/STEP010, POSTTRAN/STEP15, REPRTEST/STEP05, TRANFILE/STEP15, TRANREPT/STEP05R
- Peer/upstream references to the flat-file inputs: REPRTEST/STEP05, TRANREPT/STEP05R, TRANREPT/STEP05R

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
