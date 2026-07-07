# JCL Job: LISTFILS

| Attribute | Value |
|-----------|-------|
| File | `LISTCAT.jcl` |
| Description | CARDDEMO |
| Job Class | A |
| Msg Class | 0 |
| Steps | 2 |


## Job Steps

### Step 1: STEP01

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP01` |
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
> ******************************************************************  
> List catalog for all the files in CARDDEMO application  
> ******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `DD1` | `AWS.M2.CARDDEMO.LISTCAT` | MOD | OUTPUT | FBA | 133 |


---
### Step 2: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` || COND | `0,NE` |

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `AWS.M2.CARDDEMO.LISTCAT` | NEW | SYSTEM | FBA | 133 |

#### Inline SYSIN

```
   LISTCAT LEVEL(AWS.M2.CARDDEMO)  -
           ALL
```

---

## Summary

### COBOL Programs Executed

- [IEFBR14](../programs/IEFBR14.md)
- [IDCAMS](../programs/IDCAMS.md)


### Output Datasets

- `AWS.M2.CARDDEMO.LISTCAT`

---

*Generated 2026-03-16 19:39*