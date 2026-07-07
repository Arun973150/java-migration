# Business Rules Catalog

> **Total Rules:** 16  
> **Categories:** 3

---

## CALCULATION (4 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-002](BR-002.md) | Time Component Extraction | The system must break down the authentication time into its ... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-005](BR-005.md) | Time Component Extraction | The system must break down the authentication time into its ... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-009](BR-009.md) | Authorization Record Expiry | An authorization record expires on a calculated date based o... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-013](BR-013.md) | Expiry Date Calculation | Calculate the expiry date for each authorization record base... | [DBUNLDGS](../programs/DBUNLDGS.md) |

## VALIDATION (5 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-001](BR-001.md) | Authentication Time Validation | The system must validate the authentication time to ensure i... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-004](BR-004.md) | Authentication Time Validation | The system must validate the authentication time to ensure i... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-008](BR-008.md) | Error Handling for Authentication Time Update | The system must set an error flag if there is an issue updat... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-011](BR-011.md) | Authorization Summary Data Validation | Authorization summary data must meet specific criteria befor... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-012](BR-012.md) | Authorization Record Validation | Only process authorization records that meet specific criter... | [DBUNLDGS](../programs/DBUNLDGS.md) |

## WORKFLOW (7 rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
| [BR-003](BR-003.md) | Error Flag Setting | The system must set an error flag if the authentication time... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-006](BR-006.md) | Authentication Time Update | The system must update the authentication time for auditing ... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-007](BR-007.md) | Update Authentication Time | The system must update the user's last authentication time w... | [COPAUS2C](../programs/COPAUS2C.md) |
| [BR-010](BR-010.md) | Parent Segment Insertion | A parent segment must be inserted into the target system bef... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-014](BR-014.md) | Segment Insertion Rule | Insert parent and child segments into the target system for ... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-015](BR-015.md) | Parent Segment Insertion | Insert parent segments into the target system during the aut... | [DBUNLDGS](../programs/DBUNLDGS.md) |
| [BR-016](BR-016.md) | Insert Child Segment | A child segment must be inserted into the target system for ... | [DBUNLDGS](../programs/DBUNLDGS.md) |



---

*Generated 2026-03-16 19:39*