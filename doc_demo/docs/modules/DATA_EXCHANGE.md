# Module: Data Import/Export

> **Module ID:** `DATA_EXCHANGE`  
> **Programs:** 2

---

## Business Purpose

Data Import/Export

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [CBEXPORT](../programs/CBEXPORT.md) | BATCH | 583 |  |
| [CBIMPORT](../programs/CBIMPORT.md) | BATCH | 488 |  |



## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
| `ACCOUNT-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `ACCOUNT-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
| `CARD-INPUT` | VSAM | SEQUENTIAL | CBEXPORT |
| `CARD-OUTPUT` | SEQUENTIAL | SEQUENTIAL | CBIMPORT |
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

*Generated 2026-04-29 10:27*