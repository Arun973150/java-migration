# BMS English Documentation: CTRTUPA

## 1. Screen Purpose

`CTRTUPA` is a BMS screen map in mapset `COTRTUP` with map name `CTRTUPA`. It is associated with program `COTRTUPC` and contains 25 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 2 editable input field(s), 13 output/display field(s), and 10 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `TRTYPCD` at row 12, column 26, length 2: terminal input field with attributes `(IC,UNPROT)`.
- `TRTYDSC` at row 14, column 26, length 50: terminal input field with attributes `(UNPROT)`.

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
- `FKEY04` at row 24, column 23, length 9: display value initialized as ``.
- `FKEY05` at row 24, column 33, length 8: display value initialized as ``.
- `FKEY06` at row 24, column 43, length 6: display value initialized as ``.
- `FKEY12` at row 24, column 69, length 10: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Maintain Transaction Type, Transaction Type  :, Description       :
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COTRTUPC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
