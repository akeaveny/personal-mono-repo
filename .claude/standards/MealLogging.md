---
globs: gym/Logging_Meals.md
---

# Meal Logging Module Standards

Schema, templates, append behavior, and format for the meal log.

## Overview

A conversational meal tracker focused on building awareness of eating habits — not hitting strict calorie goals. The user texts what they ate in natural language, and Claude estimates macros and logs it. Weekly summaries surface patterns (skipped meals, protein gaps, heavy snacking, eating out vs cooking, etc.).

## User Profile

- 6'1", 197 lbs
- 4-day hypertrophy split + road cycling (see `gym/Training_Plan.md`)
- Protein reference range: ~140–197g/day (0.7–1g per lb bodyweight)
- No strict calorie target — tracking for awareness

## File

```
gym/Logging_Meals.md    # Single rolling file, newest week first
```

## File Structure

```markdown
# Meal Log

> 6'1" · 197 lb · Protein ref: 140–197g/day
> Last updated: YYYY-MM-DD HH:MM ET

## Week of YYYY-MM-DD

### Weekly Patterns
- **Avg daily calories**: ~X,XXX kcal
- **Avg daily protein**: ~Xg
- **Days logged**: X/7
- **Meals skipped**: X (list which)
- **Eating out vs home**: X out, X home
- **Notes**: {pattern observations — e.g., low protein on rest days, heavy snacking late night}

### YYYY-MM-DD (DayName)

| Meal | What | ~kcal | ~Protein |
|---|---|---|---|
| Breakfast | 3 eggs, toast, coffee | 450 | 30g |
| Lunch | Chicken wrap, side salad | 650 | 40g |
| Dinner | Salmon, rice, broccoli | 750 | 45g |
| Snacks | Protein bar, apple | 300 | 22g |

**Day total**: ~2,150 kcal · ~137g protein
```

## Calorie & Macro Estimation

All estimates are approximate. Use `~` prefix only on day totals and weekly averages, not on individual meal rows. Estimate using common portion sizes and standard nutritional data.

When the user says something vague like "had a sandwich", make a reasonable assumption (e.g., deli turkey sandwich ~400 kcal, 25g protein) and log it. Don't interrogate for exact ingredients — the goal is habit awareness, not precision.

If the user gives specifics ("6oz chicken breast, cup of rice"), use those for a tighter estimate.

## Meal Categories

Use these standard meal slots. If the user doesn't specify which meal, infer from time of day or ask briefly.

- **Breakfast**
- **Lunch**
- **Dinner**
- **Snacks** (combine all snacks into one row, or split if they're distinct)

If a meal doesn't fit (e.g., "late night food"), use a descriptive label like "Late night" instead of forcing it into a category.

## Append Behavior

When the user logs multiple times in one day:

1. Find the existing `### YYYY-MM-DD` section
2. Add new meal rows to the table (don't duplicate existing rows)
3. If the user is updating a previously logged meal ("actually I had chicken not beef for lunch"), replace that row
4. Recalculate day totals from all rows
5. Do not overwrite or remove existing entries unless the user explicitly corrects them

## Weekly Patterns Section

Generated or updated whenever:
- The user asks for a summary
- A new week starts (auto-generate for the prior week when the first entry of a new week is logged)

Focus on **observations, not judgments**:
- Protein consistency (hitting reference range or not?)
- Meal skipping patterns (always skipping breakfast?)
- Cooking vs eating out ratio
- Late-night eating frequency
- Calorie variation across the week (big swings?)
- Training day vs rest day eating differences

## Week Boundaries

Weeks start on Monday. Use the Monday date for `## Week of YYYY-MM-DD`. When the first log of a new week comes in, auto-generate the Weekly Patterns section for the previous week (if enough data exists — at least 3 days logged).

## Tone

Keep confirmations brief — the user will often be texting from their phone. Example:

> Logged lunch — chicken wrap + salad (~650 kcal, ~40g protein). Day so far: ~1,100 kcal, ~70g protein.
