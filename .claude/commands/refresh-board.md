Refresh `BOARD.md` by merging the latest tasks from `TODO/TODO.md` while preserving all manual organization, annotations, and notes in the existing board.

## Steps

### 1. Read TODO/TODO.md

Read `TODO/TODO.md`. Extract all task identifiers:

- **Google Tasks**: Each `- [ ] Task title` line under the `## Google Tasks` section. Extract the task title and any `(due: YYYY-MM-DD)` metadata.
- **Google Calendar events**: Each event line under `## Google Calendar — Next 7 Days`. Extract the event summary, date, time, and location.

Build a list of all current tasks with their identifiers.

If TODO/TODO.md does not exist or is empty, report an error and suggest running `/sync-todos` first. Do not modify BOARD.md.

### 2. Read existing TODO/BOARD.md (if it exists)

Read `TODO/BOARD.md`. If it does not exist, skip to step 5 (initial generation).

Scan the entire file content to determine which task identifiers are already present:

- **Google Tasks**: Search for each Google Task title as a substring anywhere in the file. A task is "present" if its exact title appears on any line. Be careful with short titles (under 10 characters) — match conservatively to avoid false positives.
- **Google Calendar events**: Search for each event summary as a substring. Calendar events are informational — they are added but never flagged as "removed" (since they naturally pass).

### 3. Identify changes

Compare the two sets:

- **New tasks**: In TODO/TODO.md but NOT in BOARD.md. These need to be added.
- **Removed tasks**: In BOARD.md but NO LONGER in TODO/TODO.md. These are likely completed or resolved. Only flag identifiers that match known patterns (Google Task title that was previously synced). Do not flag user-created content or calendar events as "removed."
- **Existing tasks**: Present in both. Leave completely untouched.

### 4. Merge into TODO/BOARD.md

Apply changes to the existing BOARD.md:

- **New tasks**: Append to the `## Inbox` section (create it just above `## Completed / Removed` if it doesn't exist). Format:
  - Google Tasks: `- [ ] Task title (due: date) — *via Google Tasks*`
  - Google Calendar: `- 📅 Event summary — *HH:MM – HH:MM, YYYY-MM-DD* | [Calendar](link)`
- **Removed tasks**: Find the line in BOARD.md and append ` ⚠️ gone from TODO` to the end (if not already flagged). Do NOT delete or move the line. Do NOT flag calendar events as removed.
- **Existing tasks**: Do not touch. Preserve the line and all surrounding content exactly as-is.
- **Everything else**: Preserve all other content (sections, headings, notes, blank lines, user text) exactly as-is. Do not reorder, reformat, or restructure anything.

Update the `> Last refreshed:` timestamp at the top to the current time in ET.

### 5. Initial generation (no existing BOARD.md)

If TODO/BOARD.md does not exist, create it with this structure:

```markdown
# Board

> Last refreshed: YYYY-MM-DD HH:MM ET

## Daily Focus

<!-- Pin your top priorities for today here -->

## In Progress

<!-- Active work items -->

## Up Next

<!-- Queued items you plan to start soon -->

## Inbox

<!-- New items from /refresh-board land here. Triage into sections above. -->

{all Google Tasks, formatted as: - [ ] Task title (due: date) — *via Google Tasks*}

{all Google Calendar events, formatted as: - 📅 Event summary — *HH:MM – HH:MM, YYYY-MM-DD* | [Calendar](link)}

## Backlog

<!-- Low-priority or deferred items -->

## Completed / Removed

<!-- Items flagged as gone from TODO.md. Review and delete at will. -->

---
*Managed by `/refresh-board`. Preserve Google Task titles on lines to keep merge matching working.*
```

### 6. Auto-tag new Inbox tasks

After adding new tasks to Inbox (step 4), scan each **newly added** task line against the keyword-to-tag rules below. Only tag tasks that were just added in this run — never modify tags on tasks that already existed in BOARD.md.

**Keyword → Tag rules** (case-insensitive substring match against the task title):

| Keywords | Tag |
|---|---|
| flight, flights, hotel, airbnb, trip, travel, ireland, vacation, passport | `#trip` |
| tax, taxes, RBC, CRA, bank, card, claim, finance, penalty, scotia | `#personal-finance` |
| weekly, reminder, recurring, every week | `#weekly` |

**Behavior:**

- Match each keyword as a case-insensitive substring of the task title (the text before the `—` attribution).
- A task can receive multiple tags if it matches keywords from multiple rules.
- Append tags to the end of the task title, before the `—` source attribution. Format: `- [ ] Task title #tag1 #tag2 — *via Source*`
- If no keywords match, leave the task line untagged.
- Never add, remove, or modify tags on tasks that were already in BOARD.md before this run.

### Important Notes

- NEVER modify TODO/TODO.md — it is read-only from this command's perspective.
- Preserve all user content in BOARD.md exactly as written — sections, formatting, tags, notes, indentation, blank lines.
- The merge is additive and conservative: only add new tasks and flag removed ones. Never delete, move, or reformat existing content.
- Use the current time in ET for the "Last refreshed" timestamp.
- Calendar events are transient — add new ones to Inbox, but never flag old ones as "removed."
