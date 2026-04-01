#!/usr/bin/env python3
"""
Seed the portfolio_etfs config and compute current holdings from transactions.

Creates the portfolio structure (asset categories + ETFs) and computes a holdings
snapshot from etf_transactions (net shares, weighted average cost per account/ticker).

Usage:
    python personal_finance/scripts/seed_portfolio.py
    python personal_finance/scripts/seed_portfolio.py --dry-run
    python personal_finance/scripts/seed_portfolio.py --date 2026-02-28
"""

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.db_utils import get_connection

PORTFOLIO_ETFS = [
    # (asset_category, category_order, ticker, etf_name, sort_order)
    ("Cash and Equivalents", 1, "CASH", "High-Interest Savings Accounts", 0),
    ("Canadian Equities", 2, "XIC", "iShares S&P/TSX Capped Composite Index ETF", 0),
    ("U.S. Equities", 3, "VFV", "Vanguard S&P 500 Index ETF", 0),
    ("International Equities", 4, "XEF", "iShares Core MSCI EAFE IMI Index ETF", 0),
    ("Stocks", 5, "BYN", "Banyan Gold Corp", 0),
]


def seed_portfolio_etfs(cursor, conn, dry_run=False):
    print("\n=== Seeding etf_portfolio_etfs ===")
    inserted = 0
    skipped = 0

    for category, cat_order, ticker, etf_name, sort_order in PORTFOLIO_ETFS:
        if dry_run:
            print(f"  [DRY RUN] {ticker:6s}  {category:25s}  {etf_name}")
            inserted += 1
            continue

        cursor.execute(
            """INSERT OR IGNORE INTO etf_portfolio_etfs
               (asset_category, category_order, ticker, etf_name, sort_order)
               VALUES (?, ?, ?, ?, ?)""",
            (category, cat_order, ticker, etf_name, sort_order),
        )
        if cursor.rowcount > 0:
            inserted += 1
            print(f"  Inserted: {ticker:6s}  {category:25s}  {etf_name}")
        else:
            skipped += 1
            print(f"  Skipped (exists): {ticker}")

    if not dry_run:
        conn.commit()

    print(f"  Results: {inserted} inserted, {skipped} skipped")
    return inserted


def compute_holdings(cursor, dry_run=False):
    """Compute net holdings per account/ticker from transactions."""
    print("\n=== Computing holdings from transactions ===")

    cursor.execute("""
        SELECT
            account,
            ticker,
            currency,
            SUM(CASE WHEN transaction_type = 'BUY' THEN shares ELSE 0 END) AS total_bought,
            SUM(CASE WHEN transaction_type = 'SELL' THEN shares ELSE 0 END) AS total_sold,
            SUM(CASE WHEN transaction_type = 'BUY' THEN shares * price_per_share ELSE 0 END) AS total_cost
        FROM etf_transactions
        WHERE transaction_type IN ('BUY', 'SELL')
          AND ticker IS NOT NULL
          AND shares IS NOT NULL
        GROUP BY account, ticker, currency
        ORDER BY account, ticker
    """)

    holdings = []
    for row in cursor.fetchall():
        account, ticker, currency, total_bought, total_sold, total_cost = (
            row[0], row[1], row[2], row[3], row[4], row[5]
        )
        net_shares = float(total_bought or 0) - float(total_sold or 0)

        if net_shares <= 0:
            continue

        bought_shares = float(total_bought or 0)
        avg_cost = float(total_cost) / bought_shares if bought_shares > 0 else 0
        book_value = round(net_shares * avg_cost, 2)

        holdings.append({
            "account": account,
            "ticker": ticker,
            "total_units": round(net_shares, 4),
            "avg_cost_per_unit": round(avg_cost, 4),
            "book_value": book_value,
            "currency": currency or "CAD",
        })

        status = "[DRY RUN] " if dry_run else ""
        print(
            f"  {status}{account:6s}  {ticker:6s}  "
            f"units={net_shares:>12.4f}  avg=${avg_cost:>10.4f}  "
            f"book=${book_value:>12.2f}  {currency or 'CAD'}"
        )

    return holdings


def ensure_extra_tickers(cursor, conn, holdings, dry_run=False):
    """Add any tickers found in transactions but missing from etf_portfolio_etfs."""
    cursor.execute("SELECT ticker FROM etf_portfolio_etfs")
    known = {row[0] for row in cursor.fetchall()}

    new_tickers = {h["ticker"] for h in holdings} - known
    if not new_tickers:
        return

    print(f"\n=== Adding {len(new_tickers)} extra ticker(s) to etf_portfolio_etfs ===")
    max_order = 99

    for ticker in sorted(new_tickers):
        if dry_run:
            print(f"  [DRY RUN] {ticker} -> Other")
            continue

        cursor.execute(
            """INSERT OR IGNORE INTO etf_portfolio_etfs
               (asset_category, category_order, ticker, etf_name, sort_order)
               VALUES (?, ?, ?, ?, ?)""",
            ("Other", max_order, ticker, ticker, 0),
        )
        if cursor.rowcount > 0:
            print(f"  Inserted: {ticker} -> Other")

    if not dry_run:
        conn.commit()


def insert_holdings(cursor, conn, holdings, snapshot_date, dry_run=False):
    """Insert holdings snapshot for the given date."""
    print(f"\n=== Inserting holdings for {snapshot_date} ===")

    if dry_run:
        print(f"  [DRY RUN] Would insert {len(holdings)} holding rows for {snapshot_date}")
        return

    cursor.execute("DELETE FROM etf_holdings WHERE date = ?", (snapshot_date,))
    deleted = cursor.rowcount
    if deleted:
        print(f"  Deleted {deleted} existing rows for {snapshot_date}")

    rows = [
        (snapshot_date, h["account"], h["ticker"], h["total_units"],
         h["avg_cost_per_unit"], h["book_value"], h["currency"])
        for h in holdings
    ]
    cursor.executemany(
        """INSERT INTO etf_holdings
           (date, account, ticker, total_units, avg_cost_per_unit, book_value, currency)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    print(f"  Inserted {len(rows)} holding rows")


def main():
    parser = argparse.ArgumentParser(
        description="Seed portfolio structure and compute holdings from transactions"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without inserting into DB")
    parser.add_argument("--date", type=str, default=str(date.today()),
                        help="Snapshot date (YYYY-MM-DD, default: today)")
    args = parser.parse_args()

    conn = get_connection()
    conn.row_factory = None  # Use tuple rows for this script
    cursor = conn.cursor()

    try:
        seed_portfolio_etfs(cursor, conn, args.dry_run)
        holdings = compute_holdings(cursor, args.dry_run)
        ensure_extra_tickers(cursor, conn, holdings, args.dry_run)
        insert_holdings(cursor, conn, holdings, args.date, args.dry_run)
        print(f"\nDone! Snapshot date: {args.date}")
    except Exception as e:
        print(f"\nError: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
