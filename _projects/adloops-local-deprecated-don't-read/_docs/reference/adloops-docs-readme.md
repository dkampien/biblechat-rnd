# AdLoops Documentation Index

> Entry point for AdLoops local replication docs.
>
> **Status:** Local replication working (backend pipeline verified). UI has minor issues.
> **Goal:** CLoops integration with AdLoops video pipeline.

---

## Quick Start

**First time?** Read in this order:
1. `adloops-replication-handoff.md` → Quick Reference section (commands, credentials)
2. `adloops-system-analysis.md` → Understand the architecture
3. `adloops-diagrams.md` → Visual reference

**Building seed data?**
→ `adloops-firestore-schema-complete.md` (source of truth for field values)

**Looking up a function?**
→ `adloops-functions-reference.md`

---

## Document Map

| Doc | Purpose | When to Use |
|-----|---------|-------------|
| **adloops-replication-handoff.md** | Session log, commands, gotchas, credentials | Starting the local env, troubleshooting |
| **adloops-firestore-schema-complete.md** | Exact field values for seed data | Building/fixing seed-data.js |
| **adloops-system-analysis.md** | TypeScript types, architecture, integration points | Understanding how AdLoops works |
| **adloops-diagrams.md** | Mermaid diagrams of data flow | Visual understanding of pipeline |
| **adloops-functions-reference.md** | List of all 60 Cloud Functions | Finding which function does what |

---

## Key Commands

```bash
# Start everything (3 terminals) - run from project root
meilisearch --master-key="VI6MVLjlLU63mamIQxr2MB5jQ_G_i9dTvx_hhKrHNd0" --db-path="_projects/adloops-local/data.ms"
cd "_projects/adloops-local/Ads_Platform_Web" && bun run dev
cd "_projects/adloops-local/ads-library-automation/functions" && npx ts-node src/worker/worker.ts

# Validate/fix Firestore data
cd "_projects/adloops-local/ads-library-automation/functions"
node seed-data.js validate   # Check for issues
node seed-data.js fix        # Auto-fix common issues

# MeiliSearch doesn't auto-sync locally - run after Firestore changes
node meili-backfill.js
```

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Search results empty/stale | MeiliSearch not synced | Run `node meili-backfill.js` |
| Sidebar not showing | User role wrong | Need `role: "superEditor"` in Firestore |
| Elements page error loop | MeiliSearch not running | Start MeiliSearch first |
| "Cannot read property X" | Missing seed data field | Run `node seed-data.js validate` |
| Videos not rendering | Worker not running | Start worker in Terminal 3 |

---

## Credentials

```
UI Login:     local@adloops.test / localtest123
Firebase:     adloops-local (eur3 / europe-west1)
MeiliSearch:  localhost:7700 (key in .env.local)
```

---

## Related Files (in code repo)

| File | Location |
|------|----------|
| Seed script | `ads-library-automation/functions/seed-data.js` |
| MeiliSearch backfill | `ads-library-automation/functions/meili-backfill.js` |
| Firestore indexes | `ads-library-automation/firestore.indexes.json` |
| Frontend env | `Ads_Platform_Web/.env.local` |
