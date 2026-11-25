# AdLoops System Analysis

> Extracted from codebase exploration. Use this as context for ContentLoops integration work.
>
> **Last validated:** 2026-01-09 against `_projects/_adloops/` codebase
>
> **For seed data:** This doc shows TypeScript types. For exact field VALUES required (e.g., `"english"` not `"en"`, `"portrait"` lowercase), see `adloops-firestore-schema-complete.md`

## Repository Structure

Three repos in `_adloops/`:

| Repo | Purpose | Tech | Notes |
|------|---------|------|-------|
| `Adloops-Backend` | Influencer/Supabase backend | Deno, Supabase | **Separate system** - not part of video pipeline |
| `Ads_Platform_Web` | Dashboard/UI | Next.js, TypeScript | Dual data: Firestore + Supabase |
| `ads-library-automation` | Core video automation engine | Firebase Functions, TypeScript | **Main codebase** for video pipeline |

> **Note:** `Adloops-Backend` handles influencer management, contracts, and Supabase features. The video pipeline lives entirely in `ads-library-automation`.

---

## Core Concepts (Data Model)

### Components - The Raw Building Blocks
Stored in Firestore collections:

- **`hooks`** - Attention-grabbing openings (first 1-3 seconds)
- **`bodies`** - Main content/story
- **`ctas`** - Call-to-action endings
- **`overlays`** - Visual elements layered on top (text, graphics)
- **`audios`** - Background music, sound effects
- **`scripts`** - Text content for voice generation

Each component (IHook, IBody, ICta) has:
```typescript
interface IHook {  // IBody and ICta have same structure
  // Required fields
  _firestore_id: string;
  video: string;
  raw_video: {
    portrait?: IFile;
    square?: IFile;
    landscape?: IFile;
    tiktok?: IFile;
  };
  preview: {
    fileName: string;
    fileURL: string;
    format: string;
    fullSize?: IFullSize;
  };
  extracted_texts: string[];
  duration: number;
  language: string;
  userId: string;
  companyId: string;
  status: string;
  status_updated: Date;
  uploaded_by: string;
  used_count: number;
  extracted_timestamp?: Date;

  // IHook-specific fields
  addedOn?: IAddedOn;
  excellent_count?: number;
  good_count?: number;
}
```

### Templates - The Blueprints
Two types:

**Manual Templates** (`templates` collection):
```typescript
interface IInfluencerTemplate {
  // Required fields
  hooks: IHook[];
  bodies: IBody[];
  ctas: ICta[];
  overlay: IOverlay[];
  audios: IAudio[];
  captions: ICaption;
  name: string;
  language: string;
  hookTimeLimit: number;
  bodyTimeLimit: number;

  // Optional fields
  _firestore_id?: string;
  mergeBodies?: boolean;
  crossFadeDuration?: number;
  backgroundMusicVolume?: number;
  instructions?: string[];
  templateNumber?: number;
  limitVideos?: number;
}
```

**Auto Templates** (`autoMixTemplates` collection):
```typescript
interface IMyVideoMixAutoTemplate {
  groups: MyVideoMixSourceTemplateGroup[];  // Field definitions
  translate: string[];      // Languages to generate
  language: string;         // Base language
  interval: number;         // Hours between runs
  last_generation: Timestamp;
  prompt: string;           // For voice/overlay generation
  voiceName: string;
  dataSource: string;       // Where to pull data from
  tiktokAccounts?: string[];
  facebookPages?: string[];
  outputTargets: string[];
}
```

### Video Mix - One Recipe Execution
When a template runs, creates a `videoMix` document:
```typescript
interface MyVideoMix {
  // Required fields
  id: string;
  name: string;
  identifier: string;
  components: Record<string, string[]>;  // e.g., { hook: ["id1"], body: ["id2", "id3"] }
  overlay: MyVideoMixOverlay[];
  status: MyVideoMixStatus;  // new, running, ready, uploaded, paused, retry, error
  templateFormat: string;    // Which template created this
  companyId: string;
  configId: string;
  userId: string;
  uploaded_by: string;

  // Optional fields
  voice?: MyVideoScriptAudioFile[];
  language?: string;
  affiliate?: boolean;       // Organic vs paid
  tiktokAccountId?: string;
  facebookPageId?: string;
  captions?: MyVideoMixCaptions;
  captionsOffset?: number;
  mergeBodies?: boolean;
  mergeOverlays?: boolean;
  crossFadeDuration?: number;
  hookTimeLimit?: number;
  bodyTimeLimit?: number;
  bodyOffset?: number;
  audioOffset?: number;
  audioVolume?: number;
  backgroundMusicVolume?: number;
  backgroundMusicOffset?: number;
  translate?: string[];
  resolution?: ImageResolution;
  platform?: PLATFORM;
  endAfterScript?: boolean;
  instructions?: string;
  templateId?: string;
  mixConcept?: string;
  previews?: Record<string, string[]>;
  made_by?: string;
  tiktokAccounts?: Record<string, TiktokAccount>;
}
```

### Part - One Actual Video Variant
Each Mix generates multiple Parts (subcollection `videoMixes/{id}/parts`):
```typescript
interface MyVideoMixPartDoc {
  // Required fields
  name: string;
  videoLayers: MyVideoMixPartLayer[];
  audioLayers: MyVideoMixAudioLayer[];
  overlay: MyVideoMixOverlayObject[];  // Both per-layer and cross-layer overlays stored here
  resolution: string;
  status: string;                      // new, running, ready, uploaded, paused, retry, error
  companyId: string;
  userId: string;
  uploaded_by: string;
  extracted_texts: string[];
  preview: MyAdPreview;

  // Optional fields - component references
  hook?: string;
  body?: string;
  cta?: string;
  script?: string;
  voice?: string;
  video_id?: string;  // Final rendered video ID

  // Optional fields - configuration
  srtFileName?: string;
  captions?: MyVideoMixCaptions;
  captionsOffset?: number;
  crossFadeDuration?: number;
  endAfterScript?: boolean;
  language?: string;
  templateFormat?: string;
  mixConcept?: string;
  instructions?: string;
  layers?: string[];

  // Optional fields - platform/tracking
  affiliate?: boolean;
  tiktokAccountId?: string;
  facebookPageId?: string;
  tiktokSongLink?: string;
  platform?: PLATFORM;
  scriptId?: string;
  autoScriptId?: string;
  audioId?: string;
  raw_video?: { portrait: { fileName: string } };
  hash?: string;
  uniqueToken?: string;
  made_by?: string;
}

interface MyVideoMixPartLayer {
  videos: string[];                      // Component video file paths
  overlay?: MyVideoMixOverlayObject[];   // Per-layer overlays
  offset?: number;
  maxLength?: number;
}

interface MyVideoMixAudioLayer {
  fileName: string;
  volume: number;                        // 0-100, voiceover typically 100, music 20
  offset?: number;
  maxLength?: number;
}
```

> **Note on overlays:** Both per-layer overlays (applied before cross-fade) and cross-layer overlays (applied after merge) are stored in the same `overlay` array. They are distinguished by `offset` and `layersLength` properties - overlays with `layersLength > 1` span multiple merged layers.

Example: 3 hooks × 2 bodies × 2 CTAs = 12 parts

### Video - Final Rendered Asset
```typescript
interface IVideo {
  // Required fields
  _firestore_id: string;
  companyId: string;
  configId: string;
  language: string;
  preview: IVideoPreview;
  raw_video: {
    portrait?: IFile;
    square?: IFile;
    landscape?: IFile;
    tiktok?: IFile;
  };

  // Content metadata
  description: string;
  headlines: string[];
  primary_text: string;
  tags: string[];
  feature: string;
  extracted_texts: string[];
  extracted_timestamp?: Date;
  audio_script: string;
  duration?: number;

  // Platform integrations
  facebook: IFacebookVideo;
  tiktok?: ITiktokVideo;
  snapchat?: ISnapchatVideo;

  // Tracking
  experiments: string[];
  experiments_uploaded?: IExperimentUploaded[];
  total_spend: number;
  spend?: number;
  results?: number;
  cpa?: number;

  // Mix/Part references
  mix?: boolean;
  mixConcept?: string;
  part_id?: string;
  templateFormat?: string;

  // Other optional fields
  addedOn?: IAddedOn;
  affiliate?: boolean;
  comments?: string[];
  instructions?: string[];
  resolution?: string;
}
```

### Experiment - A/B Test Campaign
```typescript
interface DTOExperiment {
  // Required fields
  provider: string;          // facebook, tiktok, snapchat
  campaign_name: string;
  adgroup_name: string;
  budget: number;
  videos: string[];          // Video IDs to test
  status: string;
  objective_type: string;
  companyId: string;
  addedOn: FieldValue;
  uploaded_by: string;
  target: {
    countries: string[];
    platform: string;        // IOS, ANDROID
    age?: string[];
    age_range?: { min: number; max: number };
  };
  campaign: {
    name: string;
    placement?: string;
    ppid?: string;
  };

  // Optional fields - platform IDs
  _firestore_id?: string;
  id?: string;
  campaign_id?: string;
  adgroup_id?: string;
  account_id?: string;
  business_id?: string;
  page_id?: string;
  configId?: string;
  userId?: string;

  // Optional fields - tracking
  landing_page_url?: string;
  conversion_event?: string;
  objective_campaign_type?: string;
  top_audience?: string;
  lastMessage?: string;
  author?: string;
}
```

---

## Pipeline Flow

```
1. TEMPLATE TRIGGER
   - Scheduled (cron) OR manual
   - MyVideoMixAutoTemplate.build() called

2. MIX CREATION
   - Queries Firestore for components matching conditions
   - Generates voice if needed (TTS from script)
   - Creates videoMix document with status: "new"
   - Location: ads-library-automation/functions/src/videomixes/MyVideoMixAutoTemplate.ts

3. PART GENERATION (Firebase trigger: onCreateMixes)
   - MyVideoMixBuilder.build() creates all part combinations
   - MyVideoMixPreviews.build() generates preview thumbnails
   - Each part = subcollection document
   - Location: ads-library-automation/functions/src/triggers/mixes.ts

4. VIDEO RENDERING (Firebase trigger: onCreateMixPart)
   - Sends task to worker queue (Pub/Sub)
   - Worker downloads components, renders video
   - Uploads to cloud storage
   - Creates video document
   - Location: ads-library-automation/functions/src/triggers/mixes.ts

5. CONTENT TAGGING (generateAdContent)
   - GPT-4o-mini analyzes video transcript
   - Generates: description, tags, headlines, primary_text
   - Tags with app feature (anxiety, relationships, etc.)
   - Location: ads-library-automation/functions/src/content/content.ts

6. EXPERIMENT CREATION
   - Groups videos by language, script, body
   - Creates experiment documents
   - Sets targeting: countries, platform, age, budget

7. AD PLATFORM UPLOAD
   - Uploads videos to Facebook/TikTok via APIs
   - Creates actual ad campaigns/adgroups

8. PERFORMANCE TRACKING
   - BigQuery pulls performance data
   - Tracks spend, installs, conversions
```

---

## External Services & Infrastructure

### AI Services
| Service | Purpose | Used In |
|---------|---------|---------|
| **OpenAI GPT-4o-mini** | Content tagging (description, tags, headlines) | `content/content.ts` |
| **Google Vision** | Video frame analysis, text extraction | Video processing |
| **FAL.ai** | AI video generation | `ai-videos` feature |
| **Google TTS** | Voice generation from scripts | `scripts` trigger |

### Search Infrastructure
| Service | Purpose | Notes |
|---------|---------|-------|
| **MeiliSearch** | Full-text search for UI | Synced via Firebase Extension (prod) or manual backfill (local) |
| **Firestore** | Primary database | All collections |

### Worker Architecture
| Component | Details |
|-----------|---------|
| **Queue** | Google Pub/Sub |
| **Topics** | `video-mix-processing-v3`, plus 6 others |
| **Worker** | `functions/src/worker/worker.ts` |
| **Timeout** | 540 seconds per task |
| **Task Types** | `process_video_mix`, `process_convert_video_part`, `process_convert_image_part`, `process_invoice`, `process_shared_video_analysis`, `process_video_by_status` |

### Ad Platforms
| Platform | Integration | Features |
|----------|-------------|----------|
| **Meta (Facebook/Instagram)** | Marketing API | Upload, create campaigns, track performance |
| **TikTok** | Marketing API | Upload, spark ads, create campaigns |
| **Snapchat** | Marketing API | Upload, create campaigns |
| **Pinterest** | Marketing API | Pin creation, campaigns |

### Analytics
| Service | Purpose |
|---------|---------|
| **BigQuery** | Performance data aggregation, reporting |
| **Firestore** | Real-time metrics |

---

## Key Technical Patterns

### Event-Driven Architecture
Everything runs on Firestore triggers:
```typescript
// ads-library-automation/functions/src/triggers/mixes.ts
export const onCreateMixes = onDocumentCreated("videoMixes/{mix_id}", async (event) => {
  // Triggers when new videoMix created
});

export const onCreateMixPart = onDocumentCreated("videoMixes/{mix_id}/parts/{part_id}", async (event) => {
  // Triggers when new part created
});

export const onUpdateMixes = onDocumentUpdated("videoMixes/{mix_id}", async (event) => {
  // Handles status changes
});

export const onUpdateMixPart = onDocumentUpdated("videoMixes/{mix_id}/parts/{part_id}", async (event) => {
  // Checks if all parts complete, sets mix to "ready"
});
```

> **Note:** All triggers are exported from the same file (`mixes.ts`), not separate files.

**Key insight:** Write a document = trigger a pipeline step.

### Status Machine
Documents use `status` field to control flow:
- `new` → ready to process
- `running` → currently processing
- `ready` → done, waiting for next step
- `uploaded` → sent to ad platform
- `paused` → temporarily stopped
- `retry` → reprocess from scratch
- `error` → processing failed (set when MyVideoMixGenerator fails)

```
Flow: new → running → ready → uploaded
              ↓
            error (on failure)
```

### Worker Queue Pattern
Heavy work (video rendering) goes to Pub/Sub worker:
```typescript
await createTaskForWorker({
  type: WorkerTaskType.ProcessVideoMix,
  data: { path: doc.ref.path },
});
```

### Overlay System
Overlays can get their data from:
- **Given overlay** - Pre-defined text/graphics
- **Generated overlay** - LLM generates text
- **Self datasource** - Content provides its own overlay data (e.g., narration)
- **Overall datasource** - External CSV/data feed

```typescript
interface MyVideoMixOverlay {
  // Required fields
  overlayId: string;
  layers: string[];

  // Optional fields
  id?: string;
  compositionId?: string;
  inputVideo?: boolean;
  generationType?: "manual" | "auto";
  params?: MyVideoMixOverlayParam[];  // e.g., { key: "text", value: "..." }
  overlay?: MyOverlay;
  isCanvas?: boolean;
  language?: string;
  preview?: MyVideoMixOverlayPreview;
  type?: "customizable" | "static";
  prompt?: string;
  description?: string;
}

interface MyVideoMixOverlayObject {
  // Required fields
  overlayId: string;
  sound: number;

  // Optional fields
  fileName?: string;
  compositionId?: string;
  generationType?: "manual" | "auto";
  params?: MyVideoMixOverlayParam[];
  offset?: number;
  layersLength?: number;
  isCanvas?: boolean;
  cloudFile?: { fileName: string; sound: number; overlayId: string };
  inputVideo?: boolean;
  text?: string;
}
```

### Template Field System
Templates define fields with conditions:
```typescript
interface MyVideoMixSourceTemplateField {
  name: string;
  type: "video" | "audio" | "text" | "image" | "overlay";
  collection: string;           // Firestore collection to pull from
  conditions?: MyVideoMixSourceTemplateFieldCondition[];
  numberOfFields?: number;      // How many to pull
  dataSource?: string;          // For overlays
  layers?: string[];
  editable?: boolean;
}

interface MyVideoMixSourceTemplateFieldCondition {
  search_field: string;
  condition: WhereFilterOp;     // "==", "in", "array-contains", etc.
  equal_with: string | number | boolean;
}
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| **Core Models** | |
| `ads-library-automation/functions/src/videomixes/models.ts` | All mix-related TypeScript interfaces |
| `Ads_Platform_Web/models/videos.ts` | Video/Hook/Body/CTA interfaces |
| `Ads_Platform_Web/models/templates.ts` | Template interfaces |
| `Ads_Platform_Web/models/experiments.ts` | Experiment interfaces |
| **Pipeline & Triggers** | |
| `ads-library-automation/functions/src/triggers/mixes.ts` | Firestore triggers (onCreateMixes, onCreateMixPart, onUpdateMixes, onUpdateMixPart) |
| `ads-library-automation/functions/src/videomixes/MyVideoMixAutoTemplate.ts` | Auto template execution logic |
| `ads-library-automation/functions/src/videomixes/MyVideoMixBuilder.ts` | Part combination generation |
| `ads-library-automation/functions/src/content/content.ts` | GPT content tagging |
| **Video Processing** | |
| `ads-library-automation/functions/src/videomixes/MyVideoMixGenerator.ts` | Video generation orchestrator |
| `ads-library-automation/functions/src/videomixes/MyVideoCloudReEncoder.ts` | Video trimming/offsetting |
| `ads-library-automation/functions/src/videomixes/MyVideoCrossFadeVideos.ts` | Layer cross-fading |
| `ads-library-automation/functions/src/videomixes/MyVideoCloudAudioMix.ts` | Audio mixing |
| `ads-library-automation/functions/src/videomixes/MyVideoCloudCaptions.ts` | Caption/subtitle rendering |
| **Overlay Processing** | |
| `ads-library-automation/functions/src/videomixes/overlays/MyVideoOverlayFactory.ts` | Overlay routing/application |

