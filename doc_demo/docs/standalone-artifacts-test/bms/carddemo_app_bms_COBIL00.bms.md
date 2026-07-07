# BMS File English Documentation: COBIL00.bms

## 1. Executive Summary

`COBIL00.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COBIL00. The extracted data links this file to COBIL00C and transaction id(s) CB00. The business-facing title is Bill Payment.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COBIL00.bms`
- Mapset names: COBIL00
- Associated programs: COBIL00C
- Transaction ids: CB00
- Business name/title: Bill Payment
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COBIL0A` / map `COBIL0A`: 24 total field(s), 2 input, 8 output, 14 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 2 editable field occurrence(s) and 8 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COBIL00C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Bill Payment, Enter Acct ID:, -----------------------, Your current balance is:, Do you want to pay your balance now. Please con firm:, (Y/N), ENTER=Continue  F3=Back  F4=Clear
- Color usage: BLUE (9), YELLOW (4), GREEN (3), NEUTRAL (2), TURQUOISE (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Continue F3=Back F4=Clear

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
