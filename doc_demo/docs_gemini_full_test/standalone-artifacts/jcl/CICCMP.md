# JCL English Documentation: CICCMP

## 1. Executive Summary

`CICCMP` is a standalone batch job defined in `CICCMP.jcl`. The extracted job description is: Compile CICS Program. It contains 2 execution step(s), reading 1 input dataset reference(s) and writing 2 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\samples\jcl\CICCMP.jcl`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: BUILDONL, SDSF
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `CICSCMP`

This step executes `BUILDONL` and expands and runs a cataloged procedure. It has 0 DD statement(s).
Extracted step notes: compile the COBOL code:
- Inputs: None found in extracted data
- Outputs: None found in extracted data

### Step 2: `NEWCOPY`

This step executes `SDSF` and runs application processing. It has 3 DD statement(s).
Extracted step notes: CICS commands in batch to perform NEWCOPY
- Inputs: inline control data
- Outputs: ISFOUT, CMDOUT
- Conditional execution: `COND=4,LT`
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data
- Output datasets: ISFOUT, CMDOUT
- System/control DDs: None found in extracted data
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
