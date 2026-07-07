# BMS File English Documentation: COTRTLI.bms

## 1. Executive Summary

`COTRTLI.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COTRTLI. The extracted data links this file to COTRTLIC and transaction id(s) CTLI. The business-facing title is Tran Type list/update/delete.

## 2. File and Mapset Context

- Source file: `carddemo\app\app-transaction-type-db2\bms\COTRTLI.bms`
- Mapset names: COTRTLI
- Associated programs: COTRTLIC
- Transaction ids: CTLI
- Business name/title: Tran Type list/update/delete
- Business description: Db2: Transaction Type Mgmt
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CTRTLIA` / map `CTRTLIA`: 81 total field(s), 9 input, 31 output, 41 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 9 editable field occurrence(s) and 31 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COTRTLIC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Maintain Transaction Type, Page, Type Filter:, Description Filter:, Select, Type, Description, ------, -----, ---
- Color usage: DEFAULT (24), BLUE (8), NEUTRAL (8), TURQUOISE (7), YELLOW (2), GREEN (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: F2=Add, F3=Exit, F7=Page Up, F8=Page Dn, F10=Save

### Repeating Regions

- Field family `TRTSEL` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 12-18.
- Field family `TRTTYP` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 12-18.
- Field family `TRTYPD` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 12-18.
- Field family `BUTNF` repeats 5 time(s) with suffixes 02, 03, 07, 08, 10 across rows 24-24.
- Field family `TITLE` repeats 2 time(s) with suffixes 01, 02 across rows 1-2.

## 6. Validation and Navigation Considerations

The BMS file alone describes screen structure, not the full navigation logic. Confirm SEND MAP, RECEIVE MAP, PF-key handling, and validation behavior in the associated CICS programs before migration.
- Review COPY-book usage and SEND/RECEIVE MAP statements in the linked COBOL programs to validate field direction and paging behavior.

## 7. Modernization Guidance

- Treat this BMS file as a UI contract for one terminal interaction area or flow segment.
- Map input fields to modern form controls and output fields to read-only display elements.
- Preserve repeated row groups as table or list components rather than flattening them into unrelated fields.
- Preserve screen grouping, command-key prompts, and labels when designing the replacement web or API-driven UI.
- Validate transaction routing, per-map behavior, paging/navigation, and error-message handling in the linked programs.
