---
created: 2026-08-10
updated: 2026-09-15 (WEB route from the funnel's own config and payments code; APP route middle from the internal builder; CPP inventory linked; purchase_completed resolved as the trial start via Graph API; two open questions added on landing page views and Apple campaign tokens; Stripe ledger facts added 2026-09-16)
---

# Measurement map: what Meta sees of our business

The company's measurement reality as actually observed in Meta (Events
Manager and Ads Manager, early August 2026). Every claim is tagged:

- **[seen]** read directly off a Meta screen or API
- **[inferred]** a best reading of the evidence, unconfirmed
- **[unknown]** nobody has looked yet; treat as blank, not as false

## Ad accounts (there are two)

[via Denis + a live API survey, 2026-08-17] The company runs TWO Meta ad
accounts:

- **Basmo IOS** (`697155031095732`): the app-route account, and the one all
  observations in this doc come from. ~70 CPT campaigns (the active
  majority), ~50 CPI campaigns (mostly paused tests), ~30 WEB campaigns
  (all paused but one). "EU" in its naming is the billing entity, not the
  audience: active campaigns target US, AU, CA/NZ, PH, LATAM, BR, WW,
  Android included.
- **A separate WEB account**: runs the live web quiz funnels. No internal
  access as of this writing; nothing in this doc describes it. The web-route
  numbers below came from Basmo IOS's own (now mostly paused) web campaigns.

Consequence: any number's "world" is defined by account + route +
optimization event + attribution window. Record all four before comparing
anything to anything.

## Datasets (where events arrive)

[seen] Three alive, rest is dead wiring:

| dataset | what it is | volume (28d) | trust level |
|---|---|---|---|
| Bible Chat Web | quiz funnel on verseread.com, Pixel + Conversions API | ~73K events | observed truth (fires on our pages) |
| Bible Chat App | in-app events via Mobile Measurement Partner + SDK | ~158M events | modeled truth (MMP attribution windows, iOS privacy modeling) |
| underline.link Pixel | small, alive | ~2K events | [unknown] what rides through it |

[seen] Dead/empty: legacy "BibleChat Pixel", "Web2App Funnels", "AdLoops.ai",
"Basmo" datasets. The Get.Basmo.App pixel (other product) flatlined
mid-July 2026.

[seen] Web dataset event match quality is 6.1/10, "update recommended":
events carry too few user identifiers, some attribution is silently lost.
Fix belongs to whoever owns the funnel code.

## Event vocabulary

**Web route** [seen]: every quiz step is a custom event. 28d counts:
PageView 18.2K -> answer_gender 6.6K -> answer_age / gender_pick ~6.4K ->
answer_lifeChallenge 4.3K -> answer_loader_q1..q3 ~4K -> Complete
registration 2.7K. The web dataset ends at registration: no checkout,
trial, or purchase events fire from the website.

Notable [seen]: the biggest single drop is PageView -> first quiz answer
(about 64% never answer question one). After question one, most finish.

**App purchase micro-funnel** [seen], 28d, all users worldwide (organic
included, NOT ad performance): purchase_started 591K -> purchase_completed
131K, with purchase_cancelled 258K and purchase_error 15K along the way.
Restore events (reinstalls) exist separately.

**Two money events coexist** [seen], resolved 2026-09-15 [seen via Graph
API]: custom purchase_completed (131K) and standard Purchase (48K) are the
SAME moment, the first transaction (trial start, plus a ~4% direct-buy
tail), read by two sensors. purchase_completed is the app's own event, sent
with custom_event_type OTHER (Meta was never told it is a trial); standard
Purchase is the iOS SDK logging the StoreKit transaction, iOS only, ~72%
coverage, $2.17 average value (a $0 trial, not a price), moving day-for-day
with purchase_completed and never lagging it. The account fires no
StartTrial or Subscribe event at all. Consequence: Cost per result on a CPT
row IS cost per trial (28d account-wide $18.19 vs the documented CPT $16.6
to 17), and the per-trial ceiling ($22 gross, $16 cash) applies to it.
Write-up: `_projects/funnel-maps/data/readings/app/purchase_completed-check_2026-09-15.md`.

**Trial events**: the datasets read here showed none, but the 2026-08-17
survey found WEB campaigns configured against pixel events including a
"Start Trial" [via survey]. Likely it lives in the WEB account's dataset,
never inspected. So "no trial event" is true only of the datasets listed
above, not of the company. The live web funnel's default plan is a paid
intro, but a 1-Week Plan with `trialDays: 7` is on its paywall (see routes),
so a trial event on the WEB account is plausible for that plan; which pixel
event it maps to is [unknown].

**App events between install and purchase** (onboarding, any in-app
registration): not in Meta's datasets as read; the onboarding screens are now
known from the builder (see routes), their event names are not.
"Registration" is a web-route term (email capture); the app's equivalent is
the sign-in gate on page 1.

## The routes (user journeys as evidenced)

```
WEB route:          ad click -> quiz -> email capture (= Complete registration)
                    -> results + paywall -> Stripe checkout (paid intro)
                    -> create account -> upsells -> App Store (Singular link)
                    -> install -> sign in with the paid email -> ??? (in-app)
APP route (CPI/CPT): ad click (optional deeplink intent) -> App Store custom
                    product page (one of 66) -> install (MMP) -> sign-in gate
                    -> notification permission -> personalization (branching)
                    -> optional trial pre-sell -> paywall (dismissible for most)
                    -> 7-day trial | direct purchase | web checkout (2 rule sets)
                    -> paid (IAP, or Stripe when routed to web)
```

**WEB route, screen by screen** [seen 2026-09-14/15, christian-archetype
funnel on verseread.com; order read from the page's own screen config
(`window.__obScreens`, 41 screens, `postPurchase` list) and its payments
script, not guessed from the copy]:

1. Quiz: gender, age, welcome, 22 more choice screens with three "break"
   interstitials, then "analyzed" and a reveal loader.
2. Email capture ("Where should we send your results?"), skippable, then
   first name. Pixel: CompleteRegistration. This is the registration
   checkpoint.
3. Card stack, then the paywall (`pricing`): countdown, promo code, three
   plans served per session by `/api/funnel/v1/session/init`:
   - 1-Week Plan: $6.49, `trialDays: 7`, then $42.20 every 4 weeks
     (the code treats it as a trial: card saved via setup-intent; whether
     the $6.49 is charged at once is [inferred, unclear])
   - 4-Week Plan: $18.99, then $42.20 every 4 weeks (featured, "MOST POPULAR")
   - 12-Week Plan: $39.99, then $88.40 every 12 weeks
   No free plan. The featured path is a paid intro, so "no trial" holds
   for the default choice, but a 7-day trial plan is on the menu.
4. Checkout (Stripe, Apple Pay / Google Pay / card). On success the page
   fires pixel `Purchase` with the amount (and PostHog `purchase_completed`,
   or `trial_started` for the 1-week plan, in which case no Purchase pixel
   fires because the amount is 0) [seen in code].
5. Post-purchase, in this order: **create account** ("Almost there!",
   then "Your account created!"), upsell Audio Mode $29.99, a 20% save
   screen, Audio Mode $23.99, guides bundle $17.49, then **handoff**.
6. Handoff: "Your plan is ready in Bible Chat". Go to App Store via a
   Singular link (`biblechatdaily.sng.link/Eryen/hfap`, iOS redirect to
   app id 6448849666, Android referrer utm_source=facebook). Or manual:
   download, open, "I have an account", sign in with the paid email. The
   download click fires CompleteRegistration a second time [seen in code].
7. Exit offer screen exists for people who bail at checkout.

Pixel: this funnel fires to Meta pixel **1358749622795508**, not the
"Bible Chat Web" dataset (1015386208074903) read in Events Manager. That
is why that dataset shows no purchase events: the live funnel reports to a
different pixel, almost certainly the WEB account's. Analytics also go to
PostHog and GA4 (G-674S39901Q). Attribution to the app: Singular link on
the handoff button; an install from that opened store page matches, a
later install by search does not [via Denis, plausible].

Consequences: a web buyer is a paying subscriber at checkout, on a 4-week
product over card rails (Stripe, no store cut). There is normally no
trial-to-paid step (only if the 1-week plan is picked). "Registration"
means email capture here and comes before payment; the account is created
right after payment, before the upsells. The customer join to the app is
the email, not the MMP. The app route's in-app middle is still [unknown].

**APP route, screen by screen** [seen 2026-09-15 in the internal builder,
read-only; full tree in `app-onboarding-map.md`]. The builder stores every
onboarding page, paywall and pricing rule and serves them to the app as JSON
at launch. Which onboarding is LIVE could not be confirmed (the placement
table is not readable with Denis's access); the most recently published one
("V6.6 PE FL - Name Personalized Paywall + paywall swap horizon", 24 pages,
3 chapters, updated 2026-09-14) is the proxy. Every page number is "this
flow", not "the flow every user gets".

1. Ad click. The ad may carry a deeplink intent
   (`biblechatapp://override-signals/...`) that routes the install into a
   sibling onboarding: marriage, parenting, catholics, man_quiz, woman_quiz,
   audio_bible_study, animated_bible_stories. So the CPP theme and the
   onboarding theme can be paired per ad. This is the app route's
   "instance" level, like the five web funnels.
2. App Store custom product page: 66 exist, 64 live, listed in
   `destinations-inventory.md`. Which ad points at which page: [unknown].
3. Install. MMP (Singular) attributes it; app dataset in Meta is modeled.
4. Page 1: feature carousel with Apple/Google sign-in [ACCOUNT]. Web buyers
   tap "I have an account" here; whether that skips the rest: [inferred yes].
5. Page 2: reviews. Page 3: notification permission [PERMISSION].
6. Pages 4 to ~20: personalization. Branches on 6 in-flow answers
   (motivation, promise, age, gender, denomination, preferred feature),
   3 device/account states (name known, already premium, intro-offer
   eligible), 4 outside variables (deeplink intent, lifecycle segment,
   country/language, platform/version). Roughly 24 page sequences times
   ~20 copy tracks. Loaders and a name input sit in here.
7. Trial pre-sell: conditional. Teens, already-premium users, and anyone not
   intro-offer eligible skip it and see a paywall with no trial framing.
8. Page 24: paywall. Adapty placement `all-products`, template
   trial-vs-direct, products `biblechat.pro.weekly` ($4.99/wk shown) and
   `biblechat.pro.yearly.discount1`; 7-day free trial or direct purchase.
   Dismissible for most users (hard paywall only for 45+ in some rule
   sets), so onboarding can end with no purchase decision.
9. Purchase rails: Apple/Google IAP by default; two rule sets
   (`bc-app2web-v1`) send the purchase to a web checkout instead, off store
   rails. Adapty mirrors the store receipts only.
10. After purchase / after dismissal: [unknown].

Sensors on the app route: the builder holds no analytics event names (its
`list_app_events` are Apple In-App Events, the store promo cards). The
purchase micro-funnel above (purchase_started -> completed) is the only
in-app sensor read so far; onboarding step events, paywall_shown and
trial_started live in the analytics stack: [unknown until BigQuery is read].

Money enters BEFORE install on the WEB route and after install on the app
route (IAP, ~26% blended store cut). The old instrumentation puzzle (web
dataset fires no purchase events) is resolved: the live funnel reports to
pixel 1358749622795508, a dataset never opened from Basmo IOS. The
colleague's web P&L (adloops.ai/web2app-pnl) remains the only web money
ledger seen.

## Campaign families (Arthur's naming tokens)

Tokens name the KPI each campaign is judged by; the KPI implies the
optimization goal (an ad set setting), which implies the rest:

| token | objective / optimization [via survey 2026-08-17] | attribution | destination | KPI |
|---|---|---|---|---|
| WEB | OUTCOME_SALES/LEADS on pixel events (Complete Registration, Start Trial, "Conversion IP 5") | 7d click + 1d view | quiz page (defaults to onboardings.thebiblechat.com) | cost per registration |
| CPI | APP_INSTALLS, install-optimized | 1d click | store listing | cost per install |
| CPT | APP_INSTALLS objective with app-event optimization (AEO); Cost per result showed purchase_completed [seen] | 7d click | store listing | cost per "trial" |

Attribution windows DIFFER between families, so cross-family cost
comparisons are doubly unfair. Known conflict on record: AdLoops code
convention says CPT = 1d click, live adsets say 7d click; live wins until
someone reconciles. Another conflict: a "targeting starts 35+" note from
Denis vs live adsets at 18-65/20-65.

Other tokens [seen]: CBO = campaign-level budget (Meta redistributes across
ad sets; keep OFF for experiments), Statics = static image creatives.

## Reading Ads Manager without fooling yourself

- A blank column is not a leak. Ask first: does a matching event exist in
  the account at all, and can THIS campaign's destination fire it? (Trial
  columns fail the first test; registration columns on app campaigns fail
  the second.)
- Never read one column down across both funnel families. Identify the
  row's family first; the blank-pattern is the signature.
- "Results" / "Cost per result" adapt to each row's optimization goal
  (fine print says which). Good for scanning mixed rows, never comparable
  across rows with different goals.
- Events Manager shows the whole pipe (all users, organic included); Ads
  Manager shows the ad-attributed slice. Never compare their magnitudes.
- Day-0 purchase ROAS on a subscription app is structurally tiny and near
  meaningless; the judge of acquisition cost is LTV, which Meta cannot see.
- Column setup in use: two presets ("Funnel LTR - web" with LP/registration
  seams, "Funnel LTR - app" with install + purchase seams) wired into two
  views filtered by campaign name token, plus the unfiltered tab for the
  pulse scan. Presets and views are personal to the login; custom metrics
  are the only shareable piece.

Economics context (targets, mo12 return, store fees) lives in
`01_biblechat-business-overview.md` next to this doc; this doc stays about
what Meta measures. The drawn versions (funnel bands, the two ad views, the
column ladder) and their artifact URLs are in `funnel-maps/README.md`.

**Web ledger, read from Stripe 2026-09-16** [via the unit-economics session,
restricted read key registered as MCP server `stripe`]: the exit offer is an
additional 20% off the intro (charges at $5.19 / $15.19 / $31.99 beside
$6.49 / $18.99 / $39.99); 13% of intro purchases Aug 12 to Sep 15 were at the
exit price. Upsells in the same window: 1,403 charges on 8,533 intros (Audio
$29.99 x677, $23.99 x405, bundle $17.49 x96), about $36k. No 30-day refund
rule is visible in Stripe; refunds in the window $1.3k on $247k gross.
**Every web intro charge carries Meta campaign, ad set and ad names and ids,
fbclid, onboarding_version and price_id in its metadata**, so per-ad
attribution on the web route is deterministic in the ledger, and web cohorts
(renewals, refunds, upsells) can be read per ad. This is the opposite of the
app route, whose ledger carries no Meta key.

## Open questions (the Arthur pile)

1. ~~purchase_completed vs standard Purchase~~ resolved 2026-09-15: one
   moment (trial start), two sensors; see "Two money events coexist".
   Confirmed in BigQuery 2026-09-15: iOS first transactions 11,625 that week vs
   the app's own purchase_completed 11,107 (96%); paid conversions 7,681. No Meta
   ad-set key exists in the billing ledger, so the check holds per route only.
2. What is CPT's target number? (Its mechanics are now known: AEO app-event
   campaigns, 7d click.)
3. Event match quality 6.1/10 on the web dataset: who owns the fix?
4. Which onboarding is live per platform (placement feature defaults, not
   readable with current access), and what fires per onboarding step.
5. What rides through the underline.link pixel?
6. Open the dataset behind pixel 1358749622795508 (WEB account) and read
   its Purchase / CompleteRegistration counts; note CompleteRegistration
   fires twice per buyer (email + download click).
7. Who has access to the WEB account, and can we get read access?
8. 35+ targeting note vs live 18-65 adsets: which is policy?
9. CPT attribution: reconcile AdLoops' 1d-click convention with the live
   7d-click adsets.
10. Landing page views on app rows: every app ad set shows 1 to 8% of link
   clicks as landing page views (median 2.5%, read across 218 ad sets on
   2026-09-15) although the destination is the App Store. Mechanism unknown
   (a web step before the store? a placement quirk? a recent change?). Ask
   the account owner. The ladder and scan flag it only above 10%.
11. Apple campaign tokens: no ad carries one (2026-09-15 read of 544 store
   URLs). The product page is set on the creative (`app_product_page_id`),
   Meta builds the link. Test on one ad set whether a `ct=` token can ride
   along; if yes, App Store Connect analytics reports page views and downloads
   per token, lighting the store-page-to-install seam per pool.

