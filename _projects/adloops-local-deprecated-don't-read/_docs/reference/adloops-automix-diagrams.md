# AutoMix System Diagrams

## A. The Data Flow

How a template goes from creation → storage → execution → output.

```mermaid
flowchart LR
    subgraph Frontend
        UI[User creates template]
        Form[Form components]
    end

    subgraph Firestore
        Config[(auto-mix-templates)]
    end

    subgraph Backend
        Trigger[Cron / manual trigger]
        Selector[ComponentSelector]
        Generator[CombinationGenerator]
        Creator[MixCreator]
    end

    Output[Video mixes]

    UI --> Form
    Form -->|saves config| Config
    Trigger -->|reads config| Config
    Config --> Selector
    Selector -->|fetches media| Generator
    Generator -->|creates combinations| Creator
    Creator --> Output
```

**Story:** User builds template in UI → saves to Firestore → backend reads it → fetches media → generates mixes.

---

## B. The Collections Map

What collections exist, what's in them, how they relate.

```mermaid
flowchart TB
    subgraph Configs
        AMT[(auto-mix-templates)]
    end

    subgraph Media Sources
        SI[(saved-images)]
        CM[(cloops-media)]
    end

    AMT -->|current| SI
    AMT -.->|NEW with CLoops| CM
```

### Collection Schemas

**auto-mix-templates** (the config)
```json
{
  "id": "template123",
  "name": "My Campaign",
  "components": [
    {
      "type": "body",
      "source": "cloops-media",
      "selectedImageIds": [],
      "conditions": [{ "field": "sourceTemplate", "operator": "==", "value": "comic-books" }]
    }
  ]
}
```

**saved-images** (manual uploads)
```json
{
  "id": "abc123",
  "type": "body",
  "language": "english",
  "tags": ["promo"],
  "image": [{ "fileURL": "...", "fileName": "..." }]
}
```

**cloops-media** (CLoops output) — NEW
```json
{
  "id": "xyz789",
  "sourceTemplate": "comic-books-standard",
  "contentType": "images",
  "language": "english",
  "tags": ["bible", "comic"],
  "media": [{ "fileURL": "...", "fileName": "..." }]
}
```

---

## C. The Component Sourcing

How a Body component gets its actual images.

### Current (No CLoops)

```mermaid
flowchart LR
    Config[ComponentConfig<br/>type: body]
    Query[Query saved-images<br/>WHERE type = body]

    subgraph saved-images
        S1[doc1: body]
        S2[doc2: hook]
    end

    Result[doc1 selected]

    Config --> Query
    Query --> saved-images
    S1 --> Result
```

Collection is implicit. `type: body` means query `saved-images` where `type == body`.

### With CLoops (NEW)

```mermaid
flowchart LR
    Config[ComponentConfig<br/>type: body<br/>source: cloops-media]

    Router{source?}

    subgraph saved-images
        SI1[manual uploads]
    end

    subgraph cloops-media
        CM1[doc1: comic-books]
        CM2[doc2: testimonials]
    end

    Result[doc1 selected]

    Config --> Router
    Router -->|saved-images| saved-images
    Router -->|cloops-media| cloops-media
    CM1 --> Result
```

**The difference:** `source` field explicitly routes to the correct collection.

---

## Summary

| Concept | Current | With CLoops |
|---------|---------|-------------|
| Media source | `saved-images` only | `saved-images` OR `cloops-media` |
| Source selection | Implicit (hardcoded) | Explicit (`source` field) |
| Role assignment | `type` field in saved-images | `type` field in ComponentConfig |
| CLoops role | N/A | Just outputs media, no role |
