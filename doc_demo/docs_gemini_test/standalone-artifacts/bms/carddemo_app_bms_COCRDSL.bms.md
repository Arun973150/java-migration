# BMS File English Documentation: COCRDSL.bms

## 1. Executive Summary

`COCRDSL.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COCRDSL. The extracted data links this file to COCRDLIC, COCRDSLC and transaction id(s) CCDL. The business-facing title is Credit Card View.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COCRDSL.bms`
- Mapset names: COCRDSL
- Associated programs: COCRDLIC, COCRDSLC
- Transaction ids: CCDL
- Business name/title: Credit Card View
- Business description: not present in extracted data
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CCRDSLA` / map `CCRDSLA`: 31 total field(s), 2 input, 13 output, 16 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 2 editable field occurrence(s) and 13 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COCRDLIC, COCRDSLC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, View Credit Card Detail, Account Number    :, Card Number       :, Name on card      :, Card Active Y/N   :, Expiry Date       :, /
- Color usage: BLUE (8), TURQUOISE (5), YELLOW (3), NEUTRAL (2), DEFAULT (2), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Search Cards F3=Exit

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
