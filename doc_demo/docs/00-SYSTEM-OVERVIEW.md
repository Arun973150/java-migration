# Carddemo - System Overview

> **Auto-generated documentation** | 2026-05-12 12:31  
> Analyzed from 44 COBOL programs across 16 functional modules

---

## What is Carddemo?

Carddemo is a mainframe COBOL application composed of 44 programs
across 16 functional modules. It exposes 21 BMS screens for
online (CICS) interaction and is orchestrated by 55 JCL batch
jobs. The sections below summarize its structure, dependencies, and modernization-relevant
characteristics.

## System at a Glance

| Metric | Count |
|--------|-------|
| Programs | 44 |
| Functional Modules | 16 |
| BMS Screens | 21 |
| Data Items | 7383 |
| CICS Commands | 101 |
| SQL Statements | 28 |
| Inter-Program Calls | 59 |
| Business Rules | 447 |
| Copybooks | 73 |

## Architecture Overview

```mermaid
flowchart TB
    subgraph ONLINE["Online (CICS) Programs"]
        COACCT01["COACCT01"]
        COACTUPC["COACTUPC"]
        COACTVWC["COACTVWC"]
        COADM01C["COADM01C"]
        COBIL00C["COBIL00C"]
        COCRDLIC["COCRDLIC"]
        COCRDSLC["COCRDSLC"]
        COCRDUPC["COCRDUPC"]
        CODATE01["CODATE01"]
        COMEN01C["COMEN01C"]
        COPAUA0C["COPAUA0C"]
        COPAUS0C["COPAUS0C"]
    end

    subgraph BATCH["Batch Programs"]
        CBACT01C["CBACT01C"]
        CBACT02C["CBACT02C"]
        CBACT03C["CBACT03C"]
        CBACT04C["CBACT04C"]
        CBCUS01C["CBCUS01C"]
        CBEXPORT["CBEXPORT"]
        CBIMPORT["CBIMPORT"]
        CBPAUP0C["CBPAUP0C"]
    end


    USER([User/CSR]) --> ONLINE
    SCHEDULER([Job Scheduler]) --> BATCH
```

## Functional Modules

### [Module CB](modules/CB.md)

Module CB

| Programs | Type |
|----------|------|
| [CBCUS01C](programs/CBCUS01C.md) | BATCH |
| [CBEXPORT](programs/CBEXPORT.md) | BATCH |
| [CBIMPORT](programs/CBIMPORT.md) | BATCH |
| [CBPAUP0C](programs/CBPAUP0C.md) | BATCH |

### [Program](modules/CBACT.md)

Program

| Programs | Type |
|----------|------|
| [CBACT01C](programs/CBACT01C.md) | BATCH |
| [CBACT02C](programs/CBACT02C.md) | BATCH |
| [CBACT03C](programs/CBACT03C.md) | BATCH |
| [CBACT04C](programs/CBACT04C.md) | BATCH |

### [Custfile](modules/CBSTM.md)

Custfile

| Programs | Type |
|----------|------|
| [CBSTM03A](programs/CBSTM03A.md) | BATCH |
| [CBSTM03B](programs/CBSTM03B.md) | BATCH |

### [Tranfile](modules/CBTRN.md)

Tranfile

| Programs | Type |
|----------|------|
| [CBTRN01C](programs/CBTRN01C.md) | BATCH |
| [CBTRN02C](programs/CBTRN02C.md) | BATCH |
| [CBTRN03C](programs/CBTRN03C.md) | BATCH |

### [Module CO](modules/CO.md)

Module CO

| Programs | Type |
|----------|------|
| [CODATE01](programs/CODATE01.md) | ONLINE |
| [COMEN01C](programs/COMEN01C.md) | ONLINE |
| [CORPT00C](programs/CORPT00C.md) | ONLINE |
| [COSGN00C](programs/COSGN00C.md) | ONLINE |

### [Pgmiderr](modules/COA.md)

Pgmiderr

| Programs | Type |
|----------|------|
| [COADM01C](programs/COADM01C.md) | ONLINE |

### [Termination](modules/COAC.md)

Termination

| Programs | Type |
|----------|------|
| [COACCT01](programs/COACCT01.md) | ONLINE |

### [Getcardxref](modules/COACT.md)

Getcardxref

| Programs | Type |
|----------|------|
| [COACTUPC](programs/COACTUPC.md) | ONLINE |
| [COACTVWC](programs/COACTVWC.md) | ONLINE |

### [Update](modules/COB.md)

Update

| Programs | Type |
|----------|------|
| [COBIL00C](programs/COBIL00C.md) | ONLINE |
| [COBSWAIT](programs/COBSWAIT.md) | BATCH |
| [COBTUPDT](programs/COBTUPDT.md) | DB2 |

### [Account](modules/COCRD.md)

Account

| Programs | Type |
|----------|------|
| [COCRDLIC](programs/COCRDLIC.md) | ONLINE |
| [COCRDSLC](programs/COCRDSLC.md) | ONLINE |
| [COCRDUPC](programs/COCRDUPC.md) | ONLINE |

### [Para](modules/COPAU.md)

Para

| Programs | Type |
|----------|------|
| [COPAUA0C](programs/COPAUA0C.md) | ONLINE |
| [COPAUS0C](programs/COPAUS0C.md) | ONLINE |
| [COPAUS1C](programs/COPAUS1C.md) | ONLINE |
| [COPAUS2C](programs/COPAUS2C.md) | ONLINE |

### [Initialize (COTRN)](modules/COTRN.md)

Initialize (COTRN)

| Programs | Type |
|----------|------|
| [COTRN00C](programs/COTRN00C.md) | ONLINE |
| [COTRN01C](programs/COTRN01C.md) | ONLINE |
| [COTRN02C](programs/COTRN02C.md) | ONLINE |

### [Alphanum](modules/COTRT.md)

Alphanum

| Programs | Type |
|----------|------|
| [COTRTLIC](programs/COTRTLIC.md) | ONLINE |
| [COTRTUPC](programs/COTRTUPC.md) | ONLINE |

### [Initialize (COUSR)](modules/COUSR.md)

Initialize (COUSR)

| Programs | Type |
|----------|------|
| [COUSR00C](programs/COUSR00C.md) | ONLINE |
| [COUSR01C](programs/COUSR01C.md) | ONLINE |
| [COUSR02C](programs/COUSR02C.md) | ONLINE |
| [COUSR03C](programs/COUSR03C.md) | ONLINE |

### [Initialize](modules/OTHER.md)

Initialize

| Programs | Type |
|----------|------|
| [CSUTLDTC](programs/CSUTLDTC.md) | BATCH |
| [DBUNLDGS](programs/DBUNLDGS.md) | BATCH |

### [Initialize (PAUDB)](modules/PAUDB.md)

Initialize (PAUDB)

| Programs | Type |
|----------|------|
| [PAUDBLOD](programs/PAUDBLOD.md) | BATCH |
| [PAUDBUNL](programs/PAUDBUNL.md) | BATCH |


## Entry Points

Programs that are not called by others -- these are likely user-facing entry points:

- [CBACT01C](programs/CBACT01C.md)
- [CBACT02C](programs/CBACT02C.md)
- [CBACT03C](programs/CBACT03C.md)
- [CBACT04C](programs/CBACT04C.md)
- [CBCUS01C](programs/CBCUS01C.md)
- [CBEXPORT](programs/CBEXPORT.md)
- [CBIMPORT](programs/CBIMPORT.md)
- [CBPAUP0C](programs/CBPAUP0C.md)
- [CBSTM03A](programs/CBSTM03A.md)
- [CBSTM03B](programs/CBSTM03B.md)
- [CBTRN01C](programs/CBTRN01C.md)
- [CBTRN02C](programs/CBTRN02C.md)
- [CBTRN03C](programs/CBTRN03C.md)
- [COACCT01](programs/COACCT01.md)
- [COACTUPC](programs/COACTUPC.md)
- [COACTVWC](programs/COACTVWC.md)
- [COADM01C](programs/COADM01C.md)
- [COBIL00C](programs/COBIL00C.md)
- [COBSWAIT](programs/COBSWAIT.md)
- [COBTUPDT](programs/COBTUPDT.md)
- [COCRDLIC](programs/COCRDLIC.md)
- [COCRDSLC](programs/COCRDSLC.md)
- [COCRDUPC](programs/COCRDUPC.md)
- [CODATE01](programs/CODATE01.md)
- [COMEN01C](programs/COMEN01C.md)
- [COPAUA0C](programs/COPAUA0C.md)
- [COPAUS0C](programs/COPAUS0C.md)
- [COPAUS1C](programs/COPAUS1C.md)
- [COPAUS2C](programs/COPAUS2C.md)
- [CORPT00C](programs/CORPT00C.md)
- [COSGN00C](programs/COSGN00C.md)
- [COTRN00C](programs/COTRN00C.md)
- [COTRN01C](programs/COTRN01C.md)
- [COTRN02C](programs/COTRN02C.md)
- [COTRTLIC](programs/COTRTLIC.md)
- [COTRTUPC](programs/COTRTUPC.md)
- [COUSR00C](programs/COUSR00C.md)
- [COUSR01C](programs/COUSR01C.md)
- [COUSR02C](programs/COUSR02C.md)
- [COUSR03C](programs/COUSR03C.md)
- [CSUTLDTC](programs/CSUTLDTC.md)
- [DBUNLDGS](programs/DBUNLDGS.md)
- [PAUDBLOD](programs/PAUDBLOD.md)
- [PAUDBUNL](programs/PAUDBUNL.md)

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Program Documentation](programs/) | Detailed walkthrough for each COBOL program |
| [Linked Programs](clusters/INDEX.md) | Connected program clusters and dependency graphs |
| [Module Documentation](modules/) | Business-grouped program clusters |
| [Business Rules Catalog](business-rules/INDEX.md) | All extracted business rules |
| [Screen Catalog](screens/INDEX.md) | BMS screen definitions and layouts |
| [Call Graph](diagrams/call-graph.md) | Inter-program dependency diagram |
| [Data Dictionary](data-dictionary.md) | Complete variable listing |
| [Copybook Reference](copybook-reference.md) | Shared data structures |

---

*Generated by COBOL Documentation Pipeline*