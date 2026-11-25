---
created: 2026-09-17
updated: 2026-09-17
---
# My share and targets

What the automated creative system is measured on, and the numbers as of Sep 17, 2026. Terms in `01-terms-and-prices.md`, mechanics in `02-how-the-numbers-work.md`, the company chain in `04-plan-chain-goal-to-spend.md`, the facts in `03-company-numbers-both-routes.md`. Nothing here is locked; each section says what is decided and what is not.

## What the share is

Dollars spent on my ads each month, while those ads keep the cost per entrant at or under the route's target.

That is the whole definition. Two parts:

1. **Spend on my ads.** I launch and fund them myself, ad by ad: more on an ad that works, none on one that does not.
2. **The condition.** Cost per entrant at or under target. Above it, the ad is cut and its dollars stop counting.

It is a dollar figure per month, not a percentage and not a count of ads. It is the same unit the buyers are measured in, and it reads straight off the Meta account: filter to my ads, sum the spend, check the cost per entrant.

Hit rate, ads launched, winners per month explain how the number is reached. They are not the target.

## The route

Not locked. Recommendation: **web**.

| | Web | App |
|---|---|---|
| Target cost | ≤ $64 per intro | ≤ $17 per trial |
| Money back at the door | $22 per intro, same day | $0 |
| What a subscriber is worth | $45.70 a month | $18 a month |
| Hard stop | $64 until the second renewal is measured; ~$85 on the model | $22 gross, $16 cash |
| Account | Bible Chat US | Basmo iOS |
| What I can prove | that my intros renew (Stripe carries the ad ids) | only that my trials were cheap |
| Room | the plan asks web for 2× to 4× its current spend | 1.4× |
| Timing | intros bought this month count next month; nothing bought after ~Dec 3 counts for the goal | same month |

Why web: a winner can be proven on value, not only on cost; the shortage of winning ads is largest there; $64 per entrant gives a better ad more dollar leverage than $17. Why not yet: web's month-12 is a model, its cost at scale is unknown, and it runs a month late. Either route works with this file; only the target column changes.

## The floor

Purpose: pay back what I cost the company. Cost: $3,000 a month, about $70k a year with overhead; about $20k inside the plan window, Sep 17 to Dec 31.

**Three framings were tried; only spend holds inside the window.**

| Framing | The bar | Why it does not hold |
|---|---|---|
| Revenue: my intros pay back my cost | revenue from my intros minus spend on my ads ≥ $20k by Dec 31 | cannot close inside the window. An intro bought in October has paid $22 at the door and at most one $42.20 renewal by Dec 31: the $64 it cost, nothing over. The surplus, about $21 per intro, exists only on the 12-month model and arrives in 2027 |
| Intros or MRR from my ads | ~3,300 intros, or ~$55k of MRR added | met trivially by any spend at all, and says nothing about whether the spend was worth it; the count is just the spend divided by $64 |
| Spend at cost | $210k on my ads at ≤ $64 per intro | the unit buyers are judged on; readable from the Meta account every day; a creative source is worth its cost at about 10% of the spend it carries |

The revenue framing is the original purpose and stays true; it is a 2027 read in Stripe, not a Dec 31 one.

**Floor: $210k of spend on my ads between Sep 17 and Dec 31, at or under $64 per intro. $60k a month.**

Same clock as the plan in `04-plan-chain-goal-to-spend.md`:

| | Per month | Sep 17 to Dec 31 |
|---|---|---|
| My cost | $5.8k | $20k |
| Spend floor at ≤ $64 | $60k | $210k |
| Intros that buys | ~940 | ~3,300 |
| Money back at the door | ~$20k | ~$72k |
| Renewals collected inside the window | $0 the first month, then ~$16k a month | ~$40k |
| MRR added by Dec 31 | ~$17k a month | ~$55k |

**As a percentage, for reference only.** The dollars are the target. The percentage is what the dollars happen to be against whatever is actually spent; the denominator moves, the target does not. Planned and simulated spend is not real spend.

| $210k against | Total, Sep 17 to Dec 31 | Share |
|---|---|---|
| net spend if web carried the whole goal (plan, simulated) | $11.2M | 1.9% |
| gross spend in that scenario (plan, simulated) | $17.0M | 1.2% |
| web's spend at today's pace (actual, projected) | $1.75M | 12% |
| company's spend at today's pace, both routes (actual, projected) | $8.75M | 2.4% |

Re-read the shares on Jan 1 against what was actually spent.

## Phase 1: Sep 17 to Oct 31, calibration

- Target: $60k a month at ≤ $64 per intro, web.
- Winner: an ad that carries ≥ $10k at ≤ $64 before fatigue, and whose intros renew at ≥ 35% read from Stripe at day 30 or later. The $10k is read from campaign sizes on the web account (4 campaigns carry 71% of spend, 6 above $20k, median $2.8k) and needs one ad-level read before it is fixed.
- Record, do not target: ads launched, hit rate, spend per winner, renewal rate per winner, plan mix per winner.
- Do not touch the target for six weeks.

## Phase 2: from Nov 1

Replace the borrowed numbers with mine and restate the share against the gap: capacity the plan needs on my route minus what the buyers supply, times what my measured hit rate and winner size can carry. That line goes into `04_mandate.md` Objectives when phase 1 closes.

## Two things to do now

1. Fix the phase-1 number above and leave it alone.
2. On the 1st of each month, read three numbers: spend on my ads and cost per intro from the Meta account; renewals of my intros from Stripe. If spend is at $60k and cost under $64, raise the target. If not, the ads are the problem, not the plan.

Two questions were struck on Sep 17: the buyers' testing pipe is not a constraint (I launch and fund my own ads), and the web / iOS / Android split is a race, not a per-team target.

## The leaderboard

The buyers' own number is the same unit. Stefan's largest campaign carried $146k in five weeks at about $56 per intro. That is the ceiling seen in this account so far; the floor above is about a tenth of it per month.

## Open

- Route: recommended web, not locked.
- The $10k winner bar: campaign-level proxy, needs the ad-level distribution.
- Web second renewal: unmeasured until early November; it moves the hard stop.
- The route split of the $5M: not a target, a race between teams (per Denis, Sep 17); it changes the room, not the definition.
