# JCL Job: CBIMPORT

| Attribute | Value |
|-----------|-------|
| File | `CBIMPORT.jcl` |
| Description | Import CARDDEMO Data |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | PGM |
| Program | [CBIMPORT](../programs/CBIMPORT.md) |
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
> IMPORT CUSTOMER DATA FROM MULTI-RECORD EXPORT FILE AND SPLIT  
> INTO SEPARATE NORMALIZED FILES FOR TARGET SYSTEM  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `EXPFILE` | `AWS.M2.CARDDEMO.EXPORT.DATA` | SHR | INPUT |  |  |
| `CUSTOUT` | `AWS.M2.CARDDEMO.CUSTDATA.IMPORT` | NEW | OUTPUT | FB | 500 |
| `ACCTOUT` | `AWS.M2.CARDDEMO.ACCTDATA.IMPORT` | NEW | OUTPUT | FB | 300 |
| `XREFOUT` | `AWS.M2.CARDDEMO.CARDXREF.IMPORT` | NEW | OUTPUT | FB | 50 |
| `TRNXOUT` | `AWS.M2.CARDDEMO.TRANSACT.IMPORT` | NEW | OUTPUT | FB | 350 |
| `ERROUT` | `AWS.M2.CARDDEMO.IMPORT.ERRORS` | NEW | OUTPUT | FB | 132 |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |


---

## Summary

### COBOL Programs Executed

- [CBIMPORT](../programs/CBIMPORT.md)

### Input Datasets

- `AWS.M2.CARDDEMO.EXPORT.DATA`

### Output Datasets

- `AWS.M2.CARDDEMO.CUSTDATA.IMPORT`
- `AWS.M2.CARDDEMO.ACCTDATA.IMPORT`
- `AWS.M2.CARDDEMO.CARDXREF.IMPORT`
- `AWS.M2.CARDDEMO.TRANSACT.IMPORT`
- `AWS.M2.CARDDEMO.IMPORT.ERRORS`

---

*Generated 2026-03-16 19:39*