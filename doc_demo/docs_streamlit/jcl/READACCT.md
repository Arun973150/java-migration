# JCL Job: READACCT

| Attribute | Value |
|-----------|-------|
| File | `READACCT.jcl` |
| Description | READACCT |
| Job Class | A |
| Msg Class | H |
| Steps | 2 |


## Job Steps

### Step 1: PREDEL

| Attribute | Value |
|-----------|-------|
| Step Name | `PREDEL` |
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
> *******************************************************************  
> PRE DELETE STEP  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `DD01` | `AWS.M2.CARDDEMO.ACCTDATA.PSCOMP` | MOD | OUTPUT |  |  |
| `DD02` | `AWS.M2.CARDDEMO.ACCTDATA.ARRYPS` | MOD | OUTPUT |  |  |
| `DD03` | `AWS.M2.CARDDEMO.ACCTDATA.VBPS` | MOD | OUTPUT |  |  |


---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | PGM |
| Program | [CBACT01C](../programs/CBACT01C.md) |
> *******************************************************************  
> RUN THE PROGRAM THAT READS THE ACCOUNT MASTER VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `ACCTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `OUTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.PSCOMP` | NEW | OUTPUT | FB | 107 |
| `ARRYFILE` | `AWS.M2.CARDDEMO.ACCTDATA.ARRYPS` | NEW | OUTPUT | FB | 110 |
| `VBRCFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VBPS` | NEW | OUTPUT | VB | 84 |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |


---

## Summary

### COBOL Programs Executed

- [IEFBR14](../programs/IEFBR14.md)
- [CBACT01C](../programs/CBACT01C.md)

### Input Datasets

- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.ACCTDATA.PSCOMP`
- `AWS.M2.CARDDEMO.ACCTDATA.ARRYPS`
- `AWS.M2.CARDDEMO.ACCTDATA.VBPS`

---

*Generated 2026-03-16 19:39*