---
created: 2026-09-16
updated: 2026-09-17
---
# BibleChat on one page, v2: both routes

App route (iOS + Android, paying through the stores) and web route (verseread.com quiz, paying through Stripe) as columns, same rows. Levels are read on Sep 16, 2026. Flows are the window Aug 12 to Sep 15, 2026, 35 complete days, the same window as the colleague's P&L page. Gross = what the customer pays; cash = what reaches the bank. Web numbers describe five weeks of a route that ramped on Aug 10; app numbers describe five weeks of a route in steady state. v1 (app only, Sep 14) is in `_archive/`.

```
BIBLECHAT ON ONE PAGE, v2                                   levels Sep 16 · flows Aug 12–Sep 15
=========================================================================================================

0. STRUCTURE  (what is sold)          App                                  Web
---------------------------------------------------------------------------------------------------------
Product                               a subscription; in via 7-day free    a subscription; in via a paid intro:
                                      trial or direct purchase             $18.99 / 4 wk (default), $39.99 / 12 wk,
                                                                           or $6.49 for a 7-day paid trial. No free trial
Renewal                               weekly $4.99, monthly $12.99,        $42.20 per 4 weeks (default), $88.40 per
                                      yearly $39.99 (US store); weekly     12 weeks; the 7-day trial renews onto $42.20
                                      = 82% of the money
Rail                                  Apple / Google keep ~25%             Stripe keeps ~3% + 30¢; gross ≈ cash
Cancel                                auto-renew off, runs to period end   ends at once
Upsells                               none                                 one-off at checkout: audio $29.99 (or $23.99),
                                                                           guide bundle $17.49; 1 in 6 intros takes one
Exit offer                            none                                 leave the page: 20% off the intro; 13% of
                                                                           intros pay that price
Ledger                                Adapty (mirrors the stores), in      Stripe only. Not in BigQuery, not in Adapty.
                                      BigQuery                             Every intro charge carries the ad's ids [1]
The same app is sold on both routes; web sends the entrant into the app after checkout.


A. SIZE  (a level, Sep 16)            App                 Web                 Basis
---------------------------------------------------------------------------------------------------------
Paying subscribers                    194k                1,388               app: active, not refunded · web: status active
MRR gross · cash                      $2.51M · $1.88M     $64k · $62k         each price normalised to a month
ARR gross · cash                      $30.1M · $22.6M     $770k · $740k       MRR × 12: a speed, not a total
  by platform                         iOS 89% · Android 11%   ·               web has no platform
  by plan                             weekly 51% of subs, 82% of MRR;     4-week $42.20: 98% of subs and MRR;
                                      yearly 43% · 12%; monthly 7% · 6%   12-week: none renewed yet
  by origin                           via trial 64% of subs, 90% of MRR;  via $6.49 7-day trial 77%, via $18.99
                                      direct 36% · 10%                    4-week intro 23% (maturity artifact) [2]
Undecided entrants                    14k in a 7-day trial 5,600 in a paid intro   the queue that feeds the pile
  web MRR if the queue renews at 100%  ·                   ~$300k              the investor P&L's reading; at the measured ~40%
                                                                              it is ~$160k; charged so far $64k (the row above)
Cancelled, running out                44k                 ·                   web cancels end at once
Past due (card failed)                ·                   659                 stores retry silently
Company MRR gross · cash              $2.57M · $1.94M                         app + web; web is 2.5%


B. THE LOOP  (a flow, 35 days)        App                 Web                 Basis
---------------------------------------------------------------------------------------------------------
Ad spend                              $2.30M              $563k               BigQuery (Meta 84%, TikTok 13%, Apple 2%) ·
                                                                              Meta WEB account; P&L page reads the same [3]
Entrants  (trial · intro purchase)    133k                8.5k                Adapty · Stripe paying customers (pixel: 8.8k)
Cost per entrant  (CPT · per intro)   $17.3               $64                 iOS $21.8, Android $7.4 · one price
Money at the door                     $0                  $189k               web: $153k intros + $36k upsells = $22 / entrant
Entry decision                        39%                 35% to 50%          app: trial-to-paid, Aug 5–Sep 5 trials, matured ·
  (trial-to-paid · intro-to-renewal)                                          web: Aug 12–18 cohort, past-due still settling
New subscribers                       64.5k               ~3.4k expected      app: 55.6k from trials + 8.9k direct ·
                                                                              web: 8.5k × ~40%, most not yet due
Cost per subscriber  (CPS)            $35.6               ~$160               spend ÷ payers · web: $64 ÷ 40%, $22 of it
                                                                              already back at the door
First payments collected, gross       $472k               $189k               app: first price after trial + direct · web: the door
Renewals collected, gross             $2.30M              $58k                app: whole base · web: 1,366 people, renewal 1
Refunds                               $18k                $1.3k
Collected, gross · cash               $2.76M · $2.07M     $247k · $235k       app −25% stores · web −4% Stripe
Collected ÷ spend, first payments     21%                 34%                 the fair comparison for a young route
Collected ÷ spend, everything         120%                44%                 app's mature base renewing; not comparable

  CPS = cost per entrant ÷ entry rate. Ads move cost per entrant; the product moves the entry rate.
  The P&L page's "revenue collected" is the door only ($191k for its window); renewals are not on it.


C. COST vs VALUE  (per entrant)       App (per trial)     Web (per intro)     Basis
---------------------------------------------------------------------------------------------------------
What one costs                        $17.3               $64                 row B
What one pays back by day 30          $5.50               $31                 app: M1 32% × CPT · web: Aug 12–18 cohort, measured
  of which at the door                $0                  $15                 that cohort was 40% on the $6.49 plan
  of which first renewal              $5.50               $16                 web: 39% renewed × $42.20
ROAS at day 30                        32% Jul · 28% Aug   49%                 value ÷ cost; web cohort's own CPT ~$60
What one pays back by month 12        $22 · cash $16      ~$85 MODELED        app: Jul 2025 cohort, measured · web: colleague's
                                                                              curve (36% renew once, 1.43 renewals by the 12th) [4]
ROAS at month 12                      129% measured,      ~133% modeled
                                      96% projected
Ceiling (spend per entrant at         $22 gross · $16 cash   ~$85 gross · ~$82 cash   web: only as good as the curve; at 25%
  M12 = 100%)                                                                 second renewal the ceiling meets today's $64

Company rule: a month's spend returns 100% within 12 months, gross.  VC rule: at least 32% at month 1.
Web pays back faster (door money); its month-12 is a forecast, the app's is a fact.


D. SPEND CAPACITY  (what +$1M of MRR by Dec 31 costs)   App          Web          Basis
---------------------------------------------------------------------------------------------------------
MRR to add, incl. leak                                  ~$2.0M       ~$2.0M       2× growth over 3.5 months at 20% leak; web leak ASSUMED
MRR per new full-price payer                            $18          $45.70
Full-price payers needed                                111k         44k
Entrants needed                                         285k         110k         ÷ 39% · ÷ 40%
Spend needed, gross                                     $4.9M        $7.0M        × $17.3 · × $64
  minus money at the door                               $0           −$2.4M       web: $22 × 110k
Spend needed, net                                       $4.9M        $4.6M
Per month, on top of today's run rate                   +$1.4M/mo    +$2.0M/mo    per $1M of MRR growth; today: app $2.0M/mo · web $0.5M/mo
Scale-up at today's spend mix (~80/20, a reading)       1.4×         2×           app +$0.8M/mo, web +$0.5M/mo; the constraint, not the money

Dated Sep 16: 106 days left. Company pile $2.57M, target $5.00M, gap $2.43M ≈ 2.4 of the units above.
Web runs one month early: an intro bought in October renews in November; December's intros do not count.
This block is the compressed unit (per $1M of MRR growth). The month-by-month tables, each route as if it added all of it, are in `04-plan-chain-goal-to-spend.md`, Step 2 (the Sep 16 worksheet is in `_archive/`).


E. MY LANE  (automated creative systems)   moved to `05-my-share-and-targets.md` (2026-09-17)


FOOTNOTES
[1] Stripe charge metadata holds fb campaign, ad set and ad names and ids, the click id, funnel version and price id.
    Per-ad attribution on web is deterministic in the ledger; on the app it ends at trial start (SKAdNetwork).
[2] 7-day intros reach renewal four times sooner than 28-day ones, so they dominate the paying pile today.
    Of everyone who entered on 7-day terms, 32% pay full price now; 28-day cohorts are only arriving.
[3] Three sources for web spend agree: Meta account $563.0k, P&L page $558.9k (time zone edge), 37 campaigns,
    all web conversion campaigns. Intros: pixel 8,807 · page 8,734 · Stripe 8,513 (charged cards).
    Web spend is absent from BigQuery (only $3k of WEB rows there).
[5] Campaign level, not ad level; the per-ad winner size is below the campaign size. Read the ad-level
    distribution from the account before fixing the $10k bar.
[4] From the P&L page's footnote, an assumption typed into the model, not a measurement. The first measured
    cohort (Aug 12–18, 1,062 intros) did $31 by day 30 against the model's $34.

OPEN
- Route split of the $5M: not a target; the teams race and whoever gets furthest wins (per Denis, Sep 17).
- Web leak (second renewal and after): unobserved. First read possible early November.
- Web CPT at 4× scale: unknown.
- Intro-to-renewal per cohort: Aug 12–18 settles ~Oct 1; Aug 19–25 day-30 closes Sep 24 (cleaner plan mix).
- Stripe account is shared with Sam Bedtime Stories and old Bible Chat web products; every web row above is the "Bible Chat" product only.
```
