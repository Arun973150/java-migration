# BMS English Documentation: COTRN1A

## 1. Screen Purpose

`COTRN1A` is a BMS screen map in mapset `COTRN01` with map name `COTRN1A`. It is associated with program `COTRN01C` and contains 56 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 1 editable input field(s), 20 output/display field(s), and 35 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `TRNIDIN` at row 6, column 21, length 16: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `TRNID` at row 10, column 22, length 16: display value initialized as ``.
- `CARDNUM` at row 10, column 58, length 16: display value initialized as ``.
- `TTYPCD` at row 12, column 15, length 2: display value initialized as ``.
- `TCATCD` at row 12, column 36, length 4: display value initialized as ``.
- `TRNSRC` at row 12, column 54, length 10: display value initialized as ``.
- `TDESC` at row 14, column 19, length 60: display value initialized as ``.
- `TRNAMT` at row 16, column 14, length 12: display value initialized as ``.
- `TORIGDT` at row 16, column 42, length 10: display value initialized as ``.
- `TPROCDT` at row 16, column 68, length 10: display value initialized as ``.
- `MID` at row 18, column 19, length 9: display value initialized as ``.
- `MNAME` at row 18, column 48, length 30: display value initialized as ``.
- `MCITY` at row 20, column 21, length 25: display value initialized as ``.
- `MZIP` at row 20, column 67, length 10: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, View Transaction, Enter Tran ID:, -----------------------, Transaction ID:, Card Number:, Type CD:, Category CD:, Source:, Description:, Amount:, Orig Date:, Proc Date:, Merchant ID:, Merchant Name:, Merchant City:, Merchant Zip:, ENTER=Fetch  F3=Back  F4=Clear  F5=Browse Tran.
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COTRN01C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
