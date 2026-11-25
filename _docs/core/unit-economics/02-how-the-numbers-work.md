---
created: 2026-09-14
updated: 2026-09-17
---
# How the numbers work

Why the numbers behave the way they do, both routes. Terms are in `01-terms-and-prices.md`. The arithmetic from goal to spend, and the ladder picture of it (rungs fixed, rates borrowed from past windows), is in `04-plan-chain-goal-to-spend.md`. The facts are in `03-company-numbers-both-routes.md`. Numbers here are September 2026, gross unless marked cash.

## 1. What is sold

Two ways into the same app.

- **App route.** A subscription, entered through a 7-day free trial or a direct purchase. Renews weekly, monthly or yearly; most take weekly, and weekly is 82% of the money. Apple and Google process every payment and keep about 25%.
- **Web route.** The same subscription, entered through a paid intro on a quiz page: $18.99 for 4 weeks by default, then $42.20 every 4 weeks. Stripe processes the payment and keeps about 4%. There is no free trial; the cheapest way in is a $6.49 paid trial for 7 days.

Four facts shape everything below: whether money changes hands at the door, when the customer first decides, what a subscriber pays per month, and who keeps a cut.

## 2. The loop

One month of ad money goes out and comes back through a chain:

spend → entrants → subscribers → revenue

Each stage is priced by dividing the month's spend by the survivors at that stage.

| Stage | Price of one | App | Web |
|---|---|---|---|
| Entrant | cost per trial · cost per intro | $17 | $64 |
| Subscriber | cost per subscriber | $36 | ~$160 |

Entrants become subscribers at the entry rate: 39% of app trials convert on day 7; about 40% of web intros renew on day 28. Cost per subscriber = cost per entrant ÷ entry rate.

Cost per entrant is the ad's number: an ad's job ends when someone enters. The entry rate is the product's number. An ad cannot make a trial convert or an intro renew; it can only send people who were going to.

**Why web's entrant costs four times more.** Under the $64 sits a ladder: $50 per thousand people shown the ad, 3.6% click, 96% of clicks load the quiz, 28% leave an email, 8.2% of those pay. Multiply the pass rates and one intro costs $64. The first two steps belong to the ad; the last three to the quiz page. An ad with cheap clicks that never buy has a good click cost and a bad $64.

**Door money.** On the app, an entrant pays nothing on day 0. On web, an intro pays about $22 on day 0: $18 for the intro plus $4 of upsells on average. So of the $64, $22 comes back the same day, and the net cost to reach the decision is $42. This is the single biggest difference between the routes and it changes every comparison below.

## 3. Cost vs value

An entrant costs money up front. Its value arrives in installments, from whoever converts and stays.

| Time since entry | App, per trial | Web, per intro |
|---|---|---|
| Day 0 | $0 | $22 |
| Day 30 | $5.50 | $31 |
| Month 12 | $22 (cash $16), measured | ~$85, modeled |

Return on ad spend (ROAS) = value ÷ cost. Same entrant, two readings: on the app 32% at month 1 and about 130% at month 12; on web 49% at day 30 and about 133% at month 12 if the model holds.

**Month 12 is not month 1 × 12.** It is month 1 plus eleven smaller collections, because people leave each month. On the app the sum comes to about 3× month 1, not 12×. On web the colleague's curve says a subscriber averages 1.4 full-price renewals in a year.

**Every app cohort is in loss at month 1 by construction.** $17 out, $5.50 back. The question is only whether the installments close the gap by month 12. Web is different: half the cost is back in 30 days because of the door, so a web cohort is less deep in loss early. The price of that is a longer wait for the rest.

**Measured versus modeled.** The app has a cohort from July 2025 that has lived a full year; its month-12 value is a fact. Web ramped on Aug 10, 2026; its first cohort has lived six weeks. Everything past day 30 on web is a curve someone typed in: 36% survive the first renewal, decaying after. The first real cohort did $31 by day 30 against the curve's $34, which is encouraging and is one cohort. Nobody has observed a second web renewal in volume yet.

**The rules.** A month's spend must return 100% by month 12, gross (company rule). At least 32% by month 1 (VC rule). They are the same bar read at two moments on the app. On web the day-30 reading is already 49%, so the month-1 rule is not the binding one there; the month-12 rule is, and it rests on the model.

**The ceiling.** The cost per entrant at which month-12 ROAS is exactly 100%. App: $22 per trial gross, $16 cash. Web: about $85 per intro on the curve; but until the second renewal is measured, treat today's $64 as the bar, because a weaker second renewal pulls $85 down fast. If only a quarter of first renewers renew a second time, month-12 value falls to about $65 and the ceiling meets $64.

**Cash changes the ceiling more on the app.** The app keeps 75% of gross, so a 100% gross return is a 75% cash return. Web keeps 96%. A web dollar of gross is worth a third more in the bank than an app dollar.

## 4. The level

MRR is the pile of all monthly paychecks, read on a date like a bank balance. App $2.51M, web $64k, company $2.57M gross. ARR = MRR × 12: a speed, not a year's earnings.

Only two things move the pile: subscribers joining (the loop) and subscribers leaving (the leak).

**The leak** = pile at start + MRR added − pile at end, measured on a past month. About 20% of the pile drains each month on the app. It is a share, not a fixed amount: a bigger pile drains more. Web's leak is unmeasured because almost no web subscriber has faced a second renewal; assume 20% until the first second-renewal read, early November.

**The queue.** Between entering and joining the pile there is a waiting room. On the app it is 7 days long, so on any day it holds about a week of trials (14k) and empties fast. On web it is 28 days long for most, so on Sep 16 it held 5,600 intros, four times the paying pile of 1,388, because the route is six weeks old and most entrants have not reached their first renewal.

This is why web MRR reads three ways and people talk past each other:

| Reading | Web MRR, Sep 16 | What it counts |
|---|---|---|
| charged | $64k | people who have paid full price |
| expected | ~$160k | plus 40% of the queue |
| if everyone renews | ~$300k | plus the whole queue |

The investor P&L uses the third. The ledger says the first. The plan should use the second.

**The lag.** An intro bought in October renews in November. So web spend raises the pile a month after it is spent, and spend in December raises it in January. Any web target with a date has to be bought a month early. The app has no lag worth planning around: 7 days.

## 5. The two routes side by side

| | App | Web |
|---|---|---|
| Money at the door | none | $22 of $64 |
| First decision | day 7 | day 28 (day 7 on the paid trial) |
| One subscriber is worth per month | $21.60 (weekly) | $45.70 |
| Rail keeps | 25% | 4% |
| Month-12 value | measured | modeled |
| Leak | 20%, measured | unknown |
| Per-ad visibility | ends at trial start | intros, renewals, refunds, all per ad, from Stripe |
| Attribution | modeled (SKAdNetwork) | deterministic: the ad's ids are on the charge |
| Ledger | Adapty in BigQuery | Stripe only |

Read together: web pays back faster and is worth more per subscriber, but its long-term value is a forecast and its numbers arrive a month late. The app is slower to pay back and worth less per head, but every number about it is a fact.

## 6. A creative system's job

It produces spend capacity: budget the buyers can put behind its ads while the cost per entrant stays at or under target. $17 per trial on the app, $64 per intro on web. That is the unit the company measures buyers in, and the unit a system should be measured in.

A winner is an ad that carries real spend at or under the target before it fatigues. On the app that is the whole definition, because nothing after trial start is visible per ad. On web there is a second half: an ad's intros can be followed to their renewal in Stripe, so a web winner can also be held to "its intros renew at 35% or better". More exposure, more proof.

The system controls only the first step of the loop. The entry rate and the price belong to the funnel. When MRR from the system's ads moves, the ladder shows which step moved it.

## Three things to re-read before a meeting

1. Value grows with the horizon; always attach a window, and say whether the number is measured or modeled.
2. Month 12 is a sum of shrinking collections, not month 1 × 12.
3. On web, $22 comes back at the door, the rest arrives a month late, and MRR counts only the second payment.
