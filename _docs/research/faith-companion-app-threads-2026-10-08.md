---
created: 2026-10-08
updated: 2026-10-08
---

# Faith, companion and app: what the session transcripts say

Scope: only the Claude Code session transcripts stored for the auto-ads-four project (`~/.claude/projects/-Users-dennisk-Documents-project---auto-ads-four/*.jsonl`). Project docs, data and readings were not used. Method: keyword scan of user and assistant messages for "faith" and "companion", then reading the matching messages in the sessions with the most hits.

## Shape of the material

The transcripts hold three kinds of threads:

1. **Ad creative work on the faith app.** Formats, hooks, grouping of ads into ad sets, and which pages the ads run under.
2. **Research and system design.** How an AI ad creative system should be built, and the evidence it should rest on.
3. **Meta-threads.** Dispatch messages between seats and the session that ran this search. Their keyword counts are inflated and say nothing about the product.

"Companion" as a product idea almost never appears in discussion. It appears in tool output and dispatch text. Treat "faith + companion" as "faith" in practice.

## 1. Ad creative work on the faith app

- **Newspaper-format ad, faith masthead (2026-08-21, `f6516497`).** Six checks ran on a static ad styled as a Sunday newspaper front page. The third gate caught a real problem: the masthead copied a real publication's name. Paid faith and health ads should not carry a live publisher's name. A one-line fix (replace the masthead text) would clear it.
- **Batch of 18 ads, one format, four ad sets (2026-09-29 `77edec98`, 2026-10-07 `2359ea82`, 2026-09-30 `fd314793`).** Two grouping options were argued. By theme: each ad set holds one problem. By persona: each ad set holds one person type and several formats across that person's problems. The recommended shape was four or five ad sets, one ad from each theme in each set, equal budgets, and seven days untouched. Reason: under broad targeting, an ad set is a budget pool and a learning unit (about 50 results a week), not an audience.
- **Problem framing in the winners (2026-10-08 `f1bdbdea`, `6c08a7ee`).** Winning faith ads treat the problem as a faith problem ("eleven years and God never used me"), and the quiz on the image answers it. Our ads treat it as a life problem (single parent, money). This gap is the main working hypothesis for why our first run lags.
- **Page placement (2026-10-05 `d80a0293`).** Our web ads ran under a creator page with 393 followers that took 17.5% of spend. Pages were picked by a rule that rotates about ten persona-style and brand pages. The page may be a poor fit for these ads. Winning statics ran under other pages.

## 2. Research and system design

- **Shape of the research brief (2026-10-07 `aa032ab0`).** The question was: which architecture lets a builder with no creative instinct produce winning faith ads at volume, and where does judgment sit. The answer carried the judgment in the system: exemplars harvested from proven ads, customer verbatim in place of invented copy, performance feedback in place of a strategist's read, and the human as a gate at a few points.
- **Trust in vision models (same thread).** The user does not trust vision models to judge faithfully. The working method: a reference ad becomes an HTML/CSS mold, and an agent writes the first version from it.
- **Evidence ranking (same thread).** Evidence was ranked: (1) our own web and app accounts, with a recent time window for fatigue, statics and static-like videos included; (2) direct faith-app competitors; (3) adjacent competitors by problem.
- **Whether faith apps are past "the third stage" (2026-10-08 `f1bdbdea`).** Faith apps claim a mechanism, which suggests they sell at the third stage of sophistication. Whether the market has moved past that is a question for competitor research.

## Open questions

- Is the faith-identity framing testable on our own accounts, or only inferable from competitors?
- Does the masthead problem also apply to any other publisher-style formats?
- Which page placement rule should the faith ads use?

## Coverage limits

- Keyword scan only. Threads that describe the same ideas without the words "faith" or "companion" were not found.
- Messages were read in excerpts (about 600 characters each, up to 25 per session), not in full.
- No session was checked against the project docs for accuracy.
