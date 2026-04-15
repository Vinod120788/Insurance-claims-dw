# SKILL: Data Cleaning — Insurance Claims

## Purpose
Reads raw Excel source data, removes blank rows, standardises 
data types, and outputs clean CSV files ready for the 
data warehouse loader.

## Script
`sql/01_clean_raw_data.py`

## When to Use This Skill
Run this script any time the source Excel file is updated 
with new data. Always run this before running the warehouse 
loader.

## What It Does — Step by Step

| Step | Action | Why |
|------|--------|-----|
| 1 | Load all 4 Excel sheets | Read raw source data |
| 2 | Drop unnamed index column | Removes Excel artefact |
| 3 | Remove blank rows | 119 empty rows removed from Claim Table |
| 4 | Parse date columns | Converts text dates to proper date objects |
| 5 | Calculate Resolution Days | New KPI: Claim Closed Date minus Claim Create Date |
| 6 | Capitalise Gender values | Standardises "male" → "Male" |
| 7 | Strip whitespace | Removes invisible spaces from text fields |
| 8 | Export to CSV | Saves 4 clean files to data/clean/ |

## Inputs
| File | Sheet | Rows |
|------|-------|------|
| data/raw/Dataset3.xlsx | Claim Table | 7,967 |
| data/raw/Dataset3.xlsx | Customer Table | 10,000 |
| data/raw/Dataset3.xlsx | Handler Table | 500 |
| data/raw/Dataset3.xlsx | Policy Table | 10,000 |

## Outputs
| File | Clean Rows |
|------|-----------|
| data/clean/claims_clean.csv | 7,838 |
| data/clean/customers_clean.csv | 10,000 |
| data/clean/handlers_clean.csv | 500 |
| data/clean/policies_clean.csv | 10,000 |

## Key Design Decisions
- Blank rows identified by NULL Claim Number (not row index)
- Resolution Days calculated here rather than in DAX for 
  performance — computed once at load time, not on every 
  dashboard interaction
- CountryFull column dropped — all records are Australian, 
  column adds no analytical value

## How to Run
```powershell
python sql/01_clean_raw_data.py
```

## Dependencies
- Python 3.11+
- pandas 2.x
- openpyxl