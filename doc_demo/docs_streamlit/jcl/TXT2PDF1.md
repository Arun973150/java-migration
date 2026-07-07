# JCL Job: TXT2PDF1

| Attribute | Value |
|-----------|-------|
| File | `TXT2PDF1.JCL` |
| Description |  |
| Job Class | X |
| Msg Class | X |
| Steps | 1 |


## Job Steps

### Step 1: TXT2PDF

| Attribute | Value |
|-----------|-------|
| Step Name | `TXT2PDF` |
| Type | PGM |
| Program | `IKJEFT1B` || COND | `0,NE` |
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
> *******************************************************************  
> ********************************************************`***********  
> CONVERT TEXT FILE TO A PDF FILE  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.LBD.TXT2PDF.LOAD` | SHR | SYSTEM |  |  |
| `SYSEXEC` | `AWS.M2.LBD.TXT2PDF.EXEC` | SHR | INPUT |  |  |
| `INDD` | `AWS.M2.CARDDEMO.STATEMNT.PS` | SHR | INPUT |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSTSPRT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
 %TXT2PDF BROWSE Y IN DD:INDD +
 OUT 'AWS.M2.CARDDEMO.STATEMNT.PS.PDF'
```

---

## Summary

### COBOL Programs Executed

- [IKJEFT1B](../programs/IKJEFT1B.md)

### Input Datasets

- `AWS.M2.LBD.TXT2PDF.EXEC`
- `AWS.M2.CARDDEMO.STATEMNT.PS`


---

*Generated 2026-03-16 19:39*