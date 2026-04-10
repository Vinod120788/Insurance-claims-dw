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
