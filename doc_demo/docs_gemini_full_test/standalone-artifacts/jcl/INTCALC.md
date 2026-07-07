# JCL English Documentation: INTCALC

## 1. Executive Summary

`INTCALC` is a standalone batch job defined in `INTCALC.jcl`. The extracted job description is: INTEREST CALCULATOR. It contains 1 execution step(s), reading 5 input dataset reference(s) and writing 1 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\INTCALC.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: CBACT04C
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP15`

This step executes `CBACT04C` and runs application processing. It has 9 DD statement(s).
Extracted step notes: Process transaction balance file and compute interest and fees.
- Inputs: AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.SYSTRAN(+1)

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH, AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS
- Output datasets: AWS.M2.CARDDEMO.SYSTRAN(+1)
- System/control DDs: AWS.M2.CARDDEMO.LOADLIB, SYSPRINT, SYSOUT
- Downstream jobs that also reference the created/managed VSAM dataset: POSTTRAN/STEP15, PRTCATBL/STEP05R, TCATBALF/STEP15, CBEXPORT/STEP02, CREASTMT/STEP040, READXREF/STEP05, TRANREPT/STEP10R, XREFFILE/STEP15, ACCTFILE/STEP15, READACCT/STEP05, DISCGRP/STEP15
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
