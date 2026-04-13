-- =============================================================
-- Script  : 02_create_star_schema.sql
-- Project : Insurance Claims Data Warehouse
-- Purpose : Define the star schema table structures
-- Author  : Vinod Ganeshan
-- Note    : Run via 03_load_warehouse.py (uses SQLite)
-- =============================================================


-- ── Dimension: Date ───────────────────────────────────────
-- One row per unique date across the whole dataset.
-- Lets us slice any metric by day, month, quarter, or year.
CREATE TABLE IF NOT EXISTS DimDate (
    DateKey       INTEGER PRIMARY KEY,   -- format: YYYYMMDD e.g. 20190704
    FullDate      DATE    NOT NULL,
    Day           INTEGER NOT NULL,
    Month         INTEGER NOT NULL,
    MonthName     TEXT    NOT NULL,
    Quarter       INTEGER NOT NULL,
    Year          INTEGER NOT NULL,
    DayOfWeek     TEXT    NOT NULL
);


-- ── Dimension: Customer ───────────────────────────────────
-- One row per customer. Holds all descriptive customer info.
CREATE TABLE IF NOT EXISTS DimCustomer (
    CustomerKey   INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID    INTEGER NOT NULL UNIQUE,
    Gender        TEXT,
    GivenName     TEXT,
    Surname       TEXT,
    Age           INTEGER,
    City          TEXT,
    State         TEXT,
    StateFull     TEXT,
    Segment       TEXT,        -- Gold / Silver / Platinum
    PolicyNumber  INTEGER
);


-- ── Dimension: Policy ─────────────────────────────────────
-- One row per insurance policy.
CREATE TABLE IF NOT EXISTS DimPolicy (
    PolicyKey            INTEGER PRIMARY KEY AUTOINCREMENT,
    PolicyNumber         INTEGER NOT NULL UNIQUE,
    PolicyCreateDate     DATE,
    PolicyExpirationDate DATE,
    AnnualPremium        REAL,   -- in AUD
    Excess               REAL    -- the deductible amount
);


-- ── Dimension: Handler ────────────────────────────────────
-- One row per claims handler (staff member).
CREATE TABLE IF NOT EXISTS DimHandler (
    HandlerKey       INTEGER PRIMARY KEY AUTOINCREMENT,
    HandlerID        INTEGER NOT NULL UNIQUE,
    GivenName        TEXT,
    Surname          TEXT,
    FullName         TEXT,       -- GivenName + Surname combined
    TeamNo           INTEGER,
    ReportingManager TEXT,
    ExperienceYears  INTEGER
);


-- ── Fact Table: Claims ────────────────────────────────────
-- One row per claim. Stores keys (links) and all the numbers.
-- This is the centre of the star.
CREATE TABLE IF NOT EXISTS FactClaims (
    ClaimKey                 INTEGER PRIMARY KEY AUTOINCREMENT,
    ClaimNumber              INTEGER NOT NULL UNIQUE,
    CustomerKey              INTEGER REFERENCES DimCustomer(CustomerKey),
    PolicyKey                INTEGER REFERENCES DimPolicy(PolicyKey),
    HandlerKey               INTEGER REFERENCES DimHandler(HandlerKey),
    DateKey                  INTEGER REFERENCES DimDate(DateKey),
    IncidentDate             DATE,
    ClaimCreateDate          DATE,
    ClaimClosedDate          DATE,
    HandlerAssignedDate      DATE,
    IncidentType             TEXT,   -- Parked Car / Multi-vehicle etc.
    IncidentSeverity         TEXT,   -- Trivial / Minor / Major / Total Loss
    NoOfVehiclesInvolved     INTEGER,
    NoOfCustomerContacts     INTEGER,
    InjuryClaim              REAL,   -- AUD payout for injury
    PropertyClaim            REAL,   -- AUD payout for property
    VehicleClaim             REAL,   -- AUD payout for vehicle
    TotalClaimAmount         REAL,   -- InjuryClaim + PropertyClaim + VehicleClaim
    ResolutionDays           INTEGER -- days from create to close
);