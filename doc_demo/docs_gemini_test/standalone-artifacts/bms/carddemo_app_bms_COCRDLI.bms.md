# BMS File English Documentation: COCRDLI.bms

## 1. Executive Summary

`COCRDLI.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COCRDLI. The extracted data links this file to COCRDLIC and transaction id(s) CCLI. The business-facing title is Credit Card List.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COCRDLI.bms`
- Mapset names: COCRDLI
- Associated programs: COCRDLIC
- Transaction ids: CCLI
- Business name/title: Credit Card List
- Business description: not present in extracted data
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CCRDLIA` / map `CCRDLIA`: 72 total field(s), 2 input, 43 output, 27 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 2 editable field occurrence(s) and 43 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COCRDLIC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, List Credit Cards, Page, Account Number    :, Credit Card Number:, Select, Account Number, Card Number, Active, ------, ---------------, --------, F3=Exit F7=Backward  F8=Forward
- Color usage: DEFAULT (34), NEUTRAL (10), BLUE (8), TURQUOISE (3), YELLOW (2), GREEN (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: F3=Exit F7=Backward F8=Forward

### Repeating Regions

- Field family `ACCTNO` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 11-17.
- Field family `CRDNUM` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 11-17.
- Field family `CRDSEL` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 11-17.
- Field family `CRDSTS` repeats 7 time(s) with suffixes 1, 2, 3, 4, 5, 6, 7 across rows 11-17.
- Field family `CRDSTP` repeats 6 time(s) with suffixes 2, 3, 4, 5, 6, 7 across rows 12-17.
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
