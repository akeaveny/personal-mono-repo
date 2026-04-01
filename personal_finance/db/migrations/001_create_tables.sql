-- Personal Finance — SQLite DDL
-- Migrated from PostgreSQL (etf_portfolio + personal_finance schemas)
-- All tables use prefixed names instead of schema separation.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- ETF Portfolio tables
-- ============================================================

CREATE TABLE IF NOT EXISTS etf_transactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    date                TEXT NOT NULL,                       -- ISO 8601 date
    account             TEXT NOT NULL,
    transaction_type    TEXT NOT NULL
                        CHECK (transaction_type IN ('BUY', 'SELL', 'DIV', 'FXCONVERSION')),
    ticker              TEXT,
    security_name       TEXT,
    shares              REAL,
    price_per_share     REAL,
    amount              REAL NOT NULL,
    balance             REAL,
    currency            TEXT DEFAULT 'CAD'
                        CHECK (currency IN ('CAD', 'USD')),
    execution_date      TEXT,
    fx_rate             REAL,
    description         TEXT,
    source_file         TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    UNIQUE(date, account, transaction_type, description, amount, currency)
);

CREATE INDEX IF NOT EXISTS idx_etf_txn_date ON etf_transactions(date DESC);
CREATE INDEX IF NOT EXISTS idx_etf_txn_account ON etf_transactions(account);
CREATE INDEX IF NOT EXISTS idx_etf_txn_ticker ON etf_transactions(ticker);

CREATE TABLE IF NOT EXISTS import_batches (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file     TEXT NOT NULL,
    row_count       INTEGER NOT NULL DEFAULT 0,
    inserted_count  INTEGER NOT NULL DEFAULT 0,
    duplicate_count INTEGER NOT NULL DEFAULT 0,
    rejected_count  INTEGER NOT NULL DEFAULT 0,
    status          TEXT NOT NULL
                    CHECK (status IN ('processing', 'completed', 'failed')),
    started_at      TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at     TEXT
);

CREATE INDEX IF NOT EXISTS idx_import_batches_started_at ON import_batches(started_at DESC);

CREATE TABLE IF NOT EXISTS etf_holdings (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    date                TEXT NOT NULL,
    account             TEXT NOT NULL,
    ticker              TEXT NOT NULL,
    total_units         REAL,
    avg_cost_per_unit   REAL,
    book_value          REAL,
    currency            TEXT DEFAULT 'CAD',
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS etf_prices (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    date            TEXT NOT NULL,
    close_price     REAL NOT NULL,
    source          TEXT DEFAULT 'yahoo',
    created_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(ticker, date)
);

CREATE INDEX IF NOT EXISTS idx_etf_prices_ticker_date ON etf_prices(ticker, date DESC);

CREATE TABLE IF NOT EXISTS etf_paper_trades (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol              TEXT NOT NULL,
    trade_date          TEXT NOT NULL,
    side                TEXT NOT NULL
                        CHECK (side IN ('BUY', 'SELL')),
    quantity            REAL NOT NULL,
    entry_price_date    TEXT NOT NULL,
    pricing_date        TEXT NOT NULL,
    entry_price         REAL NOT NULL,
    current_price       REAL NOT NULL,
    pnl                 REAL NOT NULL,
    return_pct          REAL,
    source              TEXT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_paper_trades_created_at ON etf_paper_trades(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_paper_trades_symbol ON etf_paper_trades(symbol);

CREATE TABLE IF NOT EXISTS etf_portfolio_etfs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_category  TEXT NOT NULL,
    category_order  INTEGER NOT NULL DEFAULT 0,
    ticker          TEXT NOT NULL UNIQUE,
    etf_name        TEXT NOT NULL,
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Bank transaction tables
-- ============================================================

CREATE TABLE IF NOT EXISTS bank_rbc_transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type    TEXT,
    account_number  TEXT,
    transaction_date TEXT,
    cheque_number   TEXT,
    description_1   TEXT,
    description_2   TEXT,
    cad             REAL DEFAULT 0,
    usd             REAL DEFAULT 0,
    source_file     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(account_type, account_number, transaction_date, cheque_number,
           description_1, description_2, cad, usd, source_file)
);

CREATE TABLE IF NOT EXISTS bank_scotia_transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type    TEXT,
    transaction_date TEXT,
    description_1   TEXT,
    description_2   TEXT,
    status          TEXT,
    transaction_type TEXT,
    amount          REAL DEFAULT 0,
    source_file     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(account_type, transaction_date, description_1, description_2,
           status, transaction_type, amount, source_file)
);

-- ============================================================
-- Categorization tables
-- ============================================================

CREATE TABLE IF NOT EXISTS category_patterns (
    pattern         TEXT NOT NULL PRIMARY KEY,
    category        TEXT NOT NULL,
    subcategory     TEXT,
    notes           TEXT,
    priority        INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS transaction_overrides (
    bank            TEXT NOT NULL,
    account_type    TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    description_1   TEXT NOT NULL,
    amount          REAL NOT NULL,
    category_override   TEXT,
    subcategory_override TEXT,
    description_override TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (bank, account_type, transaction_date, description_1, amount)
);
