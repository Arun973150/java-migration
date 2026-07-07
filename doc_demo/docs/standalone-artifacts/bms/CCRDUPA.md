# BMS English Documentation: CCRDUPA

## 1. Screen Purpose

`CCRDUPA` is a BMS screen map in mapset `COCRDUP` with map name `CCRDUPA`. It is associated with program `COCRDUPC` and contains 34 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 5 editable input field(s), 12 output/display field(s), and 17 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `CARDSID` at row 8, column 45, length 16: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `CRDNAME` at row 11, column 25, length 50: terminal input field with attributes `(UNPROT)`.
- `CRDSTCD` at row 13, column 25, length 1: terminal input field with attributes `(UNPROT)`.
- `EXPMON` at row 15, column 25, length 2: terminal input field with attributes `(UNPROT)`.
- `EXPYEAR` at row 15, column 30, length 4: terminal input field with attributes `(UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `ACCTSID` at row 7, column 45, length 11: display value initialized as ``.
- `EXPDAY` at row 15, column 36, length 2: display value initialized as ``.
- `INFOMSG` at row 20, column 25, length 40: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 80: display value initialized as ``.
- `FKEYS` at row 24, column 1, length 21: display value initialized as ``.
- `FKEYSC` at row 24, column 23, length 18: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Update Credit Card Details, Account Number    :, Card Number       :, Name on card      :, Card Active Y/N   :, Expiry Date       :, /
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COCRDUPC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
