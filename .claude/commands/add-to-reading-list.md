Add an item to the reading list for later consumption.

First, read `.claude/standards/Reading.md` for the full schema, templates, naming conventions, and auto-tagging rules.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — Extract title, URL, source_type, source, and why-read-this from `$ARGUMENTS`. If a URL is provided but other fields are missing, use WebFetch on the URL to extract the page title, publication/channel name, and a brief summary.

2. **Generate timestamps** — Get the current time. Set `timestamp_local` as `YYYY-MM-DD HH:MM ET` and `timestamp_utc` as `YYYY-MM-DDTHH:MM:SSZ`.

3. **Build filename** — Following the naming convention in `reading/CLAUDE.md`:
   - Map source_type to its abbreviation (article→art, podcast→pod, youtube→yt, paper→paper, newsletter→nl, tweet→tweet)
   - Slugify the title: lowercase, replace spaces with hyphens, strip special characters, keep 3-6 words
   - Format: `YYYY-MM-DD-{abbrev}-{slug}.md`

4. **Apply auto-tagging** — Scan the title, summary, and source against the auto-tagging rules in `reading/CLAUDE.md`. Collect all matching tags. Do not duplicate tags the user already provided.

5. **Check for duplicates** — Search `reading/TODO/` and `reading/LOGGED/` for an entry with the same URL. If found, inform the user and stop (don't create a duplicate).

6. **Create TODO entry** — Write the file to `reading/TODO/` using the **TODO Entry** template from `reading/CLAUDE.md`. Fill in all frontmatter fields. Set `status: "todo"`, `rating: 0`. Populate the "Why Read This" section from user input or generate a brief reason from the summary.

7. **Confirm** — Show the user the created file path and any auto-applied tags.
