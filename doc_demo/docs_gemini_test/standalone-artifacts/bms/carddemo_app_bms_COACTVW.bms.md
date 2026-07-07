# BMS File English Documentation: COACTVW.bms

## 1. Executive Summary

`COACTVW.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COACTVW. The extracted data links this file to COACTVWC and transaction id(s) CAVW. The business-facing title is Account View.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COACTVW.bms`
- Mapset names: COACTVW
- Associated programs: COACTVWC
- Transaction ids: CAVW
- Business name/title: Account View
- Business description: not present in extracted data
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CACTVWA` / map `CACTVWA`: 100 total field(s), 1 input, 36 output, 63 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 1 editable field occurrence(s) and 36 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COACTVWC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, View Account, Account Number :, Active Y/N:, Opened:, Credit Limit        :, Expiry:, Cash credit Limit   :, Reissue:, Current Balance     :, Current Cycle Credit:, Account Group:, Current Cycle Debit :, Customer Details, Customer id  :, SSN:, Date of birth:
- Color usage: TURQUOISE (29), BLUE (8), NEUTRAL (3), YELLOW (2), GREEN (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: F3=Exit

### Repeating Regions

- Field family `ACSADL` repeats 2 time(s) with suffixes 1, 2 across rows 16-17.
- Field family `ACSPHN` repeats 2 time(s) with suffixes 1, 2 across rows 19-20.
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
