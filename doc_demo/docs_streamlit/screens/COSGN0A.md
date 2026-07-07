# Screen: COSGN0A

| Attribute | Value |
|-----------|-------|
| Map Name | `COSGN0A` |
| Mapset | `COSGN00` |
| Program | [COSGN00C](../programs/COSGN00C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `USERID` | 19 | 43 | 8 | (FSET,IC,NORM,UNPROT) |
| `PASSWD` | 20 | 43 | 8 | (DRK,FSET,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 8 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 8 | 8 | (FSET,NORM,PROT) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 9 | (FSET,NORM,PROT) |
| `APPLID` | 3 | 8 | 8 | (FSET,NORM,PROT) |
| `SYSID` | 3 | 71 | 8 | (FSET,NORM,PROT) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran : | 1 | 1 |
| Date : | 1 | 64 |
| Prog : | 2 | 1 |
| Time : | 2 | 64 |
| AppID: | 3 | 1 |
| SysID: | 3 | 64 |
| This is a Credit Card Demo Application for Main frame Modernization | 5 | 6 |
| +========================================+ | 7 | 21 |
| |%%%%%%%  NATIONAL RESERVE NOTE  %%%%%%%%| | 8 | 21 |
| |%(1)  THE UNITED STATES OF KICSLAND (1)%| | 9 | 21 |
| |%$$              ___       ********  $$%| | 10 | 21 |
| |%$    {x}       (o o)                 $%| | 11 | 21 |
| |%$     ******  (  V  )      O N E     $%| | 12 | 21 |
| |%(1)          ---m-m---             (1)%| | 13 | 21 |
| |%%~~~~~~~~~~~ ONE DOLLAR ~~~~~~~~~~~~~%%| | 14 | 21 |
| +========================================+ | 15 | 21 |
| Type your User ID and Password, then press ENTE R: | 17 | 16 |
| User ID     : | 19 | 29 |
|  | 19 | 52 |
| (8 Char) | 19 | 52 |
| Password    : | 20 | 29 |
|  | 20 | 52 |
| (8 Char) | 20 | 52 |
|  | 20 | 61 |
|  | 20 | 63 |
| ENTER=Sign-on  F3=Exit | 24 | 1 |

## Visual Mockup

```
Row  1: Tran :      Date :  mm/dd/yy  
Row  2: Prog :      Time :  Ahh:mm:ss  
Row  3: AppID:    SysID:    
Row  5: This is a Credit Card Demo Application for Main frame Modernization  
Row  7: +========================================+  
Row  8: |%%%%%%%  NATIONAL RESERVE NOTE  %%%%%%%%|  
Row  9: |%(1)  THE UNITED STATES OF KICSLAND (1)%|  
Row 10: |%$$              ___       ********  $$%|  
Row 11: |%$    {x}       (o o)                 $%|  
Row 12: |%$     ******  (  V  )      O N E     $%|  
Row 13: |%(1)          ---m-m---             (1)%|  
Row 14: |%%~~~~~~~~~~~ ONE DOLLAR ~~~~~~~~~~~~~%%|  
Row 15: +========================================+  
Row 17: Type your User ID and Password, then press ENTE R:  
Row 19: User ID     :      (8 Char)  
Row 20: Password    :  ________    (8 Char)      
Row 23:   
Row 24: ENTER=Sign-on  F3=Exit  
```

---

*Generated 2026-03-16 19:39*