# JCL Job: SORTTEST

| Attribute | Value |
|-----------|-------|
| File | `SORTTEST.jcl` |
| Description | SORT STEP TESTING |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


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

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SORTIN` | `AWS.M2.CARDDEMO.TRANSACT.BKUP(0)` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SORTOUT` | `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)` | NEW | OUTPUT |  |  |

#### Inline SYSIN

```
TRAN-CARD-NUM,263,16,ZD
TRAN-PROC-DT,305,10,CH               
PARM-DATE,C'2022-06-02'                              
//SYSIN    DD *                                                         
 SORT FIELDS=(TRAN-CARD-NUM,A) 
 INCLUDE COND=(TRAN-PROC-DT,EQ,PARM-DATE)                                       
```

---

## Summary

### COBOL Programs Executed

- [SORT](../programs/SORT.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.BKUP(0)`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANSACT.DALY(+1)`

---

*Generated 2026-03-16 19:39*