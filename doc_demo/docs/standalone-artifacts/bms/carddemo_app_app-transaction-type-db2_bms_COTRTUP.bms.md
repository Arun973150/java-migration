# BMS File English Documentation: COTRTUP.bms

## 1. Executive Summary

`COTRTUP.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COTRTUP. The extracted data links this file to COTRTUPC and transaction id(s) CTTU. The business-facing title is Tran Type add/edit.

## 2. File and Mapset Context

- Source file: `carddemo\app\app-transaction-type-db2\bms\COTRTUP.bms`
- Mapset names: COTRTUP
- Associated programs: COTRTUPC
- Transaction ids: CTTU
- Business name/title: Tran Type add/edit
- Business description: Db2: Transaction Type Mgmt
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CTRTUPA` / map `CTRTUPA`: 25 total field(s), 2 input, 13 output, 10 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 2 editable field occurrence(s) and 13 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COTRTUPC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Maintain Transaction Type, Transaction Type  :, Description       :
- Color usage: BLUE (8), YELLOW (7), NEUTRAL (2), TURQUOISE (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Process F3=Exit, F4=Delete, F5=Save, F6=Add, F12=Cancel

### Repeating Regions

- Field family `FKEY` repeats 4 time(s) with suffixes 04, 05, 06, 12 across rows 24-24.
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
