# JCL Job: REPRTEST

| Attribute | Value |
|-----------|-------|
| File | `REPRTEST.jcl` |
| Description | REPRO TEST JOB |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | PROC |
| Procedure | `REPROC` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `PRC001.FILEIN` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `PRC001.FILEOUT` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)` | NEW | OUTPUT | FB | 350 |


---

## Summary


### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)`

---

*Generated 2026-03-16 19:39*