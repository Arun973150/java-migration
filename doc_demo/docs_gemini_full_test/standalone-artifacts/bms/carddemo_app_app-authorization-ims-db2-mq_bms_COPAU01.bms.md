# BMS File English Documentation: COPAU01.bms

## 1. Executive Summary

`COPAU01.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COPAU01. The extracted data links this file to COPAUS1C and transaction id(s) CPVD. The business-facing title is Pending Authorization Details.

## 2. File and Mapset Context

- Source file: `carddemo\app\app-authorization-ims-db2-mq\bms\COPAU01.bms`
- Mapset names: COPAU01
- Associated programs: COPAUS1C
- Transaction ids: CPVD
- Business name/title: Pending Authorization Details
- Business description: IMS-DB2-MQ: Pending Authorizations
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COPAU1A` / map `COPAU1A`: 54 total field(s), 0 input, 27 output, 27 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 0 editable field occurrence(s) and 27 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COPAUS1C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran:, Date:, Prog:, Time:, View Authorization Details, Card #:, Auth Date:, Auth Time:, Auth Resp:, Resp Reason:, Auth Code:, Amount:, POS Entry Mode:, Source   :, MCC Code:, Card Exp. Date:, Auth Type:, Tran Id:, Match Status:, Fraud Status:
- Color usage: BLUE (22), TURQUOISE (20), PINK (4), YELLOW (3), RED (3), NEUTRAL (2)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: F3=Back F5=Mark/Remove Fraud F8=Next Auth

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
