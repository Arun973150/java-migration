# JCL English Documentation: PRTCATBL

## 1. Executive Summary

`PRTCATBL` is a standalone batch job defined in `PRTCATBL.jcl`. The extracted job description is: Print Trasaction Category Balance File. It contains 3 execution step(s), reading 2 input dataset reference(s) and writing 2 output dataset reference(s).

## 2. Batch Runtime Context

- Source file: `carddemo\app\jcl\PRTCATBL.jcl`
- Job class: `A`
- Message class: `0`
- Application programs/procedures: REPROC
- Main utilities: IEFBR14, SORT
- Ownership clue: not present in extracted data
- Maintainer clue: not present in extracted data
- Trigger/scheduler evidence: no predecessor job, scheduler binding, or submit relationship was extracted for this JCL file

## 3. Step-by-Step Job Flow

### Step 1: `DELDEF`

This step executes `IEFBR14` and performs allocation or cleanup through DD statements. It has 1 DD statement(s).
- Inputs: None found in extracted data
- Outputs: AWS.M2.CARDDEMO.TCATBALF.REPT

### Step 2: `STEP05R`

This step executes `REPROC` and expands and runs a cataloged procedure. It has 2 DD statement(s).
Extracted step notes: ` Unload the processed transaction category balance file
- Inputs: AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS
- Outputs: AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)

### Step 3: `STEP10R`

This step executes `SORT` and sorts, filters, or reformats records. It has 4 DD statement(s).
Extracted step notes: Filter the TCATBALFions for a the parm date and sort by card num
- Inputs: AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)
- Outputs: AWS.M2.CARDDEMO.TCATBALF.REPT
- Inline SYSIN: 10 control line(s) are supplied to the step.

## 4. Dataset and Dependency Context

- Input datasets: AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)
- Output datasets: AWS.M2.CARDDEMO.TCATBALF.REPT, AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)
- System/control DDs: SYSOUT
- Downstream jobs that also reference the created/managed VSAM dataset: INTCALC/STEP15, POSTTRAN/STEP15, TCATBALF/STEP15
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
