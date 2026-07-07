# Module: Module CB

> **Module ID:** `CB`  
> **Programs:** 4

---

## Business Purpose

Module CB

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [CBCUS01C](../programs/CBCUS01C.md) | BATCH | 179 |  |
| [CBEXPORT](../programs/CBEXPORT.md) | BATCH | 583 |  |
| [CBIMPORT](../programs/CBIMPORT.md) | BATCH | 488 |  |
| [CBPAUP0C](../programs/CBPAUP0C.md) | BATCH | 387 |  |



## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
| `ACCOUNT-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `ACCOUNT-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `CARD-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `CARD-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `CUSTFILE-FILE` | VSAM | SEQUENTIAL | CBCUS01C |
| `CUSTOMER-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `CUSTOMER-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `ERROR-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `EXPORT-INPUT` | VSAM | SEQUENTIAL | CBIMPORT |
| `EXPORT-OUTPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `TRANSACTION-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `TRANSACTION-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `XREF-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `XREF-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |

---

*Generated 2026-05-12 12:31*