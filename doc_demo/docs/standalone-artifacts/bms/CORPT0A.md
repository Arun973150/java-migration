# BMS English Documentation: CORPT0A

## 1. Screen Purpose

`CORPT0A` is a BMS screen map in mapset `CORPT00` with map name `CORPT0A`. It is associated with program `CORPT00C` and contains 42 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 10 editable input field(s), 7 output/display field(s), and 25 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `MONTHLY` at row 7, column 10, length 1: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `YEARLY` at row 9, column 10, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `CUSTOM` at row 11, column 10, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SDTMM` at row 13, column 29, length 2: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `SDTDD` at row 13, column 34, length 2: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `SDTYYYY` at row 13, column 39, length 4: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `EDTMM` at row 14, column 29, length 2: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `EDTDD` at row 14, column 34, length 2: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `EDTYYYY` at row 14, column 39, length 4: terminal input field with attributes `(FSET,NORM,NUM,UNPROT)`.
- `CONFIRM` at row 19, column 66, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Transaction Reports, Monthly (Current Month), Yearly (Current Year), Custom (Date Range), Start Date :, /, /, (MM/DD/YYYY), End Date :, /, /, (MM/DD/YYYY), The Report will be submitted for printing. Plea se confirm:, (Y/N), ENTER=Continue  F3=Back
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `CORPT00C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
