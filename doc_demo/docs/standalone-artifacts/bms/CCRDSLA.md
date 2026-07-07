# BMS English Documentation: CCRDSLA

## 1. Screen Purpose

`CCRDSLA` is a BMS screen map in mapset `COCRDSL` with map name `CCRDSLA`. It is associated with program `COCRDSLC` and contains 31 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 2 editable input field(s), 13 output/display field(s), and 16 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACCTSID` at row 7, column 45, length 11: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `CARDSID` at row 8, column 45, length 16: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `CRDNAME` at row 11, column 25, length 50: display value initialized as ``.
- `CRDSTCD` at row 13, column 25, length 1: display value initialized as ``.
- `EXPMON` at row 15, column 25, length 2: display value initialized as ``.
- `EXPYEAR` at row 15, column 30, length 4: display value initialized as ``.
- `INFOMSG` at row 20, column 25, length 40: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 80: display value initialized as ``.
- `FKEYS` at row 24, column 1, length 75: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, View Credit Card Detail, Account Number    :, Card Number       :, Name on card      :, Card Active Y/N   :, Expiry Date       :, /
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COCRDSLC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
