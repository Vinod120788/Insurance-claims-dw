# SKILL: Master Data Analytics Playbook
## Version: 1.0 | Author: Vinod Ganeshan
## Purpose: Repeatable end-to-end data analytics workflow
## Use this file every time you start a new data project

---

# THE GOLDEN RULE
> The data changes. The process never does.
> Follow these phases in order, every single time.

---

# PHASE 0 — PROJECT SETUP
## Goal: Professional foundation before touching any data

### 0.1 — Create GitHub Repository
- Name: descriptive-and-lowercase (e.g. `insurance-claims-dw`)
- Visibility: Public
- Initialise with: README, .gitignore (Python), MIT License
- Add description: one sentence explaining what the project does

### 0.2 — Clone and create folder structure
```powershell
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
mkdir data\raw, data\clean, sql, skills, powerbi, docs
```

### 0.3 — Create placeholder READMEs in each folder
```powershell
echo "# Raw source data" > data\raw\README.md
echo "# SQL scripts" > sql\README.md
echo "# Skill documentation" > skills\README.md
echo "# Power BI files" > powerbi\README.md
echo "# Diagrams and documentation" > docs\README.md
```

### 0.4 — Copy raw data into data/raw/
- NEVER modify the original file
- ALWAYS work from copies or clean exports

### 0.5 — First commit
```powershell
git add .
git commit -m "Initial project structure and README"
git push origin main
```

### Phase 0 Checklist
- [ ] GitHub repo created with description
- [ ] All 5 folders created
- [ ] Raw data copied to data/raw/
- [ ] First commit pushed successfully

---

# PHASE 1 — DATA VALIDATION
## Goal: Understand what you have before writing any code

### 1.1 — Questions to answer about every dataset
Run this Python script on any new Excel/CSV file:

```python
import pandas as pd
import os

# Load the file
df = pd.read_excel("data/raw/YOUR_FILE.xlsx", sheet_name=None)

for sheet_name, data in df.items():
    print(f"\n{'='*50}")
    print(f"Sheet: {sheet_name}")
    print(f"Rows: {len(data)}, Columns: {len(data.columns)}")
    print(f"Columns: {list(data.columns)}")
    print(f"\nNull counts:")
    print(data.isnull().sum())
    print(f"\nData types:")
    print(data.dtypes)
    print(f"\nSample (3 rows):")
    print(data.head(3))
```

### 1.2 — Validation checklist for every dataset
- [ ] How many sheets / tables?
- [ ] How many rows and columns per table?
- [ ] Are there blank rows? (check with isnull)
- [ ] Are there duplicate rows?
- [ ] What are the date columns? Are they dates or text?
- [ ] What columns link tables together? (the join keys)
- [ ] Do all join keys match across tables? (orphan check)
- [ ] What are the numeric ranges? (min, max, avg)
- [ ] Are there categorical columns? What are the unique values?
- [ ] What percentage of each column is null?

### 1.3 — Null handling decision rules
| Null % | Strategy | Action |
|--------|----------|--------|
| 0–5% | Minimal | Drop null rows if key field, fill if non-key |
| 5–30% | Moderate | Fill with mean (numbers) or mode (categories) |
| 30–50% | Significant | Flag column, decide if it is needed |
| 50%+ | Critical | Drop column OR document limitation |

### 1.4 — Commit after validation
```powershell
git add .
git commit -m "Add data validation findings"
git push origin main
```

---

# PHASE 2 — DATA CLEANING
## Goal: Clean, standardised CSVs ready for the warehouse

### 2.1 — Standard cleaning script template
Save as `sql/01_clean_raw_data.py`:

```python
import pandas as pd
import os

RAW_FILE   = os.path.join("data", "raw", "YOUR_FILE.xlsx")
OUTPUT_DIR = os.path.join("data", "clean")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load all sheets
sheets = pd.read_excel(RAW_FILE, sheet_name=None)

# 2. For each sheet:
for name, df in sheets.items():
    # Remove unnamed index columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    
    # Remove fully blank rows
    df = df.dropna(how="all")
    
    # Strip whitespace from text columns
    text_cols = df.select_dtypes(include="object").columns
    df[text_cols] = df[text_cols].apply(lambda x: x.str.strip())
    
    # Parse date columns (adjust column names)
    # df["DateColumn"] = pd.to_datetime(df["DateColumn"], errors="coerce")
    
    # Calculate derived columns (adjust as needed)
    # df["Days"] = (df["EndDate"] - df["StartDate"]).dt.days
    
    # Save clean CSV
    clean_name = name.lower().replace(" ", "_") + "_clean.csv"
    df.to_csv(os.path.join(OUTPUT_DIR, clean_name), index=False)
    print(f"Saved {clean_name}: {len(df)} rows")

print("Cleaning complete.")
```

### 2.2 — Cleaning checklist
- [ ] Blank rows removed
- [ ] Unnamed columns dropped
- [ ] All date columns parsed as datetime
- [ ] Text columns stripped of whitespace
- [ ] Categorical values standardised (e.g. Male/Female not male/MALE)
- [ ] Derived columns calculated (e.g. Resolution Days)
- [ ] Clean CSVs saved to data/clean/
- [ ] Row counts verified before and after

### 2.3 — Document this as a SKILL
Create `skills/SKILL_cleaning.md` with:
- What each step does and WHY
- Input files and output files
- Row counts before and after
- Any decisions made about nulls

### 2.4 — Commit
```powershell
git add .
git commit -m "Add data cleaning script and clean CSV output"
git push origin main
```

---

# PHASE 3 — DATA WAREHOUSE DESIGN
## Goal: Star schema SQL structure

### 3.1 — Identify your tables
Ask these questions:
- What is the MAIN EVENT being tracked?
  → This becomes your FACT table (one row per event)
- What DESCRIBES the event?
  → These become DIMENSION tables (who, when, where, what)

### 3.2 — Star schema rules
| Rule | Why |
|------|-----|
| Fact table has FK columns pointing to all dimensions | Enables joins |
| Dimension tables have one PK (unique ID) | No duplicates |
| All relationships are Many-to-One (* → 1) | Correct cardinality |
| Filter direction is Single (dim → fact) | Prevents circular logic |
| One date dimension covers all date columns | Time intelligence |

### 3.3 — Standard SQL template
Save as `sql/02_create_star_schema.sql`:

```sql
-- Fact Table (centre of the star)
CREATE TABLE IF NOT EXISTS FactEvents (
    EventKey        INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Foreign keys (one per dimension)
    DimensionAKey   INTEGER REFERENCES DimA(DimAKey),
    DateKey         INTEGER REFERENCES DimDate(DateKey),
    -- Measures (the numbers)
    Amount          REAL,
    Quantity        INTEGER,
    -- Calculated fields
    DaysToComplete  INTEGER
);

-- Date Dimension (always needed)
CREATE TABLE IF NOT EXISTS DimDate (
    DateKey     INTEGER PRIMARY KEY,
    FullDate    DATE NOT NULL,
    Day         INTEGER,
    Month       INTEGER,
    MonthName   TEXT,
    Quarter     INTEGER,
    Year        INTEGER,
    DayOfWeek   TEXT
);
```

### 3.4 — Document as a SKILL
Create `skills/SKILL_star_schema.md` with:
- Schema diagram (table names and join columns)
- Why each table was designed that way
- Verification row counts after load

### 3.5 — Commit
```powershell
git add .
git commit -m "Add star schema SQL design"
git push origin main
```

---

# PHASE 4 — POWER BI DASHBOARD
## Goal: 3-page interactive dashboard

### 4.1 — Connect data
- Open Power BI Desktop
- Get Data → Text/CSV → load each file from data/clean/
- Do NOT sign in — click "Maybe later"

### 4.2 — Set up relationships (Model view)
- Drag join keys between tables
- Every relationship: Many-to-one (*:1), Single direction
- Create DimDate using DAX:
```dax
DimDate = ADDCOLUMNS(
    CALENDAR(DATE(YYYY,1,1), DATE(YYYY,12,31)),
    "Year",      YEAR([Date]),
    "Month",     MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "Quarter",   QUARTER([Date]),
    "DayOfWeek", FORMAT([Date], "DDDD"),
    "MonthYear", FORMAT([Date], "MMM YYYY"),
    "YearMonth", YEAR([Date])*100 + MONTH([Date])
)
```

### 4.3 — Create _Measures table
- Modeling → Enter Data → name it `_Measures` → Load
- Right-click `_Measures` → New measure for each DAX formula

### 4.4 — Standard DAX measures (adapt column names)
```dax
-- Volume
Total Records = COUNTROWS(FactTable)

-- Sum of value
Total Value = SUM(FactTable[ValueColumn])

-- Average of a duration
Avg Duration = AVERAGE(FactTable[DurationColumn])

-- Safe division
Rate % = DIVIDE([Numerator], [Denominator], 0) * 100

-- Filtered count
High Priority Count = 
CALCULATE([Total Records],
    FactTable[PriorityColumn] = "High")

-- SLA / threshold breach
Breach Rate % = 
VAR Breached = COUNTROWS(
    FILTER(FactTable, FactTable[Duration] > 30))
RETURN DIVIDE(Breached, [Total Records], 0) * 100
```

### 4.5 — Standard 3-page layout
| Page | Purpose | Visuals |
|------|---------|---------|
| Page 1: Overview | Headline numbers + trends | 4 KPI cards, line chart by year, donut by category |
| Page 2: Financial/Value | Money and cost analysis | Bar chart by category, column chart by year, donut by subcategory |
| Page 3: Performance | Efficiency and SLA | KPI cards, scatter chart, bar chart, trend line |

### 4.6 — Visual formatting standards
- Add title text box to every page (font 16, bold)
- Add data labels to all bar and column charts
- Add a note box for any data limitations
- Consistent background colour across all pages
- Card borders styled consistently

### 4.7 — Document as a SKILL
Create `skills/SKILL_dax_measures.md` with:
- Every measure listed with formula and plain English explanation
- DAX concepts used and what they do
- Any data limitations found

### 4.8 — Commit after each page
```powershell
git add .
git commit -m "Add Page 1 - Overview dashboard"
git push origin main
```

---

# PHASE 5 — DOCUMENTATION
## Goal: Anyone can understand and reproduce your work

### 5.1 — Files to complete in every project
| File | Location | Contents |
|------|----------|----------|
| README.md | Root | Project overview, structure, how to run, insights |
| SKILL_cleaning.md | skills/ | Cleaning logic and decisions |
| SKILL_star_schema.md | skills/ | Schema design and load process |
| SKILL_dax_measures.md | skills/ | All DAX measures explained |
| data_dictionary.md | docs/ | Every column in every table defined |
| schema_notes.md | docs/ | Design decisions and future enhancements |
| README.md | sql/ | Run order and dependencies |
| README.md | powerbi/ | How to open and use the dashboard |

### 5.2 — README.md root template
```markdown
# Project Name

## Project Overview
One paragraph explaining what this project does and why.

## Dataset
- Source: where the data came from
- Volume: rows, tables, date range
- Domain: what industry/topic

## Project Structure
| Folder | Contents |
|--------|----------|
| data/raw/ | Original unmodified data |
| data/clean/ | Cleaned CSV files |
| sql/ | Cleaning and warehouse scripts |
| skills/ | SKILL.md documentation |
| powerbi/ | Dashboard file |
| docs/ | Data dictionary and schema notes |

## Tools Used
- Python / Pandas
- SQL / SQLite
- Power BI Desktop
- Git / GitHub

## How to Run
1. `python sql/01_clean_raw_data.py`
2. `python sql/03_load_warehouse.py`
3. Open `powerbi/dashboard.pbix`

## Dashboard Pages
### Page 1 — Overview
### Page 2 — Financial/Value Summary
### Page 3 — Performance

## Key Insights Discovered
1. Insight one
2. Insight two
3. Insight three
```

### 5.3 — Final commit
```powershell
git add .
git commit -m "Complete project documentation"
git push origin main
```

---

# PHASE 6 — GIT COMMIT HABIT
## Goal: Professional version control throughout

### 6.1 — Standard routine (run after every piece of work)
```powershell
git status                          # see what changed
git add .                           # stage everything
git commit -m "Describe what you did"   # save it
git push origin main                # upload to GitHub
```

### 6.2 — Good commit message examples
| Bad | Good |
|-----|------|
| "update" | "Add data cleaning script for claims table" |
| "fix" | "Fix null handling in Resolution Days calculation" |
| "changes" | "Add Page 2 Financial Summary to dashboard" |
| "done" | "Complete project documentation and README" |

### 6.3 — When to commit
- After setting up project structure
- After validating the data
- After finishing the cleaning script
- After building the warehouse
- After each dashboard page
- After writing documentation
- Whenever you finish a logical piece of work

---

# QUICK REFERENCE — TOOLS AND THEIR PURPOSE
| Tool | When to use it | What it does |
|------|---------------|-------------|
| Python / Pandas | Phase 1 & 2 | Validate and clean raw data |
| SQL / SQLite | Phase 3 | Build structured data warehouse |
| Power BI Desktop | Phase 4 | Visualise and analyse clean data |
| DAX | Phase 4 | Write formulas for KPIs and measures |
| Markdown | Phase 5 | Document everything |
| Git / GitHub | All phases | Save and version every step |

---

# CHECKLIST — PROJECT COMPLETE WHEN:
- [ ] Raw data in data/raw/ (untouched)
- [ ] Clean CSVs in data/clean/
- [ ] SQL schema defined
- [ ] Data warehouse loaded and verified
- [ ] Power BI connected to clean CSVs
- [ ] Star schema relationships set (all Many-to-one, Single)
- [ ] DimDate created in Power BI
- [ ] _Measures table with all DAX measures
- [ ] 3 dashboard pages built and formatted
- [ ] All SKILL.md files written
- [ ] data_dictionary.md complete
- [ ] Root README.md complete with insights
- [ ] All folder READMEs filled
- [ ] Final commit pushed to GitHub
- [ ] GitHub repo public and accessible