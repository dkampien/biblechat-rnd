---
created: 2026-09-15
updated: 2026-09-15
question: "Is the app custom event `purchase_completed` the trial start (first transaction, free trial included) or the paid conversion after the trial? What is fb_mobile_purchase relative to it?"
scope: "act_697155031095732 (Basmo iOS); ad set 120246661279120160; 2026-09-08..2026-09-14, 7-day click"
status: verdict reached and confirmed against BigQuery (all checks run)
---

# Is `purchase_completed` the trial or the payment?

## Verdict, up front

**`purchase_completed` is the first transaction — the moment the store
accepts the subscription, which for this product is almost always the start
of a 7-day free trial.** It is not the paid conversion after the trial.
Confidence: **high**.

**`fb_mobile_purchase` is the same moment seen by a second, lossier sensor**
— Meta's own iOS SDK logging the StoreKit transaction — not a later stage.
It runs at ~72% of `purchase_completed` on iOS and does not exist at all on
Android. Confidence: **high**.

Main caveat: `purchase_completed` fires on *every* first transaction, so it
also contains the small direct-purchase (no-trial) tail. The company's own
August split is 124k trials vs 5k direct buys, so it is ~96% trials — close
to, but not exactly, a pure trial event. **BigQuery now confirms that split at
route level: 11,127 trial starts vs 498 direct buys on iOS in this week, 4.3%
direct** (Check 1b). It cannot be measured per ad set, because the billing
table carries no Meta ad ids at all (Check 1a).

---

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

### 1f. The comparison

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

### 1g. Accuracy of the sources

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

---

## Check 2 — what the events mean at the source

### 2a. What the ad set actually optimizes for

`GET /120246661279120160?fields=name,optimization_goal,destination_type,promoted_object,attribution_spec,bid_strategy`
(Graph v23.0, token from `project - auto-ads-four/.env.local`, read-only):

```json
"promoted_object": {
  "application_id": "246559161388001",
  "custom_event_type": "OTHER",
  "object_store_url": "http://itunes.apple.com/app/id6448849666",
  "custom_event_str": "purchase_completed",
  "smart_pse_enabled": false
},
"optimization_goal": "OFFSITE_CONVERSIONS",
"destination_type": "APP",
"attribution_spec": [{ "event_type": "CLICK_THROUGH", "window_days": 7 }]
```

`custom_event_str` names the event explicitly. `custom_event_type: OTHER`
means Meta was never told this is a standard Purchase or StartTrial — it is
an opaque custom event, so **Meta itself does not know what it means.** Only
the app does.

The MCP's `ads_get_ad_entities` returns `promoted_object` without
`custom_event_str`, which is why the earlier reading could not name the
event from the config; the Graph call carries it.

### 2b. The app's registered event catalogue

`GET /246559161388001/app_event_types?limit=500` → **408 registered event
names.** The money-relevant ones:

| Event | Kind | Meta's own description |
|---|---|---|
| `purchase_completed` | custom | (none — custom events carry no description) |
| `purchase_started` / `purchase_cancelled` / `purchase_canceled` / `purchase_error` / `purchase_restored` | custom | none |
| `purchase_completed_IAP` | custom | none — a **separate** event from `purchase_completed` |
| `web_purchase` | custom | none |
| `paywall_shown`, `onboarding_paywall_shown`, `paywall_skipped` | custom | none |
| `fb_mobile_purchase` | **standard** | "Purchases — Purchase events signaled by the application" |
| `fb_mobile_initiated_checkout` | standard | "Initiated Checkout" |
| `fb_mobile_purchase_failed` | standard | "Purchase Canceled" |
| `StartTrial` | **standard** | registered, but see below |
| `Subscribe` | standard | registered, but see below |

`StartTrial` and `Subscribe` **exist in the catalogue but carry no attributed
volume** (2c). `purchase_completed_IAP` existing alongside `purchase_completed`
says `purchase_completed` is the generic "the purchase flow succeeded" event
across rails, not a store-specific one.

Custom conversions: `ads_get_customconversions(act_697155031095732)` →
**empty, 0 total.** Nothing is built on top of `purchase_completed`; the ad
sets point at the raw app event.

The builder MCP's `list_app_events` is, as suspected, **Apple In-App Events**
(App Store promo cards from `asc_app_events`) — unrelated to analytics
events. Confirmed from the tool description; not called.

The `ads_get_datasets` / `ads_get_dataset_stats` route is a dead end for this
question: the app's events do not live in a dataset. The dataset named
"Bible Chat App" (`114743231621327`) exists but carries a trickle — over
28 days it shows ~1–2 `Subscribe` per hour plus a handful of `screen`,
`purchase_started` and `onboarding_shown` bursts, and **zero
`purchase_completed`**. It is a side channel, not the ad-serving source.

### 2c. Meta receives no trial event at all

`GET /act_697155031095732/insights?date_preset=last_28d&fields=spend,actions&action_attribution_windows=["7d_click"]`
— every money-shaped action type in the whole account over 28 days:

| action_type | 28d count |
|---|---|
| `app_custom_event.other` (all custom events pooled) | 4,768,881 |
| `mobile_app_install` | 727,567 |
| `app_custom_event.fb_mobile_activate_app` | 369,106 |
| `app_custom_event.fb_mobile_initiated_checkout` | 39,011 |
| `app_custom_event.fb_mobile_purchase` | 34,677 |
| `app_custom_event.StartTrial` | **absent** |
| `app_custom_event.Subscribe` | **absent** |

There is no trial event and no subscribe event reaching Meta. Whatever
`purchase_completed` is, it is the **only** first-money signal Meta has.

### 2d. The ad set's full action breakdown

`GET /120246661279120160/insights` with
`time_range={"since":"2026-09-08","until":"2026-09-14"}`,
`action_attribution_windows=["7d_click"]`,
`fields=spend,impressions,actions,action_values,cost_per_action_type`.
Spend $13,552.35, impressions 888,896. The relevant rows:

| action_type | count | value |
|---|---|---|
| `app_custom_event.other` (all custom pooled) | 14,409 | — |
| `mobile_app_install` | 1,560 | — |
| `app_custom_event.fb_mobile_initiated_checkout` | 377 | $676.39 |
| `app_custom_event.fb_mobile_purchase` | 337 | $730.89 |
| `web_app_in_store_purchase` | 337 | $0.07 |

and separately, via `fields=conversions`:
`app_custom_event.purchase_completed` = **467**, cost per result $29.02.

Three things fall out:

1. **467 > 377.** `purchase_completed` exceeds `fb_mobile_initiated_checkout`.
   It cannot be a step *after* the SDK's checkout chain; it is a different
   sensor watching the same moment from the app's own code.
2. **$730.89 / 337 = $2.17 per purchase.** The product sells at ~$4.99/week
   or ~$40/year. $2.17 is not a subscription price. Account-wide across all
   iOS campaigns this week the figure is $8,165.64 / 4,641 = **$1.76**. A
   real post-trial charge would show the real price. A free-trial StoreKit
   transaction shows ~$0.
3. `purchase_roas` = `mobile_app_purchase_roas` = **0.054**. At $29 per
   result, a genuine paid subscriber would not produce 5% ROAS.

### 2e. The two events fire on the same day, not seven days apart

Daily, 2026-09-01 → 2026-09-14, same ad set, 7d click:

| date | spend | installs | purchase_completed | fb_mobile_purchase |
|---|---|---|---|---|
| 09-01 | 1,735.53 | 219 | 55 | 39 |
| 09-02 | 2,229.04 | 254 | 66 | 50 |
| 09-03 | 2,153.45 | 224 | 59 | 46 |
| 09-04 | 1,828.36 | 216 | 55 | 41 |
| 09-05 | 1,729.02 | 192 | 54 | 24 |
| 09-06 | 2,517.09 | 233 | 74 | 43 |
| 09-07 | 1,943.79 | 184 | 68 | 44 |
| 09-08 | 2,433.97 | 270 | 91 | 57 |
| 09-09 | 2,062.00 | 237 | 77 | 48 |
| 09-10 | 1,368.65 | 167 | 42 | 39 |
| 09-11 | 1,837.04 | 278 | 77 | 57 |
| 09-12 | 1,790.53 | 188 | 65 | 48 |
| 09-13 | 2,001.52 | 191 | 55 | 43 |
| 09-14 | 2,058.64 | 229 | 60 | 45 |

The two curves move together, day for day, at a steady ~0.7 ratio. If
`fb_mobile_purchase` were the paid conversion at the end of a 7-day trial it
would be a 7-day-shifted, ~48%-scaled copy of `purchase_completed`. It is
neither shifted nor scaled to the trial-to-paid rate.

### 2f. Brand-new campaigns already have both events

`GET /<campaign>?fields=name,created_time,start_time`:

| campaign | started | purchase_completed | fb_mobile_purchase |
|---|---|---|---|
| Sept 12, 2026 – New Scale (`120247136242960160`) | 2026-09-12 20:07 | 207 | 119 |
| Sept 13, 2026 – 2Scale (`120247142878230160`) | 2026-09-13 14:03 | 14 | 11 |

A campaign that has been live for **one day** has 11 `fb_mobile_purchase`
events. A 7-day trial cannot have converted to paid yet. Combined with the
7-day *click* attribution window — which structurally cannot reach a day-10
charge — this rules out "paid conversion after the trial" for both events.

### 2g. Every campaign in the account is a CPT campaign on this event

Campaign level, 2026-09-08..14, sorted by spend (35 campaigns with spend):

- **34 of 35** report `results.indicator = conversions:app_custom_event.purchase_completed`;
  the remaining ones are `mobile_app_install` (CPI tests) and one `lead` campaign.
- Every one of those 34 is named **"CPT"** — cost per trial.
- `omni_purchase` is **null on every Android campaign** and populated on every
  iOS campaign. A funnel *stage* would not be platform-specific; a *sensor*
  (Meta's iOS SDK) is.
- A few campaigns have `omni_purchase` **greater** than `purchase_completed`
  (FirstUS iOS 90 vs 77; PH iOS Aug 11 75 vs 37). A later stage can never
  outrun an earlier one. Two overlapping sensors can.

Aggregating the 35 campaigns: **spend $165,956, purchase_completed 9,114,
$18.21 each.** Account-wide over 28 days: **spend $1,106,080,
purchase_completed 60,820, $18.19 each.**

### 2h. The automation that builds these campaigns

`_projects/adloops-local-deprecated-don't-read/ads-library-automation/functions/src/campaigns/facebook/`:

- `ios/FacebookSkanPurchaseExperiment.ts`, `ios/smart_plus/FacebookSmartSkanPurchaseExperiment.ts`
  and `android/FacebookAndroidPurchaseExperiment.ts` all hard-code
  `custom_event_type: "OTHER"`, `custom_event_str: "purchase_completed"`.
- The app experiment classes are only **Install** and **Purchase**. There is
  no separate Trial experiment. So the org's "CPT" campaigns *are* the
  purchase_completed campaigns: in this codebase, "purchase" and "trial"
  name the same event.

---

## Cross-check against the company's own numbers

Both figures below are already written down in the repo; neither was
re-derived from BigQuery in this session.

From `_docs/core/one-pager-numbers.md` (August 2026):

| | August |
|---|---|
| Trials | 124k |
| Direct buys (skip trial) | 5k |
| **First transactions (trials + direct)** | **129k** |
| New subscribers | 52k |
| CPT | $16.6 – $16.7 |
| CPS | $34.6 – $40.1 |

From `_docs/core/measurement-map.md`, app-wide 28 days, all users including
organic: `purchase_started` 591K → **`purchase_completed` 131K**, standard
`Purchase` 48K.

- 131K `purchase_completed` vs **129k first transactions** — a match.
- 131K vs **52k new subscribers** — off by 2.5x. `purchase_completed` is not
  the payment.
- $18.19 cost per `purchase_completed` on this account vs the company's
  documented **CPT $16.6–17** (blended across all channels and both
  platforms; Meta is the bulk of spend, so $18 on the Meta account against
  $17 blended is the right size).
- Cost per `purchase_completed` at $18.19 vs **CPS $34.6–40.1** — not the
  same number.

This also resolves the measurement map's open question ("Two money events
coexist… why both exist and what explains the 2.7x gap: [unknown], open
question for Arthur"): they are not two stages. They are one moment counted
twice — once by the app's own code on every platform and rail, once by
Meta's iOS SDK watching StoreKit. The gap is coverage loss, not conversion.

---

## Tool calls and queries used

**biblechat-analytics MCP** (read-only; nothing written to the catalog or
report tools):

1. `analytics_guide()`, `list_catalog_tables()`.
2. `describe_table` on `subscription.adapty_realtime`, `ads.marketing_adgroup_data`,
   `data_warehouse.paywall_events`, `limited.cpt_master_daily`.
3. `execute_query` x 6 — the SQL is quoted verbatim in Check 1, plus a daily
   trial/conversion series (08-18 → 09-15) used only for the freshness and
   cross-cohort checks in 1g. ~0.31 GB scanned in total.

**facebook-ads MCP** (`client_conversation_id: Kq7Lm2Xr9Tb4Wz6Yn1Pd`):

1. `ads_get_datasets(ad_account_id=697155031095732, limit=50)` → 18 rows, 9 distinct datasets.
2. `ads_get_dataset_details(dataset_id=114743231621327)` → "Bible Chat App", active, last fired 2026-09-15.
3. `ads_get_dataset_stats(dataset_id=114743231621327, aggregation=event, start_time=1787011200, end_time=1789430400)` → 28d: only `Subscribe`, `screen`, `purchase_started`, `onboarding_shown`, `PageView`, `CompleteRegistration`; single-digit counts; **no `purchase_completed`**.
4. `ads_get_customconversions(ad_account_id=697155031095732, limit=100)` → **0 custom conversions**.
5. `ads_get_field_context(field_names=[promoted_object, optimization_goal, attribution_spec, destination_type])` and a second call for the value/ROAS fields.
6. `ads_get_ad_entities(level=adset, object_ids=[120246661279120160], fields=[name, promoted_object, optimization_goal, destination_type], time_range 09-08..09-14)`.
7. `ads_get_ad_entities(level=adset, object_ids=[…], fields=[…, omni_purchase, omni_purchase_values, mobile_app_purchase_roas, purchase_roas])` → 337 / $730.89 / 0.0539.
8. `ads_get_ad_entities(level=campaign, fields=[name, amount_spent, results, cost_per_result, omni_purchase, omni_purchase_values, omni_app_install], time_range 09-08..09-14, sort=amount_spent_descending, limit=40)`.

`ads_get_dataset_quality` was not called: the app's events are not in a
dataset, so EMQ / match-key coverage does not apply to this question.

**Graph API v23.0**, read-only, token `META_ACCESS_TOKEN` from
`/Users/dennisk/Hub/focus/project - auto-ads-four/.env.local` (never printed):

```
GET /120246661279120160?fields=name,optimization_goal,destination_type,promoted_object,attribution_spec,bid_strategy
GET /246559161388001?fields=name,category,link,object_store_urls
GET /246559161388001/app_event_types?limit=500
GET /120246661279120160/insights
      ?time_range={"since":"2026-09-08","until":"2026-09-14"}
      &fields=spend,impressions,actions,action_values,cost_per_action_type
      &action_attribution_windows=["7d_click"]&level=adset
GET /120246661279120160/insights
      ?time_range={"since":"2026-09-01","until":"2026-09-14"}
      &fields=spend,actions,conversions
      &action_attribution_windows=["7d_click"]&time_increment=1
GET /act_697155031095732/insights
      ?date_preset=last_28d&fields=spend,actions
      &action_attribution_windows=["7d_click"]
GET /act_697155031095732/insights
      ?date_preset=last_28d&fields=spend,conversions,conversion_values
      &action_attribution_windows=["7d_click"]
GET /{120247136242960160,120247142878230160,120247057499270160}?fields=name,created_time,start_time
```

Endpoints tried that do not work: `/{app_id}/app_events_config` (unknown
path), `/{app_id}/activities`, `/{app_id}/aggregate_revenue` (nonexistent
fields), `/{app_id}/app_insights/app_event` (deprecated from v12.0).

**Side task (coordinator's request):** ran
`node scripts/ad-destinations.ts --ad-ids <16 ids> --json …/adset-120246661279120160_destinations.json`
from `project - auto-ads-four`. All 16 ads point at the same destination —
`http://itunes.apple.com/app/id6448849666`, custom product page
`74c0e8e2-5028-4964-817a-c315959f115e`, CTA `INSTALL_MOBILE_APP`, no deep
links anywhere. 49 URL occurrences, one distinct URL. Written to
`_projects/funnel-maps/data/readings/app/adset-120246661279120160_destinations.json`.

Nothing was modified in any system.

---

## What each event counts

| | `purchase_completed` | `fb_mobile_purchase` |
|---|---|---|
| Who emits it | the app's own analytics code | Meta's iOS SDK, automatic StoreKit logging |
| Standard or custom | custom (`custom_event_type: OTHER`) | Meta standard "Purchases" |
| Platforms | iOS **and** Android | iOS only |
| Fires when | the store accepts the first transaction — free-trial start or direct purchase | the same StoreKit transaction |
| Value carried | none exposed to Meta | ~$2 average — a $0 free trial, not a price |
| This ad set, 09-08..14 | 467 @ $29.02 | 337 @ $40.21 |
| Account, 28d | 60,820 @ $18.19 | 34,677 |
| Coverage vs the other | 100% (the reference) | ~72% on iOS, 0% on Android |

**Neither is the paid conversion.** Nothing in this ad account measures the
payment at the end of the trial. Per-ad visibility ends at trial start, which
is exactly what `_docs/core/how-the-numbers-work.md` already says: "an ad's
job ends at trial start… Per-ad visibility ends at trial start."

## Open, after the BigQuery run

1. **Answered (route only).** The trial vs direct-purchase split inside
   `purchase_completed` is 95.7 / 4.3 on iOS for this week (Check 1b), matching
   the ~96/4 company figure. Per-ad-set it stays unmeasurable — see 2.
2. **Answered: no.** `adapty_realtime` carries attribution only for Apple
   Search Ads; no cataloged table joins billing to a Meta campaign or ad set.
   Meta-side counts can be reconciled to the ledger **per route only**, never
   per pool. Anything finer needs an MMP feed that does not exist in BigQuery.
3. **Still open.** Why `fb_mobile_purchase` loses ~28% of iOS transactions, and
   whether that loss is random or skewed (ATT-opted-out users, StoreKit 2,
   restores). BigQuery cannot answer this one either — the loss happens inside
   Meta's SDK, upstream of anything the ledger sees.
4. **New, from 1e.** `ads.marketing_adgroup_data` under-captured two of the
   seven days (09-10, 09-11) by 25-55% of spend and never backfilled. If that
   table feeds any dashboard, its recent days are low. Worth telling whoever
   owns the pipeline.
