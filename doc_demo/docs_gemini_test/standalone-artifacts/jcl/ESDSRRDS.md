# JCL English Documentation: ESDSRRDS

## 1. Executive Summary

`ESDSRRDS` is a standalone batch job defined in `ESDSRRDS.jcl`. The extracted job description is: DEF ESDS RRDS  . It contains 6 execution step(s), reading 5 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\ESDSRRDS.jcl`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: None found in extracted data
- Main utilities: IDCAMS, IEBGENER, IEFBR14
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `PREDEL`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 1 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- PRE DELETE STEP
- Inputs: None found in extracted data
- Outputs: AWS.M2.CARDDEMO.ESDSRRDS.PS

### Step 2: `STEP01`

This step executes `IEBGENER` and copies sequential data or submits generated control cards. It has 4 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- CREATE USER SECURITY FILE (PS) FROM IN-STREAM DATA
- Inputs: SYSIN
- Outputs: AWS.M2.CARDDEMO.ESDSRRDS.PS
- Inline SYSIN: 10 control line(s) are supplied to the step.

### Step 3: `STEP02`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- DEFINE VSAM FILE FOR USER SECURITY (ESDS)
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 10 control line(s) are supplied to the step.

### Step 4: `STEP03`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 5 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- COPY USER SECURITY DATA FROM PS TO VSAM FILE(ESDS)
- Inputs: AWS.M2.CARDDEMO.ESDSRRDS.PS, AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

### Step 5: `STEP04`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 2 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- DEFINE VSAM FILE FOR USER SECURITY (RRDS)
- Inputs: inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 10 control line(s) are supplied to the step.

### Step 6: `STEP05`

This step executes `IDCAMS` and manages VSAM/catalog resources. It has 5 DD statement(s).
Extracted step notes: ------------------------------------------------------------------- COPY USER SECURITY DATA FROM PS TO VSAM FILE(ESDS)
- Inputs: AWS.M2.CARDDEMO.ESDSRRDS.PS, AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS, inline control data
- Outputs: None found in extracted data
- Inline SYSIN: 1 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: SYSIN, inline control data, AWS.M2.CARDDEMO.ESDSRRDS.PS, AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS, AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS
- Output datasets: AWS.M2.CARDDEMO.ESDSRRDS.PS
- System/control DDs: SYSPRINT, SYSOUT
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
