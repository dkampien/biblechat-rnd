# AI Content Generation: Workflow Architecture Guide

**Version**: 1.0
**Date**: 2025-12-31

---

## 1. Introduction

This guide teaches you how to plan AI content generation workflows - breaking content ideas into step-by-step plans.

**Use this guide when:**
- Planning multi-step content projects
- Choosing which AI modalities to use
- When you need consistent characters, styles, or settings across multiple scenes

**Use Prompt Generation Reference when:**
- You know your generation node (modality) and need to generate a prompt

**Flow:** Plan workflow (this guide) → Generate prompts for each generation node (Prompt Reference)

---

## 2. Understanding AI Models

### Why Model-Agnostic?

The AI model landscape changes constantly - new models release monthly, "best" models change weekly, specific names become outdated quickly. Instead of learning "Veo 3.1" or "Sora 2", focus on:

1. **Modalities** - What can models do?
2. **Workflows** - How do we chain capabilities?
3. **Prompting** - How do we communicate effectively?

This framework works regardless of which specific models exist.

### Models vs Platforms

**Models = The actual AI tools**
- Each has specific strengths and weaknesses
- Best suited for different purposes
- Think of them like tools in a toolbox
- Choose based on your specific needs

**Platforms = Webapps that host models**
- One platform can provide access to multiple models
- Example: Replicate hosts Veo, Flux, and many others
- Handle API access, billing, infrastructure

**Selection process:**
1. Identify purpose and scope (what you need created)
2. Choose best model for specific purpose
3. Identify modality needed (text-to-image, image-to-video, etc.)
4. Access via appropriate platform

---

## 3. Modalities: Model Capabilities

**Modality = A specific input→output capability**

Understanding modalities helps you choose the right tool, design effective workflows, and switch between models easily.

### Text / LLM Modalities

- **text-to-text (t2t)** - Text → generated/transformed text (persona, outlines, scripts, prompts)

### Image Generation Modalities

- **text-to-image (t2i)** - Text → generated image
- **image-to-image (i2i)** - Image + text → transformed image (style transfer, variations)
- **image-to-image_edit (i2i_edit)** - Image + text (prompt targeting) → edited image
- **image-to-image_reference (i2i_reference)** - Image + text + reference images/objects → transformed image with consistent elements

### Video Generation Modalities

- **text-to-video (t2v)** - Text → generated video (describes both visuals AND motion)
- **image-to-video (i2v)** - Image + text → animated video (text guides motion only)
- **image-to-video_frames (i2v_frames)** - First frame + last frame + text → interpolated video
- **image-to-video_reference (i2v_reference)** - Text + reference images → video with consistent elements (also called "elements" or "ingredients")
- **image-to-video_lipsync (i2v_lipsync)** - Image + audio (+ optional text) → lip-synced video
- **video-to-video (v2v)** - Video + text → transformed video
- **video-to-video_lipsync (v2v_lipsync)** - Video + audio (+ optional text) → lip-synced video
- **video-to-video_edit (v2v_edit)** - Video + text + targeting → edited video
- **video-to-video_motion (v2v_motion)** - Performance video + character reference image → motion/expression transferred

### 3D Generation Modalities

- **text-to-3d (t2-3d)** - Text → 3D model
- **image-to-3d (i2-3d)** - Image(s) → 3D model

**Note:** Most modern models support multiple modalities (e.g., t2v + i2v + frames-to-video in one model).

### Emerging Capabilities

**Multishot Video Generation:**
- Some new video models support camera cuts within a single generation
- Multishot prompt structures allow multiple shots/angles in one prompt
- Requires different prompting approach than traditional single-shot
- Capability and structure vary by model (requires model-specific research)

---

## 4. Workflows & Patterns

### What is a Workflow?

**Workflow = The complete pipeline from start to final output**

A workflow is a node pipeline/graph: each node transforms inputs into outputs, and outputs flow forward as inputs to later nodes.

- **Backbone:** prompt-driven generation nodes (modalities like t2t/LLM, t2i, i2v, t2v)
- **Support:** non-prompt nodes (utilities, editing, tools) that prepare/connect/polish outputs

Think of workflows like ComfyUI node graphs - each output feeds into the next input.

### Why Workflows?

Certain constraints require multi-step approaches:
- Duration Limits: Most video gen models cap at 5-12 seconds per generation. Longer content requries multiple generations chained together.
- Consistency Requirements: Same character across scenes may require multiple modalities chained together e.g., t2i, i2i_reference, i2v, etc.
- Complexity: An ad may require generating the scenes, editing the scenes, generating a character, placing a product, upscaling, etc. These may be all different modalities and nodes. 

**Simple Workflow:**
```
Goal: 8-second product video

Workflow:
├─ Step 1: Create product image → Node: text-to-image
└─ Step 2: Animate image → Node: image-to-video

Result: 8-second controlled video
```

**Complex Workflow:**
```
Goal: 30-second character video with consistency

Workflow:
└─ Pattern: Character Consistency
   ├─ Step 1: Craft persona → Node: LLM
   ├─ Step 2: Create appearance → Node: text-to-image
   ├─ Step 3: Build reference library → Node: image-to-image (×3)
   ├─ Step 4: Break down to 6 scenes → Node: LLM
   ├─ Step 5: Transform to prompts → Node: LLM (×6)
   ├─ Step 6: Generate scene images → Node: text-to-image (×6)
   ├─ Step 7: Animate scenes → Node: image-to-video (×6)
   └─ Step 8: Assemble final video → Node: Editing

Result: 30-second video, consistent character
```

> **Note:** The pattern wrapper is organizational, not structural. The actual hierarchy is Workflow → Steps → Nodes.

### Workflow Components

**Workflow**
- The complete pipeline from start to final output (e.g., "30-second character video")
- Can be simple (direct steps) or complex (using workflow patterns)
- Operations chain together: each output → next input

**Steps**
- Logical phases within a workflow
- Can contain one or multiple nodes
- Example: "Build reference library" or "Generate scene"
- Each step can use different models/modalities and supporting operations
- Steps may include prompts when they contain generation nodes (one prompt per generation node)

**Nodes**
- Atomic operations (smallest unit)
- Types: Generation modalities (t2t/LLM, t2i, i2v), utilities (extract frame), editing (stitch), tools (upscale)
- Each node can execute one modality, utility, editing operation, or tool

**Data Flow**
- Inputs: What you start with (text, image, video)
- Outputs: What each node produces → becomes next input

### Common Workflow Patterns (aka Techniques)

- Multi-step patterns for specific tasks
- Can encompass entire workflow OR be chained with other patterns
- Reusable across different workflows
- Built from multiple steps and nodes

**Tested patterns:**
- Character Consistency
- Frame Chaining
- Multi-Scene Content

**Reference (untested):**
- Relighting, Inpainting, Lipsync, Upscaling, Product Placement, LoRA training

#### Frame Chaining

**Purpose:** Extend a single continuous scene beyond model output duration limits (typically 5-10s).

**Why it's needed:**
- i2v/t2v models output fixed-duration clips (5s, 8s, 10s)
- Without chaining, every scene is locked to model output length → robotic pacing
- Frame chaining allows variable scene lengths (10s, 20s, 30s) based on narrative needs

**How it works:**
1. Generate initial video clip (t2v or i2v)
2. Extract last frame
3. Use extracted frame as input for next i2v call
4. Concatenate clips to form extended scene

```
[IMAGE] → i2v → [CLIP 1: 10s] → last frame → i2v → [CLIP 2: 10s] → last frame → i2v → [CLIP 3: 10s]

Concatenate: CLIP 1 + CLIP 2 + CLIP 3 = 30s continuous scene
```

**Scene duration is quantized:** Built from fixed blocks (10s, 20s, 30s)—not arbitrary lengths.

**Known limitations:**

| Issue | Description |
|-------|-------------|
| **Seam** | Motion discontinuity at join points (10s, 20s, etc.). The model generates fresh motion from a static frame—it doesn't know the velocity/direction that led there. Motion "restarts" at each chain. |
| **Drift** | Cumulative visual artifacts. Each chain introduces small changes (colors shift, details morph). By clip 3-4, noticeable divergence from original. |

**Practical limits:** 2-3 chains max before seam/drift become distracting. Best for extending 10s → 20-30s, not for very long continuous scenes (60s+).

**Prompt strategies (theoretical, needs validation):**
- Prefer ambient/looping motion (ripples, pulsing) over discrete actions with clear endpoints
- Camera motion may chain better than subject motion
- Continuation language ("motion continues...", "sustained drift...") may help

**When to use:**
- Scene needs 20-30s continuous action
- Variable pacing required

**When to avoid:**
- Single clip is sufficient
- Cuts between shots are acceptable
- Need more than ~30s continuous

#### Multi-Scene Content

**Planning scenes with model constraints:**

- Most models cap at 5-10 seconds per generation
- Break longer content into scenes
- Each scene = one generation (or multiple if using frame chaining)

**Scene transitions - three options:**

| Option | When to use | Trade-off |
|--------|-------------|-----------|
| **Cut** | Different angle/setting acceptable | Clean break, no continuity |
| **Frame chain** | Visual continuity needed (same character, setting) | Seam/drift issues (see Frame Chaining) |
| **Edit/dissolve** | Hide transition, stylistic choice | Post-processing required |

**Frame chaining use cases:**

| Use Case | Description | Example |
|----------|-------------|---------|
| **Scene Extension** | Same action continues beyond model limit | Walking → keeps walking (10s → 20s) |
| **Scene Transition** | Action changes, visual continuity maintained | Walking → stops → enters shop |

Scene transition is more forgiving—motion change at boundaries is expected, so seams are less jarring.

**Approaches for extending content:**
- **Frame chaining:** Last frame → i2v continuation (see Frame Chaining section)
- **First+last frame (i2v_frames):** Define start and end state, model interpolates between

**Scene structure:**
- Keep scenes focused (one main action/moment)
- Plan transitions in advance
- Consider pacing (fast cuts vs slow progression)
- Match emotional arc to story goal

**Example scene breakdown:**
```
30-second video → 6 scenes × 5 seconds

1. Establish setting (wide shot)
2. Introduce subject (medium shot)
3. Main action begins (close-up)
4. Action continues (different angle)
5. Resolution (pull back)
6. Closing (final moment)
```

**Key considerations:**
- Plan before generating (saves cost)
- Account for model duration limits
- Test frame chaining early if using it

---

## 5. Workflow Planning Process

Workflow planning is how you go from an idea → an executable pipeline.

The goal of planning is not to write prompts yet. It’s to remove ambiguity so execution is predictable.

### Planning Step 1: Define the Goal (IDEA)

Write the final output spec:
- Output type (image set, single video, multi-scene video)
- Target format (duration, aspect ratio, resolution)
- Key requirements (character consistency, specific style, must-have beats)
- Success criteria (what “done” looks like)
- Constraints (duration limits, tools available, quality requirements)

Also list any starting inputs you already have (script, voiceover, brand kit, references).

### Planning Step 2 (Optional): Gather Inspiration (INSPIRATION)

If you’re missing vocabulary or clarity, collect a small reference pack:
- **Look/style** (lighting, composition, color, wardrobe)
- **Motion/camera** (for video)
- “Do this / avoid this” examples

### Planning Step 3: Draft the Workflow Steps (MODALITIES → STEPS)

Break the goal into workflow steps (scenes/phases) you can execute within model constraints.

Guidelines:
- For video, duration ÷ per-generation limit (usually 5–10s) ≈ number of scenes/clips.
- For video, assume **one scene ≈ one video generation** unless your model supports multi-shot.
- Use patterns when needed (Character Consistency, Frame Chaining, Multi-Scene Content).

### Planning Step 4: Map Nodes + Data Flow (NODES)

This is where you make the workflow executable.

**Minimum (recommended):** a wiring diagram in text. For each step, list nodes in order and capture:
- Node type: **generation** (prompt required) vs **supporting** (no prompt)
- Inputs → outputs (what each node consumes/produces)

**Add briefs only when needed (to avoid rework):**
- For each **generation node**, add a short **prompt brief**:
  - `Modality | Intent | Inputs/Refs | Constraints | Output requirement`
- For each **supporting node**, add a short **operation brief**:
  - `Operation/Tool | Inputs | Outputs | Key settings`

### Planning Step 5: Plan Continuity + Integration

Decide how steps connect and how you’ll assemble the final output:
- **Frame chaining** vs **reference images** vs **editing plan** (cuts/transitions)
- Any required post steps (stitching, upscaling, audio sync)

Quick check: every node has clear inputs/outputs, and your continuity approach is explicit.

---

## 6. Next Steps

Once you've planned your workflow, it's time to generate prompts for each generation node.

### System Hierarchy

```
GOAL → Final Output
  ↓
WORKFLOW → Node graph (modalities + supporting ops)
  ↓
FOR EACH WORKFLOW STEP:
  NODES → supporting nodes + generation nodes
    ↓
  FOR EACH GENERATION NODE (prompt required):
    MODALITY → t2t? t2i? i2v? t2v?
      ↓
    PROMPTING APPROACH
      ├─ Focus (what to describe)
      ├─ Phrasing Style (descriptive or narrative)
      └─ Formula (structure)
        ↓
      BLOCKS → Which components?
        ↓
      DETAIL LEVEL → How much depth?
        ↓
      FINAL PROMPT → Natural text
        ↓
    MODEL → Execute
      ↓
    OUTPUT → Next node input
  ↓
ITERATION → Test & refine
  ↓
FINAL → Combine outputs
```

### Key Relationships

- **Modalities** define capabilities
- **Workflows** chain nodes (modalities + supporting ops)
- **Prompting Approach** has three components: Focus, Phrasing Style, Formula
- **Formulas** systematize prompts via blocks
- **Blocks** are reusable components
- **Detail levels** control prompt depth
- **Testing** refines everything

### Guides

**For prompt generation:**
- Use the **Prompt Generation Reference** guide
- For each generation node, you'll need: modality + intent

**For detailed formula and block methodology:**
- Reference the **Formula Framework** companion document

---

**End of Workflow Architecture Guide v1.0**
