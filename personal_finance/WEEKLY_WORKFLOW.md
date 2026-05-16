# Personal Finance — Weekly Workflow

> Manual weekly ritual. Every Thursday (aligned with PLANNING.md).

## 1. Download Transactions

- [ ] **RBC**: Online Banking → Account Activity → Download CSV (since last download)
  - Save to `personal_finance/csv_files/rbc_transactions/`
- [ ] **Scotia**: Online Banking → Credit Card → Download CSV (current statement period)
  - Save to `personal_finance/csv_files/scotia_transactions/`

## 2. Ingest to Database

From `personal_finance/`:

```bash
python scripts/upload_transactions/rbc_transactions.py
python scripts/upload_transactions/scotia_transactions.py
```

Scripts deduplicate on upsert — safe to re-run with overlapping date ranges.

## 3. Quick Spend Check

Open the DB and eyeball the week:

```sql
-- RBC: last 7 days
SELECT transaction_date, description_1, cad
FROM bank_rbc_transactions
WHERE transaction_date >= date('now', '-7 days')
ORDER BY transaction_date DESC;

-- Scotia: last 7 days
SELECT transaction_date, description_1, amount
FROM bank_scotia_transactions
WHERE transaction_date >= date('now', '-7 days')
ORDER BY transaction_date DESC;
```

What to look for:
- Any surprise charges or subscriptions you forgot about
- Interac tap totals (biggest blind spot — was $601/month avg)
- Weekend spending clusters (Fri–Sun is 38% of discretionary)

## 4. Update personal_finance.xlsx

Open `personal_finance.xlsx` and update:

### Net Worth tab (weekly)
- [ ] Wealthsimple: check app for current portfolio value (TFSA, RRSP, FHSA, Non-Reg)
- [ ] RBC: check chequing + savings balances
- [ ] Scotia: check credit card balance (enter as negative)
- Add a row to Net Worth History at the bottom

### Monthly Log tab (end of month)
At month-end, fill in the row for that month:
- Income ($7,947.77 unless pay changed)
- Fixed costs (rent $2,053 + telecom $133 + insurance + utilities)
- Discretionary (everything else)
- Net savings = Income - Total Spend
- Any contributions made to TFSA/RRSP/FHSA
- Net worth snapshot from the Net Worth tab

### Annual Spending tab (as they happen)
Log big-ticket and annual items when they hit:
- Memberships (Eau Claire, ECACL, Zwift, etc.)
- Golf (membership, course fees, gear)
- Trips (flights, hotels, trip spending)
- Bike (purchases, gear, accessories)
- Insurance (annual renewals)
- One-offs (furniture, Costco bulk, etc.)

These are tracked separately so they don't distort monthly budgets.

### Goals tab (monthly)
- Check savings rate against 29% target
- Update "Current" column for any goals that moved
- Flag anything that's slipping

## 5. Scorecard — Am I On Track?

| Metric | Target | This Week |
|---|---:|---:|
| Weekly discretionary | $779 | |
| Food delivery | $50 | |
| Dining/Bars | $150 | |
| Savings rate (month) | 29% | |
| Net worth delta | +$2,300/mo | |

If discretionary is 2x+ the weekly target, flag it.

## 6. Wealthsimple (Monthly — First Thursday of Month)

- [ ] Download monthly statement CSVs (TFSA, FHSA, RRSP, Non-Reg)
  - Save to `personal_finance/csv_files/wealthsimple/`
- [ ] Run: `python scripts/ingest_wealthsimple.py`
- [ ] Update CRA Contribution Room in the xlsx:
  - TFSA 2026 room: $7,000 (maxed Jan 2026 ✓)
  - FHSA 2026 room: $8,000 (maxed Jan 2026 ✓)
  - RRSP: check CRA My Account for remaining room

## 7. CRA Contribution Targets

| Account | 2026 Room | Status | Next Action |
|---|---:|---|---|
| TFSA | $7,000 | **Maxed** | Maintain — no more contributions |
| FHSA | $8,000 | **Maxed** | Maintain — no more contributions |
| RRSP | Check NOA | TBD | Check CRA My Account for deduction limit |

For 2027 planning:
- TFSA new room arrives Jan 1 ($7,000 expected)
- FHSA new room arrives Jan 1 ($8,000)
- RRSP room = 18% of 2026 earned income (minus pension adjustment)

## 8. Log It

After reviewing, optionally log a note in `/journal`:
- Total discretionary this week
- Net worth change
- Any wins or budget busts
- Action items (cancel subscription, return Amazon order, etc.)

---

## Quarterly Review (Every 3 Months)

- [ ] Regenerate `reports/monthly_budget.md` with fresh 3-month averages
- [ ] Review savings rate trend — target is 29% on clean months
- [ ] Check net worth growth trajectory
- [ ] Review CRA contribution room for next year planning
- [ ] Update budget targets if income or fixed costs changed
- [ ] Rebalance investment allocation if needed (check THESIS.md)
