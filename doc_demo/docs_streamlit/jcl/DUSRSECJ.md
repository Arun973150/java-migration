# JCL Job: DUSRSECJ

| Attribute | Value |
|-----------|-------|
| File | `DUSRSECJ.jcl` |
| Description | DEF USRSEC FILE |
| Job Class | A |
| Msg Class | H |
| Steps | 4 |


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
| `DD01` | `AWS.M2.CARDDEMO.USRSEC.PS` | MOD | OUTPUT |  |  |


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
| `SYSUT2` | `AWS.M2.CARDDEMO.USRSEC.PS` | NEW | OUTPUT | FB | 80 |
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
> DEFINE VSAM FILE FOR USER SECURITY  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
 DELETE                  AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS
 SET       MAXCC = 0
 DEFINE    CLUSTER (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS)    -
                    KEYS(8,0)                                 -
                    RECORDSIZE(80,80)                         -
                    REUSE                                     -
                    INDEXED                                   -
                    TRACKS(45,15)                             -
                    FREESPACE(10,15)                          -
                    CISZ(8192))                               -
           DATA    (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS.DAT)) -
           INDEX   (NAME(AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS.IDX))
```

---
### Step 4: STEP03

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP03` |
| Type | UTIL |
| Program | `IDCAMS` |
> -------------------------------------------------------------------*  
> COPY USER SECURITY DATA FROM PS TO VSAM FILE  
> -------------------------------------------------------------------*

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `IN` | `AWS.M2.CARDDEMO.USRSEC.PS` | SHR | INPUT |  |  |
| `OUT` | `AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS` | SHR | INPUT |  |  |
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

- `AWS.M2.CARDDEMO.USRSEC.PS`
- `AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.USRSEC.PS`

---

*Generated 2026-03-16 19:39*