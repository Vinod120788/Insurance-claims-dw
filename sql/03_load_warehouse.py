# =============================================================
# Script  : 03_load_warehouse.py
# Project : Insurance Claims Data Warehouse
# Purpose : Create SQLite database, build star schema tables,
#           and load clean CSV data into them
# Author  : Vinod Ganeshan
# Run     : python sql/03_load_warehouse.py
# =============================================================

import sqlite3
import pandas as pd
import os

# ── Paths ─────────────────────────────────────────────────
CLEAN_DIR = os.path.join("data", "clean")
DB_PATH   = os.path.join("data", "insurance_dw.db")
SQL_FILE  = os.path.join("sql", "02_create_star_schema.sql")

print("=" * 55)
print("  Insurance Claims — Load Data Warehouse")
print("=" * 55)

# ── 1. Load clean CSVs ────────────────────────────────────
print("\n[1/6] Loading clean CSV files...")
claims    = pd.read_csv(os.path.join(CLEAN_DIR, "claims_clean.csv"),
                        parse_dates=["Incident Date","Claim Create Date",
                                     "Claim Closed Date","Handler Assigned Date"])
customers = pd.read_csv(os.path.join(CLEAN_DIR, "customers_clean.csv"))
handlers  = pd.read_csv(os.path.join(CLEAN_DIR, "handlers_clean.csv"))
policies  = pd.read_csv(os.path.join(CLEAN_DIR, "policies_clean.csv"),
                        parse_dates=["Policy Create Date",
                                     "Policy Expiration Date"])
print(f"      Loaded: {len(claims)} claims, {len(customers)} customers,",
      f"{len(handlers)} handlers, {len(policies)} policies")

# ── 2. Connect to SQLite and create tables ─────────────────
print("\n[2/6] Creating SQLite database and star schema tables...")
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

with open(SQL_FILE, "r") as f:
    cur.executescript(f.read())
conn.commit()
print(f"      Database created at: {DB_PATH}")

# ── 3. Load DimDate ───────────────────────────────────────
print("\n[3/6] Building DimDate...")
all_dates = pd.concat([
    claims["Incident Date"].dropna(),
    claims["Claim Create Date"].dropna(),
    claims["Claim Closed Date"].dropna()
]).drop_duplicates().sort_values()

dim_date_rows = []
for d in all_dates:
    dim_date_rows.append({
        "DateKey"  : int(d.strftime("%Y%m%d")),
        "FullDate" : d.date().isoformat(),
        "Day"      : d.day,
        "Month"    : d.month,
        "MonthName": d.strftime("%B"),
        "Quarter"  : (d.month - 1) // 3 + 1,
        "Year"     : d.year,
        "DayOfWeek": d.strftime("%A")
    })

dim_date = pd.DataFrame(dim_date_rows).drop_duplicates(subset="DateKey")
dim_date.to_sql("DimDate", conn, if_exists="append", index=False)
print(f"      {len(dim_date)} unique dates loaded")

# ── 4. Load Dimension tables ──────────────────────────────
print("\n[4/6] Loading DimCustomer, DimPolicy, DimHandler...")

# DimCustomer
cust_df = customers.rename(columns={
    "Customer ID"  : "CustomerID",
    "Policy Number": "PolicyNumber"
})
# Only keep columns that exist in our DimCustomer table
# (dropping CountryFull — all customers are Australian, not needed)
cust_df = cust_df[[
    "CustomerID", "Gender", "GivenName", "Surname",
    "Age", "City", "State", "StateFull", "Segment", "PolicyNumber"
]]
cust_df["CustomerKey"] = range(1, len(cust_df) + 1)
cust_df.to_sql("DimCustomer", conn, if_exists="append", index=False)
print(f"      DimCustomer: {len(cust_df)} rows")

# DimPolicy
pol_df = policies.rename(columns={
    "Policy Number"         : "PolicyNumber",
    "Policy Create Date"    : "PolicyCreateDate",
    "Policy Expiration Date": "PolicyExpirationDate",
    "Annual Premium"        : "AnnualPremium"
})
pol_df = pol_df[[
    "PolicyNumber", "PolicyCreateDate",
    "PolicyExpirationDate", "AnnualPremium", "Excess"
]]
pol_df["PolicyKey"] = range(1, len(pol_df) + 1)
pol_df.to_sql("DimPolicy", conn, if_exists="append", index=False)
print(f"      DimPolicy  : {len(pol_df)} rows")

# DimHandler
han_df = handlers.rename(columns={
    "Handler ID"           : "HandlerID",
    "Team No"              : "TeamNo",
    "Reporting Manager"    : "ReportingManager",
    "Experience (In Years)": "ExperienceYears"
})
han_df["FullName"]   = han_df["GivenName"] + " " + han_df["Surname"]
han_df = han_df[[
    "HandlerID", "GivenName", "Surname", "FullName",
    "TeamNo", "ReportingManager", "ExperienceYears"
]]
han_df["HandlerKey"] = range(1, len(han_df) + 1)
han_df.to_sql("DimHandler", conn, if_exists="append", index=False)
print(f"      DimHandler : {len(han_df)} rows")

# ── 5. Load FactClaims ─────────────────────────────────────
print("\n[5/6] Building FactClaims (joining all keys)...")

# Build lookup maps
cust_map    = dict(zip(cust_df["CustomerID"], cust_df["CustomerKey"]))
pol_map     = dict(zip(pol_df["PolicyNumber"], pol_df["PolicyKey"]))
han_map     = dict(zip(han_df["HandlerID"], han_df["HandlerKey"]))
date_map    = dict(zip(dim_date["FullDate"], dim_date["DateKey"]))

fact = claims.copy()
fact = fact.rename(columns={
    "Customer ID"              : "CustomerID",
    "Policy Number"            : "PolicyNumber",
    "Claim Number"             : "ClaimNumber",
    "Incident Date"            : "IncidentDate",
    "Claim Create Date"        : "ClaimCreateDate",
    "Claim Closed Date"        : "ClaimClosedDate",
    "Handler ID"               : "HandlerID",
    "Handler Assigned Date"    : "HandlerAssignedDate",
    "Incident Type"            : "IncidentType",
    "Incident Severity"        : "IncidentSeverity",
    "No of Vehicles Involved"  : "NoOfVehiclesInvolved",
    "Number of Customer Contacts": "NoOfCustomerContacts",
    "Injury Claim"             : "InjuryClaim",
    "Property Claim"           : "PropertyClaim",
    "Vehicle Claim"            : "VehicleClaim",
    "Resolution Days"          : "ResolutionDays"
})

# Map foreign keys
fact["CustomerKey"] = fact["CustomerID"].map(cust_map)
fact["PolicyKey"]   = fact["PolicyNumber"].map(pol_map)
fact["HandlerKey"]  = fact["HandlerID"].map(han_map)
fact["DateKey"]     = fact["IncidentDate"].dt.date.astype(str).map(date_map)

# Calculate total claim amount
fact["TotalClaimAmount"] = (
    fact["InjuryClaim"].fillna(0) +
    fact["PropertyClaim"].fillna(0) +
    fact["VehicleClaim"].fillna(0)
)

# Convert dates to strings for SQLite
for col in ["IncidentDate","ClaimCreateDate","ClaimClosedDate","HandlerAssignedDate"]:
    fact[col] = pd.to_datetime(fact[col], errors="coerce").dt.date.astype(str)

# Select only the columns the fact table needs
fact_cols = [
    "ClaimNumber","CustomerKey","PolicyKey","HandlerKey","DateKey",
    "IncidentDate","ClaimCreateDate","ClaimClosedDate","HandlerAssignedDate",
    "IncidentType","IncidentSeverity","NoOfVehiclesInvolved",
    "NoOfCustomerContacts","InjuryClaim","PropertyClaim","VehicleClaim",
    "TotalClaimAmount","ResolutionDays"
]
fact[fact_cols].to_sql("FactClaims", conn, if_exists="append", index=False)
print(f"      FactClaims : {len(fact)} rows loaded")

# ── 6. Verify with quick queries ──────────────────────────
print("\n[6/6] Running verification queries...")

checks = {
    "Total claims"          : "SELECT COUNT(*) FROM FactClaims",
    "Unique customers"      : "SELECT COUNT(*) FROM DimCustomer",
    "Unique policies"       : "SELECT COUNT(*) FROM DimPolicy",
    "Unique handlers"       : "SELECT COUNT(*) FROM DimHandler",
    "Unique dates"          : "SELECT COUNT(*) FROM DimDate",
    "Avg resolution days"   : "SELECT ROUND(AVG(ResolutionDays),1) FROM FactClaims",
    "Total payout (AUD)"    : "SELECT ROUND(SUM(TotalClaimAmount),0) FROM FactClaims",
}

for label, query in checks.items():
    result = cur.execute(query).fetchone()[0]
    print(f"      {label:<25}: {result:,}")

conn.close()

print("\n" + "=" * 55)
print("  Data warehouse built successfully!")
print(f"  Database file: {DB_PATH}")
print("  Next step: open Power BI and connect to this DB")
print("=" * 55)