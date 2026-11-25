---
created: 2026-09-24
updated: 2026-09-25
---

# Builder creative upload: contract, routing and launch boundary

What an auto-ads-four uploader needs to know to put creatives into Builder, and what happens to them after. It maps Builder's upload (the replacement for `POST adloops.ai/api/creatives`) from source, and checks it against live BigQuery. Nothing was uploaded, approved or launched to establish any of this.

## Sources

| Source | What |
|---|---|
| Builder repo | `BookVitals-APP/onboarding_builder`, cloned at `_reference-repos/onboarding-builder-fresh-2026-09-24/`, `main` @ `131e7124db04bce2588791410eb69d3c5981804b`, fetched 2026-09-24T13:14:54Z |
| Builder deployment | GitHub deployment record: `Production` @ `131e7124d` 2026-09-24T11:55:52Z, Vercel status `success`. The cloned source is the deployed source. That `builder.thebiblechat.com` serves this deployment is taken from repo docs (`docs/ads-pipeline/GO-LIVE.md` CORS origin, `plans/08`) |
| Engine | `BookVitals-APP/ads-library-automation` `main` @ `221dcb85`, cloned 2026-09-24T15:53Z at `_reference-repos/ads-library-automation-fresh-2026-09-24/` (dependencies installed in `functions/`). Treat its comments as claims to verify, not facts. Files: `functions/src/approvals/uploadGate.ts`, `functions/src/triggers/videos.ts`, `functions/src/triggers/statusProcessors/UploadVideoOnDefaultProvidersProcessor.ts` |
| Old app | `BookVitals-APP/Ads_Platform_Web` `main` @ `458b5461` (GitHub API): `app/api/creatives/route.ts`, `agents/ad-tester/agent/lib/routing.ts`, `.../config.ts` |
| Live data | BigQuery via the biblechat-analytics MCP, 2026-09-24: `bc-ads-tester.limited.videos`, `organised_data.dw__experiments`, `ads.marketing_ads_data` |

Paths are relative to the Builder clone unless prefixed `ALA/` (engine) or `APW/` (old app).

## The shape

```
auto-ads-four            Builder (upload door)                  Engine (bc-ads-tester)            Meta
─────────────            ─────────────────────                  ──────────────────────            ────
check-hashes  ─────────▶ which files exist?
upload-url    ─────────▶ mint docId + signed PUTs
PUT bytes     ─────────────────────▶ storage (R2 in production)
create        ─────────▶ write `videos` doc, approval_state=pending
                                   │
                                   ▼
                         held at status pending_approval ◀── engine gate (no Meta asset yet)
                                   │
              Review page: approve (marketing.ads approve)
                                   │
                                   ▼
                         media posted to config's default Meta account, status video_uploaded
                                   │
                  ┌────────────────┼──────────────────────┐
                  ▼                ▼                      ▼
            config_rules     eve ad-tester          manual launcher ──▶ campaign / ad set / ad
            (auto, budget)   (auto, budget)         (a person)
```

The two doors (old adloops, new Builder) coexist. Both write the same Firestore `videos` collection and feed the same engine.

## 1. Config and routing

| Question | Answer | Status |
|---|---|---|
| `configId` | `biblechat`. The verseread URL's UUID `b76f73e8-...` is Bible Chat's Builder app id, whose `firebase_id` is `biblechat` (`docs/superpowers/plans/2026-07-29-dev-137-secrets-migration.md:14`). Live: every Bible-study quiz experiment since 2026-08-20 carries `configId=biblechat`, as do their creatives | Verified (source + live) |
| Separate WEB config? | No. The WEB ad account is chosen at **launch** time, not upload time. The upload names the config; the config has several accounts | Verified (live) |
| WEB account for the Bible-study quiz | `act_851055460791534`. All Bible-study `.../en/bible-study/facebook` experiments since 2026-08-20 ran there (one outlier on `act_4448187495404491`), objective `WEB`, campaigns named "... Biblechat WEB ... Conversion IP 5 ...". Account name not read (no Meta access to that account); consistent with the separate WEB account in project memory | Verified (live), name unverified |
| Who launched them | One person (`userId 5IfVLKl0...`, no `ruleId`), 75 experiments. **No rule or agent has ever launched onto the Bible-study quiz** in that window | Verified (live) |
| `feature` | `daily_plan` works. It is the most-used feature on `biblechat` since July (3,467 uploads, latest 2026-09-23), and 187 of the Bible-study WEB creatives carry it. Note that `create` checks only that `feature` is present, never that it is in `features_config` (`app/api/ads/videos/create/route.ts:258`) | Verified (live) |
| `platform` | `IOS`. The Bible-study WEB launches use `platform=IOS` (one ANDROID campaign). On WEB it is a lane label; it picks the CPP only on app objectives (`docs/superpowers/specs/topic-tagging-and-cpp-routing.md:179-190`) | Verified (live) |
| `problem` | Builder's per-config problem dimension. Every config carries exactly one entry, named "Default" (`lib/ads/vids/AddVideoModal.tsx:273-302`). Its id is **not** in BigQuery (`problem` is write-only: `topic-tagging-and-cpp-routing.md:266`), and `create` does not validate it against the config | **Unknown: needs the id** |
| `automation_config/main` (ad-tester) | Read 2026-09-24. `dry_run: true`, `kill_execution_enabled: false`. Web route: `web_template_ref: fb_bc_short_funnel_test`, `web_campaign_name: "Bible Chat - Web Short Funnel - AutoTest"`. That template (`ad_templates/fb_bc_short_funnel_test`, published) targets `act_851055460791534`, pixel `1015386208074903`, `COMPLETE_REGISTRATION`, link `verseread.com/w/b76f73e8-.../en/bc-app-testing/facebook`. **That is a different quiz, not Bible-study** | Verified (Firestore) |
| `testDestination` | Read by the ad-tester (`APW/.../routing.ts:28-53`), which routes images to `web_short_funnel` whatever the field says. Also read by two enabled rules as an exclusion (`test_destination not_in [web_short_funnel]`, see section 6). It does not choose a URL | Verified (source + Firestore) |

**Identifier vocabularies.** Builder's `problem` is a config-level id with one value. Builder's `pain_point` is a tag-tree code (for example `REL-01`) that carries approval and assignment semantics. **Neither is the same as aa4's customer problem or framing ids, and neither should carry them.**

## 2. Authentication

- **Supported today: a signed-in Builder user in a browser.**
  - Sign-in is Google OAuth through Supabase (`app/(main)/(builder)/(auth)/login/page.tsx:26`).
  - The upload routes verify the Supabase session from **cookies only** (`lib/supabase/server.ts`, `lib/supabase/authUser.ts:33-39`). No `Authorization` header is read on `/api/ads/videos/*`.
  - The supported client is Builder's own upload modal (`lib/ads/vids/AddVideoModal.tsx`) on `/app/<app_id>/<surface>/growth/ads/vids`.
- **Permission.**
  - Upload needs `marketing.ads` `edit` on the Bible Chat app (`lib/ads/pipeline/mediaAccess.ts:114-118`, `lib/auth/modules.ts:121`).
  - Approve is a separate verb that deliberately does not imply edit (`lib/auth/capabilities.ts:16-21`).
  - The uploader's attribution (`uploaded_by`, `userId`, `companyId`, editor prefix) comes from their adloops `users` record, matched by email (`lib/ads/identity.ts`).
- **Operational limits.**
  - Sessions are refreshed by the proxy on page navigations only. `/api/*` is outside its matcher (`proxy.ts:98-117`). How an API-only caller behaves on an expired access token is unverified.
  - A resumed upload must be finished by the **same Supabase user**, because `create` adopts a pending doc only for the user who minted it (`lib/ads/pipeline/pendingUpload.ts:235-242`).
- **Not supported:** any machine or service credential. There is no API key, no service account and no bearer path on these routes. `ADLOOPS_TOKEN` does not apply. Driving these routes headlessly with a user's cookies would be a workaround, not a supported path.
- **Proposal (a Builder team change, not existing):** accept a bearer on `check-hashes`, `upload-url` and `create`, resolved to a Builder user and checked with the same `canWriteToConfig`. Builder already verifies MCP OAuth bearers against `oauth_access_tokens` in `app/api/mcp/images/upload/route.ts:19-36`, and that pattern is the smallest fit.

## 3. Adapter contract

Production evidence says the upload pipeline runs in **R2 mode**: since 2026-09-21, new `biblechat` docs store media under slot paths (`videos/{id}/portrait/...`), which only R2 mode writes (`lib/ads/pipeline/storage.ts:181`). GCS-mode docs use ratio paths (`videos/{id}/9:16/...`). Ratio-path docs keep arriving too, which fits the old adloops door still in use. `ADS_PIPELINE_WORKFLOW=on` is inferred from this, not read. The adapter must handle both `storage` values and echo whatever step 2 returns.

**One creative = one `upload-url` call = one `docId` = one group.** Both aspects go in the same call.

**Step 1.** `POST /api/ads/videos/check-hashes` (`app/api/ads/videos/check-hashes/route.ts`)
```json
{"hashes": ["<sha256_4x5>", "<sha256_9x16>"]}
→ 200 {"existing": []}
```
- The hash is SHA-256 hex of the file's bytes (`lib/ads/uploadUtils.ts:41-44`).
- At most 200 hashes per call.
- The response returns hashes only, **never doc ids**.

**Step 2.** `POST /api/ads/videos/upload-url` (`app/api/ads/videos/upload-url/route.ts`)
```json
{"configId": "biblechat", "mode": "videos",
 "files": [
   {"fileName": "<creative-id>_4x5.png",  "aspectRatio": "4:5",  "contentType": "image/png"},
   {"fileName": "<creative-id>_9x16.png", "aspectRatio": "9:16", "contentType": "image/png"}]}
→ 200 {"docId": "<20-char id>", "expiresAt": <ms>,
   "uploads": [
     {"filePath": "videos/<docId>/fourFive/<creative-id>_4x5.png", "key": "videos/<docId>/fourFive/<creative-id>_4x5.png",
      "uploadUrl": "<presigned>", "contentType": "image/png", "storage": "r2",
      "headers": {"Content-Type": "image/png", "If-None-Match": "*"}},
     {"filePath": "videos/<docId>/portrait/<creative-id>_9x16.png", "key": "...", "uploadUrl": "<presigned>",
      "contentType": "image/png", "storage": "r2", "headers": {"Content-Type": "image/png", "If-None-Match": "*"}}]}
```
- The same order as `files` is preserved.
- GCS mode instead returns `storage: "gcs"`, no `key`, ratio paths, and headers `{"Content-Type", "x-goog-if-generation-match": "0"}` (`:167-188`).
- Limits: 1 to 40 files. `fileName` is at most 200 chars, with no `/` or `\`, no control characters, and no `resubmit-` prefix (`:65-74`). Keep pipes out of file names.
- Aspect ratios: `9:16`, `4:5`, `1:1`, `16:9` (`lib/ads/pipeline/mediaFormats.ts:28-33`).
- Accepted image types: `image/png`, `image/jpeg` (extensions `png`, `jpg`, `jpeg`), plus `webp` and `gif` (`mediaFormats.ts:121-129`).
- The server never checks pixel sizes or that the ratio is true. It trusts the declared `aspectRatio`.
- URLs expire after 30 minutes.
- In R2 mode this call **already writes a gated pending `videos` doc** (`:199-205`).

**Step 3.** `PUT <uploadUrl>` with the raw bytes and exactly the returned `headers`. The URLs are create-only, so a second PUT to a landed key is refused.

**Step 4.** `POST /api/ads/videos/create` (`app/api/ads/videos/create/route.ts`)
```json
{"mode": "videos", "configId": "biblechat", "feature": "daily_plan", "problem": "<DEFAULT_PROBLEM_ID>",
 "testDestination": "web_short_funnel", "platform": "IOS", "providers": ["facebook"], "language": "english",
 "groups": [{"docId": "<docId>", "videoNameRaw": "aa4|<creative-id>|<batch-id>", "hashedId": "<sha256 of the first file listed>",
   "files": [
     {"filePath": "<from step 2>", "key": "<from step 2>", "storage": "r2", "aspectRatio": "4:5",  "fileName": "<creative-id>_4x5.png",  "contentType": "image/png"},
     {"filePath": "<from step 2>", "key": "<from step 2>", "storage": "r2", "aspectRatio": "9:16", "fileName": "<creative-id>_9x16.png", "contentType": "image/png"}]}]}
```
- Required: `configId`, `feature`, `problem`, `testDestination`, and at least one of `providers` (`:252-261`).
- `pain_point` and `assignment_id` are optional. Omit them: a non-approver may only send their own tag codes (`:262-277`).
- Every file path and key must sit under `videos/{docId}/`.
- Media are slotted as `4:5` to `raw_image.fourFive` and `9:16` to `raw_image.portrait`.
- The doc is written with `status: "new"`, `type: "image"` and `approval_state: "pending"`.

Interpreting the response:

| Response | Meaning | Action |
|---|---|---|
| `{"created":[{"docId","video"}],"skipped":[]}` | Doc written. `video` is the stored name after any editor prefix | Record `docId` + `video` |
| `skipped:[{"reason":"duplicate","hashedId"}]` | Some doc already has this `hashed_id`. **No doc id returned** | Reconcile from the local receipt (section 5) |
| `skipped:[{"reason":"already exists","docId"}]` | This `docId` names a doc the caller cannot adopt | Stop. Inspect with `GET /api/ads/videos/<docId>` |
| 400 / 403 / 401 | Validation, tenant, or session failure | Fix, or re-authenticate as the same user, then retry |

## 4. Identifier and measurement continuity

- **The durable key is the server-minted `docId`.** Live evidence shows a complete, name-independent chain:
  - `limited.videos.video_id` = the `docId`.
  - `organised_data.dw__experiments.videos_uploaded[]` carries `video_doc_id → ad_id` (for example `1pesCtT5ussF9KwRbiY9 → ad 120246879137810160`).
  - `ads.marketing_ads_data.adId` holds the daily performance.
- **Names survive, but they are not a safe key.**
  - The old door kept `aa4|creative-id|batch-id` intact into `video` and into Meta's `adName`. Builder does not parse `videoNameRaw`, and pipes are allowed there.
  - But Builder adds the uploader's editor number unless that number already appears as a standalone token (`lib/ads/uploadUtils.ts:28-33`). With editor number 4, `aa4|...` would count as already containing it and stay unprefixed. With other numbers it becomes `N.aa4|...`. Whether the uploader has an editor number is unknown (the old door never prefixed, so August names prove nothing). `GET /api/ads/me` shows it.
  - Name parsing is therefore not sufficient.
- **Recommended mapping.** Keep a local receipt per creative: `creative_id`, `batch_id`, `format`, customer problem, framing, `docId`, the stored `video` name, `hashedId`, and per aspect `{sha256, key, fileName}`.
  - Join to results as `docId → dw__experiments.videos_uploaded.ad_id → marketing_ads_data`.
  - Keep the pipe name as the human-readable secondary key.
  - Do not put aa4 ids into `problem`, `pain_point`, `feature` or `language`.
- **A Builder API change is not required for continuity**, because the receipt and `docId` chain are enough. One would be needed only if aa4 metadata must be visible inside Builder or joined in BigQuery without the receipt: an optional external-reference field on `create`.

## 5. Safe retry and resume

Rules the adapter must keep:
- **Fix the file order.** `hashedId` is the hash of the group's first file only. Always list the same aspect first (for example 4:5), and record which hash is `hashedId`. `create` never checks the second file's hash.
- **Persist the receipt with `docId` before the first PUT.**
- **Never mint a second `docId` for a creative whose PUTs have landed.** Finish `create` on the original `docId`.

| Checkpoint | Failure | Recovery | Basis |
|---|---|---|---|
| Before step 1 | Either hash already exists | Stop. That creative is in Builder (or its bytes are). Reconcile via the receipt or a human. Never re-upload | Source |
| After step 2, no PUT landed | Crash or abandon | The R2 pending doc is discarded by the sweep once URLs expire (30 min) and all files are not present. Nothing reaches Meta. Restart from step 2 after expiry | Source: `pendingUpload.ts:26-31, 441-476`, cron `app/api/cron/ads-pending-uploads` |
| Partial PUTs | Some aspects landed | Re-PUT only the missing ones within 30 minutes (a landed key refuses a second PUT, so treat "precondition failed" on a landed key as done). After expiry with files missing, the sweep deletes the doc and objects. Then start over with a new `docId` | Source |
| All PUTs landed, `create` failed or never ran | Doc is pending | **In R2 mode the sweep completes the doc on its own**: media written, no `feature`/`problem`/`test_destination`/`hashed_id`, still `approval_state: pending`. Retrying `create` with the same body **adopts** it (the uploader marker survives confirmation). So finish `create` as the same user. Leaving it produces an unlabeled record in the review queue | Source: `pendingUpload.ts:10-31, 235-242, 318-330`, `create/route.ts:485-501` |
| `create` succeeded, response lost | Unknown outcome | Retry the identical body. The existing `hashed_id` gives `skipped: duplicate` (no doc id). Then `GET /api/ads/videos/<docId>` from the receipt and confirm `video`, `hashed_id`, `approval_state` | Source (GET is company-scoped: `app/api/ads/videos/[id]/route.ts`) |
| Receipt lost | No docId | `check-hashes` proves existence only. Find by name in `limited.videos` (lags by the export) or ask a human. Do not re-upload | Live table, lag not measured |
| Session expired mid-sequence | 401 | Re-authenticate as the **same** user, then resume at the failed step with the saved `docId` | Source |
| GCS mode (if the flag is off) | PUTs landed, no `create` | No pending doc, no sweep: orphan objects nobody lists. Retry `create` on the same `docId` (`create()` succeeds since no doc exists) | Source |

Unknowns: how the sweep and pipeline treat a sweep-completed doc that lacks `feature`/`problem` downstream; sweep cadence (a cron in `vercel.json`, not timed here); and API-only refresh behaviour on an expired session.

## 6. Approval and launch boundary

- **Upload does not spend.**
  - Builder writes `approval_state: "pending"` on every upload (`create/approval.ts:35-51`).
  - The engine also stamps `pending` on any person-made upload from any door (`ALA/functions/src/approvals/uploadGate.ts`).
  - The engine's processor holds such a doc at `status: pending_approval` **before posting media to Meta or TikTok** (`ALA/.../UploadVideoOnDefaultProvidersProcessor.ts:19-37`).
  - Live: `pending_approval` docs appear daily since 2026-09-13.
- **Who approves.**
  - The Review page `growth/creative/review` needs `marketing.ads` `approve` on the Bible Chat app (`app/api/ads/approvals/route.ts:16,45`).
  - No separation of duties is enforced: a user holding approve may approve their own upload (`app/api/ads/approvals/decide.ts`).
  - Who holds approve is a Supabase role grant, not visible in source.
- **What approval triggers.**
  - Postgres is set to approved, then the Firestore mirror is set to `approval_state: approved`, and the pipeline's approval hook resumes (`decide.ts`).
  - The engine re-enters the processor, posts the media to the config's default Meta account for `providers`, and advances to `video_uploaded`.
  - From then on the creative is eligible for:
    - **config rules**, which launch on schedule with budget;
    - the **eve ad-tester**, which selects `status = 'video_uploaded'` in BigQuery;
    - the manual launcher.
- **This is not hypothetical.** Live: the August aa4 statics from the old door (ungated then) were launched by rules with no human action:
  - `jpPticS0EqcMxTSDpKNP`: "CPI-IMG - US - ANDROID", INSTALL, `act_697155031095732`, 2026-08-21 and 2026-08-25;
  - `IL2sSmkQvghsZEXbDszC`: "WEB - bible answers", onboardings URL, not the Bible-study quiz.

  Both last fired on 2026-09-08. Other rules were still launching through 2026-09-23.
- **Enabled rules, read 2026-09-24** (`config_rules/biblechat/rules`: 45 rules, 9 enabled). Only two take fresh Facebook image uploads (datasource `editor_videos`, `lookbackDays: 0`, daily at 18:00 UTC):

  | Rule | Takes | Excludes | Fires when | Builds |
  |---|---|---|---|---|
  | `biblechat_daily_cpi_android_facebook_images` | images, any platform | `test_destination = web_short_funnel` | 4+ images | "Testing Biblechat CPI - ... - images", INSTALL |
  | `IL2sSmkQvghsZEXbDszC` | images, `platform = IOS` | nothing on `test_destination` | 10+ images in the same UTC day, counting every uploader | "Biblechat Bible Answers - Adv+ ABO", WEB, Bible Answers onboarding page |

  The other seven rules are:
  - `biblechat_daily_cpi_android_facebook_by_creator`: Facebook videos only.
  - `biblechat_daily_tiktok_ios_us_creator_cbo`: TikTok videos only.
  - Five Monday scale rules: they read the CPI winners queue, not fresh uploads.

  None targets the Bible-study quiz.
- **What this means for F005** (6 images, `platform: IOS`, `testDestination: web_short_funnel`):
  - The CPI image rule skips it, because of the exclusion. The August aa4 images were caught because the old door wrote no `test_destination`.
  - The Bible Answers rule fires only if other uploaders add 4 or more iOS images the same UTC day. Live volume since 2026-09-09 is at most 2 per day.
  - Upload timing does not avoid it. `editor_videos` has two legs (`ALA/functions/src/experiments/datasources/`):
    - the Firestore leg: `status == video_uploaded`, inside `lookbackDays`;
    - a BigQuery catch-up leg: view `webapp.vw__videos_from_editors_not_tested`. It takes untested editor images from the last 2 days and stamps every row `createdAt = CURRENT_DATE()`, so `lookbackDays: 0` does not bound it. "Untested" excludes images already in a WEB experiment in the last 30 days.
  - The ad-tester is in dry run.
  - So, as of this read, no automatic system launches F005, and the Bible-study launch is a manual step.
- **Rules select on `status` alone.** Per the engine's own comment (`ALA/functions/src/experiments/datasources/approvalGate.ts`, citing `config+rules.ts` `editor_videos`), rules pick creatives by `status`, and a new gate now also requires `approval_state: approved`. Measured there: a creative rejected on 2026-09-15 was still launched into four new ad groups and spent $44.97.
- **No automatic approval exists in code for a person's upload.** Only machine uploader labels (`auto-template`, `AutoBot`, `ScaleBot`, and similar) and mixes are exempt (`ALA/functions/src/approvals/uploadGate.ts`). The operator reports that their creatives are approved automatically in practice (policy or a person, not code). Under that practice, **upload is the spend moment**: minutes after upload, the creative can be at `video_uploaded` and eligible for the next rule sweep. Observed sweep times are on the hour (08:07, 14:01, 17:01, 18:01 UTC).
- **So approval is the effective spend authorization.** An approved F005 image may be picked up automatically by a rule or the ad-tester, onto a destination other than the Bible-study quiz. The quiz itself has only ever been reached by a manual launch.
- **Send-back does not pause ads.** Sending an approved video back to the queue holds it in the pipeline but does not pause ads already created (`decide.ts` comment).

## 7. Full automation path (upload, skip review, daily post to Bible-study)

The operator's goal: aa4 images skip human review, go to Meta, and a daily rule posts them to the Bible-study quiz. What exists, what is missing, and a draft. All facts are read-only, 2026-09-24.

**Skipping review.**
- The engine stamps `approval_state: pending` on every upload except machine uploaders. Machine uploaders are recognized by the `uploaded_by` labels in `AUTOMATED_UPLOADERS` (`ALA/functions/src/approvals/uploadGate.ts`), or an empty `uploaded_by`, or `mix`.
- Builder's new pipeline gates only a doc that carries an `approval_state` other than `approved` (`lib/ads/pipeline/steps/status.ts:211-221`). So an unstamped doc flows straight to Meta.
- Via the old door, `uploaded_by` is the token owner's display name. `fields` cannot override it: authoritative keys win (`APW/lib/creatives/creativeDoc.ts:181-216`).
- Builder's own `create` always stamps `pending`, so the Builder door cannot skip review without a Builder change.
- **The exemption, written 2026-09-24** (task 3):
  - What it adds: `AUTOMATED_PIPELINES` in `uploadGate.ts`. An upload is exempt only when three conditions are all true: `uploaded_by` is "Denis Durlescu" (case-insensitive), the name starts with `aa4|` (exact), and the doc has a non-empty string `aa4_creative_id`.
  - Why the marker field: the upload screens (Builder AddVideoModal, adloops modal) cannot set custom fields, so a hand upload named `aa4|...` stays held. A deliberate API/MCP call with the operator's token that sends the field still matches. Every exemption of a person's account has this risk. The dedicated account (task 9) removes it.
  - Where it is: PR #2324, branch `aa4-approval-exemption` (commits `3f0910f7` + `b99e0e3e` on `main` @ `221dcb85`), local copy in `_reference-repos/ads-library-automation-fresh-2026-09-24/`. Greptile's P1 comment ("manual uploads can bypass review") is answered on the PR by the marker fix.
  - Tests: `functions/tests/approvals/uploadGate.test.ts` (12 tests) plus the existing `approvalGate.test.ts` (9 tests) pass. `tsc --noEmit` is clean.
  - Scope: the old door does not add an editor-number prefix, so aa4 names arrive as written.
  - When a dedicated aa4 account exists, its label moves to `AUTOMATED_UPLOADERS`.
- This removes human review for aa4 output on a shared, spending account: a team-level choice.

**Who processes a new upload (since 2026-09-21 07:45:33 UTC).**
- The engine and Builder share the `videos` collection. `ADS_PIPELINE_FLIP_AT` (live value `2026-09-21T07:45:33Z`) splits ownership: every doc with `addedOn` at or after it belongs to Builder's workflow (`ALA/functions/src/pipeline/ownership.ts`, `lib/ads/pipeline/flag.ts`).
- The engine's `onCreateVideo` still runs the approval stamp first. It then skips all processing for docs that Builder owns (`ALA/functions/src/triggers/videos.ts:179-201`). So the exemption works on either side of the handoff.
- Builder's scan cron (`/api/cron/ads-pipeline-scan`, every 3 minutes) starts a workflow run for every doc added since the flip, also docs that Builder did not create. The old door writes `addedOn` as a server timestamp (`APW/lib/creatives/uploadCreativeCore.ts:217`), so the scan finds its docs.
- The workflow uploads stills to the Meta image library (`lib/ads/pipeline/platforms/metaSteps.ts:232`) and skips TikTok for stills. An ungated doc ends at `video_uploaded`, where the rules find it.
- Not seen in production yet: since the flip, all 207 new docs were Builder-created videos. No old-door doc and no image has gone through this path. The first aa4 batch is its first test.

**Old-door fields.**
- `fields` may add any key outside `PROTECTED_KEYS` (`APW/lib/creatives/creativeDoc.ts:56-67`). That includes `test_destination`, `creative_id`, `batch_id`, `format`, `framing`, and copy fields such as `primary_text` and `headlines`.
- Sending `test_destination: web_short_funnel` keeps `biblechat_daily_cpi_android_facebook_images` away, because that rule has no platform filter.
- Whether the old door still accepts `ADLOOPS_TOKEN` is untested. A test would be a real upload. The door is planned for retirement (`plans/08`).

**Meta asset.**
- An approved or ungated image is uploaded to Meta automatically on its way to `video_uploaded`. No separate script is needed.
- A Bible-study image that ran on `act_851055460791534` carries Meta assets under both businesses: `173558290375515` (Basmo iOS) and `3153913884770731` (WEB account owner). Checked on `videos/UrkIgq6TSXCJgcZvShVj`. Which step places the WEB-business copy is not established.

**Bible-study launch settings.** Read from `experiments/A0RAhgwJ4qkO41PnntVT`, manual, 2026-09-23:

| Setting | Value |
|---|---|
| Engine and template | `engine: template`, `templateKey: fb_bc_web2app` v4 |
| Account and business | `act_851055460791534`, business `3153913884770731` |
| Facebook page | `1236062592916008` |
| Pixel and event | `1777679486641648`, `PURCHASE`, `OFFSITE_CONVERSIONS` |
| Attribution | 7-day click, 1-day view |
| Ages | 20 to 65 |
| Objective | `OUTCOME_SALES` |
| Link | `https://verseread.com/w/b76f73e8-a42b-4410-8a3b-9f6fef2e6213/en/bible-study/facebook/` |
| Daily budget | 40000 (a scale campaign) |

**How a rule builds ad sets** (`ALA/functions/src/experiments/add/TestingExperimentsBuilder.ts`):
- `groupVideosPattern` is a waterfall of patterns. Each `{field}` resolves to that field on the image record, or `none`.
- A group is kept once it reaches the minimum; the rest fall to the next pattern, then into one `___remaining` group.
- Derived fields are `type`, `audience_tier`, and `visual_template`. `visual_template` is parsed from the name: `aa4|t-newspaper-front-v1--...` gives `t-newspaper-front-v1` (`visualTemplate.ts`).
- `problemFromName` exists but is not wired into grouping.
- A rule with `template` clones that **experiments** doc. It must declare `experimentExtraParams.account_id` and `business_id`, matching the template, or it refuses. It needs `budgetFromTemplate: true` when the template owns the budget (`templateClone.ts`).
- **Filters, and which leg honours them:**

  | Filter form | Firestore leg | BigQuery catch-up leg |
  |---|---|---|
  | Plain `field: "value"` | Equality on the image record | SQL `field = 'value'`, so the column must exist in the view |
  | Object filters (`not_in`, `is_empty`, `is_not_empty`) | Applied to the image record in memory | Applied in memory after hydration (`objectFilters.ts`) |
  | `extra` (SQL strings) | **Skipped** (`BaseFirestoreVideosDataSource.ts:63-65`) | SQL |

  - A name-prefix condition is therefore not expressible for the Firestore leg.
  - The rule identifies aa4 images by a field only aa4 writes: `aa4_creative_id` with `is_not_empty`.
  - The view's columns include `uploaded_by`, `video_name` (not `video`), `platform`, `type` and `provider`.

**The rule, saved switched off.**
- Record: `config_rules/biblechat/rules/biblechat_daily_aa4_images_web_bible_study`, created 2026-09-24 16:29 UTC with `enabled: false`. After the write there were 46 rules, 9 enabled, the same 9 as before. A local copy of what was written is in the session scratchpad as `aa4_rule_saved.json`.
- A switched-off rule does not run: `loadConfigRules` drops it (`ALA/functions/src/config/load.ts:135`), and `addExperimentsTasks` checks `enabled` again (`ALA/functions/src/experiments/add/utils.ts:92`). Only `src/test/experiments.ts --includeDisabled` loads it, and that path requires `--debug true`.
- Record id and the `id` field both carry the rule's name, as in the other named rules. The loader maps the `id` field to `local_id`.
- Fields:
```json
{
  "id": "biblechat_daily_aa4_images_web_bible_study",
  "enabled": false,
  "description": "PREPARED, NOT ENABLED ... BUDGET: template Y3vv8pRpRN0pa45P7aJf spends $350/day PER AD SET ...",
  "cron": "0 18 * * *", "lookbackDays": 0,
  "adProvider": "facebook", "platform": "IOS", "videoTypes": ["image"],
  "datasource": "editor_videos",
  "datasourceExtraFilters": {"platform": "IOS", "uploaded_by": "Denis Durlescu",
    "aa4_creative_id": {"type": "is_not_empty"}},
  "campaignObjectiveType": "WEB", "engine": "template",
  "template": "Y3vv8pRpRN0pa45P7aJf",
  "budgetFromTemplate": true,
  "experimentExtraParams": {"account_id": "act_851055460791534", "business_id": "3153913884770731"},
  "groupVideosPattern": ["{visual_template}", "{type} {uploaded_by}"],
  "minVideosToRunExperiment": 3, "maxAdsPerAdgroup": 6,
  "campaignNamePattern": "BS Biblechat WEB - aa4 - {countries} - {platform} - {month}",
  "languageCountryBudget": {"english": {"US": 0}},
  "updatedAt": "2026-09-24T16:29:08.000Z"
}
```

**The template launch, and why the budget is open.**
- `Y3vv8pRpRN0pa45P7aJf` is the newest US iOS Bible-study launch on act_851055460791534 (2026-09-23, "Weekly Scale BS", engine `template`, key `fb_bc_web2app` v4, status `uploaded`). Link `https://verseread.com/w/b76f73e8-a42b-4410-8a3b-9f6fef2e6213/en/bible-study/facebook/`, pixel 1777679486641648, event PURCHASE, iOS 17+, age 20 to 65, page 1111213102084309, ad-set budget 35000 cents.
- On the template engine only the template's budget is spent; `experiment.budget` is never read (`ALA/functions/src/experiments/add/templateClone.ts:131-155`). So the rule spends $350/day per ad set until `template` points at a launch with the intended test budget.
- The 53 Bible-study launches on the account run $200 to $400 per ad set per day. All were set up by Arthur Nastasa. None is a small test budget.
- The template's creative is a video ad (`video_data`). The template engine turns an image asset into `link_data` with the image hash and keeps the template's link and button (`ALA/functions/src/campaigns/facebook/template/runFacebookTemplateCampaign.ts:344-370`). Evidence it works live: two image ad sets, "BS - Images - CBO" (`IZddilE52bT2f5Ugol9K`, `VKk4341f9Ahppq5TdzW1`, 2026-09-11), cloned the same kind of template to the same link and reached `uploaded`. They use a campaign budget ($1,000/day) and a different page (934187293105087).

- **The grouping pattern must not use AI-classified fields** (`{problem}`, `{hook_type}`, `{visual_style}` and the rest of `CLASSIFIED_FIELDS`). Those make the builder call a model and write the result onto image records, even in a dry run (`TestingExperimentsBuilder.ts:438-548`). `{visual_template}`, `{type}` and `{uploaded_by}` trigger no writes.
- **Dry run, prepared** in the same clone at `functions/scripts/local-aa4/`, excluded from git through `.git/info/exclude`:
  - `aa4-rule.draft.json`: an earlier local copy of the rule; the saved record above is the reference.
  - `dry-run-aa4-rule.ts`: blocks every Firestore write and every Meta or TikTok request before engine code loads. Its `--selftest` passed 7 of 7 blocks.
  - Run: `npx tsx scripts/local-aa4/dry-run-aa4-rule.ts --template Y3vv8pRpRN0pa45P7aJf` from `functions/`, after `gcloud auth application-default login`.
  - Library versions: resolved fresh (the repo has no lockfile), and npm skipped some packages' install scripts.
- **To confirm in the dry run:** the launch orders it would write, their account, link and budget, and the group sizes against the per-set caps.

**Collision.** `IL2sSmkQvghsZEXbDszC` (Bible Answers: iOS images, no `test_destination` or uploader filter, 10 or more per sweep including the catch-up leg, 18:00 UTC) would also sweep aa4 images. Dedupe is per rule, so nothing established stops one image entering both rules. The fix that both legs honour: add `aa4_creative_id: {type: "is_empty"}` to that rule's `datasourceExtraFilters`.

**On-demand trigger.**
- Upload: aa4's own `src/operations/upload-batch.ts`.
- Launch now, instead of waiting for 18:00: the engine's `functions/scripts/ad-launch` (`templates` / `videos` / `plan`, dry run by default, `--apply` launches, all documents written in one batch, audit log).
- The older `functions/src/test/catchup-4ijm.ts` exists only in the 2026-09-08 local engine copy. It ran a rule recipe on demand and is superseded.
- Both need a local engine checkout with dependencies, plus `gcloud auth application-default login`.

## Chosen path and task list

Decided with the operator on 2026-09-24:
- aa4 keeps uploading through the old adloops door, with the operator's own account and token for now.
- A narrow engine exemption lets aa4 output skip review.
- A new rule posts aa4 images daily to the Bible-study quiz.
- A dedicated aa4 account replaces the operator's account later.

The Builder-door contract (sections 2 to 5) stays as reference for the day the old door is switched off.

**Definition of done (proposed 2026-09-25, awaiting Denis's confirmation with the aa4 agent):** the 6 F005 aa4 images are live as ads on one Bible-study ad set, launched by hand. Left out: the automatic rule, budgets beyond one test ad set, a Builder script door. Next steps: Denis gets the approver role from Stefan (asked 2026-09-25), approves the 5 hand uploads, then launches all 6 via Create campaign > Template > Bible Chat web2app > Previous configs > Arthur's 2026-09-23 launch > Use again, at a test budget. No stop policy covers the ad set, so it is turned off by hand.

**Identity of aa4 output**: `uploaded_by = "Denis Durlescu"` AND the `aa4_creative_id` field. The exemption also checks the name prefix `aa4|`. The rule checks only the field, because rule filters cannot match a name prefix on the Firestore leg. The operator's account is used for no manual uploads through the old door or the MCP. Uploads through Builder's own page are held regardless.

| # | Task | Owner | Depends on |
|---|---|---|---|
| 1 | Done 2026-09-24, not committed: `auto-ads-four/src/operations/upload-batch.ts` sends `fields.aa4_creative_id` (= `creative_id`) and `fields.test_destination = "web_short_funnel"`; names keep `aa4\|`. Tests 106/106. The file also carries other uncommitted aa4 work, so the aa4 thread commits it. `ADLOOPS_TOKEN` (operator's `al_at_` token, valid to 2027-07-09) is in `auto-ads-four/.env.local` (gitignored); the CLI reads only the shell env, so a run needs it exported | aa4 thread commits | |
| 2 | Done 2026-09-24 17:04:50 UTC: one F005 image (`parenting-overwhelm--a01`) uploaded, doc `0DjFGzGglH9uwZsh2SH4`, ledger receipt written; the other 5 F005 rows untouched. Proven: old door and token work, fields land, engine skips review, Builder scan claims it within 2 min. Reached `video_uploaded` 2026-09-24 18:39 UTC after a Modal outage (see blockers). The other 5 F005 images were uploaded by hand through Builder's screen on 2026-09-25 08:29 UTC (docs `7F0O7pR4Gj5rNwiVMwQO`, `gce3A0ygQgsXZYZdGAXZ`, `HNpwHGHWazlhoZpzVpAZ`, `oY1TWwXLAD5KLvioyEa8`, `cHLnuHYOksNVlWWmyuZt`; both sizes each, Web, Meta only), so their ledger rows stay unuploaded and must not be sent again. They carry no `aa4_creative_id`, so they wait at `pending_approval` for an approver (the operator has no approver role yet) and the aa4 rule does not match them | Done | 1 |
| 3 | Engine exemption: PR https://github.com/BookVitals-APP/ads-library-automation/pull/2324 (commits `3f0910f7` + `b99e0e3e`), merged 2026-09-24 16:17 UTC, deployed by Stefan Dirlea 2026-09-24 17:02:27 UTC (function hash `a3c4f2b0`). Verified live on doc `0DjFGzGglH9uwZsh2SH4`: no approval stamp, handed to the workflow | Done | |
| 4 | Template chosen: `Y3vv8pRpRN0pa45P7aJf` ($350/day per ad set). Open: the test budget. If lower, create a template launch at that budget (with `ad-launch`) and point the rule at it | Operator decides the budget | |
| 5 | Done 2026-09-24 17:12:59 UTC: `IL2sSmkQvghsZEXbDszC` (Bible Answers, enabled) gained `datasourceExtraFilters.aa4_creative_id: {type: "is_empty"}`; nothing else on the rule changed. Both legs apply object filters in memory on the hydrated Firestore doc (`ALA/functions/src/experiments/datasources/bigquery/BaseBigQueryVideosDataSource.ts:68-105`), so no view column is needed. Undo: remove that one key | Done, operator approved | |
| 6 | Dry run (section 7, prepared): needs `gcloud auth application-default login`. Real aa4 images appear in it only after tasks 1 to 3 | This workspace | 4 |
| 7 | Rule record written with `enabled: false` (2026-09-24). Remaining: enable it after the dry run and the budget decision | Operator approves enabling | 1, 3, 4, 5, 6 |
| 8 | Day after the first live run: check `dw__experiments` for aa4 docIds and confirm only the new rule took them | Next session | 7 |
| 9 | In parallel: request a dedicated aa4 email and account; find the old door's switch-off date (`NEXT_PUBLIC_ADS_UPLOADS_MOVED`, `plans/08`) | Operator | |
| 10 | Builder script door (one Builder PR): token login on `/api/ads/videos/*` (Builder can accept the same `al_at_` tokens, stored in `mcp_oauth_tokens`), plus the aa4 exemption in Builder's `create` (it always stamps `pending`). Then aa4 switches to the 4-step signed-URL upload and files land in Cloudflare R2 directly. Pairs with task 9 | This workspace writes, Builder owner reviews | 9 |
| 11 | Settle the old-door storage split: old-door files land in Firebase Storage and Cloudflare copies them on first view, so first views can be blank and deletes need a manual Firebase cleanup (see blockers). Options: live with it; ask Stefan to make the old door write to R2; or task 10 removes it. Ask Stefan together with task 9's switch-off question | Operator asks Stefan | 9 |

**Known blockers:**
- **Modal image app outage, 2026-09-24 17:06 to about 18:00 UTC (resolved).** The aa4 image `0DjFGzGglH9uwZsh2SH4` timed out at prep three times ("no prep callback within 900s"). Test uploads after 18:00 all passed prep on the same app (`ads-seal-prod`) in about 3.5 minutes: Builder screen, one size (`jXytHJ3uIW3DekmmpDCs`); old door, one size (`ymiTB7YyawNXqmg4DIwF`); old door, two sizes (`HrTz7BGdsuhL3tFZD6wO`). The scan then retried the aa4 image at 18:36:30 (beyond the documented 3 automatic starts) and it reached `video_uploaded` at 18:39:11 with a Meta image hash. Nothing alerted on the outage. If prep stalls again, the logs are Vercel → Observability → Workflows and `modal app logs ads-seal-prod` (`doc=<id>`), both Stefan's.
- **Meta library business.** The aa4 image's Meta upload landed under business 173558290375515 (account `act_697155031095732`, the Basmo / Bible Answers account). The aa4 rule launches on `act_851055460791534` (business 3153913884770731). Unverified whether the template launcher uploads the image to that business at launch or fails with "has neither an uploaded video, image, nor carousel for the business yet" (`runFacebookTemplateCampaign.ts:454`). Check in the dry run before enabling the rule.
- **Deleting a creative.** Builder has no delete for creatives. Deleting the Firestore doc runs the engine's `onDeleteVideoDoc`: it asks Builder to remove the R2 objects and drops the doc from experiments, with no Meta calls (Meta library copies stay, unused). For old-door uploads it skips the Firebase Storage originals ("media is in R2, removed by the builder"), so remove `gs://bc-ads-tester.firebasestorage.app/videos/<docId>/**` by hand. Cloudflare may keep serving a cached copy of a deleted file for a while. The 2026-09-24 test uploads were removed this way.
- Builder processing capacity: 4 sandbox slots by default (`lib/ads/pipeline/pool.ts`, `ADS_SANDBOX_CONCURRENCY`), about 7 min per video seal, shared with the team. Upload in batches of 10 to 25.
- Old-door files live in Firebase Storage; the Cloudflare CDN (`bcdn.thebiblechat.com`) copies them on first request, so the first view of a new old-door image can be slow or partial.
- The old door's switch-off stops both automated upload and the exemption. Builder would then need a script login and the same exemption.
- Minting new `al_at_` tokens may stop working if the adloops MCP sign-in is retired.
- The operator's token expires 2027-07-09.
- An engine maintainer could remove a person-named exemption.
- Rules and the ad-tester are live data that others edit. Re-read `config_rules/biblechat/rules` before each change.
