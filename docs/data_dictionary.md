# Data Dictionary — Insurance Claims Data Warehouse

## claims_clean (Fact Table)
| Column | Type | Description |
|--------|------|-------------|
| Claim Number | Integer | Unique identifier for each claim |
| Customer ID | Integer | Links to customers_clean |
| Policy Number | Integer | Links to policies_clean |
| Handler ID | Integer | Links to handlers_clean |
| Incident Date | Date | Date the incident occurred |
| Claim Create Date | Date | Date the claim was lodged |
| Claim Closed Date | Date | Date the claim was resolved |
| Handler Assigned Date | Date | Date a handler was allocated |
| Incident Type | Text | Parked Car / Multi-vehicle Collision / Vehicle Theft / Single Vehicle Collision |
| Incident Severity | Text | Trivial Damage / Minor Damage / Major Damage / Total Loss |
| No of Vehicles Involved | Integer | Number of vehicles in the incident |
| Number of Customer Contacts | Integer | How many times customer contacted the company |
| Injury Claim | Decimal | AUD payout for personal injury |
| Property Claim | Decimal | AUD payout for property damage |
| Vehicle Claim | Decimal | AUD payout for vehicle damage |
| Resolution Days | Integer | Calculated: Claim Closed Date minus Claim Create Date |

---

## customers_clean (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| Customer ID | Integer | Unique customer identifier |
| GivenName | Text | Customer first name |
| Surname | Text | Customer last name |
| Gender | Text | Male / Female |
| Age | Integer | Customer age at time of data extract |
| City | Text | Customer city of residence |
| State | Text | Australian state abbreviation (e.g. NSW, VIC) |
| StateFull | Text | Full state name |
| Segment | Text | Customer tier — Gold / Silver / Platinum |
| Policy Number | Integer | Links to policies_clean |

---

## policies_clean (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| Policy Number | Integer | Unique policy identifier |
| Policy Create Date | Date | Date the policy was issued |
| Policy Expiration Date | Date | Date the policy expires |
| Annual Premium | Decimal | Yearly premium amount in AUD |
| Excess | Decimal | Customer deductible amount in AUD |

---

## handlers_clean (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| Handler ID | Integer | Unique handler identifier |
| GivenName | Text | Handler first name |
| Surname | Text | Handler last name |
| Team No | Integer | Team number (1–5) |
| Reporting Manager | Text | Name of the handler's manager |
| Experience (In Years) | Integer | Years of experience in claims handling |

---

## Derived / Calculated Fields
| Field | Where Created | Formula |
|-------|--------------|---------|
| Resolution Days | Python cleaning script | Claim Closed Date − Claim Create Date |
| TotalClaimAmount | SQL warehouse loader | Injury + Property + Vehicle Claim |
| FullName | SQL warehouse loader | GivenName + " " + Surname |
| DimDate table | Power BI DAX | CALENDAR(2015-01-01, 2019-12-31) |