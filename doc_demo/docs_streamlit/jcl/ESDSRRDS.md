# JCL Job: ESDSRRDS

| Attribute | Value |
|-----------|-------|
| File | `ESDSRRDS.jcl` |
| Description | DEF ESDS RRDS   |
| Job Class | A |
| Msg Class | H |
| Steps | 6 |


## Job Steps

### Step 1: PREDEL

| Attribute | Value |
|-----------|-------|
| Step Name | `PREDEL` |
| Type | UTIL |
| Program | `IEFBR14` |
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
> PRE DELETE STEP  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `DD01` | `AWS.M2.CARDDEMO.ESDSRRDS.PS` | MOD | OUTPUT |  |  |


---
### Step 2: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
| Type | UTIL |
| Program | `IEBGENER` |
> -------------------------------------------------------------------*  
> CREATE USER SECURITY FILE (PS) FROM IN-STREAM DATA  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSUT2` | `AWS.M2.CARDDEMO.ESDSRRDS.PS` | NEW | OUTPUT | FB | 80 |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSIN` | `` |  | INPUT |  |  |

#### Inline SYSIN

```
ADMIN001MARGARET            GOLD                PASSWORDA
ADMIN002RUSSELL             RUSSELL             PASSWORDA
ADMIN003RAYMOND             WHITMORE            PASSWORDA
ADMIN004EMMANUEL            CASGRAIN            PASSWORDA
ADMIN005GRANVILLE           LACHAPELLE          PASSWORDA
USER0001LAWRENCE            THOMAS              PASSWORDU
USER0002AJITH               KUMAR               PASSWORDU
USER0003LAURITZ             ALME                PASSWORDU
USER0004AVERARDO            MAZZI               PASSWORDU
USER0005LEE                 TING                PASSWORDU
```

---
### Step 3: STEP02

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP02` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> DEFINE VSAM FILE FOR USER SECURITY (ESDS)  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
 DELETE                  AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS
 SET       MAXCC = 0
 DEFINE    CLUSTER (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS)    -
                    RECORDSIZE(80,80)                         -
                    REUSE                                     -
                    NONINDEXED                                -
                    TRACKS(45,15)                             -
                    FREESPACE(10,15)                          -
                    CISZ(8192))                               -
           DATA    (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS.DAT))
```

---
### Step 4: STEP03

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP03` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> COPY USER SECURITY DATA FROM PS TO VSAM FILE(ESDS)  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `IN` | `AWS.M2.CARDDEMO.ESDSRRDS.PS` | SHR | INPUT |  |  |
| `OUT` | `AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  REPRO INFILE(IN) OUTFILE(OUT)
```

---
### Step 5: STEP04

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP04` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> DEFINE VSAM FILE FOR USER SECURITY (RRDS)  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
 DELETE                  AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS
 SET       MAXCC = 0
 DEFINE    CLUSTER (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS)    -
                    RECORDSIZE(80,80)                         -
                    REUSE                                     -
                    NUMBERED                                  -
                    TRACKS(45,15)                             -
                    FREESPACE(10,15)                          -
                    CISZ(8192))                               -
           DATA    (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS.DAT))
```

---
### Step 6: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> COPY USER SECURITY DATA FROM PS TO VSAM FILE(ESDS)  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `IN` | `AWS.M2.CARDDEMO.ESDSRRDS.PS` | SHR | INPUT |  |  |
| `OUT` | `AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS` | SHR | INPUT |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  REPRO INFILE(IN) OUTFILE(OUT)
```

---

## Summary

### COBOL Programs Executed

- [IEFBR14](../programs/IEFBR14.md)
- [IEBGENER](../programs/IEBGENER.md)
- [IDCAMS](../programs/IDCAMS.md)

### Input Datasets

- `AWS.M2.CARDDEMO.ESDSRRDS.PS`
- `AWS.M2.CARDDEMO.USRSEC.VSAM.ESDS`
- `AWS.M2.CARDDEMO.USRSEC.VSAM.RRDS`

### Output Datasets

- `AWS.M2.CARDDEMO.ESDSRRDS.PS`

---

*Generated 2026-03-16 19:39*