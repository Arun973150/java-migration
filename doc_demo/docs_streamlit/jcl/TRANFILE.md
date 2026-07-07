# JCL Job: TRANFILE

| Attribute | Value |
|-----------|-------|
| File | `TRANFILE.jcl` |
| Description | DEFINE TRANSACTION MASTER |
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
 /F CICSAWSA,'CEMT SET FIL(TRANSACT ) CLO'                                      
 /F CICSAWSA,'CEMT SET FIL(CXACAIX ) CLO'                                       
```

---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DELETE TRANSACATION MASTER VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DELETE AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS -                                  
          CLUSTER                                                               
   IF MAXCC LE 08 THEN SET MAXCC = 0                                            
   DELETE AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX -                                   
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
> DEFINE TRANSACATION MASTER VSAM FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS) -                   
          CYLINDERS(1 5) -                                                      
          VOLUMES(AWSHJ1 -                                                      
          ) -                                                                   
          KEYS(16 0) -                                                          
          RECORDSIZE(350 350) -                                                 
          SHAREOPTIONS(2 3) -                                                   
          ERASE -                                                               
          INDEXED -                                                             
          ) -                                                                   
          DATA (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS.DATA) -                 
          ) -                                                                   
          INDEX (NAME(AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS.INDEX) -               
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
| `TRANSACT` | `AWS.M2.CARDDEMO.DALYTRAN.PS.INIT` | SHR | INPUT |  |  |
| `TRANVSAM` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
   REPRO INFILE(TRANSACT) OUTFILE(TRANVSAM)                                     
```

---
### Step 5: STEP20

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP20` |
| Type | UTIL |
| Program | `IDCAMS` |
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
### Step 6: STEP25

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
### Step 7: STEP30

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
### Step 8: OPCIFIL

| Attribute | Value |
|-----------|-------|
| Step Name | `OPCIFIL` |
| Type | PGM |
| Program | `SDSF` |
> ********************************************************************  
> Opem files in CICS region  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /F CICSAWSA,'CEMT SET FIL(TRANSACT ) OPE'                                      
 /F CICSAWSA,'CEMT SET FIL(CXACAIX ) OPE'                                       
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)
- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.DALYTRAN.PS.INIT`
- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`


---

*Generated 2026-03-16 19:39*