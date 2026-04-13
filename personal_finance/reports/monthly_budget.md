# Monthly Budget

> Based on spending data from Jan–Mar 2026. Income: **$7,947.77/month** after tax.

## Budget Summary

| Category | Current Avg | Budget Target | Type |
|---|---:|---:|---|
| **Rent (Airbnb)** | $3,783 | $3,783* | Fixed |
| **Groceries (UberEats >$100)** | $493 | $400 | Essential |
| **Food Delivery (UberEats <$100)** | $148 | $100 | Discretionary |
| **Interac (untracked taps)** | $601 | $300 | Discretionary |
| **Amazon** | $416 | $150 | Discretionary |
| **Dining/Bars** | $366 | $200 | Discretionary |
| **Rides/Taxi (Uber)** | $197 | $80 | Discretionary |
| **Phone/Internet (Telus + Moby)** | $194 | $194 | Fixed |
| **Activities (Ski/Trips)** | $158 | $150 | Discretionary |
| **Utilities** | $75 | $75 | Fixed |
| **Pharmacy** | $51 | $50 | Essential |
| **Personal Care (barber, spa)** | $45 | $45 | Essential |
| **Fitness (ClassPass)** | $24 | $27 | Fixed |
| **Streaming (Netflix, Apple)** | $19 | $20 | Fixed |
| **Bank Fees** | $12 | $12 | Fixed |
| **Insurance (Square One)** | $40 | $40 | Fixed |
| | | | |
| **Total Spending** | **~$6,622** | **$5,626** | |
| **Savings** | **~$1,326** | **$2,322** | |
| **Savings Rate** | **17%** | **29%** | |

*Rent is 48% of income. Moving to a standard lease (~$2,200–$2,500) is the single biggest lever — would free $1,300+/month.*

## Spending by Category (Jan–Feb 2026 Actuals)

### Fixed Bills (~$4,151/month)
| Bill | Monthly | Card |
|---|---:|---|
| Rent (Airbnb) | $3,783 | RBC Debit |
| Telus Mobility | $153 | Scotia (4% back) |
| Moby Telecom | $47 | Scotia (4% back) |
| Utilities | $75 | RBC |
| Square One Insurance | $40 | Scotia (4% back) |
| ClassPass | $27 | Scotia (4% back) |
| Netflix + Apple | $19 | RBC WestJet |
| Bank Fees | $12 | — |

### Groceries & Food (~$641/month currently)
- **Groceries via UberEats**: ~$493/month (3 orders, avg $164/order)
  - UberEats markup estimated 20–30% vs in-store
  - Switching to in-store weekly could save $100–150/month
- **Food delivery (meals)**: ~$148/month (3.5 orders, avg $42)

### Discretionary (~$1,830/month currently)
| Category | Monthly | Notes |
|---|---:|---|
| Interac (untracked) | $601 | ~20 taps/month averaging $30. Likely coffee, lunches, convenience. **Biggest blind spot.** |
| Amazon | $416 | ~7 orders/month. High variance — includes impulse buys. |
| Dining/Bars | $366 | Spikes on weekends (Jan was heavy — Banff trip). |
| Rides/Taxi | $197 | ~7 Uber rides/month. Weekend-heavy. |
| Activities | $158 | Ski trips (Sunshine, Lake Louise). Seasonal. |
| Personal Care | $45 | Barber, spa — roughly every 2 months. |
| Pharmacy | $51 | Shoppers Drug Mart. |

## Where to Cut

### High Impact (save $990/month → $2,300 savings)
| Change | Current | Target | Monthly Savings |
|---|---:|---:|---:|
| Reduce Amazon to essentials | $416 | $150 | +$266 |
| Reduce food delivery to 1x/week | $148 | $50 | +$98 |
| Reduce dining/bars | $366 | $200 | +$166 |
| Cap Interac spending | $601 | $300 | +$301 |
| Reduce Uber rides | $197 | $80 | +$117 |
| Grocery delivery → in-store | $493 | $350 | +$143 |

### Long-Term (save $1,300+/month)
- **Move off Airbnb** to a standard 1-year lease: $3,783 → ~$2,200–$2,500 = **$1,300–$1,600/month saved**

## Weekend Spending Pattern

38.5% of discretionary spending occurs Fri–Sun (3/7 days). Weekend drivers:
- Uber rides + UberEats cluster on Fri–Sun
- Dining/bars are almost exclusively weekend
- Amazon impulse purchases spike on weekends

**Strategy**: Set a weekly weekend cash budget of $200 to create a natural ceiling.

## Tracking Gaps

1. **Interac debit purchases** (`C-IDP PURCHASE-XXXX`): $601/month with no description. Check RBC app for merchant details and categorize.
2. **Groceries**: All ordered through UberEats — no separate grocery line. Identified by amount (>$100 = groceries).
3. **No category patterns seeded** in the database yet — manual SQL categorization for now.

## Data Sources

- RBC transactions: `personal_finance.db` → `bank_rbc_transactions` (Sep 2025–Mar 2026)
- Scotia transactions: `personal_finance.db` → `bank_scotia_transactions` (Nov 2025–Mar 2026)
- Note: RBC CSVs have overlapping date ranges — queries should deduplicate on `(account_type, transaction_date, description_1, cad)`.

---
*Generated 2026-03-20. Data from `personal_finance/personal_finance.db`.*
