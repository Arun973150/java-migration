# BMS English Documentation: CCRDLIA

## 1. Screen Purpose

`CCRDLIA` is a BMS screen map in mapset `COCRDLI` with map name `CCRDLIA`. It is associated with program `COCRDLIC` and contains 72 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 2 editable input field(s), 43 output/display field(s), and 27 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACCTSID` at row 6, column 44, length 11: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `CARDSID` at row 7, column 44, length 16: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `PAGENO` at row 4, column 76, length 3: display value initialized as ``.
- `CRDSEL1` at row 11, column 12, length 1: display value initialized as ``.
- `ACCTNO1` at row 11, column 22, length 11: display value initialized as ``.
- `CRDNUM1` at row 11, column 43, length 16: display value initialized as ``.
- `CRDSTS1` at row 11, column 67, length 1: display value initialized as ``.
- `CRDSEL2` at row 12, column 12, length 1: display value initialized as ``.
- `CRDSTP2` at row 12, column 14, length 1: display value initialized as ``.
- `ACCTNO2` at row 12, column 22, length 11: display value initialized as ``.
- `CRDNUM2` at row 12, column 43, length 16: display value initialized as ``.
- `CRDSTS2` at row 12, column 67, length 1: display value initialized as ``.
- `CRDSEL3` at row 13, column 12, length 1: display value initialized as ``.
- `CRDSTP3` at row 13, column 14, length 1: display value initialized as ``.
- `ACCTNO3` at row 13, column 22, length 11: display value initialized as ``.
- `CRDNUM3` at row 13, column 43, length 16: display value initialized as ``.
- `CRDSTS3` at row 13, column 67, length 1: display value initialized as ``.
- `CRDSEL4` at row 14, column 12, length 1: display value initialized as ``.
- `CRDSTP4` at row 14, column 14, length 1: display value initialized as ``.
- `ACCTNO4` at row 14, column 22, length 11: display value initialized as ``.
- `CRDNUM4` at row 14, column 43, length 16: display value initialized as ``.
- `CRDSTS4` at row 14, column 67, length 1: display value initialized as ``.
- `CRDSEL5` at row 15, column 12, length 1: display value initialized as ``.
- `CRDSTP5` at row 15, column 14, length 1: display value initialized as ``.
- `ACCTNO5` at row 15, column 22, length 11: display value initialized as ``.
- `CRDNUM5` at row 15, column 43, length 16: display value initialized as ``.
- `CRDSTS5` at row 15, column 67, length 1: display value initialized as ``.
- `CRDSEL6` at row 16, column 12, length 1: display value initialized as ``.
- `CRDSTP6` at row 16, column 14, length 1: display value initialized as ``.
- `ACCTNO6` at row 16, column 22, length 11: display value initialized as ``.
- `CRDNUM6` at row 16, column 43, length 16: display value initialized as ``.
- `CRDSTS6` at row 16, column 67, length 1: display value initialized as ``.
- `CRDSEL7` at row 17, column 12, length 1: display value initialized as ``.
- `CRDSTP7` at row 17, column 14, length 1: display value initialized as ``.
- `ACCTNO7` at row 17, column 22, length 11: display value initialized as ``.
- `CRDNUM7` at row 17, column 43, length 16: display value initialized as ``.
- 3 additional display fields are present.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, List Credit Cards, Page, Account Number    :, Credit Card Number:, Select, Account Number, Card Number, Active, ------, ---------------, ---------------, --------, F3=Exit F7=Backward  F8=Forward
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COCRDLIC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
