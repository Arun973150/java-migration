# JCL English Documentation: INTRDRJ1

## 1. Executive Summary

`INTRDRJ1` is a standalone batch job defined in `INTRDRJ1.JCL`. The extracted job description is: No job-card description was extracted.. It contains 2 execution step(s), reading 5 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\INTRDRJ1.JCL`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS, IEBGENER
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `IDCAMS`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: THIS INTRDR JOB WILL TRIGGER ANOTHER JCL
- Inputs: AWS.M2.CARDEMO.FTP.TEST, AWS.M2.CARDEMO.FTP.TEST.BKUP, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 2: `STEP01`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
- Inputs: SYSIN, AWS.M2.CARDDEMO.JCL(INTRDRJ2)
- Outputs: None found in extracted data

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDEMO.FTP.TEST, AWS.M2.CARDEMO.FTP.TEST.BKUP, inline control data, SYSIN, AWS.M2.CARDDEMO.JCL(INTRDRJ2)
- Output datasets: None found in extracted data
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
- Peer/upstream references to the flat-file inputs: INTRDRJ2/IDCAMS

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
