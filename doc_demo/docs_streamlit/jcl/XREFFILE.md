# JCL Job: XREFFILE

| Attribute | Value |
|-----------|-------|
| File | `XREFFILE.jcl` |
| Description | Delete define cross ref file |
| Job Class | A |
| Msg Class | 0 |
| Steps | 6 |


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
> DELETE CARD XREF VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
   DELETE  AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX  -                                 
          ALTERNATEINDEX                                                        
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
> DEFINE CARD XREF VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(16 0) -                                                          
          RECORDSIZE(50 50) -                                                   
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS.INDEX) -               
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
| `XREFDATA` | `AWS.M2.CARDDEMO.CARDXREF.PS` | SHR | INPUT |  |  |
| `XREFVSAM` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(XREFDATA) OUTFILE(XREFVSAM)                                     
```

---
### Step 4: STEP20

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP20` |
| Type | UTIL |
| Program | `IDCAMS` |
> ********************************************************************  
> CREATE ALTERNATE INDEX ON ACCT ID  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE ALTERNATEINDEX (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX)-              
   RELATE(AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS)                    -              
   KEYS(11,25)                                                   -              
   NONUNIQUEKEY                                                  -              
   UPGRADE                                                       -              
   RECORDSIZE(50,50)                                             -              
   FREESPACE(10,20)                                              -              
   VOLUMES(AWSHJ1)                                               -              
   CYLINDERS(5,1))                                               -              
   DATA (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.DATA))           -              
   INDEX (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.INDEX))                        
```

---
### Step 5: STEP25

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP25` |
| Type | UTIL |
| Program | `IDCAMS` |
> ********************************************************************  
> DEFINE PATH IS USED TO RELATE THE ALTERNATE INDEX TO BASE CLUSTER  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  DEFINE PATH                                           -                       
   (NAME(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH)        -                       
    PATHENTRY(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX))                               
```

---
### Step 6: STEP30

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP30` |
| Type | UTIL |
| Program | `IDCAMS` |
> ********************************************************************  
> BUILD ALTERNATE INDEX CLUSTER  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   BLDINDEX                                                      -              
   INDATASET(AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS)                 -              
   OUTDATASET(AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX)                                
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.CARDXREF.PS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*