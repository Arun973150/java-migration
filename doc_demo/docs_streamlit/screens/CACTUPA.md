# Screen: CACTUPA

| Attribute | Value |
|-----------|-------|
| Map Name | `CACTUPA` |
| Mapset | `COACTUP` |
| Program | [COACTUPC](../programs/COACTUPC.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACCTSID` | 5 | 38 | 11 | (IC,UNPROT) |
| `ACSTTUS` | 5 | 70 | 1 | (UNPROT) |
| `OPNYEAR` | 6 | 17 | 4 | (FSET,UNPROT) |
| `OPNMON` | 6 | 24 | 2 | (UNPROT) |
| `OPNDAY` | 6 | 29 | 2 | (UNPROT) |
| `ACRDLIM` | 6 | 61 | 15 | (FSET,UNPROT) |
| `EXPYEAR` | 7 | 17 | 4 | (UNPROT) |
| `EXPMON` | 7 | 24 | 2 | (UNPROT) |
| `EXPDAY` | 7 | 29 | 2 | (UNPROT) |
| `ACSHLIM` | 7 | 61 | 15 | (FSET,UNPROT) |
| `RISYEAR` | 8 | 17 | 4 | (UNPROT) |
| `RISMON` | 8 | 24 | 2 | (UNPROT) |
| `RISDAY` | 8 | 29 | 2 | (UNPROT) |
| `ACURBAL` | 8 | 61 | 15 | (FSET,UNPROT) |
| `ACRCYCR` | 9 | 61 | 15 | (FSET,UNPROT) |
| `AADDGRP` | 10 | 23 | 10 | (UNPROT) |
| `ACRCYDB` | 10 | 61 | 15 | (FSET,UNPROT) |
| `ACSTNUM` | 12 | 23 | 9 | (UNPROT) |
| `ACTSSN1` | 12 | 55 | 3 | (UNPROT) |
| `ACTSSN2` | 12 | 61 | 2 | (UNPROT) |
| `ACTSSN3` | 12 | 66 | 4 | (UNPROT) |
| `DOBYEAR` | 13 | 23 | 4 | (UNPROT) |
| `DOBMON` | 13 | 30 | 2 | (UNPROT) |
| `DOBDAY` | 13 | 35 | 2 | (UNPROT) |
| `ACSTFCO` | 13 | 62 | 3 | (UNPROT) |
| `ACSFNAM` | 15 | 1 | 25 | (UNPROT) |
| `ACSMNAM` | 15 | 28 | 25 | (UNPROT) |
| `ACSLNAM` | 15 | 55 | 25 | (UNPROT) |
| `ACSADL1` | 16 | 10 | 50 | (UNPROT) |
| `ACSSTTE` | 16 | 73 | 2 | (UNPROT) |
| `ACSADL2` | 17 | 10 | 50 | (UNPROT) |
| `ACSZIPC` | 17 | 73 | 5 | (UNPROT) |
| `ACSCITY` | 18 | 10 | 50 | (UNPROT) |
| `ACSCTRY` | 18 | 73 | 3 | (UNPROT) |
| `ACSPH1A` | 19 | 10 | 3 | (UNPROT) |
| `ACSPH1B` | 19 | 14 | 3 | (UNPROT) |
| `ACSPH1C` | 19 | 18 | 4 | (UNPROT) |
| `ACSGOVT` | 19 | 58 | 20 | (UNPROT) |
| `ACSPH2A` | 20 | 10 | 3 | (UNPROT) |
| `ACSPH2B` | 20 | 14 | 3 | (UNPROT) |
| `ACSPH2C` | 20 | 18 | 4 | (UNPROT) |
| `ACSEFTC` | 20 | 41 | 10 | (UNPROT) |
| `ACSPFLG` | 20 | 78 | 1 | (UNPROT) |

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
| `FKEY05` | 24 | 23 | 7 | (ASKIP,DRK) |
| `FKEY12` | 24 | 31 | 10 | (ASKIP,DRK) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
|  | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Update Account | 4 | 33 |
| Account Number : | 5 | 19 |
|  | 5 | 50 |
| Active Y/N: | 5 | 57 |
|  | 5 | 72 |
| Opened : | 6 | 8 |
| - | 6 | 22 |
| - | 6 | 27 |
|  | 6 | 32 |
| Credit Limit        : | 6 | 39 |
|  | 6 | 77 |
| Expiry : | 7 | 8 |
| - | 7 | 22 |
| - | 7 | 27 |
|  | 7 | 32 |
| Cash credit Limit   : | 7 | 39 |
|  | 7 | 77 |
| Reissue: | 8 | 8 |
| - | 8 | 22 |
| - | 8 | 27 |
|  | 8 | 32 |
| Current Balance     : | 8 | 39 |
|  | 8 | 77 |
| Current Cycle Credit: | 9 | 39 |
|  | 9 | 77 |
| Account Group: | 10 | 8 |
|  | 10 | 34 |
| Current Cycle Debit : | 10 | 39 |
|  | 10 | 77 |
| Customer Details | 11 | 32 |
| Customer id  : | 12 | 8 |
|  | 12 | 33 |
| SSN: | 12 | 49 |
| - | 12 | 59 |
| - | 12 | 64 |
|  | 12 | 71 |
| Date of birth: | 13 | 8 |
| - | 13 | 28 |
| - | 13 | 33 |
|  | 13 | 38 |
| FICO Score: | 13 | 49 |
|  | 13 | 66 |
| First Name | 14 | 1 |
| Middle Name: | 14 | 28 |
| Last Name : | 14 | 55 |
|  | 15 | 27 |
|  | 15 | 54 |
| Address: | 16 | 1 |
|  | 16 | 61 |
| State | 16 | 63 |
|  | 16 | 76 |
|  | 17 | 61 |
| Zip | 17 | 63 |
|  | 17 | 79 |
| City | 18 | 1 |
|  | 18 | 61 |
| Country | 18 | 63 |
|  | 18 | 77 |
| Phone 1: | 19 | 1 |
|  | 19 | 23 |
| Government Issued Id Ref    : | 19 | 24 |
|  | 19 | 79 |
| Phone 2: | 20 | 1 |
|  | 20 | 23 |
| EFT Account Id: | 20 | 24 |
|  | 20 | 52 |
| Primary Card Holder Y/N: | 20 | 53 |
|  | 20 | 80 |
|  | 22 | 69 |

## Visual Mockup

```
Row  1: Tran:        Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Update Account  
Row  5: Account Number :      Active Y/N:      
Row  6: Opened :    -    -      Credit Limit        :      
Row  7: Expiry :    -    -      Cash credit Limit   :      
Row  8: Reissue:    -    -      Current Balance     :      
Row  9: Current Cycle Credit:      
Row 10: Account Group:      Current Cycle Debit :      
Row 11: Customer Details  
Row 12: Customer id  :      SSN:  999  -  99  -  9999    
Row 13: Date of birth:    -    -      FICO Score:      
Row 14: First Name  Middle Name:  Last Name :  
Row 15:           
Row 16: Address:      State      
Row 17:     Zip      
Row 18: City      Country      
Row 19: Phone 1:          Government Issued Id Ref    :      
Row 20: Phone 2:          EFT Account Id:      Primary Card Holder Y/N:      
Row 22:     
Row 23:   
Row 24: ENTER=Process F3=Exit  F5=Save  F12=Cancel  
```

---

*Generated 2026-03-16 19:39*