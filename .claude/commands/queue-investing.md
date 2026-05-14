Queue an investing research item to consume later.

First, read `.claude/skills/Investing.md` for the full schema, templates, naming conventions, and auto-tagging rules.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — Extract title, URL, source_type, source, tickers, and why-review-this from `$ARGUMENTS`. If a URL is provided but other fields are missing, use WebFetch to extract the title, source name, and a brief description.

2. **Generate timestamps** — Get the current time. Set `timestamp_local` as `YYYY-MM-DD HH:MM ET` and `timestamp_utc` as `YYYY-MM-DDTHH:MM:SSZ`.

3. **Build filename** — Following the naming convention in `.claude/skills/Investing.md`:
   - Map source_type to its abbreviation (youtube→yt, pdf→pdf, article→art, earnings→earn, 13f→13f, newsletter→nl)
   - Slugify the title: lowercase, replace spaces with hyphens, strip special characters, keep 3-6 words
   - Format: `YYYY-MM-DD-{abbrev}-{slug}.md`

4. **Apply auto-tagging** — Scan the title, description, and tickers against the auto-tagging rules in `.claude/skills/Investing.md`. Collect all matching tags.

5. **Check for duplicates** — Search `personal_investing/references/TODO/` and `personal_investing/references/LOGGED/` for an entry with the same URL. If found, inform the user and stop.

6. **Create TODO entry** — Write the file to `personal_investing/references/TODO/` using the **TODO Entry** template from `.claude/skills/Investing.md`. Set `status: "todo"`, `conviction_delta: 0`.

7. **Confirm** — Show the user the created file path and any auto-applied tags.
