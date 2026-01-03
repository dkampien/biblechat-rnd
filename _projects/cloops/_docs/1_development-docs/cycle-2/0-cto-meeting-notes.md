# CTO Meeting Notes: CLoops Next Phase

**Date**: 2025-12-22
**Status**: Needs clarification

---

## 1. New Template: Face/Persona Videos

**Context**: AdLoops has unused "faces" assets
**Goal**: Generate hook videos with person in various settings (selfie, podcast, street, etc.)

**Questions**:
- [ ] Get face assets from AdLoops - what format? static or video?
- [ ] One template with setting parameter, or separate templates per setting?

---

## 2. Carousel Automation

**Examples shown**:
- "God wants to tell you to put a verse on your lockscreen"
- "God wants to show you a message"

**Questions**:
- [ ] Get full list of carousel types currently in production
- [ ] What's the structure? Image sequences? Page count? Layout variations?

---

## 3. Localization Strategy (40 Languages)

**CTO quotes**:
- "I want to spend $500 on each country with 150% [ROI] at 12 months"
- "I want to make the app truly localized, 40 languages"
- "I want to spend any amount of money without caring about the content"

**Interpretation**: Make content generation so cheap/automated it's not a constraint on ad spend.

**Architecture decision needed**:
```
Option A: Language as template parameter
  {template}/{story-id}/{language}/

Option B: Post-processing localization
  Generate English → translate/adapt

Option C: Generate directly in target language
  LLM prompts in each language
```

**Questions**:
- [ ] Which 10 languages are priority 1?
- [ ] Translation or cultural adaptation?
- [ ] Do visuals need localization too?
- [ ] Timeline?

---

## 4. Asset Reuse (Unclear)

**CTO question**: Can comic outputs be reused without regenerating?

**Note**: CTO created AdLoops, so he knows about Firestore component reuse. Must be asking about something else.

**Possible meanings**:
- Cross-template reuse? (comic-books-standard panel in comic-books-ads)
- Platform reformatting? (9:16 → 16:9 without regenerating)
- --replay mode awareness? (regenerate images without re-running LLM)
- Asset versioning? (same story, multiple visual styles)
- Remixing? (combine panels from different comics)

**Questions**:
- [ ] Clarify what he meant - context of the question?

---

## 5. Content Pipeline Integration

**Note**: "You need to handle content pipelines"

**Questions**:
- [ ] Who are stakeholders in marketing/production?
- [ ] What content do they produce regularly?
- [ ] What are the bottlenecks?

---

## Unclear Notes

- [ ] "Theme and content type" - what was this about?
- [ ] "Scaled marketing on content generation" - what context?

---

## Next Actions

1. Get face assets from AdLoops
2. Catalog all carousel types
3. Meet with marketing/production team
4. Design localization architecture
5. Clarify asset reuse ownership
