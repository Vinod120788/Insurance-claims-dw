# Insurance Claims Data Warehouse & Dashboard

## Project Overview
An end-to-end data engineering and analytics project built on Australian
auto insurance data. This project demonstrates a full data warehouse
pipeline — from raw Excel source data through SQL transformation to
interactive Power BI dashboards.

## Dataset
- **Source:** Australian auto insurance claims (2015–2019)
- **Volume:** ~7,800 claims, 10,000 customers, 500 handlers, 10,000 policies
- **Tables:** Claim, Customer, Handler, Policy

## Project Structure
| Folder | Contents |
|--------|----------|
| `data/raw/` | Original source data (unmodified) |
| `sql/` | Data cleaning and star schema SQL scripts |
| `skills/` | SKILL.md documentation for each script |
| `powerbi/` | Dashboard .pbix file and DAX measures reference |
| `docs/` | Schema diagrams and data dictionary |

## Key Metrics Built
- Claim volume and trend over time
- Loss ratio (total claims paid vs premiums collected)
- Average claim resolution time (days to close)
- SLA breach rate by incident type
- Handler performance benchmarking
- Customer segment analysis (Gold / Silver / Platinum)

## Tools Used
- SQL (data warehouse design and transformation)
- Python (data validation and cleaning)
- Power BI Desktop (dashboards and DAX measures)
- Git / GitHub (version control)

## How to Run
1. Clone the repo: `git clone https://github.com/Vinod120788/Insurance-claims-dw.git`
2. Run SQL scripts in order (see `sql/README.md`)
3. Open `powerbi/dashboard.pbix` in Power BI Desktop

## Dashboard Pages

### Page 1 — Claims Overview
- Total claims: 7,838 across 2015–2019
- Claims volume grew 100% over 5 years
- All 4 incident types evenly distributed (~25% each)
- Total payout: AUD $232.89M

### Page 2 — Financial Summary
- Avg claim value: $29,710
- High severity claims: 4,000+ (51% of total)
- Multi-vehicle collision = highest cost incident type
- Major Damage = 41% of all payouts
- Data limitation: Loss Ratio flagged for future enrichment

### Page 3 — Resolution Performance
- Avg resolution: 36 days (SLA target: 30 days)
- SLA breach rate: 46.2% — consistent across all years
- Multi-vehicle collision slowest to resolve (38 days)
- Handler scatter chart shows team-wide SLA breach pattern

## Key Insights Discovered
1. Claims volume doubled 2015–2019 but payout tripled —
   individual claims are getting more expensive over time
2. 46% SLA breach rate is consistent year-over-year —
   indicates a structural process problem, not individual
   handler performance
3. Multi-vehicle collision costs significantly more than
   other incident types despite equal claim frequency
4. High severity claims = 51% of all claims —
   significant risk concentration for the business