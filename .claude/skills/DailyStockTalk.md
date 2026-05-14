---
globs: personal_investing/DAILY_LOGS.md
---

# Daily Stock Talk Standards

This file defines the schema, format, auto-tagging rules, and append behavior for the daily stock talk log.

## Overview

A pure-markdown rolling log for capturing informal stock discussions — tips from friends, questions, gut reactions, ideas overheard at work. Designed for quick conversational logging via `/log-stock-talk`, with periodic thesis review via `/review-stock-talk`.

This is the raw signal layer. `/review-stock-talk` bridges it to `THESIS.md` by surfacing which entries reinforce, challenge, or extend the thesis.

## Directory Structure

```
personal_investing/
  DAILY_LOGS.md          # Single rolling file — all entries, newest first
```

One file. No subdirectories. No separate per-day files.

## Slash Commands

- **`/log-stock-talk`** — Log stock talk conversationally. Creates or appends to today's section.
- **`/review-stock-talk`** — Cross-reference recent entries against THESIS.md and surface actionable insights.

## DAILY_LOGS.md Structure

```markdown
# Daily Stock Talk

> Last updated: YYYY-MM-DD

## Week of YYYY-MM-DD

### YYYY-MM-DD (DayName)

- **TICKER** — {who said it / source}: {what was said or discussed}
- **TICKER** — {note, question, or observation}
- Open question: {broader market question not tied to a specific ticker}
```

Week headers use the Monday of that week (`## Week of YYYY-MM-DD`). Day entries use `###` with the day name.

## Entry Format Rules

- **Ticker mentions** are bolded: `**SPY**`, `**CVX**`
- **Attribution** comes after the ticker dash: who said it (Cone, Kap, Carl, guys at work, Reddit, etc.)
- **Open questions** that aren't ticker-specific use the prefix `Open question:`
- **Sub-bullets** for follow-up thoughts or related questions go indented under the parent
- Keep entries raw and informal — this is a capture layer, not analysis

## Append Behavior

When the user logs multiple times in one day:

1. Find the existing `### YYYY-MM-DD` section in DAILY_LOGS.md
2. Append new bullets below existing ones (never overwrite or reorder)
3. Do not duplicate entries that match an existing bullet's ticker + core idea
4. Update the `> Last updated:` timestamp

## Auto-Tagging

No auto-tagging on DAILY_LOGS.md entries. Tags are applied during `/review-stock-talk` when entries are analyzed against THESIS.md categories.

## Source Attribution Conventions

Use short, consistent names for recurring sources:

| Person/Source | Attribution |
|---|---|
| Friends by name | `Cone`, `Kap`, `Carl`, `Will` |
| Coworkers (general) | `guys at work` |
| Reddit / forums | `Reddit`, `WSB` |
| Podcast / YouTube | Channel or host name |
| Personal observation | omit attribution — just state the idea |
