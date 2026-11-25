## Check 1 — BigQuery: RUN, 2026-09-15

The `biblechat-analytics` MCP is now authorized. Seven read-only queries, all
partition-filtered and column-pruned; total scanned **~0.31 GB** against the
~1.5 TB/day per-person quota. Nothing was written to any catalog or report tool.

### 1a. Can the ad set be matched in the ledger? No.

`adapty_realtime.attributions` is the only attribution column in the billing
table, and it carries **Apple Search Ads only**:

```sql
SELECT attributions, COUNT(*) AS n
FROM `bc-ads-tester.subscription.adapty_realtime`
WHERE app_id='biblechat' AND environment='Production' AND store='app_store'
  AND event_type='trial_started'
  AND event_datetime >= TIMESTAMP '2026-09-08 00:00:00'
  AND event_datetime <  TIMESTAMP '2026-09-09 00:00:00'
GROUP BY attributions ORDER BY n DESC LIMIT 15
```

Of the top 15 values on a single day: one is `{}` (51 rows, the modal value),
the other fourteen are `{"apple_search_ads": {...}}` — thirteen with
`"status":"organic"` and all keys null, one `non_organic` carrying an ASA
`campaign` / `ad_group` / `creative`. **There is no Meta campaign, ad set or ad
id anywhere in the billing table.** No other cataloged table bridges Adapty to
Meta ad ids either. So **the matched-pool count asked for in (2b) cannot be
produced from BigQuery at all** — not for this ad set, not for any Meta ad set.
Per-route is the finest grain the ledger supports. This closes open question 2
below: the answer is no.

### 1b. Whole route — iOS, event date 2026-09-08 … 2026-09-14

```sql
WITH ev AS (
  SELECT event_type, event_datetime, original_transaction_id, store_country
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production' AND store='app_store'
    AND event_type IN ('trial_started','subscription_started','trial_converted')
    AND event_datetime >= TIMESTAMP '2026-08-09 00:00:00'
    AND event_datetime <  TIMESTAMP '2026-09-15 00:00:00'
),
trial_ids AS (
  SELECT DISTINCT original_transaction_id
  FROM ev WHERE event_type='trial_started' AND original_transaction_id IS NOT NULL
)
SELECT
  IF(e.store_country='US','US','ROW') AS geo,
  COUNTIF(e.event_type='trial_started') AS trial_starts,
  COUNTIF(e.event_type='subscription_started') AS subscription_started_all,
  COUNTIF(e.event_type='subscription_started' AND t.original_transaction_id IS NULL) AS direct_purchases_no_trial,
  COUNTIF(e.event_type='trial_converted') AS trial_converted_in_week
FROM ev e
LEFT JOIN trial_ids t ON t.original_transaction_id = e.original_transaction_id
WHERE e.event_datetime >= TIMESTAMP '2026-09-08 00:00:00'
  AND e.event_datetime <  TIMESTAMP '2026-09-15 00:00:00'
GROUP BY geo ORDER BY geo
```

The 30-day lookback exists only to decide whether a `subscription_started` has
a prior trial (the guide's payer rule). Result:

| iOS, 09-08…09-14 | trial starts | direct purchases | **first transactions** | trial→paid landing in the week |
|---|---|---|---|---|
| US | 6,944 | 376 | **7,320** | 5,002 |
| Rest of world | 4,183 | 122 | **4,305** | 2,679 |
| **iOS total** | **11,127** | **498** | **11,625** | **7,681** |

Every `subscription_started` in the window had no prior trial, so direct
purchases = 498 either way. Direct buys are **4.3%** of first transactions —
the company's documented ~96/4 trial/direct split, confirmed at route level.
This is the answer to open question 1, for the route (not for the ad set).

De-duplication check — the counts are one row per subscription, not repeats:

```sql
SELECT event_type, COUNT(*) AS events,
       COUNT(DISTINCT original_transaction_id) AS distinct_subs,
       COUNT(DISTINCT customer_user_id) AS distinct_users
FROM `bc-ads-tester.subscription.adapty_realtime`
WHERE app_id='biblechat' AND environment='Production' AND store='app_store'
  AND event_type IN ('trial_started','subscription_started','trial_converted')
  AND event_datetime >= TIMESTAMP '2026-09-08 00:00:00'
  AND event_datetime <  TIMESTAMP '2026-09-15 00:00:00'
GROUP BY event_type ORDER BY events DESC
```

trial_started 11,127 events / 11,126 subs / 11,126 users; trial_converted 7,681
/ 7,681 / 7,681; subscription_started 498 / 498 / 498. Clean 1:1.

### 1c. The app's own `purchase_completed`, counted in BigQuery

`data_warehouse.paywall_events` carries the **same client event Meta receives**:

```sql
SELECT event_name,
       IF(country='United States','US','ROW') AS geo,
       trial, COUNT(*) AS events, COUNT(DISTINCT user_pseudo_id) AS users
FROM `genericchatapp-4d046.data_warehouse.paywall_events`
WHERE event_date BETWEEN DATE '2026-09-08' AND DATE '2026-09-14'
  AND platform = 'IOS'
  AND event_name IN ('paywall_shown','purchase_started','purchase_completed')
GROUP BY event_name, geo, trial ORDER BY event_name, geo, trial
```

| iOS, 09-08…09-14 | paywall_shown (users) | purchase_started (users) | **purchase_completed (users)** | purchase_completed (events) |
|---|---|---|---|---|
| US | 33,098 | 16,050 | **6,918** | 6,989 |
| Rest of world | 50,119 | 24,553 | **4,091** | 4,118 |
| **iOS total** | **83,217** | **40,603** | **11,009** | **11,107** |

**11,107 `purchase_completed` events vs 11,625 Adapty first transactions in the
same week — 95.5%.** Against trial→paid conversions (7,681) it is **145%**: a
funnel stage cannot outnumber the stage above it, so `purchase_completed`
is not the paid conversion. It sits on the first transaction, one-for-one.

The `trial` flag in this table splits purchase_completed 10,131 trial / 946
no-trial (8.5%) — but that flag reads the SKU name, and the table's own gotcha
warns SKU names lie (`biblechat.pro.weekly.notrial` *has* a trial). Adapty's
event types are the truth: **4.3% direct**, not 8.5%.

### 1d. The curated iOS truth table, same week

`limited.cpt_master_daily` carries both sides of the question in one row:

```sql
SELECT IF(country='US','US','ROW') AS geo,
       ROUND(SUM(total_spend)) AS spend,
       ROUND(SUM(facebook_spend)) AS facebook_spend,
       SUM(new_installs) AS new_installs,
       SUM(trials_started) AS trials_started,
       SUM(direct_purchases) AS direct_purchases,
       SUM(total_transactions) AS total_transactions,
       SUM(trials_converted) AS trials_converted,
       SUM(new_subscribers) AS new_subscribers,
       SUM(purchase_completed_users) AS purchase_completed_users,
       ROUND(SUM(total_spend)/NULLIF(SUM(trials_started),0),2) AS cost_per_trial
FROM `bc-ads-tester.limited.cpt_master_daily`
WHERE date BETWEEN DATE '2026-09-08' AND DATE '2026-09-14'
GROUP BY geo ORDER BY geo
```

| iOS, 09-08…09-14 | spend | of which Facebook | installs | trials | direct | **total transactions** | **purchase_completed users** | CPT |
|---|---|---|---|---|---|---|---|---|
| US | $135,010 | $110,323 | 46,112 | 6,076 | 328 | **6,404** | **6,609** | $22.22 |
| Rest of world | $33,845 | $26,298 | 54,772 | 3,639 | 105 | **3,744** | **3,704** | $9.30 |
| **iOS total** | **$168,855** | **$136,621** | **100,884** | **9,715** | **433** | **10,148** | **10,313** | **$17.38** |

**`purchase_completed_users` / `total_transactions` = 1.016.** The canonical
iOS table puts the app event and "trials + direct buys" within 1.6% of each
other, computed from two independent pipelines (GA4 client events vs Adapty
billing). That is the cleanest single line of evidence in this document.

(`trials_converted` / `new_subscribers` in this table are **cohort-dated** —
they count what a given day's cohort has converted so far, so a 1-to-7-day-old
cohort reads near zero: US 300 / 628. They are not the in-week conversion
count; use the Adapty figure, 5,002. Do not read this table's
`cost_per_subscriber` on a fresh window — the $215 it shows is a maturity
artifact, not a CPS.)

### 1e. The ad set in BigQuery, and the 28-day account comparison

```sql
SELECT adsetId, adsetName, campaignId, platform, provider,
       SUM(spend) AS spend, SUM(CAST(results AS FLOAT64)) AS results,
       SUM(CAST(impressions AS FLOAT64)) AS impressions, SUM(CAST(clicks AS FLOAT64)) AS clicks,
       COUNT(*) AS rows_matched, COUNT(DISTINCT country) AS countries
FROM `bc-ads-tester.ads.marketing_adgroup_data`
WHERE app_id='biblechat'
  AND date BETWEEN DATE '2026-09-08' AND DATE '2026-09-14'
  AND (adsetId = '120246661279120160' OR campaignId = '120246606714520160'
       OR adsetName LIKE '%173fcfa4%')
GROUP BY adsetId, adsetName, campaignId, platform, provider ORDER BY spend DESC
```

**One ad set matched, 7 rows (one per day), one country (US)**, provider
`facebook`, platform `IOS`. Attribution source: Meta's own reporting, mirrored
into BigQuery — not an MMP.

| | BigQuery `marketing_adgroup_data` | Graph API (live, 7d click) |
|---|---|---|
| spend | $12,206.04 | $13,552.35 |
| results (= purchase_completed) | 416 | 467 |
| `purchase` in extraFields (= fb_mobile_purchase) | 282 | 337 |
| impressions | 809,957 | 888,896 |

The daily rows show why: 09-08, 09-09, 09-12, 09-13, 09-14 match the Graph
figures exactly, while **09-10 ($1,004 vs $1,368; 28 vs 42 results) and 09-11
($858 vs $1,837; 40 vs 77)** were captured mid-day and never refreshed. The
BigQuery ads mirror is a snapshot that can under-capture; the Graph numbers in
Check 2 stand as the ad-level truth. `extraFields` carries `omni_purchase` /
`purchase` (identical values — the same event twice) and `omni_custom` (all
custom events pooled), but **never a `purchase_completed` key** — so BigQuery
cannot break Meta's custom-event pool apart either.

Account-wide, 28 days ending 2026-09-14, all stores (the right denominator —
`purchase_completed` fires on iOS *and* Android):

```sql
WITH ev AS (
  SELECT event_type, event_datetime, original_transaction_id, store
  FROM `bc-ads-tester.subscription.adapty_realtime`
  WHERE app_id='biblechat' AND environment='Production'
    AND event_type IN ('trial_started','subscription_started','trial_converted')
    AND event_datetime >= TIMESTAMP '2026-07-19 00:00:00'
    AND event_datetime <  TIMESTAMP '2026-09-15 00:00:00'
),
trial_ids AS (
  SELECT DISTINCT original_transaction_id
  FROM ev WHERE event_type='trial_started' AND original_transaction_id IS NOT NULL
)
SELECT e.store,
  COUNTIF(e.event_type='trial_started') AS trial_starts_28d,
  COUNTIF(e.event_type='subscription_started' AND t.original_transaction_id IS NULL) AS direct_purchases_28d,
  COUNTIF(e.event_type='trial_started')
    + COUNTIF(e.event_type='subscription_started' AND t.original_transaction_id IS NULL) AS first_transactions_28d,
  COUNTIF(e.event_type='trial_converted') AS trial_converted_28d
FROM ev e
LEFT JOIN trial_ids t ON t.original_transaction_id = e.original_transaction_id
WHERE e.event_datetime >= TIMESTAMP '2026-08-18 00:00:00'
  AND e.event_datetime <  TIMESTAMP '2026-09-15 00:00:00'
GROUP BY e.store ORDER BY first_transactions_28d DESC
```

| store | trial starts | direct | **first transactions** | trial→paid |
|---|---|---|---|---|
| app_store (iOS) | 75,152 | 3,325 | **78,477** | 37,575 |
| play_store (Android) | 31,261 | 779 | **32,040** | 9,914 |
| stripe (web) | 256 | 0 | **256** | 55 |
| **all** | **106,669** | **4,104** | **110,773** | **47,544** |

New payers over the 28 days = 47,544 trial conversions + 4,104 direct = **51,648**.

---

## The comparison

**Meta's 60,820 (account, 28d, Meta-attributed spend) against the whole route:**

| Meta's `purchase_completed` compared to… | route count | ratio |
|---|---|---|
| all first transactions (trials + direct, all stores) | 110,773 | **0.55** |
| iOS-only first transactions | 78,477 | 0.78 |
| **new payers** (trial conversions + direct, all stores) | **51,648** | **1.18** |
| trial→paid conversions only, all stores | 47,544 | 1.28 |

The payer reading is **impossible**: Meta would be claiming 18% more paid
conversions than the entire company recorded in that window, organic included.
The first-transaction reading is unremarkable: Meta claims 55% of all first
transactions, on an account carrying ~$1.1M of the period's spend, with a
modeled 7-day-click window that over-claims somewhat. `purchase_completed`
lines up with **trial starts + direct purchases**.

**The ad set's 467 against the US iOS route, same week:**

| | ad set 120246661279120160 | US iOS route | ad set share |
|---|---|---|---|
| spend | $13,552 | $135,010 | 10.0% |
| installs | 1,560 | 46,112 | 3.4% |
| `purchase_completed` / first transactions | 467 | 7,320 | **6.4%** |
| cost per `purchase_completed` vs route CPT | $29.02 | $22.22 | 1.31x |

Read as trials the ad set is coherent: it buys 6.4% of the route's first
transactions for 10.0% of its spend, i.e. a CPT about 1.3x the US blended rate
— an ordinary below-average pool. Read as payments it is not: 467 would be
9.3% of the week's 5,002 US iOS trial conversions, bought with 1,560 installs
inside a 7-day *click* window that structurally cannot reach a day-10 charge.

**Caveats on every ratio above.** The two sides are not the same measurement.
Meta's counts are modeled, deduplicated to a 7-day-click window, and on iOS are
reconstructed through SKAN/ATT rather than observed — that is the direction of
the 0.55 (Meta sees less than the route) and, simultaneously, of any
over-claiming. The route counts are observed billing events dated by when the
event happened, with no channel attached at all — they include organic, Apple
Search Ads, TikTok, Google and creators alongside Meta. So the ratios bound the
question; they do not reconcile the two systems, and no BigQuery table can,
because the ad-set key does not exist on the billing side (1a).

## Accuracy note

- **Curated vs raw.** `adapty_realtime` is first-party billing truth,
  event-level, near-real-time (today's partial day already carried 1,211 trials
  when queried) — the highest-trust source here. `cpt_master_daily` is a
  curated daily materialization (~07:30 UTC), the table budget decisions are
  made from. `paywall_events` is a daily GA4 warehouse build and is explicitly
  **not** billing truth — its own gotcha says `purchase_completed` over-counted
  Adapty trial starts by ~8.8% on a measured US/en/iOS cohort; this week it ran
  4.5% *under*, so treat ±10% as the client sensor's honest band.
  `ads.marketing_adgroup_data` is a mirror of Meta's reporting and, as 1e
  shows, can be stale mid-day.
- **The week is real, not an artifact.** Daily iOS trials run 3,516 → 1,435
  from 08-18 to 09-13, a steady monotone decline, so the week's 11,127 sits
  well below the 28-day average of ~18,800/week. Because conversions landing
  this week come from a larger cohort seven days earlier, the in-week ratio
  7,681/11,127 = 69% is a **cross-cohort artifact, not a trial→paid rate**. The
  matured 28-day iOS rate is 37,575/75,152 = 50%.
- **Country basis differs by table.** Adapty US trials (6,944, `store_country`)
  vs `cpt_master_daily` US trials (6,076) differ by 12% — store country vs the
  CPT pipeline's country. Neither is wrong; do not mix them in one ratio.
- **Known gotchas that bite here:** never count `trial_started` as revenue
  (~94% of trial rows carry a phantom price); payers must be counted as
  `trial_converted` OR (`subscription_started` AND NOT `trial_started`), which
  is what the SQL above does; `results` in `ads.*` is documented unreliable
  (it happened to be close here, at 416 vs 467, only because of the two stale
  days); `singular_*_installs` are 3-5x ATT undercounts and were not used.
