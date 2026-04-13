Log a reading entry for something just consumed.

First, read `.claude/standards/Reading.md` for the full schema, templates, naming conventions, and auto-tagging rules.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — Extract title, URL, source_type, source, summary, rating, and any notes from `$ARGUMENTS`. If a URL is provided but other fields are missing, use WebFetch on the URL to extract the page title, publication/channel name, and a summary.

2. **Generate timestamps** — Get the current time. Set `timestamp_local` as `YYYY-MM-DD HH:MM ET` and `timestamp_utc` as `YYYY-MM-DDTHH:MM:SSZ`.

3. **Build filename** — Following the naming convention in `reading/CLAUDE.md`:
   - Map source_type to its abbreviation (article→art, podcast→pod, youtube→yt, paper→paper, newsletter→nl, tweet→tweet)
   - Slugify the title: lowercase, replace spaces with hyphens, strip special characters, keep 3-6 words
   - Format: `YYYY-MM-DD-{abbrev}-{slug}.md`

4. **Apply auto-tagging** — Scan the title, summary, and source against the auto-tagging rules in `reading/CLAUDE.md`. Collect all matching tags. Do not duplicate tags the user already provided.

5. **Create LOGGED entry** — Write the file to `reading/LOGGED/` using the **Reading Entry** template from `reading/CLAUDE.md`. Fill in all frontmatter fields. Set `status: "logged"`. Populate the Summary section. Leave Key Points, Takeaways, and Quotes/Data sections with placeholder prompts if the user didn't provide detailed notes.

6. **Check for matching TODO** — Search `reading/TODO/` for an entry with a matching URL or similar title. If found:
   - Copy any useful content (e.g., "Why Read This" notes) into the LOGGED entry
   - Delete the TODO file

7. **Update READING.md** — Read `reading/READING.md`. Determine today's date and the Monday of the current week.
   - If a `## Week of {monday}` section doesn't exist, create it at the top (below the header).
   - If a `### {today} ({DayName})` subsection doesn't exist, create it under the week section.
   - Prepend a one-line entry under today's heading:
     ```
     - **{source_type}** | [{Title}]({url}) | *{source}* | {#tags} | Rating: {rating}/5
       - {one-line takeaway from summary}
     ```
   - Update the `> Last updated:` line with the current timestamp.

8. **Confirm** — Show the user the created file path, the READING.md entry, and any auto-applied tags.
