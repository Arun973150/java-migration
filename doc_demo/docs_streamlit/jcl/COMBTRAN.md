# JCL Job: COMBTRAN

| Attribute | Value |
|-----------|-------|
| File | `COMBTRAN.jcl` |
| Description | COMBINE TRANSACTIONS |
| Job Class | A |
| Msg Class | 0 |
| Steps | 2 |


## Job Steps

### Step 1: STEP05R

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05R` |
| Type | UTIL |
| Program | `SORT` |
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
> Sort current transaction file and system generated transactions  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SORTIN` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(0)` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SORTOUT` | `AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)` | NEW | OUTPUT |  |  |

#### Inline SYSIN

```
TRAN-ID,1,16,CH                                                         
//SYSIN    DD *                                                                 
 SORT FIELDS=(TRAN-ID,A)                                                  
```

---
### Step 2: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> Load combined file to transaction master  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `TRANSACT` | `AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)` | SHR | INPUT |  |  |
| `TRANVSAM` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(TRANSACT) OUTFILE(TRANVSAM)                                     
```

---

## Summary

### COBOL Programs Executed

- [SORT](../programs/SORT.md)
- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.BKUP(0)`
- `AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)`
- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1)`

---

*Generated 2026-03-16 19:39*