# BMS English Documentation: COTRN2A

## 1. Screen Purpose

`COTRN2A` is a BMS screen map in mapset `COTRN02` with map name `COTRN2A`. It is associated with program `COTRN02C` and contains 61 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 14 editable input field(s), 7 output/display field(s), and 40 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACTIDIN` at row 6, column 21, length 11: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `CARDNIN` at row 6, column 55, length 16: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TTYPCD` at row 10, column 15, length 2: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TCATCD` at row 10, column 36, length 4: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRNSRC` at row 10, column 54, length 10: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TDESC` at row 12, column 19, length 60: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRNAMT` at row 14, column 14, length 12: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TORIGDT` at row 14, column 42, length 10: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TPROCDT` at row 14, column 68, length 10: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `MID` at row 16, column 19, length 9: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `MNAME` at row 16, column 48, length 30: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `MCITY` at row 18, column 21, length 25: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `MZIP` at row 18, column 67, length 10: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `CONFIRM` at row 21, column 63, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Add Transaction, Enter Acct #:, (or), Card #:, -----------------------, Type CD:, Category CD:, Source:, Description:, Amount:, Orig Date:, Proc Date:, (-99999999.99), (YYYY-MM-DD), (YYYY-MM-DD), Merchant ID:, Merchant Name:, Merchant City:, Merchant Zip:, You are about to add this transaction. Please c onfirm :, (Y/N)
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COTRN02C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
