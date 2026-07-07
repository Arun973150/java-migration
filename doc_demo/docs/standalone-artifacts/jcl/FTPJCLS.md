# JCL English Documentation: FTPJCLS

## 1. Executive Summary

`FTPJCLS` is a standalone batch job defined in `FTPJCL.JCL`. The extracted job description is: FTP JCL. It contains 1 execution step(s), reading 1 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\FTPJCL.JCL`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: None found in extracted data
- Main utilities: FTP
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP1`

This step executes `FTP` and runs application processing. It has 1 DD statement(s).
Extracted step notes: FTP JOB TO RECEIVE A FILE MY.FTP.SERVER.COM IS THE FTP SERVER NAME(SUBJECT TO CHANGE FOR SITE) USER ID - EITHER SCHEDULER ID OR TSO USER ID PASSWORD OF THE USER FOLDER TO FTP THE MAINFRAME FILE PUT COMMAND FOR SENDING MAINFRAME FILE TO TXT CHANGE THE PUT COMMAND TO GET TO RECEIVE FILE INTO MAINFRAME
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 10 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data
- Output datasets: None found in extracted data
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
