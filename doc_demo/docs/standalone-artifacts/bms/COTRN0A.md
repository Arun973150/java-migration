# BMS English Documentation: COTRN0A

## 1. Screen Purpose

`COTRN0A` is a BMS screen map in mapset `COTRN00` with map name `COTRN0A`. It is associated with program `COTRN00C` and contains 89 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 11 editable input field(s), 48 output/display field(s), and 30 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `TRNIDIN` at row 6, column 21, length 16: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0001` at row 10, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0002` at row 11, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0003` at row 12, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0004` at row 13, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0005` at row 14, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0006` at row 15, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0007` at row 16, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0008` at row 17, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0009` at row 18, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0010` at row 19, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `PAGENUM` at row 4, column 71, length 8: display value initialized as ``.
- `TRNID01` at row 10, column 8, length 16: display value initialized as ``.
- `TDATE01` at row 10, column 27, length 8: display value initialized as ``.
- `TDESC01` at row 10, column 38, length 26: display value initialized as ``.
- `TAMT001` at row 10, column 67, length 12: display value initialized as ``.
- `TRNID02` at row 11, column 8, length 16: display value initialized as ``.
- `TDATE02` at row 11, column 27, length 8: display value initialized as ``.
- `TDESC02` at row 11, column 38, length 26: display value initialized as ``.
- `TAMT002` at row 11, column 67, length 12: display value initialized as ``.
- `TRNID03` at row 12, column 8, length 16: display value initialized as ``.
- `TDATE03` at row 12, column 27, length 8: display value initialized as ``.
- `TDESC03` at row 12, column 38, length 26: display value initialized as ``.
- `TAMT003` at row 12, column 67, length 12: display value initialized as ``.
- `TRNID04` at row 13, column 8, length 16: display value initialized as ``.
- `TDATE04` at row 13, column 27, length 8: display value initialized as ``.
- `TDESC04` at row 13, column 38, length 26: display value initialized as ``.
- `TAMT004` at row 13, column 67, length 12: display value initialized as ``.
- `TRNID05` at row 14, column 8, length 16: display value initialized as ``.
- `TDATE05` at row 14, column 27, length 8: display value initialized as ``.
- `TDESC05` at row 14, column 38, length 26: display value initialized as ``.
- `TAMT005` at row 14, column 67, length 12: display value initialized as ``.
- `TRNID06` at row 15, column 8, length 16: display value initialized as ``.
- `TDATE06` at row 15, column 27, length 8: display value initialized as ``.
- `TDESC06` at row 15, column 38, length 26: display value initialized as ``.
- `TAMT006` at row 15, column 67, length 12: display value initialized as ``.
- `TRNID07` at row 16, column 8, length 16: display value initialized as ``.
- `TDATE07` at row 16, column 27, length 8: display value initialized as ``.
- `TDESC07` at row 16, column 38, length 26: display value initialized as ``.
- `TAMT007` at row 16, column 67, length 12: display value initialized as ``.
- `TRNID08` at row 17, column 8, length 16: display value initialized as ``.
- `TDATE08` at row 17, column 27, length 8: display value initialized as ``.
- `TDESC08` at row 17, column 38, length 26: display value initialized as ``.
- `TAMT008` at row 17, column 67, length 12: display value initialized as ``.
- `TRNID09` at row 18, column 8, length 16: display value initialized as ``.
- 8 additional display fields are present.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, List Transactions, Page:, Search Tran ID:, Sel, Transaction ID, Date, Description, Amount, ---, ----------------, --------, --------------------------, ------------, Type, ENTER=Continue  F3=Back  F7=Backward  F8=Forwar d
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COTRN00C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
