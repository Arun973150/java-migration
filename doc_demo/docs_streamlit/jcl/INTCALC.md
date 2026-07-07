# JCL Job: INTCALC

| Attribute | Value |
|-----------|-------|
| File | `INTCALC.jcl` |
| Description | INTEREST CALCULATOR |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP15

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP15` |
| Type | PGM |
| Program | [CBACT04C](../programs/CBACT04C.md) |
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
> Process transaction balance file and compute interest and fees.  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `TCATBALF` | `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS` | SHR | INPUT |  |  |
| `XREFFILE` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |
| `XREFFIL1` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH` | SHR | INPUT |  |  |
| `ACCTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `DISCGRP` | `AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS` | SHR | INPUT |  |  |
| `TRANSACT` | `AWS.M2.CARDDEMO.SYSTRAN(+1)` | NEW | OUTPUT | F | 350 |


---

## Summary

### COBOL Programs Executed

- [CBACT04C](../programs/CBACT04C.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH`
- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.SYSTRAN(+1)`

---

*Generated 2026-03-16 19:39*