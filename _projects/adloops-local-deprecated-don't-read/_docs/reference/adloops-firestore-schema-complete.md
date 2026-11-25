# AdLoops Firestore Schema - Complete Reference

> **Generated:** 2026-01-14
> **Purpose:** Comprehensive schema extracted from code analysis for seed-data script development
> **Source:** TypeScript types + Trigger analysis + Service analysis + Frontend hardcoded values + Current Firestore dump

---

## Quick Reference - Collections

| Collection | Purpose | Required for Demo | Current State |
|------------|---------|-------------------|---------------|
| `config` | App configuration | Yes | 1 doc |
| `web_config` | Frontend config | Yes | 1 doc |
| `mixTemplates` | Mix templates | Yes | 1 doc |
| `bodies` | Body video components | Yes | 1 doc |
| `hooks` | Hook video components | Yes | **0 docs** |
| `ctas` | CTA video components | Yes | 1 doc |
| `overlays` | Video overlays | No | **0 docs** |
| `scripts` | Voice scripts | No | 1 doc |
| `users` | User accounts | Yes | 1 doc |
| `videoMixes` | Mix jobs | Yes | 3 docs |
| `videos` | Final videos | Yes | 3 docs |
| `experiments` | Ad campaigns | No | 0 docs |
| `backgroundMusic` | Music tracks | No | 0 docs |
| `jobs-queue` | Job templates | No | 1 doc |

---

## Enum Values Reference

### MyVideoStatus
```
new | video_uploaded | video_posted | content_generated | tagged |
download_done | pending_download | reupload_facebook | reupload_snapchat |
reupload_tiktok | sharing_in_progress | posting_in_progress | content_posted |
content_posting_error | video_reupload_needed | marius | marius55 | marius56
```

### MyVideoMixStatus
```
new | running | ready | uploaded | paused | retry | error
```

### ImageResolution / VideoResolution
```
portrait | landscape | square
```
**IMPORTANT:** Must be lowercase. `"PORTRAIT"` will fail.

### PLATFORM
```
IOS | ANDROID
```
**IMPORTANT:** Must be uppercase.

### USER_ROLES
```
superEditor | editor | virtualEditor | accounting | VA
```
**IMPORTANT:** Sidebar visibility requires `superEditor` or `editor`.

### AD_PROVIDER
```
facebook | tiktok | snapchat | pinterest | apple | google | applovin
```

### VIDEO_TYPE
```
video | image | carousel | unknown
```

### Language Values
```
english | spanish | romanian | german
```
**IMPORTANT:** Use full word `"english"`, not ISO code `"en"`.

---

## Collection Schemas

### config/{configId}

```typescript
{
  id: string;                    // Required: document ID
  companyId: string;             // Required: "local-company-001"
  name: string;                  // Required: Display name for dropdown

  // Social Media Config - Required for campaign features
  social_media_config: {
    facebook?: { accounts: [] },
    snapchat?: { accounts: [] },
    meta?: {
      businesses: [{
        id: string,
        name: string,
        accounts: [{ account_id: string, name: string }]
      }],
      pages: [{ page_id: string, name: string }]
    },
    tiktok?: {
      accounts: [],
      businesses: [{
        id: string,
        name: string,
        accounts: [{ advertiser_id: string, name: string }]
      }]
    },
    pinterest?: {
      accounts: [],
      businesses: [{
        id: string,
        name: string,
        accounts: [{ advertiser_id: string, name: string }]
      }]
    }
  },

  // Features Config - Required: UI iterates this array
  features_config: [{
    id: string,           // e.g., "general"
    names: string[]       // e.g., ["General"]
  }],

  apps: {
    web?: { name: string },
    mobile?: { name: string }
  },

  url_parameters?: {}
}
```

### web_config/{companyId}

```typescript
{
  id: string;                    // Required: matches companyId
  companyId: string;             // Required
  settings?: {
    theme: string,
    language: string
  },

  // Required: UI crashes without this
  languages: string[];           // e.g., ["english"]

  // Required: DataContext accesses messages["(default)"]
  messages: {
    "(default)": string          // Required key with parentheses
  }
}
```

### mixTemplates/{templateId}

```typescript
{
  id: string;                    // Required: e.g., "Own_Creation"
  name: string;                  // Display name
  companyId: string;
  configId: string;
  resolution: "portrait" | "landscape" | "square";  // Lowercase!
  status: "active" | "inactive";

  // Required: Groups array with specific structure
  groups: [{
    // CRITICAL: Must be "videoChoosing" for video selection UI
    name: "videoChoosing",
    fields: [{
      name: "hook" | "body" | "cta",
      type: "video",
      collection: "hooks" | "bodies" | "ctas",
      label: string,
      initialValue: [],
      editable: boolean,
      priority: number,
      sequence: number
    }]
  }]
}
```

### bodies/{docId} | hooks/{docId} | ctas/{docId}

```typescript
{
  id: string;                    // Required: document ID
  video: string;                 // Video name/identifier

  // Raw video object - Required for video processing
  raw_video: {
    portrait: {
      fileName: string,          // Storage path
      fileURL: string            // Full URL
    },
    landscape?: { ... },
    square?: { ... }
  },

  // Preview object - Required for thumbnails
  preview: {
    fileName: string,
    fileURL: string,
    fullSize?: {
      format: "portrait" | "landscape" | "square",
      fileName: string,
      fileURL: string
    }
  },

  duration: number;              // Video duration in seconds
  description: string;           // AI-generated description
  tags: string[];                // Array of tags

  companyId: string;             // Required
  configId: string;              // Required
  userId: string;                // Required
  uploaded_by: string;           // User name string

  status: "approved" | "pending" | "rejected";
  language: "english";           // Full word, not "en"
  affiliate: boolean;            // Required for filtering
  used_count: number;            // Usage counter

  // Required for queries with orderBy
  addedOn: Timestamp;            // Firestore server timestamp
}
```

### videos/{docId}

```typescript
{
  id?: string;                   // Optional, set from doc ID
  video: string;                 // Video name

  raw_video: {
    portrait: { fileName: string, fileURL: string }
  },
  raw_image?: {},                // For image ads
  raw_carousel?: {},             // For carousel ads

  preview: {
    fileName: string,
    fileURL: string,
    fullSize?: { format: string, fileName: string, fileURL: string },
    format?: "portrait"
  },

  // Content fields
  description: string;
  primary_text: string;
  headlines: string[];           // Array of headline options
  tags: string[];
  audio_script?: string;         // Transcribed audio
  extracted_texts?: string[];

  // Metadata
  mix: boolean;                  // true if from mix, false if uploaded
  type?: "video" | "image" | "carousel";
  duration: number;
  language: "english";
  platform: "IOS" | "ANDROID";
  feature: string;               // Feature category, e.g., "general"
  default_plan_id?: string;

  // Detection flags (for sorting)
  feature_detected?: boolean;
  language_detected?: boolean;
  extracted_timestamp?: Timestamp;

  // Ownership
  companyId: string;
  configId: string;
  userId: string;
  uploaded_by: string;
  affiliate?: boolean;

  // Status
  status: MyVideoStatus;         // See enum above
  status_updated: Timestamp;
  addedOn: Timestamp;

  // Mix reference
  mixConcept?: string;
  part_id?: string;              // Reference to mix part
  isSin?: boolean;

  // Platform uploads (populated after publishing)
  facebook?: Record<string, any>;
  tiktok?: Record<string, any>;
  snapchat?: any;
  pinterest?: Record<string, any>;
  experiments?: string[];
  experiments_uploaded?: string[];
}
```

### videoMixes/{mixId}

```typescript
{
  id: string;
  name: string;
  identifier: string;            // Unique identifier, e.g., "603.22"

  templateFormat: string;        // Template ID, e.g., "Own_Creation"

  // Components to mix
  components: {
    hook?: string[];             // Array of hook doc IDs
    body?: string[];             // Array of body doc IDs
    cta?: string[];              // Array of cta doc IDs
  },

  overlay: any[];                // Overlay configurations
  voice?: any[];                 // Voice/audio configurations

  resolution: "portrait";        // Lowercase
  platform: "IOS" | "ANDROID";   // Uppercase
  language: "english";           // Full word

  // Ownership
  companyId: string;
  configId: string;
  userId: string;
  uploaded_by: string;
  affiliate?: boolean;

  // Status
  status: "new" | "running" | "ready" | "uploaded" | "paused" | "error";
  status_updated?: Timestamp;
  createdAt: Timestamp;

  // Generated after processing
  parts?: number;                // Count of parts
  previews?: {
    hook?: [{ fileURL: string, videoPreview: string }],
    body?: [{ fileURL: string, videoPreview: string }],
    cta?: [{ fileURL: string, videoPreview: string }]
  };

  // Subcollection: parts
}
```

### videoMixes/{mixId}/parts/{partId}

```typescript
{
  name: string;                  // e.g., "user.603.22.1"
  hash: string;                  // Content hash for deduplication

  videoLayers: [{
    videos: string[],            // Storage paths
    offset: number,
    keepSound: boolean,
    maxLength: number,
    name: "hook" | "body" | "cta"
  }],

  audioLayers: [{
    fileName: string,
    offset: number,
    volume: number
  }],

  resolution: "1080:1920";       // Actual pixel dimensions
  platform: "IOS" | "ANDROID";
  language: "english";

  // Captions
  captions: {
    template: "none" | string,
    position: "none" | "top" | "center" | "bottom"
  },
  captionsOffset: number;

  // Resources used
  resources: {
    hook?: string,               // Doc ID
    body?: string,
    cta?: string
  },

  // Processing
  crossFadeDuration: number;     // Default 0.4
  endAfterScript: boolean;
  overlay: any[];
  mixConcept: string;

  // Ownership (inherited from parent)
  companyId: string;
  configId: string;
  userId: string;
  uploaded_by: string;
  templateFormat: string;

  // Status
  status: "new" | "running" | "uploaded" | "error";
  status_updated: Timestamp;
  error?: string;                // Error message if failed

  // Output (after processing)
  preview?: {
    fileName: string,
    fileURL: string,
    fullSize?: { fileName: string, fileURL: string, format: string }
  },
  raw_video?: {
    portrait: { fileName: string, fileURL: string }
  },
  video_id?: string;             // Created video doc ID
}
```

### users/{userId}

```typescript
{
  id: string;                    // Same as userId
  userId: string;                // Same as id
  email: string;
  name: string;

  // Required for sidebar visibility
  role: "superEditor" | "editor" | "virtualEditor" | "accounting" | "VA";

  companyId: string;
  configId: string;

  affiliate: boolean;            // Affiliate user flag

  // Counters
  hooks: number;                 // Default 0
  videos: number;                // Default 0
  points?: number;               // For affiliate rewards

  // Timestamps
  createdAt: Timestamp;

  // Profile
  country?: string;
  language?: string;
  preview?: { fileURL: string }; // Profile picture

  // Status
  status?: "pending" | "active" | "inactive";

  // Subcollections (for publishing features)
  // users/{userId}/tiktokAccounts
  // users/{userId}/facebookPages
  // users/{userId}/facebookAdAccounts
}
```

### scripts/{scriptId}

```typescript
{
  id: string;
  name: string;
  script: string;                // The actual script text
  language: "english";           // Full word
  companyId: string;
  status: "ready" | "uploaded";

  // Voice array - Each entry is a generated voice file
  voices: [{
    voiceName: string,           // e.g., "en-US-Standard-A"
    voiceURL: string,            // Storage URL
    voiceFileName: string,       // Storage path
    srtFileName: string,         // Subtitle file path
    srtFileURL: string,          // Subtitle URL
    offset: number,              // Default 0
    volume: number,              // Default 1
    content: {
      language: string,
      text: string,
      transcription: string
    }
  }],

  addedOn: Timestamp;
}
```

### overlays/{overlayId}

```typescript
{
  id: string;
  name: string;
  fileName: string;              // Storage path
  fileURL: string;               // Full URL

  preview?: {
    fileURL: string
  },

  // For video overlays
  raw_video?: {
    portrait: { fileName: string, fileURL: string }
  },

  compositionId?: string;        // Remotion composition ID
  sound?: number;                // 0 = no sound
  inputVideo?: boolean;          // Has video input

  companyId: string;
  userId: string;
  language?: string;

  addedOn?: Timestamp;
}
```

---

## Hardcoded Values Checklist

Before running the app, verify these values exist:

### Critical (App will crash without these)

- [ ] `web_config` doc has `messages["(default)"]` key
- [ ] `web_config` doc has `languages` array
- [ ] `config` doc has `features_config` as array (not object)
- [ ] `config` doc has `name` field (for dropdown)
- [ ] User doc has `role: "superEditor"` (for sidebar)
- [ ] `mixTemplates` has `groups[].name = "videoChoosing"`

### Important (Features will be broken)

- [ ] Bodies/hooks/ctas have `addedOn` timestamp
- [ ] Bodies/hooks/ctas have `language: "english"` (not "en")
- [ ] Bodies/hooks/ctas have `affiliate: false` boolean
- [ ] VideoMixes have `resolution: "portrait"` (lowercase)
- [ ] VideoMixes have `platform: "IOS"` (uppercase)

### Optional (For complete features)

- [ ] Videos have `feature_detected` and `language_detected` flags
- [ ] Config has full `social_media_config` structure
- [ ] User has `tiktokAccounts` subcollection (for TikTok publishing)

---

## Index Requirements

Composite indexes needed for queries:

```json
[
  { "collection": "bodies", "fields": ["companyId", "addedOn"] },
  { "collection": "hooks", "fields": ["companyId", "addedOn"] },
  { "collection": "hooks", "fields": ["affiliate", "companyId", "addedOn"] },
  { "collection": "ctas", "fields": ["companyId", "addedOn"] },
  { "collection": "overlays", "fields": ["companyId", "addedOn"] },
  { "collection": "scripts", "fields": ["companyId", "addedOn"] },
  { "collection": "videos", "fields": ["companyId", "addedOn"] },
  { "collection": "videos", "fields": ["companyId", "mix", "addedOn"] },
  { "collection": "videoMixes", "fields": ["companyId", "status"] }
]
```

---

## Current Gaps (What's Missing)

| Gap | Impact | Resolution |
|-----|--------|------------|
| No hooks documents | CreateMix hook selector empty | Upload 1 hook video |
| No overlays documents | Overlay selector empty | Optional - can proceed without |
| No backgroundMusic documents | Music selector empty | Optional |
| No experiments documents | Campaign history empty | Optional |

---

## Appendix: Other Collections (Not Required for Demo)

These collections exist in the codebase but are **not needed** for the core VideoMix pipeline demo:

| Collection | Purpose | Used By |
|------------|---------|---------|
| `autoMixTemplates` | Scheduled auto-generation templates | MyVideoMixAutoTemplate.ts |
| `image-mixes` | Image carousel mix jobs | imageMixes.ts triggers |
| `image-parts` | Image processing queue | MyImagePartProcessor.ts |
| `saved-images` | Cached component images | MyAutoMixComponentSelector.ts |
| `ai-videos` | AI-generated video jobs | aiVideos.ts trigger |
| `briefs` | Content brief assignments | briefs.ts trigger |
| `influencers` | Influencer CRM records | Influencers/ services |
| `contracts` | Influencer contracts | InvoicePDFGenerator.ts |
| `deals` | Deal tracking | Influencers/ services |
| `invoices` | Billing/payment records | InvoicePDFGenerator.ts |
| `scheduler` | Cron job scheduling | MyVideoMixTemplateScheduler.ts |
| `autoScripts` | Auto-generated voice scripts | MyVideoMixAutoTemplate.ts |
| `jobs` | Generic async job queue | jobs.ts trigger |
| `templates` | Influencer video templates | MyVideoMixTemplateBuilder.ts |

### When These Are Needed

- **Image carousel ads:** `image-mixes`, `image-parts`, `saved-images`
- **Influencer management:** `influencers`, `contracts`, `deals`, `invoices`
- **Automated content generation:** `autoMixTemplates`, `autoScripts`, `scheduler`
- **AI video features:** `ai-videos`

For CLoops integration demo, only the core VideoMix pipeline collections are required.

---

## See Also

- `adloops-replication-handoff.md` - Session progress log
- `adloops-functions-reference.md` - All 60 Cloud Functions
- `firestore.indexes.json` - Deployed composite indexes
