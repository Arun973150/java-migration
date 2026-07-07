# BMS English Documentation: COBIL0A

## 1. Screen Purpose

`COBIL0A` is a BMS screen map in mapset `COBIL00` with map name `COBIL0A`. It is associated with program `COBIL00C` and contains 24 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 2 editable input field(s), 8 output/display field(s), and 14 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACTIDIN` at row 6, column 21, length 11: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `CONFIRM` at row 15, column 60, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `CURBAL` at row 11, column 32, length 14: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Bill Payment, Enter Acct ID:, -----------------------, Your current balance is:, Do you want to pay your balance now. Please con firm:, (Y/N), ENTER=Continue  F3=Back  F4=Clear
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COBIL00C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
