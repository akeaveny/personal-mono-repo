# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Obsidian vault that serves as a personal productivity system — task tracking, weekly planning, daily journaling, reading logs, investing research, and meal logging. All manually maintained.

## Vault Structure

```
daily_journal/
  JOURNAL.md             # Single rolling file — all entries, newest first
  GOALS.md               # Personal operating doc — health, structure, habits
  PLANNING.md            # Rolling weekly plan (overwritten each week)
  BOARD.md               # Backlog and longer-term tasks (manually maintained)
reading/
  READING.md             # Rolling weekly reading log (newest first)
  TODO/                  # Items queued to read/watch (status: "todo")
  LOGGED/                # Consumed items with notes (status: "logged")
documents/
  lease/                 # Lease agreements, by year
  bills/                 # Utility bills, subscriptions, by year
  invoices/              # Invoices sent or received, by year
  insurance/             # Policies, claim docs, by year
  identity/              # Passport scans, IDs (flat, no year dirs)
  employment/            # Employment agreements, offer letters, by year
personal_finance/        # Financial data pipeline (CSVs, DB, dbt, scripts)
taxes/                   # Tax filing by year (slips, returns, disputes)
personal_investing/
  THESIS.md              # Master investing thesis
  RESEARCH.md            # Rolling log of consumed research (newest first)
  DAILY_LOGS.md          # Rolling stock talk log (newest first)
  TODO.md                # Investing action items and TODOs
  references/
    TODO/                # Research items queued to consume
    LOGGED/              # Consumed research with thesis impact notes
gym/
  Training_Plan.md       # 4-day hypertrophy split + cycling schedule
  Meal_Prep.md           # Meal prep notes
  Logging_Meals.md       # Rolling meal log (newest week first)
CLAUDE.md                # This file
.claude/standards/
  Reading.md             # Reading module standards (schema, templates, rules)
  DailyJournal.md        # Daily journal standards (schema, templates, rules)
  Documents.md           # Documents module standards (schema, naming, rules)
  Investing.md           # Investing module standards (schema, templates, rules)
  DailyStockTalk.md      # Stock talk log standards (schema, format, rules)
  MealLogging.md         # Meal logging standards (schema, estimation, patterns)
.claude/commands/        # Slash command definitions
  log-reading.md         # /log-reading command
  add-to-reading-list.md # /add-to-reading-list command
  weekly-digest.md       # /weekly-digest command
  journal.md             # /journal command
  journal-review.md      # /journal-review command
  log-investing.md       # /log-investing command
  queue-investing.md     # /queue-investing command
  log-stock-talk.md      # /log-stock-talk command
  review-stock-talk.md   # /review-stock-talk command
  log-meal.md            # /log-meal command
```

## Task & Planning System

`TODO/BOARD.md` is a manually maintained backlog for longer-term tasks, organized by category sections (Trips, Personal Finance, etc.) with inline `#hashtags`. Edit it directly — there is no automated sync.

`daily_journal/PLANNING.md` is a rolling weekly plan — overwritten each week with the upcoming schedule, tasks for the week, and any random items. Kept separate from the backlog.

`daily_journal/GOALS.md` is a personal operating document covering health goals, habit patterns, and structure rules. Reviewed monthly, referenced by `/journal-review`.

## Reading Module

The `reading/` directory is a self-contained reading tracker. Standards (schema, templates, naming, auto-tag rules) are in `.claude/standards/Reading.md`.

- **`/add-to-reading-list`** — Queue an article, podcast, or video to read/watch later
- **`/log-reading`** — Log something you just consumed
- **`/weekly-digest`** — Generate a weekly summary from logged entries

## Daily Journal Module

The `daily_journal/` directory is a self-contained daily journal for logging food, spending, mood, personal growth, and relationships. Standards (schema, templates, naming, auto-tag rules, append behavior) are in `.claude/standards/DailyJournal.md`.

- **`/journal`** — Log a daily entry conversationally (designed for quick phone sessions)
- **`/journal-review`** — Generate a weekly review with patterns, spending breakdown, and goals

Everything lives in a single `JOURNAL.md` file — entries are grouped by week, newest first. Multiple logs in one day append to the same day's section.

## Documents Module

The `documents/` directory stores personal reference documents — bills, leases, invoices, insurance, identity, and employment contracts. Standards (naming convention, boundary rules) are in `.claude/standards/Documents.md`.

This is separate from `personal_finance/` (data pipeline for transaction analytics) and `taxes/` (tax filing and compliance). The boundary: if it's a **reference record** you might look up later, it goes in `documents/`. If it's analytical source data, it stays in `personal_finance/`. If it's tax-related, it stays in `taxes/`.

Files follow the naming convention: `YYYY-MM-DD_vendor_description.ext` (day optional). Subdirectories are organized by year (except `identity/`, which is flat).

## Investing Module

The `personal_investing/` directory is a self-contained investing research tracker. Standards (schema, templates, naming, auto-tag rules) are in `.claude/standards/Investing.md`.

- **`/queue-investing`** — Queue a YouTube video, PDF, article, or earnings report to review later
- **`/log-investing`** — Log something you just consumed, with explicit thesis impact
- **`/log-stock-talk`** — Log informal stock discussions conversationally (tips, questions, ideas)
- **`/review-stock-talk`** — Cross-reference recent stock talk against THESIS.md to surface actionable insights

Each logged entry ties its claims back to `THESIS.md`, so research accumulates over time and continually builds the thesis. `RESEARCH.md` is the rolling log (mirrors `reading/READING.md`). `DAILY_LOGS.md` captures raw conversational signal — `/review-stock-talk` bridges it to the thesis. `references/TODO/` and `references/LOGGED/` mirror `reading/TODO/` and `reading/LOGGED/`.

## Meal Logging Module

The `gym/` directory includes a meal tracker focused on building awareness of eating habits — not strict calorie goals. Standards (schema, estimation rules, weekly patterns) are in `.claude/standards/MealLogging.md`.

- **`/log-meal`** — Log what you ate conversationally (designed for quick phone sessions)

Everything lives in a single `Logging_Meals.md` file — entries are grouped by week, newest first. Multiple logs in one day append to the same day's meal table. Weekly pattern summaries auto-generate when a new week starts (if 3+ days were logged). Calorie and protein estimates are approximate — the goal is spotting patterns over time, not precision tracking.

