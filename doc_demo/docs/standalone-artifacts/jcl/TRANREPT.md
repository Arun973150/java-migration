# JCL English Documentation: TRANREPT

## 1. Executive Summary

`TRANREPT` is a standalone batch job defined in `TRANREPT.jcl`. The extracted job description is: TRANSACTION REPORT. It contains 2 execution step(s), reading 7 input dataset reference(s) and writing 3 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\TRANREPT.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBTRN03C
- Main utilities: SORT
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05R`

This step executes `SORT` and sorts, filters, or reformats records. It has 6 DD statement(s).
Extracted step notes: Filter the transactions for a the parm date and sort by card num
- Inputs: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)
- Outputs: AWS.M2.CARDDEMO.TRANSACT.BKUP(+1), AWS.M2.CARDDEMO.TRANSACT.DALY(+1)
- Inline SYSIN: 8 control line(s) are supplied to the step.

### Step 2: `STEP10R`

This step executes `CBTRN03C` and runs application processing. It has 9 DD statement(s).
Extracted step notes: Produce a formatted report for processed transactions
- Inputs: AWS.M2.CARDDEMO.TRANSACT.DALY(+1), AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, AWS.M2.CARDDEMO.DATEPARM
- Outputs: AWS.M2.CARDDEMO.TRANREPT(+1)

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.TRANSACT.BKUP(+1), AWS.M2.CARDDEMO.TRANSACT.DALY(+1), AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, AWS.M2.CARDDEMO.DATEPARM
- Output datasets: AWS.M2.CARDDEMO.TRANSACT.BKUP(+1), AWS.M2.CARDDEMO.TRANSACT.DALY(+1), AWS.M2.CARDDEMO.TRANREPT(+1)
- System/control DDs: SYSOUT, AWS.M2.CARDDEMO.LOADLIB, SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, COMBTRAN/STEP10, CREASTMT/STEP010, POSTTRAN/STEP15, REPRTEST/STEP05, TRANBKP/STEP05R, TRANFILE/STEP15, CREASTMT/STEP040, INTCALC/STEP15, READXREF/STEP05, XREFFILE/STEP15, TRANTYPE/STEP15, TRANCATG/STEP15
- Peer/upstream references to the flat-file inputs: REPRTEST/STEP05, TRANBKP/STEP05R, SORTTEST/STEP05R

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
