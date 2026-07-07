# JCL Job: CARDFILE

| Attribute | Value |
|-----------|-------|
| File | `CARDFILE.jcl` |
| Description | Delete define card data |
| Job Class | A |
| Msg Class | 0 |
| Steps | 8 |


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
 /F CICSAWSA,'CEMT SET FIL(CARDDAT ) CLO'                                       
 /F CICSAWSA,'CEMT SET FIL(CARDAIX ) CLO'                                       
```

---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DELETE CARD DATA VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
   DELETE AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX -                                   
          ALTERNATEINDEX                                                        
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
> DEFINE CARD DATA VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(16 0) -                                                          
          RECORDSIZE(150 150) -                                                 
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS.INDEX) -               
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
| `CARDDATA` | `AWS.M2.CARDDEMO.CARDDATA.PS` | SHR | INPUT |  |  |
| `CARDVSAM` | `AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(CARDDATA) OUTFILE(CARDVSAM)                                     
```

---
### Step 5: STEP40

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP40` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> CREATE ALTERNATE INDEX ON ACCT ID  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE ALTERNATEINDEX (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX)-              
   RELATE(AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS)                    -              
   KEYS(11 16)                                                   -              
   NONUNIQUEKEY                                                  -              
   UPGRADE                                                       -              
   RECORDSIZE(150,150)                                           -              
   VOLUMES(AWSHJ1)                                               -              
   CYLINDERS(5,1))                                               -              
   DATA (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX.DATA))           -              
   INDEX (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX.INDEX))                        
```

---
### Step 6: STEP50

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP50` |
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
   (NAME(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX.PATH)        -                       
    PATHENTRY(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX))                               
```

---
### Step 7: STEP60

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP60` |
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
   INDATASET(AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS)                 -              
   OUTDATASET(AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX)                                
```

---
### Step 8: OPCIFIL

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
 /F CICSAWSA,'CEMT SET FIL(CARDDAT ) OPE'                                       
 /F CICSAWSA,'CEMT SET FIL(CARDAIX ) OPE'                                       
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)
- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.CARDDATA.PS`
- `AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*