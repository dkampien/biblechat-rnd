---
description: Data analysis cycle — drafts question specification, loads schema, drafts query, validates, interprets with bias check, assigns confidence, confirms with human before logging
argument-hint: <analytical question in plain language>
allowed-tools: Bash, Read, Edit, Glob, Grep
---

# Data Analysis Cycle

You are running one cycle of the data analysis workflow. Follow each step in order. Do not skip steps. Print each step's output visibly so the human can verify.

**User input:** $ARGUMENTS

**Analytical plan:** See `_projects/biblechat-ltv/_docs/1_development-docs/plan/bc-analysis-plan-v4.md` for the active plan. If no specific question is provided, check the current state section for what's next and ask the human which to tackle. The plan is not a backlog — next question is decided after the current one is answered.

---

## Step 1: Define Question

State the analytical question clearly. Then:

**If exploratory** (e.g., "what's in the data?"):
- State the purpose: what are we trying to learn?
- State what we'll do with the answer

**If analytical** (e.g., "does X correlate with Y?"):
- State the expected outcome based on docs, benchmarks, or prior findings
- State what we'd do if the answer is high vs low vs unexpected
- Ask the human to sanity-check the expectation

**Question specification — 4 slots.** The agent drafts each slot, the human reviews.

1. **Population** — which users? (cohort definition + platform + country)
2. **Time window** — when? (date range + cohort maturity check)
3. **Definition** — what counts? (e.g., "active" = app open? core action? completion?)
4. **Metric** — how to measure? (count of users, rate, total events, average, distribution)

**How to fill the slots:**
- Propose a default for each slot based on project conventions (see workflow doc operational definitions) and prior findings in the analysis plan
- **Flag any slot that requires a business/product judgment call** — do NOT guess these, ask the human directly. Examples: which segment matters, which metric matches the business question, what threshold counts as "engaged."
- Default platform = iOS unless the question clearly needs Android

**Why this matters:** Same question words with different slots produce different answers. "How many active subscribers?" can mean 123K (billing-active) or ~57K (actually opens the app). Both are correct for their specification. Don't run until all 4 slots are explicit.

Print the draft specification for human review.

**STOP. Wait for human confirmation before proceeding.**

---

## Step 2: Load Schema

For each table that will be queried, run:
```bash
bq show --schema --format=json [project:]dataset.table_name
```

Print the relevant columns, their types, and the partition column. Reference `_projects/biblechat-ltv/_docs/2_reference-docs/data-surface/bc-full-data-architecture.md` Section 13 (Table Purpose Index) for the full table inventory — do not go from memory.

**Two projects available:**
- `genericchatapp-4d046.sandbox_analytics` — behavioral data (19 tables)
- `bc-ads-tester.subscription` — Adapty subscription/revenue data

---

## Step 3: Draft Query

Write the SQL. Before presenting it, self-check:

- [ ] Partition filter in WHERE clause?
- [ ] Only needed columns (no `SELECT *`)?
- [ ] CTE referenced multiple times? → materialize instead
- [ ] Working on a sample for exploratory work?
- [ ] Cohort excludes immature cohorts?
- [ ] Using `user_id` (stable) or `user_pseudo_id` (device-bound)?
- [ ] Column types match what schema showed in Step 2?
- [ ] All relevant tables included (checked reference doc)?
- [ ] When comparing across tables: same platform filter, same date range, same null handling?
- [ ] Filtering by categorical values (event names, status, type)? Verified actual values exist, not guessed?

Print the query and the checklist results.

---

## Step 4: Cost Check

```bash
bq query --dry_run --use_legacy_sql=false "QUERY"
```

Print: bytes to be scanned, estimated cost (bytes ÷ 1TB × $6.25), cumulative session spend.

**Auto-block** if single query > $1. Ask human for confirmation before executing.

---

## Step 5: Execute

```bash
bq query --use_legacy_sql=false --maximum_bytes_billed=LIMIT "QUERY"
```

Log the result. Update cumulative session spend.

---

## Step 6: Validate

Before interpreting, check:

- Row counts — expected range?
- Null rates on key columns?
- Values make sense? (retention can't be >100%, counts can't be negative)
- What does this number represent? (events, unique users, sessions?)
- Any anomalous cohorts? (sudden jumps = bot traffic or tracking change?)
- **Cross-check against existing findings:** Does this number count a population that a previous finding already counted? If so, do they reconcile?
- **(Optional) Cross-check against CTO's data warehouse:** Search `_archive/bq_export/` for existing queries on the same metric. Compare definitions if found.
- **Assign a confidence label** to the finding:
  - **Verified** — cross-checked multiple ways, known current, known source
  - **Plausible** — exists in the source but not independently verified (might be legacy)
  - **Stale** — known deprecated or historical
  Print the label with a one-line reason. It gets logged with the finding in Step 8.

Print validation results.

---

## Step 6.5: Verify Math with Python

Any time you compute derived numbers from raw query output (percentages, ratios, weighted averages, deltas), verify with Python before presenting. Raw counts straight from BigQuery don't need this — anything you calculate from those counts does.

```python
# Example: verify percentages from count data
python3 -c "
total = a + b + c
print(f'a: {a/total*100:.1f}%')
...
"
```

If Python produces different numbers than what you computed, use Python's numbers and flag the correction.

---

## Step 7: Interpret

Follow the layers strictly. Print each one separately.

**Observation** (what the data shows — numbers only, no narrative):
> _state the raw finding_

**Bias check** (which of these could apply?):
> Survivorship bias? Selection bias? Regression to the mean? Seasonal effect? Average masking distribution? Correlation ≠ causation?
> **"What's the most important thing this data DOESN'T tell us?"**

**Gap** (explicit, not hedged):
> _state what the data doesn't tell us as a concrete sentence, not a qualifier sprinkled into the observation_

**Draft interpretation — collaborative, not pre-drafted.**

Do NOT present a polished interpretation as if it were a finding. Insights should be built with the human, not written in advance and handed over for acceptance. The act of thinking together is the point — AI-drafted insights look like findings to a reader but carry no verification.

If you have a proposed interpretation, label it explicitly as "DRAFT — for discussion, not validated" and invite conversation. If no interpretation is obvious from the data alone, skip this layer and ask the human what they make of the observation.

**Hypothesis** (what would confirm or deny a proposed interpretation):
> _state how to test it_

**Never skip from observation to recommendation.**

---

## Step 7.5: Confirm

**STOP. Present to the human before writing anything:**

1. **The finding** — one sentence summary
2. **The key numbers** — list each number and the exact calculation or query that produced it
3. **Source label** — table(s) + scope + time window + population filter (e.g., `adapty_realtime, iOS weekly trial converters, last 83 days`)
4. **Confidence label** — Verified / Plausible / Stale with a one-line reason
5. **How I'd log it** — what goes in the analytical plan
6. **How I'd visualize it** — if the finding has a visual story, what chart type fits the data shape (or "no visualization needed")

**Writing style: don't hedge.** State findings directly. Avoid qualifiers like "this might suggest," "it could possibly indicate," "perhaps users are." Hedging dilutes strong findings by making them sound as uncertain as weak ones. If something is uncertain, mark it "Plausible" or state the gap explicitly — don't sprinkle qualifiers on every sentence.

**Wait for human confirmation before proceeding to Step 8.** If the human questions a number, show the source query and re-verify before logging.

---

## Step 8: Log & Visualize

Update the query log in the active analysis plan:
- Query number, date, question, population/filters used, bytes scanned, cost, key finding

**If the finding has a visual story, propose the right visualization.** Chart type depends on data shape — don't force findings into a predetermined dashboard. Present the visualization proposal to the human for confirmation before building.

Then ask: **What question does this answer suggest next?**
