# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Obsidian vault that serves as a lightweight TODO tracker. Tasks are pulled on-demand from Google Tasks and Google Calendar via the `/sync-todos` slash command.

## Vault Structure

```
TODO/
  TODO.md                # Auto-generated task list (do not edit manually)
  BOARD.md               # Curated task board (manually organized, merge-updated)
reading/
  READING.md             # Rolling weekly reading log (newest first)
  TODO/                  # Items queued to read/watch (status: "todo")
  LOGGED/                # Consumed items with notes (status: "logged")
daily_journal/
  JOURNAL.md             # Single rolling file — all entries, newest first
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
CLAUDE.md                # This file
.claude/standards/
  Reading.md             # Reading module standards (schema, templates, rules)
  DailyJournal.md        # Daily journal standards (schema, templates, rules)
  Documents.md           # Documents module standards (schema, naming, rules)
  Investing.md           # Investing module standards (schema, templates, rules)
  DailyStockTalk.md      # Stock talk log standards (schema, format, rules)
.claude/commands/        # Slash command definitions
  sync-todos.md          # /sync-todos command
  refresh-board.md       # /refresh-board command
  log-reading.md         # /log-reading command
  add-to-reading-list.md # /add-to-reading-list command
  weekly-digest.md       # /weekly-digest command
  journal.md             # /journal command
  journal-review.md      # /journal-review command
  log-investing.md       # /log-investing command
  queue-investing.md     # /queue-investing command
  log-stock-talk.md      # /log-stock-talk command
  review-stock-talk.md   # /review-stock-talk command
```

## How `/sync-todos` Works

Run `/sync-todos` to regenerate `TODO/TODO.md` with current tasks from:

1. **Google Tasks** — All incomplete tasks
2. **Google Calendar** — Upcoming events for the next 7 days

The command fully replaces `TODO/TODO.md` on each run. Partial failures (e.g., Google Tasks unavailable) produce inline HTML comments but don't block the sync.

`TODO/TODO.md` is auto-generated. Do not edit it manually — changes will be overwritten on the next sync.

## How `/refresh-board` Works

Run `/refresh-board` to merge the latest tasks from `TODO/TODO.md` into `TODO/BOARD.md`:

1. **New tasks** from TODO.md are added to the `## Inbox` section of BOARD.md
2. **Removed tasks** (in BOARD.md but no longer in TODO.md) are flagged with ` ⚠️ gone from TODO`
3. **Existing tasks** and all user annotations, groupings, tags, and notes are preserved exactly as-is

The merge matches tasks by Google Task title. Preserve task titles on lines to keep sync working. Calendar events are transient and never flagged as removed.

`TODO/BOARD.md` is user-curated. Edit it freely — `/refresh-board` only adds new tasks to Inbox and flags removed ones. It never deletes, moves, or reformats your content.

Typical workflow:
1. Run `/sync-todos` to pull latest from Google Tasks and Google Calendar
2. Run `/refresh-board` to merge new tasks into your board
3. Manually organize: move items from Inbox to Daily Focus, In Progress, etc.

## Tagging System

BOARD.md uses a combination of **section-based grouping** and **inline hashtags** for task categorization.

### Category sections

The board includes dedicated sections between "Up Next" and "Inbox" for primary categories:

- **Trips** — Travel-related tasks (flights, hotels, trip planning)
- **Personal Finance** — Banking, taxes, insurance claims, cards
- **Weekly Reminders** — Recurring weekly items

Move tasks from Inbox into these sections during triage. New sections can be added freely.

### Inline hashtags

Tasks can carry inline hashtags for cross-cutting concerns: `#trip`, `#personal-finance`, `#weekly`. Tags go at the end of the task title, before the `—` source attribution:

```
- [ ] Book flights for Ireland #trip — *via Google Tasks*
```

Users can add any custom hashtag — the system is open-ended.

### Auto-tagging rules

`/refresh-board` automatically tags **new** tasks added to Inbox using keyword matching (case-insensitive):

| Keywords | Tag |
|---|---|
| flight, flights, hotel, airbnb, trip, travel, ireland, vacation, passport | `#trip` |
| tax, taxes, RBC, CRA, bank, card, claim, finance, penalty, scotia | `#personal-finance` |
| weekly, reminder, recurring, every week | `#weekly` |

Auto-tagging only applies to newly added tasks. Existing tasks are never re-tagged — manual tag edits are always preserved.

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

## MCP Integrations

- **Google Tasks**: Configured in `.mcp.json`. Provides `list`, `search`, `create`, `update`, `delete`, and `clear` operations.
- **Google Calendar**: Configured in `.mcp.json`. Provides `list-events`, `search-events`, `create-event`, `update-event`, `delete-event`, and more.
