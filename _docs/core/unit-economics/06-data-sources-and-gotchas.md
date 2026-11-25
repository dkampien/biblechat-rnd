---
created: 2026-09-16
updated: 2026-09-16
---
# Data sources, gotchas and reference points

For the next agent. Bullet list, grouped by source. Numbers are dated; treat them as reference, re-pull before using. Sheets built from these: `03-company-numbers-both-routes.md` (both routes; until written, `03-company-numbers-both-routes.md`), `04-plan-chain-goal-to-spend.md`, `02-how-the-numbers-work.md`, `01-terms-and-prices.md`; older versions in `_archive/`.

## The two routes, in one line each

- App route: iOS and Android, stores process payment, Adapty mirrors the store receipts, the mirror sits in BigQuery. Free 7-day trial or direct purchase.
- Web route: verseread.com quiz funnels, Stripe processes payment, nothing of it reaches BigQuery or Adapty. Paid intro, then full price. Buyer is sent into the app afterwards.
- Company MRR = app + web, summed by hand. No table holds both.

## Stripe (web route ledger)

- Access: restricted, read-only, live-mode key, registered as user-scope MCP server `stripe` (`npx -y @stripe/mcp --api-key=...` in `~/.claude.json`). Reads on subscriptions, invoices, charges, customers, balance_transactions work; writes are refused. The Claude Code Stripe plugin (hosted mcp.stripe.com) is OAuth-only and needs a dashboard seat; ignore it. No Sigma, so aggregations run in a local script over paged GETs (limit=100, starting_after). ~11.5k subscriptions ever, ~7k charges per 5 weeks; fine.
- The account is SHARED. Products in it: "Bible Chat" (the live web funnels), "Sam - Bedtime Stories" (sister app, ~$4k MRR), "Bible Chat Pro ... Stay Connected" (2025 web attempt, all cancelled), "Bible Chat Premium In App" (small, unclear), QA products, upsell placeholders. Filter every web number to product name "Bible Chat". Map customer → product through the customer's subscription; charges do not carry the product.
- How the intro is wired: the intro is a separate one-off charge (no `invoice`), and the subscription starts as a $0 Stripe TRIAL of the intro length. So `status=trialing` = inside the paid intro; `active` = renewed at full price; `past_due` = renewal attempted, card failed, retries running; `canceled` = gone. `cancel_at_period_end` is almost never used on web (1 of 1,388): cancels end at once.
- Renewal charges have an `invoice`; intro and upsell charges do not. Split first charges into intro vs upsell by amount.
- Intro amounts: $18.99 (4-week), $6.49 (7-day trial), $39.99 (12-week), $79.99 (1-year, rare), plus "post-timer" full-price firsts ($42.20, $88.40) and exit-offer prices at 20% off ($5.19, $15.19, $31.99). Exit offer = 13% of buyers (Aug 12 to Sep 15). Upsell amounts: $29.99 and $23.99 (audio), $17.49 (guide bundle), $12.99 (single guide), $5.77 and $16.88 (other). 1 in 6 buyers takes an upsell.
- Renewal prices: $42.20 per 4 weeks (98% of paying subs), $14.99 weekly (other funnel or old), $88.40 per 12 weeks (nobody has reached it yet), $129.99 yearly.
- Trial length per plan: 7 days ($6.49), 28 days ($18.99), 84 days ($39.99), 365 (rare). Intro-to-renewal is read per cohort of `trial_end`: active (+past_due) vs canceled.
- Stripe fee: ~2.9% + $0.30 per charge; ~4.3% of gross on this mix. Gross ≈ cash on web.
- Charge metadata (intro charges) carries: `fb_campaign_name`, `fb_adset_name`, `fb_ad_name`, campaign/adset/ad ids in `fb_event_source_url` (utm_campaign, utm_term, utm_content), `fb_fbclid`, `fbp`, `onboarding_version` (funnel slug), `price_id`, `subscription_price_id`, `subscription_trial_days`, `web_user_id`, `customer_user_id` (email). Per-ad attribution on web is deterministic from the ledger.
- Failed charges are numerous (5,712 for "Bible Chat" in 5 weeks): they are renewal retries. Count `status=succeeded` only.
- Web history: Feb to May 2025 attempt (~1.2k subs, ~2% retained), tiny until Aug 10, 2026, then the ramp. Ignore pre-Aug 2026 for rates.
- Reference, Sep 16: paying 1,388; past due 659; in intro 5,600; MRR $64k gross ($94k with past due; ~$300k if the whole queue renewed, which is the investor P&L's reading); Aug cohort intro-to-renewal 35% clean, 50% incl. past due; Aug 12 to 18 cohort 39% within 30 days, $31 per buyer by day 30 ($15 door, $16 renewal).

## Adapty in BigQuery (app route ledger)

- Table `bc-ads-tester.subscription.adapty_realtime` via the `biblechat-analytics` MCP (`execute_query`; browser OAuth via `/mcp` when it drops). Validated queries: `.claude/commands/unit-economics.md`. Gotchas in memory `project_mrr_method.md`.
- `trial_started` carries PHANTOM revenue (~$470k a month). Never sum it. Payment events: subscription_renewed, trial_converted, subscription_started, non_subscription_purchase; refunds are negative rows in subscription_refunded (and non_subscription_purchase_refunded).
- `revenue_usd` = gross. `proceeds_usd` = cash after store cut (~74 to 75%). `net_revenue_usd` and `tax_amount_usd` unusable before Jul 2026.
- Filters: `app_id='biblechat'`, `environment='Production'`, `store != 'stripe'` (18 to 300 Stripe rows exist in Adapty; unrelated to the web route). Dedup on transaction_id (+event_type).
- Lifecycle names: `trial_renewal_cancelled` and `subscription_renewal_cancelled` (auto-renew off), `trial_expired`, `subscription_expired`, `billing_issue_detected`, `entered_grace_period`, `trial_renewal_reactivated`. There is no `trial_cancelled` or `renewal_cancelled`. Auto-renew off during a trial fires on the day the user flips it, so app trials are often "decided" on day 1 or 2.
- Normalized MRR (Query 1): per original_transaction_id, MAX(subscription_expires_at) > now, last paid product and price, not refunded; weekly × 52/12, yearly ÷ 12. Split committed (auto-renew on) vs cancelled-but-active by last lifecycle event.
- Origin: "direct" = no `trial_started` ever for that original_transaction_id. Direct buyers are 36% of subs and 10% of MRR (they buy yearly).
- Spend: `subscription.daily_data`, platforms IOS and ANDROID, channels facebook / tiktok / apple / google (channel sum runs 0.3% under the spend column). WEB rows there are ~$3k and stop Sep 11: web spend is NOT in BigQuery.
- Return curves: `limited.cpt_master_daily` (iOS, per country per day; spend-weight; ROAS columns are GROSS; `predicted_roas_m1` = `realized_roas_30d` once 30+ days old; M12 ≈ 3.1 to 3.4 × M1) and `limited.cpt_master_daily_regions_android` (`row_type='overall'`). `biblechat_cpt_merged` "proceeds_month*" do not behave like cash; prefer Adapty for money.
- `limited.dashboard_daily.purchase_completed` is all zeros. `purchase_completed` in `paywall_events` is a TRIAL START (Meta's "purchases" on the app account are trials).
- MAU: `ga_events_staging` session_start, device level, ~1.2 GB per month queried.
- Trial-to-paid, matured (trials Aug 5 to Sep 5, 2026): iOS 44%, Android 27%, blended 39%. Earlier months read 48 / 27 / 42; August's spend spike bought weaker trials.
- Reference, Sep 16: paying 194k (150k auto-renew on, 44k running out); MRR $2.51M gross / $1.88M cash; iOS 89%; weekly 51% of subs and 82% of MRR; yearly 43% and 12%. 14k in a 7-day trial right now.
- Reference, Aug 12 to Sep 15 (35 days): spend $2.30M (Meta 84%, TikTok 13%, Apple 2%); trials 133k; CPT $17.3 (iOS $21.8, Android $7.4); new payers 64.5k (8.9k direct); CPS $35.6; collected $2.76M gross / $2.07M cash, of which first payments $472k, renewals $2.30M, refunds $18k.
- LTV per iOS trial, Jul 2025 cohort, matured: $22.20 gross / $15.56 cash by month 12; that cohort returned 142% gross on a $15.39 CPT. Projected M12 from the model runs 94 to 98% for 2026 months. The ~112% that circulated in docs has no source.
- Quota: per-person daily BigQuery quota; partition-filter and column-prune everything. Bulk pulls run in a subagent that writes a file (memory `feedback_meta_mcp_via_subagent.md`).

## Meta ad accounts (two)

- Web: "Bible Chat US", act_851055460791534, business BookVitals Inc (3153913884770731). All 37 campaigns in the window are web conversion campaigns named "Biblechat WEB - Conversion IP 5 - IOS - <date> - <buyer>" (buyers Stefan, Arthur). Results metric: `offsite_conversion.fb_pixel_purchase` (pixel 1777679486641648). Read via the `facebook-ads` MCP (`ads_get_ad_entities`, insights; client_conversation_id `Kx7mQ2pR9vT4wY8zA3bC`), in a subagent. Time zone of the account not exposed by the MCP.
- App: "Basmo iOS", act_697155031095732, business Bookvitals APP (173558290375515). Carries both platforms. Optimizes for `purchase_completed` = trial start.
- Reference, Aug 12 to Sep 15, web account: spend $563.0k; pixel purchases 8,807; 4 campaigns carry 71% of spend; 6 above $20k; median campaign $2.8k. Per-ad distribution not yet read.
- Meta's own CPT on the app account reads higher than the blended $17 because it counts only attributed trials.

## Colleague's web P&L page

- `https://adloops.ai/web2app-pnl`, data at `https://adloops.ai/api/web2app-pnl?days=N` (public, no auth; returns `data` rows per date × funnel × platform, `campaignRows`, `funnels` with URLs, `pltv` per scenario). Its window rolls forward daily; its default view may be filtered to one funnel (christian-archetype = 75% of spend).
- Spend = the Meta web account (matches within 0.7%). Purchases = its own purchase feed (8,734 vs Stripe's 8,513 charged cards vs pixel 8,807).
- "Revenue collected" = FIRST purchases only (intro + upsells). Renewals are not on the page. Its "34% collected" is 44% with Stripe renewals added.
- pLTV is a model: footnote says "36.0% surviving the first renewal down to 2.74% at the 12th, i.e. 1.433 renewals". Three scenarios (optimistic, pessimistic, effective; names not ordered as expected). Effective M12 ≈ 134% all funnels, per buyer ≈ $85; M1 per buyer $34 vs measured $31.
- The investor version of the P&L counts web MRR with 100% of the intro queue renewing (~$300k at Sep 16). Ask "charged or assumed?" when a web MRR is quoted.
- Funnels: christian-archetype, bible-study (converts ~2× at the door), marriage, sin, app-funnel. URL pattern `verseread.com/w/b76f73e8-.../en/<slug>/facebook`.
- Colleague said (Sep 15) Stripe will be backfilled into Supabase; not done as of Sep 16.

## Web funnel itself (from the funnel-mapping session)

- Exact prices and screens: `_projects/funnel-maps/data/web-funnel/christian-archetype-pricing.json`, `christian-archetype-screens.json`; write-up in `_docs/core/measurement-map.md`.
- Paywall: 4-Week $18.99 → $42.20 (default), 12-Week $39.99 → $88.40, 1-Week $6.49 trial → $42.20. Countdown timer; post-timer sells at full price. Exit offer = extra 20% off. Upsells after checkout. Then Singular link to the App Store.
- PostHog holds quiz-step analytics; not read yet.

## Cross-source reconciliations that hold (Aug 12 to Sep 15 unless stated)

- Web spend: Meta $563.0k = P&L $558.9k (time zone edge).
- Web entrants: pixel 8,807 ≈ P&L 8,734 ≈ Stripe 8,513 charged customers (3.5% spread).
- Web door money: P&L $191k (its window) = Stripe first charges $193k.
- Stripe monthly creations (Aug 5,578) ≈ P&L new payers (Aug 5,420).
- App M1: `cpt_master_daily` realized_roas_30d (Jul 2026 iOS 31.9%) = Adapty gross (32.4%).

## Definitions used everywhere

- Gross = what the customer pays. Cash = what reaches the bank (app −25%, web −4%). Never on one line.
- Level (a snapshot: subscribers, MRR) vs flow (a window: spend, entrants, collected). MRR is a level; ARR = MRR × 12 is a speed.
- Entrant = trial start (app) or intro purchase (web). Entry decision = trial-to-paid (day 7) or intro-to-renewal (day 7 / 28 / 84 by plan; settled ~3 weeks later after card retries).
- CPS = cost per entrant ÷ entry rate. Web CPS ≈ $160 with $22 already back at the door.
- Leak = pile at start + MRR added − pile at end; ~20% a month on the app; unmeasured on web (assumed 20%).
- Rules: 100% of a month's spend back by month 12, gross (company); ≥ 32% by month 1 (VC). Ceilings: app $22 gross / $16 cash per trial; web ~$85 per buyer on the curve, $64 as the bar until renewal 2 is measured.
- Window convention: end on the last complete day, not today. Current flow window: Aug 12 to Sep 15, 2026, to match the P&L page.

## Open questions (Sep 16)

- Route split of the $5M target (told as web +$2M, iOS +$2M, Android +$1M; sums to the level, not the gap).
- Web leak (renewal 2 and after): first read possible early November.
- Web CPT at 4× scale.
- Per-ad winner size on the web account (ad-level distribution not read).
- Whether the "Bible Chat Premium In App" Stripe product is a live flow.
- App: month-12 ruling (projection 96% vs matured cohort 142%); August spike explanation; Apple payout reconciliation.
