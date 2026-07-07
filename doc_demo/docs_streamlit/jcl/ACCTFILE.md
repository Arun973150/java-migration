# JCL Job: ACCTFILE

| Attribute | Value |
|-----------|-------|
| File | `ACCTFILE.jcl` |
| Description | Delete define Account Data |
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
> DELETE ACCOUNT VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
```

---
### Step 2: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DEFINE ACCOUNT VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(11 0) -                                                          
          RECORDSIZE(300 300) -                                                 
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS.INDEX) -               
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
| `ACCTDATA` | `AWS.M2.CARDDEMO.ACCTDATA.PS` | SHR | INPUT |  |  |
| `ACCTVSAM` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(ACCTDATA) OUTFILE(ACCTVSAM)                                     
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.ACCTDATA.PS`
- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*