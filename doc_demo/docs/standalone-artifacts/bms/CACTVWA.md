# BMS English Documentation: CACTVWA

## 1. Screen Purpose

`CACTVWA` is a BMS screen map in mapset `COACTVW` with map name `CACTVWA`. It is associated with program `COACTVWC` and contains 100 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 1 editable input field(s), 36 output/display field(s), and 63 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- `ACCTSID` at row 5, column 38, length 11: terminal input field with attributes `(FSET,IC,NORM,UNPROT)`.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `ACSTTUS` at row 5, column 70, length 1: display value initialized as ``.
- `ADTOPEN` at row 6, column 17, length 10: display value initialized as ``.
- `ACRDLIM` at row 6, column 61, length 15: display value initialized as ``.
- `AEXPDT` at row 7, column 17, length 10: display value initialized as ``.
- `ACSHLIM` at row 7, column 61, length 15: display value initialized as ``.
- `AREISDT` at row 8, column 17, length 10: display value initialized as ``.
- `ACURBAL` at row 8, column 61, length 15: display value initialized as ``.
- `ACRCYCR` at row 9, column 61, length 15: display value initialized as ``.
- `AADDGRP` at row 10, column 23, length 10: display value initialized as ``.
- `ACRCYDB` at row 10, column 61, length 15: display value initialized as ``.
- `ACSTNUM` at row 12, column 23, length 9: display value initialized as ``.
- `ACSTSSN` at row 12, column 54, length 12: display value initialized as ``.
- `ACSTDOB` at row 13, column 23, length 10: display value initialized as ``.
- `ACSTFCO` at row 13, column 61, length 3: display value initialized as ``.
- `ACSFNAM` at row 15, column 1, length 25: display value initialized as ``.
- `ACSMNAM` at row 15, column 28, length 25: display value initialized as ``.
- `ACSLNAM` at row 15, column 55, length 25: display value initialized as ``.
- `ACSADL1` at row 16, column 10, length 50: display value initialized as ``.
- `ACSSTTE` at row 16, column 73, length 2: display value initialized as ``.
- `ACSADL2` at row 17, column 10, length 50: display value initialized as ``.
- `ACSZIPC` at row 17, column 73, length 5: display value initialized as ``.
- `ACSCITY` at row 18, column 10, length 50: display value initialized as ``.
- `ACSCTRY` at row 18, column 73, length 3: display value initialized as ``.
- `ACSPHN1` at row 19, column 10, length 13: display value initialized as ``.
- `ACSGOVT` at row 19, column 58, length 20: display value initialized as ``.
- `ACSPHN2` at row 20, column 10, length 13: display value initialized as ``.
- `ACSEFTC` at row 20, column 41, length 10: display value initialized as ``.
- `ACSPFLG` at row 20, column 78, length 1: display value initialized as ``.
- `INFOMSG` at row 22, column 23, length 45: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, View Account, Account Number :, Active Y/N:, Opened:, Credit Limit        :, Expiry:, Cash credit Limit   :, Reissue:, Current Balance     :, Current Cycle Credit:, Account Group:, Current Cycle Debit :, Customer Details, Customer id  :, SSN:, Date of birth:, FICO Score:, First Name, Middle Name:, Last Name :, Address:
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `COACTVWC`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
