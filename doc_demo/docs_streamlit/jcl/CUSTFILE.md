# JCL Job: CUSTFILE

| Attribute | Value |
|-----------|-------|
| File | `CUSTFILE.jcl` |
| Description | DEFINE CUSTOMER FILE |
| Job Class | A |
| Msg Class | 0 |
| Steps | 5 |


## Job Steps

### Step 1: CLCIFIL

| Attribute | Value |
|-----------|-------|
| Step Name | `CLCIFIL` |
| Type | PGM |
| Program | `SDSF` |
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
> ********************************************************************  
> Close files in CICS region  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /F CICSAWSA,'CEMT SET FIL(CUSTDAT ) CLO'                                       
```

---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DELETE CUSTOMER VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
```

---
### Step 3: STEP10

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP10` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DEFINE CUSTOMER VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(9 0) -                                                           
          RECORDSIZE(500 500) -                                                 
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS.INDEX) -               
          )                                                                     
```

---
### Step 4: STEP15

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
| `CUSTDATA` | `AWS.M2.CARDDEMO.CUSTDATA.PS` | SHR | INPUT |  |  |
| `CUSTVSAM` | `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(CUSTDATA) OUTFILE(CUSTVSAM)                                     
```

---
### Step 5: OPCIFIL

| Attribute | Value |
|-----------|-------|
| Step Name | `OPCIFIL` |
| Type | PGM |
| Program | `SDSF` |
> ********************************************************************  
> Open files in CICS region  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /F CICSAWSA,'CEMT SET FIL(CUSTDAT ) OPE'                                       
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)
- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.CUSTDATA.PS`
- `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*