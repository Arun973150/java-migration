# BMS File English Documentation: COACTUP.bms

## 1. Executive Summary

`COACTUP.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COACTUP. The extracted data links this file to COACTUPC and transaction id(s) CAUP. The business-facing title is Account Update.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COACTUP.bms`
- Mapset names: COACTUP
- Associated programs: COACTUPC
- Transaction ids: CAUP
- Business name/title: Account Update
- Business description: not present in extracted data
- DFHMSD controls: LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `CACTUPA` / map `CACTUPA`: 128 total field(s), 43 input, 11 output, 74 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 43 editable field occurrence(s) and 11 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COACTUPC.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, Update Account, Account Number :, Active Y/N:, Opened :, -, Credit Limit        :, Expiry :, Cash credit Limit   :, Reissue:, Current Balance     :, Current Cycle Credit:, Account Group:, Current Cycle Debit :, Customer Details, Customer id  :, SSN:
- Color usage: TURQUOISE (28), BLUE (8), YELLOW (5), NEUTRAL (3), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Process F3=Exit, F5=Save, F12=Cancel

### Repeating Regions

- Field family `ACTSSN` repeats 3 time(s) with suffixes 1, 2, 3 across rows 12-12.
- Field family `ACSADL` repeats 2 time(s) with suffixes 1, 2 across rows 16-17.
- Field family `FKEY` repeats 2 time(s) with suffixes 05, 12 across rows 24-24.
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
