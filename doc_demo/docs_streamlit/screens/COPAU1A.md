# Screen: COPAU1A

| Attribute | Value |
|-----------|-------|
| Map Name | `COPAU1A` |
| Mapset | `COPAU01` |

## Screen Layout

The following fields are defined in this BMS map:


### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,NORM) |
| `CARDNUM` | 7 | 11 | 16 | (ASKIP,NORM) |
| `AUTHDT` | 7 | 43 | 10 | (ASKIP,NORM) |
| `AUTHTM` | 7 | 68 | 10 | (ASKIP,NORM) |
| `AUTHRSP` | 9 | 14 | 1 | (ASKIP,NORM) |
| `AUTHRSN` | 9 | 32 | 20 | (ASKIP,NORM) |
| `AUTHCD` | 9 | 68 | 6 | (ASKIP,NORM) |
| `AUTHAMT` | 11 | 11 | 12 | (ASKIP,NORM) |
| `POSEMD` | 11 | 46 | 4 | (ASKIP,NORM) |
| `AUTHSRC` | 11 | 68 | 10 | (ASKIP,NORM) |
| `MCCCD` | 13 | 13 | 4 | (ASKIP,NORM) |
| `CRDEXP` | 13 | 42 | 5 | (ASKIP,NORM) |
| `AUTHTYP` | 13 | 64 | 14 | (ASKIP,NORM) |
| `TRNID` | 15 | 12 | 15 | (ASKIP,NORM) |
| `AUTHMTC` | 15 | 46 | 1 | (ASKIP,NORM) |
| `AUTHFRD` | 15 | 67 | 10 | (ASKIP,NORM) |
| `MERNAME` | 19 | 9 | 25 | (ASKIP,NORM) |
| `MERID` | 19 | 55 | 15 | (ASKIP,NORM) |
| `MERCITY` | 21 | 9 | 25 | (ASKIP,NORM) |
| `MERST` | 21 | 49 | 2 | (ASKIP,NORM) |
| `MERZIP` | 21 | 61 | 10 | (ASKIP,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| View Authorization Details | 4 | 27 |
| Card #: | 7 | 2 |
| Auth Date: | 7 | 31 |
| Auth Time: | 7 | 56 |
| Auth Resp: | 9 | 2 |
| Resp Reason: | 9 | 18 |
| Auth Code: | 9 | 56 |
| Amount: | 11 | 2 |
| POS Entry Mode: | 11 | 29 |
| Source   : | 11 | 56 |
| MCC Code: | 13 | 2 |
| Card Exp. Date: | 13 | 25 |
| Auth Type: | 13 | 52 |
| Tran Id: | 15 | 2 |
| Match Status: | 15 | 31 |
| Fraud Status: | 15 | 52 |
| Merchant Details ----------------------------- | 17 | 2 |
| Name: | 19 | 2 |
| Merchant ID: | 19 | 41 |
| City: | 21 | 2 |
| State: | 21 | 41 |
| Zip: | 21 | 55 |
| F3=Back  F5=Mark/Remove Fraud  F8=Next Auth | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: View Authorization Details  
Row  7: Card #:    Auth Date:    Auth Time:    
Row  9: Auth Resp:    Resp Reason:    Auth Code:    
Row 11: Amount:    POS Entry Mode:    Source   :    
Row 13: MCC Code:    Card Exp. Date:    Auth Type:    
Row 15: Tran Id:    Match Status:    Fraud Status:    
Row 17: Merchant Details -----------------------------  
Row 19: Name:    Merchant ID:    
Row 21: City:    State:    Zip:    
Row 23:   
Row 24: F3=Back  F5=Mark/Remove Fraud  F8=Next Auth  
```

---

*Generated 2026-03-16 19:39*