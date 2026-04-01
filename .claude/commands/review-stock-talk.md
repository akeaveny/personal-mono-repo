Review recent stock talk entries against the investing thesis.

First, read `.claude/standards/DailyStockTalk.md` for the DAILY_LOGS.md format.

## Steps

1. **Determine date range** — Default to the last 2 weeks. If the user specifies a range (e.g., "this week", "last month"), use that instead.

2. **Read inputs** — Read both files:
   - `personal_investing/DAILY_LOGS.md` — extract all entries within the date range
   - `personal_investing/THESIS.md` — the current thesis (sector views, watchlist, triggers, principles)
   - `personal_investing/STOCKS.md` — the current stock watchlist

3. **Categorize each entry** against the thesis:

   **Reinforces thesis** — Entry aligns with an existing sector view, watchlist pick, or conviction. Cite the specific thesis claim it supports.

   **Challenges thesis** — Entry contradicts or raises doubt about an existing position or assumption. Cite what it challenges.

   **New signal** — Entry mentions a ticker, sector, or idea not currently in THESIS.md or STOCKS.md. Flag as a potential watchlist addition.

   **Open questions** — Questions that deserve research. Suggest which fetch.py command or research approach could answer them.

4. **Generate the review** — Output in this format:

   ```markdown
   ## Stock Talk Review: YYYY-MM-DD — YYYY-MM-DD

   ### Reinforces Thesis
   - **TICKER** — {who/when}: {what was said}
     → Supports: *{quoted or paraphrased thesis claim}*

   ### Challenges Thesis
   - **TICKER** — {who/when}: {what was said}
     → Challenges: *{quoted or paraphrased thesis claim}*

   ### New Signals
   - **TICKER** — {who/when}: {what was said}
     → Not in watchlist. Consider adding to STOCKS.md under {section}.

   ### Open Questions to Research
   - {question from the logs}
     → Try: `python fetch.py {command}` or research {topic}

   ### Summary
   - {1-2 sentences: what the recent talk suggests about conviction}
   - {any action items: tickers to add to STOCKS.md, thesis claims to revisit}
   ```

5. **Present to user** — Show the full review. Lead with the most actionable insight (e.g., "3 people independently mentioned BTU — coal isn't in your thesis yet").
