#!/usr/bin/env python3
"""Apply SQL migrations to create/update personal_finance.db."""

import sqlite3
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "db" / "migrations"
DB_PATH = Path(__file__).resolve().parent.parent / "personal_finance.db"


def apply_migrations(db_path: Path = DB_PATH, migrations_dir: Path = MIGRATIONS_DIR):
    """Read all .sql files in order and execute them against the database."""
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print(f"No migration files found in {migrations_dir}")
        return

    conn = sqlite3.connect(str(db_path))
    print(f"Database: {db_path}")

    for sql_file in migration_files:
        print(f"  Applying {sql_file.name} ...")
        sql = sql_file.read_text()
        conn.executescript(sql)

    conn.close()
    print(f"Done — {len(migration_files)} migration(s) applied.")


if __name__ == "__main__":
    apply_migrations()
