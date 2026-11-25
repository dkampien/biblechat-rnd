---
created: 2026-08-10
updated: 2026-08-18
---

# AdLoops: upload and posting mechanics (operator's field guide)

How creatives get uploaded, how they get posted to Meta, what the rules do on their own, and where the two "template" engines fit. Written for an operator. Compiled from twelve working threads (13 Jul to 10 Aug 2026) plus live Firestore checks on 10 Aug 2026; sections 3, 4, and 6 re-verified 18 Aug 2026 against live Firestore (rules, experiments, ad_templates) and the Meta Graph API (the account image library). Live-state facts in here are snapshots and go stale: re-check before acting on them.

The rendered version with diagrams: https://claude.ai/code/artifact/d3ffdf79-d805-426a-a612-495c53565c16

## The bottom line

There is no posting parameter. An uploaded image becomes eligible on its own: the pipeline advances it to launch-ready (`video_uploaded`) about 2 to 4 minutes after upload. Whether it then actually posts depends on the config rules. As of 18 Aug 2026 one rule is enabled: it sweeps daily at 18:00 UTC with a same-UTC-day window, and launches nothing unless at least 10 qualifying images arrived that day. Current state: the rule sweeps but cannot post. Every armed firing has died at ad-set creation on a Meta error (section 4); images reach Meta's library, no ads get created. Treat the sweep as broken machinery still pointed at qualifying uploads, not as safety. Upload = publish stands regardless: humans launch from the sidebar with no query and no schedule.

## 1. The shape of the system

AdLoops and our creative tooling never call each other. Everything meets in one Firestore database (Google Cloud project `bc-ads-tester`). We drop creatives in; AdLoops picks them up on its own schedule and turns them into Meta campaigns. Results come back only as BigQuery reports, joined on the ad name. This is why naming discipline matters: the ad name is the only thread connecting a creative to its results.

Two codebases run this (both cloned under `_reference-repos/adloops/`):

- **Ads_Platform_Web**: the web app. The upload door, the sidebar UI the team clicks, the template definitions.
- **ads-library-automation**: the engine. Background workers that process uploads, the scheduled rules, the runners that create things on Meta.

### The four record types

AdLoops is four kinds of records plus machinery that reacts to them:

| Collection | Question it answers | Notes |
|---|---|---|
| `videos` | What creative? | Our uploads. The nouns. One record per creative, all aspects inside. |
| `ad_templates` | What should the campaign look like? | Reusable blueprints of exact Meta settings. V2 engine only; V1 has no templates. |
| `config_rules` | When does launching happen by itself? | Standing scheduler instructions. The `enabled` flag is the on/off switch for automation. |
| `experiments` | One concrete launch order | The verbs. One record is roughly one ad set with its ads (the campaign is found or created by name around it). Starts as instructions, ends as a receipt with the Meta IDs written back. |

An `experiments` record has three possible authors: a rule fires on schedule, a human launches from the UI, or a script writes the record directly. All three converge on the same collection and the same engine picks them all up. "Running your own experiment" means the script path: the launch order is written directly with the campaign settings carried inline (`templateConfig`), so no saved template and no rule are involved. A template is nothing more than a saved, reusable copy of that same settings block for launches that go through the UI.

## 2. Uploading: one door, a strict shape

Every creative enters through `POST https://adloops.ai/api/creatives` (multipart, Bearer `al_at_` year-long token). The MCP tools and the web UI are other handles on the same door. What you send becomes a `videos` record:

| You send | What it becomes |
|---|---|
| `name` | **The Meta ad name, verbatim.** Lands as the record's `video` field, flows onto the live ad unchanged, and is the only join key for results. Convention: `name = creative_id`, always (e.g. `drowning-in-bills--debt-01`). |
| `file_portrait` | The 9:16 image. Effectively required: without a portrait slot the record is typed UNKNOWN and every image rule ignores it. |
| `file_square`, `file_four_five` | The 1:1 and 4:5 images. Send all aspects in one upload; aspects added later never reach Meta. |
| `feature` | The routing key. Not a tag: it decides the landing page / App Store product page via the feature's config. |
| `language` | Full lowercase word (`english`), never a code. |
| `config_id`, `platform`, `providers` | `biblechat` / `IOS` / `facebook` for this lane. |
| `fields` (JSON) | Extra fields, flattened onto the record's top level (how `pain_point` rides along). Custom fields never reach BigQuery without a manual SQL change on their side. |

The server also stamps `affiliate: false` and `mix: false` on every upload. These are load-bearing: rule datasources select on them.

Duplicate protection is byte-level (SHA-256): uploading identical bytes returns "skipped" with the existing record's id. You cannot re-upload to fix a field.

## 3. After upload: the conveyor belt

A new record moves through fixed stages, driven by background workers:

```
new -> download_done -> tagged -> content_generated -> video_uploaded
                        (AI describes)  (AI writes copy)   (launch-ready)
```

- The whole run takes 2 to 4 minutes.
- Seed at `content_generated` with your own `description`, `primary_text`, and `headlines` to skip both AI steps.
- Never seed `video_uploaded` by hand: that final hop is where the image is physically uploaded to Meta and gets its hash; faking the status means launch fails with "has no Facebook upload for business".
- Truly launchable = status `video_uploaded` AND a Meta image hash on the record AND copy present. A record missing copy is silently dropped at launch, not rejected loudly. Provide at least two headlines, or Meta degrades the format and the App Store product page link falls off.
- What `video_uploaded` physically means: the image bytes now sit in the ad account's media library on Meta, addressed by their hash. That is a file in storage, not an ad: no campaign references it, nothing is posted, nothing spends. Verified live (18 Aug): the Graph API (`adimages` on the account) lists the Aug 3 uploads sitting in the Basmo iOS library by name and hash, with zero ads attached. The library has no standalone page in Ads Manager; it only surfaces inside ad creation (Add media, choose existing image). Creative Hub, despite the name, is a mockup tool and is not this library.

## 4. Auto-posting: the config rules

A config rule is a recipe stored as data, not code: "every day at X, collect matching launch-ready creatives, group them into ad sets, launch." A scheduler checks hourly which rules are due. Whether a rule runs is a single `enabled` flag on the rule record, so "is auto-posting on" can only be answered by checking live.

### Live state, checked 10 Aug, re-verified 18 Aug 2026

34 rules exist for biblechat. 33 disabled, 1 enabled:

- **`IL2sSmkQvghsZEXbDszC`**: "Bible Answers - one adgroup per user problem (pain_point), universal landing page." Facebook, iOS, US, images, daily 18:00 UTC. Full record verified:
  - **Who gets swept: any qualifying image, not just one lane.** Extra filters are only platform iOS and provider Facebook. No `problem` or `feature` scoping. Qualifying = launch-ready image, not affiliate-flagged, uploaded inside the window. Since the upload door stamps `affiliate: false` and `mix: false` on every upload, anything pushed through the API qualifies by construction.
  - **The window is one UTC day, then gone forever.** `lookbackDays: 0`: the sweep only sees records uploaded the same UTC day it fires. It is not a backlog processor. A record that survives its upload day unswept is invisible to this rule for the rest of time, which is why the Meta library can hold hundreds of unused images the rule never touches again.
  - **Why it rarely fires: `minVideosToRunExperiment: 10`.** Fewer than 10 qualifying images in a day = nothing launches. Batches of 10 to 20 ads, max 20 per ad set.
  - **What it builds:** campaign `Biblechat Bible Answers - Adv+ ABO {countries} - {platform} - {month}`, ad sets grouped by each record's `problem` field, $20/day per ad set, ages 25 to 54, WEB objective, on `act_697155031095732`. Every ad points at one universal landing page baked into the rule (`onboardings.thebiblechat.com/.../bible_answers/...`). Campaign and ad set names come from these patterns at launch; the ad name is whatever the upload sent, verbatim. Created 2 Aug, last edited 3 Aug. Field mismatch: the rule groups by `problem`, but the prior system's records carry `pain_point`, so its uploads lump into generic batches (three uniform batches of 20 on Aug 3 to 4) instead of one ad set per problem.
  - **What happened when it fired armed (experiments read 18 Aug):** the Aug 3 to 4 firings swept the prior system's ~60 images into three experiments of 20. All 60 images reached Meta's library. All three experiments then died at ad-set creation (`final-error-max-retries`) on the same Meta error: "Must have uniform pixel when creating an ad set with ad set budget sharing enabled in the parent campaign" (subcode 4834009). Zero ads were ever posted by this rule. Likely cause: campaigns are found-or-created by name, and an existing Bible Answers campaign shell with budget sharing enabled collides with the experiment's own template settings, which set `is_adset_budget_sharing_enabled: false`. A stale shell fighting a newer template, not a deep design flaw.
  - **Broken but armed.** The rule is still enabled and still fails the same way. Any day with 10 or more qualifying image uploads gets swept into the failing path: images land in Meta's library (permanently, byte-deduped), experiments are created and die, nothing posts, nobody is alerted. Do not read the silence as protection, and do not fix the rule without its owner: the fix is either repairing the campaign collision (or letting a fresh month mint a fresh campaign name) or disabling the rule until a scoped replacement exists.
- **`4iJm3tpgfG7beGOeTdeV`** (disabled): "Test images uploaded today by editors on Facebook IOS", the reference rule from the July launches.

### Timing

Upload before 18:00 UTC and a qualifying creative is in that evening's sweep; after 18:00, it waits for tomorrow's sweep and only counts if tomorrow is still its upload day in UTC terms (with `lookbackDays: 0` it is not, so a post-18:00 upload is effectively never swept by this rule). "Uploaded today" is measured on the record's arrival timestamp.

### The guard

`scripts/disable-biblechat-rules.js` in the engine repo lists what it would disable (dry-run by default) and flips everything off with `--apply`. It disables the team's automation too, so coordinate instead when possible.

### Standing law

**Upload = publish.** True even before any rule was enabled (the media buyer launched both August waves within 40 to 90 minutes of upload, unprompted); with a rule enabled it is literal automation. Nothing goes into the library unless it is ready to spend money that evening. The August upload scripts encode this as a `CONFIRM_UPLOAD=yes` gate.

## 5. Launching by hand

Three ways when rules are off:

1. **The sidebar.** A human picks creatives in the AdLoops UI and launches. Same machinery underneath as the automation.
2. **A local rule script.** Copy the rule's recipe into a local script so it runs while the real rule is disabled. Ours: `ads-library-automation/functions/src/test/catchup-4ijm.ts` (untracked). From `functions/`:
   ```bash
   GOOGLE_CLOUD_PROJECT=bc-ads-tester npx tsx src/test/catchup-4ijm.ts --debug true   # dry run, prints grouping
   GOOGLE_CLOUD_PROJECT=bc-ads-tester npx tsx src/test/catchup-4ijm.ts                # real run = launches
   ```
   It dedupes against experiments already created today for the same rule id. Aim it by editing the recipe in the file: lookback window, `feature` filter, media type.
3. **The team's runner** (`src/test/experiments.ts`): `runLocalRule` (enabled rules only) and `addFacebookExperimentsForCustomRule` (a recipe passed by hand; what the catchup script imitates).

Credentials: `gcloud auth application-default login` as `denis@thebiblechat.com`. Trap: if `GOOGLE_APPLICATION_CREDENTIALS` is set (on this machine it points at the adloops-local service account), it silently overrides the login; unset it first (`env -u GOOGLE_APPLICATION_CREDENTIALS ...`). The Meta token lives inside AdLoops config; we never handle it.

### Testing without spending (the ladder)

1. Push into the sandbox collections (`videos_test` / `experiments_test`).
2. Template dry run (`debugLocal: true`): zero contact with Meta. Only true for the V2 engine; on V1, `debugLocal` still creates real but PAUSED campaigns.
3. Real launch created PAUSED; inspect in Ads Manager.
4. Activate. Only this step spends.

Useful engine-repo test scripts (run `npx tsx` from `functions/`): `test/campaigns/debugProviderNewCampaign.ts` (the launch harness, real-but-paused, `--cleanup`), `test/campaigns/TestExperimentBuilder.ts` (sandbox collections), `test/configRules/listLivePolicies.ts` and `explore.ts` (inspect rules), `test/_linkOverrideSmoke.ts` (pure in-memory).

## 6. The two launch engines ("V1 vs V2 templates")

One field on the experiments record decides which engine executes it. That field is the entire V1 vs V2 story. Nothing in the data says "v1" or "v2": the literal marker is `engine: "template"` present (template runner) or `engine` absent (classic runner). A template-engine record also carries `templateKey` (which blueprint), `templateVersion` (which revision of that blueprint, not an engine version: `fb_cpt_app_promotion` is at revision 13), and a full `templateConfig` snapshot of the resolved settings frozen in at launch time. That snapshot is an audit trail: you can always read exactly which settings a given launch ran with, even after the blueprint moves on.

The `ad_templates` collection holds 15 saved blueprints, named by channel and funnel: nine Facebook (`facebook_base`, `fb_bc_web2app`, `fb_bc_web_funnel_trial`, `fb_bc_short_funnel_test`, `fb_cpt_app_promotion`, `fb_cpi_app_promotion`, `fb_roas_web2app`, `fb_web_conversions`, `fb_adapty_lead`) and six TikTok. Each is a frozen Meta API payload with per-setting modes (`preset` = fixed value, `platform` = per-platform values, `resolved` = filled at launch), reaching knobs no rule field ever expressed: attribution windows, opting out of Meta's AI creative enhancements, device targeting down to iPad/iPhone/iPod.

What runs in practice (18 Aug): the team's current launches are almost all template engine on `fb_cpt_app_promotion` (23 of the 25 most recent experiments). The classic path is legacy; the last classic-engine record in the recent window is from early July. The enabled Bible Answers rule also launches through the template engine (`fb_bc_short_funnel_test`, revision 2). Any future lane here will be template-engine with some blueprint key.

**V1, the classic runner (no `engine` field). The historical mainline, legacy in practice.** The blueprint is the code itself: the engine picks a runner class by objective + platform (`FacebookWebExperiment`, SKAN, Android, Smart+ variants on one 1,013-line base class) and that class fills in everything the short form didn't say, with baked-in opinions: mobile-only placements, CompleteRegistration optimization, `age_max` always 65, Advantage+ audience auto-enabled when `age_min <= 25`. Where the form had no room, conventions hide in names: `cbo` anywhere in the campaign name turns on campaign-level budget; `cpt` turns on 1-day click attribution (literal substring checks). What V1 can do that V2 can't: per-experiment `landingPage` with per-ad `{{ad.name}}` substitution, and no cap on ads per ad set. Caveat: `{{ad.name}}` resolves to a richer internal string (`<video> <objective> <countries>`), not the bare Meta ad name.

**V2, the template runner (`engine: "template"`). The newer graft.** Deliberately branchless: it obeys a settings block verbatim (`templateConfig`: raw Meta campaign, ad set, creative bodies) and adds nothing. The block comes from an `ad_templates` record (UI launches) or inline from your script. One link per template, copied onto every ad (`link_overrides` is the per-ad exception, solo ads only). Caps on the batch surface: 4 to 7 ads per set, max 9 sets. Supports `automaticTexts: false` + `copy_overrides` to lock your copy, `debugLocal` for a true dry run. New campaigns default to PAUSED. Drops custom fields (whitelist).

**Granularity:** one experiments record is one launch order, roughly one ad set. A campaign with three ad sets is three records sharing one campaign name; find-or-reuse by name lands them together.

**Receipts:** V1 writes a per-creative map with real Meta ad ids (`videos_uploaded`). V2 writes `ads[]` with ids keyed by creative name only. Either way the ad name is the join key downstream (BigQuery `bc-ads-tester.ads.marketing_ads_data`, join on `adName == videos.video`).

**Not to be confused with:** our own format molds (`challenge-v1`, `search-v1`, `listicle-v1`). Those are HTML layout files on our side that render the PNGs; the "-v1" is a version suffix, unrelated to AdLoops engines.

## 7. The laws (learned by paying for them)

1. **Upload = publish.** Now enforced by automation; previously by a fast media buyer. The only real gate is the one in your own upload script.
2. **Compared things get separate ad sets.** Meta shifts budget freely inside an ad set; the w2 format duel shared one set and the challenger got under 4% of impressions. One question per ad set, budget on the set.
3. **The ad name is sacred.** Set at upload, flows to Meta verbatim, only join key for results. Same name on a reused ad set = silently skipped, no error. Blocked words (sex, adult, ...) silently rewritten to "content", which breaks the join.
4. **Ship every aspect in one upload, portrait included.** No portrait = invisible to image rules. Late aspects never reach Meta. Replacing image bytes later does not refresh Meta's copy.
5. **Write your own copy, and lock it.** Seed description and copy at upload, give at least 2 headlines, and on V2 set `automaticTexts: false`; otherwise AdLoops may silently rewrite copy when the campaign geography implies a language.
6. **Exact sizes only.** 1080x1920, 1080x1350, 1080x1080 pass untouched; anything else is center-cropped and re-encoded, and a near-miss ratio can be re-filed into the wrong slot.
7. **"The rules are disabled" is a fact with a timestamp.** It is data someone can flip any moment; it went stale within hours once. Check live before any volume push.
8. **Some hosts are exempt from link enrichment.** Landing URLs on `app.thebiblechat.com`, `*.sng.link`, or `api-ua.adapty.io` skip all parameter substitution. Per-ad landing page schemes need another domain (verseread.com is safe).

## 8. Where everything lives

| Thing | Location / value |
|---|---|
| Upload door (code) | `Ads_Platform_Web/app/api/creatives/route.ts` -> `lib/creatives/uploadCreativeCore.ts` |
| Engine switch | `ads-library-automation/functions/src/campaigns/facebook/FacebookExperimentFactory.ts` |
| V1 runner | `.../campaigns/facebook/BaseFacebookExperimentRunner.ts` |
| V2 template runner | `.../campaigns/facebook/template/runFacebookTemplateCampaign.ts` |
| Manual launch script (ours) | `.../functions/src/test/catchup-4ijm.ts` |
| Rule kill switch | `ads-library-automation/scripts/disable-biblechat-rules.js` (`--apply`) |
| Rules themselves | Data, not files: `config_rules/biblechat/rules/...` in Firestore |
| Google project / bucket | `bc-ads-tester` / `bc-ads-tester.firebasestorage.app` |
| Company / config | `krmeFwuy24LKyPw9Wn6y` / `biblechat` |
| Ad account (used so far) | `act_697155031095732` ("Basmo IOS", business `173558290375515`) |
| Pixel / default page | `675497693950555` / `142979542221369` |
| Results | BigQuery `bc-ads-tester.ads.marketing_ads_data`, joined on ad name |

### Open questions, as of 18 Aug 2026

- Which ad account future launches should target: everything so far ran on "Basmo IOS", while Bible Chat US (`act_851055460791534`) sits under a different business. Explicitly Denis's call.
- How the 7 Aug teammate images (`general_ST_brief...` names, uploader Kseniya Aryka) actually went live. They are spending, but the enabled rule's Bible Answers campaign holds only the three failed experiments, so those launches rode a different campaign name or mechanism (likely a hand launch). One question for the team.
- Which of biblechat's 35 `feature` ids new ad lanes should ride on (feature routes the landing page).
- The MCP tool implementations were never read (their repo, `ui-web`, was never cloned); everything about them is inferred from the backend they call.
- Whether the team intends the enabled rule to sweep all editor images or meant to scope it to the pain_point lane (its description uses the pain_point vocabulary, but the query has no such filter).
