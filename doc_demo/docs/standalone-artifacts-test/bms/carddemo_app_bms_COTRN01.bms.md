# BMS File English Documentation: COTRN01.bms

## 1. Executive Summary

`COTRN01.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COTRN01. The extracted data links this file to COTRN01C and transaction id(s) CT01. The business-facing title is Transaction View.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COTRN01.bms`
- Mapset names: COTRN01
- Associated programs: COTRN01C
- Transaction ids: CT01
- Business name/title: Transaction View
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COTRN1A` / map `COTRN1A`: 56 total field(s), 1 input, 20 output, 35 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 1 editable field occurrence(s) and 20 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COTRN01C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, View Transaction, Enter Tran ID:, -----------------------, Transaction ID:, Card Number:, Type CD:, Category CD:, Source:, Description:, Amount:, Orig Date:, Proc Date:, Merchant ID:, Merchant Name:, Merchant City:, Merchant Zip:
- Color usage: BLUE (21), TURQUOISE (14), YELLOW (3), NEUTRAL (2), GREEN (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Fetch F3=Back F4=Clear F5=Browse Tran.

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
