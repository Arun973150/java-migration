# BMS English Documentation: COUSR1A

## 1. Screen Purpose

`COUSR1A` is a BMS screen map in mapset `COUSR01` with map name `COUSR1A`. It is associated with program `COUSR01C` and contains 28 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 5 editable input field(s), 7 output/display field(s), and 16 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `FNAME` at row 8, column 18, length 20: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `LNAME` at row 8, column 56, length 20: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `USERID` at row 11, column 15, length 8: terminal input field with attributes `(FSET,NORM,UNPROT)`.
- `PASSWD` at row 11, column 55, length 8: terminal input field with attributes `(DRK,FSET,UNPROT)`.
- `USRTYPE` at row 14, column 17, length 1: terminal input field with attributes `(FSET,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, Add User, First Name:, Last Name:, User ID:, (8 Char), Password:, (8 Char), User Type:, (A=Admin, U=User), ENTER=Add User  F3=Back  F4=Clear  F12=Exit
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COUSR01C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
