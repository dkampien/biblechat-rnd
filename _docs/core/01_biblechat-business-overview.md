---
created: 2026-08-15
updated: 2026-09-07
---
# BibleChat Business Overview

Ground truth for building on BibleChat's marketing.

## 1. What is BibleChat

Bible Chat (Book Vitals Inc.) is a subscription app for Christians, on iOS and Android, in English and 16 other languages. The business is **faith-shaped mental health**: people arrive with a life problem (marriage, anxiety, grief) and pay for help that works through faith. Hundreds of thousands of App Store ratings at 4.9 stars.

## 2. Monetization and prices

- Auto-renewing subscriptions. Two ways in: a 7-day free trial, or subscribing directly.
- Paywall prices, in USD. App Store prices are set per storefront; emerging markets run at roughly half the US tier. The US is ~86% of iOS revenue, so the US column is the one to reason from.

| Plan | Romania storefront | US App Store |
|---|---|---|
| Weekly (with trial) | $2.20/week | $4.99/week |
| Monthly (with trial) | $4.40/month | $12.99/month |
| Yearly (no trial) | $33/year | $39.99/year |

- Growth is paid Meta ads, on two routes:
  - Web quiz funnels: quiz, registration, then a paywall.
  - Ads straight to the App Store listing, via custom product pages (CPPs).
- Two Meta ad accounts: Basmo IOS (app route: CPT/CPI campaigns sending to the store listing; EU is the billing entity) and a separate WEB account (runs the web funnels; limited internal access).

## 3. Key metrics, in funnel order

One month's spend flows down this funnel; each cost metric is that same spend divided by the survivors at one stage. Blended = all channels, organic included; paid-only numbers run higher at the money stages (iOS paid-cohort CPT is ~$19 against ~$17 blended).

Two blocks, because they have different sources. The ratios (CPT, trial-to-paid, store cut) are stable month to month. The volumes are not: weekly spend ran $346k in late July, peaked at $617k in the week of Aug 17, and was back to $416k by the week of Aug 31, so August is a spike month and neither month alone is typical.

**Paid Meta funnel, observed ranges** (Meta Ads Manager, early August 2026; the ad account mapped at the time, per-account provenance not fully pinned down):

| Funnel stage | Metric | Value | Notes |
|---|---|---|---|
| Impressions | CPM | $9-21 | |
| Clicks | Link CTR | 0.75-1.44% video · ~9-12% problem-targeted statics | different audiences, not comparable |
| Clicks | CPC (link) | $1.16-1.47 | |
| Landing page | Clicks reaching the page | 89-98% | healthy pages |
| Landing page | Cost per landing page view | $0.12-0.43 | quiz route |
| Quiz | Bounce before question 1 | ~64% | biggest visible web leak |
| Registration | Cost per registration | $1.04-3.35 | 12-41 per ad set within days |

**Monthly outcomes** (BigQuery, pulled 2026-09-07: spend from `subscription.daily_data`, billing from `subscription.adapty_realtime`, projections spend-weighted from `limited.cpt_master_daily` and its Android twin):

| Stage | Metric | Jul 2026 | Aug 2026 | Notes |
|---|---|---|---|---|
| Spend | Monthly ad spend | $1.25M | $2.08M | Meta 89% then 83%, TikTok 6% then 15%; rest Apple Search, Google |
| Trial | Trials | 75k | 124k | ~70% iOS |
| Trial | CPT (blended) | $16.6 | $16.7 | the daily steering metric; held flat through the spike |
| Subscriber | Subscribers | 36k | 52k | ~5-6k/month are direct purchases, no trial |
| Subscriber | CPS (blended CAC) | $34.6 | $40.1 | the August rise is mix (more Android trials), not efficiency |
| Subscriber | Trial-to-paid | 43% (iOS 50% · Android 30%) | 42% (iOS 48% · Android 27%) | matured cohorts: trials started from the 15th of the prior month through the 14th, converted at any later time |
| Return | Month-1 return, measured | iOS 32% · Android 40% | iOS 28% · Android 31% | gross revenue in the first 30 days over that month's spend (`cpt_master_daily`, its Android twin); the model projects M12 at roughly 3.1x M1, so ~32% M1 is what a 100% M12 requires |
| Return | Month-12 return, measured | matures Jul 2027 | matures Aug 2027 | latest measurable month is July 2025 iOS spend: 142% gross · 107% cash after 12 months (94.7k trials, $15.39 CPT) |
| Return | Month-12 return, projected | iOS 98% · Android 107% | iOS 96% · Android 84% | model estimate for the month's own spend, gross, pre store fees; below the 100% rule on iOS both months |

**Scale** (2026-09-07 snapshot): MAU 4.2M (August 2026, device-level) · paying subscriptions 199k (152k with auto-renew on) · MRR $2.55M gross / $1.91M net · ARR $30.6M gross / $22.9M net. Net = after store fees.

Live dashboard of these metrics, refreshed on the 2nd of each month: https://claude.ai/code/artifact/8f66edad-cc5d-4322-b927-030b2a7275bf (layout and refresh procedure in `_projects/metrics-dashboard/README.md`).

Store fees: essentially all recorded revenue pays through Apple/Google (blended cut ~25%), so net cash break-even needs a gross mo12 of ~143% on iOS (~134% blended).

## 4. Company goals and metric targets

- The goal: spend as much on ads as possible while every month's spend still earns back at least 100% of itself within 12 months (measured on gross mo12, the projected pre-fee number).
- Day to day, the team steers by CPT.
- What a trial is worth, measured: the one fully matured cohort (iOS trials started July 2025, 94.7k trials) returned $22.20 gross / $15.56 net per trial over 12 months, which was 142% gross / 107% cash on that month's $15.39 CPT. Under the gross rule that caps CPT at ~$22; cash break-even caps it at ~$16. Say which rule a ceiling is built on, because they differ by 43%.
- Projected and realized are two different numbers. The projection read below 100% on iOS throughout mid-2026 while the matured cohort realized 142%, and the model's calibration against matured cohorts has not been established. A decision should name which of the two it uses.
