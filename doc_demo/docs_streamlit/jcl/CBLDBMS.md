# JCL Job: CBLDBMS

| Attribute | Value |
|-----------|-------|
| File | `BMSCMP.jcl` |
| Description | Compile BMS Map |
| Job Class | A |
| Msg Class | H |
| Steps | 2 |


## Job Steps

### Step 1: STEP1

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP1` |
| Type | PROC |
| Procedure | `BUILDBMS` |



---
### Step 2: SDSF1

| Attribute | Value |
|-----------|-------|
| Step Name | `SDSF1` |
| Type | PGM |
| Program | `SDSF` |
> ********************************************************************  
> ***  CICS commands in batch to Execute NEWCOPY                ******  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /MODIFY CICSAWSA,'CEMT SET PROG(CICSMAP) NEWCOPY'
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)



---

*Generated 2026-03-16 19:39*