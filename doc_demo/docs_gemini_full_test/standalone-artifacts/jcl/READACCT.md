# JCL English Documentation: READACCT

## 1. Executive Summary

`READACCT` is a standalone batch job defined in `READACCT.jcl`. The extracted job description is: READACCT. It contains 2 execution step(s), reading 1 input dataset reference(s) and writing 3 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\READACCT.jcl`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: CBACT01C
- Main utilities: IEFBR14
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `PREDEL`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 3 DD statement(s).
Extracted step notes: PRE DELETE STEP
- Inputs: None found in extracted data
- Outputs: AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS, AWS.M2.CARDDEMO.ACCTDATA.VBPS

### Step 2: `STEP05`

This step executes `CBACT01C` and runs application processing. It has 7 DD statement(s).
Extracted step notes: RUN THE PROGRAM THAT READS THE ACCOUNT MASTER VSAM FILE
- Inputs: AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS, AWS.M2.CARDDEMO.ACCTDATA.VBPS

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS
- Output datasets: AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS, AWS.M2.CARDDEMO.ACCTDATA.VBPS
- System/control DDs: AWS.M2.CARDDEMO.LOADLIB, SYSOUT, SYSPRINT
- Downstream jobs that also reference the created/managed VSAM dataset: ACCTFILE/STEP15, CBEXPORT/STEP02, CREASTMT/STEP040, INTCALC/STEP15, POSTTRAN/STEP15
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
