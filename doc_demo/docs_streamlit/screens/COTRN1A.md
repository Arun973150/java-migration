# Screen: COTRN1A

| Attribute | Value |
|-----------|-------|
| Map Name | `COTRN1A` |
| Mapset | `COTRN01` |
| Program | [COTRN01C](../programs/COTRN01C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNIDIN` | 6 | 21 | 16 | (FSET,IC,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,FSET,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,FSET,NORM) |
| `TRNID` | 10 | 22 | 16 | (ASKIP,NORM) |
| `CARDNUM` | 10 | 58 | 16 | (ASKIP,NORM) |
| `TTYPCD` | 12 | 15 | 2 | (ASKIP,NORM) |
| `TCATCD` | 12 | 36 | 4 | (ASKIP,NORM) |
| `TRNSRC` | 12 | 54 | 10 | (ASKIP,NORM) |
| `TDESC` | 14 | 19 | 60 | (ASKIP,NORM) |
| `TRNAMT` | 16 | 14 | 12 | (ASKIP,NORM) |
| `TORIGDT` | 16 | 42 | 10 | (ASKIP,NORM) |
| `TPROCDT` | 16 | 68 | 10 | (ASKIP,NORM) |
| `MID` | 18 | 19 | 9 | (ASKIP,NORM) |
| `MNAME` | 18 | 48 | 30 | (ASKIP,NORM) |
| `MCITY` | 20 | 21 | 25 | (ASKIP,NORM) |
| `MZIP` | 20 | 67 | 10 | (ASKIP,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| View Transaction | 4 | 30 |
| Enter Tran ID: | 6 | 6 |
|  | 6 | 38 |
| ----------------------- | 8 | 6 |
| Transaction ID: | 10 | 6 |
|  | 10 | 39 |
| Card Number: | 10 | 45 |
|  | 10 | 75 |
| Type CD: | 12 | 6 |
|  | 12 | 18 |
| Category CD: | 12 | 23 |
|  | 12 | 41 |
| Source: | 12 | 46 |
|  | 12 | 65 |
| Description: | 14 | 6 |
|  | 14 | 80 |
| Amount: | 16 | 6 |
|  | 16 | 27 |
| Orig Date: | 16 | 31 |
|  | 16 | 53 |
| Proc Date: | 16 | 57 |
|  | 16 | 79 |
| Merchant ID: | 18 | 6 |
|  | 18 | 29 |
| Merchant Name: | 18 | 33 |
|  | 18 | 79 |
| Merchant City: | 20 | 6 |
|  | 20 | 47 |
| Merchant Zip: | 20 | 53 |
|  | 20 | 78 |
| ENTER=Fetch  F3=Back  F4=Clear  F5=Browse Tran. | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: View Transaction  
Row  6: Enter Tran ID:      
Row  8: -----------------------  
Row 10: Transaction ID:      Card Number:      
Row 12: Type CD:      Category CD:      Source:      
Row 14: Description:      
Row 16: Amount:      Orig Date:      Proc Date:      
Row 18: Merchant ID:      Merchant Name:      
Row 20: Merchant City:      Merchant Zip:      
Row 23:   
Row 24: ENTER=Fetch  F3=Back  F4=Clear  F5=Browse Tran.  
```

---

*Generated 2026-03-16 19:39*