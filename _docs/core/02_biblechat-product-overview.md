---
created: 2026-08-15
updated: 2026-08-17
---
# BibleChat Product Overview

Ground truth about the product, for anyone building marketing on top of it.

## 1. What the app is

Bible Chat is a daily spiritual companion. At its core it is a way to interact with and consume the Bible: conversation, daily plans, devotionals, meditations, audio. It does not start from the text, the way a classic Bible app does; it starts from the person, a gene it was born with: the founders' previous app let people talk to books, the book everyone asked for was the Bible, and Bible Chat began as exactly that. People come to it in two states: hurting (a life problem, wanting relief through faith) or seeking (wanting to get closer to God and make faith a daily habit). The Bible is the material; the app makes it personal, daily, and easy.

## 2. Positioning

- **What it is in the buyer's mind:** a spiritual companion. The ads, though, enter through the hurting stream: faith-shaped mental health, help with a life problem (a failing marriage, anxiety, grief) through faith. That's a choice, not the whole identity: pain is specific, targetable, and legible in one image, while "get closer to God" is generic demand every faith app bids on. Marketing starts from the problem, never from the app.
- **Who it's for:** the mined problem map (auto-ads-loop `data/problems.json`) is the customer profile, in the customers' own words. When you need "the audience," read it there, not from a persona sketch.
- **What it competes with:** two different groups. In the app store, other faith apps (Hallow, Pray.com, Glorify, YouVersion) compete for the same subscriber. At the moment someone sees an ad, the ad competes with everything that person considers for their problem: therapy, self-help, or just living with it.
- **The product class:** an intangible transformation. The benefit (peace, a mended marriage, feeling close to God) is invisible; it cannot be displayed like a physical product, and a feature tour does not convey it. Selling this class means making an invisible outcome feel concrete and believable to someone in the middle of the problem. How is an open question, the central creative one of this business; one proven arrangement, a starting point not a rule, is a specific pain moment in the buyer's own words, the mechanism (what concretely happens when she uses the product), and proof from someone she believes.
- **What an ad actually sells:** in this product, the believable form of the benefit is the plan built for the buyer's problem, which is what the paywall unlocks. An ad's natural ask is "get your plan," not "download our app."

## 3. Features

The full feature list lives in its own doc: [03_biblechat-features.md](03_biblechat-features.md). It is distilled from the iOS repo (every feature cites a real code path, no invented features) and each row is already phrased as an ad mechanism: what it does, the pain it cures, the outcome in her words, whether it can be demoed on screen.

## 4. The daily plan

Mechanics as of the app's June snapshot; check the live app before an ad quotes exact details.

- During onboarding the user describes their problem in their own words; the app generates a plan from it (theme, title, day sequence). The paywall appears right after the plan preview, so what the paywall sells is the just-generated personal plan.
- One day: 3-5 short cards, about 5 minutes total: a mood check-in, a verse, a devotional, a prayer.
- A plan runs 7 days and can be continued or restarted with an edited problem.
- The sentence ads can complete honestly: "You get 3-5 short cards every day, built around your [pain], in about 5 minutes."

Still missing: a real day's actual content (needs the live app), and 3-5 real user outcome quotes (pullable from VoC purchase triggers or store reviews).
