# JCL Job: TRANIDX

| Attribute | Value |
|-----------|-------|
| File | `TRANIDX.jcl` |
| Description | Define AIX on Transaction Master |
| Job Class | A |
| Msg Class | 0 |
| Steps | 3 |


## Job Steps

### Step 1: STEP20

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP20` |
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
> -------------------------------------------------------------------*  
> CREATE ALTERNATE INDEX ON PROCESSED TIMESTAMP  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE ALTERNATEINDEX (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX)-              
   RELATE(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS)                    -              
   KEYS(26 304)                                                  -             
   NONUNIQUEKEY                                                  -              
   UPGRADE                                                       -              
   RECORDSIZE(350,350)                                           -              
   VOLUMES(AWSHJ1)                                               -              
   CYLINDERS(5,1))                                               -              
   DATA (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.DATA))           -              
   INDEX (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.INDEX))                        
```

---
### Step 2: STEP25

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP25` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> DEFINE PATH IS USED TO RELATE THE ALTERNATE INDEX TO BASE CLUSTER  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  DEFINE PATH                                           -                       
   (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX.PATH)        -                       
    PATHENTRY(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX))                               
```

---
### Step 3: STEP30

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP30` |
| Type | UTIL |
| Program | `IDCAMS` |
> ------------------------------------------------------------------  
> BUILD ALTERNATE INDEX CLUSTER  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   BLDINDEX                                                      -              
   INDATASET(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS)                 -              
   OUTDATASET(AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX)                                
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)



---

*Generated 2026-03-16 19:39*