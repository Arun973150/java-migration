# JCL Job: PRTCATBL

| Attribute | Value |
|-----------|-------|
| File | `PRTCATBL.jcl` |
| Description | Print Trasaction Category Balance File |
| Job Class | A |
| Msg Class | 0 |
| Steps | 3 |


## Job Steps

### Step 1: DELDEF

| Attribute | Value |
|-----------|-------|
| Step Name | `DELDEF` |
| Type | UTIL |
| Program | `IEFBR14` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `THEFILE` | `AWS.M2.CARDDEMO.TCATBALF.REPT` | MOD | OUTPUT |  |  |


---
### Step 2: STEP05R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05R` |
| Type | PROC |
| Procedure | `REPROC` |
> ********************************************************`***********  
> Unload the processed transaction category balance file  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `PRC001.FILEIN` | `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS` | SHR | INPUT |  |  |
| `PRC001.FILEOUT` | `AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)` | NEW | OUTPUT | FB | 50 |


---
### Step 3: STEP10R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10R` |
| Type | UTIL |
| Program | `SORT` |
> *******************************************************************  
> Filter the TCATBALFions for a the parm date and sort by card num  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SORTIN` | `AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SORTOUT` | `AWS.M2.CARDDEMO.TCATBALF.REPT` | NEW | OUTPUT | FB | 40 |

#### Inline SYSIN

```
TRANCAT-ACCT-ID,1,11,ZD                                                         
TRANCAT-TYPE-CD,12,2,CH                                                         
TRANCAT-CD,14,4,ZD
TRAN-CAT-BAL,18,11,ZD
//SYSIN    DD *                                                                 
 SORT FIELDS=(TRANCAT-ACCT-ID,A,TRANCAT-TYPE-CD,A,TRANCAT-CD,A)                 
 OUTREC FIELDS=(TRANCAT-ACCT-ID,X,
     TRANCAT-TYPE-CD,X,
     TRANCAT-CD,X,
     TRAN-CAT-BAL,EDIT=(TTTTTTTTT.TT),9X)
```

---

## Summary

### COBOL Programs Executed

- [IEFBR14](../programs/IEFBR14.md)
- [SORT](../programs/SORT.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)`

### Output Datasets

- `AWS.M2.CARDDEMO.TCATBALF.REPT`
- `AWS.M2.CARDDEMO.TCATBALF.BKUP(+1)`

---

*Generated 2026-03-16 19:39*