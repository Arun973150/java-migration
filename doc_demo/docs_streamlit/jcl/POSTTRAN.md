# JCL Job: POSTTRAN

| Attribute | Value |
|-----------|-------|
| File | `POSTTRAN.jcl` |
| Description | POSTTRAN |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP15

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP15` |
| Type | PGM |
| Program | [CBTRN02C](../programs/CBTRN02C.md) |
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
> *******************************************************************  
> Process and load daily transaction file and create transaction  
> category balance and update transaction master vsam  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `TRANFILE` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `DALYTRAN` | `AWS.M2.CARDDEMO.DALYTRAN.PS` | SHR | INPUT |  |  |
| `XREFFILE` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |
| `DALYREJS` | `AWS.M2.CARDDEMO.DALYREJS(+1)` | NEW | OUTPUT | F | 430 |
| `ACCTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `TCATBALF` | `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS` | SHR | INPUT |  |  |


---

## Summary

### COBOL Programs Executed

- [CBTRN02C](../programs/CBTRN02C.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`
- `AWS.M2.CARDDEMO.DALYTRAN.PS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.DALYREJS(+1)`

---

*Generated 2026-03-16 19:39*