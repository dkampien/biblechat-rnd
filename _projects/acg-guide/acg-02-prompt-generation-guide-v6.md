# AI Content Generation: Prompt Generation Reference

**Version**: 6.0
**Date**: 2025-12-31

---

## 1. Introduction

This guide teaches you how to create effective prompts for AI content generation models.

**Use this guide when:**
- You know your modality (e.g., text-to-image, image-to-video)
- You know your intent (what content to create)
- You need to generate the actual prompt

**Use Workflow Architecture Guide when:**
- You're planning multi-step projects
- You need to choose which modalities to use

**Flow:** Plan workflow (Workflow guide) → Generate prompts for each generation node (this guide)

**Handoff note:** In workflows, prompts are written per generation node (modality execution). Supporting nodes (utilities/editing/tools) do not require prompts. This guide assumes you have a prompt brief: modality + intent + inputs/refs + constraints.

---

## 2. How Modalities Require Different Prompts

**Critical insight:** Different modalities need fundamentally different prompts.

**Note:** This section uses representative modalities. Apply the same focus logic to other modalities (i2i, v2v, edits, lipsync, etc.). See the Workflow Architecture Guide for the full list.

### Text-to-Image

**What to describe:** Visuals only (what exists)

**Example:**
```
Portrait of young adult female, striking green eyes, long auburn hair,
neutral studio backdrop, soft diffused lighting, photorealistic
```

### Image-to-Video

**What to describe:** Motion only (what happens)

**Important:** Do NOT describe visuals - the image already has them.

**Example:**
```
Person slowly turns head toward camera, subtle smile forming,
slight camera push-in, smooth natural motion
```

### Text-to-Video

**What to describe:** Visuals AND motion (both)

**Example:**
```
Young woman with auburn hair in cozy living room, warm lighting,
looks up from book, smiles at camera, slow push-in, 5 seconds,
photorealistic
```

### Summary

| Modality | Visuals? | Motion? | Why? |
|----------|----------|---------|------|
| text-to-image | ✅ | ❌ | Static image |
| image-to-video | ❌ | ✅ | Image has visuals |
| text-to-video | ✅ | ✅ | Creating everything |

---

## 3. The Prompting Approach

For each modality, your prompting approach consists of three components:

### 1. FOCUS - What to Describe

**Determined by modality:**
- text-to-image: Describe what exists (visuals)
- image-to-video: Describe what happens (motion only)
- text-to-video: Describe both (visuals + motion)

### 2. PHRASING STYLE - How to write block values

**Descriptive:** Lists what exists (compact, direct)
- Example: "A man cleaning a car engine, wiping sweat from his brow, exhausted expression"
- Within descriptive, two writing styles exist:
  - **Direct/Compact**: "blue sports car", "person in blood-splattered jacket"
  - **Verbose/Predicative**: "the car is blue and sporty", "the person has blood streaming"
  - Note: Direct style is generally more efficient; worth testing which works better for your model

**Narrative:** Tells what happens (sequential, story-like)
- Example: "A man leans over the hood, wipes his brow, then looks at the camera and says 'This is hard work'"

**Note:** Both phrasing styles work with block-based formulas - the difference is how you write the block values, not the structure itself.

### 3. FORMULA - Which Structure to Use

- Block structure (which blocks)
- Block order (arrangement)
- Block level of detail (depth)

> See `prompt-formula-framework-v3.md` for detailed methodology on formulas and blocks.

### The Flow

```
Modality → Focus (what to describe) → Phrasing Style (how to write)
→ Formula (structure) → Blocks → Detail Level → Final Prompt
```

---

## 4. Best Practices

### Language Evolution

**Modern models use natural, descriptive language:**
- Old: `woman, long hair, smiling, beach, sunset, 4k`
- New: `Woman with long hair smiles warmly while walking on beach at sunset`

### Block Order Matters

- AI models often weight earlier elements more heavily
- Test different orderings
- Platform-specific variations exist
- Prioritize important elements early

### Natural Flow

Prompts should read coherently:
```
Good: Young woman sits in cozy room, warm light streaming through
      window, reading book, looks up with gentle smile

Poor: Woman, book, smile, young, cozy, room, window, warm, light
```

### Model-Specific Considerations

Different platforms and models may have specific preferences:

**Negative Prompts:**
Some models (e.g., Veo 3) support a separate `negativePrompt` parameter:
```
Prompt: "Generate a short animation of a large oak tree with leaves blowing in wind"
Negative Prompt: "urban background, man-made structures, dark, stormy atmosphere"
```
Note: Describe what to avoid, not instructive language like "no" or "don't"

**Phrasing Preferences:**
- **Use positive phrasing** - Describe what should happen, not what to avoid
  - ❌ "No camera movement. The camera doesn't move."
  - ✅ "Locked camera. The camera remains still."

**Language Style:**
- **Avoid conversational language** - Skip greetings, pleasantries, questions
  - ❌ "Can you please add a dog to the scene?"
  - ✅ "A dog runs into the scene from off-camera"

- **Avoid command-based prompts** - Describe instead of instructing
  - ❌ "Add more lighting" or "Make it brighter"
  - ✅ "Bright natural sunlight fills the room"

**Prompt Complexity:**
- **Keep prompts direct and simple** - Avoid overly conceptual language
  - ❌ "The subject embodies the essence of joyful greeting"
  - ✅ "The woman smiles and waves"

- **Single scene focus** - Consider duration limits (5-10s = one scene)
  - ❌ "Cat transforms into dragon while jumping through forest that changes seasons..."
  - ✅ "Cat transforms into dragon while running through forest"

**Always consult:**
- Platform documentation
- Model-specific prompting guides
- Community best practices
- Recent updates and changes

### Model Prompt Adherence

Different models have varying levels of **prompt adherence** - how accurately they follow instructions.

**Key points:**
- Well-crafted prompts may not work equally across all models
- Some models excel at complex instructions, others work better with simplicity
- Certain elements (specific angles, subtle emotions, precise positioning) are harder to follow
- Prompt adherence varies between models and versions

**Testing approach:**
- Test prompts across different models to compare results
- Identify which elements the model follows vs. ignores
- Adjust strategy based on model strengths and limitations
- Sometimes simplification improves adherence more than adding detail

**Bottom line:** A "perfect" prompt for one model may fail on another. Testing is essential.

---

## 5. Applying This Framework

### What You Need

To generate a prompt, you need two things:
1. **Modality** - How to generate (text-to-image, image-to-video, etc.)
2. **Intent** - What content to create

### Generation Process

**Step 1: Identify modality and intent**
- If user provides both → proceed
- If something is missing → ask for it

**Understanding Intent:**
Intent describes what the modality generates:
- If modality has input (image, video): describe what changes/happens
- If modality generates from scratch: describe what should exist

**Step 2: Choose prompting approach**
- Refer to Section 2 for modality-specific focus (visuals, motion, or both)
- Decide on phrasing style (descriptive or narrative)

**Step 3: Select appropriate formula**
- Use block structure suited for the modality
- Reference Formula Framework for detailed block methodology

**Step 4: Fill blocks based on intent**
- Populate blocks with content from user's intent
- Apply natural language flow
- Prioritize important elements early

**Step 5: Test and refine**
- Generate and evaluate output
- Adjust based on model adherence and results
- Sometimes simplification works better than more detail

**Step 6: Document**
- Capture what works for future use
- Use output formats from Formula Framework

---

## 6. Next Steps

**For detailed formula and block methodology:**
- Reference **Formula Framework** (`prompt-formula-framework-v3.md`)
- Covers block structure, hierarchies, output formats, and LLM usage rules

**For workflow planning:**
- Use **Workflow Architecture Guide** (`prompt-workflow-gen-guide-v1.md`)
- Plan multi-step projects and choose modalities

**Process:**
- Plan workflow → Generate prompts (this guide) → Execute → Refine

---

**End of Prompt Generation Reference v6.0**
