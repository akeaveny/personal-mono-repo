Log a daily stock talk entry from conversational input.

First, read `.claude/standards/DailyStockTalk.md` for the full schema, format, and append behavior.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — The user speaks naturally. Extract:
   - Ticker mentions (e.g., "SPY", "CVX", "$BTU")
   - Who said it / source (e.g., "Cone thinks...", "heard at work...")
   - The claim, opinion, question, or observation
   - Any open questions not tied to a specific ticker

   Do NOT interrogate the user for missing details. Log what's given.

2. **Determine date** — Use today's date (YYYY-MM-DD) and day of week.

3. **Read DAILY_LOGS.md** — Read `personal_investing/DAILY_LOGS.md` and check if a `### YYYY-MM-DD` section already exists for today:
   - **If it exists**: Follow the append behavior from the standards. Add new bullets below existing ones. Do not duplicate entries with the same ticker + core idea.
   - **If it doesn't exist**: Determine the Monday of the current week. If a `## Week of {monday}` section doesn't exist, create it at the top (below the header and last-updated line). Insert a new day entry under the week section.

4. **Format entries** — Each entry should follow the format:
   - `- **TICKER** — {attribution}: {what was said}`
   - `- **TICKER** — {observation or idea}` (if no external source)
   - `- Open question: {broader question}` (if not ticker-specific)
   - Use sub-bullets for follow-up thoughts or related questions

5. **Update last-updated timestamp** — Update the `> Last updated:` line at the top of DAILY_LOGS.md.

6. **Confirm briefly** — Show a short confirmation. Include: date, tickers mentioned, and number of entries added.
