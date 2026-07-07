# JCL Job: CICCMP

| Attribute | Value |
|-----------|-------|
| File | `CICCMP.jcl` |
| Description | Compile CICS Program |
| Job Class | A |
| Msg Class | H |
| Steps | 2 |


## Job Steps

### Step 1: CICSCMP

| Attribute | Value |
|-----------|-------|
| Step Name | `CICSCMP` |
| Type | PROC |
| Procedure | `BUILDONL` |
> ********************************************************************  
> compile the COBOL code:  
> ********************************************************************



---
### Step 2: NEWCOPY

| Attribute | Value |
|-----------|-------|
| Step Name | `NEWCOPY` |
| Type | PGM |
| Program | `SDSF` || COND | `4,LT` |
> ********************************************************************  
> ***  CICS commands in batch to perform NEWCOPY                ******  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /MODIFY CICSAWSA,'CEMT SET PROG(CICSPGMN) NEWCOPY'                             
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)



---

*Generated 2026-03-16 19:39*