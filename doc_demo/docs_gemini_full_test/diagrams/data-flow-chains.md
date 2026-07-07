# End-to-End Data Flow Chains

> Auto-generated 2026-05-12 12:20

Each chain traces how data flows: a JCL job triggers a program, which writes a file/dataset, which is then read by another program, and so on. Use this to decide migration units that must move together.

**Chains discovered:** 84

## Chain 1 — JCL-rooted

`JCL ACCTFILE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 2 — JCL-rooted

`JCL CARDFILE` → [SDSF](../programs/SDSF.md)

## Chain 3 — JCL-rooted

`JCL CARDFILE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 4 — JCL-rooted

`JCL CBADMCDJ` → [DFHCSDUP](../programs/DFHCSDUP.md)

## Chain 5 — JCL-rooted

`JCL CBEXPORT` → [IDCAMS](../programs/IDCAMS.md)

## Chain 6 — JCL-rooted

`JCL CBEXPORT` → [CBEXPORT](../programs/CBEXPORT.md)

## Chain 7 — JCL-rooted

`JCL CBIMPORT` → [CBIMPORT](../programs/CBIMPORT.md)

## Chain 8 — JCL-rooted

`JCL CBLDBMS`

## Chain 9 — JCL-rooted

`JCL CBLDBMS` → [SDSF](../programs/SDSF.md)

## Chain 10 — JCL-rooted

`JCL CBPAUP0J` → [DFSRRC00](../programs/DFSRRC00.md)

## Chain 11 — JCL-rooted

`JCL CICCMP`

## Chain 12 — JCL-rooted

`JCL CICCMP` → [SDSF](../programs/SDSF.md)

## Chain 13 — JCL-rooted

`JCL CIDBCMP`

## Chain 14 — JCL-rooted

`JCL CLOSEFIL` → [SDSF](../programs/SDSF.md)

## Chain 15 — JCL-rooted

`JCL CNJBATMP`

## Chain 16 — JCL-rooted

`JCL COMBTRAN` → [SORT](../programs/SORT.md)

## Chain 17 — JCL-rooted

`JCL COMBTRAN` → [IDCAMS](../programs/IDCAMS.md)

## Chain 18 — JCL-rooted

`JCL CREADB2` → [IKJEFT01](../programs/IKJEFT01.md)

## Chain 19 — JCL-rooted

`JCL CREADB2` → [IEFBR14](../programs/IEFBR14.md)

## Chain 20 — JCL-rooted

`JCL CREASTMT` → [IDCAMS](../programs/IDCAMS.md)

## Chain 21 — JCL-rooted

`JCL CREASTMT` → [SORT](../programs/SORT.md)

## Chain 22 — JCL-rooted

`JCL CREASTMT` → [IEFBR14](../programs/IEFBR14.md)

## Chain 23 — JCL-rooted

`JCL CREASTMT` → [CBSTM03A](../programs/CBSTM03A.md)

## Chain 24 — JCL-rooted

`JCL CUSTFILE` → [SDSF](../programs/SDSF.md)

## Chain 25 — JCL-rooted

`JCL CUSTFILE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 26 — JCL-rooted

`JCL DALYREJS` → [IDCAMS](../programs/IDCAMS.md)

## Chain 27 — JCL-rooted

`JCL DBPAUTP0` → [IEFBR14](../programs/IEFBR14.md)

## Chain 28 — JCL-rooted

`JCL DBPAUTP0` → [DFSRRC00](../programs/DFSRRC00.md)

## Chain 29 — JCL-rooted

`JCL DEFCUST` → [IDCAMS](../programs/IDCAMS.md)

## Chain 30 — JCL-rooted

`JCL DEFGDGB` → [IDCAMS](../programs/IDCAMS.md)

## Chain 31 — JCL-rooted

`JCL DEFGDGD` → [IDCAMS](../programs/IDCAMS.md)

## Chain 32 — JCL-rooted

`JCL DEFGDGD` → [IEBGENER](../programs/IEBGENER.md)

## Chain 33 — JCL-rooted

`JCL DISCGRP` → [IDCAMS](../programs/IDCAMS.md)

## Chain 34 — JCL-rooted

`JCL DUSRSECJ` → [IEFBR14](../programs/IEFBR14.md)

## Chain 35 — JCL-rooted

`JCL DUSRSECJ` → [IEBGENER](../programs/IEBGENER.md)

## Chain 36 — JCL-rooted

`JCL DUSRSECJ` → [IDCAMS](../programs/IDCAMS.md)

## Chain 37 — JCL-rooted

`JCL ESDSRRDS` → [IEFBR14](../programs/IEFBR14.md)

## Chain 38 — JCL-rooted

`JCL ESDSRRDS` → [IEBGENER](../programs/IEBGENER.md)

## Chain 39 — JCL-rooted

`JCL ESDSRRDS` → [IDCAMS](../programs/IDCAMS.md)

## Chain 40 — JCL-rooted

`JCL FTPJCLS` → [FTP](../programs/FTP.md)

## Chain 41 — JCL-rooted

`JCL IMSMQCMP` → [DFHECP1](../programs/DFHECP1.md)

## Chain 42 — JCL-rooted

`JCL IMSMQCMP` → [IGYCRCTL](../programs/IGYCRCTL.md)

## Chain 43 — JCL-rooted

`JCL IMSMQCMP` → [IEBGENER](../programs/IEBGENER.md)

## Chain 44 — JCL-rooted

`JCL INTCALC` → [CBACT04C](../programs/CBACT04C.md)

## Chain 45 — JCL-rooted

`JCL INTRDRJ1` → [IDCAMS](../programs/IDCAMS.md)

## Chain 46 — JCL-rooted

`JCL INTRDRJ1` → [IEBGENER](../programs/IEBGENER.md)

## Chain 47 — JCL-rooted

`JCL INTRDRJ2` → [IDCAMS](../programs/IDCAMS.md)

## Chain 48 — JCL-rooted

`JCL LISTFILS` → [IEFBR14](../programs/IEFBR14.md)

## Chain 49 — JCL-rooted

`JCL LISTFILS` → [IDCAMS](../programs/IDCAMS.md)

## Chain 50 — JCL-rooted

`JCL LOADPADB` → [DFSRRC00](../programs/DFSRRC00.md)

## Chain 51 — JCL-rooted

`JCL MNTTRDB2` → [IKJEFT01](../programs/IKJEFT01.md)

## Chain 52 — JCL-rooted

`JCL OPENFIL` → [SDSF](../programs/SDSF.md)

## Chain 53 — JCL-rooted

`JCL POSTTRAN` → [CBTRN02C](../programs/CBTRN02C.md)

## Chain 54 — JCL-rooted

`JCL PRTCATBL` → [IEFBR14](../programs/IEFBR14.md)

## Chain 55 — JCL-rooted

`JCL PRTCATBL`

## Chain 56 — JCL-rooted

`JCL PRTCATBL` → [SORT](../programs/SORT.md)

## Chain 57 — JCL-rooted

`JCL RACFCMDS` → [IKJEFT01](../programs/IKJEFT01.md)

## Chain 58 — JCL-rooted

`JCL READACCT` → [IEFBR14](../programs/IEFBR14.md)

## Chain 59 — JCL-rooted

`JCL READACCT` → [CBACT01C](../programs/CBACT01C.md)

## Chain 60 — JCL-rooted

`JCL READCARD` → [CBACT02C](../programs/CBACT02C.md)

## Chain 61 — JCL-rooted

`JCL READCUST` → [CBCUS01C](../programs/CBCUS01C.md)

## Chain 62 — JCL-rooted

`JCL READXREF` → [CBACT03C](../programs/CBACT03C.md)

## Chain 63 — JCL-rooted

`JCL REPRTEST`

## Chain 64 — JCL-rooted

`JCL REPTFILE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 65 — JCL-rooted

`JCL SORTTEST` → [SORT](../programs/SORT.md)

## Chain 66 — JCL-rooted

`JCL TCATBALF` → [IDCAMS](../programs/IDCAMS.md)

## Chain 67 — JCL-rooted

`JCL TRANBKP`

## Chain 68 — JCL-rooted

`JCL TRANBKP` → [IDCAMS](../programs/IDCAMS.md)

## Chain 69 — JCL-rooted

`JCL TRANCATG` → [IDCAMS](../programs/IDCAMS.md)

## Chain 70 — JCL-rooted

`JCL TRANEXTR` → [IEBGENER](../programs/IEBGENER.md)

## Chain 71 — JCL-rooted

`JCL TRANEXTR` → [IEFBR14](../programs/IEFBR14.md)

## Chain 72 — JCL-rooted

`JCL TRANEXTR` → [IKJEFT01](../programs/IKJEFT01.md)

## Chain 73 — JCL-rooted

`JCL TRANFILE` → [SDSF](../programs/SDSF.md)

## Chain 74 — JCL-rooted

`JCL TRANFILE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 75 — JCL-rooted

`JCL TRANIDX` → [IDCAMS](../programs/IDCAMS.md)

## Chain 76 — JCL-rooted

`JCL TRANREPT` → [SORT](../programs/SORT.md)

## Chain 77 — JCL-rooted

`JCL TRANREPT` → [CBTRN03C](../programs/CBTRN03C.md)

## Chain 78 — JCL-rooted

`JCL TRANTYPE` → [IDCAMS](../programs/IDCAMS.md)

## Chain 79 — JCL-rooted

`JCL TXT2PDF1` → [IKJEFT1B](../programs/IKJEFT1B.md)

## Chain 80 — JCL-rooted

`JCL UNLDGSAM` → [DFSRRC00](../programs/DFSRRC00.md)

## Chain 81 — JCL-rooted

`JCL UNLDPADB` → [IEFBR14](../programs/IEFBR14.md)

## Chain 82 — JCL-rooted

`JCL UNLDPADB` → [DFSRRC00](../programs/DFSRRC00.md)

## Chain 83 — JCL-rooted

`JCL WAITSTEP` → [COBSWAIT](../programs/COBSWAIT.md)

## Chain 84 — JCL-rooted

`JCL XREFFILE` → [IDCAMS](../programs/IDCAMS.md)
