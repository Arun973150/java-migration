# Module: Online Processing (Uncategorised)

> **Module ID:** `ONLINE_PROCESSING`  
> **Programs:** 8

---

## Business Purpose

Online Processing (Uncategorised)

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
| [COACCT01](../programs/COACCT01.md) | ONLINE | 621 |  |
| [COBTUPDT](../programs/COBTUPDT.md) | DB2 | 238 |  |
| [CODATE01](../programs/CODATE01.md) | ONLINE | 525 |  |
| [COPAUA0C](../programs/COPAUA0C.md) | ONLINE | 1027 | This program is triggered by incoming message queue requests... |
| [COPAUS0C](../programs/COPAUS0C.md) | ONLINE | 1033 | This program is triggered by a user's interaction with a CIC... |
| [COPAUS1C](../programs/COPAUS1C.md) | ONLINE | 605 | This program is triggered when a user navigates to the authe... |
| [COPAUS2C](../programs/COPAUS2C.md) | ONLINE | 245 | This program is triggered when a user signs on to the system... |
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
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |
| [CTRTLIA](../screens/CTRTLIA.md) | CTRTLIA | COTRTLI | [COTRTLIC](../programs/COTRTLIC.md) |


---

*Generated 2026-03-16 19:39*