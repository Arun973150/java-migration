# JCL Job: READCUST

| Attribute | Value |
|-----------|-------|
| File | `READCUST.jcl` |
| Description | Read Customer Data file |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | PGM |
| Program | [CBCUS01C](../programs/CBCUS01C.md) |
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
> *******************************************************************  
> RUN THE PROGRAM THAT READS THE CUSTOMER MASTER VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `CUSTFILE` | `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |


---

## Summary

### COBOL Programs Executed

- [CBCUS01C](../programs/CBCUS01C.md)

### Input Datasets

- `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*