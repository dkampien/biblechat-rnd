---
created: 2026-09-15
updated: 2026-09-15 (web column ladder added, overview renamed and debloated, app ladder data-driven, app scan added over 218 ad sets with the ad-to-product-page pairing)
---
# Funnel maps

The family of BibleChat marketing-funnel views, one page per question. Source HTML lives here next to the docs it draws from; the published pages are artifacts. Raw data behind them sits in `_projects/funnel-maps/data/`.

| Role | Page | File | Artifact |
|---|---|---|---|
| Overview | Funnel map | `funnel-bands.html` | https://claude.ai/artifact/FgxQZjV9GssNTJ1efWH3s3 |
| Scan, app route | App route scan | `app-scan.html` | https://claude.ai/artifact/MbK7pPgRfnsw97pDhkgWg6 |
| Ad view, app route | App route column ladder | `app-column-ladder.html` | https://claude.ai/artifact/62v3xLW1258bfv7ZQZVVv3 |
| Ad view, web route | Web route column ladder | `web-column-ladder.html` | https://claude.ai/artifact/Fy2SK15Av8MCV999CGdfBS |
| Reference drawing, app | App route, ad view | `app-ad-view.html` | https://claude.ai/artifact/7XC7bGow8eVXupovSmDp68 |
| Reference drawing, web | Web route, ad view | `web-ad-view.html` | https://claude.ai/artifact/6J93DauCiQ2Vx68c5pZSFW |

- **Overview**: six commitment bands, doors at the top, web and app routes as threads. Needs polish and a debloat.
- **Scan** (the daily list): every ad set on the app route as one row, rules already run, flagged rows first by spend; group by campaign, door, product page, platform or attribution window. Renders the `SCAN` block (`readings/app/scan-adsets_<from>_<to>.json`) plus the `PAIRING` block (`data/app-store/adset-to-cpp-<date>.json`, folded from the per-ad destinations pull). Same `BENCH` thresholds as the ladder.
- **Ad views** (the observability layer): the Ads Manager columns in funnel order, one page per route. Counts are nodes, rates sit on edges, cost-pers hang off nodes, one spend pool. Below the cut: the cohort tripwire (trial-to-paid for app, renewal 1 for web).
  - App ladder is **data-driven** since 2026-09-15: it holds no numbers, it renders the `READING` block (one pool's raw counts and world) and computes rates, cost-pers and the diagnosis rules (`BENCH` block holds the thresholds). Per-ad rows render as a scan table under the ladder. The ladder also embeds every pool of the last scan (`POOLS` block) plus the pairing: `#pool=<adset id>` in the URL, or the picker, reads any of them; scan rows link here. To read another pool: pull a reading into `_projects/funnel-maps/data/readings/<route>/` (format in its README, pull via an Opus subagent on the facebook-ads MCP), paste it between the `/*READING*/` markers, republish.
  - Web ladder is still hand-typed from the web2app P&L; per-ad reads need WEB account access. Same rewrite pending.
- **Reference drawings**: the routes as narrowing funnels with seams (rate, lever, owner). Kept for the drawing style, not the role.

For another agent needing context from the session that built this: its line in `_docs/core/sessions.jsonl` (transcript path, what it did, what is only in the thread, how to query it).

## How to edit and republish

1. Edit the HTML here. The files are complete pages without doctype/html/head/body (the artifact host wraps them).
2. Preview: headless Brave renders them on the mini (Chrome is not installed):
   `"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=4000 --window-size=1300,1700 --screenshot=out.png file:///path/to/preview.html`
   (wrap the file in `<!doctype html><html><head><meta charset="utf-8"></head><body>...</body></html>` first, as the host does).
3. Publish with the Artifact tool, passing the artifact URL above as `url` so the link stays the same.

## Data behind the pages (`_projects/funnel-maps/data/`)

- `data/web-funnel/`: the christian-archetype funnel's own screen config (`window.__obScreens`, 41 screens, `postPurchase` order), the per-session pricing response (three plans), and the payments script (Purchase pixel, trial mode). Read 2026-09-15 from verseread.com.
- `data/app-store/`: the 66 custom product pages from the App Store Connect API (names, ppids, version states), read 2026-09-15 with Denis's individual key.
- `data/builder/`: raw extracts from the internal builder MCP (onboardings list, the mapped onboarding's pages, paywalls, rule sets, segments), read 2026-09-15, read-only.
- `data/meta-active-ads-2026-09-15.json`: 587 active Basmo IOS ads with 7-day spend and impressions from the MCP (no destinations).
- `data/app-store/ad-destinations-2026-09-15.json`, `ad-to-cpp-2026-09-15.json`, `adset-to-cpp-2026-09-15.json`: every active ad's destination from the Graph API (script in the auto-ads-four project), per ad and folded per ad set. Summary: `_docs/core/ad-to-cpp-summary.md`.
- `data/readings/`: one raw reading per pool per period (format in its README); `_subagent-scripts/` holds the build scripts the pulls used.

Written-up versions of all of this: `_docs/core/measurement-map.md`, `_docs/core/app-onboarding-map.md`, `_docs/core/destinations-inventory.md`.

## Scope agreed 2026-09-15

Overview: polish and debloat later. Web column ladder: built 2026-09-15 (rename of the overview the same day). App columns: only after the "Funnel LTR - app" preset is actually settled. Simulation view: parked until end-of-year goals and the app-side blank rates exist. Nothing else gets built.
