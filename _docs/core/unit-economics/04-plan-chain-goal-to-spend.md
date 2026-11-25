---
created: 2026-09-17
updated: 2026-09-17
---
# The plan chain, from the goal down to spend

The arithmetic that turns the company goal into ad spend. Terms in `01-terms-and-prices.md`, the reasons behind each step in `02-how-the-numbers-work.md`, the facts in `03-company-numbers-both-routes.md`. Numbers dated Sep 17, 2026; re-run them, the chain does not change.

## The order

```
company goal  ->  per route  ->  my share
```

1. **Company.** Goal, pile, gap, leak, MRR to add, month by month to December. One set of numbers, whichever route does the work.
2. **Per route.** The company table run through each route as if it added all of it, month by month. No split needed; the two tables bracket the real cost.
3. **My share.** A slice of the picked route's spend column. In `05-my-share-and-targets.md`.

## The ladder

The chain is a ladder with MRR at the top rung and ad spend at the bottom. Between them, three rungs: subscribers, entrants, spend. Each step down divides or multiplies by a rate.

The rates are not part of the ladder; they are borrowed from the past. Each one is read from a window that already happened: $64 per intro from the last five weeks of the Meta account and Stripe, 40% from the August cohorts, 20% leak from three weeks of Adapty. The ladder carries them forward. When a window is re-read, the rate changes and the ladder is re-run; the rungs stay.

Two ways to climb. Planning runs down: start at the MRR you need, end at the spend. Explaining runs up: start at the spend, end at the MRR it produced. Same rungs, same rates.

## Step 1. Company: from the goal to MRR to add

| # | Line | Sep 17, 2026 |
|---|---|---|
| 1 | Goal | $5.00M MRR on Dec 31 |
| 2 | Pile now | $2.57M (app $2.51M + web $0.06M) |
| 3 | Gap = goal − pile | $2.43M |
| 4 | Time left | 106 days, 3.5 months |
| 5 | Growth per month = gap ÷ months | $0.69M per 30 days (a 31-day month gets $0.71M) |
| 6 | Leak rate | 20% of the pile per month (one app read, Aug 16 to Sep 7, ±5 pts; assumed on web). The CTO puts it higher. Re-measure on the 1st of each month; at 25% the total to add is $5.5M, at 30% $6.1M |
| 7 | Leak this month = pile at start × 20% | October: $2.89M × 20% = $0.60M |
| 8 | MRR to add = leak + growth | October: $0.60M + $0.71M = $1.31M |

Rolled forward, the pile grows, so the leak grows, so each month asks for more:

| Step | Sep 17–30 | Oct | Nov | Dec | Total |
|---|---|---|---|---|---|
| Pile at start | $2.57M | $2.89M | $3.60M | $4.29M | |
| × 20% = leak to refill | $0.24M | $0.60M | $0.72M | $0.89M | $2.44M |
| + growth (gap ÷ months left) | $0.32M | $0.71M | $0.69M | $0.71M | $2.43M |
| = MRR to add | $0.56M | $1.31M | $1.41M | $1.60M | $4.87M |

Half of everything added goes to refilling the leak. That is the plan's hidden cost.

## Step 2. Per route: from MRR to add down to spend

Three divisions and one multiplication. The four inputs are the only things that can be wrong.

| # | Line | App | Web |
|---|---|---|---|
| 9 | Subscribers = MRR to add ÷ MRR per subscriber | ÷ $18 | ÷ $45.70 |
| 10 | Entrants = subscribers ÷ entry rate | ÷ 39% (trial-to-paid) | ÷ 40% (intro-to-renewal) |
| 11 | Spend = entrants × cost per entrant | × $17.3 per trial | × $64 per intro |
| 12 | Door money back = entrants × paid on day 0 | × $0 | × $22 |
| 13 | Net spend = spend − door money | = spend | spend − 12 |
| 14 | When it lands in the pile | same month (7 days) | next month (28 days) |

**Month by month, each route as if it added all of it.** No split needed; the company table from Step 1 run through one route at a time. Neither will happen as written; each is the whole plan carried by one route, and the two bracket the real cost.

Every column is one month read top to bottom. A subscriber is a person making the full-price payment after the intro (the second payment, $42.20 on web), not the intro payment.

Web, if it added all of it:

| Step | Sep 17–30 | Oct | Nov | Dec | Total |
|---|---|---|---|---|---|
| MRR to add | $0.56M | $1.31M | $1.41M | $1.60M | $4.87M |
| ÷ $45.70 per subscriber = subscribers | 12k | 29k | 31k | 35k | 107k |
| ÷ 40% renew = intros (bought the month before) | 31k | 72k | 77k | 88k | 266k |
| × $64 per intro = spend | $2.0M | $4.6M | $4.9M | $5.6M | $17.0M |
| − $22 per intro = door money back | $0.7M | $1.6M | $1.7M | $1.9M | $5.9M |
| = net spend | $1.3M | $3.0M | $3.2M | $3.7M | $11.2M |

App, if it added all of it:

| Step | Sep 17–30 | Oct | Nov | Dec | Total |
|---|---|---|---|---|---|
| MRR to add | $0.56M | $1.31M | $1.41M | $1.60M | $4.87M |
| ÷ $18 per subscriber = subscribers | 31k | 73k | 78k | 89k | 271k |
| ÷ 39% convert = trials (same month) | 80k | 187k | 201k | 228k | 696k |
| × $17.3 per trial = spend, net (nothing back at the door) | $1.4M | $3.2M | $3.5M | $3.9M | $12.0M |

Same net cost within 10%. The routes differ in who and when, not in how much. Once a route is picked, its table is the month-by-month reference; a share is a slice of its spend column.

## What the total means

The real cost lands between the two tables above: about $11M to $12M net by Dec 31 whichever route does the work, about $3.5M a month against $2.5M a month today. Today's spend mix, read from the two ad accounts, is about 80% app and 20% web; at that mix the app must run about 1.4x its current spend and web about 2x. The mix is a reading, not a decision; the teams race, and whoever gets furthest wins.

## The four inputs

Everything above is these four, run through the chain. Check these, not the cells.

| Input | App | Web | Where it comes from |
|---|---|---|---|
| MRR per new subscriber | $18 | $45.70 | prices and plan mix |
| Entry rate | 39% | 40% (range 35 to 45) | app: BigQuery, matured cohort · web: Stripe, Aug cohort 35% clean / 50% with recoveries, Aug 12–18 cohort 39% at day 30; next read Sep 24. At 35% October's web spend is $5.3M, at 45% $4.1M |
| Cost per entrant | $17.3 | $64 | app: BigQuery spend ÷ Adapty trials · web: Meta account ÷ Stripe intros |
| Leak per month | 20% | 20% assumed | app: measured · web: first read early November |

## Two checks that catch most mistakes

- Subscribers × MRR per subscriber must give back the MRR to add.
- If a month's spend is more than 1.5× what that route spent last month, the number is a scale-up question for the buyers, not a budget line.

## What is not in this file

Your own target inside this spend: `05-my-share-and-targets.md`. Per-route monthly tables at a split: dropped on Sep 17; the split is a reading, not a decision, and the two 100% tables bracket the cost.
