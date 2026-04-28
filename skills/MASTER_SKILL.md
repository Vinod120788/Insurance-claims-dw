# Master Skill: Repeatable Data Warehouse ETL Pipeline

This master skill document provides a repeatable, dataset-agnostic system for building an end-to-end Data Warehouse pipeline. By following this framework, you can take any raw dataset and systematically convert it into a structured star schema ready for Business Intelligence (BI) reporting.

## Phase 1: Data Assessment & Profiling
Before writing code, analyze the raw data to understand its shape and business context.
1. **Identify the "Grain":** What does one row of your primary data represent? (e.g., one insurance claim, one sales transaction, one website click). This will become your Fact Table.
2. **Identify the "Dimensions":** What entities describe the facts? Look for recurring entities like Customers, Products, Employees, Locations, or Dates.
3. **Identify "Measures":** What are the numeric values you want to aggregate? (e.g., Total Cost, Quantity Sold, Resolution Days).
4. **Data Quality Check:** Look for missing values, inconsistent formats (especially dates and strings), and duplicated records.

## Phase 2: Data Cleaning (The "Extract & Transform" Stage)
Use a Python script (e.g., `01_clean_raw_data.py`) using `pandas` to standardize the data.

**Standard Template Operations:**
*   **Load:** Extract sheets or files (`pd.read_excel()` or `pd.read_csv()`).
*   **Drop Garbage:** Remove empty columns and rows containing completely blank primary keys.
*   **Type Casting:** Force columns into correct data types, particularly converting date columns using `pd.to_datetime()`.
*   **Text Standardization:** Strip whitespaces (`.str.strip()`) and standardize casing (`.str.title()` or `.str.capitalize()`).
*   **Feature Engineering:** Calculate critical initial KPIs (e.g., difference between dates to find SLA/processing times).
*   **Export:** Save intermediate "clean" datasets as CSVs to decouple cleaning from database loading.

## Phase 3: Star Schema Design (The Data Model)
Write a SQL DDL script (e.g., `02_create_star_schema.sql`) to define the structure of your data warehouse.

**Standard Template Rules:**
*   **Surrogate Keys:** Always use auto-incrementing integer Primary Keys (e.g., `CustomerKey INTEGER PRIMARY KEY AUTOINCREMENT`) instead of natural business keys (`CustomerID`).
*   **DimDate:** Always include a comprehensive Date Dimension table to enable robust time-intelligence slicing (Year, Quarter, Month, Day, DayOfWeek).
*   **Dimension Tables:** Hold descriptive text attributes.
*   **Fact Tables:** Hold only Foreign Keys (linking to Dimensions) and numeric measures.

## Phase 4: Automated Data Loading (The "Load" Stage)
Use a Python script (e.g., `03_load_warehouse.py`) to map the clean CSVs into the relational database structure.

**Standard Template Operations:**
*   **Database Connection:** Connect to your target DB (SQLite, PostgreSQL, Snowflake).
*   **Execute DDL:** Run the Star Schema SQL script to instantiate empty tables.
*   **Generate DimDate Dynamically:** Extract all unique dates from the fact data, generate calendar attributes, and insert them into the `DimDate` table.
*   **Load Dimensions:** Generate Surrogate Keys for each dimension dataframe (e.g., `df["CustomerKey"] = range(1, len(df) + 1)`) and insert them into the DB.
*   **Map Facts:** Create dictionaries mapping natural keys to the newly generated surrogate keys. Use `.map()` on the Fact dataframe to swap natural keys for surrogate keys.
*   **Insert Facts:** Load the finalized Fact table into the DB.
*   **Verification:** Run automated `COUNT(*)` and `SUM()` queries to ensure data integrity post-load.

## Phase 5: BI Integration & Visualization
Connect your BI tool (Power BI, Tableau, Metabase) directly to the data warehouse database.

**Standard Template Operations:**
*   **Model Relationships:** Ensure the BI tool recognizes the 1-to-Many relationships between Dimensions and Facts based on the Surrogate Keys.
*   **DAX/Calculated Measures:** Build aggregated metrics centrally within the BI tool (e.g., Total Revenue, YoY Growth, Average SLA).
*   **Dashboard Construction:** Segment visual reporting into logical pages (e.g., High-level Overview, Financials, Operational Performance).

---
**Summary for Automation:** 
By standardizing the scripts into a 3-step execution (`Clean` -> `Define Schema` -> `Load Map`), you can copy this directory structure and simply update column names and file paths to automate the processing of any new analytical dataset.