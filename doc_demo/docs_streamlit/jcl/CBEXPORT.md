# JCL Job: CBEXPORT

| Attribute | Value |
|-----------|-------|
| File | `CBEXPORT.jcl` |
| Description | Export Customer Data for Migration |
| Job Class | A |
| Msg Class | 0 |
| Steps | 2 |


## Job Steps

### Step 1: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | UTIL |
| Program | `IDCAMS` |
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
> EXPORT CUSTOMER DATA FROM VSAM FILES TO MULTI-RECORD EXPORT FILE  
> FOR BRANCH MIGRATION OR DATA TRANSFER PURPOSES  
> *******************************************************************  
> STEP 1: DEFINE VSAM CLUSTER FOR EXPORT FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  DELETE AWS.M2.CARDDEMO.EXPORT.DATA CLUSTER PURGE
  SET MAXCC = 0
  
  DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.EXPORT.DATA) -
                  INDEXED -
                  KEYS(4 28) -
                  RECORDSIZE(500 500) -
                  CYLINDERS(10 5) -
                  FREESPACE(10 10) -
                  SHAREOPTIONS(2 3)) -
         DATA (NAME(AWS.M2.CARDDEMO.EXPORT.DATA.DATA)) -
         INDEX (NAME(AWS.M2.CARDDEMO.EXPORT.DATA.INDEX))
```

---
### Step 2: STEP02

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP02` |
| Type | PGM |
| Program | [CBEXPORT](../programs/CBEXPORT.md) |
> *******************************************************************  
> STEP 2: RUN EXPORT PROGRAM  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `CUSTFILE` | `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `ACCTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `XREFFILE` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |
| `TRANSACT` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `CARDFILE` | `AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `EXPFILE` | `AWS.M2.CARDDEMO.EXPORT.DATA` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |


---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)
- [CBEXPORT](../programs/CBEXPORT.md)

### Input Datasets

- `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.EXPORT.DATA`


---

*Generated 2026-03-16 19:39*