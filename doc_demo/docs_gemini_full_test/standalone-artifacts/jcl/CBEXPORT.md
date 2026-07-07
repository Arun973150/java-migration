# JCL English Documentation: CBEXPORT

## 1. Executive Summary

`CBEXPORT` is a standalone batch job defined in `CBEXPORT.jcl`. The extracted job description is: Export Customer Data for Migration. It contains 2 execution step(s), reading 7 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\CBEXPORT.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBEXPORT
- Main utilities: IDCAMS
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP01`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: EXPORT CUSTOMER DATA FROM VSAM FILES TO MULTI-RECORD EXPORT FILE FOR BRANCH MIGRATION OR DATA TRANSFER PURPOSES STEP 1: DEFINE VSAM CLUSTER FOR EXPORT FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 12 control line(s) are supplied to the step.

### Step 2: `STEP02`

This step executes `CBEXPORT` and runs application processing. It has 9 DD statement(s).
Extracted step notes: STEP 2: RUN EXPORT PROGRAM
- Inputs: AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS, AWS.M2.CARDDEMO.EXPORT.DATA
- Outputs: None found in extracted data

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS, AWS.M2.CARDDEMO.EXPORT.DATA
- Output datasets: None found in extracted data
- System/control DDs: SYSPRINT, AWS.M2.CARDDEMO.LOADLIB, SYSOUT
- Downstream jobs that also reference the created/managed VSAM dataset: CREASTMT/STEP040, CUSTFILE/STEP15, READCUST/STEP05, ACCTFILE/STEP15, INTCALC/STEP15, POSTTRAN/STEP15, READACCT/STEP05, READXREF/STEP05, TRANREPT/STEP10R, XREFFILE/STEP15, COMBTRAN/STEP10, CREASTMT/STEP010, REPRTEST/STEP05, TRANBKP/STEP05R, TRANFILE/STEP15, TRANREPT/STEP05R, CARDFILE/STEP15, READCARD/STEP05
- Peer/upstream references to the flat-file inputs: CBIMPORT/STEP01

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
