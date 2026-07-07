# JCL English Documentation: READCARD

## 1. Executive Summary

`READCARD` is a standalone batch job defined in `READCARD.jcl`. The extracted job description is: READCARD. It contains 1 execution step(s), reading 1 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\READCARD.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBACT02C
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05`

This step executes `CBACT02C` and runs application processing. It has 4 DD statement(s).
Extracted step notes: RUN THE PROGRAM THAT READS THE CARD MASTER VSAM FILE
- Inputs: AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS
- Outputs: None found in extracted data

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS
- Output datasets: None found in extracted data
- System/control DDs: AWS.M2.CARDDEMO.LOADLIB, SYSOUT, SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CARDFILE/STEP15, CBEXPORT/STEP02
- Peer/upstream references to the flat-file inputs: not present in extracted data

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
