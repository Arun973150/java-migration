# BMS File English Documentation: COUSR01.bms

## 1. Executive Summary

`COUSR01.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COUSR01. The extracted data links this file to COUSR01C and transaction id(s) CU01. The business-facing title is Add User.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COUSR01.bms`
- Mapset names: COUSR01
- Associated programs: COUSR01C
- Transaction ids: CU01
- Business name/title: Add User
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COUSR1A` / map `COUSR1A`: 28 total field(s), 5 input, 7 output, 16 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 5 editable field occurrence(s) and 7 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COUSR01C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Add User, First Name:, Last Name:, User ID:, (8 Char), Password:, User Type:, (A=Admin, U=User), ENTER=Add User  F3=Back  F4=Clear  F12=Exit
- Color usage: BLUE (11), GREEN (6), TURQUOISE (5), YELLOW (3), NEUTRAL (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Add User F3=Back F4=Clear F12=Exit

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
