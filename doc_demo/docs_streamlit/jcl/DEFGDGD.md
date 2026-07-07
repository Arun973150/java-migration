# JCL Job: DEFGDGD

| Attribute | Value |
|-----------|-------|
| File | `DEFGDGD.jcl` |
| Description | DEF DB2 GDG |
| Job Class | A |
| Msg Class | 0 |
| Steps | 6 |


## Job Steps

### Step 1: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` |
> RESTART=STEP30                                                     JOB05067  
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
> This jcl will create GDGs and load first generation for  
> Transaction reference data  
> *******************************************************************  
> Define GDG for Transaction Type  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE GENERATIONDATAGROUP -
   (NAME(AWS.M2.CARDDEMO.TRANTYPE.BKUP) -
    LIMIT(5) -
    SCRATCH -
   )
```

---
### Step 2: STEP20

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP20` |
| Type | UTIL |
| Program | `IEBGENER` || COND | `0,NE` |
> *******************************************************************  
> Create the first generation of GDG Transaction Type  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `AWS.M2.CARDDEMO.TRANTYPE.PS` | SHR | INPUT |  |  |
| `SYSUT2` | `AWS.M2.CARDDEMO.TRANTYPE.BKUP(+1)` | NEW | OUTPUT | FB | 60 |


---
### Step 3: STEP30

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP30` |
| Type | UTIL |
| Program | `IDCAMS` || COND | `0,NE` |
> *******************************************************************  
> Transaction Category type  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE GENERATIONDATAGROUP -
   (NAME(AWS.M2.CARDDEMO.TRANCATG.PS.BKUP) -
    LIMIT(5) -
    SCRATCH -
   )
```

---
### Step 4: STEP40

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP40` |
| Type | UTIL |
| Program | `IEBGENER` || COND | `0,NE` |
> *******************************************************************  
> Create the first generation of GDG Transaction Category Type  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `AWS.M2.CARDDEMO.TRANCATG.PS` | SHR | INPUT |  |  |
| `SYSUT2` | `AWS.M2.CARDDEMO.TRANCATG.PS.BKUP(+1)` | NEW | OUTPUT | FB | 60 |


---
### Step 5: STEP50

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP50` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> Disclosure Group  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE GENERATIONDATAGROUP -
   (NAME(AWS.M2.CARDDEMO.DISCGRP.BKUP) -
    LIMIT(5) -
    SCRATCH -
   )
```

---
### Step 6: STEP60

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP60` |
| Type | UTIL |
| Program | `IEBGENER` || COND | `0,NE` |
> *******************************************************************  
> Create the first generation of GDG disclosure group  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |
| `SYSUT1` | `AWS.M2.CARDDEMO.DISCGRP.PS` | SHR | INPUT |  |  |
| `SYSUT2` | `AWS.M2.CARDDEMO.DISCGRP.BKUP(+1)` | NEW | OUTPUT | FB | 50 |


---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)
- [IEBGENER](../programs/IEBGENER.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANTYPE.PS`
- `AWS.M2.CARDDEMO.TRANCATG.PS`
- `AWS.M2.CARDDEMO.DISCGRP.PS`

### Output Datasets

- `AWS.M2.CARDDEMO.TRANTYPE.BKUP(+1)`
- `AWS.M2.CARDDEMO.TRANCATG.PS.BKUP(+1)`
- `AWS.M2.CARDDEMO.DISCGRP.BKUP(+1)`

---

*Generated 2026-03-16 19:39*