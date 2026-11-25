---
created: 2026-09-07
updated: 2026-09-07
---
# BibleChat metrics dashboard

A published page that charts BibleChat's business metrics month by month and refreshes itself on the 2nd of every month. The page holds no numbers: it reads one document per month from its artifact database and draws inline SVG charts. A scheduled Orca automation runs a fresh Claude session in this workspace, queries BigQuery through the `biblechat-analytics` MCP, and writes the new month into that database.

**Dashboard URL:** https://claude.ai/code/artifact/8f66edad-cc5d-4322-b927-030b2a7275bf
(private to the owner's claude.ai organization; the page declares the `db` capability, which blocks public sharing by design)

**Automation:** Orca automation `9c37ef6a-6a61-4ba7-a15d-18391f1b09c2`, "BibleChat metrics dashboard refresh", cron `0 9 2 * *` in `Europe/Bucharest`, provider `claude`, runs in this worktree with a fresh session each time. Enabled; next run 2026-10-02 09:00 Europe/Bucharest. Missed-run policy: run once within a 12-hour grace window.

## Files

| Path | Role |
|---|---|
| `_projects/metrics-dashboard/dashboard.html` | Page source. Republish it to the same URL with the Artifact tool (`url` = the dashboard URL). Never bake numbers into it. |
| `_projects/metrics-dashboard/README.md` | This file: layout, procedure, limitations, last refresh. |
| `_projects/metrics-dashboard/brief.md` | The original build brief. |
| `.claude/commands/unit-economics.md` | The validated BigQuery queries and the correctness rules the dashboard's numbers rest on. |
| `_docs/core/01_biblechat-business-overview.md` | The ground-truth doc. Its "Monthly outcomes" table and "Scale" line are updated by the same refresh so doc and dashboard never disagree. |

## What the page shows, top to bottom

A freshness line reads `meta/latest` and the months collection: latest complete month, the month-to-date month, snapshot date, MAU, refresh time and source.

1. **Monthly revenue, gross and cash.** Grouped bars per month, gross (blue) and proceeds (light blue). A month flagged `partial` is drawn hatched and labelled month to date.
2. **Ad spend, trials and cost per trial.** Three panels on one month axis (spend, trials, CPT line). No dual axis, by design: two measures on two scales invent correlations. August 2026 reads as a spike in spend and trials while CPT stays flat.
3. **Month-1 return by spend month, gross.** iOS and Android lines from the first month that has data (March 2026, the return tables hold about six rolling months), with a dashed reference at 32%, the month-1 level that projects to the 100% month-12 rule under the model's roughly 3.1x multiplier. Every figure is gross.
4. **Trial-to-paid by platform, matured cohorts.** iOS and Android lines. A month with no point has a cohort that had not matured at refresh.
5. **Subscription base, latest snapshot.** Six tiles: MRR gross, MRR cash, committed floor (gross), active subscriptions, ARR gross, ARR cash, each with its change against the previous snapshot. Every money tile names gross or cash.

Every chart has a Table button (the accessible twin), a hover and keyboard tooltip per month, and a caption naming its window and source table. If `claude.use("db")` resolves null the page shows "Database unreachable"; if the months collection is empty it says so.

## Database layout

Artifact database of the URL above. Write with the Artifact tool (`action: write_db`), read with `read_db`. Access rule: everyone who can open the page reads; only the owner writes.

### Collection `months`, doc id `YYYY-MM`

| Field | Meaning | Source |
|---|---|---|
| `revenue_gross`, `revenue_proceeds` | Recognized revenue that calendar month; gross customer spend and proceeds after store commission. Payment events only, refunds netted. | `bc-ads-tester.subscription.adapty_realtime` |
| `revenue_ios_gross`, `revenue_android_gross` | Gross split by store (`app_store`, `play_store`). | same |
| `ad_spend`, `spend_facebook`, `spend_tiktok`, `spend_apple`, `spend_google` | Ad spend that month; `ad_spend` is the table's `spend` column (sum of channels). | `bc-ads-tester.subscription.daily_data` |
| `spend_creators` | Creator video production spend, optional, informational only. Not part of `ad_spend`. | `bc-ads-tester.limited.creators_spent_per_day` |
| `trials`, `new_payers`, `direct_purchases`, `payers_ios`, `payers_android` | Funnel counts by event month. `new_payers` = trial_converted + subscription_started; `direct_purchases` = subscription_started. | `adapty_realtime` |
| `cpt_blended`, `cps_blended` | `ad_spend / trials`, `ad_spend / new_payers`, rounded to cents. | derived |
| `m1_ios_gross`, `m1_android_gross` | Month-1 return on that month's spend, gross, spend-weighted by day. | `limited.cpt_master_daily` (iOS), `limited.cpt_master_daily_regions_android` with `row_type='overall'` (Android) |
| `m12_projected_ios`, `m12_projected_android` | The model's month-12 projection for the same spend, gross, spend-weighted. | same |
| `trial_to_paid_ios`, `trial_to_paid_android` | Matured cohort: trials started from the 15th of the prior month through the 14th of this month, converted at any later time. Null until the window has ended 10+ days before the refresh. | `adapty_realtime` |
| `mau` | Device-level monthly active users (`session_start`, distinct `user_pseudo_id`). About 1.2 GB per month queried; required for the latest month, optional for history. | `genericchatapp-4d046.data_warehouse.ga_events_staging` |
| `partial` | `true` only on a month that is not complete. Omit on complete months. | |
| `through` | Last day covered, only on a partial month (`YYYY-MM-DD`). | |
| `queried_at` | Date the numbers were pulled (`YYYY-MM-DD`). | |

Missing values are written as `null` (JSON null), never 0. History starts 2025-07; `daily_data` begins 2025-08, so 2025-07 has null spend and null CPT/CPS.

### Collection `snapshots`, doc id `YYYY-MM-DD`

`active_subs`, `active_subs_committed`, `mrr_gross`, `mrr_proceeds`, `mrr_gross_committed`, `mrr_proceeds_committed`, `arr_gross`, `arr_proceeds`, `source`. From unit-economics Query 1: total = both rows summed, committed = the `autorenew_off = false` row. ARR = MRR x 12.

### Doc `meta/latest`

`{ month, partial_month, snapshot, refreshed_at, source, history_from }`. `month` is the latest complete month written; `partial_month` the month-to-date month if one was written; `snapshot` the latest snapshot id; `refreshed_at` ISO timestamp; `source` is `"biblechat-analytics MCP"`. The page subscribes to this doc and re-reads everything when it changes.

## Monthly refresh procedure

For a fresh agent with zero history. The automation prompt points here. Everything runs through `mcp__biblechat-analytics__execute_query` (load it with ToolSearch first; pass the intent as `question`). BigQuery is read-only and per-person quota-limited: keep the partition filters below, do not widen windows.

Let `M` be the previous calendar month (`YYYY-MM`), `M_START` its first day, `M_END` the first day of the following month, `PREV15` the 15th of the month before `M`, `M15` the 15th of `M`, and `TODAY` today's date.

**Step 0, reachability.** Run a cheap catalog query, for example the spend query below. A table-less probe such as `SELECT 1` is rejected by design (the server fails closed when no catalog table is referenced), so it proves nothing. If the MCP is not connected, stop, write the failure under "Last refresh" and in the worktree comment, and ask Denis to run `/mcp` and authenticate it.

**Step 1, revenue** (about 0.1 GB per month):

```sql
SELECT ROUND(SUM(revenue_usd),0)  revenue_gross,
       ROUND(SUM(proceeds_usd),0) revenue_proceeds,
       ROUND(SUM(IF(store='app_store',  revenue_usd, 0)),0) revenue_ios_gross,
       ROUND(SUM(IF(store='play_store', revenue_usd, 0)),0) revenue_android_gross
FROM `bc-ads-tester.subscription.adapty_realtime`
WHERE app_id='biblechat' AND environment='Production'
  AND event_type IN ('subscription_renewed','trial_converted','subscription_started',
                     'non_subscription_purchase','subscription_refunded','non_subscription_purchase_refunded')
  AND event_datetime >= TIMESTAMP 'M_START 00:00:00' AND event_datetime < TIMESTAMP 'M_END 00:00:00'
```

**Step 2, spend** (tiny table):

```sql
SELECT ROUND(SUM(spend),0) ad_spend, ROUND(SUM(facebook_spend),0) spend_facebook,
       ROUND(SUM(tiktok_spend),0) spend_tiktok, ROUND(SUM(apple_spend),0) spend_apple,
       ROUND(SUM(google_spend),0) spend_google
FROM `bc-ads-tester.subscription.daily_data`
WHERE app_id='biblechat' AND date >= 'M_START' AND date < 'M_END'
```

Optional: `SELECT ROUND(SUM(total_spend),0) FROM bc-ads-tester.limited.creators_spent_per_day WHERE app_id='biblechat' AND date >= 'M_START' AND date < 'M_END'` for `spend_creators` (the column is NUMERIC and may come back as a decimal object; read its digits). Keep it out of `ad_spend`.

**Step 3, funnel:**

```sql
SELECT COUNTIF(event_type='trial_started') trials,
       COUNTIF(event_type IN ('trial_converted','subscription_started')) new_payers,
       COUNTIF(event_type='subscription_started') direct_purchases,
       COUNTIF(event_type IN ('trial_converted','subscription_started') AND store='app_store')  payers_ios,
       COUNTIF(event_type IN ('trial_converted','subscription_started') AND store='play_store') payers_android
FROM `bc-ads-tester.subscription.adapty_realtime`
WHERE app_id='biblechat' AND environment='Production'
  AND event_type IN ('trial_started','trial_converted','subscription_started')
  AND event_datetime >= TIMESTAMP 'M_START 00:00:00' AND event_datetime < TIMESTAMP 'M_END 00:00:00'
```

`cpt_blended = ROUND(ad_spend / trials, 2)`, `cps_blended = ROUND(ad_spend / new_payers, 2)`.

**Step 4, trial-to-paid, matured cohort** (window PREV15 to M15; on the 2nd of the month the window ended 17+ days earlier, so it is matured):

```sql
WITH trials AS (
  SELECT original_transaction_id,
         ANY_VALUE(IF(event_type='trial_started', store, NULL)) store,
         LOGICAL_OR(event_type='trial_started'
                    AND event_datetime >= TIMESTAMP 'PREV15 00:00:00'
                    AND event_datetime <  TIMESTAMP 'M15 00:00:00') in_cohort,
         LOGICAL_OR(event_type='trial_converted') converted
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production'
    AND event_type IN ('trial_started','trial_converted')
    AND event_datetime >= TIMESTAMP 'PREV15 00:00:00'
    AND original_transaction_id IS NOT NULL AND original_transaction_id != ''
  GROUP BY original_transaction_id
)
SELECT ROUND(SAFE_DIVIDE(COUNTIF(in_cohort AND store='app_store'  AND converted), COUNTIF(in_cohort AND store='app_store')),4)  trial_to_paid_ios,
       ROUND(SAFE_DIVIDE(COUNTIF(in_cohort AND store='play_store' AND converted), COUNTIF(in_cohort AND store='play_store')),4) trial_to_paid_android
FROM trials
```

**Step 5, month-1 return and month-12 projection** (both tables are tiny; run once per platform):

```sql
-- iOS
SELECT ROUND(SUM(total_spend*predicted_roas_m1)/NULLIF(SUM(total_spend),0),4)  m1_ios_gross,
       ROUND(SUM(total_spend*predicted_roas_m12)/NULLIF(SUM(total_spend),0),4) m12_projected_ios
FROM `bc-ads-tester.limited.cpt_master_daily`
WHERE date >= 'M_START' AND date < 'M_END'
-- Android
SELECT ROUND(SUM(total_spend*predicted_roas_m1)/NULLIF(SUM(total_spend),0),4)  m1_android_gross,
       ROUND(SUM(total_spend*predicted_roas_m12)/NULLIF(SUM(total_spend),0),4) m12_projected_android
FROM `bc-ads-tester.limited.cpt_master_daily_regions_android`
WHERE row_type='overall' AND date >= 'M_START' AND date < 'M_END'
```

`predicted_roas_m1` equals `realized_roas_30d` once a day is 30+ days old; on the 2nd of the month the last days of `M` are still younger than that, so the month's value is part model estimate. That is accepted and matches how the overview doc quotes it. Both columns are gross.

**Step 6, MAU** (about 1.2 GB):

```sql
SELECT COUNT(DISTINCT user_pseudo_id) mau
FROM `genericchatapp-4d046.data_warehouse.ga_events_staging`
WHERE event_name = 'session_start' AND shard_date >= 'M_START' AND shard_date < 'M_END'
```

**Step 7, snapshot.** Run unit-economics Query 1 unchanged (its lookback literal must stay 13+ months behind today; advance it when needed). Total = both rows summed; committed = the `autorenew_off = false` row.

**Step 8, write.** With the Artifact tool: `action: read` on the dashboard URL first (harmless, and it registers the artifact with the session), then `action: write_db`, `db_op: batch`, `url` = the dashboard URL, with three `set` writes:

- `months` / `M`: all fields from the table above, `queried_at: TODAY`, no `partial`, no `through`.
- `snapshots` / `TODAY`: the eight snapshot fields plus `source: "unit-economics Query 1, run TODAY"`.
- `meta` / `latest`: `{ month: M, partial_month: null, snapshot: TODAY, refreshed_at: <ISO now>, source: "biblechat-analytics MCP", history_from: "2025-07" }`.

Optionally also write the current month as a partial doc (`partial: true`, `through: <yesterday>`, and set `partial_month` in meta); this doubles the revenue and funnel scans, so only do it when quota is not a concern.

**Step 9, doc sync.** In `_docs/core/01_biblechat-business-overview.md`, move the "Monthly outcomes" table to the two latest complete months (spend with channel shares, trials, CPT, subscribers, CPS, trial-to-paid, month-1 measured, month-12 projected) and rewrite the "Scale" line (MAU, subs, MRR gross and net, ARR gross and net) from the snapshot. Bump the `updated` date in its frontmatter. Do not touch other sections.

**Step 10, record.** Update "Last refresh" below and the Orca worktree comment. If any number differs from the overview doc by more than 10% before you update it, list both under "Discrepancies" and keep going.

## Refreshing by hand

Open a Claude Code session in this worktree (any Orca terminal here) and paste the automation's prompt: `orca automations show 9c37ef6a-6a61-4ba7-a15d-18391f1b09c2 --json` prints it. Or trigger the automation itself: `orca automations run 9c37ef6a-6a61-4ba7-a15d-18391f1b09c2 --json`, then follow with `orca automations runs --id 9c37ef6a-6a61-4ba7-a15d-18391f1b09c2 --json` and `orca terminal list --worktree active --json` to find its terminal. To backfill or correct a month, run the same queries with that month's window and `write_db` the doc; to change the page, edit `dashboard.html` and republish to the same URL.

Enable or pause: `orca automations edit <id> --enabled --json` / `--disabled --json`.

## Known limitations

- **The automation needs the analytics MCP in the automation's session.** The MCP is configured for this workspace and a scheduled-style run (fresh Claude session launched by the automation, bypass permissions on) reaches it; see "Last refresh". If a run cannot reach it, the run stops and writes that fact here; the fallback is the manual procedure above.
- **The automation writes to the database through the Artifact tool, which acts as the signed-in claude.ai user.** If that session is signed out, `write_db` fails; sign in and rerun.
- **Month-1 return history starts March 2026.** `cpt_master_daily` keeps about six rolling months; earlier months cannot be reconstructed from it.
- **Spend history starts August 2025**, where `daily_data` begins. July 2025 shows revenue and funnel only. Early months' CPT (about $8 to $11) is much lower than 2026's and may reflect incomplete channel coverage in the table then; treat pre-2026 CPT as indicative.
- **Trial-to-paid for the current month is always null** until its cohort window closes; the chart leaves that point out.
- **MAU is device-level** (GA pseudo id) and only stored for months where it was queried (July 2026 onward).
- **Scope:** `app_id='biblechat'` only; web and Stripe revenue only where it flows through Adapty; `revenue_usd` is gross and `proceeds_usd` cash; `net_revenue_usd` is not used anywhere.
- **The page cannot be shared publicly** because it declares the `db` capability; viewers must be signed-in members of the owner's organization.

## Discrepancies

Recorded when a query result differs from the ground-truth doc by more than 10%. Both numbers are kept; the dashboard shows the query result.

| Date | Metric | Overview doc | Query result | Note |
|---|---|---|---|---|
| 2026-09-07 | Android month-1 return, Aug 2026 | 40% | 31.3% | Spend-weighted `predicted_roas_m1` from `cpt_master_daily_regions_android`, `row_type='overall'`, Aug 1 to 31. July 2026 agrees (39.8% vs the doc's 40%), so the August 40% in the doc looks like a carry-over. Seen in the build session and again in the refresh run the same day; the refresh run rewrote the doc's cell to 31%. |

All other numbers agreed within tolerance on 2026-09-07: Aug 2026 revenue $2.34M gross, spend $2.08M, trials 124k, CPT $16.74, CPS $40.05, trial-to-paid 47.9% iOS / 27.1% Android (blended 42.2%), iOS M1 28.2%, M12 projected 96% iOS / 84% Android, MAU 4.21M, and the 2026-09-07 snapshot (198,711 subs, MRR $2.55M gross / $1.91M cash, committed $2.30M gross, ARR $30.6M gross / $22.9M cash).

## Last refresh

- **2026-09-07, build session.** Seeded `months` 2025-07 through 2026-09 (2026-09 partial through 2026-09-06), `snapshots` 2026-08-16 (seeded by hand from the 16 Aug read) and 2026-09-07 (Query 1), and `meta/latest`. Automation created disabled.
- **2026-09-07, refresh run (automation prompt, fresh session).** MCP reachable (spend probe, 0.0003 GB). Wrote `months/2026-08` (full replace, complete month, `queried_at` 2026-09-07), `snapshots/2026-09-07` (198,712 subs, 151,645 committed; MRR $2,551,854 gross / $1,907,612 cash; ARR $30,622,243 gross / $22,891,337 cash) and `meta/latest` (month 2026-08, no partial month, snapshot 2026-09-07, refreshed_at 2026-09-07T10:34:55Z). August 2026: revenue $2,341,509 gross / $1,750,600 cash; spend $2,075,844 (creators spend null); trials 124,016; new payers 51,825; CPT $16.74; CPS $40.05; trial-to-paid 47.9% iOS / 27.1% Android; M1 28.2% iOS / 31.3% Android gross; M12 projected 96% iOS / 84% Android; MAU 4,209,489. One discrepancy over 10% against the overview doc before the sync (Android M1 Aug, see Discrepancies); the doc's Monthly outcomes table and Scale line were rewritten from the database and the snapshot. Total scan about 0.11 GB plus the MAU and snapshot queries. `dashboard.html` untouched; the 2026-09 partial doc from the build session was left as is.
