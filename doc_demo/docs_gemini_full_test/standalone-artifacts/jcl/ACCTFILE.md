# JCL English Documentation: ACCTFILE

## 1. Executive Summary

`ACCTFILE` is a standalone batch job defined in `ACCTFILE.jcl`. The extracted job description is: Delete define Account Data. It contains 3 execution step(s), reading 3 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\ACCTFILE.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DELETE ACCOUNT VSAM FILE IF ONE ALREADY EXISTS
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 3 control line(s) are supplied to the step.

### Step 2: `STEP10`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: DEFINE ACCOUNT VSAM FILE
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 14 control line(s) are supplied to the step.

### Step 3: `STEP15`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 4 DD statement(s).
Extracted step notes: COPY DATA FROM FLAT FILE TO VSAM FILE
- Inputs: AWS.M2.CARDDEMO.ACCTDATA.PS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: inline control data, AWS.M2.CARDDEMO.ACCTDATA.PS, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS
- Output datasets: None found in extracted data
- System/control DDs: SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: CBEXPORT/STEP02, CREASTMT/STEP040, INTCALC/STEP15, POSTTRAN/STEP15, READACCT/STEP05
- Peer/upstream references to the flat-file inputs: not present in extracted data

## 5. Source Record Layout

Copybook field evidence suggests the logical account record layout is:
- Copybook `CIPAUSMY` field `PA-ACCOUNT-STATUS` PIC `X(02)`
- Copybook `COCOM01Y` field `CDEMO-ACCOUNT-INFO` PIC `-`
- Copybook `COCOM01Y` field `CDEMO-ACCT-ID` PIC `9(11)`
- Copybook `COCOM01Y` field `CDEMO-ACCT-STATUS` PIC `X(01)`
- Copybook `CUSTREC` field `CUST-EFT-ACCOUNT-ID` PIC `X(10)`
- Copybook `CVACT01Y` field `ACCT-ID` PIC `9(11)`
- Copybook `CVACT01Y` field `ACCT-ACTIVE-STATUS` PIC `X(01)`
- Copybook `CVACT01Y` field `ACCT-CURR-BAL` PIC `S9(10)V99`
- Copybook `CVACT01Y` field `ACCT-CREDIT-LIMIT` PIC `S9(10)V99`
- Copybook `CVACT01Y` field `ACCT-CASH-CREDIT-LIMIT` PIC `S9(10)V99`
- Copybook `CVACT01Y` field `ACCT-OPEN-DATE` PIC `X(10)`
- Copybook `CVACT01Y` field `ACCT-EXPIRAION-DATE` PIC `X(10)`
- Copybook `CVACT01Y` field `ACCT-REISSUE-DATE` PIC `X(10)`
- Copybook `CVACT01Y` field `ACCT-CURR-CYC-CREDIT` PIC `S9(10)V99`
- Copybook `CVACT01Y` field `ACCT-CURR-CYC-DEBIT` PIC `S9(10)V99`
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
