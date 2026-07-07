# BMS File English Documentation: COUSR03.bms

## 1. Executive Summary

`COUSR03.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COUSR03. The extracted data links this file to COUSR03C and transaction id(s) CU03. The business-facing title is Delete User.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COUSR03.bms`
- Mapset names: COUSR03
- Associated programs: COUSR03C
- Transaction ids: CU03
- Business name/title: Delete User
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COUSR3A` / map `COUSR3A`: 25 total field(s), 1 input, 10 output, 14 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 1 editable field occurrence(s) and 10 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COUSR03C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Delete User, Enter User ID:, *********************************************** DFHMDF ATTRB=(ASKIP,NORM), COLOR=TURQUOISE, LENGTH=11, POS=(11,6), INITIAL=, Last Name:, User Type:, (A=Admin, U=User), ENTER=Fetch  F3=Back  F4=Clear  F5=Delete
- Color usage: BLUE (12), YELLOW (4), GREEN (3), TURQUOISE (2), NEUTRAL (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Fetch F3=Back F4=Clear F5=Delete

### Repeating Regions

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
