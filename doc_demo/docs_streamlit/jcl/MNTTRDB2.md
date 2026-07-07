# JCL Job: MNTTRDB2

| Attribute | Value |
|-----------|-------|
| File | `MNTTRDB2.jcl` |
| Description |  |
| Job Class | A |
| Msg Class | H |
| Steps | 1 |


## Job Steps

### Step 1: STEP1

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP1` |
| Type | UTIL |
| Program | `IKJEFT01` |
> ******************************************************************//  
> *//  
> USE THIS JOB TO MAINTAIN DB2 TRANSACTION TABLE, INSERTING,      *//  
> UPDATING OR REMOVING RECORDS IN BATCH.                          *//  
> *//  
> INPFILE - THE INPUT FILE TO USE FOR UPDATES. THE ALLOWED VALUES *//  
> ARE:                                                  *//  
> *//  
> COLUMN 1     - A - ADD                                          *//  
> D - DELETE                                       *//  
> U - UPDATE                                       *//  
> * - COMMENT                                      *//  
> *//  
> COLUMNS 2-3  - TRANSACTION TYPE. NUMERIC VALUE                  *//  
> *//  
> COLUMNS 4-53 - TRANSACTION DESCRIPTION                          *//  
> *//  
> ******************************************************************//

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.DAZ1.SDSNEXIT` | SHR | SYSTEM |  |  |
| `DBRMLIB` | `AWS.M2.CARDDEMO.DBRMLIB` | SHR | INPUT |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `INPFILE` | `INPFILE` | SHR | INPUT |  |  |

#### Inline SYSIN

```
     DSN SYSTEM(DAZ1)
          RUN PROGRAM(COBTUPDT) PLAN(CARDDEMO)
```

---

## Summary

### COBOL Programs Executed

- [IKJEFT01](../programs/IKJEFT01.md)

### Input Datasets

- `AWS.M2.CARDDEMO.DBRMLIB`
- `INPFILE`


---

*Generated 2026-03-16 19:39*