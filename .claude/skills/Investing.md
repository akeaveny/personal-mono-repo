---
globs: personal_investing/**
---

# Investing Module Standards

This file defines the schema, templates, naming conventions, and rules for the investing research tracker.

## Overview

A pure-markdown system for logging investing research (YouTube, PDFs, articles, earnings, 13F filings) with a TODO → LOGGED lifecycle, rolling research log, and thesis impact tracking. Each logged item explicitly ties back to claims in `personal_investing/THESIS.md`, so research accumulates over time to continually build and sharpen the thesis.

## Directory Structure

```
personal_investing/
  THESIS.md              # Master investing thesis
  RESEARCH.md            # Rolling log of consumed research (newest first)
  references/
    TODO/                # Items queued to consume
    LOGGED/              # Consumed research with thesis impact notes
```

Flat files (one `.md` per item). Entries are self-contained with URLs or file paths.

## Slash Commands

- **`/log-investing`** — Log research you just consumed. Creates a LOGGED entry and updates RESEARCH.md.
- **`/queue-investing`** — Queue something to consume later. Creates a TODO entry.

## YAML Frontmatter Schema

Every investing entry (TODO or LOGGED) uses this frontmatter:

```yaml
---
timestamp_local: "YYYY-MM-DD HH:MM ET"
timestamp_utc: "YYYY-MM-DDTHH:MM:SSZ"
source_type: ""         # youtube | pdf | article | earnings | 13f | newsletter
source: ""              # channel/publication/company name
url: ""                 # URL or file path
tickers: []             # affected tickers, e.g. [CVX, DVN]
tags: []                # e.g. [energy, uranium, macro]
summary: ""             # 1-2 sentence summary
thesis_impact: ""       # SUPPORTS | CONTRADICTS | NEUTRAL | MIXED
conviction_delta: 0     # -2 to +2 (-2 major reduction, +2 major boost, 0 no change)
status: "todo"          # "todo" or "logged"
---
```

## File Naming Convention

Format: `YYYY-MM-DD-{type}-{slug}.md`

Type abbreviations:

| source_type | abbreviation |
|---|---|
| youtube | `yt` |
| pdf | `pdf` |
| article | `art` |
| earnings | `earn` |
| 13f | `13f` |
| newsletter | `nl` |

Slug rules:
- Lowercase, hyphen-separated
- Derived from title
- Keep short but recognizable (3-6 words)

Examples:
- `2026-03-30-yt-uranium-bull-case-cameco.md`
- `2026-03-30-pdf-morningstar-canadian-equity-highlights.md`
- `2026-03-30-earn-cvx-q4-2025.md`

## Entry Templates

### Research Entry (LOGGED/)

Used when logging something you've already consumed.

```markdown
---
timestamp_local: "{timestamp_local}"
timestamp_utc: "{timestamp_utc}"
source_type: "{source_type}"
source: "{source}"
url: "{url}"
tickers: [{tickers}]
tags: [{tags}]
summary: "{summary}"
thesis_impact: "{SUPPORTS|CONTRADICTS|NEUTRAL|MIXED}"
conviction_delta: {-2 to +2}
status: "logged"
---

# {Title}

## Summary

{1-3 sentence summary of what this source covers and why it matters.}

## Key Claims

1. **{Claim headline.}** {Supporting detail — specific numbers, quotes, or data points.}
2. **{Claim headline.}** {Supporting detail.}
3. **{Claim headline.}** {Supporting detail.}

## Thesis Impact

- **Impact:** SUPPORTS | CONTRADICTS | NEUTRAL | MIXED
- **Tickers affected:** {tickers}
- **Claims touched:**
  - *STRONGLY SUPPORTS* — {thesis claim this strongly reinforces, quoted or paraphrased from THESIS.md}
  - *SUPPORTS* — {thesis claim this supports}
  - *CONTRADICTS* — {thesis claim this challenges}
  - *NEUTRAL* — {thesis claim this is tangentially related to but doesn't move}

## What I'm Taking Away

- {Concrete belief update, position change, or action item. Be specific.}

## Source

[{Title}]({url}) — *{source}*
```

### TODO Entry (TODO/)

Used when queuing something to consume later.

```markdown
---
timestamp_local: "{timestamp_local}"
timestamp_utc: "{timestamp_utc}"
source_type: "{source_type}"
source: "{source}"
url: "{url}"
tickers: [{tickers}]
tags: [{tags}]
summary: "{summary}"
thesis_impact: ""
conviction_delta: 0
status: "todo"
---

# {Title}

## Why Review This

{What you expect to learn — which thesis area does this touch?}

## Source

[{Title}]({url}) — *{source}*
```

## Auto-Tagging Rules

Applied at creation time only (keyword matching, case-insensitive). Manual edits are never overwritten.

| Keywords | Tag |
|---|---|
| energy, oil, gas, crude, pipeline, lng, refin, chevron, devon, valero, cheniere | `#energy` |
| uranium, nuclear, cameco, uec, cigar | `#uranium` |
| gold, silver, copper, materials, mining, miner, barrick, agnico | `#materials` |
| ai, artificial intelligence, semiconductor, chip, nvidia, tsmc, broadcom, marvell, micron | `#ai-semis` |
| macro, fed, rate, inflation, recession, yield, economy, tariff, gdp | `#macro` |
| 13f, insider, form4, sedi, filing | `#filing` |
| earnings, revenue, guidance, eps, q1, q2, q3, q4, results | `#earnings` |
| canada, tsx, xic, cad, morningstar canada | `#canada` |

## RESEARCH.md Format

Rolling log, newest first, grouped by week then day:

```markdown
# Investing Research Log

> Last updated: YYYY-MM-DD HH:MM ET

## Week of YYYY-MM-DD

### YYYY-MM-DD (Day)

- **youtube** | [Title](url) | *Channel* | #energy #uranium | Impact: SUPPORTS | Delta: +1
  - One-line thesis takeaway
```

Week headers use the Monday of that week. Day headers include the day name (e.g., `Monday`).
