Generate a weekly journal review with patterns, spending breakdown, and goals.

First, read `.claude/standards/DailyJournal.md` for the schema, JOURNAL.md format, and weekly review format.

## Steps

1. **Determine date range** — Calculate the current week's Monday through Sunday (or today if mid-week).

2. **Scan entries** — Read `daily_journal/JOURNAL.md`. Find all `### YYYY-MM-DD` day entries that fall within the current week. Parse each day's sections to extract: mood score, energy score, spending rows (item, amount, category), tags, highlight, food entries, personal growth notes, and relationship notes.

3. **Compile statistics**:
   - Days logged (out of 7, or out of days elapsed if mid-week)
   - Average mood score (exclude 0/unrecorded days)
   - Average energy score (exclude 0/unrecorded days)
   - Total spending across all days
   - Spending breakdown by category (sum amounts per category from all spending tables)
   - Tag frequency (count days per tag, sorted descending)

4. **Identify patterns**:
   - Mood/energy correlations with tags (e.g., higher mood on #fitness days)
   - Spending outliers (days significantly above/below average)
   - Recurring themes in personal growth and relationships sections

5. **Check previous goals** — Search `daily_journal/JOURNAL.md` for the most recent `### Weekly Review` section. Extract any goals listed under `#### Goals for Next Week`. Assess progress based on this week's entries.

6. **Generate review** — Format using the Weekly Review template from the standards:
   - Numbers (days logged, avg mood/energy, total spending)
   - Spending Breakdown table (by category with percentages)
   - Patterns & Insights (3-5 bullet points)
   - Progress on Previous Goals (or "First review — no previous goals" if none found)
   - Goals for Next Week (3 actionable goals based on patterns observed)

7. **Insert into JOURNAL.md** — Insert the review at the top of the current week section (after the `## Week of` header, before any day entries). Update the `> Last updated:` timestamp.

8. **Present to user** — Show the full review. Highlight the single most actionable insight (e.g., "You spent 40% more on eating out this week" or "Your mood averaged 2 points higher on days you exercised").
