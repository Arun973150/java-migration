# JCL Job: DBPAUTP0

| Attribute | Value |
|-----------|-------|
| File | `DBPAUTP0.jcl` |
| Description | DBPAUTP0 DB UNLOAD |
| Job Class | A |
| Msg Class | X |
| Steps | 2 |


## Job Steps

### Step 1: STEPDEL

| Attribute | Value |
|-----------|-------|
| Step Name | `STEPDEL` |
| Type | UTIL |
| Program | `IEFBR14` |
> *********************************************************************  
> DELETE OUTPUT DATASET  
> *********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSUT1` | `AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0` | MOD | OUTPUT |  |  |


---
### Step 2: UNLOAD

| Attribute | Value |
|-----------|-------|
| Step Name | `UNLOAD` |
| Type | PGM |
| Program | `DFSRRC00` |
> *********************************************************************  
> DOWNLOAD DBD DBPAUTP0  
> *********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | SYSTEM |  |  |
| `DFSRESLB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | INPUT |  |  |
| `IMS` | `OEM.IMS.IMSP.PSBLIB` | SHR | INPUT |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `DFSURGU1` | `AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0` |  | UNKNOWN | VB | 27990 |
| `DDPAUTP0` | `OEM.IMS.IMSP.PAUTHDB` | SHR | INPUT |  |  |
| `DDPAUTX0` | `OEM.IMS.IMSP.PAUTHDBX` | SHR | INPUT |  |  |
| `DFSVSAMP` | `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)` | SHR | INPUT |  |  |

#### Inline SYSIN

```
SBPARM ACTIV=COND                                                               
//SYSUDUMP DD SYSOUT=*, DCB=(RECFM=FBA,LRECL=133), SPACE=(605,(500,500),RLSE,,ROUND)
//*
//RECON1 DD DSN=OEM.IMS.IMSP.RECON1,DISP=SHR                                    
//RECON2 DD DSN=OEM.IMS.IMSP.RECON2,DISP=SHR                                    
//RECON3 DD DSN=OEM.IMS.IMSP.RECON3,DISP=SHR                
//*
//DFSWRK01  DD DUMMY                                                            
//DFSSRT01  DD DUMMY                                                       //*
//*Ver: CardDemo_v2.0-35-gcfa73b2-245 Date: 2025-04-29 17:01:37 CDT
//*
```

---

## Summary

### COBOL Programs Executed

- [IEFBR14](../programs/IEFBR14.md)
- [DFSRRC00](../programs/DFSRRC00.md)

### Input Datasets

- `OEMA.IMS.IMSP.SDFSRESL`
- `OEM.IMS.IMSP.PSBLIB`
- `OEM.IMS.IMSP.PAUTHDB`
- `OEM.IMS.IMSP.PAUTHDBX`
- `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)`

### Output Datasets

- `AWS.M2.CARDDEMO.IMSDATA.DBPAUTP0`

---

*Generated 2026-03-16 19:39*