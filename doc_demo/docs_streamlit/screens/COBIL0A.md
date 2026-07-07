# Screen: COBIL0A

| Attribute | Value |
|-----------|-------|
| Map Name | `COBIL0A` |
| Mapset | `COBIL00` |
| Program | [COBIL00C](../programs/COBIL00C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACTIDIN` | 6 | 21 | 11 | (FSET,IC,NORM,UNPROT) |
| `CONFIRM` | 15 | 60 | 1 | (FSET,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,FSET,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,FSET,NORM) |
| `CURBAL` | 11 | 32 | 14 | (ASKIP,FSET,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Bill Payment | 4 | 35 |
| Enter Acct ID: | 6 | 6 |
|  | 6 | 33 |
| ----------------------- | 8 | 6 |
| Your current balance is: | 11 | 6 |
|  | 11 | 47 |
| Do you want to pay your balance now. Please con firm: | 15 | 6 |
|  | 15 | 62 |
| (Y/N) | 15 | 63 |
| ENTER=Continue  F3=Back  F4=Clear | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Bill Payment  
Row  6: Enter Acct ID:      
Row  8: -----------------------  
Row 11: Your current balance is:      
Row 15: Do you want to pay your balance now. Please con firm:      (Y/N)  
Row 23:   
Row 24: ENTER=Continue  F3=Back  F4=Clear  
```

---

*Generated 2026-03-16 19:39*