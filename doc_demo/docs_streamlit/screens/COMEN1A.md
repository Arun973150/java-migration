# Screen: COMEN1A

| Attribute | Value |
|-----------|-------|
| Map Name | `COMEN1A` |
| Mapset | `COMEN01` |
| Program | [COMEN01C](../programs/COMEN01C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `OPTION` | 20 | 41 | 2 | (FSET,IC,NORM,NUM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,FSET,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,FSET,NORM) |
| `OPTN001` | 6 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN002` | 7 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN003` | 8 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN004` | 9 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN005` | 10 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN006` | 11 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN007` | 12 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN008` | 13 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN009` | 14 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN010` | 15 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN011` | 16 | 20 | 40 | (ASKIP,FSET,NORM) |
| `OPTN012` | 17 | 20 | 40 | (ASKIP,FSET,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Main Menu | 4 | 35 |
| Please select an option : | 20 | 15 |
|  | 20 | 44 |
| ENTER=Continue  F3=Exit | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Main Menu  
Row  6:   
Row  7:   
Row  8:   
Row  9:   
Row 10:   
Row 11:   
Row 12:   
Row 13:   
Row 14:   
Row 15:   
Row 16:   
Row 17:   
Row 20: Please select an option :      
Row 23:   
Row 24: ENTER=Continue  F3=Exit  
```

---

*Generated 2026-03-16 19:39*