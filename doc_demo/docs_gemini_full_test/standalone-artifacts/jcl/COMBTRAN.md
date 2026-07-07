# JCL English Documentation: COMBTRAN

## 1. Executive Summary

`COMBTRAN` is a standalone batch job defined in `COMBTRAN.jcl`. The extracted job description is: COMBINE TRANSACTIONS. It contains 2 execution step(s), reading 4 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\COMBTRAN.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS, SORT
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05R`

This step executes `SORT` and sorts, filters, or reformats records. It has 4 DD statement(s).
Extracted step notes: Sort current transaction file and system generated transactions
- Inputs: AWS.M2.CARDDEMO.TRANSACT.BKUP(0)
- Outputs: AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 2: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: Load combined file to transaction master
- Inputs: AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1), AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TRANSACT.BKUP(0), AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1), AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, inline control data
- Output datasets: AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)
- System/control DDs: SYSOUT, SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, CREASTMT/STEP010, POSTTRAN/STEP15, REPRTEST/STEP05, TRANBKP/STEP05R, TRANFILE/STEP15, TRANREPT/STEP05R
- Peer/upstream references to the flat-file inputs: SORTTEST/STEP05R

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
