# BMS English Documentation: COPAU0A

## 1. Screen Purpose

`COPAU0A` is a BMS screen map in mapset `COPAU00` with map name `COPAU0A`. It is associated with program `not present in extracted data` and contains 104 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 6 editable input field(s), 56 output/display field(s), and 42 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACCTID` at row 5, column 19, length 11: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0001` at row 16, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0002` at row 17, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0003` at row 18, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0004` at row 19, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `SEL0005` at row 20, column 3, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `CNAME` at row 6, column 10, length 25: display value initialized as ``.
- `CUSTID` at row 6, column 58, length 9: display value initialized as ``.
- `ADDR001` at row 7, column 10, length 25: display value initialized as ``.
- `ACCSTAT` at row 7, column 58, length 1: display value initialized as ``.
- `ADDR002` at row 8, column 10, length 25: display value initialized as ``.
- `PHONE1` at row 9, column 15, length 13: display value initialized as ``.
- `APPRCNT` at row 9, column 58, length 3: display value initialized as ``.
- `DECLCNT` at row 9, column 76, length 3: display value initialized as ``.
- `CREDLIM` at row 11, column 19, length 12: display value initialized as ``.
- `CASHLIM` at row 11, column 46, length 9: display value initialized as ``.
- `APPRAMT` at row 11, column 69, length 10: display value initialized as ``.
- `CREDBAL` at row 12, column 19, length 12: display value initialized as ``.
- `CASHBAL` at row 12, column 46, length 9: display value initialized as ``.
- `DECLAMT` at row 12, column 69, length 10: display value initialized as ``.
- `TRNID01` at row 16, column 8, length 16: display value initialized as ``.
- `PDATE01` at row 16, column 27, length 8: display value initialized as ``.
- `PTIME01` at row 16, column 38, length 8: display value initialized as ``.
- `PTYPE01` at row 16, column 49, length 4: display value initialized as ``.
- `PAPRV01` at row 16, column 58, length 1: display value initialized as ``.
- `PSTAT01` at row 16, column 63, length 1: display value initialized as ``.
- `PAMT001` at row 16, column 67, length 12: display value initialized as ``.
- `TRNID02` at row 17, column 8, length 16: display value initialized as ``.
- `PDATE02` at row 17, column 27, length 8: display value initialized as ``.
- `PTIME02` at row 17, column 38, length 8: display value initialized as ``.
- `PTYPE02` at row 17, column 49, length 4: display value initialized as ``.
- `PAPRV02` at row 17, column 58, length 1: display value initialized as ``.
- `PSTAT02` at row 17, column 63, length 1: display value initialized as ``.
- `PAMT002` at row 17, column 67, length 12: display value initialized as ``.
- `TRNID03` at row 18, column 8, length 16: display value initialized as ``.
- `PDATE03` at row 18, column 27, length 8: display value initialized as ``.
- `PTIME03` at row 18, column 38, length 8: display value initialized as ``.
- `PTYPE03` at row 18, column 49, length 4: display value initialized as ``.
- `PAPRV03` at row 18, column 58, length 1: display value initialized as ``.
- `PSTAT03` at row 18, column 63, length 1: display value initialized as ``.
- 16 additional display fields are present.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, View Authorizations, Search Acct Id:, Name:, Customer Id:, Acct Status:, PH:, Approval # :, Decline #:, Credit Lim:, Cash Lim:, Appr Amt:, Credit Bal:, Cash Bal:, Decl Amt:, Sel, Transaction ID, Date, Time, Type, A/D, STS
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `not present in extracted data`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
