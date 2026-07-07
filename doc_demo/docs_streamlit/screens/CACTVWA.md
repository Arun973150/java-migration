# Screen: CACTVWA

| Attribute | Value |
|-----------|-------|
| Map Name | `CACTVWA` |
| Mapset | `COACTVW` |
| Program | [COACTVWC](../programs/COACTVWC.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `ACCTSID` | 5 | 38 | 11 | (FSET,IC,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,NORM) |
| `ACSTTUS` | 5 | 70 | 1 | (ASKIP) |
| `ADTOPEN` | 6 | 17 | 10 |  |
| `ACRDLIM` | 6 | 61 | 15 |  |
| `AEXPDT` | 7 | 17 | 10 |  |
| `ACSHLIM` | 7 | 61 | 15 |  |
| `AREISDT` | 8 | 17 | 10 |  |
| `ACURBAL` | 8 | 61 | 15 |  |
| `ACRCYCR` | 9 | 61 | 15 |  |
| `AADDGRP` | 10 | 23 | 10 |  |
| `ACRCYDB` | 10 | 61 | 15 |  |
| `ACSTNUM` | 12 | 23 | 9 |  |
| `ACSTSSN` | 12 | 54 | 12 |  |
| `ACSTDOB` | 13 | 23 | 10 |  |
| `ACSTFCO` | 13 | 61 | 3 |  |
| `ACSFNAM` | 15 | 1 | 25 |  |
| `ACSMNAM` | 15 | 28 | 25 |  |
| `ACSLNAM` | 15 | 55 | 25 |  |
| `ACSADL1` | 16 | 10 | 50 |  |
| `ACSSTTE` | 16 | 73 | 2 |  |
| `ACSADL2` | 17 | 10 | 50 |  |
| `ACSZIPC` | 17 | 73 | 5 |  |
| `ACSCITY` | 18 | 10 | 50 |  |
| `ACSCTRY` | 18 | 73 | 3 |  |
| `ACSPHN1` | 19 | 10 | 13 |  |
| `ACSGOVT` | 19 | 58 | 20 |  |
| `ACSPHN2` | 20 | 10 | 13 |  |
| `ACSEFTC` | 20 | 41 | 10 |  |
| `ACSPFLG` | 20 | 78 | 1 |  |
| `INFOMSG` | 22 | 23 | 45 | (PROT) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
|  | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| View Account | 4 | 33 |
| Account Number : | 5 | 19 |
|  | 5 | 50 |
| Active Y/N: | 5 | 57 |
|  | 5 | 72 |
| Opened: | 6 | 8 |
|  | 6 | 28 |
| Credit Limit        : | 6 | 39 |
|  | 6 | 77 |
| Expiry: | 7 | 8 |
|  | 7 | 28 |
| Cash credit Limit   : | 7 | 39 |
|  | 7 | 77 |
| Reissue: | 8 | 8 |
|  | 8 | 28 |
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
|  | 12 | 67 |
| Date of birth: | 13 | 8 |
|  | 13 | 34 |
| FICO Score: | 13 | 49 |
|  | 13 | 65 |
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
| Government Issued Id Ref    : | 19 | 24 |
|  | 19 | 79 |
| Phone 2: | 20 | 1 |
| EFT Account Id: | 20 | 24 |
|  | 20 | 52 |
| Primary Card Holder Y/N: | 20 | 53 |
|  | 20 | 80 |
|  | 22 | 69 |
| F3=Exit | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:        Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: View Account  
Row  5: Account Number :      Active Y/N:      
Row  6: Opened:      Credit Limit        :      
Row  7: Expiry:      Cash credit Limit   :      
Row  8: Reissue:      Current Balance     :      
Row  9: Current Cycle Credit:      
Row 10: Account Group:      Current Cycle Debit :      
Row 11: Customer Details  
Row 12: Customer id  :      SSN:      
Row 13: Date of birth:      FICO Score:      
Row 14: First Name  Middle Name:  Last Name :  
Row 15:           
Row 16: Address:      State      
Row 17:     Zip      
Row 18: City      Country      
Row 19: Phone 1:    Government Issued Id Ref    :      
Row 20: Phone 2:    EFT Account Id:      Primary Card Holder Y/N:      
Row 22:     
Row 23:   
Row 24: F3=Exit  
```

---

*Generated 2026-03-16 19:39*