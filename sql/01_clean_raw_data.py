# =============================================================
# Script: 01_clean_raw_data.py
# Project: Insurance Claims Data Warehouse
# Purpose: Read raw Excel data, clean it, and export clean CSVs
# Author:  Vinod Ganeshan
# =============================================================

import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────
RAW_FILE   = os.path.join("data", "raw", "Dataset3.xlsx")
OUTPUT_DIR = os.path.join("data", "clean")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 55)
print("  Insurance Claims — Data Cleaning Script")
print("=" * 55)

# ── 1. Load all four sheets ────────────────────────────────
print("\n[1/5] Loading raw Excel sheets...")

claims   = pd.read_excel(RAW_FILE, sheet_name="Claim Table")
customers = pd.read_excel(RAW_FILE, sheet_name="Customer Table")
handlers = pd.read_excel(RAW_FILE, sheet_name="Handler Table")
policies = pd.read_excel(RAW_FILE, sheet_name="Policy Table")

print(f"      Claim Table    : {len(claims):>6} rows loaded")
print(f"      Customer Table : {len(customers):>6} rows loaded")
print(f"      Handler Table  : {len(handlers):>6} rows loaded")
print(f"      Policy Table   : {len(policies):>6} rows loaded")

# ── 2. Drop the unnamed first column (blank index column) ──
print("\n[2/5] Dropping blank index columns...")
claims    = claims.loc[:, ~claims.columns.str.contains("^Unnamed")]
customers = customers.loc[:, ~customers.columns.str.contains("^Unnamed")]
handlers  = handlers.loc[:, ~handlers.columns.str.contains("^Unnamed")]
policies  = policies.loc[:, ~policies.columns.str.contains("^Unnamed")]

# ── 3. Remove fully blank rows in Claims ──────────────────
print("\n[3/5] Removing blank rows from Claim Table...")
before = len(claims)
claims = claims.dropna(subset=["Claim Number"])
after  = len(claims)
print(f"      Removed {before - after} blank rows  "
      f"({after} clean rows remaining)")

# ── 4. Fix data types ─────────────────────────────────────
print("\n[4/5] Fixing data types...")

# Claims — dates
date_cols = [
    "Incident Date", "Claim Create Date",
    "Claim Closed Date", "Handler Assigned Date"
]
for col in date_cols:
    claims[col] = pd.to_datetime(claims[col], errors="coerce")

# Claims — calculate resolution days (key KPI)
claims["Resolution Days"] = (
    claims["Claim Closed Date"] - claims["Claim Create Date"]
).dt.days

# Claims — integers
for col in ["Customer ID", "Claim Number", "Handler ID",
            "No of Vehicles Involved", "Number of Customer Contacts"]:
    claims[col] = pd.to_numeric(claims[col], errors="coerce")

# Customers — strip extra whitespace from text fields
for col in ["Gender", "City", "State", "StateFull", "Segment"]:
    customers[col] = customers[col].str.strip()

# Customers — capitalise gender consistently
customers["Gender"] = customers["Gender"].str.capitalize()

# Policies — dates
policies["Policy Create Date"]     = pd.to_datetime(
    policies["Policy Create Date"],     errors="coerce")
policies["Policy Expiration Date"] = pd.to_datetime(
    policies["Policy Expiration Date"], errors="coerce")

print("      Dates parsed, Resolution Days calculated,")
print("      Gender capitalised, whitespace stripped.")

# ── 5. Save clean CSVs ────────────────────────────────────
print("\n[5/5] Saving clean CSV files...")

claims.to_csv(   os.path.join(OUTPUT_DIR, "claims_clean.csv"),    index=False)
customers.to_csv(os.path.join(OUTPUT_DIR, "customers_clean.csv"), index=False)
handlers.to_csv( os.path.join(OUTPUT_DIR, "handlers_clean.csv"),  index=False)
policies.to_csv( os.path.join(OUTPUT_DIR, "policies_clean.csv"),  index=False)

print(f"      Saved to: {OUTPUT_DIR}/")
print(f"        claims_clean.csv    — {len(claims)} rows")
print(f"        customers_clean.csv — {len(customers)} rows")
print(f"        handlers_clean.csv  — {len(handlers)} rows")
print(f"        policies_clean.csv  — {len(policies)} rows")

# ── Summary ───────────────────────────────────────────────
print("\n" + "=" * 55)
print("  Cleaning complete — no errors.")
print("  Key field added: 'Resolution Days'")
print("  Next step: run 02_create_star_schema.sql")
print("=" * 55)