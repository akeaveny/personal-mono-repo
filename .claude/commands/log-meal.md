Log a meal entry from conversational input.

First, read `.claude/standards/MealLogging.md` for the full schema, templates, estimation rules, and append behavior.

The user's input: $ARGUMENTS

## Steps

1. **Parse input** — The user speaks naturally ("had eggs and toast for breakfast", "grabbed a burrito for lunch", "snacked on some chips"). Extract:
   - What they ate (food items, portions if given)
   - Which meal (breakfast/lunch/dinner/snacks — infer from context or time of day if not stated)
   - Whether they ate out or cooked at home (infer if obvious, otherwise don't assume)

   Do NOT interrogate for missing details. Estimate with reasonable assumptions and log it.

2. **Estimate macros** — Estimate calories and protein for each food item using standard nutritional data and common portion sizes. Keep estimates reasonable, not inflated.

3. **Determine date** — Use today's date (YYYY-MM-DD) and day of week. If the user says "yesterday" or a specific day, use that date instead.

4. **Read Logging_Meals.md** — Read `gym/Logging_Meals.md` and check if a `### YYYY-MM-DD` section exists for the target date:
   - **If it exists**: Follow append behavior from the standards. Add new meal rows to the table. Recalculate day totals.
   - **If it doesn't exist**: Determine the Monday of the current week. If `## Week of {monday}` doesn't exist, create it at the top (below the header). Insert a new day entry under the correct week section.

5. **Check for new week** — If this is the first log of a new week, generate a Weekly Patterns section for the previous week (if at least 3 days were logged). Insert it under the previous week's `## Week of` header, before the day entries.

6. **Update last-updated timestamp** — Update the `> Last updated:` line at the top.

7. **Confirm briefly** — Short confirmation (user is on phone). Include: meal logged, estimated cals + protein, running day total if other meals already logged. Example:

   > Logged lunch — chicken wrap + salad (~650 kcal, ~40g protein). Day so far: ~1,100 kcal, ~70g protein.
