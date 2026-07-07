# BMS File English Documentation: COSGN00.bms

## 1. Executive Summary

`COSGN00.bms` is a BMS source file that defines 1 extracted map(s)/screen(s) across mapset(s) COSGN00. The extracted data links this file to COSGN00C and transaction id(s) CC00. The business-facing title is Signon Screen.

## 2. File and Mapset Context

- Source file: `carddemo\app\bms\COSGN00.bms`
- Mapset names: COSGN00
- Associated programs: COSGN00C
- Transaction ids: CC00
- Business name/title: Signon Screen
- Business description: not present in extracted data
- DFHMSD controls: CTRL=(ALARM,FREEKB), EXTATT=YES, LANG=COBOL, MODE=INOUT, STORAGE=AUTO, TIOAPFX=YES, TYPE=&&SYSPARM

## 3. Map-by-Map Structure

- `COSGN0A` / map `COSGN0A`: 37 total field(s), 2 input, 9 output, 26 label, rows 1-24, size (24,80).

## 4. User Interaction Flow

Across the file, the extracted maps expose 2 editable field occurrence(s) and 9 display field occurrence(s). This indicates the file supports interactive CICS-style terminal flows where users enter values into unprotected fields and receive program-populated output fields on the returned map.

Repository evidence should be used to confirm the live terminal flow. Linked COBOL programs include COSGN00C.

## 5. Shared Field and Layout Patterns

- Representative labels: Tran :, Date :, Prog :, Time :, AppID:, SysID:, This is a Credit Card Demo Application for Main frame Modernization, +========================================+, |%%%%%%%  NATIONAL RESERVE NOTE  %%%%%%%%|, |%(1)  THE UNITED STATES OF KICSLAND (1)%|, |%$$              ___       ********  $$%|, |%$    {x}       (o o)                 $%|, |%$     ******  (  V  )      O N E     $%|, |%(1)          ---m-m---             (1)%|, |%%~~~~~~~~~~~ ONE DOLLAR ~~~~~~~~~~~~~%%|, Type your User ID and Password, then press ENTE R:, User ID     :, (8 Char), Password    :, ENTER=Sign-on  F3=Exit
- Color usage: BLUE (23), GREEN (4), YELLOW (3), TURQUOISE (3), NEUTRAL (1), RED (1)
- Preserve field lengths, row/column positions, and attribute flags because they define the terminal contract.
- Command-key/footer hints: ENTER=Signon F3=Exit

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
