# JCL Job: LOADPADB

| Attribute | Value |
|-----------|-------|
| File | `LOADPADB.JCL` |
| Description | M2APP |
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
> YLIBS JCLLIB ORDER=VIPINGP.CNTL.PROCLIB  
> *********************************************************************  
> EXECUTE IMS PROGRAM  
> *********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | SYSTEM |  |  |
| `DFSRESLB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | INPUT |  |  |
| `IMS` | `OEM.IMS.IMSP.PSBLIB` | SHR | INPUT |  |  |
| `INFILE1` | `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO` | SHR | INPUT |  |  |
| `INFILE2` | `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO` | SHR | INPUT |  |  |
| `DFSVSAMP` | `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)` | SHR | INPUT |  |  |
| `IMSLOGR` | `` |  | UNKNOWN |  |  |
| `IEFRDER` | `` |  | UNKNOWN |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSUDUMP` | `` |  | SYSTEM |  |  |
| `IMSERR` | `` |  | UNKNOWN |  |  |


---

## Summary

### COBOL Programs Executed

- [DFSRRC00](../programs/DFSRRC00.md)

### Input Datasets

- `OEMA.IMS.IMSP.SDFSRESL`
- `OEM.IMS.IMSP.PSBLIB`
- `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO`
- `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO`
- `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)`


---

*Generated 2026-03-16 19:39*