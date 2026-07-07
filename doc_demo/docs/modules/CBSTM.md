# Module: Custfile

> **Module ID:** `CBSTM`  
> **Programs:** 2

---

## Business Purpose

Custfile

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [CBSTM03A](../programs/CBSTM03A.md) | BATCH | 925 |  |
| [CBSTM03B](../programs/CBSTM03B.md) | BATCH | 231 |  |



## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
| `ACCT-FILE` | VSAM | RANDOM | CBSTM03B |
| `CUST-FILE` | VSAM | RANDOM | CBSTM03B |
| `HTML-FILE` | None | None | CBSTM03A |
| `STMT-FILE` | None | None | CBSTM03A |
| `TRNX-FILE` | VSAM | SEQUENTIAL | CBSTM03B |
| `XREF-FILE` | VSAM | SEQUENTIAL | CBSTM03B |

---

*Generated 2026-05-12 12:31*