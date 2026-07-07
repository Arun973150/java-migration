# Screen: CCRDSLA

| Attribute | Value |
|-----------|-------|
| Map Name | `CCRDSLA` |
| Mapset | `COCRDSL` |
| Program | [COCRDSLC](../programs/COCRDSLC.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACCTSID` | 7 | 45 | 11 | (FSET,IC,NORM,UNPROT) |
| `CARDSID` | 8 | 45 | 16 | (FSET,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,NORM) |
| `CRDNAME` | 11 | 25 | 50 |  |
| `CRDSTCD` | 13 | 25 | 1 | (ASKIP) |
| `EXPMON` | 15 | 25 | 2 | (ASKIP) |
| `EXPYEAR` | 15 | 30 | 4 | (ASKIP) |
| `INFOMSG` | 20 | 25 | 40 | (PROT) |
| `ERRMSG` | 23 | 1 | 80 | (ASKIP,BRT,FSET) |
| `FKEYS` | 24 | 1 | 75 | (ASKIP,NORM) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| View Credit Card Detail | 4 | 30 |
| Account Number    : | 7 | 23 |
|  | 7 | 57 |
| Card Number       : | 8 | 23 |
|  | 8 | 62 |
| Name on card      : | 11 | 4 |
|  | 11 | 76 |
| Card Active Y/N   : | 13 | 4 |
|  | 13 | 27 |
| Expiry Date       : | 15 | 4 |
| / | 15 | 28 |
|  | 15 | 35 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: View Credit Card Detail  
Row  7: Account Number    :      
Row  8: Card Number       :      
Row 11: Name on card      :      
Row 13: Card Active Y/N   :      
Row 15: Expiry Date       :    /      
Row 20:   
Row 23:   
Row 24: ENTER=Search Cards  F3=Exit  
```

---

*Generated 2026-03-16 19:39*