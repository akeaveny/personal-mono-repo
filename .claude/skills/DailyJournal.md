---
globs: daily_journal/**
---

# Daily Journal Module Standards

This file defines the schema, templates, append behavior, auto-tagging rules, and format for the daily journal.

## Overview

A pure-markdown system for logging daily food, spending, mood, personal growth, and relationships. All entries live in a single rolling file (`JOURNAL.md`), newest first, grouped by week. Designed for quick conversational logging via remote Claude Code sessions (phone), with a weekly review cycle.

## Directory Structure

```
daily_journal/
  JOURNAL.md             # Single rolling file — all entries, newest first
```

One file. No subdirectories. No separate per-day files.

## Slash Commands

- **`/journal`** — Log a daily entry conversationally. Creates or appends to today's section in JOURNAL.md.
- **`/journal-review`** — Generate a weekly review with patterns, spending breakdown, and goals.

## JOURNAL.md Structure

```markdown
# Daily Journal

> Last updated: YYYY-MM-DD HH:MM ET

## Week of YYYY-MM-DD

### YYYY-MM-DD (DayName) | Mood: X/10 | Energy: X/10 | Spent: $X.XX | #tags

> {highlight}

#### Mood & Energy

- **Mood**: {score}/10 — {brief description}
- **Energy**: {score}/10 — {brief description}
- **Notes**: {physical/emotional context}

#### Food

| Meal | What |
|---|---|
| Breakfast | |
| Lunch | |
| Dinner | |
| Snacks | |

#### Spending

| Item | Amount | Category |
|---|---|---|
| | | |

**Day total**: $0.00

#### Personal Growth

- {reflections on self-improvement, lessons learned, habits}

#### Relationships

- {reflections on interactions, conversations, connection}

#### Free Notes

{anything else — highlights, gratitude, random thoughts}
```

Week headers use the Monday of that week (`## Week of YYYY-MM-DD`). Day entries use `###` with metadata inline. Sections within a day use `####`.

## Append Behavior

When the user logs multiple times in one day:

1. Find the existing `### YYYY-MM-DD` section in JOURNAL.md
2. Merge new info into existing sections (don't duplicate, don't overwrite user edits)
3. Add new food/spending rows to tables
4. Recalculate spending total from all spending rows
5. Update mood/energy scores to latest provided (note time of day if different)
6. Update highlight if improved or was empty
7. Update the `###` header line with latest mood/energy/spend/tags

## Auto-Tagging Rules

Content-based (not just title), case-insensitive, applied at creation/update. Manual edits are never overwritten.

| Keywords | Tag |
|---|---|
| gym, workout, exercise, run, running, lift, yoga, swim | `fitness` |
| date, friends, family, party, dinner out, social, hangout | `social` |
| work, meeting, project, deadline, office | `work` |
| travel, trip, flight, airport, hotel | `travel` |
| sick, tired, headache, unwell, doctor, medication | `health` |
| book, reading, course, learning, study | `learning` |
| rest, relax, lazy, recovery, sleep in, nap | `rest` |

## Weekly Review Format

Inserted into JOURNAL.md at the top of the current week section (after `## Week of` header, before any day entries):

```markdown
### Weekly Review: YYYY-MM-DD — YYYY-MM-DD

#### Numbers
- **Days logged**: X/7
- **Avg mood**: X.X/10
- **Avg energy**: X.X/10
- **Total spending**: $X.XX

#### Spending Breakdown

| Category | Amount | % of Total |
|---|---|---|
| Food | $X.XX | XX% |
| ... | ... | ... |

#### Patterns & Insights
- {mood/energy correlations with tags}
- {spending outliers}
- {recurring themes}

#### Progress on Previous Goals
- {goal from last review} — {status}

#### Goals for Next Week
- {goal 1}
- {goal 2}
- {goal 3}
```
