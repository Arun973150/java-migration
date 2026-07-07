# JCL Job: INTRDRJ2

| Attribute | Value |
|-----------|-------|
| File | `INTRDRJ2.JCL` |
| Description |  |
| Job Class | A |
| Msg Class | H |
| Steps | 1 |


## Job Steps

### Step 1: IDCAMS

| Attribute | Value |
|-----------|-------|
| Step Name | `IDCAMS` |
| Type | UTIL |
| Program | `IDCAMS` |
> ********************************************************************  
> ***  THIS JOB IS TO CREATE PHYSICAL VSAM FILE FOR IMS DEMODB    ****  
> ***  AND INDEX DEMODX                                           ****  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `IN` | `AWS.M2.CARDEMO.FTP.TEST.BKUP` | SHR | INPUT |  |  |
| `OUT` | `AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR` | SHR | INPUT |  |  |

#### Inline SYSIN

```
  REPRO IFILE(IN) OFILE(OUT)
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDEMO.FTP.TEST.BKUP`
- `AWS.M2.CARDEMO.FTP.TEST.BKUP.INTRDR`


---

*Generated 2026-03-16 19:39*