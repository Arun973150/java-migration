# JCL Job: TRANEXTR

| Attribute | Value |
|-----------|-------|
| File | `TRANEXTR.jcl` |
| Description | EXTRACT TRAN TYPE |
| Job Class | A |
| Msg Class | 0 |
| Steps | 5 |


## Job Steps

### Step 1: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IEBGENER` |
> ********************************************************************  
> ***  Db2 Unload using DSNTIAUL utility                        ******  
> ********************************************************************  
> **   STEP 10 : BACKUP THE PREVIOUS VERSION OF TRANTYPE FILE TO GDG  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `&HLQ..TRANTYPE.PS` | SHR | INPUT |  |  |
| `SYSUT2` | `&HLQ..TRANTYPE.BKUP(+1)` | NEW | OUTPUT | FB | 60 |


---
### Step 2: STEP20

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP20` |
| Type | UTIL |
| Program | `IEBGENER` || COND | `0,NE` |
> ********************************************************************  
> **   STEP 20 : BACKUP THE PREVIOUS VERSION OF TRANCATG FILE TO GDG  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `&HLQ..TRANCATG.PS` | SHR | INPUT |  |  |
| `SYSUT2` | `&HLQ..TRANCATG.PS.BKUP(+1)` | NEW | OUTPUT | FB | 60 |


---
### Step 3: STEP30

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP30` |
| Type | UTIL |
| Program | `IEFBR14` || COND | `0,NE` |
> ********************************************************************  
> ***  STEP 30 : DELETE FILES FROM PREVIOUS RUN                 ******  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `DD01` | `&HLQ..TRANTYPE.PS` | MOD | OUTPUT |  |  |
| `DD02` | `&HLQ..TRANCATG.PS` | MOD | OUTPUT |  |  |


---
### Step 4: STEP40

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP40` |
| Type | UTIL |
| Program | `IKJEFT01` || COND | `0,NE` |
> ********************************************************************  
> ***  STEP 40 : EXTRACT DATA FROM TRANSACTION TYPE TABLE       ******  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.DAZ1.RUNLIB.LOAD` | SHR | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSPUNCH` | `` |  | UNKNOWN |  |  |
| `SYSREC00` | `&HLQ..TRANTYPE.PS` | NEW | OUTPUT |  |  |

#### Inline SYSIN

```
 SELECT CAST(CONCAT(CONCAT(
   TR_TYPE
  ,CAST(TR_DESCRIPTION AS CHAR(50))
   )
  ,REPEAT('0',8)
 ) AS CHAR(60))
  FROM
  CARDDEMO.TRANSACTION_TYPE
  ORDER BY TR_TYPE;
  DSN SYSTEM(DAZ1)
  RUN PROGRAM(DSNTIAUL) -
  PLAN(DSNTIAUL) -
  PARMS('SQL')
```

---
### Step 5: STEP50

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP50` |
| Type | UTIL |
| Program | `IKJEFT01` || COND | `4,LT` |
> ********************************************************************  
> ***  STEP 50 : EXTRACT DATA FROM TRANSACTION TYPE TABLE       ******  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEM.DB2.DAZ1.RUNLIB.LOAD` | SHR | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `SYSPUNCH` | `` |  | UNKNOWN |  |  |
| `SYSREC00` | `&HLQ..TRANCATG.PS` | NEW | OUTPUT |  |  |

#### Inline SYSIN

```
  SELECT CAST(
        TRC_TYPE_CODE
     || TRC_TYPE_CATEGORY
     || CAST(TRC_CAT_DATA AS CHAR(50))
     || REPEAT('0',4)
                      AS CHAR(60))
  FROM  CARDDEMO.TRANSACTION_TYPE_CATEGORY
  ORDER BY
        TRC_TYPE_CODE
      , TRC_TYPE_CATEGORY;
  DSN SYSTEM(DAZ1)
  RUN PROGRAM(DSNTIAUL) -
  PLAN(DSNTIAUL) -
  PARMS('SQL')
```

---

## Summary

### COBOL Programs Executed

- [IEBGENER](../programs/IEBGENER.md)
- [IEFBR14](../programs/IEFBR14.md)
- [IKJEFT01](../programs/IKJEFT01.md)

### Input Datasets

- `&HLQ..TRANTYPE.PS`
- `&HLQ..TRANCATG.PS`

### Output Datasets

- `&HLQ..TRANTYPE.BKUP(+1)`
- `&HLQ..TRANCATG.PS.BKUP(+1)`
- `&HLQ..TRANTYPE.PS`
- `&HLQ..TRANCATG.PS`

---

*Generated 2026-03-16 19:39*