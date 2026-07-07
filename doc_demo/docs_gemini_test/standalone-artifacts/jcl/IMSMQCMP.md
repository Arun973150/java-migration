# JCL English Documentation: IMSMQCMP

## 1. Executive Summary

`IMSMQCMP` is a standalone batch job defined in `IMSMQCMP.jcl`. The extracted job description is: No job-card description was extracted.. It contains 3 execution step(s), reading 3 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\samples\jcl\IMSMQCMP.jcl`
- Job class: `A`
- Message class: `-`
- Application programs/procedures: DFHECP1, IGYCRCTL
- Main utilities: IEBGENER
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `TRN`

This step executes `DFHECP1` and runs application processing. It has 4 DD statement(s).
- Inputs: &HLQ..COBOL.SRC(IMSMQPGM)
- Outputs: None found in extracted data

### Step 2: `COBOL`

This step executes `IGYCRCTL` and runs application processing. It has 21 DD statement(s).
- Inputs: CEE.SCEESAMP, &&SYSCIN
- Outputs: SYSLIN
- Conditional execution: `COND=4,LT`

### Step 3: `COPYIMS`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 2 DD statement(s).
Extracted step notes: COPY LINK STEP
- Inputs: None found in extracted data
- Outputs: None found in extracted data
- Conditional execution: `COND=4,LT`
- Inline SYSIN: 27 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: &HLQ..COBOL.SRC(IMSMQPGM), CEE.SCEESAMP, &&SYSCIN
- Output datasets: SYSLIN
- System/control DDs: &CICSHLQ..CICS.SDFHLOAD, SYSPRINT, STEPLIB
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
