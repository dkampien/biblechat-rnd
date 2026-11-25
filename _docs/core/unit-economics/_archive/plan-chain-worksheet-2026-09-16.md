---
created: 2026-09-16
updated: 2026-09-16
archived: 2026-09-17 (superseded by ../03-plan-chain-goal-to-spend.md)
---
# The plan chain, one page, fill in the blanks

Every plan number comes from one chain, run once per month per route. Four inputs, four steps. Check the inputs; the arithmetic takes care of itself.

```
MRR to add  ÷  MRR per payer  =  payers
payers      ÷  entry rate     =  entrants
entrants    ×  cost per entrant  =  spend
```

MRR to add = leak + growth. Leak = pile at the start of the month × leak rate. Growth = your share of the gap ÷ months left.

## 1. The four inputs

Write the number you trust and where it came from. Reference values are Sep 16, 2026.

| Input | App | Web | Where to get it | Reference (Sep 16) |
|---|---|---|---|---|
| MRR one new payer brings, per month | ______ | ______ | pricing and plan mix | app $18 · web $45.70 |
| Entry rate (trial-to-paid · intro-to-renewal) | ______ | ______ | app: BigQuery · web: Stripe or Stefan | app 39% · web ~40% |
| Cost per entrant (CPT · cost per intro) | ______ | ______ | ad accounts, P&L page | app $17.3 · web $64 |
| Leak per month, share of the pile that leaves | ______ | ______ | app: measured · web: unknown, ask | app 20% · web 20% assumed |

Two more that frame the chain:

| Frame | App | Web | Reference |
|---|---|---|---|
| Pile today (MRR) | ______ | ______ | app $2.51M · web $64k |
| Target on Dec 31 | ______ | ______ | company $5.0M; split by route: ______ (ask who set it) |
| Money back at the door per entrant | $0 | ______ | web $22 (intro + upsells) |

## 2. One month, worked

October, web, with reference inputs:

```
pile at start            $200k     (what September ends with)
leak      = 200k × 20%   $40k
growth    = share ÷ months left      $282k
MRR to add               $322k
payers    = 322k ÷ 45.70            7,050
entrants  = 7,050 ÷ 40%             17,600
spend     = 17,600 × $64            $1.13M
back at the door = 17,600 × $22     $0.39M
net spend                            $0.74M
```

## 3. The grid, blank

Fill left to right, one row per month. Pile at start of a month = pile at start of the previous month + that month's growth.

**App**

| Month | Pile at start | Leak | Growth | MRR to add | Payers | Entrants | Spend |
|---|---|---|---|---|---|---|---|
| Sep 16 to 30 (half) | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| October | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| November | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| December | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| Total | | | ______ | ______ | ______ | ______ | ______ |

**Web**

| Month | Pile at start | Leak | Growth | MRR to add | Payers | Entrants to buy | Spend | Back at door |
|---|---|---|---|---|---|---|---|---|
| Sep 16 to 30 (half) | ______ | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| October | ______ | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| November | ______ | ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| December | ______ | ______ | ______ | ______ | ______ | 0 | 0 | 0 |
| Total | | | ______ | ______ | ______ | ______ | ______ | ______ |

## 4. Three rules that bend the grid

1. **Web runs one month early.** An intro bought in October renews in November. Write October's entrants from November's payers. December's entrants land in January and do not count.
2. **Half a month gets half a leak and half a growth.** Sep 16 to 30 is 15 days: multiply both by 15 ÷ 30.
3. **Check the bottom line against today.** App runs ~$2.0M a month now, web ~$0.5M. A month that asks for 4x today's spend is a scale-up question for the buyers, not a budget question.

## 5. Sanity checks that catch most mistakes

- Payers × MRR per payer must equal MRR to add. If not, the division slipped.
- Spend ÷ entrants must give back the cost per entrant. If not, a row was mixed up.
- Total growth across the months must equal the gap you wrote in section 1.
- If the sum of spend is far from ~$9M app and ~$4M web, one input moved a lot. Find which.
