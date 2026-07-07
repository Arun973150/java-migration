# Business Rules Catalog

> **Total Rules:** 447  
> **Categories:** 4

---

## CALCULATION (16 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-024](BR-024.md) | Authorization Period Calculation | The program calculates the duration of an authorization, pos... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-027](BR-027.md) | Authorization Period Calculation | The program calculates the duration of an authorization, lik... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-089](BR-089.md) | Late Payment Fee Assessment | If a customer's payment is received after the due date, a la... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-090](BR-090.md) | Interest Calculation | Interest is calculated and applied to customer accounts base... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-095](BR-095.md) | Apply Standard Interest Rate | If a specific interest rate is not found for an account, app... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-096](BR-096.md) | Apply Discounted Interest Rate | If the account belongs to a discount group, apply the discou... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-097](BR-097.md) | Default Interest Rate Assignment | If a specific interest rate is not found for an account, a d... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-249](BR-249.md) | Increase Transaction Category Balance for Credits | If a transaction is a credit, increase the corresponding tra... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-250](BR-250.md) | Decrease Transaction Category Balance for Debits | If a transaction is a debit, decrease the corresponding tran... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-252](BR-252.md) | Initial Transaction Category Balance | When creating a new transaction category balance record, the... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-253](BR-253.md) | Increase Transaction Category Balance for Credits | If a transaction is a credit, increase the corresponding tra... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-254](BR-254.md) | Decrease Transaction Category Balance for Debits | If a transaction is a debit, decrease the corresponding tran... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-257](BR-257.md) | Transaction Category Balance Update | The transaction category balance is updated to reflect the t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-260](BR-260.md) | Transaction Category Balance Update | If a transaction is successfully processed, the correspondin... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-264](BR-264.md) | Transaction Category Balance Update | The transaction category balance file is updated to reflect ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-446](BR-446.md) | Date Conversion to Lillian Format | The system converts a valid date to the Lillian date format. | [CSUTLDTC](../programs/CSUTLDTC.md) |

## COMPLIANCE (17 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-001](BR-001.md) | Update Fraud Indicator | Under certain conditions, flag a transaction as potentially ... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-002](BR-002.md) | Flag Potentially Fraudulent Activity | If a specific, but currently unknown, condition is met, then... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-023](BR-023.md) | Authorization Expiry Date Validation | If the authorization expiry date is in the past, the authori... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-026](BR-026.md) | Authorization Expiry Date Validation | If the authorization expiry date is in the past, the authori... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-029](BR-029.md) | Authorization Record Flagging Based on Expiry Date Difference | If the difference between the authorization expiry date and ... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-030](BR-030.md) | Authorization Record Deletion Based on Expiry Date | Authorization records are automatically deleted if the expir... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-162](BR-162.md) | Transaction Amount Limit | Transactions exceeding a predefined amount limit are flagged... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-276](BR-276.md) | Account Activity Limit | If an account's total transaction activity exceeds a predefi... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-289](BR-289.md) | Report Date Range Control | The report includes transactions within a specific date rang... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-307](BR-307.md) | Transaction Recording | All payment transactions, whether successful or failed, must... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-329](BR-329.md) | Transaction Report Request Logging | The system logs details of transaction report submissions. | [CORPT00C](../programs/CORPT00C.md) |
| [BR-418](BR-418.md) | Security Profile Authorization | The system verifies if the user initiating the creation of a... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-432](BR-432.md) | User Deletion Authorization | The system must verify that the user attempting to delete an... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-437](BR-437.md) | Security Record Deletion | The system must delete the user's security record when a use... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-438](BR-438.md) | General Information Deletion | The system must delete the user's general information when a... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-440](BR-440.md) | Security Record Deletion | The system must delete the user's security record when a use... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-441](BR-441.md) | General Information Deletion | The system must delete the user's general information when a... | [COUSR03C](../programs/COUSR03C.md) |

## VALIDATION (140 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-007](BR-007.md) | Authorization Detail Record Limit | There is a limit to the number of detail records that can be... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-010](BR-010.md) | Root Segment Data Validation | If the root segment data is invalid, the authorization data ... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-011](BR-011.md) | Child Segment Data Validation | If the child segment data is invalid, the authorization data... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-012](BR-012.md) | Root Record Validation | If a root segment record is invalid, the authorization data ... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-014](BR-014.md) | Child Record Validation | If a child record is invalid, it will be rejected. | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-021](BR-021.md) | Authorization Expiry Date Validation | If the authorization expiry date is in the past, the authori... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-028](BR-028.md) | Authorization Record Flagging | Authorization records are flagged based on the calculated au... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-039](BR-039.md) | Record Type Validation | The system determines the type of database update (insert, u... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-041](BR-041.md) | Delete Record Validation | If the database delete operation fails, set the DB2 delete s... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-043](BR-043.md) | Account Record Type Validation | The system must validate the account record type to ensure i... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-050](BR-050.md) | Account Record Type Validation | The system validates the account record type to determine th... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-056](BR-056.md) | Account Record Type Validation | The system validates the account record type to determine th... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-058](BR-058.md) | Account Record Type Validation | If the account record type is invalid, the program should te... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-059](BR-059.md) | Account File Closing Validation | If the account file closing process fails, the program shoul... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-069](BR-069.md) | Cross-Reference File Read Error | If there is a problem reading a record from the card cross-r... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-074](BR-074.md) | Handle Cross-Reference File Close Error | If an error occurs while closing the cross-reference file, t... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-075](BR-075.md) | Cross-Reference File Read Error | If there is an issue reading the cross-reference file, the p... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-076](BR-076.md) | Cross-Reference File Write Error | If there is an issue writing to the cross-reference file, th... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-077](BR-077.md) | Invalid Transaction Record | If a transaction record is invalid, the transaction is rejec... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-078](BR-078.md) | Account Not Found | If an account cannot be found for a transaction, the transac... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-079](BR-079.md) | Cross-Reference File Open Validation | The program must successfully open the cross-reference file ... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-080](BR-080.md) | Transaction File Open Validation | The program must successfully open the transaction file cont... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-083](BR-083.md) | Transaction File Open Validation | The transaction file must be successfully opened before proc... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-084](BR-084.md) | Account File Open Validation | The account file must be successfully opened before processi... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-085](BR-085.md) | Transaction File Open Validation | The transaction file must be available and successfully open... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-086](BR-086.md) | Account File Open Validation | The account file must be available and successfully opened b... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-087](BR-087.md) | Invalid Transaction Handling | If a transaction record is identified as invalid, the transa... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-088](BR-088.md) | Account Not Found Handling | If an account cannot be found for a given transaction, the t... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-091](BR-091.md) | Invalid Account Handling | If an account record cannot be found for a given transaction... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-092](BR-092.md) | Account Status Check | Transactions are rejected if the associated account is not i... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-093](BR-093.md) | Invalid Card Number Handling | If a card number is not found in the cross-reference file, t... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-107](BR-107.md) | Transaction File Close - Record Count Validation | Verify that the number of transaction records processed is g... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-108](BR-108.md) | Transaction File Close - Update Count Validation | Verify that the number of account records updated is greater... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-123](BR-123.md) | Invalid Customer Record | If a customer record is invalid, it is rejected and not incl... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-129](BR-129.md) | Transaction Amount Validation | If a transaction amount is negative, the transaction is cons... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-131](BR-131.md) | Invalid Card Record Handling | If a card record is invalid, the system should log the error... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-142](BR-142.md) | Record Type Validation | The system must identify the type of record being processed ... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-156](BR-156.md) | Invalid Record Handling | If a record from the external file is of an unrecognized typ... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-157](BR-157.md) | Transaction Type Validation | Only transactions of type 'Credit', 'Debit', or 'Adjustment'... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-161](BR-161.md) | Transaction Record Validation | Only process transaction records with a valid transaction co... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-167](BR-167.md) | Transaction Type Validation | Only transactions of type 'P', 'D', 'W', or 'I' are included... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-175](BR-175.md) | Transaction File Open Check | The system verifies if the transaction file can be opened ba... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-176](BR-176.md) | Cross-Reference File Open Check | The system verifies if the cross-reference file can be opene... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-177](BR-177.md) | Customer File Open Check | The system verifies if the customer file can be opened based... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-178](BR-178.md) | Account File Open Check | The system verifies if the account file can be opened based ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-179](BR-179.md) | Transaction File Close Check | The system verifies if the transaction file can be closed ba... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-180](BR-180.md) | Cross-Reference File Close Check | The system verifies if the cross-reference file can be close... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-181](BR-181.md) | Customer File Close Check | The system verifies if the customer file can be closed based... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-182](BR-182.md) | Account File Close Check | The system verifies if the account file can be closed based ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-183](BR-183.md) | Transaction File Read Check | The system verifies if the transaction file can be read base... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-184](BR-184.md) | Cross-Reference File Read Check | The system verifies if the cross-reference file can be read ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-185](BR-185.md) | Customer File Read Check | The system verifies if the customer file can be read based o... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-186](BR-186.md) | Account File Read Check | The system verifies if the account file can be read based on... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-187](BR-187.md) | Transaction File Read-Key Check | The system verifies if the transaction file can be read by k... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-188](BR-188.md) | Cross-Reference File Read-Key Check | The system verifies if the cross-reference file can be read ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-189](BR-189.md) | Customer File Read-Key Check | The system verifies if the customer file can be read by key ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-190](BR-190.md) | Account File Read-Key Check | The system verifies if the account file can be read by key b... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-191](BR-191.md) | Transaction File Write Check | The system verifies if the transaction file can be written t... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-192](BR-192.md) | Cross-Reference File Write Check | The system verifies if the cross-reference file can be writt... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-193](BR-193.md) | Customer File Write Check | The system verifies if the customer file can be written to b... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-194](BR-194.md) | Account File Write Check | The system verifies if the account file can be written to ba... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-195](BR-195.md) | Transaction File Open Status Check | The system verifies if the transaction file can be opened su... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-196](BR-196.md) | Transaction File Read Status Check | The system verifies if records can be read from the transact... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-197](BR-197.md) | Transaction File Write Status Check | The system verifies if records can be written to the transac... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-198](BR-198.md) | Cross-Reference File Open Status Check | The system verifies if the cross-reference file can be opene... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-199](BR-199.md) | Cross-Reference File Read Status Check | The system verifies if records can be read from the cross-re... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-200](BR-200.md) | Cross-Reference File Close Status Check | The system verifies if the cross-reference file can be close... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-201](BR-201.md) | Customer File Read Status Check | If the attempt to read the customer file fails, the customer... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-202](BR-202.md) | Customer File Write Status Check | If the attempt to write to the customer file fails, the cust... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-203](BR-203.md) | Account File Open Status Check | The system verifies if the account file can be opened succes... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-204](BR-204.md) | Account File Read Status Check | The system verifies if records can be read from the account ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-205](BR-205.md) | Account File Read-by-Key Status Check | The system verifies if records can be read from the account ... | [CBSTM03B](../programs/CBSTM03B.md) |
| [BR-208](BR-208.md) | Transaction File Open Validation | The daily transaction file must be successfully opened befor... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-209](BR-209.md) | Customer Cross-Reference File Open Validation | The customer cross-reference file, linking transaction detai... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-222](BR-222.md) | Customer File Close Status Check | The system verifies that the customer file has been successf... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-223](BR-223.md) | Cross-Reference File Close Status Check | The system verifies that the cross-reference file has been s... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-227](BR-227.md) | Card File Error Handling | If an error occurs while closing the card file, an error mes... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-228](BR-228.md) | Account File Status Check | If the account file is not successfully closed, an error mes... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-229](BR-229.md) | Transaction File Status Check | If the transaction file is not successfully closed, an error... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-230](BR-230.md) | Transaction File Close Success Check | Verify that the daily transaction file has been successfully... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-231](BR-231.md) | Customer Cross-Reference File Close Success Check | Ensure the customer cross-reference file is successfully clo... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-242](BR-242.md) | Invalid Account Number | If a matching account record is not found in the account fil... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-247](BR-247.md) | Invalid Transaction Code | If a transaction has an invalid transaction code, it is reje... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-255](BR-255.md) | Transaction Amount Limit Check | If a transaction amount exceeds a predefined limit, the tran... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-256](BR-256.md) | Account Status Check | Transactions are only allowed for accounts that are in good ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-265](BR-265.md) | Reject Record if TCATBAL Update Fails | If updating the Transaction Category Balance file (TCATBAL) ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-272](BR-272.md) | Invalid Date Range | If the report's start date is later than the end date, the r... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-274](BR-274.md) | Invalid Transaction Handling | If a transaction record has an invalid transaction type, it ... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-279](BR-279.md) | Transaction File Open Validation | The transaction file must be successfully opened before proc... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-280](BR-280.md) | Cross-Reference File Open Validation | The cross-reference file must be successfully opened before ... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-283](BR-283.md) | Cross-Reference File Open Validation | The program must successfully open the cross-reference file ... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-284](BR-284.md) | Transaction Data Validation | The program validates transaction data against the cross-ref... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-285](BR-285.md) | Transaction Type Validation | If the transaction type is invalid, the transaction should b... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-290](BR-290.md) | Report Date Range Validation | The report will only be generated if the specified start dat... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-297](BR-297.md) | Transaction Type Validation | If the transaction type is invalid, the transaction should b... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-300](BR-300.md) | Report Date Range Validation | The report will only be generated if the specified start dat... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-302](BR-302.md) | Invalid Program ID Error | If the user enters an invalid program ID, an error message i... | [COADM01C](../programs/COADM01C.md) |
| [BR-303](BR-303.md) | Invalid Program ID Error Message | If the user enters an invalid program ID, an error message i... | [COADM01C](../programs/COADM01C.md) |
| [BR-304](BR-304.md) | Invalid Program ID Error Message | If the user enters an invalid program ID, an error message i... | [COADM01C](../programs/COADM01C.md) |
| [BR-305](BR-305.md) | Insufficient Funds Check | If the payment amount exceeds the available account balance,... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-306](BR-306.md) | Payment Amount Exceeds Balance | A payment cannot be processed if the payment amount is great... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-308](BR-308.md) | Payment Amount Validation | The system must ensure that the payment amount entered by th... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-310](BR-310.md) | Insufficient Funds | Bill payment is rejected if the payment amount exceeds the a... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-311](BR-311.md) | Insufficient Funds | If the payment amount exceeds the available account balance,... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-313](BR-313.md) | Account Status Check | Payments are only allowed from active accounts. | [COBIL00C](../programs/COBIL00C.md) |
| [BR-314](BR-314.md) | Sufficient Funds Check | A payment can only be processed if the account has sufficien... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-319](BR-319.md) | Invalid Menu Option | If the user enters an invalid menu option, an error message ... | [COMEN01C](../programs/COMEN01C.md) |
| [BR-332](BR-332.md) | Invalid Login Attempt | If the provided User ID and Password combination does not ma... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-333](BR-333.md) | Invalid User ID Message | If the entered User ID is invalid, display an error message ... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-334](BR-334.md) | Invalid Password Message | If the entered Password does not match the Password associat... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-337](BR-337.md) | Invalid User ID | If the provided User ID does not exist in the user security ... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-338](BR-338.md) | Inactive User Account | If the user account associated with the provided User ID is ... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-339](BR-339.md) | Password Mismatch | If the provided password does not match the password stored ... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-347](BR-347.md) | Check for End of Transaction Data | Before displaying the next page, verify if the end of the tr... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-359](BR-359.md) | Transaction Code Validation | If the entered transaction code is invalid, display an error... | [COTRN01C](../programs/COTRN01C.md) |
| [BR-371](BR-371.md) | Invalid Transaction Type Handling | If the transaction type is not A, B, C, or D, the system dis... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-372](BR-372.md) | Transaction Type Validation | The transaction type must be one of the allowed values. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-373](BR-373.md) | Account Number Validation | The account number must be numeric. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-374](BR-374.md) | Amount Validation | The transaction amount must be numeric. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-375](BR-375.md) | Transaction Type Validation | The transaction type must be a valid code. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-376](BR-376.md) | Cross-Reference Validation | The cross-reference code must be a valid code. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-377](BR-377.md) | Amount Validation | The transaction amount must be within acceptable limits. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-380](BR-380.md) | Invalid CXACAIX Record | If the CXACAIX record cannot be read, display an error messa... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-381](BR-381.md) | Invalid CCXREF Record | If the CCXREF record is not found, display an error message. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-399](BR-399.md) | Handle Invalid Menu Option | If the user enters an invalid option on the menu, display an... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-409](BR-409.md) | Invalid Security File Status | If the security file is not in a valid state after an attemp... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-414](BR-414.md) | Invalid Security Level | If the entered security level is not valid, the user will be... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-415](BR-415.md) | Invalid User ID | If the entered User ID is invalid, the user will be notified... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-416](BR-416.md) | User ID Format Check | The system validates the format of the entered User ID. | [COUSR01C](../programs/COUSR01C.md) |
| [BR-417](BR-417.md) | Password Complexity Check | The system enforces password complexity rules when a new pas... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-420](BR-420.md) | Invalid Security Level | If the entered security level is not valid, display an error... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-422](BR-422.md) | Profile Update Validation | The system validates the updated profile information entered... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-425](BR-425.md) | Invalid Security Code | If the security code entered by the user is invalid, the upd... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-428](BR-428.md) | Invalid Security Level | If the user enters a security level that is not valid, the u... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-429](BR-429.md) | Security Record Not Found | If the user's security record cannot be found, the update wi... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-430](BR-430.md) | Invalid Security Level | If the security level entered is not valid, the update will ... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-431](BR-431.md) | Password Complexity Check | The new password must meet complexity requirements before it... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-433](BR-433.md) | User Existence Check Before Deletion | The system must confirm that the user account to be deleted ... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-445](BR-445.md) | Date Validation Result | The system validates a date against a specified format and p... | [CSUTLDTC](../programs/CSUTLDTC.md) |
| [BR-447](BR-447.md) | Error Reporting for Invalid Dates | The system reports an error when a date is invalid. | [CSUTLDTC](../programs/CSUTLDTC.md) |

## WORKFLOW (274 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-003](BR-003.md) | Authorization Summary Record Found | If an authorization summary record is successfully read from... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-004](BR-004.md) | Authorization Detail Record Found | If an authorization detail record is successfully read from ... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-005](BR-005.md) | End of Authorization Detail Records | If there are no more authorization detail records associated... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-006](BR-006.md) | Detail Record Belongs to Summary Record | A detail record is only processed if it is associated with t... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-008](BR-008.md) | Authorization Summary Record Insertion | An authorization summary record must be written to the GSAM ... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-009](BR-009.md) | Authorization Detail Record Insertion | Authorization detail records associated with a summary recor... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-013](BR-013.md) | Root Segment Insert Failure | If inserting a root segment into the database fails, the pro... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-015](BR-015.md) | Child Segment Insertion | Child segment data is added to the database to provide more ... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-016](BR-016.md) | Root Segment Insertion Success Check | If the attempt to insert a root segment into the database is... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-017](BR-017.md) | Child Segment Insertion Success Check | If the attempt to insert a child segment into the database i... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-018](BR-018.md) | Database Insertion Error Handling | If an error occurs during the insertion of either a root or ... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-019](BR-019.md) | Input File Close Status Check | If the input file close operation fails, the program should ... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-020](BR-020.md) | Output File Close Status Check | If the output file close operation fails, the program should... | [PAUDBLOD](../programs/PAUDBLOD.md) |
| [BR-022](BR-022.md) | Authorization Grace Period Handling | Authorizations are granted a grace period after their expiry... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-025](BR-025.md) | Authorization Record Processing | Authorization summary and detail records are passed to exter... | [PAUDBUNL](../programs/PAUDBUNL.md) |
| [BR-031](BR-031.md) | Transaction File Open Success | The transaction file must open successfully for the update p... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-032](BR-032.md) | Database Connection Success | A successful connection to the DB2 database is required to p... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-033](BR-033.md) | Process Insert Record | When a transaction record indicates an insert operation, a n... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-034](BR-034.md) | Process Update Record | When a transaction record indicates an update operation, an ... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-035](BR-035.md) | Process Delete Record | When a transaction record indicates a delete operation, an e... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-036](BR-036.md) | Process Insert Record | When a transaction record indicates an insert operation, add... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-037](BR-037.md) | Process Update Record | When a transaction record indicates an update operation, mod... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-038](BR-038.md) | Process Delete Record | When a transaction record indicates a delete operation, remo... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-040](BR-040.md) | Transaction Type Validation | The system determines the type of database update (insert, u... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-042](BR-042.md) | Delete Record Failure Handling | If the database delete operation fails, set the overall prog... | [COBTUPDT](../programs/COBTUPDT.md) |
| [BR-044](BR-044.md) | High Balance Account Archiving | Accounts with balances exceeding a defined threshold are arc... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-045](BR-045.md) | Populate Account Record | When an account record is processed, populate the account re... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-046](BR-046.md) | Account Record Archiving | Account records are archived to specific output files based ... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-047](BR-047.md) | Archive Account Record | Account records are written to an archive file. | [CBACT01C](../programs/CBACT01C.md) |
| [BR-048](BR-048.md) | Populate VB1 Record | Account data is extracted and formatted into a VB1 record. | [CBACT01C](../programs/CBACT01C.md) |
| [BR-049](BR-049.md) | Populate VB2 Record | When a specific condition is met (unspecified in provided co... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-051](BR-051.md) | Account Record Processing | The system processes account records based on their specific... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-052](BR-052.md) | Open Account Type 1 File | The program opens a specific output file for account records... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-053](BR-053.md) | Open Account Type 2 File | The program opens a specific output file for account records... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-054](BR-054.md) | Account File Open Status Check | If the account file fails to open, the archiving process can... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-055](BR-055.md) | Output File Open Status Check | If any of the output files fail to open, the archiving proce... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-057](BR-057.md) | Account Data Archiving | Account data is archived to specific output files based on t... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-060](BR-060.md) | File Status Display | The program displays the status of input and output files to... | [CBACT01C](../programs/CBACT01C.md) |
| [BR-061](BR-061.md) | Card File Read Successful | If a card record is successfully read from the input file, t... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-062](BR-062.md) | Card File End of File | When the end of the card input file is reached, the system c... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-063](BR-063.md) | Card File Open Successful | The card file must open successfully before processing can c... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-064](BR-064.md) | Card File Open Unsuccessful | If the card file cannot be opened, the batch process will te... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-065](BR-065.md) | Card File Close Successful | The card file must be closed successfully after processing a... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-066](BR-066.md) | Card File Close Unsuccessful | If the card file cannot be closed successfully, the program ... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-067](BR-067.md) | File Open Successful | The card file must open successfully before processing can c... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-068](BR-068.md) | File Read Successful | The card file must be read successfully to process card reco... | [CBACT02C](../programs/CBACT02C.md) |
| [BR-070](BR-070.md) | End of Cross-Reference File Processing | When the end of the card cross-reference file is reached, th... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-071](BR-071.md) | Cross-Reference File Open Successful | The cross-reference file must open successfully before proce... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-072](BR-072.md) | Cross-Reference File Read Successful | The cross-reference file must be read successfully. | [CBACT03C](../programs/CBACT03C.md) |
| [BR-073](BR-073.md) | Cross-Reference File Close Successful | The cross-reference file should be closed successfully at th... | [CBACT03C](../programs/CBACT03C.md) |
| [BR-081](BR-081.md) | Discount Group File Open Status Check | The program verifies that the Discount Group file has been s... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-082](BR-082.md) | Interest Rate File Open Status Check | The program verifies that the Interest Rate file has been su... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-094](BR-094.md) | Account ID Retrieval | If a card number is found in the cross-reference file, the c... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-098](BR-098.md) | Transaction Record Update | The transaction record is updated with specific values after... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-099](BR-099.md) | Transaction File Close Status Check | If the transaction file did not close successfully, an error... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-100](BR-100.md) | Account Balance File Close Status Check | If the account balance file did not close successfully, an e... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-101](BR-101.md) | Cross-Reference File Close Status Check | If the cross-reference file (linking card numbers to account... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-102](BR-102.md) | Transaction File Close Status Check | If the transaction file does not close successfully, the pro... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-103](BR-103.md) | Discount Group File Close Status Check | If the discount group file is not successfully closed, an er... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-104](BR-104.md) | Discount Group File Close Error Handling | If closing the discount group file fails, the program sets a... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-105](BR-105.md) | Transaction File Status Check | If the transaction file processing is incomplete, an error m... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-106](BR-106.md) | Account File Status Check | If the account file processing is incomplete, an error messa... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-109](BR-109.md) | I/O Status Display | The program displays the I/O status of file operations for d... | [CBACT04C](../programs/CBACT04C.md) |
| [BR-110](BR-110.md) | End of Customer File Processing | When all customer records have been processed, the system sh... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-111](BR-111.md) | Customer Record Read Error | If there is an error reading a customer record, the system s... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-112](BR-112.md) | Customer File Open Successful | The customer file must open successfully for processing to c... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-113](BR-113.md) | Customer File Open Unsuccessful | If the customer file cannot be opened, the program must term... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-114](BR-114.md) | Customer File Close Successful | The customer file is closed successfully. | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-115](BR-115.md) | Customer File Close Unsuccessful | If the customer file cannot be closed, an error handling rou... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-116](BR-116.md) | Abnormal Termination Handling | If an error occurs during processing, the system will execut... | [CBCUS01C](../programs/CBCUS01C.md) |
| [BR-117](BR-117.md) | Customer File Open Status Check | The export process cannot proceed if the customer file is no... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-118](BR-118.md) | Account File Open Status Check | The export process cannot proceed if the account file is not... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-119](BR-119.md) | Cross-Reference File Open Status Check | The export process cannot proceed if the cross-reference fil... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-120](BR-120.md) | Transaction File Open Status Check | The export process cannot proceed if the transaction file is... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-121](BR-121.md) | Export File Open Status Check | The export process cannot proceed if the export file is not ... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-122](BR-122.md) | Timestamp File Open Status Check | The export process cannot proceed if the timestamp file is n... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-124](BR-124.md) | Populate Customer Export Record | When creating a customer export record, populate the record ... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-125](BR-125.md) | Account Record Read Error | If there is an error reading an account record, the export p... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-126](BR-126.md) | Populate Account Export Record | Populate the account export record with data from the accoun... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-127](BR-127.md) | Cross-Reference Record Processing | If a cross-reference record is successfully read, process it... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-128](BR-128.md) | Populate Cross-Reference Export Record | When creating a cross-reference export record, populate it w... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-130](BR-130.md) | Populate Transaction Export Record | When creating a transaction export record, populate the reco... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-132](BR-132.md) | Populate Export Record - Customer Data | When creating an export record, populate the customer-relate... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-133](BR-133.md) | Populate Export Record - Account Data | When creating an export record, populate the account-related... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-134](BR-134.md) | Populate Export Record - Cross-Reference Data | When creating an export record, populate the cross-reference... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-135](BR-135.md) | Populate Export Record - Transaction Data | When creating an export record, populate the transaction-rel... | [CBEXPORT](../programs/CBEXPORT.md) |
| [BR-136](BR-136.md) | Process Customer Record | When a record from the import file is identified as a Custom... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-137](BR-137.md) | Process Account Record | When a record from the import file is identified as an Accou... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-138](BR-138.md) | Process Cross-Reference Record | When a record from the import file is identified as a Cross-... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-139](BR-139.md) | Process Transaction Record | When a record from the import file is identified as a Transa... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-140](BR-140.md) | Process Card Record | When a record from the import file is identified as a Card r... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-141](BR-141.md) | Handle Invalid Record Type | When a record from the import file has an unknown or invalid... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-143](BR-143.md) | Invalid Record Handling | If the system cannot identify the record type, the record is... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-144](BR-144.md) | Process Customer Record | When a record represents a customer, update the customer inf... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-145](BR-145.md) | Process Account Record | When a record represents an account, update the account info... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-146](BR-146.md) | Process Cross-Reference Record | When a record represents a cross-reference, update the cross... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-147](BR-147.md) | Process Transaction Record | When a record represents a transaction, update the transacti... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-148](BR-148.md) | Process Card Record | When a record represents a card, update the card information... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-149](BR-149.md) | Handle Invalid Record | When a record type is unknown or invalid, write the record t... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-150](BR-150.md) | Populate Customer Information | When processing a customer record, populate the customer's c... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-151](BR-151.md) | Set Account Status to Active | When processing an account record, the account's status is s... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-152](BR-152.md) | Populate Account Details | When processing an account record, the account details are p... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-153](BR-153.md) | Populate Cross-Reference Record | When processing a cross-reference record, populate the corre... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-154](BR-154.md) | Transaction Record Processing | When a transaction record is processed, the system updates t... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-155](BR-155.md) | Populate Card Details | When processing a card record, populate the card details in ... | [CBIMPORT](../programs/CBIMPORT.md) |
| [BR-158](BR-158.md) | Cross-Reference Record Found | When a cross-reference record is successfully read, the card... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-159](BR-159.md) | Handle Invalid Customer Status | If a customer's status is invalid, the system should proceed... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-160](BR-160.md) | Account Status Handling | The system must handle different account statuses appropriat... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-163](BR-163.md) | Cross-Reference File Open Successful | If the cross-reference file opens successfully, proceed to t... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-164](BR-164.md) | Cross-Reference File Open Unsuccessful | If the cross-reference file fails to open, the statement gen... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-165](BR-165.md) | Customer File Open Error | If the customer file cannot be opened, the statement generat... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-166](BR-166.md) | Account File Open Status Check | If the account file cannot be opened, the statement generati... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-168](BR-168.md) | Transaction Code Handling | Specific transaction codes trigger different descriptions to... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-169](BR-169.md) | Transaction File Close Status | If the transaction file is successfully closed, set the tran... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-170](BR-170.md) | Transaction File Close Status Unsuccessful | If the transaction file is not successfully closed, set the ... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-171](BR-171.md) | Cross-Reference File Close Status | If the cross-reference file is successfully closed, proceed ... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-172](BR-172.md) | Cross-Reference File Close Error | If the cross-reference file fails to close, stop the stateme... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-173](BR-173.md) | End of Customer File Processing | When the end of the customer file is reached, the program pr... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-174](BR-174.md) | Account File Closing Procedure | When the account file processing is complete, specific actio... | [CBSTM03A](../programs/CBSTM03A.md) |
| [BR-206](BR-206.md) | Transaction Record Read Failure | If a transaction record cannot be read from the daily transa... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-207](BR-207.md) | End of Daily Transaction File | When the end of the daily transaction file is reached, the p... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-210](BR-210.md) | Customer File Open Successful | The program must successfully open the customer file to proc... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-211](BR-211.md) | Customer File Open Unsuccessful | If the customer file cannot be opened, the transaction proce... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-212](BR-212.md) | Cross-Reference File Open Successful | The program must successfully open the cross-reference file ... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-213](BR-213.md) | Cross-Reference File Open Unsuccessful | If the cross-reference file cannot be opened, the transactio... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-214](BR-214.md) | Card File Open Status Check | If the card file fails to open, the transaction processing w... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-215](BR-215.md) | Card File Not Found Handling | If the card file is not found, the transaction processing wi... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-216](BR-216.md) | Account File Open Successful | The system must successfully open the account file before pr... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-217](BR-217.md) | Account File Open Unsuccessful | If the account file cannot be opened, the transaction proces... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-218](BR-218.md) | Transaction File Open Successful | The daily transaction file must open successfully for proces... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-219](BR-219.md) | Customer Cross-Reference File Open Successful | The customer cross-reference file must open successfully to ... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-220](BR-220.md) | Transaction File Closing Success | Ensure the daily transaction file is successfully closed. | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-221](BR-221.md) | Account File Closing Success | Ensure the account file is successfully closed. | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-224](BR-224.md) | Cross-Reference File Close Status Check | If the cross-reference file does not close successfully, the... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-225](BR-225.md) | Customer File Close Status Check | If the customer file does not close successfully, the progra... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-226](BR-226.md) | Card File Status Check | If the card file is not successfully closed, the transaction... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-232](BR-232.md) | Transaction File Read Error | If the program fails to read a transaction record, the batch... | [CBTRN01C](../programs/CBTRN01C.md) |
| [BR-233](BR-233.md) | Transaction File Open Successful | The daily transaction file must be successfully opened befor... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-234](BR-234.md) | Cross-Reference File Open Successful | The cross-reference file, used for validating transaction da... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-235](BR-235.md) | Transaction File Open Successful | The transaction file must open successfully for processing t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-236](BR-236.md) | Transaction File Open Unsuccessful | If the transaction file cannot be opened, the batch process ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-237](BR-237.md) | Cross-Reference File Open Successful | The program must successfully open the cross-reference file ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-238](BR-238.md) | Cross-Reference File Open Unsuccessful | If the program fails to open the cross-reference file, the t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-239](BR-239.md) | Transaction File Open Validation | The daily transaction file must be successfully opened befor... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-240](BR-240.md) | Reject File Open Validation | The reject file must be successfully opened before invalid t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-241](BR-241.md) | Account Record Found | If a matching account record is found in the account file, p... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-243](BR-243.md) | TCATBAL File Open Status Check | The program verifies that the Transaction Category Balance f... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-244](BR-244.md) | TCATBAL File Availability Check | The program checks if the Transaction Category Balance file ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-245](BR-245.md) | Transaction Record Validation | If a transaction record is read successfully from the input ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-246](BR-246.md) | End of Daily Transaction Processing | If the end of the daily transaction input file is reached, f... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-248](BR-248.md) | Invalid Transaction Record Handling | If a transaction record is determined to be invalid, write t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-251](BR-251.md) | Handle Zero Amount Transactions | If a transaction has a zero amount, it may be handled differ... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-258](BR-258.md) | Transaction Record Write Success | If a transaction record is successfully written to the outpu... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-259](BR-259.md) | Transaction Record Write Failure | If a transaction record cannot be written to the output file... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-261](BR-261.md) | Reject Invalid Transactions | If a transaction fails validation, it is written to a reject... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-262](BR-262.md) | Transaction File Status Check | If the transaction file processing was successful, proceed t... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-263](BR-263.md) | Transaction File Error Handling | If the transaction file processing encountered errors, bypas... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-266](BR-266.md) | Close Reject File After Processing | After processing all transaction records, the reject file mu... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-267](BR-267.md) | Account File Status Check | Verify the account file was successfully processed. | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-268](BR-268.md) | Transaction Category Balance File Status Check | Verify the transaction category balance file was successfull... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-269](BR-269.md) | TCATBAL File Status Check | If the transaction category balance file (TCATBAL) close ope... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-270](BR-270.md) | TCATBAL File Close Error Handling | If an error occurs during the closing of the transaction cat... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-271](BR-271.md) | File Status Display | The program displays the status of input/output operations f... | [CBTRN02C](../programs/CBTRN02C.md) |
| [BR-273](BR-273.md) | Transaction Type Processing | Different actions are taken based on the type of transaction... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-275](BR-275.md) | Transaction Amount Threshold | If a transaction amount exceeds a predefined threshold, it m... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-277](BR-277.md) | Page Overflow Check | If the current line count exceeds the maximum lines per page... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-278](BR-278.md) | Account Overflow Check | If the current page count exceeds the maximum pages per acco... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-281](BR-281.md) | Page Overflow Check | If the current line count on the report page exceeds the max... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-282](BR-282.md) | Account Overflow Check | If the current account number changes, print the account tot... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-286](BR-286.md) | High Value Transaction Handling | Transactions exceeding a certain value require special handl... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-287](BR-287.md) | Transaction Category Assignment | Transactions are categorized based on specific criteria to f... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-288](BR-288.md) | Transaction Data Enrichment | Transaction data is enhanced with additional information fro... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-291](BR-291.md) | Parameter File Required | The report generation requires a valid parameter file to def... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-292](BR-292.md) | Transaction File Status Check | If the transaction file does not close successfully, stop th... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-293](BR-293.md) | Report File Status Check | If the report file is not successfully closed, stop the repo... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-294](BR-294.md) | Transaction File Status Check | If the transaction file is not successfully closed, stop the... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-295](BR-295.md) | Card Cross-Reference File Status Check | If the card cross-reference file is not successfully closed,... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-296](BR-296.md) | Card Cross-Reference File Status Check | If the card cross-reference file is successfully closed, a c... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-298](BR-298.md) | Transaction Type Closure | When processing a specific transaction type, a closure proce... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-299](BR-299.md) | Transaction Category Closing Procedure | When processing of a specific transaction category is comple... | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-301](BR-301.md) | File Status Check | If a file operation fails, the program must stop. | [CBTRN03C](../programs/CBTRN03C.md) |
| [BR-309](BR-309.md) | Return to Previous Screen | The system allows the user to return to the previous screen ... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-312](BR-312.md) | Record Transaction | Every successful payment transaction must be recorded in the... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-315](BR-315.md) | Transaction File Status Check | If the transaction file is unavailable, the payment process ... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-316](BR-316.md) | Transaction File Read Status | If the attempt to read the previous transaction file is unsu... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-317](BR-317.md) | Transaction File Write Error | If writing the transaction record to the transaction history... | [COBIL00C](../programs/COBIL00C.md) |
| [BR-318](BR-318.md) | Menu Option Selection | The system determines the next action based on the user's me... | [COMEN01C](../programs/COMEN01C.md) |
| [BR-320](BR-320.md) | Transfer to Selected Program | Based on the user's menu selection, control is transferred t... | [COMEN01C](../programs/COMEN01C.md) |
| [BR-321](BR-321.md) | Return to Sign-On Screen | If the user chooses to return to the sign-on screen, the sys... | [COMEN01C](../programs/COMEN01C.md) |
| [BR-322](BR-322.md) | Transaction Report Submission | A user submits a transaction report request via an online sc... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-323](BR-323.md) | Report Request Submission | When the user presses the ENTER key, the system submits a re... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-324](BR-324.md) | Job Submission Confirmation | After submitting the report generation job, the system provi... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-325](BR-325.md) | Job Submission Confirmation | If the job submission to the internal reader is successful, ... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-326](BR-326.md) | Confirmation Screen Display | If writing job details to the temporary data queue is succes... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-327](BR-327.md) | Transaction Report Submission Confirmation | The system confirms the successful submission of a transacti... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-328](BR-328.md) | Transaction Report Request Processing | The system processes transaction report requests in the back... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-330](BR-330.md) | Return to Previous Screen | The system returns the user to the previous screen. | [CORPT00C](../programs/CORPT00C.md) |
| [BR-331](BR-331.md) | Transaction Report Submission | The system accepts a transaction report request from the use... | [CORPT00C](../programs/CORPT00C.md) |
| [BR-335](BR-335.md) | Successful Login - Populate Header | Upon successful validation of User ID and Password, populate... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-336](BR-336.md) | Successful Login - Proceed to Next Transaction | After successful login and header population, direct the use... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-340](BR-340.md) | Successful Authentication | If the User ID and Password are valid, the system should pop... | [COSGN00C](../programs/COSGN00C.md) |
| [BR-341](BR-341.md) | Transaction Display Limit Reached | If the maximum number of transactions that can be displayed ... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-342](BR-342.md) | Transaction Display Limit | The system limits the number of transactions displayed on a ... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-343](BR-343.md) | Transaction Data Formatting | Transaction data must be formatted in a specific way for dis... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-344](BR-344.md) | User Navigation | Users can navigate through the list of transactions using sp... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-345](BR-345.md) | Display Previous Page of Transactions | The system displays the previous page of transaction records... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-346](BR-346.md) | Display Next Page of Transactions | When the user presses the PF8 key, display the next page of ... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-348](BR-348.md) | Transaction Display - Page Forward Limit | The system determines if the last transaction has been displ... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-349](BR-349.md) | Prevent Paging Beyond First Page | The user cannot navigate to a previous page if they are alre... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-350](BR-350.md) | Transaction Data Population | Transaction details are retrieved and prepared for display o... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-351](BR-351.md) | Transaction Display Logic | The program determines which transactions to display based o... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-352](BR-352.md) | Return to Previous Screen | The system displays the previous screen of transaction data. | [COTRN00C](../programs/COTRN00C.md) |
| [BR-353](BR-353.md) | Transaction List Display | Display the transaction list on the user's terminal screen. | [COTRN00C](../programs/COTRN00C.md) |
| [BR-354](BR-354.md) | Transaction Display Logic | The system determines which set of transactions to display t... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-355](BR-355.md) | Transaction File End of File Handling | When the end of the transaction file is reached, the system ... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-356](BR-356.md) | Transaction File Read Error Handling | If an error occurs while reading the transaction file, the s... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-357](BR-357.md) | Transaction File End of File Handling | When attempting to read the previous transaction, if the beg... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-358](BR-358.md) | Transaction File Read Error Handling | If an error occurs while attempting to read the previous tra... | [COTRN00C](../programs/COTRN00C.md) |
| [BR-360](BR-360.md) | Return to Previous Screen | If the user presses the 'Return' key, the system should navi... | [COTRN01C](../programs/COTRN01C.md) |
| [BR-361](BR-361.md) | Return to Previous Screen | The system allows the user to return to the previous screen. | [COTRN01C](../programs/COTRN01C.md) |
| [BR-362](BR-362.md) | Transaction Record Not Found | If a transaction record cannot be found, display an error me... | [COTRN01C](../programs/COTRN01C.md) |
| [BR-363](BR-363.md) | Transaction Record Creation | A new transaction record is created and added to the TRANSAC... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-364](BR-364.md) | Transaction Data Copy | Transaction data is copied for potential reuse in subsequent... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-365](BR-365.md) | Data Entry Assistance | Related information from CXACAIX and CCXREF files is retriev... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-366](BR-366.md) | Transaction Type Validation | The system determines the subsequent processing steps based ... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-367](BR-367.md) | Transaction Type A Processing | If the transaction type is 'A', the system performs specific... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-368](BR-368.md) | Transaction Type B Processing | If the transaction type is 'B', the system performs specific... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-369](BR-369.md) | Transaction Type C Processing | If the transaction type is 'C', the system performs specific... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-370](BR-370.md) | Transaction Type D Processing | If the transaction type is 'D', the system performs specific... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-378](BR-378.md) | Copy Last Transaction Data | The system copies the last entered transaction data to pre-p... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-379](BR-379.md) | Return to Previous Screen | The system returns the user to the previous screen after pro... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-382](BR-382.md) | Transaction File Read Error | If there is a problem accessing the transaction file, inform... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-383](BR-383.md) | Transaction File Not Found | If the transaction file cannot be found, inform the user. | [COTRN02C](../programs/COTRN02C.md) |
| [BR-384](BR-384.md) | Transaction File Permanent Error | If a permanent error occurs while accessing the transaction ... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-385](BR-385.md) | Transaction File Read Error | If there is an error reading the previous transaction file, ... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-386](BR-386.md) | Transaction File Not Found | If the previous transaction file is not found, the system wi... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-387](BR-387.md) | Transaction File Write Success | If writing the transaction record to the TRANSACT file is su... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-388](BR-388.md) | Transaction File Write Error | If writing the transaction record to the TRANSACT file fails... | [COTRN02C](../programs/COTRN02C.md) |
| [BR-389](BR-389.md) | Display User Data | User data is prepared for display on the terminal screen. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-390](BR-390.md) | Display Next Page of Users | When the user requests the next page of user data, display t... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-391](BR-391.md) | Display Previous Page of Users | When the user requests the previous page of user data, displ... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-392](BR-392.md) | Return to Previous Menu | When the user requests to return to the previous menu, termi... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-393](BR-393.md) | Display Next Page | If the user presses the PF7 key, display the next page of us... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-394](BR-394.md) | Display Previous Page | If the user presses the PF7 key, display the previous page o... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-395](BR-395.md) | Display Next Page | If the user presses the PF8 key, display the next page of us... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-396](BR-396.md) | End of User List | The user cannot page forward if they are already viewing the... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-397](BR-397.md) | Prevent Paging Beyond First Page | The user cannot page backward if they are already on the fir... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-398](BR-398.md) | User Status Determination | The system determines the status of a user based on a specif... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-400](BR-400.md) | Display User List | Display a list of users from the security file on the termin... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-401](BR-401.md) | Page Forward Through User List | Allow the user to page forward through the list of users. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-402](BR-402.md) | Page Backward Through User List | Allow the user to page backward through the list of users. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-403](BR-403.md) | Return to Previous Screen | Allow the user to return to the previous screen (presumably ... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-404](BR-404.md) | Return to Previous Screen | When the user chooses to return to the previous screen, the ... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-405](BR-405.md) | Display User List | The system displays a list of users from the security file o... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-406](BR-406.md) | Page Through User List | The user can navigate through the list of users. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-407](BR-407.md) | Return to Previous Screen | The user can return to the previous screen. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-408](BR-408.md) | Handle Errors and Display Messages | The system handles errors and displays messages to the user. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-410](BR-410.md) | Display User Record | Display the user's record on the terminal screen. | [COUSR00C](../programs/COUSR00C.md) |
| [BR-411](BR-411.md) | Handle End of File | Inform the user that the end of the user list has been reach... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-412](BR-412.md) | Handle File Read Error | Inform the user that there was an error reading the user lis... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-413](BR-413.md) | Display Previous User Record | The system retrieves and displays the previous user record f... | [COUSR00C](../programs/COUSR00C.md) |
| [BR-419](BR-419.md) | Clear Screen and Return | After processing, the system clears the input screen and ret... | [COUSR01C](../programs/COUSR01C.md) |
| [BR-421](BR-421.md) | Data Movement | Data is moved from one location to another. | [COUSR02C](../programs/COUSR02C.md) |
| [BR-423](BR-423.md) | Security Record Update | The system updates the user's security record with the valid... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-424](BR-424.md) | Display Updated Information | The system displays the updated profile information to the u... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-426](BR-426.md) | Profile Update Confirmation | The user must confirm the changes to their profile informati... | [COUSR02C](../programs/COUSR02C.md) |
| [BR-427](BR-427.md) | Clear Screen Messages | The system clears the screen message fields. | [COUSR02C](../programs/COUSR02C.md) |
| [BR-434](BR-434.md) | Security Record Deletion | When a user account is deleted, the corresponding security r... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-435](BR-435.md) | General Information Deletion | When a user account is deleted, the user's general informati... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-436](BR-436.md) | User Deletion Confirmation | The system must confirm the user's intent to delete a user a... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-439](BR-439.md) | User Deletion Confirmation | The system must confirm the user's intention to delete a use... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-442](BR-442.md) | Return to Previous Screen | After deleting a user account, the system returns the user t... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-443](BR-443.md) | User Security Record Not Found | If a user's security record cannot be found, the user cannot... | [COUSR03C](../programs/COUSR03C.md) |
| [BR-444](BR-444.md) | User Security Record Deletion Status | The system must confirm the successful deletion of the user'... | [COUSR03C](../programs/COUSR03C.md) |



---

*Generated 2026-05-12 12:31*