# BMS English Documentation: COUSR0A

## 1. Screen Purpose

`COUSR0A` is a BMS screen map in mapset `COUSR00` with map name `COUSR0A`. It is associated with program `COUSR00C` and contains 89 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 11 editable input field(s), 48 output/display field(s), and 30 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `USRIDIN` at row 6, column 21, length 8: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0001` at row 10, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0002` at row 11, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0003` at row 12, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0004` at row 13, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0005` at row 14, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0006` at row 15, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0007` at row 16, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0008` at row 17, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0009` at row 18, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0010` at row 19, column 6, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `PAGENUM` at row 4, column 71, length 8: display value initialized as ``.
- `USRID01` at row 10, column 12, length 8: display value initialized as ``.
- `FNAME01` at row 10, column 24, length 20: display value initialized as ``.
- `LNAME01` at row 10, column 48, length 20: display value initialized as ``.
- `UTYPE01` at row 10, column 73, length 1: display value initialized as ``.
- `USRID02` at row 11, column 12, length 8: display value initialized as ``.
- `FNAME02` at row 11, column 24, length 20: display value initialized as ``.
- `LNAME02` at row 11, column 48, length 20: display value initialized as ``.
- `UTYPE02` at row 11, column 73, length 1: display value initialized as ``.
- `USRID03` at row 12, column 12, length 8: display value initialized as ``.
- `FNAME03` at row 12, column 24, length 20: display value initialized as ``.
- `LNAME03` at row 12, column 48, length 20: display value initialized as ``.
- `UTYPE03` at row 12, column 73, length 1: display value initialized as ``.
- `USRID04` at row 13, column 12, length 8: display value initialized as ``.
- `FNAME04` at row 13, column 24, length 20: display value initialized as ``.
- `LNAME04` at row 13, column 48, length 20: display value initialized as ``.
- `UTYPE04` at row 13, column 73, length 1: display value initialized as ``.
- `USRID05` at row 14, column 12, length 8: display value initialized as ``.
- `FNAME05` at row 14, column 24, length 20: display value initialized as ``.
- `LNAME05` at row 14, column 48, length 20: display value initialized as ``.
- `UTYPE05` at row 14, column 73, length 1: display value initialized as ``.
- `USRID06` at row 15, column 12, length 8: display value initialized as ``.
- `FNAME06` at row 15, column 24, length 20: display value initialized as ``.
- `LNAME06` at row 15, column 48, length 20: display value initialized as ``.
- `UTYPE06` at row 15, column 73, length 1: display value initialized as ``.
- `USRID07` at row 16, column 12, length 8: display value initialized as ``.
- `FNAME07` at row 16, column 24, length 20: display value initialized as ``.
- `LNAME07` at row 16, column 48, length 20: display value initialized as ``.
- `UTYPE07` at row 16, column 73, length 1: display value initialized as ``.
- `USRID08` at row 17, column 12, length 8: display value initialized as ``.
- `FNAME08` at row 17, column 24, length 20: display value initialized as ``.
- `LNAME08` at row 17, column 48, length 20: display value initialized as ``.
- `UTYPE08` at row 17, column 73, length 1: display value initialized as ``.
- `USRID09` at row 18, column 12, length 8: display value initialized as ``.
- 8 additional display fields are present.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, List Users, Page:, Search User ID:, Sel, User ID, First Name, Last Name, Type, ---, --------, --------------------, --------------------, ----, Type, ENTER=Continue  F3=Back  F7=Backward  F8=Forwar d
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COUSR00C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
