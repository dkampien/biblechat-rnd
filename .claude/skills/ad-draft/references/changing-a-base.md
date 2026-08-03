---
created: 2026-08-03
updated: 2026-08-03
---

# Changing a base: the change economics

Loaded only on EXISTING BASE entry. The dependency facts, per kind of change. The right column is YOURS to act on: in place it is your `replan` list; on a child it is what you leave OUT of `inherit`.

| change | scope | what it invalidates |
|---|---|---|
| voice fill | whole-ad | every vo + every video sized to one |
| music fill | whole-ad | the music bed only |
| a beat's `vo` line | per-beat | that beat's vo + the video sized to it |
| a beat's `visual` | per-beat | that beat's still + video |
| a cast member's lock/anchor | per-member | the stills + videos of beats whose visual names that member |
| a cast member's voice | per-member | that member's voiced lines + their videos |
| **swap a file reference** | per-beat | **nothing; a relink is $0** |
| character / treatment / set / anchor | whole-ad | every GENERATED still + video |

- The gender rule survives every change: **voice and character stay gender-matched**.
- **The reference exception (load-bearing):** references are never regenerated, they were never generated. They change only by explicit re-reference: in place via `use-asset` (idea status), on a child via the beat's `asset` key. A different hook clip or music bed on a reference-mix ad is a $0 swap.
- **Editing in place writes ONLY the script.** `update-beat` takes `vo`/`visual`/`delivery`/`speaker`; `update-ad` takes the whole-ad fills plus `anchor`/`notes`; send only actual deltas (the verbs refuse no-op edits). No production consequence happens on its own: you follow with `replan` on each position the edit invalidates (a prompt-only change is a `replan` carrying the new prompt, no script edit at all). The net for your judgment is `npm run ads -- lint <slug>`: its staleness section compares the script against what every row was made from. Run it after an edit round, always before handing to production.
- **Batching children is the point**: several hooks at once, each its own child, everything else held fixed so the batch tests ONE cell; keep the batch divergent, near-identical variants cannibalize each other's reach.
- **Metrics-driven picks (when Meta data exists):** weak 2s/6s views → the hook; weak 25%/50% watch-through → the body beats; weak CTR → the cta. Read the metric, point at the cell, land the batch as children.
