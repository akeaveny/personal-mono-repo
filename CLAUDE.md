# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Obsidian vault that serves as a personal productivity system — task tracking, weekly planning, daily journaling, and investing research. All manually maintained.

## Vault Structure

```
daily_journal/
  JOURNAL.md             # Single rolling file — all entries, newest first
  GOALS.md               # Personal operating doc — health, structure, habits
  PLANNING.md            # Rolling weekly plan (overwritten each week)
  BOARD.md               # Backlog and longer-term tasks (manually maintained)
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
.claude/skills/
  DailyJournal.md        # Daily journal standards (schema, templates, rules)
  Documents.md           # Documents module standards (schema, naming, rules)
  Investing.md           # Investing module standards (schema, templates, rules)
  DailyStockTalk.md      # Stock talk log standards (schema, format, rules)
.claude/commands/        # Slash command definitions
  journal.md             # /journal command
  journal-review.md      # /journal-review command
  log-investing.md       # /log-investing command
  queue-investing.md     # /queue-investing command
  log-stock-talk.md      # /log-stock-talk command
  review-stock-talk.md   # /review-stock-talk command
```

## Task & Planning System

`TODO/BOARD.md` is a manually maintained backlog for longer-term tasks, organized by category sections (Trips, Personal Finance, etc.) with inline `#hashtags`. Edit it directly — there is no automated sync.

`daily_journal/PLANNING.md` is a rolling weekly plan — overwritten each week with the upcoming schedule, tasks for the week, and any random items. Kept separate from the backlog.

`daily_journal/GOALS.md` is a personal operating document covering health goals, habit patterns, and structure rules. Reviewed monthly, referenced by `/journal-review`.

## Daily Journal Module

The `daily_journal/` directory is a self-contained daily journal for logging food, spending, mood, personal growth, and relationships. Standards (schema, templates, naming, auto-tag rules, append behavior) are in `.claude/skills/DailyJournal.md`.

- **`/journal`** — Log a daily entry conversationally (designed for quick phone sessions)
- **`/journal-review`** — Generate a weekly review with patterns, spending breakdown, and goals

Everything lives in a single `JOURNAL.md` file — entries are grouped by week, newest first. Multiple logs in one day append to the same day's section.

## Documents Module

The `documents/` directory stores personal reference documents — bills, leases, invoices, insurance, identity, and employment contracts. Standards (naming convention, boundary rules) are in `.claude/skills/Documents.md`.

This is separate from `personal_finance/` (data pipeline for transaction analytics) and `taxes/` (tax filing and compliance). The boundary: if it's a **reference record** you might look up later, it goes in `documents/`. If it's analytical source data, it stays in `personal_finance/`. If it's tax-related, it stays in `taxes/`.

Files follow the naming convention: `YYYY-MM-DD_vendor_description.ext` (day optional). Subdirectories are organized by year (except `identity/`, which is flat).

## Investing Module

The `personal_investing/` directory is a self-contained investing research tracker. Standards (schema, templates, naming, auto-tag rules) are in `.claude/skills/Investing.md`.

- **`/queue-investing`** — Queue a YouTube video, PDF, article, or earnings report to review later
- **`/log-investing`** — Log something you just consumed, with explicit thesis impact
- **`/log-stock-talk`** — Log informal stock discussions conversationally (tips, questions, ideas)
- **`/review-stock-talk`** — Cross-reference recent stock talk against THESIS.md to surface actionable insights

Each logged entry ties its claims back to `THESIS.md`, so research accumulates over time and continually builds the thesis. `RESEARCH.md` is the rolling log. `DAILY_LOGS.md` captures raw conversational signal — `/review-stock-talk` bridges it to the thesis. `references/TODO/` and `references/LOGGED/` hold queued and consumed research respectively.

---
name: karpathy-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

