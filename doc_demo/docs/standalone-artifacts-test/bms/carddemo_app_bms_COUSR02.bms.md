# BMS File English Documentation: COUSR02.bms

## 1. Executive Summary

`COUSR02.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COUSR02. The extracted data links this file to COUSR02C and transaction id(s) CU02. The business-facing title is Update User.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COUSR02.bms`
- Mapset names: COUSR02
- Associated programs: COUSR02C
- Transaction ids: CU02
- Business name/title: Update User
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COUSR2A` / map `COUSR2A`: 28 total field(s), 5 input, 7 output, 16 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 5 editable field occurrence(s) and 7 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COUSR02C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Update User, Enter User ID:, *********************************************** DFHMDF ATTRB=(ASKIP,NORM), COLOR=TURQUOISE, LENGTH=11, POS=(11,6), INITIAL=, Last Name:, Password:, (8 Char), User Type:, (A=Admin, U=User), ENTER=Fetch  F3=Save&&Exit  F4=Clear  F5=Save F12=Cancel
- Color usage: BLUE (10), GREEN (7), YELLOW (4), TURQUOISE (3), NEUTRAL (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Fetch F3=Save&&Exit F4=Clear F5=Save F12=Cancel

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
