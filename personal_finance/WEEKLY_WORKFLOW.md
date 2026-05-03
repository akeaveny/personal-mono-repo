# Personal Finance — Weekly Workflow

> Manual weekly ritual. Do this every Thursday (or whenever you batch it).

## 1. Download Transactions

- [ ] **RBC**: Online Banking → Account Activity → Download CSV (last 7 days or since last download)
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
SELECT transaction_date, description, amount
FROM bank_scotia_transactions
WHERE transaction_date >= date('now', '-7 days')
ORDER BY transaction_date DESC;
```

What to look for:
- Any surprise charges or subscriptions you forgot about
- Interac tap totals (your biggest blind spot — $601/month avg)
- Weekend spending clusters (Fri–Sun is 38% of discretionary)

## 4. Weekly Scorecard

Compare against budget targets from `reports/monthly_budget.md`:

| Category | Weekly Target | This Week |
|---|---:|---:|
| Groceries | $100 | |
| Food delivery | $25 | |
| Dining/Bars | $50 | |
| Amazon | $37 | |
| Uber rides | $20 | |
| Interac (taps) | $75 | |

Fill in actuals. If any category is 2x+ the weekly target, flag it.

## 5. Wealthsimple (Monthly — First Thursday of Month)

- [ ] Download monthly statement CSVs from Wealthsimple (TFSA, FHSA, RRSP, personal)
  - Save to `personal_finance/csv_files/wealthsimple/`
- [ ] Run: `python scripts/ingest_wealthsimple.py`
- [ ] Check portfolio value and contribution room

## 6. Log It

After reviewing, optionally log a quick note in your journal via `/journal`:
- Total discretionary spend this week
- Any budget busts or wins
- Action items (cancel a subscription, return an Amazon order, etc.)

---

## Quarterly Review (Every 3 Months)

- [ ] Regenerate `reports/monthly_budget.md` with fresh 3-month averages
- [ ] Review savings rate trend — target is 29%
- [ ] Check if rent situation has changed (biggest lever: $1,300+/month)
- [ ] Update budget targets if income or fixed costs changed
