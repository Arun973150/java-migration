# JCL Job: UNLDGSAM

| Attribute | Value |
|-----------|-------|
| File | `UNLDGSAM.JCL` |
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
> *********************************************************************  
> EXECUTE IMS PROGRAM  
> *********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | SYSTEM |  |  |
| `DFSRESLB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | INPUT |  |  |
| `IMS` | `OEM.IMS.IMSP.PSBLIB` | SHR | INPUT |  |  |
| `PASFILOP` | `AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM` | OLD | INPUT |  |  |
| `PADFILOP` | `AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM` | OLD | INPUT |  |  |
| `DDPAUTP0` | `OEM.IMS.IMSP.PAUTHDB` | SHR | INPUT |  |  |
| `DDPAUTX0` | `OEM.IMS.IMSP.PAUTHDBX` | SHR | INPUT |  |  |
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
- `AWS.M2.CARDDEMO.PAUTDB.ROOT.GSAM`
- `AWS.M2.CARDDEMO.PAUTDB.CHILD.GSAM`
- `OEM.IMS.IMSP.PAUTHDB`
- `OEM.IMS.IMSP.PAUTHDBX`
- `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)`


---

*Generated 2026-03-16 19:39*