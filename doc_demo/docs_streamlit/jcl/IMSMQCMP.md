# JCL Job: IMSMQCMP

| Attribute | Value |
|-----------|-------|
| File | `IMSMQCMP.jcl` |
| Description |  |
| Job Class | A |
| Msg Class |  |
| Steps | 3 |


## Job Steps

### Step 1: TRN

| Attribute | Value |
|-----------|-------|
| Step Name | `TRN` |
| Type | PGM |
| Program | `DFHECP1` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `&CICSHLQ..CICS.SDFHLOAD` | SHR | SYSTEM |  |  |
| `SYSIN` | `&HLQ..COBOL.SRC(IMSMQPGM)` | SHR | INPUT |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSPUNCH` | `&&SYSCIN` |  | UNKNOWN |  |  |


---
### Step 2: COBOL

| Attribute | Value |
|-----------|-------|
| Step Name | `COBOL` |
| Type | PGM |
| Program | `IGYCRCTL` || COND | `4,LT` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `` | SHR | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSLIN` | `` | MOD | OUTPUT |  |  |
| `SYSUT1` | `` |  | UNKNOWN |  |  |
| `SYSUT2` | `` |  | UNKNOWN |  |  |
| `SYSUT3` | `` |  | UNKNOWN |  |  |
| `SYSUT4` | `` |  | UNKNOWN |  |  |
| `SYSUT5` | `` |  | UNKNOWN |  |  |
| `SYSUT6` | `` |  | UNKNOWN |  |  |
| `SYSUT7` | `` |  | UNKNOWN |  |  |
| `SYSUT8` | `` |  | UNKNOWN |  |  |
| `SYSUT9` | `` |  | UNKNOWN |  |  |
| `SYSUT10` | `` |  | UNKNOWN |  |  |
| `SYSUT11` | `` |  | UNKNOWN |  |  |
| `SYSUT12` | `` |  | UNKNOWN |  |  |
| `SYSUT13` | `` |  | UNKNOWN |  |  |
| `SYSUT14` | `` |  | UNKNOWN |  |  |
| `SYSUT15` | `` |  | UNKNOWN |  |  |
| `SYSMDECK` | `` |  | UNKNOWN |  |  |
| `SYSLIB` | `CEE.SCEESAMP` | SHR | INPUT |  |  |
| `SYSIN` | `&&SYSCIN` | OLD | INPUT |  |  |


---
### Step 3: COPYIMS

| Attribute | Value |
|-----------|-------|
| Step Name | `COPYIMS` |
| Type | UTIL |
| Program | `IEBGENER` || COND | `4,LT` |
> *********************************  
> COPY LINK STEP  
> *********************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   ENTRY IMSMQPGM
   NAME IMSMQPGM(R)
//SYSUT2   DD DSN=&&COPYIMS,DISP=(NEW,PASS), DCB=(LRECL=80,BLKSIZE=400,RECFM=FB), UNIT=3390,SPACE=(400,(20,20))
//SYSPRINT DD SYSOUT=*
//SYSIN    DD DUMMY
//*
//COPYLINK EXEC PGM=IEBGENER,COND=(4,LT)
//SYSUT1   DD *
  INCLUDE SYSLIB(DFHELII)
//SYSUT2   DD DSN=&&COPYLINK,DISP=(NEW,PASS), DCB=(LRECL=80,BLKSIZE=400,RECFM=FB), UNIT=3390,SPACE=(400,(20,20))
//SYSPRINT DD SYSOUT=*
//SYSIN    DD DUMMY
//*
//COPYMQ   EXEC PGM=IEBGENER,COND=(4,LT)
//SYSUT1   DD *
 INCLUDE CSQSTUB(CSQCSTUB)
//SYSUT2   DD DSN=&&COPYMQ,DISP=(NEW,PASS), DCB=(LRECL=80,BLKSIZE=400,RECFM=FB), UNIT=3390,SPACE=(400,(20,20))
//SYSPRINT DD SYSOUT=*
//SYSIN    DD DUMMY
//*
//LKED   EXEC PGM=IEWL,REGION=0M,PARM='LIST,XREF',COND=(4,LT)
//SYSLIB   DD DSN=&MQHLQ..SCSQLOAD,DISP=SHR DD DSN=SYS1.LINKLIB,DISP=SHR DD DSN=CEE.SCEELKED,DISP=SHR DD DSN=&CICSHLQ..CICS.SDFHLOAD,DISP=SHR DD DSN=&IMSHLQ..SDFSRESL,DISP=SHR
//CSQSTUB  DD DSN=&MQHLQ..SCSQLOAD,DISP=SHR
//SYSLIN   DD DSN=&&COPYLINK,DISP=(OLD,DELETE) DD DSN=&&COPYMQ,DISP=(OLD,DELETE) DD DSN=&&LOADSET,DISP=(OLD,DELETE) DD DSN=&&COPYIMS,DISP=(OLD,DELETE)
//SYSPRINT DD SYSOUT=*
//SYSLMOD  DD DSNAME=&HLQ..CICSLOAD(IMSMQPGM), DISP=SHR
//SYSUT1   DD UNIT=VIO,SPACE=(TRK,(10,10))
```

---

## Summary

### COBOL Programs Executed

- [DFHECP1](../programs/DFHECP1.md)
- [IGYCRCTL](../programs/IGYCRCTL.md)
- [IEBGENER](../programs/IEBGENER.md)

### Input Datasets

- `&HLQ..COBOL.SRC(IMSMQPGM)`
- `CEE.SCEESAMP`
- `&&SYSCIN`


---

*Generated 2026-03-16 19:39*