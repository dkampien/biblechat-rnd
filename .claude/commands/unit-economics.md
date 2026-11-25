---
description: Pull company unit economics from BigQuery — MRR/ARR, monthly revenue trend, spend/CPT/CPS funnel, matured trial-to-paid, MAU — using validated queries with the Adapty gotchas baked in
argument-hint: [month YYYY-MM, defaults to last full month]
created: 2026-08-17
updated: 2026-08-17
---

# Company Unit Economics from BigQuery

Run the queries below through `mcp__biblechat-analytics__execute_query` (pass the user's ask as `question`). They were validated against the live schema on 2026-08-16. If a query errors or a result looks implausible, `describe_table` the table before changing the SQL: the gotchas live there.

**Target month:** $ARGUMENTS (if empty, use the last full calendar month). Replace the date literals in every query accordingly.

## Rules that make these numbers correct (violating any one gives wrong answers)

1. **Never count `trial_started` events as revenue.** Adapty logs the subscription price when a FREE trial starts; no cash moves. ~94% of trial rows carry this phantom revenue (~$470k/month scale). Payment events are only: `subscription_renewed`, `trial_converted`, `subscription_started`, `non_subscription_purchase`, minus `subscription_refunded` (already negative).
2. **`revenue_usd` = gross customer spend. `proceeds_usd` = after store commission (~74% of gross), the closest field to actual payout.** `net_revenue_usd` and `tax_amount_usd` are unreliable for months before July 2026 (partial backfill): do not use them.
3. Always filter `app_id='biblechat'`, `environment='Production'`, and a tight `event_datetime` window (partition key; the table exceeds the scan cap unfiltered).
4. Quote gross and proceeds as separate numbers, never interchangeably. ARR = MRR x 12 is a snapshot, not a forecast: label it as such.
5. Trials last 7 days: a trial-to-paid rate is only real when the trial cohort's window ends 10+ days before today.

## Query 1 — Point-in-time MRR / ARR (normalized active subscriptions)

Latest state per subscription; active = paid entitlement covers now, refunds excluded; last paid price normalized to monthly. Billing-period regex on product_id is validated against actual entitlement lengths (weekly median 7d, monthly 31d, annual 365d). The lookback must stay 13+ months behind today so annual subs' last payment is in-window: advance the literal over time.

Report the `autorenew_off = false` row as the committed floor and the sum of both rows as total MRR. Grace-period users can linger in "active", which is another reason committed-only is the honest floor.

```sql
WITH events AS (
  SELECT original_transaction_id, event_type, event_datetime, subscription_expires_at,
         product_id, revenue_usd, proceeds_usd
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production'
    AND event_datetime >= TIMESTAMP '2025-07-01 00:00:00'  -- keep 13+ months back
    AND original_transaction_id IS NOT NULL AND original_transaction_id != ''
),
subs AS (
  SELECT original_transaction_id,
    MAX(subscription_expires_at) expires,
    ARRAY_AGG(IF(event_type IN ('subscription_renewed','trial_converted','subscription_started') AND revenue_usd > 0,
                 STRUCT(product_id, revenue_usd, proceeds_usd), NULL) IGNORE NULLS
              ORDER BY event_datetime DESC LIMIT 1)[SAFE_OFFSET(0)] pay,
    ARRAY_AGG(IF(event_type IN ('subscription_renewal_cancelled','trial_renewal_cancelled',
                                'subscription_renewal_reactivated','trial_renewal_reactivated',
                                'subscription_renewed','trial_converted','subscription_started'), event_type, NULL) IGNORE NULLS
              ORDER BY event_datetime DESC LIMIT 1)[SAFE_OFFSET(0)] last_state,
    LOGICAL_OR(event_type='subscription_refunded') refunded
  FROM events
  GROUP BY original_transaction_id
),
active AS (
  SELECT subs.*,
    CASE WHEN REGEXP_CONTAINS(LOWER(pay.product_id),'week') THEN 52/12.0
         WHEN REGEXP_CONTAINS(LOWER(pay.product_id),'month') THEN 1.0
         WHEN REGEXP_CONTAINS(LOWER(pay.product_id),'year|annual') THEN 1/12.0
         ELSE 1.0 END factor,
    last_state IN ('subscription_renewal_cancelled','trial_renewal_cancelled') AS autorenew_off
  FROM subs
  WHERE expires > CURRENT_TIMESTAMP() AND pay IS NOT NULL AND NOT refunded
)
SELECT autorenew_off,
       COUNT(*) subs,
       ROUND(SUM(pay.revenue_usd  * factor),0) mrr_gross,
       ROUND(SUM(pay.proceeds_usd * factor),0) mrr_proceeds,
       ROUND(SUM(pay.revenue_usd  * factor) * 12,0) arr_gross,
       ROUND(SUM(pay.proceeds_usd * factor) * 12,0) arr_proceeds
FROM active
GROUP BY autorenew_off
```

## Query 2 — Monthly recognized revenue trend (13 months)

```sql
SELECT FORMAT_DATE('%Y-%m', DATE(event_datetime)) month,
       ROUND(SUM(revenue_usd),0)  gross_usd,
       ROUND(SUM(proceeds_usd),0) proceeds_usd,
       ROUND(SUM(IF(store='app_store',  revenue_usd, 0)),0) ios_gross,
       ROUND(SUM(IF(store='play_store', revenue_usd, 0)),0) android_gross
FROM `bc-ads-tester.subscription.adapty_realtime`
WHERE app_id='biblechat' AND environment='Production'
  AND event_type IN ('subscription_renewed','trial_converted','subscription_started',
                     'non_subscription_purchase','subscription_refunded','non_subscription_purchase_refunded')
  AND event_datetime >= TIMESTAMP '2025-07-01 00:00:00'  -- 13 months back
GROUP BY month ORDER BY month
```

Mark the current month as month-to-date. Cross-check: the latest full month's gross here should sit within ~5% of Query 1's total `mrr_gross`; a bigger gap means something changed, so investigate before reporting.

## Query 3 — Monthly funnel: spend, trials, new payers, CPT, CPS, payer split

Spend covers Facebook/TikTok/Apple Search/Google. Creator/UGC spend lives separately in `bc-ads-tester.limited.creators_spent_per_day` (`total_spend` column): check it for the month and add it if non-empty.

```sql
WITH spend AS (
  SELECT ROUND(SUM(spend),0) ad_spend
  FROM `bc-ads-tester.subscription.daily_data`
  WHERE app_id='biblechat' AND date >= '2026-07-01' AND date < '2026-08-01'
),
funnel AS (
  SELECT COUNTIF(event_type='trial_started') trials,
         COUNTIF(event_type IN ('trial_converted','subscription_started')) new_payers,
         COUNTIF(event_type='subscription_started') direct_purchases,
         COUNTIF(event_type IN ('trial_converted','subscription_started') AND store='app_store')  payers_ios,
         COUNTIF(event_type IN ('trial_converted','subscription_started') AND store='play_store') payers_android,
         COUNTIF(event_type IN ('trial_converted','subscription_started')
                 AND store NOT IN ('app_store','play_store')) payers_web
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production'
    AND event_type IN ('trial_started','trial_converted','subscription_started')
    AND event_datetime >= TIMESTAMP '2026-07-01 00:00:00'
    AND event_datetime <  TIMESTAMP '2026-08-01 00:00:00'
)
SELECT spend.ad_spend, funnel.*,
       ROUND(spend.ad_spend / funnel.trials, 2)     cpt_blended,
       ROUND(spend.ad_spend / funnel.new_payers, 2) cps_blended
FROM spend, funnel
```

## Query 4 — Matured trial-to-paid rate

Cohort window: 30 days, ending 10+ days before today (7-day trials plus margin).

```sql
WITH cohort AS (
  SELECT original_transaction_id,
         LOGICAL_OR(event_type='trial_started'
                    AND event_datetime >= TIMESTAMP '2026-06-15 00:00:00'
                    AND event_datetime <  TIMESTAMP '2026-07-15 00:00:00') in_cohort,
         LOGICAL_OR(event_type='trial_converted') converted
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production'
    AND event_type IN ('trial_started','trial_converted')
    AND event_datetime >= TIMESTAMP '2026-06-15 00:00:00'
    AND original_transaction_id IS NOT NULL AND original_transaction_id != ''
  GROUP BY original_transaction_id
)
SELECT COUNTIF(in_cohort) trials,
       COUNTIF(in_cohort AND converted) converted,
       ROUND(COUNTIF(in_cohort AND converted) / COUNTIF(in_cohort), 4) trial_to_paid
FROM cohort
```

## Query 5 (optional) — MAU

Device-level (GA pseudo id), so multi-device users count more than once. Scans ~1.2 GB per month queried.

```sql
SELECT COUNT(DISTINCT user_pseudo_id) mau
FROM `genericchatapp-4d046.data_warehouse.ga_events_staging`
WHERE event_name = 'session_start'
  AND shard_date >= '2026-07-01' AND shard_date <= '2026-07-31'
```

## Output format

One compact table: metric, value, window, source table. State gross vs proceeds explicitly on every money number. Scope caveats to carry on every report: `biblechat` app only (the kids app is a separate app_id); web/Stripe revenue is only visible if it flows through Adapty; month-12 ROAS figures elsewhere in the org (`predicted_roas_m12`) are GROSS and run ~1.56x hot vs realized.
