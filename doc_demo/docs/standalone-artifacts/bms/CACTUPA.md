# BMS English Documentation: CACTUPA

## 1. Screen Purpose

`CACTUPA` is a BMS screen map in mapset `COACTUP` with map name `CACTUPA`. It is associated with program `COACTUPC` and contains 128 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 43 editable input field(s), 11 output/display field(s), and 74 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACCTSID` at row 5, column 38, length 11: terminal input field with attributes `(IC,UNPROT)`.
- `ACSTTUS` at row 5, column 70, length 1: terminal input field with attributes `(UNPROT)`.
- `OPNYEAR` at row 6, column 17, length 4: terminal input field with attributes `(FSET,UNPROT)`.
- `OPNMON` at row 6, column 24, length 2: terminal input field with attributes `(UNPROT)`.
- `OPNDAY` at row 6, column 29, length 2: terminal input field with attributes `(UNPROT)`.
- `ACRDLIM` at row 6, column 61, length 15: terminal input field with attributes `(FSET,UNPROT)`.
- `EXPYEAR` at row 7, column 17, length 4: terminal input field with attributes `(UNPROT)`.
- `EXPMON` at row 7, column 24, length 2: terminal input field with attributes `(UNPROT)`.
- `EXPDAY` at row 7, column 29, length 2: terminal input field with attributes `(UNPROT)`.
- `ACSHLIM` at row 7, column 61, length 15: terminal input field with attributes `(FSET,UNPROT)`.
- `RISYEAR` at row 8, column 17, length 4: terminal input field with attributes `(UNPROT)`.
- `RISMON` at row 8, column 24, length 2: terminal input field with attributes `(UNPROT)`.
- `RISDAY` at row 8, column 29, length 2: terminal input field with attributes `(UNPROT)`.
- `ACURBAL` at row 8, column 61, length 15: terminal input field with attributes `(FSET,UNPROT)`.
- `ACRCYCR` at row 9, column 61, length 15: terminal input field with attributes `(FSET,UNPROT)`.
- `AADDGRP` at row 10, column 23, length 10: terminal input field with attributes `(UNPROT)`.
- `ACRCYDB` at row 10, column 61, length 15: terminal input field with attributes `(FSET,UNPROT)`.
- `ACSTNUM` at row 12, column 23, length 9: terminal input field with attributes `(UNPROT)`.
- `ACTSSN1` at row 12, column 55, length 3: terminal input field with attributes `(UNPROT)`.
- `ACTSSN2` at row 12, column 61, length 2: terminal input field with attributes `(UNPROT)`.
- `ACTSSN3` at row 12, column 66, length 4: terminal input field with attributes `(UNPROT)`.
- `DOBYEAR` at row 13, column 23, length 4: terminal input field with attributes `(UNPROT)`.
- `DOBMON` at row 13, column 30, length 2: terminal input field with attributes `(UNPROT)`.
- `DOBDAY` at row 13, column 35, length 2: terminal input field with attributes `(UNPROT)`.
- `ACSTFCO` at row 13, column 62, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSFNAM` at row 15, column 1, length 25: terminal input field with attributes `(UNPROT)`.
- `ACSMNAM` at row 15, column 28, length 25: terminal input field with attributes `(UNPROT)`.
- `ACSLNAM` at row 15, column 55, length 25: terminal input field with attributes `(UNPROT)`.
- `ACSADL1` at row 16, column 10, length 50: terminal input field with attributes `(UNPROT)`.
- `ACSSTTE` at row 16, column 73, length 2: terminal input field with attributes `(UNPROT)`.
- `ACSADL2` at row 17, column 10, length 50: terminal input field with attributes `(UNPROT)`.
- `ACSZIPC` at row 17, column 73, length 5: terminal input field with attributes `(UNPROT)`.
- `ACSCITY` at row 18, column 10, length 50: terminal input field with attributes `(UNPROT)`.
- `ACSCTRY` at row 18, column 73, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSPH1A` at row 19, column 10, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSPH1B` at row 19, column 14, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSPH1C` at row 19, column 18, length 4: terminal input field with attributes `(UNPROT)`.
- `ACSGOVT` at row 19, column 58, length 20: terminal input field with attributes `(UNPROT)`.
- `ACSPH2A` at row 20, column 10, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSPH2B` at row 20, column 14, length 3: terminal input field with attributes `(UNPROT)`.
- `ACSPH2C` at row 20, column 18, length 4: terminal input field with attributes `(UNPROT)`.
- `ACSEFTC` at row 20, column 41, length 10: terminal input field with attributes `(UNPROT)`.
- `ACSPFLG` at row 20, column 78, length 1: terminal input field with attributes `(UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `INFOMSG` at row 22, column 23, length 45: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.
- `FKEYS` at row 24, column 1, length 21: display value initialized as ``.
- `FKEY05` at row 24, column 23, length 7: display value initialized as ``.
- `FKEY12` at row 24, column 31, length 10: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Update Account, Account Number :, Active Y/N:, Opened :, -, -, Credit Limit        :, Expiry :, -, -, Cash credit Limit   :, Reissue:, -, -, Current Balance     :, Current Cycle Credit:, Account Group:, Current Cycle Debit :, Customer Details, Customer id  :, SSN:
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COACTUPC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
