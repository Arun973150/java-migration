# Screen: CCRDLIA

| Attribute | Value |
|-----------|-------|
| Map Name | `CCRDLIA` |
| Mapset | `COCRDLI` |
| Program | [COCRDLIC](../programs/COCRDLIC.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACCTSID` | 6 | 44 | 11 | (FSET,IC,NORM,UNPROT) |
| `CARDSID` | 7 | 44 | 16 | (FSET,NORM,UNPROT) |

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
| `CRDSEL1` | 11 | 12 | 1 | (FSET,NORM,PROT) |
| `ACCTNO1` | 11 | 22 | 11 | (NORM,PROT) |
| `CRDNUM1` | 11 | 43 | 16 | (NORM,PROT) |
| `CRDSTS1` | 11 | 67 | 1 | (NORM,PROT) |
| `CRDSEL2` | 12 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP2` | 12 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO2` | 12 | 22 | 11 | (NORM,PROT) |
| `CRDNUM2` | 12 | 43 | 16 | (NORM,PROT) |
| `CRDSTS2` | 12 | 67 | 1 | (NORM,PROT) |
| `CRDSEL3` | 13 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP3` | 13 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO3` | 13 | 22 | 11 | (NORM,PROT) |
| `CRDNUM3` | 13 | 43 | 16 | (NORM,PROT) |
| `CRDSTS3` | 13 | 67 | 1 | (NORM,PROT) |
| `CRDSEL4` | 14 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP4` | 14 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO4` | 14 | 22 | 11 | (NORM,PROT) |
| `CRDNUM4` | 14 | 43 | 16 | (NORM,PROT) |
| `CRDSTS4` | 14 | 67 | 1 | (NORM,PROT) |
| `CRDSEL5` | 15 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP5` | 15 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO5` | 15 | 22 | 11 | (NORM,PROT) |
| `CRDNUM5` | 15 | 43 | 16 | (NORM,PROT) |
| `CRDSTS5` | 15 | 67 | 1 | (NORM,PROT) |
| `CRDSEL6` | 16 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP6` | 16 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO6` | 16 | 22 | 11 | (NORM,PROT) |
| `CRDNUM6` | 16 | 43 | 16 | (NORM,PROT) |
| `CRDSTS6` | 16 | 67 | 1 | (NORM,PROT) |
| `CRDSEL7` | 17 | 12 | 1 | (FSET,NORM,PROT) |
| `CRDSTP7` | 17 | 14 | 1 | (ASKIP,DRK,FSET) |
| `ACCTNO7` | 17 | 22 | 11 | (NORM,PROT) |
| `CRDNUM7` | 17 | 43 | 16 | (NORM,PROT) |
| `CRDSTS7` | 17 | 67 | 1 | (NORM,PROT) |
| `INFOMSG` | 20 | 19 | 45 | (PROT) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| List Credit Cards | 4 | 31 |
| Page | 4 | 70 |
| Account Number    : | 6 | 22 |
|  | 6 | 56 |
| Credit Card Number: | 7 | 22 |
|  | 7 | 61 |
| Select | 9 | 10 |
| Account Number | 9 | 21 |
| Card Number | 9 | 45 |
| Active | 9 | 66 |
| ------ | 10 | 10 |
| --------------- | 10 | 20 |
| --------------- | 10 | 43 |
| -------- | 10 | 65 |
|  | 11 | 14 |
|  | 12 | 14 |
|  | 13 | 14 |
|  | 14 | 14 |
|  | 15 | 14 |
|  | 16 | 14 |
|  | 17 | 14 |
|  | 20 | 65 |
| F3=Exit F7=Backward  F8=Forward | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: List Credit Cards  Page    
Row  6: Account Number    :      
Row  7: Credit Card Number:      
Row  9: Select  Account Number  Card Number  Active  
Row 10: ------  ---------------  ---------------  --------  
Row 11:           
Row 12:             
Row 13:             
Row 14:             
Row 15:             
Row 16:             
Row 17:             
Row 20:     
Row 23:   
Row 24: F3=Exit F7=Backward  F8=Forward  
```

---

*Generated 2026-03-16 19:39*