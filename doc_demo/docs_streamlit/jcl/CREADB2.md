# JCL Job: CREADB2

| Attribute | Value |
|-----------|-------|
| File | `CREADB21.jcl` |
| Description |  |
| Job Class | A |
| Msg Class | A |
| Steps | 5 |


## Job Steps

### Step 1: FREEPLN

| Attribute | Value |
|-----------|-------|
| Step Name | `FREEPLN` |
| Type | UTIL |
| Program | `IKJEFT01` |
> ******************************************************************** 00100123  
> ***  STEP 00 : Free existing plans and packages               ****** 00100223  
> ***          : It ends with RC 8 if not existing.             ****** 00100324  
> ***          : So dont run it if creating new database        ****** 00100424  
> ******************************************************************** 00100524

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.DAZ1.SDSNEXIT` | SHR | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSTSIN` | `&LBNM..CNTL(DB2FREE)` | SHR | INPUT |  |  |


---
### Step 2: CRCRDDB

| Attribute | Value |
|-----------|-------|
| Step Name | `CRCRDDB` |
| Type | UTIL |
| Program | `IKJEFT01` |
> ******************************************************************** 00110004  
> ***  STEP 10 : Use Utility DSNTIAD to create the database     ****** 00120019  
> ***            This uses an existing STOGROUP AWST1STG        ****** 00121018  
> ***            You would have to create it if not available   ****** 00122023  
> ******************************************************************** 00130004

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.&DB2S..RUNLIB.LOAD` | SHR | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSTSIN` | `&LBNM..CNTL(DB2TIAD1)` | SHR | INPUT |  |  |
| `SYSIN` | `&LBNM..CNTL(DB2CREAT)` | SHR | INPUT |  |  |


---
### Step 3: LDTTYPE

| Attribute | Value |
|-----------|-------|
| Step Name | `LDTTYPE` |
| Type | UTIL |
| Program | `IEFBR14` || COND | `0,NE` |
> ******************************************************************** 00470011  
> ***  STEP 20 : Load the transaction Type table                ****** 00480019  
> ***            using DSNTEP4 utility                          ****** 00481019  
> ******************************************************************** 00490011



---
### Step 4: RUNTEP2

| Attribute | Value |
|-----------|-------|
| Step Name | `RUNTEP2` |
| Type | UTIL |
| Program | `IKJEFT01` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.&DB2S..RUNLIB.LOAD` | SHR | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSTSIN` | `&LBNM..CNTL(DB2TEP41)` | SHR | INPUT |  |  |
| `SYSIN` | `&LBNM..CNTL(DB2LTTYP)` | SHR | INPUT |  |  |


---
### Step 5: LDTCCAT

| Attribute | Value |
|-----------|-------|
| Step Name | `LDTCCAT` |
| Type | UTIL |
| Program | `IKJEFT01` || COND | `0,NE` |
> ******************************************************************** 00750015  
> ***  STEP 30 : Load Transaction Type Category table           ****** 00760019  
> ***            using DSNTEP4 utility                          ****** 00761019  
> ******************************************************************** 00770015

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.&DB2S..RUNLIB.LOAD` | SHR | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSTSIN` | `&LBNM..CNTL(DB2TEP41)` | SHR | INPUT |  |  |
| `SYSIN` | `&LBNM..CNTL(DB2LTCAT)` | SHR | INPUT |  |  |


---

## Summary

### COBOL Programs Executed

- [IKJEFT01](../programs/IKJEFT01.md)
- [IEFBR14](../programs/IEFBR14.md)

### Input Datasets

- `&LBNM..CNTL(DB2FREE)`
- `&LBNM..CNTL(DB2TIAD1)`
- `&LBNM..CNTL(DB2CREAT)`
- `&LBNM..CNTL(DB2TEP41)`
- `&LBNM..CNTL(DB2LTTYP)`
- `&LBNM..CNTL(DB2LTCAT)`


---

*Generated 2026-03-16 19:39*