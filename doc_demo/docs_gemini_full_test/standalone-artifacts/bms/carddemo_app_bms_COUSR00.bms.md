# BMS File English Documentation: COUSR00.bms

## 1. Executive Summary

`COUSR00.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COUSR00. The extracted data links this file to COUSR00C and transaction id(s) CU00. The business-facing title is List Users.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COUSR00.bms`
- Mapset names: COUSR00
- Associated programs: COUSR00C
- Transaction ids: CU00
- Business name/title: List Users
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COUSR0A` / map `COUSR0A`: 89 total field(s), 11 input, 48 output, 30 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 11 editable field occurrence(s) and 48 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COUSR00C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, List Users, Page:, Search User ID:, Sel, User ID, First Name, Last Name, Type, ---, --------, --------------------, ----, ENTER=Continue  F3=Back  F7=Backward  F8=Forwar d
- Color usage: BLUE (49), NEUTRAL (12), GREEN (11), YELLOW (3), TURQUOISE (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Continue F3=Back F7=Backward F8=Forward

### Repeating Regions

- Field family `FNAME` repeats 10 time(s) with suffixes 01, 02, 03, 04, 05, 06, 07, 08 across rows 10-19.
- Field family `LNAME` repeats 10 time(s) with suffixes 01, 02, 03, 04, 05, 06, 07, 08 across rows 10-19.
- Field family `SEL` repeats 10 time(s) with suffixes 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008 across rows 10-19.
- Field family `USRID` repeats 10 time(s) with suffixes 01, 02, 03, 04, 05, 06, 07, 08 across rows 10-19.
- Field family `UTYPE` repeats 10 time(s) with suffixes 01, 02, 03, 04, 05, 06, 07, 08 across rows 10-19.
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
