# SKILL: Star Schema — Insurance Data Warehouse

## Purpose
Defines and loads a star schema data warehouse using SQLite,
structured for efficient Power BI reporting on insurance 
claims data.

## Scripts
- `sql/02_create_star_schema.sql` — table definitions
- `sql/03_load_warehouse.py`      — data loader

## Star Schema Design

The warehouse follows a star schema pattern:
- **FactClaims** sits in the centre (one row per claim)
- Four dimension tables surround it, each connected by a key

## Tables
| Table | Type | Rows | Connects via |
|-------|------|------|-------------|
| FactClaims | Fact | 7,838 | Centre table |
| DimCustomer | Dimension | 10,000 | Customer ID |
| DimPolicy | Dimension | 10,000 | Policy Number |
| DimHandler | Dimension | 500 | Handler ID |
| DimDate | Dimension | 1,836 | Incident Date |

### FactClaims (centre of the star)
One row per claim. Stores all numeric measures and 
foreign keys linking to dimension tables.

| Column | Type | Description |
|--------|------|-------------|
| ClaimKey | INT PK | Surrogate key |
| CustomerKey | INT FK | Links to DimCustomer |
| PolicyKey | INT FK | Links to DimPolicy |
| HandlerKey | INT FK | Links to DimHandler |
| DateKey | INT FK | Links to DimDate |
| InjuryClaim | REAL | AUD payout — injury |
| PropertyClaim | REAL | AUD payout — property |
| VehicleClaim | REAL | AUD payout — vehicle |
| TotalClaimAmount | REAL | Sum of all three payouts |
| ResolutionDays | INT | Days from create to close |

### DimCustomer
One row per customer. Descriptive attributes only.
Key fields: CustomerID, Segment, State, Age, Gender

### DimPolicy
One row per insurance policy.
Key fields: PolicyNumber, AnnualPremium, Excess

### DimHandler
One row per claims handler (staff member).
Key fields: HandlerID, FullName, TeamNo, ExperienceYears

### DimDate
One row per unique date in the dataset.
Key fields: DateKey (YYYYMMDD), Year, Quarter, Month, DayOfWeek

## Why SQLite?
SQLite is a lightweight, file-based database — no server 
installation required. Ideal for portfolio projects and 
prototyping. The same schema would work in PostgreSQL or 
SQL Server with minimal changes.

## Verification Results (on load)
| Check | Result |
|-------|--------|
| Total claims | 7,838 |
| Unique customers | 10,000 |
| Unique policies | 10,000 |
| Unique handlers | 500 |
| Unique dates | 1,836 |
| Avg resolution days | 36.1 |
| Total payout (AUD) | $232,891,533 |

## How to Run
```powershell
# Step 1 — clean the data first
python sql/01_clean_raw_data.py

# Step 2 — build and load the warehouse
python sql/03_load_warehouse.py
```