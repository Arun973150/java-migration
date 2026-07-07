# BMS File English Documentation: COADM01.bms

## 1. Executive Summary

`COADM01.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COADM01. The extracted data links this file to COADM01C and transaction id(s) CA00. The business-facing title is Admin Menu.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COADM01.bms`
- Mapset names: COADM01
- Associated programs: COADM01C
- Transaction ids: CA00
- Business name/title: Admin Menu
- Business description: Db2: Transaction Type Mgmt
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COADM1A` / map `COADM1A`: 28 total field(s), 1 input, 19 output, 8 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 1 editable field occurrence(s) and 19 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COADM01C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Admin Menu, Please select an option :, ENTER=Continue  F3=Exit
- Color usage: BLUE (20), YELLOW (3), NEUTRAL (1), TURQUOISE (1), GREEN (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Continue F3=Exit

### Repeating Regions

- Field family `OPTN` repeats 12 time(s) with suffixes 001, 002, 003, 004, 005, 006, 007, 008 across rows 6-17.
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
