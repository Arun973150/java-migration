# BMS English Documentation: COPAU1A

## 1. Screen Purpose

`COPAU1A` is a BMS screen map in mapset `COPAU01` with map name `COPAU1A`. It is associated with program `not present in extracted data` and contains 54 extracted field(s) across rows 1 through 24.

## 2. User Interaction Model

The screen exposes 0 editable input field(s), 27 output/display field(s), and 27 label/decorative field(s). Input fields represent values the terminal user can provide. Output fields represent values the backing CICS program prepares and sends to the terminal.

## 3. Input Fields

- No editable input fields were extracted for this map.

## 4. Display Fields

- `TRNNAME` at row 1, column 7, length 4: display value initialized as ``.
- `TITLE01` at row 1, column 21, length 40: display value initialized as ``.
- `CURDATE` at row 1, column 71, length 8: display value initialized as ``.
- `PGMNAME` at row 2, column 7, length 8: display value initialized as ``.
- `TITLE02` at row 2, column 21, length 40: display value initialized as ``.
- `CURTIME` at row 2, column 71, length 8: display value initialized as ``.
- `CARDNUM` at row 7, column 11, length 16: display value initialized as ``.
- `AUTHDT` at row 7, column 43, length 10: display value initialized as ``.
- `AUTHTM` at row 7, column 68, length 10: display value initialized as ``.
- `AUTHRSP` at row 9, column 14, length 1: display value initialized as ``.
- `AUTHRSN` at row 9, column 32, length 20: display value initialized as ``.
- `AUTHCD` at row 9, column 68, length 6: display value initialized as ``.
- `AUTHAMT` at row 11, column 11, length 12: display value initialized as ``.
- `POSEMD` at row 11, column 46, length 4: display value initialized as ``.
- `AUTHSRC` at row 11, column 68, length 10: display value initialized as ``.
- `MCCCD` at row 13, column 13, length 4: display value initialized as ``.
- `CRDEXP` at row 13, column 42, length 5: display value initialized as ``.
- `AUTHTYP` at row 13, column 64, length 14: display value initialized as ``.
- `TRNID` at row 15, column 12, length 15: display value initialized as ``.
- `AUTHMTC` at row 15, column 46, length 1: display value initialized as ``.
- `AUTHFRD` at row 15, column 67, length 10: display value initialized as ``.
- `MERNAME` at row 19, column 9, length 25: display value initialized as ``.
- `MERID` at row 19, column 55, length 15: display value initialized as ``.
- `MERCITY` at row 21, column 9, length 25: display value initialized as ``.
- `MERST` at row 21, column 49, length 2: display value initialized as ``.
- `MERZIP` at row 21, column 61, length 10: display value initialized as ``.
- `ERRMSG` at row 23, column 1, length 78: display value initialized as ``.

## 5. Labels and Layout

- Layout labels sampled from the map: Tran:, Date:, Prog:, Time:, View Authorization Details, Card #:, Auth Date:, Auth Time:, Auth Resp:, Resp Reason:, Auth Code:, Amount:, POS Entry Mode:, Source   :, MCC Code:, Card Exp. Date:, Auth Type:, Tran Id:, Match Status:, Fraud Status:, Merchant Details -----------------------------, Name:, Merchant ID:, City:, State:
- Color usage: None found in extracted data

## 6. Program and Navigation Context

The extracted program link is `not present in extracted data`. In a CICS migration, this screen should be analyzed with the program's SEND MAP and RECEIVE MAP commands to determine submit, validation, and navigation behavior.

## 7. Migration Notes

- Modern equivalent: a UI form or read-only detail/list view, depending on the input/display field mix.
- Preserve field lengths and row/column grouping as validation and layout hints.
- Convert labels into UI captions, input fields into form controls, and output fields into read-only values.
- Validate PF-key and transaction navigation from the associated CICS program before replacing the 3270 flow.
