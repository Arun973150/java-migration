# JCL English Documentation: CBIMPORT

## 1. Executive Summary

`CBIMPORT` is a standalone batch job defined in `CBIMPORT.jcl`. The extracted job description is: Import CARDDEMO Data. It contains 1 execution step(s), reading 1 input dataset reference(s) and writing 5 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\CBIMPORT.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBIMPORT
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP01`

This step executes `CBIMPORT` and runs application processing. It has 9 DD statement(s).
Extracted step notes: IMPORT CUSTOMER DATA FROM MULTI-RECORD EXPORT FILE AND SPLIT INTO SEPARATE NORMALIZED FILES FOR TARGET SYSTEM
- Inputs: AWS.M2.CARDDEMO.EXPORT.DATA
- Outputs: AWS.M2.CARDDEMO.CUSTDATA.IMPORT, AWS.M2.CARDDEMO.ACCTDATA.IMPORT, AWS.M2.CARDDEMO.CARDXREF.IMPORT, AWS.M2.CARDDEMO.TRANSACT.IMPORT, AWS.M2.CARDDEMO.IMPORT.ERRORS

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.EXPORT.DATA
- Output datasets: AWS.M2.CARDDEMO.CUSTDATA.IMPORT, AWS.M2.CARDDEMO.ACCTDATA.IMPORT, AWS.M2.CARDDEMO.CARDXREF.IMPORT, AWS.M2.CARDDEMO.TRANSACT.IMPORT, AWS.M2.CARDDEMO.IMPORT.ERRORS
- System/control DDs: AWS.M2.CARDDEMO.LOADLIB, SYSOUT, SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
- Peer/upstream references to the flat-file inputs: CBEXPORT/STEP02

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
