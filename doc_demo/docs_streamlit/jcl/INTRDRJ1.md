# JCL Job: INTRDRJ1

| Attribute | Value |
|-----------|-------|
| File | `INTRDRJ1.JCL` |
| Description |  |
| Job Class | A |
| Msg Class | H |
| Steps | 2 |


## Job Steps

### Step 1: IDCAMS

| Attribute | Value |
|-----------|-------|
| Step Name | `IDCAMS` |
| Type | UTIL |
| Program | `IDCAMS` |
> ********************************************************************  
> ** THIS INTRDR JOB WILL TRIGGER ANOTHER JCL  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `IN` | `AWS.M2.CARDEMO.FTP.TEST` | SHR | INPUT |  |  |
| `OUT` | `AWS.M2.CARDEMO.FTP.TEST.BKUP` | SHR | INPUT |  |  |

#### Inline SYSIN

```
  REPRO IFILE(IN) OFILE(OUT)
```

---
### Step 2: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | UTIL |
| Program | `IEBGENER` |
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `AWS.M2.CARDDEMO.JCL(INTRDRJ2)` | SHR | INPUT |  |  |
| `SYSUT2` | `` |  | UNKNOWN |  | 80 |


---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)
- [IEBGENER](../programs/IEBGENER.md)

### Input Datasets

- `AWS.M2.CARDEMO.FTP.TEST`
- `AWS.M2.CARDEMO.FTP.TEST.BKUP`
- `AWS.M2.CARDDEMO.JCL(INTRDRJ2)`


---

*Generated 2026-03-16 19:39*