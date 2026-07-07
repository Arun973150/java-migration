# Screen: CORPT0A

| Attribute | Value |
|-----------|-------|
| Map Name | `CORPT0A` |
| Mapset | `CORPT00` |
| Program | [CORPT00C](../programs/CORPT00C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `MONTHLY` | 7 | 10 | 1 | (FSET,IC,NORM,UNPROT) |
| `YEARLY` | 9 | 10 | 1 | (FSET,NORM,UNPROT) |
| `CUSTOM` | 11 | 10 | 1 | (FSET,NORM,UNPROT) |
| `SDTMM` | 13 | 29 | 2 | (FSET,NORM,NUM,UNPROT) |
| `SDTDD` | 13 | 34 | 2 | (FSET,NORM,NUM,UNPROT) |
| `SDTYYYY` | 13 | 39 | 4 | (FSET,NORM,NUM,UNPROT) |
| `EDTMM` | 14 | 29 | 2 | (FSET,NORM,NUM,UNPROT) |
| `EDTDD` | 14 | 34 | 2 | (FSET,NORM,NUM,UNPROT) |
| `EDTYYYY` | 14 | 39 | 4 | (FSET,NORM,NUM,UNPROT) |
| `CONFIRM` | 19 | 66 | 1 | (FSET,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,FSET,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,FSET,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Transaction Reports | 4 | 30 |
|  | 7 | 12 |
| Monthly (Current Month) | 7 | 15 |
|  | 9 | 12 |
| Yearly (Current Year) | 9 | 15 |
|  | 11 | 12 |
| Custom (Date Range) | 11 | 15 |
| Start Date : | 13 | 15 |
| / | 13 | 32 |
| / | 13 | 37 |
|  | 13 | 44 |
| (MM/DD/YYYY) | 13 | 46 |
| End Date : | 14 | 15 |
| / | 14 | 32 |
| / | 14 | 37 |
|  | 14 | 44 |
| (MM/DD/YYYY) | 14 | 46 |
| The Report will be submitted for printing. Plea se confirm: | 19 | 6 |
|  | 19 | 68 |
| (Y/N) | 19 | 69 |
| ENTER=Continue  F3=Back | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Transaction Reports  
Row  7:     Monthly (Current Month)  
Row  9:     Yearly (Current Year)  
Row 11:     Custom (Date Range)  
Row 13: Start Date :    /    /      (MM/DD/YYYY)  
Row 14: End Date :    /    /      (MM/DD/YYYY)  
Row 19: The Report will be submitted for printing. Plea se confirm:      (Y/N)  
Row 23:   
Row 24: ENTER=Continue  F3=Back  
```

---

*Generated 2026-03-16 19:39*