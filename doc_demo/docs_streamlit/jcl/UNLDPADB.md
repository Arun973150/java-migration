# JCL Job: UNLDPADB

| Attribute | Value |
|-----------|-------|
| File | `UNLDPADB.JCL` |
| Description | M2APP |
| Job Class | A |
| Msg Class | H |
| Steps | 2 |


## Job Steps

### Step 1: STEP0

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP0` |
| Type | UTIL |
| Program | `IEFBR14` |
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
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSDUMP` | `` |  | UNKNOWN |  |  |
| `DD1` | `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO` | OLD | INPUT |  |  |
| `DD2` | `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO` | OLD | INPUT |  |  |


---
### Step 2: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | PGM |
| Program | `DFSRRC00` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | SYSTEM |  |  |
| `DFSRESLB` | `OEMA.IMS.IMSP.SDFSRESL` | SHR | INPUT |  |  |
| `IMS` | `OEM.IMS.IMSP.PSBLIB` | SHR | INPUT |  |  |
| `OUTFIL1` | `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO` | NEW | OUTPUT | FB | 100 |
| `OUTFIL2` | `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO` | NEW | OUTPUT | FB | 206 |
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

- [IEFBR14](../programs/IEFBR14.md)
- [DFSRRC00](../programs/DFSRRC00.md)

### Input Datasets

- `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO`
- `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO`
- `OEMA.IMS.IMSP.SDFSRESL`
- `OEM.IMS.IMSP.PSBLIB`
- `OEM.IMS.IMSP.PAUTHDB`
- `OEM.IMS.IMSP.PAUTHDBX`
- `OEMPP.IMS.V15R01MB.PROCLIB(DFSVSMDB)`

### Output Datasets

- `AWS.M2.CARDDEMO.PAUTDB.ROOT.FILEO`
- `AWS.M2.CARDDEMO.PAUTDB.CHILD.FILEO`

---

*Generated 2026-03-16 19:39*