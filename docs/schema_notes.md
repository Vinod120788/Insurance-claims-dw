# Star Schema Design Notes

## Architecture Decision
This project uses a star schema — the industry standard for 
analytical (OLAP) databases and Power BI reporting.

## Why Star Schema over a flat table?
| Flat Table | Star Schema |
|-----------|-------------|
| One giant table with all columns | Fact + dimension tables |
| Slow for aggregations | Fast for aggregations |
| Lots of repeated data (customer name on every claim row) | Each customer stored once |
| Hard to filter and slice | Designed for slicing and filtering |
| Difficult to maintain | Easy to extend |

## Table Relationships
| From | Column | To | Column | Type |
|------|--------|----|--------|------|
| claims_clean | Customer ID | customers_clean | Customer ID | Many-to-one |
| claims_clean | Policy Number | policies_clean | Policy Number | Many-to-one |
| claims_clean | Handler ID | handlers_clean | Handler ID | Many-to-one |
| claims_clean | Incident Date | DimDate | Date | Many-to-one |

## Design Decisions

### Why SQLite?
Chosen for portability — no server installation required.
The same SQL schema works in PostgreSQL or SQL Server
with minimal syntax changes.

### Why CSV files for Power BI?
Power BI Desktop requires a driver installation to connect
to SQLite directly. CSVs from data/clean/ provide identical
data with zero configuration overhead — standard practice
for portfolio and prototyping projects.

### Why a separate _Measures table in Power BI?
Storing all DAX measures in one dedicated table keeps the
data model clean. Measures scattered across fact and
dimension tables are hard to find and maintain.

### SLA Threshold — 30 days
The 30-day resolution target is an industry standard for
straightforward auto insurance claims. In production this
value would be confirmed with the operations team and
stored as a configurable parameter rather than hardcoded.

### Loss Ratio — Data Limitation
The policies_clean table contains no date column linking
premiums to specific years. This prevents accurate year-
over-year Loss Ratio calculation. Flagged for enrichment
in future data iterations.

## Future Enhancements
- Add claim date to policies table for accurate Loss Ratio
- Build customer segmentation analysis page in Power BI
- Add geographic map visual using State field
- Automate data refresh using Python scheduler
- Migrate from SQLite to PostgreSQL for production use