# JCL Job: CREASTMT

| Attribute | Value |
|-----------|-------|
| File | `CREASTMT.JCL` |
| Description | Create Statement |
| Job Class | A |
| Msg Class | H |
| Steps | 5 |


## Job Steps

### Step 1: DELDEF01

| Attribute | Value |
|-----------|-------|
| Step Name | `DELDEF01` |
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
> This JCL will create statement for each CARD present in the XREF  
> file  
> *****************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
  DELETE    AWS.M2.CARDDEMO.TRXFL.SEQ
  DELETE    AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS                     -
            CLUSTER
  SET       MAXCC = 0
  DEFINE    CLUSTER  (NAME(AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS)     -
                      KEYS(32 0)                                -
                      VOLUMES(TSU023)                           -
                      RECORDSIZE(350 350)                       -
                      SHAREOPTIONS(2 3)                         -
                      ERASE                                     -
                      INDEXED                                   -
                      CYL(1 5))                                 -
            DATA      (NAME(AWS.M2.CARDDEMO.TRXFL.DATA)         -
                      CISZ(4096))                               -
            INDEX     (NAME(AWS.M2.CARDDEMO.TRXFL.INDEX))
```

---
### Step 2: STEP010

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP010` |
| Type | UTIL |
| Program | `SORT` |
> ********************************************************************  
> CREATE COPY OF TRANSACT FILE WITH CARD NUMBER AND TRAN ID AS KEY  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SORTIN` | `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS` | SHR | INPUT |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `SORTOUT` | `AWS.M2.CARDDEMO.TRXFL.SEQ` | NEW | OUTPUT | FB | 350 |

#### Inline SYSIN

```
  SORT FIELDS=(263,16,CH,A,1,16,CH,A)
  OUTREC FIELDS=(1:263,16,17:1,262,279:279,50)
```

---
### Step 3: STEP020

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP020` |
| Type | UTIL |
| Program | `IDCAMS` || COND | `0,NE` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `INFILE` | `AWS.M2.CARDDEMO.TRXFL.SEQ` | SHR | INPUT |  |  |
| `OUTFILE` | `AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS` | SHR | INPUT |  |  |

#### Inline SYSIN

```
  REPRO INFILE(INFILE) OUTFILE(OUTFILE)
```

---
### Step 4: STEP030

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP030` |
| Type | UTIL |
| Program | `IEFBR14` || COND | `0,NE` |
> ********************************************************************  
> DELETE TRANSACTION REPORTS FROM PREVIOUS RUN  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `HTMLFILE` | `AWS.M2.CARDDEMO.STATEMNT.HTML` | MOD | OUTPUT | FB | 80 |
| `STMTFILE` | `AWS.M2.CARDDEMO.STATEMNT.PS` | MOD | OUTPUT | FB | 80 |


---
### Step 5: STEP040

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP040` |
| Type | PGM |
| Program | [CBSTM03A](../programs/CBSTM03A.md) || COND | `0,NE` |
> ********************************************************************  
> PRODUCING REPORT IN TEXT AND HTML - DEMONSTRATES CALLED SUBROUTINE  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |
| `TRNXFILE` | `AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS` | SHR | INPUT |  |  |
| `XREFFILE` | `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS` | SHR | INPUT |  |  |
| `ACCTFILE` | `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `CUSTFILE` | `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS` | SHR | INPUT |  |  |
| `STMTFILE` | `AWS.M2.CARDDEMO.STATEMNT.PS` | NEW | OUTPUT | FB | 80 |
| `HTMLFILE` | `AWS.M2.CARDDEMO.STATEMNT.HTML` | NEW | OUTPUT | FB | 100 |


---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)
- [SORT](../programs/SORT.md)
- [IEFBR14](../programs/IEFBR14.md)
- [CBSTM03A](../programs/CBSTM03A.md)

### Input Datasets

- `AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS`
- `AWS.M2.CARDDEMO.TRXFL.SEQ`
- `AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`
- `AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`
- `AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS`

### Output Datasets

- `AWS.M2.CARDDEMO.TRXFL.SEQ`
- `AWS.M2.CARDDEMO.STATEMNT.HTML`
- `AWS.M2.CARDDEMO.STATEMNT.PS`

---

*Generated 2026-03-16 19:39*