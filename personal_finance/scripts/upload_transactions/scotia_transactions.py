"""Upload Scotia bank transaction CSVs to SQLite."""

import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.db_utils import get_connection, upsert_dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_DIR = Path(__file__).resolve().parent.parent.parent / "csv_files" / "scotia_transactions"
TABLE_NAME = "bank_scotia_transactions"

COLUMN_NAMES = [
    "account_type", "transaction_date", "description_1",
    "description_2", "status", "transaction_type", "amount",
]


def _concat(csv_dir: Path) -> pd.DataFrame:
    csv_files = list(csv_dir.glob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files in {csv_dir}")

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, index_col=False, header=0)
        df.columns = COLUMN_NAMES
        df["source_file"] = csv_file.name
        dfs.append(df)
        logger.info(f"  Read {len(df)} rows from {csv_file.name}")

    df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total rows after concat: {len(df)}")
    return df


def _format(df: pd.DataFrame) -> pd.DataFrame:
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")

    str_cols = ["account_type", "description_1", "description_2", "status", "transaction_type", "source_file"]
    for col in str_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Dropped {before - len(df)} duplicate rows")
    return df


def main(csv_dir: Path = CSV_DIR, table_name: str = TABLE_NAME):
    logger.info(f"=== {table_name} ===")
    df = _concat(csv_dir=csv_dir)
    df = _format(df=df)

    conn = get_connection()
    conflict_columns = [
        "account_type", "transaction_date", "description_1", "description_2",
        "status", "transaction_type", "amount", "source_file",
    ]
    upsert_dataframe(conn, table_name, df, conflict_columns, mode="replace")
    conn.close()
    logger.info("Done.")
    return df


if __name__ == "__main__":
    main()
