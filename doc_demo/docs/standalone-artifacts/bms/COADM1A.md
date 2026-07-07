# BMS English Documentation: COADM1A

## 1. Screen Purpose

`COADM1A` is a BMS screen map in mapset `COADM01` with map name `COADM1A`. It is associated with program `COADM01C` and contains 28 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 1 editable input field(s), 19 output/display field(s), and 8 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `OPTION` at row 20, column 41, length 2: terminal input field with attributes `(FSET,IC,NORM,NUM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `OPTN001` at row 6, column 20, length 40: display value initialized as ``.
- `OPTN002` at row 7, column 20, length 40: display value initialized as ``.
- `OPTN003` at row 8, column 20, length 40: display value initialized as ``.
- `OPTN004` at row 9, column 20, length 40: display value initialized as ``.
- `OPTN005` at row 10, column 20, length 40: display value initialized as ``.
- `OPTN006` at row 11, column 20, length 40: display value initialized as ``.
- `OPTN007` at row 12, column 20, length 40: display value initialized as ``.
- `OPTN008` at row 13, column 20, length 40: display value initialized as ``.
- `OPTN009` at row 14, column 20, length 40: display value initialized as ``.
- `OPTN010` at row 15, column 20, length 40: display value initialized as ``.
- `OPTN011` at row 16, column 20, length 40: display value initialized as ``.
- `OPTN012` at row 17, column 20, length 40: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Admin Menu, Please select an option :, ENTER=Continue  F3=Exit
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COADM01C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
