# BMS English Documentation: COSGN0A

## 1. Screen Purpose

`COSGN0A` is a BMS screen map in mapset `COSGN00` with map name `COSGN0A`. It is associated with program `COSGN00C` and contains 37 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 2 editable input field(s), 9 output/display field(s), and 26 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `USERID` at row 19, column 43, length 8: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.
- `PASSWD` at row 20, column 43, length 8: terminal input field with attributes `(DRK,FSET,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 8, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 8, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 9: display value initialized as ``.
- `APPLID` at row 3, column 8, length 8: display value initialized as ``.
- `SYSID` at row 3, column 71, length 8: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran :, Date :, Prog :, Time :, AppID:, SysID:, This is a Credit Card Demo Application for Main frame Modernization, +========================================+, |%%%%%%%  NATIONAL RESERVE NOTE  %%%%%%%%|, |%(1)  THE UNITED STATES OF KICSLAND (1)%|, |%$$              ___       ********  $$%|, |%$    {x}       (o o)                 $%|, |%$     ******  (  V  )      O N E     $%|, |%(1)          ---m-m---             (1)%|, |%%~~~~~~~~~~~ ONE DOLLAR ~~~~~~~~~~~~~%%|, +========================================+, Type your User ID and Password, then press ENTE R:, User ID     :, (8 Char), Password    :, (8 Char), ENTER=Sign-on  F3=Exit
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COSGN00C`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
