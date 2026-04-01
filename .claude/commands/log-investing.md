Log an investing research entry for something just consumed.

First, read `.claude/standards/Investing.md` for the full schema, templates, naming conventions, and auto-tagging rules.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — Extract title, URL, source_type, source, tickers, summary, thesis_impact, conviction_delta, and notes from `$ARGUMENTS`. If a URL is provided but other fields are missing, use WebFetch on the URL to extract the page title, channel/publication name, and a summary.

2. **Generate timestamps** — Get the current time. Set `timestamp_local` as `YYYY-MM-DD HH:MM ET` and `timestamp_utc` as `YYYY-MM-DDTHH:MM:SSZ`.

3. **Build filename** — Following the naming convention in `.claude/standards/Investing.md`:
   - Map source_type to its abbreviation (youtube→yt, pdf→pdf, article→art, earnings→earn, 13f→13f, newsletter→nl)
   - Slugify the title: lowercase, replace spaces with hyphens, strip special characters, keep 3-6 words
   - Format: `YYYY-MM-DD-{abbrev}-{slug}.md`

4. **Apply auto-tagging** — Scan the title, summary, tickers, and source against the auto-tagging rules in `.claude/standards/Investing.md`. Collect all matching tags. Do not duplicate tags the user already provided.

5. **Create LOGGED entry** — Write the file to `personal_investing/references/LOGGED/` using the **Research Entry** template from `.claude/standards/Investing.md`. Fill in all frontmatter fields. Set `status: "logged"`. Populate Summary and Key Claims from what the user provided. If thesis_impact or conviction_delta were not specified, make a reasonable inference from the content and label it as inferred.

5a. **Move and rename source file (PDFs only)** — If source_type is `pdf` and the url points to a local file path, rename the file to match the markdown filename (same `YYYY-MM-DD-pdf-{slug}` stem, `.pdf` extension) and move it to `personal_investing/references/LOGGED/`. Update the `url` frontmatter field and any inline file references in the entry to reflect the new path and name.

6. **Check for matching TODO** — Search `personal_investing/references/TODO/` for an entry with a matching URL or similar title. If found:
   - Copy any useful "Why Review This" notes into the LOGGED entry
   - Delete the TODO file

7. **Update RESEARCH.md** — Read `personal_investing/RESEARCH.md`. Determine today's date and the Monday of the current week.
   - If a `## Week of {monday}` section doesn't exist, create it at the top (below the header).
   - If a `### {today} ({DayName})` subsection doesn't exist, create it under the week section.
   - Prepend a one-line entry under today's heading:
     ```
     - **{source_type}** | [{Title}]({url}) | *{source}* | {#tags} | Impact: {thesis_impact} | Delta: {conviction_delta:+d}
       - {one-line takeaway from summary}
     ```
   - Update the `> Last updated:` line with the current timestamp.

8. **Confirm** — Show the user the created file path, the RESEARCH.md entry, and any auto-applied tags.
