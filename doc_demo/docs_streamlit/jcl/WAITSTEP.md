# JCL Job: WAITSTEP

| Attribute | Value |
|-----------|-------|
| File | `WAITSTEP.jcl` |
| Description | WAIT STEP |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: WAIT

| Attribute | Value |
|-----------|-------|
| Step Name | `WAIT` |
| Type | PGM |
| Program | [COBSWAIT](../programs/COBSWAIT.md) |
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
> WAIT FOR CENTISECONDS IN THE PARM EG: 00003600  = 36 SECONDS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `STEPLIB` | `AWS.M2.CARDDEMO.LOADLIB` | SHR | SYSTEM |  |  |
| `SYSOUT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
00003600      VALUE IN CENTISECONDS                                     00080000
/*                                                                      00080000
```

---

## Summary

### COBOL Programs Executed

- [COBSWAIT](../programs/COBSWAIT.md)



---

*Generated 2026-03-16 19:39*