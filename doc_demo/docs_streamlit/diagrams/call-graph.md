# Program Call Hierarchy

> Inter-program call relationships across the entire CardDemo application.

## Visual Call Graph

```mermaid
graph LR
    COACCT01["COACCT01"] --> MQOPEN["MQOPEN"]
    COACCT01["COACCT01"] --> MQGET["MQGET"]
    COACCT01["COACCT01"] --> MQPUT["MQPUT"]
    COACCT01["COACCT01"] --> MQCLOSE["MQCLOSE"]
    CODATE01["CODATE01"] --> MQOPEN["MQOPEN"]
    CODATE01["CODATE01"] --> MQGET["MQGET"]
    CODATE01["CODATE01"] --> MQPUT["MQPUT"]
    CODATE01["CODATE01"] --> MQCLOSE["MQCLOSE"]
    COPAUA0C["Message Queue Request Processor"] --> MQOPEN["MQOPEN"]
    COPAUA0C["Message Queue Request Processor"] --> MQGET["MQGET"]
    COPAUA0C["Message Queue Request Processor"] --> MQPUT1["MQPUT1"]
    COPAUA0C["Message Queue Request Processor"] --> MQCLOSE["MQCLOSE"]
```

## Call Matrix

| Caller | Calls | Line |
|--------|-------|------|
| [COACCT01](../programs/COACCT01.md) | [MQOPEN](../programs/MQOPEN.md) | 233 |
| [COACCT01](../programs/COACCT01.md) | [MQOPEN](../programs/MQOPEN.md) | 267 |
| [COACCT01](../programs/COACCT01.md) | [MQOPEN](../programs/MQOPEN.md) | 302 |
| [COACCT01](../programs/COACCT01.md) | [MQGET](../programs/MQGET.md) | 352 |
| [COACCT01](../programs/COACCT01.md) | [MQPUT](../programs/MQPUT.md) | 479 |
| [COACCT01](../programs/COACCT01.md) | [MQPUT](../programs/MQPUT.md) | 516 |
| [COACCT01](../programs/COACCT01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 557 |
| [COACCT01](../programs/COACCT01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 579 |
| [COACCT01](../programs/COACCT01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 602 |
| [CODATE01](../programs/CODATE01.md) | [MQOPEN](../programs/MQOPEN.md) | 182 |
| [CODATE01](../programs/CODATE01.md) | [MQOPEN](../programs/MQOPEN.md) | 216 |
| [CODATE01](../programs/CODATE01.md) | [MQOPEN](../programs/MQOPEN.md) | 251 |
| [CODATE01](../programs/CODATE01.md) | [MQGET](../programs/MQGET.md) | 301 |
| [CODATE01](../programs/CODATE01.md) | [MQPUT](../programs/MQPUT.md) | 383 |
| [CODATE01](../programs/CODATE01.md) | [MQPUT](../programs/MQPUT.md) | 420 |
| [CODATE01](../programs/CODATE01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 461 |
| [CODATE01](../programs/CODATE01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 483 |
| [CODATE01](../programs/CODATE01.md) | [MQCLOSE](../programs/MQCLOSE.md) | 506 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQOPEN](../programs/MQOPEN.md) | 262 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQGET](../programs/MQGET.md) | 400 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQPUT1](../programs/MQPUT1.md) | 758 |
| [COPAUA0C](../programs/COPAUA0C.md) | [MQCLOSE](../programs/MQCLOSE.md) | 956 |

## Entry Points

Programs not called by any other program (likely top-level entry points or CICS transaction starters):

- [00220000](../programs/00220000.md)
- [CBACT01C](../programs/CBACT01C.md)
- [CBACT02C](../programs/CBACT02C.md)
- [CBACT03C](../programs/CBACT03C.md)
- [CBACT04C](../programs/CBACT04C.md)
- [CBCUS01C](../programs/CBCUS01C.md)
- [CBEXPORT](../programs/CBEXPORT.md)
- [CBIMPORT](../programs/CBIMPORT.md)
- [CBPAUP0C](../programs/CBPAUP0C.md)
- [CBSTM03A](../programs/CBSTM03A.md)
- [CBSTM03B](../programs/CBSTM03B.md)
- [CBTRN01C](../programs/CBTRN01C.md)
- [CBTRN02C](../programs/CBTRN02C.md)
- [CBTRN03C](../programs/CBTRN03C.md)
- [COACCT01](../programs/COACCT01.md)
- [COACTUPC](../programs/COACTUPC.md)
- [COACTVWC](../programs/COACTVWC.md)
- [COADM01C](../programs/COADM01C.md)
- [COBIL00C](../programs/COBIL00C.md)
- [COBSWAIT](../programs/COBSWAIT.md)
- [COBTUPDT](../programs/COBTUPDT.md)
- [COCRDLIC](../programs/COCRDLIC.md)
- [COCRDSLC](../programs/COCRDSLC.md)
- [COCRDUPC](../programs/COCRDUPC.md)
- [CODATE01](../programs/CODATE01.md)
- [COMEN01C](../programs/COMEN01C.md)
- [COPAUA0C](../programs/COPAUA0C.md)
- [COPAUS0C](../programs/COPAUS0C.md)
- [COPAUS1C](../programs/COPAUS1C.md)
- [COPAUS2C](../programs/COPAUS2C.md)
- [CORPT00C](../programs/CORPT00C.md)
- [COSGN00C](../programs/COSGN00C.md)
- [COTRN00C](../programs/COTRN00C.md)
- [COTRN01C](../programs/COTRN01C.md)
- [COTRN02C](../programs/COTRN02C.md)
- [COTRTLIC](../programs/COTRTLIC.md)
- [COUSR00C](../programs/COUSR00C.md)
- [COUSR01C](../programs/COUSR01C.md)
- [COUSR02C](../programs/COUSR02C.md)
- [COUSR03C](../programs/COUSR03C.md)
- [CSUTLDTC](../programs/CSUTLDTC.md)
- [DBUNLDGS](../programs/DBUNLDGS.md)
- [PAUDBLOD](../programs/PAUDBLOD.md)
- [PAUDBUNL](../programs/PAUDBUNL.md)

## Leaf Programs

Programs that don't call any other program (utility or terminal logic):

- [00220000](../programs/00220000.md)
- [CBPAUP0C](../programs/CBPAUP0C.md)
- [CBSTM03B](../programs/CBSTM03B.md)
- [COACTUPC](../programs/COACTUPC.md)
- [COACTVWC](../programs/COACTVWC.md)
- [COADM01C](../programs/COADM01C.md)
- [COBIL00C](../programs/COBIL00C.md)
- [COBSWAIT](../programs/COBSWAIT.md)
- [COBTUPDT](../programs/COBTUPDT.md)
- [COCRDLIC](../programs/COCRDLIC.md)
- [COCRDSLC](../programs/COCRDSLC.md)
- [COCRDUPC](../programs/COCRDUPC.md)
- [COMEN01C](../programs/COMEN01C.md)
- [COPAUS0C](../programs/COPAUS0C.md)
- [COPAUS1C](../programs/COPAUS1C.md)
- [COPAUS2C](../programs/COPAUS2C.md)
- [CORPT00C](../programs/CORPT00C.md)
- [COSGN00C](../programs/COSGN00C.md)
- [COTRN00C](../programs/COTRN00C.md)
- [COTRN01C](../programs/COTRN01C.md)
- [COTRTLIC](../programs/COTRTLIC.md)
- [COUSR00C](../programs/COUSR00C.md)
- [COUSR01C](../programs/COUSR01C.md)
- [COUSR02C](../programs/COUSR02C.md)
- [COUSR03C](../programs/COUSR03C.md)

---

*Generated 2026-03-16 19:39*