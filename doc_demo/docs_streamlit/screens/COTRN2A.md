# Screen: COTRN2A

| Attribute | Value |
|-----------|-------|
| Map Name | `COTRN2A` |
| Mapset | `COTRN02` |
| Program | [COTRN02C](../programs/COTRN02C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACTIDIN` | 6 | 21 | 11 | (FSET,IC,NORM,UNPROT) |
| `CARDNIN` | 6 | 55 | 16 | (FSET,NORM,UNPROT) |
| `TTYPCD` | 10 | 15 | 2 | (FSET,NORM,UNPROT) |
| `TCATCD` | 10 | 36 | 4 | (FSET,NORM,UNPROT) |
| `TRNSRC` | 10 | 54 | 10 | (FSET,NORM,UNPROT) |
| `TDESC` | 12 | 19 | 60 | (FSET,NORM,UNPROT) |
| `TRNAMT` | 14 | 14 | 12 | (FSET,NORM,UNPROT) |
| `TORIGDT` | 14 | 42 | 10 | (FSET,NORM,UNPROT) |
| `TPROCDT` | 14 | 68 | 10 | (FSET,NORM,UNPROT) |
| `MID` | 16 | 19 | 9 | (FSET,NORM,UNPROT) |
| `MNAME` | 16 | 48 | 30 | (FSET,NORM,UNPROT) |
| `MCITY` | 18 | 21 | 25 | (FSET,NORM,UNPROT) |
| `MZIP` | 18 | 67 | 10 | (FSET,NORM,UNPROT) |
| `CONFIRM` | 21 | 63 | 1 | (FSET,NORM,UNPROT) |

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
| Add Transaction | 4 | 30 |
| Enter Acct #: | 6 | 6 |
|  | 6 | 33 |
| (or) | 6 | 37 |
| Card #: | 6 | 46 |
|  | 6 | 72 |
| ----------------------- | 8 | 6 |
| Type CD: | 10 | 6 |
|  | 10 | 18 |
| Category CD: | 10 | 23 |
|  | 10 | 41 |
| Source: | 10 | 46 |
|  | 10 | 65 |
| Description: | 12 | 6 |
|  | 12 | 80 |
| Amount: | 14 | 6 |
|  | 14 | 27 |
| Orig Date: | 14 | 31 |
|  | 14 | 53 |
| Proc Date: | 14 | 57 |
|  | 14 | 79 |
| (-99999999.99) | 15 | 13 |
| (YYYY-MM-DD) | 15 | 41 |
| (YYYY-MM-DD) | 15 | 67 |
| Merchant ID: | 16 | 6 |
|  | 16 | 29 |
| Merchant Name: | 16 | 33 |
|  | 16 | 79 |
| Merchant City: | 18 | 6 |
|  | 18 | 47 |
| Merchant Zip: | 18 | 53 |
|  | 18 | 78 |
| You are about to add this transaction. Please c onfirm : | 21 | 6 |
|  | 21 | 65 |
| (Y/N) | 21 | 66 |
| ENTER=Continue  F3=Back  F4=Clear  F5=Copy Last Tran. | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Add Transaction  
Row  6: Enter Acct #:      (or)  Card #:      
Row  8: -----------------------  
Row 10: Type CD:      Category CD:      Source:      
Row 12: Description:      
Row 14: Amount:      Orig Date:      Proc Date:      
Row 15: (-99999999.99)  (YYYY-MM-DD)  (YYYY-MM-DD)  
Row 16: Merchant ID:      Merchant Name:      
Row 18: Merchant City:      Merchant Zip:      
Row 21: You are about to add this transaction. Please c onfirm :      (Y/N)  
Row 23:   
Row 24: ENTER=Continue  F3=Back  F4=Clear  F5=Copy Last Tran.  
```

---

*Generated 2026-03-16 19:39*