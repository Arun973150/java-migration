# Screen: COUSR3A

| Attribute | Value |
|-----------|-------|
| Map Name | `COUSR3A` |
| Mapset | `COUSR03` |
| Program | [COUSR03C](../programs/COUSR03C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `USRIDIN` | 6 | 21 | 8 | (FSET,IC,NORM,UNPROT) |

### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `TRNNAME` | 1 | 7 | 4 | (ASKIP,FSET,NORM) |
| `TITLE01` | 1 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURDATE` | 1 | 71 | 8 | (ASKIP,FSET,NORM) |
| `PGMNAME` | 2 | 7 | 8 | (ASKIP,FSET,NORM) |
| `TITLE02` | 2 | 21 | 40 | (ASKIP,FSET,NORM) |
| `CURTIME` | 2 | 71 | 8 | (ASKIP,FSET,NORM) |
| `FNAME` | 11 | 18 | 20 | (ASKIP,FSET,NORM) |
| `LNAME` | 13 | 18 | 20 | (ASKIP,FSET,NORM) |
| `USRTYPE` | 15 | 17 | 1 | (ASKIP,FSET,NORM) |
| `ERRMSG` | 23 | 1 | 78 | (ASKIP,BRT,FSET) |

### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
| Tran: | 1 | 1 |
| Date: | 1 | 65 |
| Prog: | 2 | 1 |
| Time: | 2 | 65 |
| Delete User | 4 | 35 |
| Enter User ID: | 6 | 6 |
|  | 6 | 30 |
| *********************************************** DFHMDF ATTRB=(ASKIP,NORM), COLOR=TURQUOISE, LENGTH=11, POS=(11,6), INITIAL= | 8 | 6 |
|  | 11 | 39 |
| Last Name: | 13 | 6 |
|  | 13 | 39 |
| User Type: | 15 | 6 |
| (A=Admin, U=User) | 15 | 19 |
| ENTER=Fetch  F3=Back  F4=Clear  F5=Delete | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Delete User  
Row  6: Enter User ID:      
Row  8: *********************************************** DFHMDF ATTRB=(ASKIP,NORM), COLOR=TURQUOISE, LENGTH=11, POS=(11,6), INITIAL=  
Row 11:     
Row 13: Last Name:      
Row 15: User Type:    (A=Admin, U=User)  
Row 23:   
Row 24: ENTER=Fetch  F3=Back  F4=Clear  F5=Delete  
```

---

*Generated 2026-03-16 19:39*