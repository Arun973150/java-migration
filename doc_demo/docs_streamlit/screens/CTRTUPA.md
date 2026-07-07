# Screen: CTRTUPA

| Attribute | Value |
|-----------|-------|
| Map Name | `CTRTUPA` |
| Mapset | `COTRTUP` |

## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRTYPCD` | 12 | 26 | 2 | (IC,UNPROT) |
| `TRTYDSC` | 14 | 26 | 50 | (UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,NORM) |
| `INFOMSG` | 22 | 23 | 45 | (ASKIP) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |
| `FKEYS` | 24 | 1 | 21 | (ASKIP,NORM) |
| `FKEY04` | 24 | 23 | 9 | (ASKIP,DRK) |
| `FKEY05` | 24 | 33 | 8 | (ASKIP,DRK) |
| `FKEY06` | 24 | 43 | 6 | (ASKIP,DRK) |
| `FKEY12` | 24 | 69 | 10 | (ASKIP,DRK) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Maintain Transaction Type | 7 | 28 |
| Transaction Type  : | 12 | 4 |
|  | 12 | 29 |
| Description       : | 14 | 4 |
|  | 14 | 77 |
|  | 22 | 69 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  7: Maintain Transaction Type  
Row 12: Transaction Type  :      
Row 14: Description       :      
Row 22:     
Row 23:   
Row 24: ENTER=Process F3=Exit  F4=Delete  F5=Save  F6=Add  F12=Cancel  
```

---

*Generated 2026-03-16 19:39*