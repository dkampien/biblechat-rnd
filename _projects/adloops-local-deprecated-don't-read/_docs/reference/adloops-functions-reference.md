# AdLoops Cloud Functions Reference

> **60 functions** deployed to `europe-west1` | Project: `adloops-local`
>
> Last updated: 2026-01-11

---

## Quick Stats

| Type | Count |
|------|-------|
| Firestore Triggers | 42 |
| Scheduled Functions | 8 |
| Pub/Sub Triggers | 7 |
| HTTP Functions | 7 |
| **Total** | **60** |

---

## VIDEO PROCESSING PIPELINE (5)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateVideo` | Firestore create | triggers/videos.ts | Processes new videos: probes duration, detects content type, generates previews |
| `onUpdateVideo` | Firestore update | triggers/videos.ts | Handles status changes, delegates to processVideoByStatus |
| `onDeleteVideoDoc` | Firestore delete | triggers/videos.ts | Cleans up previews, updates related image-parts |
| `retryToProcessVideosHttp` | HTTP | triggers/videos.ts | Manual retry for stuck videos |
| `retryToProcessVideosScheduler` | Scheduled (10min) | triggers/videos.ts | Auto-retry stuck videos |

**Flow:** `onCreateVideo` → preview → `onUpdateVideo` → processVideoByStatus → generateAdContent

---

## VIDEOMIX PIPELINE (8)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateMixes` | Firestore create | triggers/mixes.ts | Initializes mix, runs MyVideoMixBuilder |
| `onUpdateMixes` | Firestore update | triggers/mixes.ts | Handles RETRY/PAUSED/RUNNING/READY transitions |
| `onDeleteMixes` | Firestore delete | triggers/mixes.ts | Cascade deletes all parts |
| `onCreateMixPart` | Firestore create | triggers/mixes.ts | Creates worker task for video generation |
| `onUpdateMixPart` | Firestore update | triggers/mixes.ts | Monitors completion, marks parent "ready" |
| `onDeleteMixPart` | Firestore delete | triggers/mixes.ts | Cascade deletes video, decrements counters |
| `videoMixTemplateSchedulerPubSub` | Pub/Sub | videomixes/pubsub.ts | Builds influencer mix templates |
| `autoVideoMixTemplateSchedulerPubSub` | Pub/Sub | videomixes/pubsub.ts | Processes auto-templates |

**Flow:** `onCreateMixes` → `onCreateMixPart` (per part) → `onUpdateMixPart` → `onUpdateMixes` (ready)

**Status flow:**
```
VideoMix: new → running → ready → uploaded
               ↓
             error
```

---

## IMAGEMIX PIPELINE (6)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onImageMixCreated` | Firestore create | triggers/imageMixes.ts | Initializes image mix, runs MyImageMixAutoTemplateV2 |
| `onImageMixUpdated` | Firestore update | triggers/imageMixes.ts | Handles "retry" - deletes parts, regenerates |
| `onImageMixDeleted` | Firestore delete | triggers/imageMixes.ts | Cascade deletes image-parts |
| `onImagePartCreated` | Firestore create | triggers/imageParts.ts | Processes part with MyImagePartProcessor |
| `onImagePartUpdated` | Firestore update | triggers/imageParts.ts | Supports "retry" status |
| `onImagePartDeleted` | Firestore delete | triggers/imageParts.ts | Cascade deletes videos with matching part_id |

**Status flow:**
```
ImageMix: new → processing → completed
                    ↓
                  error | retry
```

---

## VIDEO COMPONENTS (11)

### Bodies (3)
| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateBodies` | Firestore create | triggers/bodies.ts | Processes new body component |
| `onUpdatedBodies` | Firestore update | triggers/bodies.ts | On "download_done" → process, on "tagged" → generate content |
| `onDeleteBodies` | Firestore delete | triggers/bodies.ts | Cleans up previews |

### Hooks (3)
| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateHook` | Firestore create | triggers/hooks.ts | Processes hook, increments affiliate count |
| `onUpdateHook` | Firestore update | triggers/hooks.ts | Syncs affiliate preview URL |
| `onDeleteHook` | Firestore delete | triggers/hooks.ts | Deletes part, decrements count |

### CTAs (3)
| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateCTAs` | Firestore create | triggers/ctas.ts | Processes new CTA |
| `onUpdatedCTAs` | Firestore update | triggers/ctas.ts | On "download_done" → process |
| `onDeleteCTAs` | Firestore delete | triggers/ctas.ts | Cleans up |

### Overlays (2)
| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateOverlay` | Firestore create | triggers/overlays.ts | Generates preview, extracts raw_video |
| `onUpdateOverlay` | Firestore update | triggers/overlays.ts | Regenerates preview on fileName change |

---

## SCRIPTS & AUDIO (2)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateScript` | Firestore create | triggers/scripts.ts | Generates voice audio using MyAudioGenerator |
| `onUpdateScript` | Firestore update | triggers/scripts.ts | Regenerates audio and SRT subtitles |

---

## EXPERIMENTS/CAMPAIGNS (10)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateExperiments` | Firestore create | triggers/experiments.ts | Creates campaign on FB/TikTok/Snap/Pinterest |
| `onDeleteExperiments` | Firestore delete | triggers/experiments.ts | Removes from videos, deletes from provider APIs |
| `addExperimentsPubSub` | Pub/Sub | experiments/pubsub.ts | Rule-based experiment creation |
| `runConfigRuleActionsPubSub` | Pub/Sub | experiments/pubsub.ts | Executes config rule actions |
| `runConfigRulesScheduler` | Scheduled (hourly) | experiments/pubsub.ts | Queues experiment creation tasks |
| `runConfigRulesActionsScheduler` | Scheduled (hourly) | experiments/pubsub.ts | Executes rule actions for all configs |
| `runExperimentsScheduler` | Scheduled (10min) | experiments/pubsub.ts | Creates campaigns for "new" experiments |
| `runFacebookAdDeepLinkFixerScheduler` | Scheduled (daily 11:00) | experiments/pubsub.ts | Fixes FB ad deep links |
| `uploadFeaturesConfigHttps` | HTTP | experiments/index.ts | Admin: uploads features_config |
| `uploadRulesV2Https` | HTTP | experiments/index.ts | Admin: uploads testing rules |

**Providers supported:** Facebook, TikTok, Snapchat, Pinterest

---

## REPORTING & ANALYTICS (6)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `updatePartsFromVideosWithPotentialPubSub` | Pub/Sub | reporting/pubsub.ts | Evaluates video performance, scales ads |
| `updateVideoLabelsPubSub` | Pub/Sub | reporting/pubsub.ts | Updates performance labels |
| `runAdReportsScheduler` | Scheduled (hourly) | reporting/ads/index.ts | Publishes report tasks to Pub/Sub |
| `runAdReportsPubSub` | Pub/Sub | reporting/ads/index.ts | Fetches from FB/TikTok/Snap/Pinterest → BigQuery |
| `runAdReportsSyncScheduler` | Scheduled | reporting/ads/index.ts | Syncs BigQuery → Firestore |
| `syncYesterdayVideoSpendDataPubSub` | Pub/Sub | bigquery/pubsub.ts | Syncs yesterday's spend to Firestore |

**Flow:**
```
runAdReportsScheduler (hourly)
        ↓
runAdReportsPubSub → BigQuery
        ↓
syncYesterdayVideoSpendDataPubSub → Firestore
        ↓
updatePartsFromVideosWithPotentialPubSub (scale ads)
```

---

## USERS, JOBS, INFLUENCERS (5)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onCreateUser` | Firestore create | triggers/users.ts | Initializes user, creates affiliate jobs |
| `onUserUpdated` | Firestore update | triggers/users.ts | Creates jobs when becoming affiliate |
| `onUpdateJob` | Firestore update | triggers/jobs.ts | Processes job status, advances queue |
| `updateInfluencerStatuses` | Scheduled (daily) | Influencers/InfluencerScheduler.ts | Updates status from Supabase |
| `signContracts` | Scheduled | Influencers/InfluencerScheduler.ts | Generates PDF contracts |

---

## OTHER (7)

| Function | Type | Path | Summary |
|----------|------|------|---------|
| `onUpdatedBriefs` | Firestore update | triggers/briefs.ts | Awards points when brief "approved" |
| `onUpdatedAIVideos` | Firestore update | triggers/aiVideos.ts | On "completed" → creates video mixes |
| `adaptyWebHookHttps` | HTTP | webhooks/adapty/index.ts | Receives payment/subscription events |
| `fixBrokenFeaturesHttps` | HTTP | test/https/upload.ts | Admin: fixes broken features from BigQuery |
| `fixVideosGroupsHttps` | HTTP | test/https/upload.ts | Admin: fixes video groups |
| `fixRunningExperimentsHttps` | HTTP | test/https/upload.ts | Admin: reruns stuck experiments |
| `fixUploadingVideosHttps` | HTTP | test/https/upload.ts | Admin: reprocesses videos |

---

## Key Architecture Patterns

### 1. Event-Driven State Machine
Functions react to Firestore document changes. Status field drives transitions:
- `new` → `processing` → `ready` → `uploaded`
- Error states trigger retry logic

### 2. Worker Queue Pattern
Heavy processing uses Pub/Sub topic `"video-mix-processing-v3"` to defer work to background workers.

### 3. Cascade Delete Pattern
Parent document deletion triggers child cleanup:
- `onDeleteMixes` → deletes all `parts`
- `onImageMixDeleted` → deletes all `image-parts`
- `onDeleteVideoDoc` → cleans up previews

### 4. Multi-Provider Abstraction
Experiments abstract provider logic through factory classes:
- FacebookUtils, TiktokUtils, PinterestUtils
- Provider-specific campaign creation/deletion

---

## Collections Watched

| Collection | Triggers |
|------------|----------|
| `videos` | create, update, delete |
| `videoMixes` | create, update, delete |
| `videoMixes/{id}/parts` | create, update, delete |
| `image-mixes` | create, update, delete |
| `image-parts` | create, update, delete |
| `bodies` | create, update, delete |
| `hooks` | create, update, delete |
| `ctas` | create, update, delete |
| `overlays` | create, update |
| `scripts` | create, update |
| `experiments` | create, delete |
| `users` | create, update |
| `jobs` | update |
| `briefs` | update |
| `ai-videos` | update |

---

## How to Count Functions

```bash
# From deployed (source of truth)
firebase functions:list --project adloops-local | grep "v2" | wc -l

# From code (approximate)
cd functions/src
grep "export \* from" index.ts | grep -v "^//" | \
  sed 's/export \* from "//' | sed 's/";//' | \
  while read file; do
    grep -cE "^export const \w+ = (onDocument|onSchedule|onMessagePublished|onRequest)" "${file}.ts" 2>/dev/null
  done | awk '{sum+=$1} END {print sum}'
```

Note: Code count may include commented-out functions. Deploy count is authoritative.
