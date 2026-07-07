# JCL Job: CBPAUP0J

| Attribute | Value |
|-----------|-------|
| File | `CBPAUP0J.jcl` |
| Description | CARDDEMO |
| Job Class | A |
| Msg Class | H |
| Steps | 1 |


## Job Steps

### Step 1: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | PGM |
| Program | `DFSRRC00` |
> *****************************************************************  
> Copyright Amazon.com, Inc. or its affiliates.  
> All Rights Reserved.  
> Licensed under the Apache License, Version 2.0 (the "License").  
> You may not use this file except in compliance with the License.  
> You may obtain a copy of the License at  
> http://www.apache.org/licenses/LICENSE-2.0  
> Unless required by applicable law or agreed to in writing,  
> software distributed under the License is distributed on an  
> "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,  
> either express or implied. See the License for the specific  
> language governing permissions and limitations under the License  
> *****************************************************************  
> *********************************************************************  
> EXECUTE IMS PROGRAM TO DELETE EXPIRED AUTHORIZATIONS  
> *********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `IMS.SDFSRESL` | SHR | SYSTEM |  |  |
| `DFSRESLB` | `IMS.SDFSRESL` | SHR | INPUT |  |  |
| `PROCLIB` | `IMS.PROCLIB` | SHR | INPUT |  |  |
| `DFSSEL` | `IMS.SDFSRESL` | SHR | INPUT |  |  |
| `IMS` | `IMS.PSBLIB` | SHR | INPUT |  |  |

#### Inline SYSIN

```
00,00001,00001,Y
//*
//SYSOUX     DD SYSOUT=*
//SYSOUT     DD SYSOUT=*
//SYSABOUT   DD SYSOUT=*
//ABENDAID   DD SYSOUT=*
//IEFRDER    DD DUMMY
//IMSLOGR    DD DUMMY
//SYSPRINT   DD SYSOUT=*
//SYSUDUMP   DD SYSOUT=*
//IMSERR     DD SYSOUT=*
```

---

## Summary

### COBOL Programs Executed

- [DFSRRC00](../programs/DFSRRC00.md)

### Input Datasets

- `IMS.SDFSRESL`
- `IMS.PROCLIB`
- `IMS.PSBLIB`


---

*Generated 2026-03-16 19:39*