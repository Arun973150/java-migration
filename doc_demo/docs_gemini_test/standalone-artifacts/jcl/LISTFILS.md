# JCL English Documentation: LISTFILS

## 1. Executive Summary

`LISTFILS` is a standalone batch job defined in `LISTCAT.jcl`. The extracted job description is: CARDDEMO. It contains 2 execution step(s), reading 1 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\samples\jcl\LISTCAT.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS, IEFBR14
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP01`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 1 DD statement(s).
Extracted step notes: List catalog for all the files in CARDDEMO application
- Inputs: None found in extracted data
- Outputs: AWS.M2.CARDDEMO.LISTCAT

### Step 2: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
- Inputs: inline control data
- Outputs: None found in extracted data
- Conditional execution: `COND=0,NE`
- Inline SYSIN: 2 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data
- Output datasets: AWS.M2.CARDDEMO.LISTCAT
- System/control DDs: AWS.M2.CARDDEMO.LISTCAT
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
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
