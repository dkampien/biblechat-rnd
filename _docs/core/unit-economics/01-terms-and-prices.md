---
created: 2026-09-17
updated: 2026-09-17
---
# The words

The terms every numbers file uses. Read this first. No links out; everything else links here.

## The people

| Word | Means | On the app | On web |
|---|---|---|---|
| Entrant | the person an ad pays for; where the ad's job ends | a trial (free, 7 days) or a direct purchase | an intro (paid, 7 / 28 / 84 days) |
| Subscriber | someone paying full price | a trial that converted, or a direct purchase | someone who renewed at $42.20 |
| Entry rate | entrants who become subscribers | trial-to-paid, 39% | intro-to-renewal, about 40% |
| Buyers | the media buyers who run the ads (Stefan, Arthur on web) | | |

When talking about one route, use its own word: trial, intro. Across both: entrant. Never "buyer" for a customer.

## The three money words

Take one web subscriber, Maria. She entered on Oct 1.

- **Spend** is what the ad cost to get her: $64. The price.
- **Revenue** is what she has paid so far: $18.99 on Oct 1, $42.20 on Oct 29, so $61.19 by Halloween. The past, a total.
- **MRR** is what she is worth per month while she stays: $45.70. A label on her, not a total. Zero the day she cancels. The pace.

MRR only counts people who have made the full-price payment. Door money is revenue right away; it is not MRR.

## Level and flow

- A **level** is read on a day: subscribers, MRR. Like a bank balance.
- A **flow** is counted over a window: spend, entrants, revenue collected. Like a month's deposits.
- ARR = MRR × 12. A speed, not a year's earnings.
- The **leak** is the share of the level that leaves each month. Measured as: level at start + MRR added − level at end. About 20% a month on the app; unmeasured on web.

## Gross and cash

- **Gross** is what the customer pays.
- **Cash** is what reaches the bank. App: 75%, the stores keep the rest. Web: 96%, Stripe keeps 2.9% plus 30¢ per charge, about 4% on this mix.
- Never on one line without saying which.

## Prices and periods

| | Pays now (the door) | Then pays | Every | Counts as MRR |
|---|---|---|---|---|
| App, free trial | $0 | $4.99 | week | $21.60 |
| App, monthly | $0 | $12.99 | month | $12.99 |
| App, yearly | $0 | $39.99 | year | $3.33 |
| Web, 4-week (default) | $18.99 | $42.20 | 4 weeks | $45.70 |
| Web, 7-day paid trial | $6.49 | $42.20 | 4 weeks | $45.70 |
| Web, 12-week | $39.99 | $88.40 | 12 weeks | $31.90 |

App prices are the US store. Web intros can be 20% lower (exit offer) and come with optional upsells ($29.99 audio, $17.49 guides); on average an intro pays $18 plus $4 of upsells, $22 at the door.

## The moment a route decides

- App: day 7, when the trial converts or expires. Cancelling auto-renew during the trial fires on the day it is flipped, so many are decided on day 1 or 2.
- Web: day 28 for the default plan, when Stripe charges $42.20. Day 7 for the paid trial, day 84 for the 12-week plan. Failed cards retry for about three weeks after, so a cohort's rate settles around seven weeks after entry.

## Windows

- A flow window ends on the last complete day, not today.
- The current one: Aug 12 to Sep 15, 2026, chosen to match the colleague's P&L page (web ramped on Aug 10).
- A level is dated to the day it was read.
