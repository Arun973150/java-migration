# BMS File English Documentation: COPAU00.bms

## 1. Executive Summary

`COPAU00.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COPAU00. The extracted data links this file to COPAUS0C and transaction id(s) CPVS. The business-facing title is Pending Authorization Summary.

## 2. File and Mapset Context

- Source file: `carddemo\app\app-authorization-ims-db2-mq\bms\COPAU00.bms`
- Mapset names: COPAU00
- Associated programs: COPAUS0C
- Transaction ids: CPVS
- Business name/title: Pending Authorization Summary
- Business description: IMS-DB2-MQ: Pending Authorizations
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COPAU0A` / map `COPAU0A`: 104 total field(s), 6 input, 56 output, 42 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 6 editable field occurrence(s) and 56 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COPAUS0C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, View Authorizations, Search Acct Id:, Name:, Customer Id:, Acct Status:, PH:, Approval # :, Decline #:, Credit Lim:, Cash Lim:, Appr Amt:, Credit Bal:, Cash Bal:, Decl Amt:, Sel, Transaction ID
- Color usage: BLUE (57), NEUTRAL (18), DEFAULT (7), GREEN (6), YELLOW (3), TURQUOISE (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Continue F3=Back F7=Backward F8=Forward

### Repeating Regions

- Field family `PAMT` repeats 5 time(s) with suffixes 001, 002, 003, 004, 005 across rows 16-20.
- Field family `PAPRV` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `PDATE` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `PSTAT` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `PTIME` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `PTYPE` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `SEL` repeats 5 time(s) with suffixes 0001, 0002, 0003, 0004, 0005 across rows 16-20.
- Field family `TRNID` repeats 5 time(s) with suffixes 01, 02, 03, 04, 05 across rows 16-20.
- Field family `ADDR` repeats 2 time(s) with suffixes 001, 002 across rows 7-8.
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
