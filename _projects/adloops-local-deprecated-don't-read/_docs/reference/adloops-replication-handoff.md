# AdLoops Local Replication - Progress Log

> **Purpose:** Changelog of the local AdLoops replication project. Read latest entry for current status.
> **Goal:** Demonstrate CLoops integration capability to CTO (Jan 12, 2026 meeting)

---

## Quick Reference

### Login Credentials
```
Email:    local@adloops.test
Password: localtest123
Role:     superEditor
```

### Firebase Config
```
Project ID: adloops-local
Firestore Region: eur3 (Europe multi-region)
Functions Region: europe-west1
Storage Bucket: adloops-local.firebasestorage.app
```

### Key Paths
| What | Path |
|------|------|
| Functions code | `_projects/adloops-local/ads-library-automation/functions/` |
| UI code | `_projects/adloops-local/Ads_Platform_Web/` |
| Service account | `~/adloops-credentials/adloops-local-firebase-adminsdk-fbsvc-44775403ca.json` |

### Quick Commands
```bash
# Start MeiliSearch (Terminal 1) - REQUIRED for search to work
# Run from project root, data stored in adloops-local/data.ms
meilisearch --master-key="VI6MVLjlLU63mamIQxr2MB5jQ_G_i9dTvx_hhKrHNd0" --db-path="_projects/adloops-local/data.ms"

# Start UI (Terminal 2)
cd "_projects/adloops-local/Ads_Platform_Web" && bun run dev

# Start Worker (Terminal 3) - for processing video mixes
cd "_projects/adloops-local/ads-library-automation/functions" && npx ts-node src/worker/worker.ts

# ⚠️ IMPORTANT: MeiliSearch does NOT auto-sync with Firestore locally!
# In production, a Firebase Extension handles sync. Locally, you must run backfill manually.
# If search results are missing/stale after adding Firestore data, run this:
cd "_projects/adloops-local/ads-library-automation/functions" && node meili-backfill.js

# Deploy functions
cd "_projects/adloops-local/ads-library-automation" && firebase deploy --only functions --project adloops-local

# Deploy Firestore indexes
firebase deploy --only firestore:indexes --project adloops-local

# View logs (Note: 30-45 min delay - use GCP Console for real-time)
firebase functions:log --project adloops-local

# Create test mix (backend)
cd "_projects/adloops-local/ads-library-automation/functions" && node seed-data.js mix
```

---

## Replication Philosophy

> **Critical principle for all sessions working on this replication.**

### The Code is the Source of Truth

```
Production:  Code ←→ Firebase (data/infra)  ✅ Works perfectly
Local:       Code ←→ ??? (we must reverse-engineer what's missing)
```

**Core Rules:**

1. **The code is correct** - It runs in production. Never assume bugs.
2. **If something breaks locally, our infra/data is wrong** - Not the code.
3. **Reverse-engineer expectations from code** - Read queries, field accesses, conditionals.
4. **Build local infra to match code expectations** - Don't patch code to handle missing data.

**When Debugging:**
- ❌ Don't modify code to handle undefined/missing data
- ✅ Do add the missing data/config that the code expects
- ✅ Do trace what data structure the code assumes exists

**The Challenge:**
- **Explicit expectations:** Firestore collection names, query filters, field names
- **Implicit expectations:** Nested object shapes, enum values, required array structures
- **Discovery method:** We only find implicit expectations when something crashes

**Example Pattern:**
```
Crash: "Cannot read property 'map' of undefined"
Wrong fix: Add optional chaining (?.) to the code
Right fix: Find what array the code expects and seed it in Firestore
```

This principle applies to ALL layers: Firestore data, Storage files, config structures, MeiliSearch indexes.

---

## Progress Log

> Read from top to bottom to follow the journey chronologically.

### 2026-01-09 - Session 1: Initial Setup

**What happened:**
- Created Firebase project `adloops-local`
- Set up Firestore (eur3) and Storage
- Cloned all repos to `_projects/adloops-local/`
- Updated hardcoded values (project IDs, bucket names)
- Created seed data (config, bodies, mixTemplates)
- First function deployments
- Frontend running but hitting various errors

**Problems encountered:**
- Import bug: `onCreateMixes` trigger wasn't firing. Wrong import path (`firebase-functions/firestore` instead of `firebase-functions/v2/firestore`)
- Frontend crashed with "supabaseUrl is required" - needed placeholder env vars
- `onCreateMixes` failed with "Template Own_Creation not found" - template document was missing

**Key learnings:**
1. Firebase data model is implicit - discovered by reading code or hitting errors
2. Template `groups` array required for VideoMix processing
3. tiktok-scraper dependency removed (caused build failures)

---

### 2026-01-10 - Session 2: Region Mismatch Discovery & Fix

**What happened:**
- Functions deployed successfully but triggers STILL weren't firing
- Spent time debugging - logs showed functions deployed but no execution on document create
- Discovered the root cause: **Region mismatch**
  - Firestore location: `eur3` (Europe)
  - Functions deployed to: `us-central1` (US default)
  - Eventarc can't route events across regions!
- Fixed by adding `region: "europe-west1"` to mixes.ts triggers (europe-west1 pairs with eur3)
- Confirmed triggers now fire when VideoMix created

**Key learning:**
- Firestore region `eur3` requires functions in `europe-west1` (not us-central1)
- This wasn't documented anywhere - discovered by debugging

---

### 2026-01-10 - Session 3: Full Local Environment Working

**What happened:**
- Previous session left functions in mixed state (some us-central1, some europe-west1)
- Decided to start fresh: deleted ALL functions
- Discovered `setGlobalOptions()` - better than adding region to each function individually
- Added `setGlobalOptions({ region: "europe-west1" })` to `index.ts`
- Removed individual `region` settings from trigger files (now inherited from global)
- Deployed all 60 functions fresh to europe-west1
- Set up UI locally:
  - Created Firebase Auth user
  - Created Firestore user document
  - Discovered sidebar is role-based (needed `role: "superEditor"`, not `admin`)
- Hit Firestore index errors - complex queries need composite indexes
- Reverse-engineered required indexes from error messages
- Created and deployed 11 Firestore composite indexes
- Sidebar menus now visible, UI functional

**What's working:**
- Firebase project (adloops-local) ✅
- Firestore (eur3) ✅
- 60 Cloud Functions (europe-west1) ✅
- UI at localhost:3000 ✅
- Auth + login ✅
- Firestore indexes ✅

**What's NOT working / needs investigation:**
- VideoMix pipeline: triggers fire but status stays "new" (logs delayed 30-45 min, couldn't confirm)
- Supabase tasks feature (expected - Supabase not running locally)
- Some React key warnings (cosmetic)

**Key learnings:**
1. **Global region config:** Use `setGlobalOptions({ region: "europe-west1" })` in index.ts instead of adding region to each function
2. **Sidebar is role-based:** User needs `role: "superEditor"` in Firestore to see menus (not "admin")
3. **Firestore indexes:** Complex queries fail until indexes created. Can deploy via `firestore.indexes.json`
4. **Firebase logs delayed:** CLI logs have 30-45 min delay. Use Cloud Console for real-time logs.

**Files modified:**
- `functions/src/index.ts` - Added setGlobalOptions
- `functions/src/triggers/mixes.ts` - Removed redundant region settings
- `functions/src/triggers/imageParts.ts` - Changed from us-central1 to inherit global
- `firebase.json` - Added firestore indexes config
- `firestore.indexes.json` - Added 11 composite indexes

---

### 2026-01-11 - Session 4: VideoMix Pipeline Debugging

**What happened:**
- Verified function count: 60 functions (not 59)
- Created comprehensive documentation:
  - `adloops-functions-reference.md` - All 60 functions with types, paths, summaries
  - `adloops-firestore-schema.md` - Complete Firestore data model (28 collections)
- Rebuilt `seed-data.js` with comprehensive seed data for all collections
- Debugged VideoMix pipeline through multiple errors:
  1. "Video layers are missing" → Fixed: `resolution` must be lowercase `"portrait"` not `"PORTRAIT"`
  2. "Cannot use undefined (field: platform)" → Fixed: Added `platform: "IOS"` to VideoMix
  3. "Resource not found (video-mix-processing-v3)" → Fixed: Created Pub/Sub topic in GCP Console
- **Pipeline now works!** Status transitions: `new` → `running`, parts created, messages queued

**Current status:**
- VideoMix pipeline runs successfully up to message queuing
- Pub/Sub topic `video-mix-processing-v3` receives messages
- **BLOCKER:** No worker/service processes the queue (actual video rendering)

**Key learnings:**
1. **Enum values are case-sensitive:** `ImageResolution.PORTRAIT = "portrait"` (lowercase)
2. **Field values matter, not just names:** Schema extraction should include enum values
3. **Pub/Sub topics are infrastructure:** Must be created in GCP Console, not in code
4. **Worker is external:** Video processing happens outside Firebase Functions

**Files created/modified:**
- `adloops-functions-reference.md` - New reference doc
- `adloops-firestore-schema.md` - New schema doc
- `seed-data.js` - Comprehensive rebuild with all collections

**Next steps:**
1. Find what processes `video-mix-processing-v3` messages (worker/service)
2. Either deploy the worker or mock the processing step
3. Test full pipeline to "ready" status

---

## Seed Data Created

| Collection | Document ID | Purpose |
|------------|-------------|---------|
| `config` | `local-config` | App configuration with social_media_config |
| `web_config` | `local-company-001` | Frontend config |
| `mixTemplates` | `Own_Creation` | Template with hook/body/cta groups |
| `bodies` | `test-body-001` | Body video component (points to real file) |
| `hooks` | `test-hook-001` | Hook video component |
| `ctas` | `test-cta-001` | CTA video component |
| `overlays` | `test-overlay-001` | Overlay graphic |
| `scripts` | `test-script-001` | Voice script with audio |
| `users` | `local-user-001` | Test user |
| `jobs-queue` | `default-job` | Job template |

**Seed commands:**
```bash
node seed-data.js all      # Seed everything
node seed-data.js simple   # Create body-only mix
node seed-data.js mix      # Create full mix (hook+body+cta)
node seed-data.js list     # Check what's in Firestore
node seed-data.js clean    # Delete test mixes
```

**Test VideoMixes:** Created with IDs like `simple-mix-TIMESTAMP`

---

## File Locations

| What | Path |
|------|------|
| Local replica repos | `_projects/adloops-local/` |
| Reference repos (read-only) | `_projects/_adloops/` |
| CLoops project | `_projects/cloops/` |
| Frontend .env | `_projects/adloops-local/Ads_Platform_Web/.env.local` |
| Functions .env | `_projects/adloops-local/ads-library-automation/functions/.env` |
| Seed script | `_projects/adloops-local/ads-library-automation/functions/seed-data.js` |
| Firebase config | `_projects/adloops-local/ads-library-automation/firebase.json` |
| Firestore indexes | `_projects/adloops-local/ads-library-automation/firestore.indexes.json` |

---

## Firestore Data Model

Key collections and their purpose:

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `videos` | Final video ads | status, preview, raw_video, companyId |
| `videoMixes` | Mix jobs | status, components, overlay, templateFormat |
| `videoMixes/{id}/parts` | Individual mix outputs | videoLayers, status |
| `hooks/bodies/ctas` | Video components | video, preview, raw_video, status |
| `overlays` | Graphics overlays | fileName, fileURL, compositionId |
| `scripts` | Audio scripts | script, voices[], language |
| `config` | App settings | companyId, apps, features_config |
| `users` | User accounts | email, name, companyId, role |
| `experiments` | Ad campaigns | videos[], budget, target, provider |
| `mixTemplates` | Manual templates | id, name, groups[] |

**Status flow:**
```
VideoMix: new → running → ready → uploaded
                ↓
              error
```

---

## Known Issues / Gotchas

1. **Firebase reserved env vars**: Don't use `GCLOUD_PROJECT` or `FIREBASE_*` in .env - Firebase auto-injects these

2. **tiktok-scraper removed**: Was causing npm install to fail due to canvas native module. Removed from `functions/package.json`

3. **First deploy timing**: Google Cloud needs a few minutes to set up Eventarc for 2nd gen functions on first deploy

4. **Bun installed**: Frontend uses bun, installed at `~/.bun/bin/bun`

5. **Logs delayed**: Firebase CLI logs can take 30-45 minutes to appear. Use Cloud Console for real-time logs.

6. **Region pairing**: Firestore `eur3` must pair with functions in `europe-west1` (not us-central1)

7. **Sidebar role-based**: User needs `role: "superEditor"` in Firestore `users` collection to see menu items

8. **Firestore indexes**: Complex queries require composite indexes. Deploy via `firebase deploy --only firestore:indexes`

9. **MeiliSearch no auto-sync locally**: In production, a Firebase Extension syncs Firestore → MeiliSearch automatically. Locally, this extension isn't running. If search results are missing or stale after adding/changing Firestore data, run `node meili-backfill.js` manually.

---

## Lessons Learned (All Sessions)

### 1. Import Bug in mixes.ts (Session 1)
**Problem:** `onCreateMixes` trigger wasn't firing after deploy.
**Cause:** Wrong import path:
```typescript
// WRONG (v1 style)
import { onDocumentCreated } from "firebase-functions/firestore";

// CORRECT (v2 style)
import { onDocumentCreated } from "firebase-functions/v2/firestore";
```

### 2. Supabase Mobile Env Vars (Session 1)
**Problem:** Frontend crashed with "supabaseUrl is required"
**Fix:** Added placeholder env vars to `.env.local`

### 3. Template Required for VideoMix (Session 1)
**Problem:** `onCreateMixes` failed with "Template Own_Creation not found"
**Fix:** Created `mixTemplates/Own_Creation` document with `groups` array

### 4. Region Mismatch (Session 2)
**Problem:** Triggers not firing despite successful deploy
**Cause:** Firestore in `eur3`, functions in `us-central1`
**Fix:** Use `setGlobalOptions({ region: "europe-west1" })` in index.ts

### 5. Global Region Config (Session 3)
**Better approach:** Instead of adding `region` to each function, use:
```typescript
import { setGlobalOptions } from "firebase-functions/v2";
setGlobalOptions({ region: "europe-west1" });
```

### 6. Firebase Data Model is Implicit
**Key insight:** Firestore has no schema. The CODE defines expected document structure. Discover requirements by reading code or hitting runtime errors.

---

## Reference Docs

| Doc | Purpose |
|-----|---------|
| `adloops-system-analysis.md` | How AdLoops architecture works |
| `adloops-diagrams.md` | Visual architecture diagrams |

---

## What's Intentionally Skipped

| Feature | Why |
|---------|-----|
| Supabase | Only needed for influencer/payments features |
| TikTok/Instagram integration | Social APIs not needed for pipeline demo |
| Stripe/PayPal | Payments not needed |
| MeiliSearch | Search is optional |

---

### 2026-01-12 - Session 5: Worker Setup & UI Config Fixes

**What happened:**
- Discovered worker is a standalone service in `functions/src/worker/worker.ts` (not a Cloud Function)
- Created Pub/Sub subscription `video-mix-processing-subscription` attached to topic
- Fixed IAM: Added `Pub/Sub Subscriber` role to service account
- Copied Firebase credentials to expected path for worker
- **Worker now runs locally and receives messages!**
- Worker processed a message but failed on missing video file in Storage (expected - seed data had fake paths)

**UI Config Fixes (incremental discovery):**
- Added `features_config` array to `config/local-config` (was empty object `{}`)
- Added `languages` array to `web_config/local-company-001`
- Added `messages["(default)"]` to `web_config` (UI crashed without it)
- Added `name` field to `config/local-config` (dropdown showed blank)
- Deleted duplicate `configs` collection (only `config` singular is used)

**Video Upload via UI:**
- Successfully uploaded 2 videos through UI (`test-body`, `test-cta`)
- Videos went to `videos` collection with AI-generated descriptions/tags
- Thumbnails generated, status `video_uploaded`

**Blocking Issues Remaining:**
1. Uploaded videos go to `videos` collection, but createMix needs them in `bodies`/`ctas`
2. `/elements` page has infinite error loop (couldn't capture logs)
3. `/createMix` page shows template but no videos visible to select
4. Multiple Firestore index errors when navigating different pages

**Key Learnings:**
1. **Worker architecture:** `mixes.ts` publishes → Pub/Sub topic → subscription → `worker.ts` pulls → `processVideoMixTask`
2. **Two upload flows exist:** Home page uploads to `videos` (final ads). Elements page uploads to `bodies/hooks/ctas` (mix components)
3. **Firestore schema is incomplete:** Each UI page reveals new required fields. Need comprehensive code extraction.
4. **Config fields discovered this session:**
   - `config.name` - for dropdown display
   - `config.features_config[]` - array with `{id, names[]}`
   - `web_config.languages[]` - string array
   - `web_config.messages["(default)"]` - required by DataContext

**Files modified:**
- Copied service account to `ads-library-automation/adloops-local-firebase-adminsdk-gg78k-13954b62f1.json`
- Updated Firestore docs: `config/local-config`, `web_config/local-company-001`

**Commands added:**
```bash
# Run worker locally
cd "_projects/adloops-local/ads-library-automation/functions" && npx ts-node src/worker/worker.ts
```

---

## Identified Gaps / Recommended Next Steps

### 1. Firestore Schema Extraction (Priority)
The current schema doc is incomplete. Need dedicated thread to:
- Scan ALL UI components for Firestore queries
- Extract ALL required fields and their expected values/types
- Document enum values (e.g., `status: "approved"` vs `"content_generated"`)

### 2. Firestore Indexes
- Multiple index errors appearing as we navigate UI
- Could batch-deploy via `firestore.indexes.json`
- Need to collect all required indexes from error messages

### 3. Debug Tooling Setup

| Source | Use For | Capture Method |
|--------|---------|----------------|
| **Chrome DevTools MCP** | UI errors, network, screenshots | Claude can access directly ✅ |
| Next.js terminal | API route errors (server-side) | Check `bun run dev` output |
| Browser console | Client-side JS errors | DevTools MCP or manual |
| GCP Cloud Console | Cloud Function logs | Real-time (CLI has 30-45min delay) |
| Worker terminal | Pub/Sub message processing | Direct stdout |
| Firebase Console | Firestore data inspection | Manual |

**Key Lesson (Session 7):** Chrome DevTools MCP is powerful for:
- `take_snapshot` - See page structure without screenshot
- `list_console_messages` - Filter by error type
- `list_network_requests` - See API calls and responses
- `take_screenshot` - Visual confirmation

**Critical:** For API route errors, check **Next.js terminal first** - browser only shows empty 200 responses.

### 4. Elements Page Fix - RESOLVED
- ~~Infinite error loop blocks component video upload~~
- ~~Root cause unknown - needs debugging~~
- **FIXED in Session 6** - See below

---

### 2026-01-12 - Session 6: Elements Page MeiliSearch Fix

**Problem:** Elements page stuck in infinite error loop, couldn't load.

**Root Cause Identified:**
- Elements page has 7 components (HooksTable, BodiesTable, CtaTable, etc.)
- Each component calls `/api/search/*` endpoints
- These endpoints import from `meili_search_config.ts`
- MeiliSearch client crashes at module load when `NEXT_PUBLIC_MEILI_SEARCH_HOST` is undefined
- Error: `MeiliSearchError: The provided host is not valid`
- SWR (data fetching library) retries failed requests indefinitely
- 7 components × infinite retries = error loop (158+ errors)

**Solution:** Mocked all search routes to query Firestore directly instead of MeiliSearch.

**Files Modified (6 routes):**
```
app/api/search/hooks/route.ts
app/api/search/bodies/route.ts
app/api/search/ctas/route.ts
app/api/search/overlays/route.ts
app/api/search/backgroundMusic/route.ts
app/api/search/scripts/route.ts
```

**How to Restore Original MeiliSearch Routes:**
- Original code in reference repo: `_projects/_adloops/`
- Each mocked file has header comment indicating original import

**Note:** These mocked routes were further modified in Session 7:
- Added `affiliate` filter to hooks route
- Fixed `hasMore` calculation (was causing infinite scroll)
- Added `offset()` for proper pagination
- Added MeiliSearch compatibility fields (`estimatedTotalHits`, `limit`, `offset`)

**Result:**
- Elements page now loads without error loop
- All search endpoints return 200
- Tables render (empty until data seeded with correct companyId)
- Remaining errors are Supabase connection (expected - not running)

**Key Learnings:**
1. **MeiliSearch is required for Elements page** - not optional as previously thought
2. **Module-level crashes** - MeiliSearch client fails at import time, not request time
3. **Chrome DevTools MCP** - useful for targeted debugging (filter errors, check network requests)

---

### 2026-01-12 - Session 6 (continued): Data Not Showing in Tables

**Problem:** After mocking routes, tables showed loading spinners but no data.

**Debugging Journey (multiple issues found):**

1. **Missing `addedOn` field** - Seed data lacked `addedOn` timestamp, Firestore `orderBy` excludes docs without the field
   - Fix: Added `addedOn` to seed documents via script

2. **Wrong language value** - Seed data had `language: "en"`, UI filters by `language: "english"`
   - Fix: Updated seed data to use `"english"`

3. **Missing Firestore indexes** - Queries on `companyId + addedOn` require composite indexes
   - Fix: Added 6 indexes to `firestore.indexes.json` and deployed

4. **Firebase Admin not initializing** - The real blocker!
   - Error: `TypeError: privateKey.replace is not a function`
   - Root cause: `initAdmin()` tried to use env vars (`NEXT_FIREBASE_PRIVATE_KEY`) which weren't set
   - The `isDev` check existed but was AFTER `formatPrivateKey()` call
   - Fix 1: Added `NEXT_ENV_VAR=DEV` to `.env.local`
   - Fix 2: Moved `isDev` check BEFORE `formatPrivateKey()` in `firebase_admin.ts`

5. **Additional index needed for affiliate filter** - When `affiliate=true`, query needs `affiliate + companyId + addedOn` index
   - Fix: Disabled affiliate filter in hooks route for demo

**Critical Debugging Lesson:**
```
| Log Source          | Shows                              | Where                    |
|---------------------|------------------------------------|--------------------------|
| Browser Console     | Client-side JS (React components)  | DevTools → Console       |
| Next.js Terminal    | Server-side (API routes)           | Terminal running bun dev |
| GCP Cloud Console   | Firebase Cloud Functions           | Not relevant for UI      |
```

The actual error (`privateKey.replace`) was in **Next.js terminal** the whole time. Browser only showed empty responses (200 with `{hits: []}`). **Always check server logs first for API route issues.**

**Files Modified This Session:**
```
configs/firebase_admin.ts          - Fixed isDev check order
.env.local                         - Added NEXT_ENV_VAR=DEV
firestore.indexes.json             - Added 6 composite indexes
app/api/search/hooks/route.ts      - Simplified query, disabled affiliate filter
```

**Result:**
- Elements page loads with actual data
- Tables show seeded hooks, bodies, ctas, overlays, scripts
- Image 403 errors expected (seed data has placeholder URLs)

**What's Working Now:**
- ✅ Elements page loads
- ✅ Data displays in tables
- ✅ Firebase Admin initializes with `key.json`
- ✅ Firestore queries execute successfully

**Remaining for Demo:**
- Upload real video files via UI to replace placeholder URLs
- Or update seed data with valid Storage URLs

---

### 2026-01-12 - Session 7: Elements Page Polish & Data Cleanup + CreateMix Fix

**What happened:**
- Fixed Firestore index error for hooks with `affiliate` filter
- Discovered and fixed duplicate data in tables (same item showing 4x)
- Root cause: affiliate filter was disabled + pagination didn't use offset
- Cleaned up mock seed data (fake Storage paths) → deleted `test-hook-001`, `test-body-001`, `test-cta-001`, `test-overlay-001`
- Recreated bodies/ctas entries from real uploaded videos in `videos` collection
- Fixed perpetual loading spinners in all table components
- **Fixed CreateMix page** - video selectors now render

**Bugs Fixed:**

1. **Duplicate rows in tables**
   - Cause: Hooks route had affiliate filter disabled, so `affiliate=true` and `affiliate=false` queries returned same results
   - Fix: Enabled affiliate filter, added proper `offset()` for pagination

2. **Loading spinners never stopping**
   - Cause: `<MiniLoading />` was always rendered (unconditional)
   - Fix: Made conditional on `isValidating` in HooksTable, BodiesTable, CtaTable, OverlayTable

3. **Mock data with fake Storage paths**
   - Cause: Seed script created documents pointing to non-existent files
   - Fix: Deleted mock data, recreated from real uploaded videos

4. **CreateMix page showing empty selectors**
   - Cause: Template `groups[].name` was "Hooks"/"Bodies"/"CTAs" but UI expects `"videoChoosing"`
   - Fix: Updated `mixTemplates/Own_Creation` to use `groups[].name = "videoChoosing"`
   - Location: `Generic_Templates.tsx:419` has hardcoded `group.name === "videoChoosing"` check

**Files Modified:**
```
# API Routes - fixed hasMore calculation + affiliate filter
app/api/search/hooks/route.ts
app/api/search/bodies/route.ts
app/api/search/ctas/route.ts
app/api/search/overlays/route.ts
app/api/search/scripts/route.ts
app/api/search/backgroundMusic/route.ts

# UI Components - fixed perpetual spinners
app/(home)/hooks/(hooksTable)/HooksTable.tsx
app/(home)/hooks/(bodiesTable)/BodiesTable.tsx
app/(home)/hooks/(ctasTable)/CtaTable.tsx
app/(home)/hooks/(overlaysTable)/OverlayTable.tsx

# Firestore indexes
firestore.indexes.json  # Added affiliate+companyId+addedOn index
```

**Current Data State:**
| Collection | Count | Real Files |
|------------|-------|------------|
| bodies | 1 | ✅ `kZrBETlhcA3aWr4jkPhJ` (test-body) |
| ctas | 1 | ✅ `qq54gK5U6SSpMyg8VXOB` (test-cta) |
| hooks | 0 | ❌ Need to upload |
| overlays | 0 | ❌ Need to upload |
| videos | 2 | ✅ Original uploads from Session 5 |

**What's Working Now:**
- ✅ Elements page loads cleanly
- ✅ Tables show only real data (no mock/fake paths)
- ✅ No perpetual loading spinners
- ✅ SWR revalidation works correctly (spinner shows briefly on tab focus, then hides)

**Next Steps:**
1. Upload a hook video via Elements page
2. Test CreateMix page
3. Test VideoMix pipeline end-to-end

---

### 2026-01-13 - Session 8: Video Pipeline Backend Verified + MeiliSearch Integration

**What happened:**
- Verified video pipeline works END-TO-END on **backend** (not UI)
- Integrated MeiliSearch locally (no Docker)
- Fixed multiple data/config issues
- Cleaned up duplicate user records

**Video Pipeline Verification (Backend):**
```
1. Created VideoMix via script (node seed-data.js mix)
2. Trigger fired (onCreateMixes) ✅
3. Parts subcollection created ✅
4. Pub/Sub message published ✅
5. Worker received and processed ✅
6. Video rendered and uploaded to Storage ✅
7. VideoMix status → "ready" ✅
8. New video doc created: videos/uJPF7VJx5E2G9XiyFiBb
```

**Output location:**
- Storage: `mixes/2026-01-13/test-mix-{id}/local-user-001.603.22.1.mp4`
- Downloaded to: `~/Downloads/rendered-mix-output.mp4`

**MeiliSearch Integration:**
- Installed via `brew install meilisearch`
- Created `meili-backfill.js` script to index Firestore → MeiliSearch
- Master key: `VI6MVLjlLU63mamIQxr2MB5jQ_G_i9dTvx_hhKrHNd0`
- All 11 indexes configured and populated

**New Commands:**
```bash
# Start MeiliSearch (Terminal 1)
meilisearch --master-key="VI6MVLjlLU63mamIQxr2MB5jQ_G_i9dTvx_hhKrHNd0"

# Run backfill (Terminal 2) - indexes Firestore data into MeiliSearch
cd "_projects/adloops-local/ads-library-automation/functions" && node meili-backfill.js
```

**Files Created:**
```
ads-library-automation/functions/meili-backfill.js  # Firestore → MeiliSearch indexer
```

**Files Modified:**
```
Ads_Platform_Web/.env.local  # Added NEXT_PUBLIC_MEILI_SEARCH_HOST and KEY
```

**Data Fixes:**
1. **Uploaded real video files** to Storage:
   - `videos/kZrBETlhcA3aWr4jkPhJ/9:16/test-body.mp4` (8.7 MB)
   - `videos/qq54gK5U6SSpMyg8VXOB/9:16/test-cta.mp4` (2.5 MB)

2. **Added mock social_media_config** to `config/local-config`:
   - `social_media_config.meta.businesses[]`
   - `social_media_config.meta.pages[]`
   - `social_media_config.tiktok.businesses[]`
   - `social_media_config.pinterest.businesses[]`

3. **Deleted duplicate/test users:**
   - Removed `local-user-001` (duplicate email with auth user)
   - Removed `test-user-1768071860283`, `trigger-test-1768074855680`
   - Remaining: `ivntJL5sL6YEEmMFbE788q74lYi2` (actual auth user)

**What's Working:**
- ✅ Video pipeline (backend): Mix creation → trigger → worker → render → upload
- ✅ MeiliSearch: Videos page search, Mixes page search
- ✅ Elements page: All tables load with real data
- ✅ Videos page: Search returns results

**What's Still Broken:**
- ❌ **Sidebar crash on video checkbox** - `dataToSent.videos` undefined
  - Root cause: Data dependency not fully seeded
  - Impact: Can't select videos for campaign creation via UI
- ❌ Supabase features (expected - not in scope)

**Key Learnings:**
1. **MeiliSearch local setup is simple** - `brew install` + backfill script, no Docker needed
2. **Storage files vs Firestore docs** - Documents can exist but point to missing files
3. **Data dependencies cascade** - UI features touch multiple data structures unexpectedly
4. **Backend vs UI verification** - Pipeline working on backend ≠ UI flow working

**Remaining for Full UI Demo:**
- Debug Sidebar crash (video selection)
- Or accept limitation: demo video pipeline via backend, not UI

---

### 2026-01-14 - Session 9: Firestore Indexes & System Analysis

**What happened:**
- Analyzed all query patterns across codebase (functions + frontend)
- Updated `firestore.indexes.json`: 17 → 38 composite indexes
- Deployed indexes to adloops-local
- Validated existing docs against new findings

**Files Modified:**
- `firestore.indexes.json` - Added 21 composite indexes
- `adloops-firestore-schema.md` - Added indexes reference section

**Key Finding:**
MeiliSearch sync uses Firebase Extension (not custom code) - configured in `.firebaserc`. This explains why mocking routes worked for local setup without needing sync logic.

**Commands:**
```bash
# Deploy all indexes
firebase deploy --only firestore:indexes --project adloops-local

# View current indexes
firebase firestore:indexes --project adloops-local
```

**Doc Gaps Identified (for future threads):**
- MeiliSearch section missing from system-analysis.md
- Function interaction map (what triggers what)
- Complete schema extraction

---

## Master Task List

### Phase 1: Complete Replication (Current)

**Definition of "Working":**
- [x] Elements page loads with real data ✅
- [x] CreateMix page shows selectors ✅
- [x] VideoMix triggers fire (onCreateMixes) ✅ (verified backend)
- [x] Worker processes queue ✅ (verified backend)
- [x] VideoMix status reaches "ready" ✅ (verified backend)
- [x] MeiliSearch integrated ✅
- [ ] **UI flow: Select video → create campaign** ❌ (Sidebar crash)

**Backend Pipeline: VERIFIED ✅**
```
VideoMix created → Trigger fires → Parts created → Pub/Sub → Worker → Render → Upload → Status "ready"
```

**Remaining for Full UI:**
- [ ] Debug Sidebar crash (`dataToSent.videos` undefined)
- [ ] Test CreateMix page submission via UI
- [ ] Test full UI flow: Select videos → Submit → See result

### Phase 2: Documentation

**Schema Extraction (Dedicated Thread):**
- [ ] Consolidate schema corrections into main doc
- [ ] Query actual Firestore data to verify state
- [ ] Grep UI code for remaining hardcoded values
- [ ] Document all enum values systematically

**Decide Doc Structure:**
- [ ] What does handoff doc become? (Thread handoff vs official guide)
- [ ] Create `adloops-internals-guide.md`? (How system works)
- [ ] Separate replication guide from integration guide?

### Phase 3: CLoops Integration

**Planning:**
- [ ] Identify integration points in AdLoops pipeline
- [ ] Define what CLoops provides (content generation?)
- [ ] Map CLoops output → AdLoops input

**Implementation:**
- [ ] Create new CLoops template in mixTemplates
- [ ] Test CLoops → VideoMix flow
- [ ] Demo to CTO

### Sprint Success Criteria

> **Goal:** Prove to CTO ability to build and implement CLoops independently without external resources.

- [ ] Local AdLoops replication working
- [ ] CLoops integration points documented
- [ ] New CLoops template created
- [ ] End-to-end demo ready
