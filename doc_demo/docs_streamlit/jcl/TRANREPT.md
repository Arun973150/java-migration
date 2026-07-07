# JCL Job: TRANREPT

| Attribute | Value |
|-----------|-------|
| File | `TRANREPT.jcl` |
| Description | TRANSACTION REPORT |
| Job Class | A |
| Msg Class | 0 |
| Steps | 2 |


## Job Steps

### Step 1: STEP05R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05R` |
| Type | UTIL |
| Program | `SORT` |
> *******************************************************************  
> Filter the transactions for a the parm date and sort by card num  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `PRC001.FILEIN` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `PRC001.FILEOUT` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)` | NEW | OUTPUT | FB | 350 |
| `SORTIN` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SORTOUT` | `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)` | NEW | OUTPUT |  |  |

#### Inline SYSIN

```
TRAN-CARD-NUM,263,16,ZD                                                         
TRAN-PROC-DT,305,10,CH                                                          
PARM-START-DATE,C'2022-01-01'                                      //Date       
PARM-END-DATE,C'2022-07-06'                                        //Date       
//SYSIN    DD *                                                                 
 SORT FIELDS=(TRAN-CARD-NUM,A)                                                  
 INCLUDE COND=(TRAN-PROC-DT,GE,PARM-START-DATE,AND,                             
         TRAN-PROC-DT,LE,PARM-END-DATE)                                         
```

---
### Step 2: STEP10R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10R` |
| Type | PGM |
| Program | [CBTRN03C](../programs/CBTRN03C.md) |
> *******************************************************************  
> Produce a formatted report for processed transactions  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `TRANFILE` | `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)` | SHR | INPUT |  |  |
| `CARDXREF` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |
| `TRANTYPE` | `AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS` | SHR | INPUT |  |  |
| `TRANCATG` | `AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS` | SHR | INPUT |  |  |
| `DATEPARM` | `AWS.M2.CARDDEMO.DATEPARM` | SHR | INPUT |  |  |
| `TRANREPT` | `AWS.M2.CARDDEMO.TRANREPT(+1)` | NEW | OUTPUT | FB | 133 |


---

## Summary

### COBOL Programs Executed

- [SORT](../programs/SORT.md)
- [CBTRN03C](../programs/CBTRN03C.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)`
- `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS`
- `AWS.M2.CARDDEMO.DATEPARM`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)`
- `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)`
- `AWS.M2.CARDDEMO.TRANREPT(+1)`

---

*Generated 2026-03-16 19:39*