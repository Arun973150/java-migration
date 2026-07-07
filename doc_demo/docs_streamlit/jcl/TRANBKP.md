# JCL Job: TRANBKP

| Attribute | Value |
|-----------|-------|
| File | `TRANBKP.jcl` |
| Description | REPRO and Delete Transaction Master |
| Job Class | A |
| Msg Class | 0 |
| Steps | 3 |


## Job Steps

### Step 1: STEP05R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05R` |
| Type | PROC |
| Procedure | `REPROC` |
> *******************************************************************  
> Repro the processed transaction file  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `PRC001.FILEIN` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `PRC001.FILEOUT` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)` | NEW | OUTPUT | FB | 350 |


---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DELETE TRANSACATION MASTER VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
   DELETE AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX -                                   
          ALTERNATEINDEX                                                        
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
```

---
### Step 3: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` || COND | `4,LT` |
> *******************************************************************  
> DEFINE TRANSACATION MASTER VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(16 0) -                                                          
          RECORDSIZE(350 350) -                                                 
          SHAREOPTIONS(2 3) -                                 
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS.INDEX) -               
          )                                                                     
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)`

---

*Generated 2026-03-16 19:39*