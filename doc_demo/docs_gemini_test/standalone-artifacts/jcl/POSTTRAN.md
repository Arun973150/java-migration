# JCL English Documentation: POSTTRAN

## 1. Executive Summary

`POSTTRAN` is a standalone batch job defined in `POSTTRAN.jcl`. The extracted job description is: POSTTRAN. It contains 1 execution step(s), reading 5 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\POSTTRAN.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBTRN02C
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP15`

This step executes `CBTRN02C` and runs application processing. It has 9 DD statement(s).
Extracted step notes: Process and load daily transaction file and create transaction category balance and update transaction master vsam
- Inputs: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.DALYTRAN.PS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.DALYREJS(+1)

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, AWS.M2.CARDDEMO.DALYTRAN.PS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS
- Output datasets: AWS.M2.CARDDEMO.DALYREJS(+1)
- System/control DDs: AWS.M2.CARDDEMO.LOADLIB, SYSPRINT, SYSOUT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, COMBTRAN/STEP10, CREASTMT/STEP010, REPRTEST/STEP05, TRANBKP/STEP05R, TRANFILE/STEP15, TRANREPT/STEP05R, CREASTMT/STEP040, INTCALC/STEP15, READXREF/STEP05, TRANREPT/STEP10R, XREFFILE/STEP15, ACCTFILE/STEP15, READACCT/STEP05, PRTCATBL/STEP05R, TCATBALF/STEP15
- Peer/upstream references to the flat-file inputs: not present in extracted data

## 5. Source Record Layout

Program FD evidence suggests the physical account file contract is:
- `CBTRN01C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-TRAN-RECORD` PIC `-`
- `CBTRN01C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-TRAN-ID` PIC `X(16)`
- `CBTRN01C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-CUST-DATA` PIC `X(334)`
- `CBTRN02C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-TRAN-RECORD` PIC `-`
- `CBTRN02C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-TRAN-ID` PIC `X(16)`
- `CBTRN02C` / `DALYTRAN-FILE` / `FD-TRAN-RECORD`: `FD-CUST-DATA` PIC `X(334)`
Copybook field evidence suggests the logical account record layout is:
- Copybook `CVTRA06Y` field `DALYTRAN-RECORD` PIC `-`
- Copybook `CVTRA06Y` field `DALYTRAN-ID` PIC `X(16)`
- Copybook `CVTRA06Y` field `DALYTRAN-TYPE-CD` PIC `X(02)`
- Copybook `CVTRA06Y` field `DALYTRAN-CAT-CD` PIC `9(04)`
- Copybook `CVTRA06Y` field `DALYTRAN-SOURCE` PIC `X(10)`
- Copybook `CVTRA06Y` field `DALYTRAN-DESC` PIC `X(100)`
- Copybook `CVTRA06Y` field `DALYTRAN-AMT` PIC `S9(09)V99`
- Copybook `CVTRA06Y` field `DALYTRAN-MERCHANT-ID` PIC `9(09)`
- Copybook `CVTRA06Y` field `DALYTRAN-MERCHANT-NAME` PIC `X(50)`
- Copybook `CVTRA06Y` field `DALYTRAN-MERCHANT-CITY` PIC `X(50)`
- Copybook `CVTRA06Y` field `DALYTRAN-MERCHANT-ZIP` PIC `X(10)`
- Copybook `CVTRA06Y` field `DALYTRAN-CARD-NUM` PIC `X(16)`
- Copybook `CVTRA06Y` field `DALYTRAN-ORIG-TS` PIC `X(26)`
- Copybook `CVTRA06Y` field `DALYTRAN-PROC-TS` PIC `X(26)`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
