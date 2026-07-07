# JCL English Documentation: UNLDGSAM

## 1. Executive Summary

`UNLDGSAM` is a standalone batch job defined in `UNLDGSAM.JCL`. The extracted job description is: M2APP. It contains 1 execution step(s), reading 7 input dataset reference(s) and writing 0 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\app-authorization-ims-db2-mq\jcl\UNLDGSAM.JCL`
- Job class: `A`
- Message class: `H`
- Application programs/procedures: DFSRRC00
- Main utilities: None found in extracted data
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `STEP01`

This step executes `DFSRRC00` and runs an IMS dependent region program. It has 13 DD statement(s).
Extracted step notes: EXECUTE IMS PROGRAM
- Inputs: OEMA.IMS.IMSP.SDFSRESL, OEM.IMS.IMSP.PSBLIB, AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM, AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM, OEM.IMS.IMSP.PAUTHDB, OEM.IMS.IMSP.PAUTHDBX, OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)
- Outputs: None found in extracted data

## 4. Dataset and Dependency Context

- Input datasets: OEMA.IMS.IMSP.SDFSRESL, OEM.IMS.IMSP.PSBLIB, AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM, AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM, OEM.IMS.IMSP.PAUTHDB, OEM.IMS.IMSP.PAUTHDBX, OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)
- Output datasets: None found in extracted data
- System/control DDs: OEMA.IMS.IMSP.SDFSRESL, SYSPRINT, SYSUDUMP
- Downstream jobs that also reference the created/managed VSAM dataset: not present in extracted data
- Peer/upstream references to the flat-file inputs: DBPAUTP0/UNLOAD, DBPAUTP0/UNLOAD, LOADPADB/STEP01, LOADPADB/STEP01, UNLDPADB/STEP01, UNLDPADB/STEP01

## 5. Source Record Layout

No record-layout evidence was matched for the flat-file datasets.
- Encoding/charset: not present in extracted data.

## 6. Operational Meaning

For migration planning, treat this JCL file as an independently schedulable batch workflow. Each EXEC step becomes either an application batch task, a managed utility operation, or a data-preparation step. Preserve the dataset ordering and inline SYSIN content because those values define the job's runtime contract.

## 7. Migration Notes

- Modern equivalent: scheduler workflow with one task per JCL step.
- Candidate platforms: cloud batch job, Step Functions-style orchestration, or Control-M equivalent.
- Key migration checks: dataset availability, utility behavior, return-code handling, restart semantics, downstream dataset consumers, and validation of the flat-file record contract before data conversion.
