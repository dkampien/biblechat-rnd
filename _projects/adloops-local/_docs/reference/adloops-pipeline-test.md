# AdLoops Pipeline Test Plan

## Fix Applied
- ✅ Added `region: "eur3"` to all triggers in `functions/src/triggers/mixes.ts`
- ✅ Deleted old broken us-central1 functions
- ⏳ Redeploying to eur3 (in progress)

## Test Sequence (Once Deployment Complete)

### Step 1: Create Test VideoMix
```bash
cd _projects/adloops-local/ads-library-automation/functions
node seed-data.js mix
```

### Step 2: Monitor Logs for Trigger Firing
```bash
firebase functions:log --project adloops-local
```

**Expected logs:**
```
onCreateMixes: Creating parts for mix...
onCreateMixPart: Processing part 1 of 1
onCreateMixPart: Creating task for worker
```

### Step 3: Check VideoMix Status
```bash
node -e "
const admin = require('firebase-admin');
const path = require('path');
admin.initializeApp({
  credential: admin.credential.cert(
    path.join(process.env.HOME, 'adloops-credentials/adloops-local-firebase-adminsdk-fbsvc-44775403ca.json')
  ),
  storageBucket: 'adloops-local.firebasestorage.app'
});

const db = admin.firestore();
(async () => {
  const mix = await db.collection('videoMixes').orderBy('createdAt', 'desc').limit(1).get();
  mix.forEach(doc => {
    console.log('Mix ID:', doc.id);
    console.log('Status:', doc.data().status);
  });
  process.exit(0);
})();
"
```

**Expected results:**
- `status: "new"` immediately after creation
- `status: "running"` after `onCreateMixes` starts processing (if parts created)
- `status: "ready"` when all parts complete (eventually)

### Step 4: Check Parts Created
```bash
node -e "
const admin = require('firebase-admin');
const path = require('path');
admin.initializeApp({
  credential: admin.credential.cert(
    path.join(process.env.HOME, 'adloops-credentials/adloops-local-firebase-adminsdk-fbsvc-44775403ca.json')
  ),
  storageBucket: 'adloops-local.firebasestorage.app'
});

const db = admin.firestore();
(async () => {
  const mix = await db.collection('videoMixes').orderBy('createdAt', 'desc').limit(1).get();
  const mixId = mix.docs[0].id;
  const parts = await db.collection('videoMixes').doc(mixId).collection('parts').get();
  console.log('Mix ID:', mixId);
  console.log('Parts count:', parts.size);
  parts.forEach(doc => {
    console.log('  -', doc.id, '|', doc.data().status);
  });
  process.exit(0);
})();
"
```

**Expected:** At least 1 part created with `status: "new"`

### Step 5: Check Storage Output
If worker processes complete:
- Go to Firebase Console → Storage
- Check `outputs/` folder for rendered videos
- Should see files like `test-mix-*/part-1/output.mp4`

## Success Criteria

✅ All of the following must be true:

1. **Trigger fires:** `onCreateMixes` appears in logs when VideoMix created
2. **Parts created:** Subcollection `videoMixes/{id}/parts` has at least 1 document
3. **Part status:** Part has `status: "new"` or `status: "uploaded"` (if processing completes)
4. **Worker processes:** Logs show `onCreateMixPart` → `createTaskForWorker`
5. **Output video:** Final processed video appears in Storage (eventually)

## If Tests Fail

**Check 1: Function deployed to eur3?**
```bash
firebase functions:list --project adloops-local | grep "eur3"
```

**Check 2: Any error logs?**
```bash
firebase functions:log --project adloops-local | grep -i error
```

**Check 3: Firestore rules allow writes?**
Firebase Console → Firestore → Rules → should be in test mode (allow all)

## Known Issues to Check

1. **MyVideoMixBuilder.build() failing** - Check if it's trying to access undefined config
2. **Worker not processing** - Check if Pub/Sub topic exists
3. **Video output not in storage** - Check if FFmpeg is available in function environment

