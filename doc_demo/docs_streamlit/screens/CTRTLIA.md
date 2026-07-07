# Screen: CTRTLIA

| Attribute | Value |
|-----------|-------|
| Map Name | `CTRTLIA` |
| Mapset | `COTRTLI` |
| Program | [COTRTLIC](../programs/COTRTLIC.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRTYPE` | 6 | 44 | 2 | (FSET,IC,NORM,UNPROT) |
| `TRDESC` | 8 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD1` | 12 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD2` | 13 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD3` | 14 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD4` | 15 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD5` | 16 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD6` | 17 | 25 | 50 | (FSET,NORM,UNPROT) |
| `TRTYPD7` | 18 | 25 | 50 | (FSET,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,NORM) |
| `PAGENO` | 4 | 76 | 3 |  |
| `TRTSEL1` | 12 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP1` | 12 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL2` | 13 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP2` | 13 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL3` | 14 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP3` | 14 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL4` | 15 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP4` | 15 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL5` | 16 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP5` | 16 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL6` | 17 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP6` | 17 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSEL7` | 18 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYP7` | 18 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTSELA` | 19 | 6 | 1 | (FSET,NORM,PROT) |
| `TRTTYPA` | 19 | 17 | 2 | (FSET,NORM,PROT) |
| `TRTDSCA` | 19 | 25 | 50 | (FSET,NORM,PROT) |
| `INFOMSG` | 21 | 19 | 45 | (PROT) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |
| `BUTNF02` | 24 | 1 | 7 | (ASKIP,NORM) |
| `BUTNF03` | 24 | 10 | 7 | (ASKIP,NORM) |
| `BUTNF07` | 24 | 19 | 10 | (ASKIP,NORM) |
| `BUTNF08` | 24 | 32 | 10 | (ASKIP,NORM) |
| `BUTNF10` | 24 | 44 | 8 | (ASKIP,NORM) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Maintain Transaction Type | 4 | 28 |
| Page | 4 | 70 |
| Type Filter: | 6 | 30 |
|  | 6 | 47 |
| Description Filter: | 8 | 4 |
|  | 8 | 76 |
| Select | 10 | 4 |
| Type | 10 | 16 |
| Description | 10 | 42 |
| ------ | 11 | 4 |
| ----- | 11 | 15 |
| --- | 11 | 25 |
|  | 12 | 8 |
|  | 12 | 20 |
|  | 12 | 76 |
|  | 13 | 8 |
|  | 13 | 20 |
|  | 13 | 76 |
|  | 14 | 8 |
|  | 14 | 20 |
|  | 14 | 76 |
|  | 15 | 8 |
|  | 15 | 20 |
|  | 15 | 76 |
|  | 16 | 8 |
|  | 16 | 20 |
|  | 16 | 76 |
|  | 17 | 8 |
|  | 17 | 20 |
|  | 17 | 76 |
|  | 18 | 8 |
|  | 18 | 20 |
|  | 18 | 76 |
|  | 19 | 8 |
|  | 19 | 20 |
|  | 19 | 76 |
|  | 21 | 65 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Maintain Transaction Type  Page    
Row  6: Type Filter:      
Row  8: Description Filter:      
Row 10: Select  Type  Description  
Row 11: ------  -----  ---  
Row 12:             
Row 13:             
Row 14:             
Row 15:             
Row 16:             
Row 17:             
Row 18:             
Row 19:             
Row 21:     
Row 23:   
Row 24: F2=Add  F3=Exit  F7=Page Up  F8=Page Dn  F10=Save  
```

---

*Generated 2026-03-16 19:39*