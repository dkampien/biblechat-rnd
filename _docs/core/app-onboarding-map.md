---
created: 2026-09-15
updated: 2026-09-15
---

# App onboarding map (the "???" between install and paywall)

## What the builder is

The builder is an internal no-code tool that stores every onboarding screen, paywall layout and pricing rule as database rows, and serves them to the app as JSON at launch, so the flow can change without an App Store release. The same builder publishes the web quiz funnels; the mobile side uses onboardings made of chapters and pages instead of the web side's flat ordered screen list.

### Which onboarding is live

Not confirmable with the access I have. The table that names the live onboarding per feature and segment is the placement feature defaults, and `list_placements` returned empty for this app id, as did `list_experiments`. `get_app_context` also failed because the server resolves apps by host and `builder.thebiblechat.com` is not a registered host (it knows `onboardings.thebiblechat.com`).

What I could see: 50 onboardings, about 20 marked published. Published means saved and publishable, not serving traffic. The rows carry no platform field and no locale field, so there is no iOS versus Android split visible at the onboarding level. Platform lives one layer down, in the pricing rule sets.

I mapped the most recently updated published onboarding as the best available proxy for the current control:

- **V6.6 PE FL - Name Personalized Paywall + paywall swap horizon**, id `5c6ff30a-0341-45a3-a210-24cca226a837`, updated 2026-09-14, 24 pages, 3 chapters.

Treat every page number below as "this flow", not "the flow every user gets".

## The screen tree

Two different mechanisms branch this flow, and they are easy to confuse:

- **conditions** on a page decide whether the page is shown at all. This changes the page count.
- **conditional_overrides** on a page swap its title, description or answer options in place. The page still shows, but says something different.

The list below shows conditions in the branch column. Override counts are noted in the text.

```
01. 4eee7321 | featureIntroLogin     | 7-slide feature carousel with Apple/Google sign-in  | branch: all  [ACCOUNT]
02. 1054bf10 | healingReviews        | "40 million and counting", 12 App Store reviews     | branch: all
03. ca4848d8 | healingNotifications  | "Don't let tomorrow start without God"              | branch: all  [PERMISSION]
04. 50858826 | healingPicker         | "Something brought you here today." 6 motivations   | branch: all
05. fc22fcf7 | healingPicker         | "If you could change one thing..." the promise      | branch: all (6 option sets by motivation)
06. 862c5735 | healingPicker         | "How long have you been carrying this?"             | branch: all (6 copy sets by motivation + age)
07. ee0496c2 | healingNameInput      | "What should we call you?"                          | branch: firstName is empty
08. 2f304ed8 | healingBreathingMoment| Affirmation, "even God rested."                      | branch: all (20 copy sets by promise)
09. e20e36d4 | healingPicker         | Denomination, 12 options                            | branch: all
10. 83a6aca8 | healingPicker         | "Which Bible speaks to your heart?" 27 versions     | branch: all (6 reorderings by denomination)
11. 84962500 | healingPicker         | "What's your age group?" 6 buckets                  | branch: all
12. 9b6d7293 | healingPicker         | "How did God create you?" woman/man                 | branch: all (teen set adds "prefer not to say")
13. 3ed5123e | healingPicker         | "When your plan is ready, start with..." pick 3     | branch: age 13-17 or 18-24
14. 8385afff | healingPicker         | "Your plan should start with..." pick 3             | branch: age 25-34 or 35-44
15. a7abe5af | healingPicker         | "Your plan will begin with..." pick 3               | branch: age 45-54 or 55+
16. ced58388 | widgetTutorial        | Home screen verse widget setup, 5 steps             | branch: picked lock_screen_widget AND age not 45+
17. b5e2d7e7 | healingFaithChart     | "here's what happens next", 3-week growth chart     | branch: all (8 copy sets by age, promise, feature)
18. 90594c0e | healingPicker         | "Your first week starts with..." pick 3            | branch: all (8 option sets by motivation + age)
19. 737065d0 | healingInput          | Free text: "Tell it what you're carrying."          | branch: all (6 copy sets by motivation)
20. 7358ff49 | loaderV3              | 20s build, 3 questions, prefetches the paywall      | branch: all  [LOADER]
21. aae1ad6d | healingJourneyPreview | The generated plan, CTA "Start My Plan"             | branch: all
22. 31662637 | animatedTrialInfo     | "Unlock it free for 7 days"                         | branch: not premium AND intro-offer eligible AND age not 13-17
23. cf2cb701 | animatedTrialReminder | "On day 5, we'll check in"                          | branch: not premium AND intro-offer eligible AND age not 13-17
24. f0726818 | paywall               | Horizon hero, free-7-days vs paid, $4.99/wk shown  | branch: all  [PAYWALL]
```

Notes on the tree:

- Sign-in is page 1, before any question, not at the end.
- Notification permission is page 3 of 24, before a single personal question is asked.
- Page index 14 is missing from the stored sequence. A page was deleted and nothing records what it was.
- The name page is skipped when the app already knows `firstName`, which is what sign-in on page 1 supplies. The rest of the flow still runs.
- The loader is not just a wait. It declares three prefetches: the personalised plan, the Bible, and the paywall at Adapty placement `all-products`. The paywall is warmed while the user watches the progress bar.
- There are no pages after the paywall. The web funnel's postPurchase list has no mobile equivalent here.

## Branching summary

Six variables come from answers inside the flow:

1. **motivation**, 6 values (no time for the Bible, closer to God, fighting temptation, need peace, Bible is hard, enjoy the Bible). Rewrites pages 5, 6, 18 and 19.
2. **promise**, about 20 values, each only reachable from one motivation. Rewrites pages 8, 16 and 17. This is the deepest personalisation key in the flow.
3. **age**, 6 buckets. Picks which of pages 13, 14 or 15 shows, gates the widget page off for 45+, gates both trial pages off for 13-17, and rewrites pages 6, 12, 17 and 18.
4. **gender**, 2 or 3 values.
5. **denomination**, 12 values. Reorders the Bible translation list on page 10.
6. **preferredFeature**, multi-select up to 3. Gates the widget tutorial page.

Three come from device and account state: whether `firstName` is already known, whether the user is already premium, and whether the store says they are eligible for an introductory offer.

Four more sit outside the flow and decide which onboarding runs at all: deeplink intent, lifecycle segment, country and language, and platform plus app version.

Rough size. Page-level show and hide gives about 24 distinct page sequences (3 age variants of the feature page, times widget on or off, times trial pages on or off, times name page on or off). Copy overrides multiply that by roughly 20 promise tracks, so several hundred rendered variants of this one onboarding. On top of that sit at least seven sibling onboardings reached by deeplink intent, plus the lifecycle re-onboardings.

The intent mechanism matters for the ad route. A `biblechatapp://override-signals/<base64>` deeplink carrying an intent routes the user to a dedicated onboarding: marriage, parenting, catholics, man_quiz, woman_quiz, audio_bible_study, animated_bible_stories, web2app_restore, reengage_discount. So "ad click leads to onboarding" is not one flow, it is a switchboard.

## Paywalls at the onboarding placement

The live onboarding's paywall is not a row in the paywalls table. It is defined inline on page 24. The paywalls table returned about 120 rows, all keyed `harvest_<hex>`, all with zero associations and all stamped 2026-08-05. Those are archived snapshots of past paywalls and past experiment arms, not what ships.

What page 24 declares:

- Adapty placement `all-products`, template `trial_vs_direct`, layout `horizon`.
- Products `biblechat.pro.weekly` and `biblechat.pro.yearly.discount1`.
- Two choices side by side: Free for 7 days with badge "No Payment Now", and 1 period at price.
- Trial timeline on the page: today full access, day 5 reminder, day 7 charged $4.99/wk.
- The close button is on, so this paywall can be dismissed.

Which prices actually appear is decided by a pricing rule set, selected by platform, country, language, age, gender, denomination and app version. The production-looking ones:

- iOS `v6_6_regional_pricing_v1`: rest of world monthly + yearly.discount1; US weekly + yearly.discount1, with 45+ moved to monthly + yearly.reduced; GB weekly without trial + yearly.discount1.
- iOS adaptive family (`us_adaptive_v2` and about twelve `global_adaptive_v2_*` clones): same prices everywhere, presentation varying by age times gender times denomination. Their own descriptions say draft or test.
- Android, one rule set per region, each bound to its own Adapty placement: US, Tier1 (AU/CA/GB/NZ), LATAM, Philippines, Southern Africa, and an "others" catch-all. Layouts differ, for example Philippines gets monthly plus yearly-with-trial rather than weekly.
- Two web-checkout rule sets (`global_yearly_only_trial_button_web_v1`, `global_elite_weekly_trial_button_web_v1`) add a trial button that sends the buyer to a web checkout on price set `bc-app2web-v1`, and add a hard paywall for 45-54 and 55+.

Named prices found in rule set descriptions: yearly.discount1 is $39.99/yr, sixmonths.reduced is $29.99, elite.weekly is $7.99 against a $4.99 control, elite.yearly.reduced is $99.99 list with a $49.99 first year.

## Live experiments touching onboarding or paywall

None readable. `list_experiments` returned nothing for this app id, with and without the active-only filter. Experiment names do survive inside paywall and rule set descriptions (AU/CA/NZ hard direct paywall, US-EN Android V6.2 vs V6.5, PH new_install price test, RO-EN Live Activity, and others), but all of those look historical.

## App events around onboarding and purchase

`list_app_events` does not return analytics events. It returns Apple In-App Events, the promo cards that appear on the App Store product page. 25 rows, all liturgical feast days, each with per-locale copy and a SPECIAL_EVENT badge. One is currently published: the Exaltation of the Holy Cross, 2026-09-14.

So the builder holds no `onboarding_started`, `paywall_shown` or `trial_started` style names. Those live in the app client and in the analytics warehouse, not here.

## Open questions

1. **Which onboarding is live, for iOS and for Android.** Needs placement feature defaults, which my access does not return. Ask whoever can read placements to name the current default for the `default` feature and `new_install` segment.
2. **Whether onboardings are platform-scoped at all.** The rows carry no platform field. The Android-named drafts suggest the split is by convention, with the real platform switch happening in the rule sets.
3. **Can the paywall be skipped.** On this variant yes, the close button is on. Some rule sets add a hard paywall, but only for 45-54 and 55+. So a meaningful share of installs can finish onboarding without seeing a purchase decision they must answer.
4. **What happens after purchase.** Nothing in the builder. This onboarding has no post-paywall pages, and the web funnel's postPurchase list has no mobile counterpart.
5. **Does "I have an account" bypass onboarding.** Partially at most. Sign-in on page 1 supplies the name, which skips page 7, but no config makes it skip the rest.
6. **What page 14 was.** A gap in the stored sequence with no record.
7. **Which experiments are running now.** Not readable here.

## What contradicts "install to onboarding to paywall to trial to paid"

- Sign-in and notification permission come first, at pages 1 and 3, before any personalisation.
- The trial pre-sell is conditional. Teens skip it, and so does anyone the store says is not eligible for an introductory offer, or who is already premium. Those users reach a paywall with no trial framing.
- The paywall is dismissible for most users, so onboarding can end with no purchase decision.
- Some rule sets route the purchase to a web checkout rather than the App Store, which moves the paid step off the store rails and out of the App Store attribution picture.
- The single "onboarding" is really a switchboard. A deeplink intent from an ad can route the install to a completely different onboarding before any of the above applies.
