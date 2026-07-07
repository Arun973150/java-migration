# Module: Batch Transaction Processing

> **Module ID:** `TRANSACTION_BATCH`  
> **Programs:** 3

---

## Business Purpose

Batch Transaction Processing

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [CBTRN01C](../programs/CBTRN01C.md) | BATCH | 495 |  |
| [CBTRN02C](../programs/CBTRN02C.md) | BATCH | 732 |  |
| [CBTRN03C](../programs/CBTRN03C.md) | BATCH | 650 |  |



## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
| `ACCOUNT-FILE` | VSAM | RANDOM | CBTRN01C |
| `ACCOUNT-FILE` | VSAM | RANDOM | CBTRN02C |
| `CARD-FILE` | VSAM | RANDOM | CBTRN01C |
| `CUSTOMER-FILE` | VSAM | RANDOM | CBTRN01C |
| `DALYREJS-FILE` | SEQUENTIAL | SEQUENTIAL | CBTRN02C |
| `DALYTRAN-FILE` | SEQUENTIAL | SEQUENTIAL | CBTRN01C |
| `DALYTRAN-FILE` | SEQUENTIAL | SEQUENTIAL | CBTRN02C |
| `DATE-PARMS-FILE` | SEQUENTIAL | None | CBTRN03C |
| `REPORT-FILE` | SEQUENTIAL | None | CBTRN03C |
| `TCATBAL-FILE` | VSAM | RANDOM | CBTRN02C |
| `TRANCATG-FILE` | VSAM | RANDOM | CBTRN03C |
| `TRANSACT-FILE` | VSAM | RANDOM | CBTRN01C |
| `TRANSACT-FILE` | VSAM | RANDOM | CBTRN02C |
| `TRANSACT-FILE` | SEQUENTIAL | None | CBTRN03C |
| `TRANTYPE-FILE` | VSAM | RANDOM | CBTRN03C |
| `XREF-FILE` | VSAM | RANDOM | CBTRN01C |
| `XREF-FILE` | VSAM | RANDOM | CBTRN02C |
| `XREF-FILE` | VSAM | RANDOM | CBTRN03C |

---

*Generated 2026-04-29 10:27*