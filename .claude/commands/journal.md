Log a daily journal entry from conversational input.

First, read `.claude/standards/DailyJournal.md` for the full schema, templates, auto-tagging rules, and append behavior.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — The user speaks naturally. Extract any of the following from `$ARGUMENTS`:
   - Food (meals, snacks)
   - Spending (items, amounts, categories)
   - Mood/energy (explicit scores or infer from tone: "feeling great" → 8, "exhausted" → 3, "pretty good" → 7, "okay" → 5)
   - Personal growth reflections
   - Relationship notes
   - Free-form notes, highlights, gratitude

   Do NOT interrogate the user for missing sections. Log what's given, leave the rest blank or at defaults.

2. **Determine date** — Use today's date (YYYY-MM-DD) and day of week.

3. **Read JOURNAL.md** — Read `daily_journal/JOURNAL.md` and check if a `### YYYY-MM-DD` section already exists for today:
   - **If it exists**: Follow the append behavior from the standards. Merge new data into existing sections. Add new food/spending rows (don't duplicate). Update mood/energy if new values provided. Recalculate spending total from all rows in the table. Update the `###` header line with latest metadata.
   - **If it doesn't exist**: Determine the Monday of the current week. If a `## Week of {monday}` section doesn't exist, create it at the top (below the header and last-updated line). Insert a new day entry under the week section using the template from the standards.

4. **Apply auto-tagging** — Scan all content (food, spending, notes, growth, relationships) against the auto-tagging rules in the standards. Add matching tags to the `###` header. Do not duplicate existing tags. Do not remove manually added tags.

5. **Set highlight** — If the user mentioned something notable, set it as the highlight in the `>` blockquote below the `###` header. If an existing highlight is already set and the new one isn't clearly better, keep the existing one.

6. **Update last-updated timestamp** — Update the `> Last updated:` line at the top of JOURNAL.md with the current timestamp.

7. **Confirm briefly** — Show a short confirmation (user is on phone). Include: date, mood/energy scores if set, spending total if any, auto-applied tags, and any highlight.
