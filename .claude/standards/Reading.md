---
globs: reading/**
---

# Reading Module Standards

This file defines the schema, templates, naming conventions, and rules for the reading tracker module.

## Overview

A pure-markdown system for logging articles, podcasts, and YouTube videos with a TODO → LOGGED lifecycle, rolling log, and slash command automation.

## Directory Structure

```
reading/
  CLAUDE.md              # Module-specific instructions (points here)
  READING.md             # Rolling weekly reading log (newest first)
  TODO/                  # Items queued to read/watch (status: "todo")
  LOGGED/                # Consumed items with notes (status: "logged")
```

Flat files (one `.md` per item). Reading entries are self-contained with URLs.

## Slash Commands

- **`/log-reading`** — Log something you just consumed. Creates a LOGGED entry and updates READING.md.
- **`/add-to-reading-list`** — Queue something to read later. Creates a TODO entry.
- **`/weekly-digest`** — Generate a weekly summary from LOGGED entries.

## YAML Frontmatter Schema

Every reading entry (TODO or LOGGED) uses this frontmatter:

```yaml
---
timestamp_local: "YYYY-MM-DD HH:MM ET"
timestamp_utc: "YYYY-MM-DDTHH:MM:SSZ"
source_type: ""       # article | podcast | youtube | paper | newsletter | tweet
source: ""            # publication/channel/podcast name
url: ""               # original URL
tags: []              # open-ended, e.g. [ai, economics, climate]
summary: ""           # 1-2 sentence summary
rating: 0             # 1-5 (0 = unrated, for TODO items)
status: "todo"        # "todo" or "logged"
---
```

## File Naming Convention

Format: `YYYY-MM-DD-{type}-{slug}.md`

Type abbreviations:

| source_type | abbreviation |
|---|---|
| article | `art` |
| podcast | `pod` |
| youtube | `yt` |
| paper | `paper` |
| newsletter | `nl` |
| tweet | `tweet` |

Slug rules:
- Lowercase, hyphen-separated
- Derived from title
- Keep short but recognizable (3-6 words)

Examples:
- `2026-03-19-pod-huberman-sleep-optimization.md`
- `2026-03-18-art-economist-ai-regulation.md`
- `2026-03-17-yt-veritasium-quantum-computing.md`

## Entry Templates

### Reading Entry (LOGGED/)

Used when logging something you've already consumed.

```markdown
---
timestamp_local: "{timestamp_local}"
timestamp_utc: "{timestamp_utc}"
source_type: "{source_type}"
source: "{source}"
url: "{url}"
tags: [{tags}]
summary: "{summary}"
rating: {rating}
status: "logged"
---

# {Title}

## Summary

{1-2 sentence summary of the content}

## Key Points

- {key point 1}
- {key point 2}
- {key point 3}

## Takeaways

- {personal takeaway or action item}

## Quotes / Data

> {notable quote or data point}

## Source

[{Title}]({url}) — *{source}*
```

### TODO Entry (TODO/)

Used when queuing something to read/watch later.

```markdown
---
timestamp_local: "{timestamp_local}"
timestamp_utc: "{timestamp_utc}"
source_type: "{source_type}"
source: "{source}"
url: "{url}"
tags: [{tags}]
summary: "{summary}"
rating: 0
status: "todo"
---

# {Title}

## Why Read This

{Why this is worth reading/watching — what you expect to learn}

## Source

[{Title}]({url}) — *{source}*
```

### Research Entry (TODO/ → LOGGED/)

Used for research questions that involve multiple sources.

```markdown
---
timestamp_local: "{timestamp_local}"
timestamp_utc: "{timestamp_utc}"
source_type: "{source_type}"
source: "{source}"
url: "{url}"
tags: [{tags}]
summary: "{summary}"
rating: {rating}
status: "{status}"
---

# {Title}

## Question / Hypothesis

{The question you're investigating or hypothesis you're testing}

## Research Notes

{Notes from reading/watching}

## Sources

- [{Source 1 Title}]({url1})
- [{Source 2 Title}]({url2})

## Conclusion

{What you concluded from the research}
```

## Auto-Tagging Rules

Applied at creation time only (keyword matching, case-insensitive). Manual edits are never overwritten.

| Keywords | Tag |
|---|---|
| ai, artificial intelligence, machine learning, llm, gpt, claude, openai, deepmind, neural | `#ai` |
| finance, investing, markets, stocks, bonds, crypto, bitcoin, economy, economics | `#finance` |
| health, fitness, sleep, nutrition, exercise, mental health, meditation | `#health` |
| climate, energy, solar, wind, nuclear, carbon, emissions | `#climate` |
| programming, software, code, engineering, developer, typescript, python, rust | `#tech` |
| politics, policy, regulation, government, election | `#politics` |
| science, research, study, physics, biology, chemistry | `#science` |
| productivity, workflow, habits, systems, tools | `#productivity` |

## READING.md Format

Rolling log, newest first, grouped by week then day:

```markdown
# Reading Log

> Last updated: YYYY-MM-DD HH:MM ET

## Week of YYYY-MM-DD

### YYYY-MM-DD (Day)

- **article** | [Title](url) | *Source* | #tag1 #tag2 | Rating: 3/5
  - One-line takeaway
```

Week headers use the Monday of that week. Day headers include the day name (e.g., `Thursday`).
