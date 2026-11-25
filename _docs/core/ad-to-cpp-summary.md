---
title: Ad-to-destination pairing — Basmo iOS (act_697155031095732)
created: 2026-09-15
updated: 2026-09-15
source_pull: _projects/funnel-maps/data/app-store/ad-destinations-2026-09-15.json
pairing_table: _projects/funnel-maps/data/app-store/ad-to-cpp-2026-09-15.json
inventory: _docs/core/cpp-inventory.json
scope: act_697155031095732, ads created since 2025-01-01, --active-only
pulled_at_utc: 2026-09-15T14:51:22Z
ad_count: 597
---

# Where the active ads land

## The shape

Every ad in this account ends at one of three destinations:

1. **iOS App Store** — 212 ads. This is the only route where a custom product page (CPP) exists. 209 of the 212 carry a ppid; 3 fall through to the default store page.
2. **Google Play** — 332 ads. No CPP concept in the data (Play custom store listings are not exposed by the Graph API), so all 332 read as the default store page.
3. **Web onboarding** — 53 ads to `onboardings.thebiblechat.com`. 13 of them carry a `ppid=` parameter in the URL (all Lockscreen Widget V1), so the page identity survives the web hop; 40 carry none.

Store URLs are uniform: `http://itunes.apple.com/app/id6448849666` and `http://play.google.com/store/apps/details?id=com.basmo.BibleChat`.
Promoted app id is `246559161388001` on all 544 store-routed ads; the 53 web ads have none.
Optimization goal: OFFSITE_CONVERSIONS 505, APP_INSTALLS 92.
`url_tags` is null on every ad — no ad carries URL tags.

## Product pages by ad count

Counts are ads / ad sets / campaigns. "Route" shows how the ads reach the page.

| # | Page | ppid | Ads | Ad sets | Campaigns | Route |
|---|------|------|-----|---------|-----------|-------|
| 1 | default store page | — | 375 | 67 | 21 | Google Play 332, web 40, iOS 3 |
| 2 | Lockscreen Widget V1 | 5c3e6d53-c159-44c2-b431-bcb0b0bde19b | 61 | 18 | 8 | iOS 48, web 13 |
| 3 | Custom Journey | dd285908-3abd-4b51-8f2f-526f6e57de1b | 30 | 12 | 7 | iOS 30 |
| 4 | Know the Bible - Audio Lessons | ca9a9ae2-029b-4b48-bdb7-7230acc4d874 | 25 | 4 | 2 | iOS 25 |
| 5 | Parenting V1 | 74c0e8e2-5028-4964-817a-c315959f115e | 23 | 4 | 3 | iOS 23 |
| 6 | Women of the Bible Quiz | d3d05403-3f82-4de1-b5ab-dec522183b97 | 22 | 3 | 2 | iOS 22 |
| 7 | Catholic (Teo) | 04e6f5ba-f662-425d-b1ab-4f3a2c5134d5 | 15 | 3 | 1 | iOS 15 |
| 8 | Men of the Bible Quiz | a658f244-5cf4-4b71-a4af-ee6a8f226c1a | 10 | 1 | 1 | iOS 10 |
| 9 | Calendar Catholic Widget | 92791336-17a1-439b-b515-ca4ae1c7c16a | 10 | 2 | 1 | iOS 10 |
| 10 | Chat V1 | 14ec91c4-4ab0-493f-afad-76cbebc27082 | 8 | 6 | 5 | iOS 8 |
| 11 | Bible Affirmations | ce55fae0-49f9-4e0c-88cf-0a576f5a3f4f | 8 | 5 | 2 | iOS 8 |
| 12 | Daily Plan New Generalist 2026 | 10050feb-9ec8-493f-9dfb-728daffe026d | 7 | 1 | 1 | iOS 7 |
| 13 | Audio Bible | a0c1dc72-1aaf-4df9-b714-e01a6b848a00 | 1 | 1 | 1 | iOS 1 |
| 14 | Study Plans V1 | 297f5fe9-7e34-42f8-9ddd-ceecc1522603 | 1 | 1 | 1 | iOS 1 |
| 15 | Bible Trivia (Teo) | 7ab71dc8-c7e8-4148-b5e4-60b781640d5b | 1 | 1 | 1 | iOS 1 |

**14 distinct custom product pages** are in use, out of the full inventory. Every ppid seen resolved against `cpp-inventory.json` — **no ppid is missing from the inventory**.

## Default store page

375 ads land on a default page, but they are three different situations:

- **332 Google Play ads** — the Graph API exposes no product-page id for Play, so "default" here means "not visible in this data", not necessarily "no custom listing".
- **40 web ads** — web onboarding URLs with no `ppid=` parameter.
- **3 iOS ads** — genuinely on the default App Store page:
  - `120246553892410160` 88.W1_animation_doll (Biblechat CPT Third - US - IOS - June 05, 2026 - Cristina)
  - `120243871054390160` 304.copy_3E716B41-D76A-40FA-A153-5E1DEF239CCB (same campaign)
  - `120243869091980160` 18.1275.affirmations.i2 (Biblechat CPT - Second US - IOS - June 05, 2026 - Cristina)

## Web destinations

53 ads, 11 ad sets, 3 campaigns, all pointing at `onboardings.thebiblechat.com`:

- Biblechat Daily Testing - Adv+ ABO US - IOS - February 2026
- Biblechat Daily Testing - Adv+ ABO US - ANDROID - February 2026
- Biblechat Daily Testing - Adv+ ABO US - ANDROID

All 53 are `ADSET_PAUSED` — the web route is not actually serving. The URLs carry `aid`, `placement`, `use_version` (lock_screen_v1, study_plans_v1, your_spiritual_journey, general_v1), `life_challange`, a base64 `_ddl` deep-link payload, and on 13 of them a `ppid=` pointing at Lockscreen Widget V1.

## Deep links

57 ads carry a `biblechatapp://` deep link, all on the iOS route. Intents seen:

| Intent | Ads |
|--------|-----|
| lock_screen | 29 |
| daily_plan | 13 |
| lock_screen_hourly_affirmations | 7 |
| chat_text | 3 |
| encoded task payload (launchInAppOnboardingPlacement `ios_lock_screen_widget_in_app` / `lock_screen_widget_in_app` + onboarding `chapters.widget.promoting.onboarding.v9_12`) | 2 |
| audio_bible | 1 |
| study_plans | 1 |
| bible_trivia | 1 |

## ppids not in the inventory

None. All 14 ppids found on ads resolve to a name in `cpp-inventory.json`.

## Oddities

- **The account is named "Basmo iOS" but 332 of 597 ads are Android.** 17 campaigns are Play-Store campaigns (CPT Scale US/LATAM/CA/AU/NZ, CPI US by creator, PH). No campaign mixes platforms, and no ad set mixes platforms.
- **`--active-only` does not mean "serving".** Meta's ad-level filter returned 537 ACTIVE, 53 ADSET_PAUSED, 7 WITH_ISSUES. The 53 ADSET_PAUSED are exactly the 53 web ads.
- **15 ad sets mix product pages** (iOS only — the CPP is set per creative, not per ad set). The biggest mixes:
  - `120245704287510160` (11 ads, CPT - US - IOS, July 06 2026) — Custom Journey + Parenting V1 + Chat V1
  - `120243869050720160` (6 ads, CPT - US 2. - IOS, June 05 2026) — Custom Journey + Study Plans V1 + Bible Affirmations + Lockscreen Widget V1 + default
  - `120243871036600160` (7 ads, CPT - US 5.. - IOS, June 05 2026) — Custom Journey + Audio Bible + Lockscreen Widget V1 + default
  - The rest are 2-3 page combinations, mostly Lockscreen Widget V1 paired with Custom Journey or Chat V1.
  This makes per-ad-set CPP attribution unsafe; pairing has to be read at the ad level.
- **Two ad sets mix a CPP with the default page** (`120243871036600160`, `120243869050720160`) — likely an oversight rather than a test.
- **No ad carries `url_tags`.** Any attribution parameters must come from elsewhere (the web URLs carry their own `utm_*`).
- **Concentration:** the top iOS page (Lockscreen Widget V1) holds 23% of iOS ads; the top 5 iOS pages hold 70% (148 of 212).

## Method

One read-only pull with `scripts/ad-destinations.ts --account act_697155031095732 --active-only --since 2025-01-01`. No rate limiting was hit. The 2025-01-01 window is not binding: the oldest ad returned was created 2026-01-22.

ppid resolution order per ad: `creative.app_product_page_id` (209 ads) → `ppid=` parsed from the destination URL (13 web ads) → null (default store page).
