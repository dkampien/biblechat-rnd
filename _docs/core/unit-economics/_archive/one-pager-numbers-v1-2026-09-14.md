---
created: 2026-09-14
archived: 2026-09-17 (superseded by ../04-company-numbers-both-routes.md)
updated: 2026-09-16
---
# BibleChat on one page

App route only (iOS + Android, paying through the stores). Web route is a separate box until its numbers are known. Every money line exists twice: gross is what customers pay, cash is what reaches the bank after the ~25% store cut. Values as of 2026-09-14 unless stated.

```
BIBLECHAT ON ONE PAGE                                App route only · 2026-09-14
====================================================================================

0. STRUCTURE  (what is sold; everything below depends on these four)
------------------------------------------------------------------------------------
Product                               a subscription; in via 7-day free trial or direct purchase
Renewal                               weekly, monthly or yearly; most new subscribers take weekly; weekly = 80% of the money
Rail                                  Apple / Google process every payment and keep ~25%; gross = customer pays, cash = the 75% that arrives
Web route differs                     no free trial (paid intro, then $42.20 per 4 weeks), Stripe rail at ~3%; see F


A. SIZE  (a level, right now)         Value          Basis
------------------------------------------------------------------------------------
Paying subscribers                    199k           snapshot Sep 7          [1]
MRR gross                             $2.55M         snapshot Sep 7
MRR cash                              $1.90M         gross − ~25% store fees [2]
ARR gross / cash                      $30.6M / $22.9M   MRR × 12, a speed not a total
MAU                                   4.2M           August, devices


B. THE LOOP  (a flow, one month)      Jul 2026       Aug 2026       Cost per unit
------------------------------------------------------------------------------------
Ad spend                              $1.25M         $2.08M         .              [3]
Trials                                75k            124k           CPT  $16.6 / $16.7
Direct buys (skip trial)              6k             5k             .              [4]
New subscribers                       36k            52k            CPS  $34.6 / $40.1
Trial to paid, blended                43%            42%            iOS 48% · Android 27%
Revenue that month, gross             $2.22M         $2.34M         .
Revenue that month, cash              $1.65M         $1.75M         .

  CPS = CPT ÷ trial-to-paid.  Ads move CPT; the product moves trial-to-paid.


C. COST vs VALUE  (is the spend allowed)
------------------------------------------------------------------------------------
                                      per trial      per subscriber   Basis
What one costs (Aug)                  $17            $40              spend ÷ count
What one pays back, 30 days           $5.50          $13              gross
What one pays back, 12 months         $22            $52              gross, Jul 2025 cohort
  same, cash                          $16            $38              after store fees
ROAS = value ÷ cost                   32% at M1      ·                129% at M12, gross
Ceiling (ROAS = 100% at M12)          $22 gross      $52 gross        spend above this is
  same, cash break-even               $16            $38              not allowed

Company rule: a month's spend returns 100% within 12 months, gross.
Same rule read at 30 days: M1 ≈ 32%.        Measured M1: Jul 32%, Aug 28% (iOS)
Projected M12 (model):  Jul 98%, Aug 96%    (under the bar, slightly)


D. SPEND CAPACITY  (what the plan needs, and what ads must supply)
------------------------------------------------------------------------------------
Capacity = spend the buyers can deploy at ≤ target CPT without the CPT breaking.
Money is not the constraint; ads that can absorb it are.

Period          Pile at   Leak     Growth   MRR to   New     Trials   CAPACITY NEEDED
                start     (20%)    needed   ADD      subs    (÷42%)   at ≤ $17 CPT
------------------------------------------------------------------------------------
Sep 14–30       $2.55M    $0.28M   $0.38M   $0.66M   37k     87k      $1.5M  (16 days)
October         $2.93M    $0.59M   $0.69M   $1.28M   71k     169k     $2.9M
November        $3.62M    $0.72M   $0.69M   $1.41M   78k     187k     $3.2M
December        $4.31M    $0.86M   $0.69M   $1.55M   86k     205k     $3.5M
------------------------------------------------------------------------------------
Total                                       $4.90M   272k    648k     $11.0M
August, for scale: $2.08M absorbed at $16.7.  December needs 1.7 × August.
Weekly, by December:  ~$800k a week at ≤ $17.

Payback on the whole plan if CPT holds $17 and a trial stays worth $22:
  gross  648k × $22 = $14.3M ÷ $11.0M = 129%   passes the rule
  cash   648k × $16 = $10.4M ÷ $11.0M =  94%   under, in the bank
What bends first: CPT rises as capacity is pushed (Aug: +66% spend, M1 32% → 28%).


E. MY LANE  (automated creative systems)
------------------------------------------------------------------------------------
What I produce                        Spend capacity: budget my ads absorb at ≤ $17
Target                                ____ % of D  →  $______ / month at ≤ $17    [5]
Winner (definition)                   an ad that absorbs ≥ $____ at ≤ $17 before fatigue
Winners per month                     ____
My CPT vs team CPT                    same account, same weeks
Hard stop                             nothing counts above $22, whatever it absorbed
Thresholds come from the Basmo account's own history, not from this page.  [6]


F. WEB ROUTE  (quiz funnel, card payments)      NOT IN A–E · second-hand, unreconciled
------------------------------------------------------------------------------------
Spend                                 $320k (Aug) · Sep pacing ~$450k   colleague's P&L page, reads the WEB Meta account [7]
New payers (intro purchase, ~$19)     5,420 (Aug) · 8,529 since Jun 30       same page; the web twin of B's "new subscribers"
Active subscribers (paying $42.20)    1,636 renewing · 826 past due (card failed)   Stripe, Sep 16; plus 5,870 still inside a paid intro
Intro to renewal (web trial-to-paid)  Aug cohort 35% renewed · 50% incl. past due   Stripe; Sep cohort reads 43% / 65% but is young
MRR                                   $69k gross from renewers (+$34k past due)   Stripe, Sep 16; intro cohort not yet recurring
CPS (per new payer)                   $59 (Aug) · $71 (Sep, CPMs up)         spend ÷ new payers; ~$19 comes back at the door, so net ~$40
Tracked in                            Stripe (money) · WEB Meta account (spend, per-ad funnel; via adloops.ai/web2app-pnl) · PostHog (quiz steps). Not in BigQuery, not in Adapty.
Company MRR = A + F.  Web's share of $5M reduces every row of D by the same share.
No store cut on web: a web paycheck is worth ~1/3 more in cash.


FOOTNOTES
[1] 151k auto-renew on, 47k cancelled but not yet expired.
[2] Gross = what customers pay. Cash = what reaches the bank. Never mix on one line.
[3] Aug: Meta 83%, TikTok 15%, Apple 2%. Peak week $617k (Aug 17), $416k by Aug 31.
[4] Enter the loop at the subscriber row; counted in CPS, not in trial-to-paid.
[5] 10% of October = ~$290k a month at ≤ $17.
[6] Meta's own CPT reads higher than $17: it counts only trials it can attribute.
    Set thresholds from the account's numbers; the $17 here is blended, all channels.
    Leak: pile at start + MRR added − pile at end, over a past window. Aug 16 → Sep 7:
    2.28 + ~0.68 − 2.55 ≈ $0.41M in 22 days ≈ 20%/month, ±5 pts.
    US ≈ 86% of iOS revenue. Split by platform only where shown; never by country here.
[7] adloops.ai/web2app-pnl. Not Stripe. "Second-hand" = read from a colleague's model, not a ledger.
    Stripe rows (Sep 16): read with a restricted key, all 11,491 subscriptions ever. Stripe calls the paid intro a "trial"
    (7 / 28 / 84 days, matching the intro plans), so status trialing = inside intro, active = renewed at full price.
    Stripe's Aug creations (5,578) agree with the P&L's 5,420 new payers.
```
