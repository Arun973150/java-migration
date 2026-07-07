# Screen: COUSR1A

| Attribute | Value |
|-----------|-------|
| Map Name | `COUSR1A` |
| Mapset | `COUSR01` |
| Program | [COUSR01C](../programs/COUSR01C.md) |
## Screen Layout

The following fields are defined in this BMS map:

### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
| `FNAME` | 8 | 18 | 20 | (FSET,IC,NORM,UNPROT) |
| `LNAME` | 8 | 56 | 20 | (FSET,NORM,UNPROT) |
| `USERID` | 11 | 15 | 8 | (FSET,NORM,UNPROT) |
| `PASSWD` | 11 | 55 | 8 | (DRK,FSET,UNPROT) |
| `USRTYPE` | 14 | 17 | 1 | (FSET,NORM,UNPROT) |

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
| Add User | 4 | 35 |
| First Name: | 8 | 6 |
|  | 8 | 39 |
| Last Name: | 8 | 45 |
|  | 8 | 77 |
| User ID: | 11 | 6 |
| (8 Char) | 11 | 24 |
| Password: | 11 | 45 |
| (8 Char) | 11 | 64 |
| User Type: | 14 | 6 |
| (A=Admin, U=User) | 14 | 19 |
| ENTER=Add User  F3=Back  F4=Clear  F12=Exit | 24 | 1 |

## Visual Mockup

```
Row  1: Tran:      Date:  mm/dd/yy  
Row  2: Prog:      Time:  hh:mm:ss  
Row  4: Add User  
Row  8: First Name:      Last Name:      
Row 11: User ID:    (8 Char)  Password:    (8 Char)  
Row 14: User Type:    (A=Admin, U=User)  
Row 23:   
Row 24: ENTER=Add User  F3=Back  F4=Clear  F12=Exit  
```

---

*Generated 2026-03-16 19:39*