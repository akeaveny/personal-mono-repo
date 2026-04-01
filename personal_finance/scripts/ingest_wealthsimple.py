#!/usr/bin/env python3
"""
Ingest Wealthsimple monthly statement CSVs into SQLite.

Parses BUY, SELL, DIV, and FXCONVERSION transactions from Wealthsimple's
CSV export format. Extracts ticker, shares, price, and execution date
from the description field.

Usage:
    python personal_finance/scripts/ingest_wealthsimple.py --account TFSA path/to/statement.csv
    python personal_finance/scripts/ingest_wealthsimple.py --dir personal_finance/csv_files/wealthsimple/
    python personal_finance/scripts/ingest_wealthsimple.py --account TFSA ~/Downloads/*.csv --dry-run
"""

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.db_utils import get_connection, create_import_batch, finish_import_batch

VALID_ACCOUNTS = ["TFSA", "RRSP", "FHSA", "Non-registered"]


def parse_buy_sell(description):
    ticker_match = re.match(r'^(\S+)\s*-\s*(.+?):\s*(Bought|Sold)', description)
    if not ticker_match:
        return None

    ticker = ticker_match.group(1)
    security_name = ticker_match.group(2).strip()

    shares_match = re.search(r'(Bought|Sold)\s+([\d.]+)\s+shares?\s+at\s+\$([\d.]+)', description)
    shares = float(shares_match.group(2)) if shares_match else None
    price = float(shares_match.group(3)) if shares_match else None

    exec_match = re.search(r'\(executed at (\d{4}-\d{2}-\d{2})\)', description)
    exec_date = exec_match.group(1) if exec_match else None

    return {
        "ticker": ticker,
        "security_name": security_name,
        "shares": shares,
        "price_per_share": price,
        "execution_date": exec_date,
    }


def parse_dividend(description):
    ticker_match = re.match(r'^(\S+)\s*-\s*(.+?):', description)
    if not ticker_match:
        return None

    ticker = ticker_match.group(1)
    security_name = ticker_match.group(2).strip()

    received_match = re.search(r'received on (\d{4}-\d{2}-\d{2})', description)
    exec_date = received_match.group(1) if received_match else None

    return {
        "ticker": ticker,
        "security_name": security_name,
        "shares": None,
        "price_per_share": None,
        "execution_date": exec_date,
    }


def parse_fx(description):
    exec_match = re.search(r'\(executed at (\d{4}-\d{2}-\d{2})\)', description)
    exec_date = exec_match.group(1) if exec_match else None

    rate_match = re.search(r'\$1USD\s*=\s*\$([\d.]+)CAD', description)
    fx_rate = float(rate_match.group(1)) if rate_match else None

    return {
        "ticker": None,
        "security_name": None,
        "shares": None,
        "price_per_share": None,
        "execution_date": exec_date,
        "fx_rate": fx_rate,
    }


def parse_row(row):
    txn_type = row["transaction"]
    description = row["description"]

    if txn_type in ("BUY", "SELL"):
        parsed = parse_buy_sell(description)
    elif txn_type == "DIV":
        parsed = parse_dividend(description)
    elif txn_type == "FXCONVERSION":
        parsed = parse_fx(description)
    else:
        parsed = {
            "ticker": None, "security_name": None, "shares": None,
            "price_per_share": None, "execution_date": None,
        }

    if parsed is None:
        print(f"  Warning: Could not parse description: {description}")
        parsed = {
            "ticker": None, "security_name": None, "shares": None,
            "price_per_share": None, "execution_date": None,
        }

    return parsed


def ingest_file(filepath, account, conn, dry_run=False):
    filepath = Path(filepath)
    print(f"\nProcessing: {filepath.name}")

    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    batch_id = None
    if not dry_run:
        batch_id = create_import_batch(conn, filepath.name)

    inserted = 0
    skipped = 0
    errors = 0

    # Collect all rows for batch insert
    insert_rows = []
    for row in rows:
        if not row.get("date") or not row.get("transaction"):
            continue

        parsed = parse_row(row)
        amount = float(row["amount"]) if row["amount"] else 0
        balance = float(row["balance"]) if row["balance"] else None
        currency = row.get("currency", "CAD")

        if dry_run:
            ticker_str = parsed.get("ticker") or "N/A"
            shares_str = f"{parsed.get('shares', 'N/A')}"
            print(f"  [DRY RUN] {row['date']} {row['transaction']:15s} {ticker_str:10s} "
                  f"shares={shares_str:>10s}  amount={amount:>12,.2f} {currency}")
            inserted += 1
            continue

        insert_rows.append((
            row["date"], account, row["transaction"],
            parsed.get("ticker"), parsed.get("security_name"),
            parsed.get("shares"), parsed.get("price_per_share"),
            amount, balance, currency,
            parsed.get("execution_date"), parsed.get("fx_rate"),
            row["description"], filepath.name,
        ))

    if not dry_run and insert_rows:
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT OR IGNORE INTO etf_transactions
               (date, account, transaction_type, ticker, security_name,
                shares, price_per_share, amount, balance, currency,
                execution_date, fx_rate, description, source_file)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            insert_rows,
        )
        conn.commit()
        inserted = cursor.rowcount if cursor.rowcount > 0 else 0
        skipped = len(insert_rows) - inserted

    if not dry_run and batch_id is not None:
        finish_import_batch(
            conn, batch_id,
            row_count=len(insert_rows),
            inserted=inserted,
            duplicates=skipped,
            rejected=errors,
        )

    print(f"  Results: {inserted} inserted, {skipped} skipped (duplicates), {errors} errors")
    return inserted, skipped, errors


def detect_account_from_filename(filename):
    name = Path(filename).name
    if name.startswith("Non-registered-"):
        return "Non-registered"
    for acct in ["TFSA", "RRSP", "FHSA"]:
        if name.startswith(acct + "-"):
            return acct
    return None


def main():
    parser = argparse.ArgumentParser(description="Ingest Wealthsimple statement CSVs")
    parser.add_argument("files", nargs="*", help="CSV file(s) to ingest")
    parser.add_argument("--dir", type=str,
                        help="Directory of CSVs to ingest (auto-detects account from filename)")
    parser.add_argument("--account", type=str, choices=VALID_ACCOUNTS,
                        help="Account type (required when passing files, ignored with --dir)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and display without inserting into DB")
    args = parser.parse_args()

    file_account_pairs = []

    if args.dir:
        csv_dir = Path(args.dir)
        if not csv_dir.is_dir():
            print(f"Directory not found: {csv_dir}")
            sys.exit(1)
        for csv_file in sorted(csv_dir.glob("*.csv")):
            account = detect_account_from_filename(csv_file)
            if account is None:
                print(f"Warning: Could not detect account from {csv_file.name}, skipping")
                continue
            file_account_pairs.append((csv_file, account))
        if not file_account_pairs:
            print("No CSV files found in directory.")
            sys.exit(1)
    elif args.files:
        if not args.account:
            print("--account is required when passing individual files.")
            sys.exit(1)
        file_account_pairs = [(f, args.account) for f in args.files]
    else:
        parser.print_help()
        sys.exit(1)

    conn = None
    if not args.dry_run:
        conn = get_connection()

    total_inserted = 0
    total_skipped = 0
    total_errors = 0

    for filepath, account in file_account_pairs:
        i, s, e = ingest_file(filepath, account, conn, args.dry_run)
        total_inserted += i
        total_skipped += s
        total_errors += e

    if conn:
        conn.close()

    print(f"\nTotal: {total_inserted} inserted, {total_skipped} skipped, {total_errors} errors")


if __name__ == "__main__":
    main()
