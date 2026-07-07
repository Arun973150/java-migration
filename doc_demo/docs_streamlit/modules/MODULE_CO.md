# Module: Module: MODULE_CO

> **Module ID:** `MODULE_CO`  
> **Programs:** 8

---

## Business Purpose

Module: MODULE_CO

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [COACCT01](../programs/COACCT01.md) | ONLINE | 621 |  |
| [COBTUPDT](../programs/COBTUPDT.md) | DB2 | 238 |  |
| [CODATE01](../programs/CODATE01.md) | ONLINE | 525 |  |
| [COPAUA0C](../programs/COPAUA0C.md) | ONLINE | 1027 |  |
| [COPAUS0C](../programs/COPAUS0C.md) | ONLINE | 1033 |  |
| [COPAUS1C](../programs/COPAUS1C.md) | ONLINE | 605 |  |
| [COPAUS2C](../programs/COPAUS2C.md) | ONLINE | 245 |  |
| [COTRTLIC](../programs/COTRTLIC.md) | ONLINE | 2099 |  |

## Internal Call Flow

Programs in this module interact through the following call chain:

```mermaid
flowchart LR
    COACCT01["COACCT01"] --> MQCLOSE["MQCLOSE"]
    COACCT01["COACCT01"] --> MQGET["MQGET"]
    COACCT01["COACCT01"] --> MQOPEN["MQOPEN"]
    COACCT01["COACCT01"] --> MQPUT["MQPUT"]
    CODATE01["CODATE01"] --> MQCLOSE["MQCLOSE"]
    CODATE01["CODATE01"] --> MQGET["MQGET"]
    CODATE01["CODATE01"] --> MQOPEN["MQOPEN"]
    CODATE01["CODATE01"] --> MQPUT["MQPUT"]
    COPAUA0C["COPAUA0C"] --> MQCLOSE["MQCLOSE"]
    COPAUA0C["COPAUA0C"] --> MQGET["MQGET"]
    COPAUA0C["COPAUA0C"] --> MQOPEN["MQOPEN"]
    COPAUA0C["COPAUA0C"] --> MQPUT1["MQPUT1"]
```

| Caller | Calls | Line |
|--------|-------|------|
| [COACCT01](../programs/COACCT01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 557 |
| [COACCT01](../programs/COACCT01.md) | [MQGET](../programs/MQGET.md) | 352 |
| [COACCT01](../programs/COACCT01.md) | [MQOPEN](../programs/MQOPEN.md) | 233 |
| [COACCT01](../programs/COACCT01.md) | [MQPUT](../programs/MQPUT.md) | 479 |
| [CODATE01](../programs/CODATE01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 461 |
| [CODATE01](../programs/CODATE01.md) | [MQGET](../programs/MQGET.md) | 301 |
| [CODATE01](../programs/CODATE01.md) | [MQOPEN](../programs/MQOPEN.md) | 182 |
| [CODATE01](../programs/CODATE01.md) | [MQPUT](../programs/MQPUT.md) | 383 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQCLOSE](../programs/MQCLOSE.md) | 956 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQGET](../programs/MQGET.md) | 400 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQOPEN](../programs/MQOPEN.md) | 262 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQPUT1](../programs/MQPUT1.md) | 758 |

## Associated Screens

| Screen | Map | Mapset | Program |
|--------|-----|--------|---------|
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |


---

*Generated 2026-02-13 16:01*