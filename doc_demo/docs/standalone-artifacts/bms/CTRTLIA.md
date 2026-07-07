# BMS English Documentation: CTRTLIA

## 1. Screen Purpose

`CTRTLIA` is a BMS screen map in mapset `COTRTLI` with map name `CTRTLIA`. It is associated with program `COTRTLIC` and contains 81 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 9 editable input field(s), 31 output/display field(s), and 41 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `TRTYPE` at row 6, column 44, length 2: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `TRDESC` at row 8, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD1` at row 12, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD2` at row 13, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD3` at row 14, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD4` at row 15, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD5` at row 16, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD6` at row 17, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `TRTYPD7` at row 18, column 25, length 50: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `PAGENO` at row 4, column 76, length 3: display value initialized as ``.
- `TRTSEL1` at row 12, column 6, length 1: display value initialized as ``.
- `TRTTYP1` at row 12, column 17, length 2: display value initialized as ``.
- `TRTSEL2` at row 13, column 6, length 1: display value initialized as ``.
- `TRTTYP2` at row 13, column 17, length 2: display value initialized as ``.
- `TRTSEL3` at row 14, column 6, length 1: display value initialized as ``.
- `TRTTYP3` at row 14, column 17, length 2: display value initialized as ``.
- `TRTSEL4` at row 15, column 6, length 1: display value initialized as ``.
- `TRTTYP4` at row 15, column 17, length 2: display value initialized as ``.
- `TRTSEL5` at row 16, column 6, length 1: display value initialized as ``.
- `TRTTYP5` at row 16, column 17, length 2: display value initialized as ``.
- `TRTSEL6` at row 17, column 6, length 1: display value initialized as ``.
- `TRTTYP6` at row 17, column 17, length 2: display value initialized as ``.
- `TRTSEL7` at row 18, column 6, length 1: display value initialized as ``.
- `TRTTYP7` at row 18, column 17, length 2: display value initialized as ``.
- `TRTSELA` at row 19, column 6, length 1: display value initialized as ``.
- `TRTTYPA` at row 19, column 17, length 2: display value initialized as ``.
- `TRTDSCA` at row 19, column 25, length 50: display value initialized as ``.
- `INFOMSG` at row 21, column 19, length 45: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.
- `BUTNF02` at row 24, column 1, length 7: display value initialized as ``.
- `BUTNF03` at row 24, column 10, length 7: display value initialized as ``.
- `BUTNF07` at row 24, column 19, length 10: display value initialized as ``.
- `BUTNF08` at row 24, column 32, length 10: display value initialized as ``.
- `BUTNF10` at row 24, column 44, length 8: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Maintain Transaction Type, Page, Type Filter:, Description Filter:, Select, Type, Description, ------, -----, ---
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COTRTLIC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
