Generate a weekly reading digest from logged entries.

First, read `.claude/standards/Reading.md` for the schema and READING.md format.

## Steps

1. **Determine date range** — Calculate the current week's Monday through Sunday (or today if mid-week).

2. **Scan LOGGED entries** — Read all files in `reading/LOGGED/` whose filenames start with dates in the current week (`YYYY-MM-DD-*`). Parse each file's YAML frontmatter to extract: title (from `# heading`), source_type, source, url, tags, rating, summary.

3. **Compile statistics**:
   - Total items logged this week
   - Breakdown by source_type (e.g., 3 articles, 2 podcasts, 1 youtube)
   - Top-rated items (rating >= 4)
   - Tag frequency (count items per tag, sorted descending)

4. **Generate digest** — Format a digest section:

   ```markdown
   ## Weekly Digest: {Monday YYYY-MM-DD} — {Sunday YYYY-MM-DD}

   **{N} items logged** | {breakdown by type}

   ### Top Rated

   - **{rating}/5** | [{Title}]({url}) | *{source}* | {#tags}
     - {summary}

   ### By Tag

   - **#ai** (3): [Title1](url1), [Title2](url2), [Title3](url3)
   - **#finance** (2): [Title4](url4), [Title5](url5)

   ---
   ```

5. **Update READING.md** — Read `reading/READING.md`. Insert the digest section at the top, below the `# Reading Log` header and `> Last updated:` line but above any `## Week of` sections. Update the `> Last updated:` timestamp.

6. **Handle empty week** — If no entries found for the current week, inform the user and do not modify READING.md.

7. **Confirm** — Show the user a summary of the digest: total items, top-rated entries, and most common tags.
