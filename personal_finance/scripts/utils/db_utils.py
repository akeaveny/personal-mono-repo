"""SQLite connection and bulk upsert helpers for personal_finance.db."""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent.parent.parent / "personal_finance.db"


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Return a sqlite3.Connection to the personal_finance database."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def upsert_dataframe(
    conn: sqlite3.Connection,
    table: str,
    df: pd.DataFrame,
    conflict_columns: List[str],
    mode: str = "ignore",
) -> int:
    """Bulk upsert a DataFrame into a SQLite table.

    Args:
        conn: SQLite connection.
        table: Target table name.
        df: DataFrame to insert.
        conflict_columns: Columns that form the UNIQUE/PK constraint.
        mode: 'ignore' for INSERT OR IGNORE, 'replace' for INSERT OR REPLACE.

    Returns:
        Number of rows affected.
    """
    if df.empty:
        logger.info(f"Empty DataFrame — nothing to upsert into {table}")
        return 0

    columns = df.columns.tolist()
    placeholders = ", ".join(["?"] * len(columns))
    col_str = ", ".join(columns)

    if mode == "replace":
        sql = f"INSERT OR REPLACE INTO {table} ({col_str}) VALUES ({placeholders})"
    else:
        sql = f"INSERT OR IGNORE INTO {table} ({col_str}) VALUES ({placeholders})"

    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    cursor = conn.cursor()
    before = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    cursor.executemany(sql, rows)
    conn.commit()
    after = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    inserted = after - before
    duplicates = len(rows) - inserted
    logger.info(
        f"Upserted into {table}: {len(rows)} rows processed, "
        f"{inserted} inserted, {duplicates} duplicates/skipped"
    )
    return inserted


def create_import_batch(conn: sqlite3.Connection, source_file: str) -> int:
    """Create a new import batch record and return its ID."""
    now = datetime.utcnow().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO import_batches (source_file, status, started_at)
           VALUES (?, 'processing', ?)""",
        (source_file, now),
    )
    conn.commit()
    return cursor.lastrowid


def finish_import_batch(
    conn: sqlite3.Connection,
    batch_id: int,
    row_count: int,
    inserted: int,
    duplicates: int,
    rejected: int,
    status: str = "completed",
) -> None:
    """Finalize an import batch record."""
    now = datetime.utcnow().isoformat()
    conn.execute(
        """UPDATE import_batches
           SET row_count = ?, inserted_count = ?, duplicate_count = ?,
               rejected_count = ?, status = ?, finished_at = ?
           WHERE id = ?""",
        (row_count, inserted, duplicates, rejected, status, now, batch_id),
    )
    conn.commit()
