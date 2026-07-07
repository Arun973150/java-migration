# JCL Job: TRANCATG

| Attribute | Value |
|-----------|-------|
| File | `TRANCATG.jcl` |
| Description | DEFINE TRAN CATEGORY |
| Job Class | A |
| Msg Class | 0 |
| Steps | 3 |


## Job Steps

### Step 1: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
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
> *****************************************************************  
> *******************************************************************  
> DELETE TRANSACTION CATEGORY TYPE VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS -                                  
          CLUSTER                                                               
   SET    MAXCC = 0                                                             
```

---
### Step 2: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DEFINE TRANSACTION CATEGORY TYPE VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(6 0) -                                                           
          RECORDSIZE(60 60) -                                                   
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS.INDEX) -               
          )                                                                     
```

---
### Step 3: STEP15

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP15` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> COPY DATA FROM FLAT FILE TO VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `TRANCATG` | `AWS.M2.CARDDEMO.TRANCATG.PS` | SHR | INPUT |  |  |
| `TCATVSAM` | `AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS` | OLD | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(TRANCATG) OUTFILE(TCATVSAM)                                     
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANCATG.PS`
- `AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*