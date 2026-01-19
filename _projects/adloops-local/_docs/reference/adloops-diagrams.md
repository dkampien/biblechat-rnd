# AdLoops System Diagrams

> Visual reference for AdLoops architecture. Companion to `adloops-system-analysis.md`.
>
> **Last validated:** 2026-01-09 against `_projects/_adloops/` codebase

---

## 1. Component Data Structure

Components (hooks, bodies, ctas) are just video files with metadata.

```mermaid
graph TD
    subgraph "Firestore Collections"
        Hooks[(hooks/)]
        Bodies[(bodies/)]
        CTAs[(ctas/)]
    end

    subgraph "Component Structure"
        VidStruct["`**IHook / IBody / ICta**
        {
          video: 'file-123.mp4'
          raw_video: {portrait, square, landscape, tiktok}
          preview: {fileURL, format}
          extracted_texts: ['text from video']
          duration: number
          language, userId, companyId
        }`"]
    end

    Hooks --> VidStruct
    Bodies --> VidStruct
    CTAs --> VidStruct

    classDef collectionNode fill:#e74c3c,stroke:#c0392b,color:#fff,font-weight:bold
    classDef structNode fill:#3498db,stroke:#2980b9,color:#fff

    class Hooks,Bodies,CTAs collectionNode
    class VidStruct structNode
```

---

## 2. Mix Creation Flow

Overlays are defined at mix/part level, not stored with components.

```mermaid
graph TD
    User[User/AutoTemplate]

    User --> CreateMix[Create VideoMix Document]

    CreateMix --> MixDoc["`**MyVideoMix**
    {
      components: {hooks, bodies, ctas},
      overlay: [...],
      captions: {...},
      crossFadeDuration: 0.4
    }`"]

    MixDoc --> BuildProcess[MyVideoMixBuilder.build]

    BuildProcess --> CreateParts[Create Mix Parts]

    CreateParts --> Part1["`**MyVideoMixPartDoc**
    videoLayers: [
      {videos: ['hook.mp4'], overlay: [...]},
      {videos: ['body.mp4'], overlay: [...]}
    ]
    audioLayers: [...]`"]

    Part1 --> ProcessPart[MyVideoMixGenerator.build]

    ProcessPart --> Steps["`**Processing Steps:**
    1. Build each video layer
    2. Add per-layer overlays
    3. Cross-fade layers together
    4. Add cross-layer overlays
    5. Add captions if configured
    6. Mix audio tracks
    7. Upload final video`"]

    classDef userNode fill:#9b59b6,stroke:#8e44ad,color:#fff
    classDef docNode fill:#3498db,stroke:#2980b9,color:#fff
    classDef processNode fill:#e67e22,stroke:#d35400,color:#fff

    class User userNode
    class MixDoc,Part1 docNode
    class CreateMix,BuildProcess,CreateParts,ProcessPart,Steps processNode
```

---

## 3. Overlay Processing

Two types of overlays with different application timing.

```mermaid
graph TD
    MixPart[Mix Part with Layers]

    MixPart --> PerLayer[Per-Layer Overlays]
    MixPart --> CrossLayer[Cross-Layer Overlays]

    PerLayer --> PerLayerDef["`**MyVideoMixPartLayer.overlay**
    Applied to specific video layer
    Rendered BEFORE cross-fade`"]

    CrossLayer --> CrossLayerDef["`**MyVideoMixPartDoc.overlay**
    Applied AFTER layers merged
    Can span multiple layers
    Uses offset + layersLength`"]

    PerLayerDef --> OverlayTypes[Overlay Types]
    CrossLayerDef --> OverlayTypes

    OverlayTypes --> StaticOverlay["`**Static Overlay**
    generationType: 'manual'
    fileName: 'overlay.png'`"]

    OverlayTypes --> DynamicOverlay["`**Dynamic Overlay**
    generationType: 'auto'
    compositionId: 'text-overlay'
    params: [{key: 'text', value: '...'}]`"]

    OverlayTypes --> Captions["`**Captions (Timed)**
    srtFileName: 'captions.srt'
    Per-screen timing`"]

    classDef partNode fill:#3498db,stroke:#2980b9,color:#fff
    classDef typeNode fill:#e67e22,stroke:#d35400,color:#fff
    classDef overlayNode fill:#2ecc71,stroke:#27ae60,color:#fff

    class MixPart partNode
    class PerLayer,CrossLayer typeNode
    class StaticOverlay,DynamicOverlay,Captions overlayNode
```

---

## 4. Processing Pipeline

Complete flow from trigger to final video.

```mermaid
graph TD
    Start[User or AutoTemplate]

    Start --> Step1["`**1. Create VideoMix**
    Status: 'new'
    Firestore: videoMixes/`"]

    Step1 --> Trigger1[Firebase Trigger:<br/>onCreateMixes]

    Trigger1 --> Step2["`**2. Build Mix Structure**
    MyVideoMixBuilder.build
    - Resolve component IDs
    - Generate combinations
    - Create parts`"]

    Step2 --> Step3["`**3. Create Mix Parts**
    Firestore: videoMixes/{id}/parts/
    Each part = one video output`"]

    Step3 --> Trigger2[Firebase Trigger:<br/>onCreateMixPart]

    Trigger2 --> Step4["`**4. Queue Worker Task**
    Pub/Sub: ProcessVideoMix`"]

    Step4 --> Step5["`**5. Generate Video**
    MyVideoMixGenerator.build
    - Re-encode layers
    - Apply overlays
    - Cross-fade
    - Add captions
    - Mix audio`"]

    Step5 --> Step6["`**6. Upload Result**
    - Upload to Cloud Storage
    - Create videos/ document
    - Status: 'uploaded'`"]

    Step6 --> Step7["`**7. Complete**
    If all parts done:
    Mix status: 'ready'`"]

    classDef userNode fill:#9b59b6,stroke:#8e44ad,color:#fff
    classDef stepNode fill:#3498db,stroke:#2980b9,color:#fff
    classDef triggerNode fill:#e74c3c,stroke:#c0392b,color:#fff
    classDef processNode fill:#e67e22,stroke:#d35400,color:#fff

    class Start userNode
    class Step1,Step2,Step3,Step6,Step7 stepNode
    class Trigger1,Trigger2 triggerNode
    class Step4,Step5 processNode
```

---

## 5. Data Sources

Where overlay content comes from.

```mermaid
graph TD
    OverlayNeedsData[Overlay Needs Content]

    OverlayNeedsData --> Source1[Overall Datasource]
    OverlayNeedsData --> Source2[Self Datasource]

    Source1 --> Overall["`**AutoTemplateFormat.dataSource**
    - CSV file
    - BigQuery table
    - Firestore query

    Example: Story metadata
    {story, verse, character}`"]

    Source2 --> Self["`**Component extracted_texts**
    Text extracted from video

    Example: Transcription
    ['David said...', 'Goliath replied...']`"]

    Overall --> UseCase1["`**Use Cases:**
    Title cards
    Verse references
    Static metadata`"]

    Self --> UseCase2["`**Use Cases:**
    Subtitles/captions
    Transcriptions
    Per-scene content`"]

    classDef sourceNode fill:#3498db,stroke:#2980b9,color:#fff
    classDef detailNode fill:#2ecc71,stroke:#27ae60,color:#fff
    classDef useCaseNode fill:#f39c12,stroke:#d68910,color:#fff

    class OverlayNeedsData sourceNode
    class Overall,Self detailNode
    class UseCase1,UseCase2 useCaseNode
```

---

## 6. Vertical Stack Model

Each component is processed as a vertical stack of layers.

```mermaid
graph LR
    subgraph "Timeline (Horizontal)"
        direction LR
        Hook[HOOK<br/>3 sec]
        Body[BODY<br/>15 sec]
        CTA[CTA<br/>2 sec]

        Hook -->|cross-fade| Body
        Body -->|cross-fade| CTA
    end

    subgraph "Each Component = Vertical Stack"
        Stack["Base Video<br/>+<br/>Overlay 1<br/>+<br/>Overlay 2<br/>+<br/>Audio"]
    end

    Hook -.->|has| Stack
    Body -.->|has| Stack
    CTA -.->|has| Stack

    classDef timelineNode fill:#2ecc71,stroke:#27ae60,color:#fff,font-weight:bold
    classDef stackNode fill:#f39c12,stroke:#d68910,color:#fff

    class Hook,Body,CTA timelineNode
    class Stack stackNode
```

**Processing Order per Component:**
```
1. Load base video
2. Apply overlay 1 (on top)
3. Apply overlay 2 (on top)
4. Apply overlay n...
5. Mix audio layers
= Complete component ready for merge
```

**After all components:**
```
6. Cross-fade merge (Hook → Body → CTA)
7. Apply cross-layer overlays
8. Add captions (timed)
9. Final audio mix
10. Upload
```

---

## 7. Video Ad Structure

Decision tree for component processing.

```mermaid
graph TD
    Start[Video Ad]

    Start --> Hook[HOOK]
    Start --> Body[BODY - 1 or more]
    Start --> CTA[CTA]

    Body --> BodyGenerated[GENERATED<br/>AI-created]
    Body --> BodyAsset[ASSET<br/>Pre-made video]

    BodyGenerated --> BodySelfOverlay[SELF OVERLAY<br/>Complete - no overlays needed]
    BodyGenerated --> BodyOverlay[NEEDS OVERLAY]
    BodyAsset --> BodyOverlay

    BodyOverlay --> OverlayType[Overlay Type]

    OverlayType --> PreMade[PRE-MADE<br/>generationType: 'manual']
    OverlayType --> Generated[GENERATED<br/>generationType: 'auto']

    PreMade --> DataSource[Data Source]
    Generated --> DataSource

    DataSource --> Overall[OVERALL<br/>CSV/BigQuery]
    DataSource --> Self[SELF<br/>extracted_texts]

    classDef primaryNode fill:#4a90e2,stroke:#2e5c8a,color:#fff
    classDef convergeNode fill:#50c878,stroke:#2e8b57,color:#fff
    classDef dataNode fill:#f39c12,stroke:#d68910,color:#fff
    classDef endNode fill:#e74c3c,stroke:#c0392b,color:#fff

    class Start,Hook,Body,CTA primaryNode
    class BodyOverlay,OverlayType,DataSource convergeNode
    class Overall,Self dataNode
    class BodySelfOverlay endNode
```

---

## Quick Reference

| Concept | Technical Reality |
|---------|-------------------|
| Component Types | All are just video files (IHook/IBody/ICta) |
| Where Overlays Defined | At mix/part level, not component level |
| GENERATED vs ASSET | Workflow distinction only |
| Overlay Types | `generationType: "manual" \| "auto"` |
| Data Sources | Overall (dataSource) vs Self (extracted_texts) |
| Per-Screen Timing | Only for captions (SRT files) |
