---
created: 2026-09-08
updated: 2026-09-08
---
# What TikTok's faith audience saves: a brief for scaling BibleChat on TikTok

Source: four partitions (4 of 27) of the public `kuben-developer/tiktok-videos-4b` dataset, about 665M TikTok posts scraped through 2 September 2026. They hold 6.82M English faith-captioned posts with 47.7B views, 90% of the views US. Method, caveats, and how to rerun are at the end. Files under `out/`.

The one number to hold: **saves per 1,000 views** (s/1k). A save means "I want this again," the closest thing in the data to intent. The faith average is 9.3 s/1k; the English platform average is about 6.5.

## 1. The customer Meta delivers and the customer TikTok would deliver carry different problems

The problem map (auto-ads-loop `data/problems.json`) ranks 60 problems by who pays. Its verbatims are what users typed into onboarding, and those users arrived through Meta ads, so the map is a record of the problems Meta traffic carries. Tier A is marriage, illness, widowhood, a lost child, bills, single parenthood, caregiving. On TikTok most of those are small and get sympathy, not saves.

| Problem group (map tier) | Posts (5k+ views) | Views | Saves/1k |
|---|---|---|---|
| A: marriage, illness, widowed, lost child, bills, single parent, caregiver | 5,742 | 773M | 6.4 |
| B: addiction, depression, abuse, past hurts, anger, work | 7,474 | 739M | 9.8 |
| C: breakups, feeling lost, doubt, relationships, infertility | 8,486 | 962M | 8.2 |
| D: temptation, discipline, doubt, distant from God, school | 5,416 | 420M | 12.0 |

Problems with at least 100 posts over 5k views, ranked by save rate. Tier A marked.

| Problem | Tier | Posts 5k+ | Saves/1k | Shares/1k | Read |
|---|---|---|---|---|---|
| temptation-battles | D | 968 | 16.9 | 14.2 | |
| my-quiet-addiction (lust, purity) | B | 731 | 16.6 | 7.2 | private struggle, saved not liked |
| struggling-financially | A | 140 | 16.6 | 8.1 | payer problem that works here |
| single-and-searching | C | 190 | 13.8 | 7.1 | "dear future husband" |
| past-hurts (trauma, forgiveness) | B | 2,110 | 13.3 | 8.4 | big and saved |
| not-good-enough | B | 495 | 12.2 | 8.5 | |
| doubting-faith | D | 1,782 | 12.0 | 8.7 | big and saved |
| feels-alone | A | 606 | 11.9 | 7.9 | payer problem that works here |
| no-discipline | D | 1,832 | 10.8 | 7.3 | big and saved |
| breakup-heartbreak | C | 1,734 | 10.5 | 4.4 | biggest by views |
| feels-lost-no-direction | C | 153 | 10.5 | 4.1 | |
| depression | B | 1,059 | 10.2 | 6.5 | |
| future-dread (anxiety, worry) | C | 2,753 | 9.9 | 7.3 | biggest by post count |
| school-pressure | D | 609 | 9.4 | 6.0 | |
| new-believer | explore | 365 | 9.4 | 11.5 | |
| relationship-struggles | C | 547 | 8.9 | 5.4 | |
| spouse-infidelity | A | 142 | 8.4 | 9.1 | |
| marriage-in-trouble | A | 217 | 7.6 | 5.8 | |
| going-through-divorce | A | 1,001 | 7.4 | 6.0 | big, average saves |
| overwhelmed-exhausted | B | 804 | 6.5 | 5.4 | |
| grieving-a-loss | A | 1,855 | 6.0 | 3.9 | high volume, low saves |
| single-parent | A | 360 | 5.0 | 7.4 | shared, not saved |
| widowed | A | 228 | 4.3 | 4.1 | |
| own-illness | A | 830 | 3.9 | 2.6 | |
| lost-a-child | A | 118 | 3.4 | 1.4 | |
| miscarriage-infertility | C | 1,170 | 2.8 | 2.0 | high volume, lowest saves |
| caregiver-burnout | A | 182 | 2.5 | 2.1 | |

Plain reading: the TikTok faith audience is younger and what it saves is private: temptation, lust, doubt, discipline, forgiveness of past hurts, not feeling enough. Grief, illness, infertility and caregiving content is everywhere, and people like it and move on. Three payer problems hold up: money stress, feeling alone, and anxiety (the largest topic by post count, saved at about the average). Divorce and marriage are large on TikTok but saved at or below average.

Implication for a TikTok push: TikTok needs its own problem list, not the Meta one ported over. Lead probes with anxiety, feeling alone, and money stress (big here and known to pay), and run discipline, doubt, temptation, and past hurts as TikTok-only bets the Meta map would never surface. Do not expect widowed, illness, lost child, or caregiving to travel.

Variance note: the divorce save rate was 14.6 on the first partition alone and 7.4 across four. Rows are clustered by creator, so a single partition can be swung by one account. Rates in this brief are from four partitions; treat anything under about 300 posts as indicative.

## 2. Faith content that gets saved is long

Saves per 1,000 views by video length, posts with 1k+ views:

| Length | Faith posts | Faith s/1k | Faith 90th pct views | Platform s/1k |
|---|---|---|---|---|
| photo post | 29,890 | 11.6 | 7k | 11.5 |
| 0-7s | 200,733 | 7.6 | 14k | 6.6 |
| 8-15s | 401,191 | 7.5 | 17k | 6.1 |
| 16-30s | 256,563 | 8.8 | 21k | 7.4 |
| 31-60s | 286,035 | 9.3 | 29k | 6.7 |
| 61-120s | 193,276 | 11.8 | 49k | 6.5 |
| 120s+ | 137,600 | 10.9 | 58k | 6.7 |

On the platform as a whole, length barely moves the save rate. In faith, 61 to 120 second videos save at 1.57x the rate of 8 to 15 second ones and reach three times further (90th percentile 49k views against 17k). Pain-tagged faith posts show the same curve (6.2 at 8-15s, 11.6 at 61-120s). Most 8 to 15s faith posts are verse cards and clips; what gets kept is the whole thought: a teaching, a testimony, a prayer.

Implication: TikTok tests should include 45 to 90 second cuts that deliver the mechanism in full, not only the 15 second hook-and-cut that Meta rewards. Photo posts save well (11.6) but reach little; cheap to test as carousels.

## 3. Sounds

Two thirds of faith posts with 20k+ views run on original audio (a voice). Among reusable sounds, ranked by save rate with at least 200 faith posts. All need clearing against TikTok's Commercial Music Library before use in an ad.

| Sound | Faith posts | Views | Saves/1k | Shares/1k | Last seen |
|---|---|---|---|---|---|
| The God Frequency | 295 | 45M | 41.4 | 75.7 | May 2026 |
| Ambient music with a wilderness image | 565 | 29M | 40.6 | 58.5 | Aug 2026 |
| Live in the Spirit (two versions) | 1,321 | 58M | 29-35 | 13-17 | Aug 2026 |
| peace | 274 | 27M | 34.4 | 47.0 | Aug 2026 |
| growth | 858 | 35M | 32.8 | 21.9 | Jan 2026 |
| Boundless Worship | 7,707 | 295M | 25.2 | 17.3 | Aug 2026 |
| Last Hope (plus slowed version) | 1,271 | 55M | 20-22 | 13-33 | Aug 2026 |
| Ambient-style emotional piano | 1,260 | 54M | 21.0 | 21.0 | Aug 2026 |
| snowfall | 1,274 | 36M | 20.1 | 8.8 | Aug 2026 |
| Gods creation | 2,925 | 88M | 18.8 | | Aug 2026 |

Boundless Worship is the workhorse: 7,707 faith posts and 295M views at nearly three times the faith average, still in use the week of the scrape. Full list in `out/sounds_top.csv` (300 sounds) and `out/sounds_pain_posts.csv` (sounds under pain-tagged posts).

## 4. Bible Chat already has a proven TikTok format in this data

520 posts mention Bible Chat, 23M views. 69 of them are one creator series, July to September 2025: a prayer video, median 104 seconds, captioned "If you struggle in your walk with God, I'm praying for all of you. You can also join me on Bible chat for free with the link in my bio." Seven of those posts passed 1M views. The series totals 20.1M views at 35 saves and 32 shares per 1,000, nearly four times the faith average on both. The best single post (3.6M views) opened with "My mom has been very sick, pray with me for mine and yours."

Whoever ran this (an affiliate, a partner creator, or the team) found the format the rest of this brief points at: long, a real voice, a specific pain, a soft ask. Worth finding out internally what it converted, because it is the closest thing to a TikTok control we have.

The other 438 mentions are organic and quiz-series posts ("The quizzes on Bible Chat are so good", "@Bible Chat App helps me stay consistent") at 11 s/1k.

## 5. Competitors on TikTok

The dataset's ad flag catches almost nothing useful. The captions do:

- **Hallow**: 122 app mentions plus 27 tagged `#hallowpartner` since September 2024. Catholic creators, rosary and Lent content, "link in bio." A creator partner program, not a paid ad program.
- **Haven Bible App**: appeared April 2026 with sponsored creator posts, 140k views on 4 posts by May. A newcomer buying TikTok creators now.
- **Blessed Bible App**: 43 mentions, sponsored creator posts through 2025.
- **Pray.com**: 30 mentions. **Glorify**: 24. Both near-absent.

## 6. Hook bank

`out/hooks_clean.md`: 1,463 first-person faith-plus-pain captions with 20k+ views, spam and fandom stripped, ranked by save rate, overall and per problem. The kind of line that gets saved:

- "I said 'God why can't I stop giving into lust'" (354k views, 40 s/1k)
- "if you struggle with lust, welcome to my page. i see you and you're not judged here" (253k, 39.5)
- "Lust has to rush. We serve a God that sits outside of time." (145k, 43.5)
- "I thank God that version of me passed away." (60k, 57.1)
- "Lord, let conviction and grace be with us as we go our separate ways." (180k, 53.6)
- "Dear future husband, I pray for you often." (56k, 39.9)
- "God i feel so alone." (22k, 48.9)
- "It's been 65 days since my father passed… and I think I'm beginning to understand what David meant" (487k, 39.6)
- "If you're worried right now let me pray for you!" (34k, 38.7, shares 62.9)
- "I hope this sees the right people #anxiety #trustgod" (66k, 43.7, shares 58.0)
- "a prayer over preshift anxiety for all my nurses out there" (31k, 68.1)
- "You don't have to be anxious, worried, or have any other overwhelming feeling. God calls us to let him carry the burden." (46k, 59.5, shares 126)

The raw, unfiltered rankings are in `out/hooks_by_problem.md` and `out/hooks_overall_top200.md`; they include content-farm prophecy accounts that dominate the very top of save rate and are worth knowing about as a format even if not as a hook source.

## What this does not say

- Nothing here is a conversion number. Saves are attention with intent, not trials. Every hook and problem still earns its place through a probe.
- Four partitions of 27. Counts scale by about 7x; rates should hold within the variance noted above.
- Engagement is a snapshot at scrape time. Posts before July 2026 only, so every post had at least two months to accumulate.
- Problem tagging is keyword regex on captions. It undercounts (many posts have no caption) and mis-tags some (fandom edits, jokes). The clean hook bank was filtered for spam patterns, not read line by line.
- The dataset is research-licensed, personal data under GDPR, and was scraped against TikTok's terms. Aggregate wording analysis is the defensible use. Nothing here identifies a person or account.

## Files and rerun

- `data/videos-NN.parquet`: raw partitions (10.7 GB each, gitignored). 00 to 03 downloaded.
- `pipeline.py "data/videos-0*.parquet"`: extracts the faith subset, tags problems, writes every table under `out/`. About 40 seconds for four partitions with DuckDB.
- `hooks_clean.py`: the filtered hook bank from `out/faith_en.parquet`.
- `out_p00/`: the single-partition outputs kept for comparison.
- `out/problem_demand.csv`, `out/format_faith.csv`, `out/format_faith_pain.csv`, `out/format_faith_us.csv`, `out/baseline_en.csv`, `out/sounds_top.csv`, `out/sounds_pain_posts.csv`, `out/faith_by_country.csv`, `out/faith_by_month.csv`, `out/competitors.csv`.
