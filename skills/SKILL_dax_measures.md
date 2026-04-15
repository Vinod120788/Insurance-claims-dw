# SKILL: DAX Measures — Insurance Claims Dashboard

## Purpose
Documents all DAX measures used in the Power BI dashboard.
All measures are stored in the _Measures table.

## File
`powerbi/dashboard.pbix`

---

## Measure Reference

### Total Claims
```dax
Total Claims = COUNTROWS(claims_clean)
```
Counts total number of claims. Base measure used in all 
percentage calculations. Auto-filters with all slicers.

---

### Total Payout
```dax
Total Payout = 
SUMX(
    claims_clean,
    claims_clean[Injury Claim] + 
    claims_clean[Property Claim] + 
    claims_clean[Vehicle Claim]
)
```
Sum of all three payout types per claim, across all claims.
SUMX used (not SUM) because we are summing a row-level 
calculation across three columns simultaneously.

---

### Total Annual Premium
```dax
Total Annual Premium = SUM(policies_clean[Annual Premium])
```
Total premium revenue collected across all policies.
Used as the denominator in Loss Ratio calculation.

---

### Loss Ratio %
```dax
Loss Ratio % = 
DIVIDE([Total Payout], [Total Annual Premium], 0) * 100
```
Core insurance profitability KPI.
- Below 60% = very profitable
- 60–80% = healthy
- 80–100% = margin pressure
- Above 100% = unprofitable (paying out more than collecting)

DIVIDE used instead of / to safely handle division by zero.

---

### Avg Resolution Days
```dax
Avg Resolution Days = AVERAGE(claims_clean[Resolution Days])
```
Average days from claim creation to claim closure.
SLA target = 30 days. Slice by handler to benchmark 
individual performance.

---

### SLA Breach Rate %
```dax
SLA Breach Rate % = 
VAR BreachedClaims = 
    COUNTROWS(
        FILTER(claims_clean, claims_clean[Resolution Days] > 30)
    )
RETURN
DIVIDE(BreachedClaims, [Total Claims], 0) * 100
```
Percentage of claims that exceeded the 30-day SLA target.
VAR/RETURN pattern used for readability.
Threshold (30 days) can be adjusted to match actual SLA policy.

---

### High Severity Claims
```dax
High Severity Claims = 
CALCULATE(
    [Total Claims],
    claims_clean[Incident Severity] IN {"Major Damage", "Total Loss"}
)
```
Count of claims classified as Major Damage or Total Loss.
CALCULATE modifies the filter context to restrict to 
high-severity rows only.

---

### Avg Claim Value
```dax
Avg Claim Value = DIVIDE([Total Payout], [Total Claims], 0)
```
Average total payout per claim (AUD).
Rising values may indicate fraud trends or claim inflation.

---

## DAX Concepts Used
| Concept | Measures that use it |
|---------|---------------------|
| COUNTROWS | Total Claims, SLA Breach Rate % |
| SUMX (row context) | Total Payout |
| SUM | Total Annual Premium |
| DIVIDE (safe division) | Loss Ratio %, SLA Breach Rate %, Avg Claim Value |
| AVERAGE | Avg Resolution Days |
| VAR / RETURN | SLA Breach Rate % |
| CALCULATE + FILTER | High Severity Claims, SLA Breach Rate % |
| IN operator | High Severity Claims |