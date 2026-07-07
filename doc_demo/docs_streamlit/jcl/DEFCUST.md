# JCL Job: DEFCUST

| Attribute | Value |
|-----------|-------|
| File | `DEFCUST.jcl` |
| Description | Define Customer Data File |
| Job Class | A |
| Msg Class | 0 |
| Steps | 1 |


## Job Steps

### Step 1: STEP05

| Attribute | Value |
|-----------|-------|
| Step Name | `STEP05` |
| Type | UTIL |
| Program | `IDCAMS` |
> *******************************************************************  
> DELETE CUSTOMER VSAM FILE IF ONE ALREADY EXISTS  
> *******************************************************************

#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
| `SYSPRINT` | `` |  | SYSTEM |  |  |
| `SYSPRINT` | `` |  | SYSTEM |  |  |

#### Inline SYSIN

```
   DEFINE CLUSTER (NAME(AWS.CUSTDATA.CLUSTER) - 
          CYLINDERS(1 5) -                      
          KEYS(10 0) -                          
          RECORDSIZE(500 500) -                 
          SHAREOPTIONS(1 4) -                   
          ERASE -                               
          INDEXED -                             
          ) -                                        
          DATA (NAME(AWS.CUSTDATA.CLUSTER.DATA) -    
          ) -                                        
          INDEX (NAME(AWS.CUSTDATA.CLUSTER.INDEX) -  
          )                                             
```

---

## Summary

### COBOL Programs Executed

- [IDCAMS](../programs/IDCAMS.md)



---

*Generated 2026-03-16 19:39*