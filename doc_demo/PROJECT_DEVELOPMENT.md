# Project Development Record

> A comprehensive, chronological account of everything we built, every dead end we hit, every fix we found, and the state of the system today. Written for a reader who knows nothing about mainframe modernization, COBOL, or the specific tools used here.

---

## Table of Contents

1. [What Is This Project About?](#1-what-is-this-project-about)
2. [The Domain: Mainframe Modernization](#2-the-domain-mainframe-modernization)
3. [Stage 1 — Exploration and Benchmarking](#3-stage-1--exploration-and-benchmarking)
4. [Stage 2 — The COBOL Parser Pipeline (Proof of Concept)](#4-stage-2--the-cobol-parser-pipeline-proof-of-concept)
5. [Stage 3 — The Unified Parser (COBOL + JCL + BMS + CICS)](#5-stage-3--the-unified-parser-cobol--jcl--bms--cics)
6. [Current State of the System](#6-current-state-of-the-system)
7. [Known Limitations (Across All Stages)](#7-known-limitations-across-all-stages)
8. [What Can Be Improved](#8-what-can-be-improved)
9. [Stage 4 — The 3-Layer Graph and Multi-Target Generation](#9-stage-4--the-3-layer-graph-and-multi-target-generation)

---

## 1. What Is This Project About?

At the highest level, this project is about **understanding legacy mainframe software automatically** — specifically, software written in COBOL (a programming language from 1959 that still runs the financial systems of most of the world) running on IBM Z-series mainframes.

The goal is to build a pipeline that can:

1. Take the raw source code of a real mainframe application
2. Automatically parse and understand its structure (programs, subroutines, data definitions, job scripts, screen maps)
3. Store everything in a structured, queryable database
4. Use that structured knowledge as a foundation for modernization, migration analysis, or LLM-assisted code translation

The target application we use throughout is **AWS's CardDemo repository** — an open-source sample credit card management system written exactly as a real 1980s mainframe application would be, complete with COBOL programs, JCL job scripts, BMS screen definitions, and CICS transaction calls. It's the closest thing to a real mainframe application you can work with publicly.

The target migration platform is **Unisys MCP** — a different mainframe-class operating system with its own programming languages (WFL for job scripts, MCP COBOL for programs). Migrating from IBM Z to Unisys MCP is exactly the kind of expensive, risky, multi-year effort this project is trying to make more tractable.

---

## 2. The Domain: Mainframe Modernization

Before describing what we built, it helps to understand the terminology that will come up constantly.

### COBOL

COBOL (Common Business-Oriented Language, 1959) is a rigid, verbose, column-based programming language. Unlike Python or Java, every line has a **fixed physical layout**:
- Columns 1-6: sequence numbers (just labels, ignored by the compiler)
- Column 7: indicator (`*` means comment, `-` means continuation, space means code)
- Columns 8-72: actual code
- Columns 73+: identification area (ignored)

This matters because any tool that reads COBOL must respect this structure, or it will misidentify comments as code and vice versa.

### Copybooks

COBOL programs share data structures through **copybooks** — separate files that get textually included at compile time via a `COPY` statement. This is functionally similar to `#include` in C, but with an important difference: the COBOL compiler (or parser) must physically locate and read every referenced copybook file before it can parse anything. A missing copybook causes a complete parse failure for the entire program, not just for that one file.

IBM's CICS middleware and MQ messaging platform distribute their own copybooks (`DFHBMSCA`, `DFHAID`, `CMQMDV`, etc.) that are proprietary and not included in any open-source repository. Any real CICS or MQ application will reference these. This is one of the fundamental obstacles we had to solve.

### JCL (Job Control Language)

JCL is how IBM Z mainframe jobs are submitted — it's the script that says "run this program, in this order, reading from these files, writing to those files." Every batch job on a mainframe is defined by a JCL script. Understanding JCL is essential for migration because it defines the execution flow of the entire system. Unisys uses WFL (Work Flow Language) instead.

### BMS (Basic Mapping Support)

BMS is the way CICS interactive terminal screens are defined in IBM COBOL applications. A BMS source file (sometimes called a mapset) defines the layout of a terminal screen — where fields appear, their lengths, their attributes (protected, unprotected, numeric, etc.). These need to be translated into equivalent screen definitions on the target platform.

### CICS (Customer Information Control System)

CICS is the IBM transaction processing middleware. When a COBOL program needs to read from a screen, write to a screen, call another program, or access a file transactionally, it uses `EXEC CICS ... END-EXEC` blocks. ProLeap (our primary COBOL parser) understands most of these, but not all.

### ProLeap

ProLeap is an open-source Java library (version 4.0.0) that parses COBOL source files into a structured data format called an **ASG (Abstract Syntax Graph)**. It's the most capable open-source COBOL parser available. We access it from Python using **Py4J**, a library that creates a socket bridge between Python and a running Java virtual machine. ProLeap is the backbone of the COBOL parsing side of the entire project.

---

## 3. Stage 1 — Exploration and Benchmarking

### What We Were Trying to Do

Before building anything production-quality, the first stage was about understanding the landscape. The goal at this point was to answer: *Can LLMs actually be useful for COBOL-to-Python (or COBOL-to-MCP-COBOL) translation if you feed them structured, parsed COBOL rather than raw source?*

Two systems were built in parallel during this stage.

### 3.1 The Hybrid Demo (`hybrid-demo/`)

The hybrid demo was the conceptual proof of the overall architecture. It demonstrated a four-agent pipeline:

1. **Parser Agent** — deterministic extraction of JCL and COBOL structure
2. **Planner Agent** — LLM enrichment for business intent and migration plan
3. **Executor Agent** — code generation targeting WFL and MCP COBOL
4. **Critic Agent** — validation and migration report generation

The key insight captured in this demo is a design principle that has held throughout the entire project: **the LLM should never recalculate what deterministic tools can get right.** Byte offsets, PIC clause lengths, file-to-dataset mappings — these are exact and should come from the parser. The LLM should focus only on what parsers are bad at: business intent, naming conventions for cryptic variables, identifying dead code, and estimating migration complexity.

This demo also contained the first version of the **ProLeap gateway** — the Java shim that wraps ProLeap's API and exposes it over a Py4J socket so Python code can call it. Everything built in later stages depends on this gateway.

The demo included working sample translations showing JCL-to-WFL and COBOL-to-MCP-COBOL conversion rules, but it was not automated — it was designed for showcasing the concept, not for running against a full codebase.

### 3.2 The LLM Evaluation Framework (`llm-eval-app/` and `Week_1/mcp-migration-eval/`)

The second piece of Stage 1 was a benchmarking harness to answer a quantitative question: given the ProLeap ASG (structured parse output) of a COBOL program as input, which LLM produces the most faithful Python translation?

The evaluation framework tested four providers:
- **OpenRouter** (Mistral, Llama, and other open-weight models via cloud API)
- **Google Gemini** (gemini-2.5-flash)
- **Groq** (llama, mixtral, gemma on Groq hardware)
- **LM Studio** (local GGUF models, for on-premise evaluation)

Translations were scored on four dimensions:

| Metric | Weight | What It Checks |
|--------|--------|----------------|
| Dependency Resolution | 30% | Did the LLM correctly acknowledge data fields coming from copied libraries? |
| Logic Fidelity | 40% | Did a `> 5000` check stay `> 5000`, not become `>= 5000`? |
| Syntax Validity | 20% | Does `python -m py_compile` pass on the output? |
| Hallucination | 10% | Did the LLM invent variables that don't exist in the input? |

The separate `mcp-migration-eval` harness in Stage 1 targeted Unisys MCP specifically — scoring outputs for WFL and MCP COBOL target languages across multiple LLM models configured in a YAML file. It used the same ASG inputs, just targeted the migration platform rather than Python translation.

### 3.3 What We Learned from Stage 1

- LLMs perform significantly better when given structured ASG input rather than raw COBOL source. The structured format removes ambiguity and forces the model to focus on logic rather than syntax comprehension.
- Logic fidelity (getting comparison operators and boundary conditions exactly right) was the hardest metric for all models.
- The ProLeap gateway worked reliably as a subprocess, but getting it to handle the full diversity of a real-world COBOL codebase required additional work. The existing `parse_carddemo_asg.py` script (the first reference implementation) was too brittle for anything beyond a demonstration.
- There was clear value in automating the parsing across the entire CardDemo codebase rather than running it file-by-file by hand. The natural next step was to build a proper pipeline.

---

## 4. Stage 2 — The COBOL Parser Pipeline (Proof of Concept)

### What We Inherited and Why It Wasn't Good Enough

At the start of Stage 2, the reference implementation was a single script: `llm-eval-app/src/parse_carddemo_asg.py`. This script showed how to call ProLeap and get structured output, but it had serious problems:

| Problem | Consequence |
|---------|------------|
| Hardcoded copybook paths | Only worked on the exact machine with the exact directory structure it expected |
| Only 5 copybook stubs | Any program referencing IBM CICS or MQ system copybooks would fail entirely |
| No EXEC DLI handling | Four IMS-facing programs would crash the parser with an unrecognized grammar error |
| Flat JSON file output | Useful for one-off inspection, not for queries like "which programs call X?" |
| No error recovery | One failure could corrupt state |
| Not idempotent | Running twice produced inconsistent results |

The instruction was: *"Use this as a base to understand how my system uses ProLeap. I want it to be better than this because it was very brittle."*

### 4.1 Design Decisions Made Before Writing Code

Several key decisions were made upfront:

1. **Modular architecture** — Each concern gets its own file. No monolithic scripts.
2. **SQLite over flat JSON** — One queryable file, full SQL support, built into Python, no server needed.
3. **Auto-discovery over hardcoding** — Walk the repo tree to find copybook directories rather than hardcoding paths.
4. **Source scanner independent of ProLeap** — Always extract COPY/CALL/PERFORM from raw text, even when ProLeap fails. That way, failed programs still contribute dependency data.
5. **Context manager for the gateway** — The Java process is always shut down cleanly.

### 4.2 What Was Built (v1)

Six new modules were written from scratch:

| Module | Role |
|--------|------|
| `resolver.py` | Walks the repo tree to find copybook directories; writes stub copybooks for proprietary IBM files |
| `gateway.py` | Starts the ProLeap Java process, manages the Py4J connection, shuts it down on exit |
| `cobol_source_scanner.py` | Regex-based scanner for COPY/CALL/PERFORM statements, respecting COBOL's fixed column layout |
| `asg_extractor.py` | Translates ProLeap's raw JSON output into typed Python structures |
| `db.py` | SQLite schema with 7 tables, all insert/query/upsert operations |
| `pipeline.py` | Master orchestrator: discovery → gateway → scan → persist → report |

Plus `run.py` (CLI entry point) and `showcase.py` (11-section SQL query reporter).

### 4.3 Run 1: The First Attempt — 31/44 Parsed (70.5%)

The very first run parsed 31 out of 44 COBOL files. The failures fell into four categories.

**Category 1: EXEC DLI (4 files)**

Four programs in the IMS/DB2/MQ variant directory used `EXEC DLI ... END-EXEC` syntax for calling IMS database operations. ProLeap 4.0.0 has no IMS grammar. When it hits `EXEC DLI`, the parser's state machine breaks and the entire file fails.

These four files are: `CBPAUP0C.cbl`, `COPAUA0C.cbl`, `COPAUS0C.cbl`, `COPAUS1C.cbl`.

**Category 2: Missing CSSTRPFY copybook (5 files)**

`CSSTRPFY` is a CardDemo-internal utility copybook that is referenced but simply not present in this version of the repository. ProLeap refuses to proceed without it.

**Category 3: Missing CSUTLDWY copybook (2 files)**

Same root cause as CSSTRPFY. A different CardDemo-internal utility copybook, absent from the repo snapshot.

**Category 4: Missing IBM MQ copybooks (2 files)**

The initial stub inventory only covered 5 IBM system copybooks. The MQ-variant programs (`CBPAUP0C` and related) also needed `CMQMDV`, `CMQODV`, `CMQTML`, and `CMQV` — the IBM MQ Message Descriptor and related structures.

### 4.4 Iteration 1: Fixing EXEC DLI and More MQ Stubs — 37/44 (84.1%)

**The EXEC DLI solution:**

The approach chosen was surgical: try to parse normally first, and only if ProLeap returns an error mentioning "EXEC DLI", strip those blocks from a temp copy and re-parse.

The first implementation of the temp file was wrong. It wrote the stripped file to the system temp directory (`C:\Users\user\AppData\Local\Temp\`). ProLeap resolves copybook references partly based on the source file's own directory. A file placed in the system temp directory can't find any copybooks, and the parse would either fail or succeed with missing dependencies.

The fix: place the temp file in `dir=str(src.parent)` — the same directory as the original source file. This preserves ProLeap's copybook resolution logic. The temp file (`_proleap_tmp_<random>.cbl`) is deleted in a `finally` block regardless of what happens.

**The new stubs:**

Added 6 new stubs: `CMQMDV` (IBM MQ message descriptor, 8 fields in v1), `CMQODV`, `CMQTML`, `CMQV` (return code constants), and two initial attempts at `CSSTRPFY` and `CSUTLDWY`.

The CSSTRPFY/CSUTLDWY stubs were written as data-definition stubs:
```cobol
       01 CSSTRPFY.
          05 FILLER PIC X(1).
```

This seemed reasonable at the time. It would turn out to be wrong.

**Result: 31 → 37 (6 more files parsing)**

### 4.5 Iteration 2: The "Mismatched FILLER" Problem — 43/44 (97.7%)

After adding the stubs, the DB2 variant programs (`CBSTM03A.CBL`, `CBSTM03B.CBL`, and others that COPY `CSSTRPFY`) now failed with a different error: `CobolParserException: mismatched input 'FILLER' expecting...`

This took investigation to understand. The root cause: when ProLeap preprocesses COBOL, it **textually injects** the full content of each copybook at the point of the COPY statement. The programs that COPY `CSSTRPFY` already have their own data section with their own `01`-level items. Injecting another `01 CSSTRPFY` group into the middle of an existing data section creates a structural conflict — ProLeap sees a new top-level group item where it expected continuation of the existing one.

The solution: make CSSTRPFY and CSUTLDWY **comment-only stubs** — files that contain only comment lines and no data definitions at all. ProLeap finds the file, "includes" it, but nothing gets injected into the host program's data section.

```cobol
      * CSSTRPFY stub - auto-generated by CardDemo parser
      * (original file not present in this repo snapshot)
```

At the same time, a second bug was discovered: the stub writer only wrote files if they didn't already exist. This meant that when stub content was updated (from data definition to comment-only), the old bad stub file remained on disk. The fix was simple: always overwrite, never check for existence first.

A third fix in this iteration: when a file that previously failed now succeeds on re-parse, the old error record needs to be removed from the `parse_errors` table. Without this, the database would show `parse_status = 'ok'` in the programs table AND an error record in parse_errors for the same file — contradictory state. Added `clear_parse_error()` to handle this.

**The one permanent failure:**

`COTRTLIC.cbl` uses the CICS verb `SEND-PLAIN-TEXT`, which ProLeap 4.0.0's grammar does not recognize. Error: `extraneous input 'SEND-PLAIN-TEXT'`. This is a genuine parser grammar gap that cannot be fixed by stubs or preprocessing. The only fix would be upgrading ProLeap to a version with this grammar rule, or patching the COBOL source. For now, this is accepted as permanent.

**Result: 37 → 43/44 (97.7%)**

### 4.6 A Platform-Specific Bug: Windows and Unicode

After the 43/44 milestone, a bug appeared when printing the summary table. The original code used Unicode box-drawing characters (`║`, `═`, `╔`, etc.) for visual formatting. On Windows PowerShell with code page 1252 (Western European), these characters cannot be encoded and the script crashed with `UnicodeEncodeError`.

This affected both `pipeline.py` (the parse summary table) and `showcase.py` (section headers). The fix: replace all Unicode box-drawing characters with plain ASCII equivalents (`+`, `|`, `=`, `-`). This is simpler than setting console encoding explicitly and works across all environments.

### 4.7 Brittleness Audit and Hardening (Iteration 4)

With 43/44 working, a full audit of all hardcoded and brittle elements was conducted. Every value that was baked into the code and would break on a different machine or different repository layout was identified and replaced with configurable, portable alternatives.

**gateway.py:**
- JAR path: was hardcoded relative to `Week 2/`'s location. Replaced with `_find_default_jar()` which walks up to 6 ancestor directories searching any `target/` subdirectory for `proleap-gateway-*.jar`.
- Port: was hardcoded as `25333`. Now auto-increments (up to +10) if the port is occupied. Configurable via `--port` CLI arg or `PROLEAP_GATEWAY_PORT` env var.
- Connect timeout: was hardcoded 120 seconds. Now configurable via `--timeout` or `PROLEAP_GATEWAY_TIMEOUT`.

**pipeline.py:**
- COBOL file extensions expanded from `{.cbl, .CBL, .cob, .COB}` to include `.cobol` and `.COBOL`.
- The `_strip_exec_dli()` function was patched for two edge cases: (1) a comment line containing `EXEC DLI` in a comment was incorrectly triggering the strip; (2) a single-line `EXEC DLI ... END-EXEC` wasn't handled in one pass.

**cobol_source_scanner.py:**
- Previously always applied FIXED-format column rules regardless of what `--format` said. Added proper support for TANDEM and VARIABLE formats (which treat the full line as code, without column restrictions).

**resolver.py:**
- `DFHAID` stub expanded from PF1-PF12 to the full set (PF1-PF24 plus DFHNULL, DFHCLRP, DFHPEN, DFHOPID, DFHMSRE, DFHSTRF, DFHTRIG).
- `DFHBMSCA` stub expanded from 5 fields to the full 33-field BMS attribute byte constant set.
- `CMQMDV` stub expanded from 8 fields to the complete 31-field IBM MQ MQMD structure.
- Copybook directory discovery patterns expanded from 6 to 10, with an `extra_patterns` parameter for custom layouts.

**showcase.py:**
- The call graph section previously used fuzzy `LIKE '%' || name` SQL matching which produced false positives (callee named `ACT` would match `CBACT01C`). Replaced with exact `UPPER(program_id) = UPPER(callee_name)` matching.

After all changes, re-parsing confirmed: still 43/44, same counts, fully portable across machines.

### 4.8 Iteration 5: The Resumable Stub Agent

The parser was stable, but there was still a gap: when applied to a real-world repository (not CardDemo), new unknown proprietary copybooks would appear. Manually writing stubs by hand is tedious and error-prone.

To address this, a **stub proposal agent** was built using the Groq API (OSS120B model). The design priorities were:

- **Resumable**: if the process is interrupted (rate limit, crash), it can resume from the last completed copybook without reprocessing everything.
- **Non-destructive**: proposals are written to an output directory and require manual promotion. The live `_stub_copybooks/` directory is never automatically modified.
- **Deterministic-first**: a template-based approach handles known copybook naming patterns (e.g., anything starting with `CMQ` gets an MQ-style struct). LLM is only called for genuinely unknown copybooks in hybrid mode.

The agent introduced two new SQLite tables (`stub_agent_runs`, `stub_proposals`) for checkpointing, and new CLI flags: `--stub-agent`, `--stub-agent-mode`, `--stub-agent-run-id`, plus rate-limit controls.

Also during this iteration, the source scanner was hardened against a subtle false-positive: the `COPY REPLACING` syntax (`COPY DFHCOMMAREA REPLACING ==:PREFIX:== BY ==WS==.`) caused `REPLACING` to be captured as a copybook name. The scanner now correctly excludes COPY syntax keywords from being treated as names.

### 4.9 Final Results from Stage 2

```
Files parsed OK   : 43  (97.7%)
Parse errors      :  1  (COTRTLIC.cbl — permanent ProLeap grammar limitation)
Programs          : 44
Paragraphs        : 828
Data items        : 13,505
Copy dependencies : 339
Call dependencies : 68
```

All 339 COPY references resolved — zero unresolved. The database is queryable with SQL and can answer questions like "which programs call CBACT01C?" or "which copybook is used by the most programs?" in under a second.

---

## 5. Stage 3 — The Unified Parser (COBOL + JCL + BMS + CICS)

Stage 3 is where the system grew from a COBOL-only parser into a **complete mainframe source analysis pipeline** covering all four source languages used in a real IBM Z application. This is also where the most technically interesting and difficult engineering happened.

### 5.1 Why Stage 3 Was Needed

At the end of Stage 2, we had a complete, working COBOL parser. But a COBOL parser alone is not enough to understand a mainframe application. A real IBM Z application consists of:

1. **COBOL programs** — the business logic
2. **JCL scripts** — the job definitions that run the programs in sequence, with their datasets
3. **BMS mapsets** — the screen layouts for interactive CICS terminal users
4. **CICS statements** — the transaction system calls embedded within COBOL (EXEC CICS READ, SEND MAP, LINK, etc.)

Without JCL, you don't know the execution order or data flow. Without BMS, you don't know what the screens look like. Without CICS extraction, you don't know which programs talk to which screens or files. Stage 3 added all three.

It also addressed a key maintainability problem from Stage 2: the pipeline had grown complex, and a new user needed a simpler entry point. Stage 3 introduced a clean `--verify` mode that checks expected counts against known CardDemo ground truth, making it easy to confirm the parser is working correctly.

### 5.2 New Files Added in Stage 3

Stage 3 started by forking the Stage 2 parser and extending it significantly. The new modules were:

| Module | What It Does |
|--------|--------------|
| `jcl_source_scanner.py` | Deterministic regex-based JCL/PROC parser |
| `jcl_gateway.py` | Java JCL parser (grossvater) lifecycle manager via Py4J |
| `bms_source_scanner.py` | Deterministic BMS mapset parser (DFHMSD, DFHMDI, DFHMDF macros) |
| `cics_source_scanner.py` | Deterministic EXEC CICS statement extractor within COBOL |
| `verify.py` | Verification module comparing parsed counts to expected CardDemo values |
| `cli.py` | Simplified entry point (`-m carddemo_parser`) |

Plus new database tables: `jcl_jobs`, `jcl_steps`, `jcl_dds`, `jcl_libraries`, `jcl_variable_refs`, `bms_maps`, `bms_fields`, `cics_statements`.

### 5.3 The BMS Scanner

BMS source files are IBM assembler macro files, not COBOL. They use three macros: `DFHMSD` (mapset definition), `DFHMDI` (individual map within the mapset), and `DFHMDF` (field within a map). Each macro has keyword parameters like `SIZE`, `POS`, `LENGTH`, `ATTRB`, `COLOR`, `HILIGHT`, `INITIAL`.

The scanner uses regex to identify these macros by name in the assembler source, then parses their parameters. Continuation lines in assembler use a `X` in column 72 to indicate the statement continues on the next line — the scanner handles these by concatenating continued lines before parsing parameters.

For the full CardDemo BMS corpus:
- **21 mapsets** discovered
- **1,164 fields** extracted

Each field record captures: position (row/col), length, attribute byte, colour, highlight, and initial value. This is exactly what you need to reconstruct the screen in any target platform.

### 5.4 The CICS Scanner

CICS calls inside COBOL look like:
```cobol
       EXEC CICS
           SEND MAP('COADM01')
                MAPSET('COADM0A')
                ERASE
       END-EXEC.
```

The scanner identifies `EXEC CICS ... END-EXEC` blocks, extracts the verb (`SEND`, `READ`, `LINK`, `XCTL`, `RETURN`, etc.), and captures the key parameters (`MAP`, `MAPSET`, `PROGRAM`, `FILE`/`DATASET`). This links the COBOL programs to the BMS screen definitions — you can now answer "which COBOL program sends which screen?"

For CardDemo: **240 CICS statements** extracted across all COBOL programs.

### 5.5 The JCL Scanner — Deterministic Layer

JCL (Job Control Language) looks nothing like COBOL. A JCL file defines a **job** with one or more **steps**, each step executing a program or procedure, with **DD statements** that define the input/output datasets.

```jcl
//CBACT01J JOB 1,NOTIFY=&SYSUID
//COBRUN   EXEC IGYWCL
//COBOL.SYSIN  DD DSN=&SYSUID..CBL(CBACT01C),DISP=SHR
//RUN      EXEC PGM=CBACT01C
//STEPLIB   DD DSN=&SYSUID..LOAD,DISP=SHR
```

The deterministic JCL scanner uses a regex state machine to identify:
- JOB cards (job name, class, notify)
- EXEC cards (program name or procedure name, PARM, COND)
- DD cards (dataset name, DISP, SYSOUT, DCB attributes, instream data)
- JCLLIB cards (procedure library order)
- Variable references (`&SYSUID`, `&DSNAME`, etc.)
- Multi-line continuation (lines starting with `//` followed by space)

For the full CardDemo JCL corpus (62 files):
- **153 steps**
- **550 DD statements**
- **8 JCLLIB definitions**
- **194 variable references**

The deterministic scanner became the **baseline** — reliable, fast, zero Java dependencies. It always works. The Java JCL parser (grossvater) was added as a potential upgrade path.

### 5.6 The Java JCL Parser — What It Is and Why It's Hard

The `grossvater/jcl-parser` project is an open-source Java library that uses an ANTLR grammar to parse JCL into a proper parse tree. This is more powerful than regex — it can understand JCL's grammar formally rather than approximating it with patterns.

To use it from Python, a Java gateway shim was built (similar to how ProLeap is wrapped): `java/jcl-gateway/` packages a Py4J entry point around grossvater's grammar and lexer. `carddemo_parser/jcl_gateway.py` manages the gateway lifecycle from Python.

The integration strategy was **Java with deterministic fallback**: try Java first; if Java reports parser errors for a file, fall back to the deterministic scanner for that file. This means:
- Java can be evaluated continuously without breaking anything
- Extraction quality never degrades
- Java error telemetry accumulates over time for grammar improvement

### 5.7 The Grossvater Investigation: What Went Wrong and What Was Fixed

When Java mode was first run against the full CardDemo JCL corpus, the results were alarming:

```
Files scanned: 62
Java error files: 62
Java error total: 12,481
Max errors in one file: 3,910 (CARDFILE.jcl)
Fallback files: 62 (100%)
```

Every single file triggered the fallback. The error count for one file was nearly 4,000. This required a real investigation.

A set of debug scripts was written (`debug_jcl_errors.py`, `aggregate_jcl_error_messages.py`, `debug_jcl_remaining_errors.py`) to probe specific files, correlate error line numbers with actual JCL source, and identify patterns in the errors.

Three root causes were found:

**Root Cause A: Instream mode transition defect**

JCL supports instream data — data cards that appear inline within the JCL, between a `DD *` card and a `/*` delimiter:

```jcl
//SYSIN DD *
some data card here
another data card
/*
```

In the grossvater ANTLR grammar, the `DD *` card switches the lexer into a special "instream mode" where subsequent lines are treated as data rather than JCL statements. The mode switch back to normal JCL should happen when `/*` is seen.

The problem: in `JclBaseLexer.g4`, the rule `END_LINE_COMMENT_NL` (which handles the newline after trailing comments) was switching the lexer back to `DEFAULT_MODE` unconditionally. For CardDemo's `DD *` cards, which frequently have trailing spaces, those spaces were being routed through `MODE_END_LINE_COMMENT`, and the newline was causing an early mode switch back to default. Instream data lines were then being tokenized as regular JCL statements, producing cascading lexical errors.

**Fix:** Updated `END_LINE_COMMENT_NL` to check if the `instreamType` is active before switching modes, and preserve `MODE_INSTREAM_DATA` if it is.

**Root Cause B: Right margin mismatch with CardDemo line formatting**

CardDemo JCL files include sequence numbers in fixed-width position near column 80. With the default right margin settings, the parser was treating these sequence fields as code continuation or parameter text, producing false errors.

**Fix:** Set `rightMargin=132` in the parser options within `JclRecordMapper`. This tells the parser to treat everything past column 132 as sequence/identification area, which eliminates the false positives for CardDemo's line format.

**Root Cause C: Null pointer crashes in the record mapper**

When the parser produced a partial parse tree (due to the mode transition bug above), the `JclRecordMapper.mapInstreamRecord()` method assumed certain nested parser nodes were always present and dereferenced them directly. On partial parse trees, those nodes were null, causing a Java `NullPointerException` that propagated as a gateway crash rather than a structured error response.

**Fix:** Added null guards for `instreamEnd` and `instreamOp` node access in `mapInstreamRecord()`. Now partial parse trees emit a structured error response instead of crashing.

### 5.8 Results After the Grossvater Fixes

```
Files scanned: 62
Java status OK: 62         ← up from 0
Java status error: 0       ← down from 62
Java error total: 259      ← down from 12,481
Max errors in one file: 29 ← down from 3,910
Fallback files: 62         ← still 100% (because errors remain)
```

The gateway no longer crashes. The total error count dropped from 12,481 to 259 — a 98% reduction. But because *any* Java parser errors for a file still trigger the deterministic fallback under the current policy, the extraction results are still coming from the deterministic scanner. The extracted counts match the deterministic baseline exactly (zero mismatches on the parity check).

### 5.9 Why Errors Still Remain (And What They Mean)

The 259 remaining errors are concentrated in specific recurring patterns:

| Error Message | Cause |
|--------------|-------|
| `no viable alternative at input '//*'` | Comment cards in positions grossvater doesn't expect |
| `mismatched input '//' expecting {FIELD_INSTREAM_DELIM, NL, INSTREAM_DATA_LINE}` | Multi-record instream sequences |
| `mismatched input 'NOTIFY' expecting {<EOF>, '//'}` | NOTIFY= parameter on JOB card variants |
| `no viable alternative at input 'DD DISP=SHR,...\n//'` | Certain DD continuation forms |
| `no viable alternative at input 'JCLLIB ORDER=('` | JCLLIB ORDER parameter |

These are **grammar coverage gaps** — JCL constructs that the grossvater ANTLR grammar doesn't yet have rules for. These are not bugs in the integration layer (which we fixed); they are places where the grammar needs to be extended to cover CardDemo-specific JCL patterns.

The integration wiring (mode transitions, right margin, null safety) was fixed. The grammar itself would need incremental additions to handle these constructs.

### 5.10 The Operational Decision: Deterministic Fallback as Default

Given the remaining grammar gaps, the operational policy is:

- **Run Java mode** — it provides useful diagnostic telemetry for grammar improvement
- **Fallback to deterministic** — any file with Java errors uses the deterministic scanner for actual extraction
- **Parity as the quality gate** — the deterministic and Java extraction results must match; zero mismatches confirms the fallback logic is working

This design means Java can be improved incrementally without ever regressing the pipeline's accuracy.

### 5.11 The Verification System

Stage 3 introduced a `--verify` flag that checks the parsed output against known ground-truth counts for the CardDemo corpus:

| Category | Expected | Description |
|----------|----------|-------------|
| JCL jobs | 62 | All `.jcl`, `.JCL`, `.prc`, and `.jcl.template` files |
| JCL steps | 153 | Individual EXEC statements across all jobs |
| DD statements | 550 | Dataset definitions across all steps |
| JCLLIB entries | 8 | Procedure library definitions |
| Variable refs | 194 | `&VARIABLE` style JCL variable references |
| BMS mapsets | 21 | Screen mapset definitions |
| BMS fields | 1,164 | Individual screen field definitions |
| CICS statements | 240 | EXEC CICS blocks across all COBOL programs |

The `--verify-only` flag can be used to check an existing database without re-parsing, which is useful for CI validation.

One known parse error is explicitly allowed: `COTRTLIC.cbl` (the ProLeap grammar limitation from Stage 2 that persists in Stage 3).

### 5.12 The Simplified CLI

Stage 2's `run.py` had accumulated many flags for gateway configuration, stub agent options, showcase settings, etc. For most users, these are irrelevant. Stage 3 added a cleaner entry point:

```bash
python -m carddemo_parser --carddemo-root <path> --verify
```

The module's `__main__.py` exposes a simplified set of flags:

| Flag | Purpose |
|------|---------|
| `--carddemo-root` | Root of the CardDemo repository |
| `--db-path` | Output SQLite database path |
| `--force` | Re-parse already-parsed files |
| `--no-jcl` | Skip JCL/PROC parsing |
| `--no-bms` | Skip BMS parsing |
| `--no-cics` | Skip EXEC CICS extraction |
| `--jcl-parser` | `java` or `deterministic` |
| `--verify` | Check expected CardDemo counts after parsing |
| `--verify-only` | Only verify an existing DB |
| `--allow-parse-error` | Allow known error substrings to pass verification |

The advanced `run.py` still exists for stub agent usage and gateway tuning.

### 5.13 The ASG Export

Stage 3 also added `export_cobol_asg.py` — a script that exports the ProLeap ASG output (the full structured parse tree) to JSON files. This is useful for feeding into downstream LLM analysis, comparison with other parsers, or archival. The export includes the full ASG JSON per program alongside a manifest file listing all programs and their export status.

### 5.14 Stage 3 Final Results

| Category | Count |
|----------|-------|
| COBOL programs parsed | 43/44 (97.7%) |
| JCL files processed | 62/62 (100%) |
| BMS mapsets parsed | 21 |
| BMS fields extracted | 1,164 |
| CICS statements extracted | 240 |
| Paragraphs | 828 |
| Data items | 13,505 |
| Copy dependencies | 339 (all resolved) |
| Call dependencies | 68 |

---

## 6. Current State of the System

### What Exists

The project currently lives in the `Week 3/` directory (referred to as Stage 3 in this document). It is a self-contained Python package that can be run as:

```bash
python -m carddemo_parser --carddemo-root <path>
```

or with the full advanced CLI:

```bash
python run.py [flags]
```

The output is a single SQLite database (`output/carddemo.db`) containing all parsed information across all four source types (COBOL, JCL, BMS, CICS).

### Technology Stack

| Component | Technology | Version / Notes |
|-----------|-----------|-----------------|
| COBOL parser | ProLeap (Java) via Py4J | 4.0.0; one known grammar gap (SEND-PLAIN-TEXT) |
| JCL parser | Deterministic regex scanner (primary) | Fully working, 100% coverage |
| JCL parser | grossvater ANTLR grammar (secondary) | Works but still has CardDemo dialect gaps; always falls back |
| BMS parser | Deterministic regex scanner | 100% coverage |
| CICS extractor | Deterministic regex scanner | 100% coverage |
| Database | SQLite | Built into Python; 12+ tables |
| Stub generation | Groq API (OSS120B) + deterministic templates | Optional, non-destructive |
| Runtime | Python 3.10+, Java 17+ | Windows-first; portable with minor adjustments |

### Repository Structure

```
Week 3/
├── carddemo_parser/           # Main package
│   ├── __main__.py            # Simple CLI entry point
│   ├── cli.py                 # CLI argument definitions
│   ├── pipeline.py            # Orchestrator (COBOL flow)
│   ├── gateway.py             # ProLeap (COBOL) Java bridge
│   ├── jcl_gateway.py         # grossvater (JCL) Java bridge
│   ├── resolver.py            # Copybook discovery + stub writing
│   ├── cobol_source_scanner.py
│   ├── jcl_source_scanner.py
│   ├── bms_source_scanner.py
│   ├── cics_source_scanner.py
│   ├── asg_extractor.py
│   ├── db.py                  # SQLite schema + all operations
│   ├── stub_agent.py          # Resumable LLM-backed stub generator
│   └── verify.py              # Expected count verification
├── java/
│   └── jcl-gateway/           # Maven project for grossvater gateway
├── output/
│   ├── carddemo.db            # Main output database
│   └── cobol_asg/             # Exported ASG JSON files
├── run.py                     # Advanced CLI
└── smoke_test.py              # Quick validation
```

---

## 7. Known Limitations (Across All Stages)

### 7.1 ProLeap Cannot Parse SEND-PLAIN-TEXT

`COTRTLIC.cbl` uses a non-standard CICS verb that ProLeap 4.0.0 does not recognize. This program fails to parse through the Java layer. Its COPY and CALL dependencies are still captured by the source scanner, but its paragraphs and data items are absent from the database. Fix requires a ProLeap upgrade or patching the COBOL source.

### 7.2 EXEC DLI Data Is Lost

When EXEC DLI blocks are stripped from IMS-facing COBOL programs, the IMS call parameters inside those blocks are gone. We know *how many* DLI blocks existed (logged), but not what database segments they accessed. A proper fix would parse the DLI syntax to extract PCB name, call function (GU, GN, ISRT), and segment name into a new `ims_calls` table.

### 7.3 Dynamic CALL Resolution Is Incomplete

COBOL programs can call other programs dynamically: `CALL WS-PROGRAM-NAME`. The program name is in a variable at runtime. The scanner captures these as `call_type = "identifier"` but cannot determine the actual program called without runtime data or symbolic analysis. Dynamic calls cannot be included in the static call graph.

### 7.4 COPY REPLACING Not Parsed

The COBOL `COPY REPLACING` clause substitutes text within the included copybook. The scanner captures the copybook name correctly, but the REPLACING substitutions are not tracked. This means data items from copybooks with REPLACING will appear under their original names, not the substituted names used in the host program.

### 7.5 No Transitive Copybook Dependencies

The dependency graph shows direct COPY statements — if program A copies B, and B copies C, only A→B is recorded, not A→B→C. A transitive closure pass could be added as a post-processing step.

### 7.6 The grossvater JCL Parser Has Grammar Gaps for CardDemo

Despite the fixes to the integration layer (mode transitions, right margin, null safety), the grossvater grammar does not cover all JCL constructs that appear in CardDemo. Comment card handling, some NOTIFY parameter forms, and certain JCLLIB ORDER constructs are not yet parsed. All such files fall back to the deterministic scanner, which does parse them correctly.

### 7.7 Stale Parse Logic (No File Hash Tracking)

The incremental skip logic checks only whether a program record exists in the database, not whether the source file has changed. If a COBOL file is modified after the initial parse, `--force` is required to re-parse it. Adding MD5/SHA256 hash tracking would make this automatic.

### 7.8 Windows Paths in Database

Resolved copybook paths in the database use Windows backslash separators. If the database is used on a Linux system, path string comparisons would fail. The paths are display-only (for auditing), so this is low-risk, but it's a portability concern for cross-platform workflows.

---

## 8. What Can Be Improved

### Near-Term (Low Effort)

1. **Source file hash tracking** — Store MD5/SHA256 at parse time; only re-parse when the hash changes.
2. **Transitive copy dependency closure** — Post-processing SQL pass to compute A→B→C relationships.
3. **REPLACING clause capture** — Extend the COPY regex to capture `REPLACING == ... == BY == ... ==` and store in `copy_deps`.
4. **Severity-based fallback for JCL** — Instead of "any Java error = fallback," classify errors by severity. Warnings should not force fallback; only actual parse-blocking errors should.
5. **Grammar additions for grossvater** — Targeted ANTLR rule additions for the top 5 remaining error patterns (comment cards, NOTIFY, JCLLIB ORDER, certain DD continuations).

### Medium-Term (Moderate Effort)

6. **IMS call analysis** — Parse EXEC DLI blocks instead of stripping them. Extract PCB name, call function, and segment name into a new `ims_calls` table.
7. **ProLeap upgrade** — If a newer ProLeap version supports `SEND-PLAIN-TEXT` and other missing CICS verbs, the one remaining COBOL parse failure would be resolved.
8. **External stub files** — Allow stubs to be provided as `.cpy` files in a user-controlled directory rather than hardcoded in Python source.
9. **Call graph resolution** — After parsing all programs, run a resolution pass to match dynamic `call_deps.callee_name` to `programs.program_id` where possible.
10. **Cross-program data flow** — Use ProLeap's full ASG (not just the structural output) to trace data flow between variables across programs.

### Long-Term (Significant Effort)

11. **Multi-repo support** — Remove the single-root assumption; support parsing multiple repositories in one run with cross-repo dependency tracking.
12. **Migration transformation layer** — Extend the Stage 1 executor agent concept to work against the Stage 3 structured database rather than individual parsed files.
13. **Dead code detection** — Use the call graph and paragraph-level PERFORM tracking to identify programs and paragraphs that are never called.

---

## 9. Stage 4 — The 3-Layer Graph and Multi-Target Generation

### 9.1 The Motivation: Why Move from SQLite to a Graph?

By the end of Stage 3, the pipeline was successfully parsing COBOL, JCL, BMS, and CICS into a local SQLite database. However, this flat relational model presented severe limitations for modernization:

1. **Complex Traversals:** Answering questions like *"Which screen is ultimately affected if I change this file definition?"* requires joining Programs to FileControls, Programs to CICS statements, and CICS statements to BMS Maps. In SQL, this is a rigid, multi-join nightmare.
2. **Lack of Semantic Abstraction:** The SQLite database held raw AST/ASG syntax trees. A program is just a list of statements. To modernize, we need to extract **business components** and **services**, which requires inferring relationships that aren't explicitly written in the code.
3. **No Generation Engine:** Stage 3 stopped at extraction. It provided no automated mechanism to actually translate the extracted knowledge into modernized code.

Stage 4 was initiated to replace SQLite with **Neo4j**, build a multi-layered semantic graph on top of the raw syntax, and orchestrate the automated generation of modern artifacts.

### 9.2 What Was Built: The Neo4j Integration and 3-Layer Architecture

The entire persistence layer was rewritten. `src/neo4j_client.py` and `StatementRepository` replaced the SQLite logic, introducing batched Cypher merges and unique constraints (`schema.initializer.py`) for performance. 

More importantly, the system now constructs a **3-Layer Knowledge Graph**:

**Layer 1 — Statement Layer (Raw Syntax + Semantics)**
- Directly mirrors the JSON AST/ASG structure. Nodes include `Program`, `Paragraph`, `Statement`, `Variable`, and `FileControl`.
- **Enrichment:** The `StatementLayerBuilder` runs Cypher queries to tag raw statements with semantic categories. `READ`/`WRITE` become `IOStatement`; `IF`/`PERFORM` become `ControlStatement`; `MOVE`/`COMPUTE` become `DataMovement`.
- Creates cross-domain edges like `USES_MAPSET` (Program → BMS) and `EXECUTES` (JCL Step → Program).

**Layer 2 — Logical Grouping Layer**
- The `LogicalLayerBuilder` infers business groupings. It calculates a `cohesionScore` for each paragraph based on variable usage density.
- It groups related paragraphs into `Section` nodes based on legacy naming conventions (e.g., grouping `1000-ACCTFILE-GET-NEXT` and `1100-DISPLAY-ACCT` into `Section 1xxx`).
- Creates `ScreenFlow` nodes to link Programs to the BMS maps they render.

**Layer 3 — Component Layer (Service Oriented Architecture)**
- The `ComponentLayerBuilder` promotes highly cohesive Layer 2 `Section` nodes into abstract `Component` nodes.
- Components are linked to abstract `Service` and `Interface` nodes, mapping physical files (`FileControl`) to logical contracts.
- This layer represents the target modernized architecture, completely decoupled from COBOL syntax.

### 9.3 What Was Built: The Multi-Target Generation Engine

With Layer 3 established, the pipeline shifts from ingestion to generation. The `GenerationOrchestrator` queries Neo4j for all Components and builds Pydantic projections (`ComponentProjection`, `VariableProjection`, `InterfaceProjection`).

These projections are routed to four distinct generators:

1. **Java Generator:** Emits modern, Spring-Boot-like Java Services. COBOL variables are typed using their PIC clauses and converted to class fields. Paragraphs are mapped to private methods, complete with semantic comments indicating their operations (e.g., I/O, Invocation).
2. **LDL+ Generator:** Emits AB Suite LDL+ definitions, mapping variables to Local data items and capturing file interfaces and operational methods.
3. **PModel XML Generator:** Constructs a strict, schema-validated XML representation of the component (DataItems, Interfaces, Methods). Validated strictly against `pmodel.xsd` using `lxml`.
4. **Documentation Generator:** Uses Jinja2 templates to emit Markdown architecture documents, generating data dictionaries and paragraph operation tables.

### 9.4 Key Challenges and Fixes in Stage 4

**The Naming Collision Bug:** 
Initially, components generated across different programs were overwriting each other because they shared generic section names (e.g., `Component_0xxx`). This was fixed in the `ComponentLayerBuilder` by prepending the `programId` to ensure unique identifiers across the graph (e.g., `Component_0xxx_CBACT04C`).

**Orphan Statement Validation:** 
The `GraphValidator` was initially too aggressive, halting the pipeline when it found statements not linked to a paragraph (which happens naturally with terminal `STOP RUN` or `EXIT` statements). The validation was converted to a non-blocking warning mode to preserve pipeline stability.

**Assign To Resolution:**
Early JSON extractions mapped file `ASSIGN TO` clauses to internal ProLeap Java pointers (e.g., `CallValueStmtImpl@...`). The extraction configuration was updated to successfully resolve these to actual DD names (e.g., `TCATBALF`, `XREFFILE`), providing accurate file mappings in the generated Java handlers and Documentation.

### 9.5 Results from Stage 4

The pipeline successfully processes the CardDemo application through all phases, resulting in:
- A fully populated Neo4j Graph with constraints and indexes.
- **384 modernized artifacts generated** (96 components × 4 targets).
- 100% successful XSD validation for all generated PModel XML files.
- A 1:1 structural mapping between the original COBOL paragraphs/variables and the generated Java methods/fields.

### 9.6 Known Limitations (Stage 4)

**Missing True Control and Data Flow:** 
While the graph correctly captures variables, file controls, and sequential statement flows (`FLOWS_TO`), it lacks explicit inter-paragraph control flow and data flow. 

When ProLeap parses a `PERFORM 1000-READ`, or a `MOVE A TO B`, the current JSON serialization outputs a Java object reference (e.g., `PerformStatementImpl@5f70b7f5`) in the `raw_text` field instead of extracting the target paragraph (`1000-READ`) or the source/target operands (`A`, `B`). 

Consequently, the Neo4j graph cannot presently draw `CALLS` edges between paragraphs, nor `READS`/`WRITES` edges between statements and variables. Resolving this requires updating the Java extraction layer to explicitly serialize statement operands into the JSON ASG before ingestion.

---

