# JCL Job: OPENFIL

| Attribute | Value |
|-----------|-------|
| File | `OPENFIL.jcl` |
| Description | Open files in CICS |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: OPCIFIL

| Attribute | Value |
|-----------|-------|
| Step Name | `OPCIFIL` |
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
> Open files in CICS region  
> ********************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `ISFOUT` | `` |  | OUTPUT |  |  |
| `CMDOUT` | `` |  | OUTPUT |  |  |

#### Inline SYSIN

```
 /F CICSAWSA,'CEMT SET FIL(TRANSACT ) OPE'                                      
 /F CICSAWSA,'CEMT SET FIL(CCXREF ) OPE'                                        
 /F CICSAWSA,'CEMT SET FIL(ACCTDAT ) OPE'                                       
 /F CICSAWSA,'CEMT SET FIL(CXACAIX ) OPE'                                       
 /F CICSAWSA,'CEMT SET FIL(USRSEC ) OPE'                                       
```

---

## Summary

### COBOL Programs Executed

- [SDSF](../programs/SDSF.md)



---

*Generated 2026-03-16 19:39*