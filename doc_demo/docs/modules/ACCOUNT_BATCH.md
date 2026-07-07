# Module: Batch Account Processing

> **Module ID:** `ACCOUNT_BATCH`  
> **Programs:** 4

---

## Business Purpose

Batch Account Processing

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [CBACT01C](../programs/CBACT01C.md) | BATCH | 431 |  |
| [CBACT02C](../programs/CBACT02C.md) | BATCH | 179 |  |
| [CBACT03C](../programs/CBACT03C.md) | BATCH | 179 |  |
| [CBACT04C](../programs/CBACT04C.md) | BATCH | 653 |  |



## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
| `ACCOUNT-FILE` | VSAM | RANDOM | CBACT04C |
| `ACCTFILE-FILE` | VSAM | SEQUENTIAL | CBACT01C |
| `ARRY-FILE` | SEQUENTIAL | SEQUENTIAL | CBACT01C |
| `CARDFILE-FILE` | VSAM | SEQUENTIAL | CBACT02C |
| `DISCGRP-FILE` | VSAM | RANDOM | CBACT04C |
| `OUT-FILE` | SEQUENTIAL | SEQUENTIAL | CBACT01C |
| `TCATBAL-FILE` | VSAM | SEQUENTIAL | CBACT04C |
| `TRANSACT-FILE` | SEQUENTIAL | SEQUENTIAL | CBACT04C |
| `VBRC-FILE` | SEQUENTIAL | SEQUENTIAL | CBACT01C |
| `XREF-FILE` | VSAM | RANDOM | CBACT04C |
| `XREFFILE-FILE` | VSAM | SEQUENTIAL | CBACT03C |

---

*Generated 2026-04-29 10:27*