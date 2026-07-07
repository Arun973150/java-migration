# JCL Job: RACFCMDS

| Attribute | Value |
|-----------|-------|
| File | `RACFCMDS.jcl` |
| Description |  |
| Job Class | A |
| Msg Class | Y |
| Steps | 1 |


## Job Steps

### Step 1: TSOBAT

| Attribute | Value |
|-----------|-------|
| Step Name | `TSOBAT` |
| Type | UTIL |
| Program | `IKJEFT01` |
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

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSTSPRT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
 RALT GCICSTRN CARD ADDMEM(CT02)                                                
 CONNECT AWSCODR GROUP(M2APPDEV)                                                
```

---

## Summary

### COBOL Programs Executed

- [IKJEFT01](../programs/IKJEFT01.md)



---

*Generated 2026-03-16 19:39*