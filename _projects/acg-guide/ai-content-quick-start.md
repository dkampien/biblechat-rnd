# AI Content Generation: Quick Start Guide

**Version**: 1.0
**Date**: 2025-12-30

---

## Overview

This practical guide shows you how to plan and execute AI content generation projects from start to finish. Perfect for creating content workflows and templates.

**Workflow-first approach:** Start with your goal, design the workflow, create prompts, execute.

**For deep technical details:** See [Prompt Generation Guide](archive/prompt-generation-guide-v5.5.md) (Comprehensive)

---

## The 4-Step Workflow Planning Process

### Step 1: Establish Brief & Outputs

**Define what you're creating:**
- **Goal:** What's the end result? (30-second video, image series, character animation)
- **Inputs:** What do you have? (story brief, concept, character description)
- **Outputs:** What formats do you need? (video, images, thumbnails)
- **Constraints:** Duration limits, style requirements, consistency needs

**Example:**
```
Goal: 30-second video of bee character helping mom get child to take vitamins
Inputs: Story concept, bee character design notes
Outputs: 6 scenes × 5 seconds each, stitched together
Constraints: Consistent bee character, child-friendly style
```

---

### Step 2: Design Workflow (Modalities & Steps)

**Choose AI capabilities and chain them:**

**Common patterns:**
- **Single modality:** text-to-video (simplest, less control)
- **Controlled video:** text-to-image → image-to-video (more control over starting frame)
- **Character consistency:** t2i (character) → i2i (variations) → t2i (scenes with refs) → i2v (animations)
- **Multi-scene:** Generate scenes → Frame chaining for continuity → Stitch

**Example workflow breakdown:**
```
Bee Character Project:
1. Scene planning: Break 30-second video into 6 scenes
2. For each scene:
   - Scene description (text) → image generation (t2i)
   - Static image → animation (i2v)
3. Stitch 6 videos together
```

**Key decision:** More steps = more control, but more work

---

### Step 3: Create Prompts for Each Step

**Critical insight: Different modalities need different prompts**

| Modality | What to Describe | Example |
|----------|------------------|---------|
| text-to-image (t2i) | What exists (visuals) | "Cartoon bee character in kitchen, bright colors, child-friendly style" |
| image-to-video (i2v) | What changes (motion only) | "Bee flies from left to right, wings buzzing, smooth motion" |
| text-to-video (t2v) | Both visuals + motion | "Cartoon bee flies through kitchen, bright colors, smooth motion" |

**For detailed prompting technique:** See [Prompt Generation Guide](archive/prompt-generation-guide-v5.5.md)
**For formula/block structure:** See [Prompt Formula Framework](archive/prompt-formula-framework-v2.md)

---

### Step 4: Choose Models & Execute

**Select appropriate models:**
- Consider: quality, speed, cost, capabilities
- Platform examples: Replicate, RunwayML, Stability AI
- Test and iterate based on results

**Execution tips:**
- Test prompts before full run
- Save successful prompts for reuse
- Iterate on quality before scaling

---

## Common Workflow Patterns

### Pattern 1: Controlled Video (2 steps)

**Use when:** You want precise control over the starting frame

**Workflow:**
```
text-to-image → image-to-video
```

**Why:** Separating image generation from animation gives you control. You can perfect the image before animating it.

**Examples:**
- Product showcase (generate product shot, then add motion)
- Character portrait animation (create portrait, then animate expression)
- Scene setup (establish setting, then add camera movement)

---

### Pattern 2: Character Consistency (multi-step)

**Use when:** You need the same character across multiple scenes

**Workflow:**
```
1. Create character (t2i) → Character portrait
2. Generate variations (i2i) → Reference library (angles, expressions, poses)
3. Generate scenes (t2i + character refs) → Scene images with consistent character
4. Animate scenes (i2v) → Final videos
```

**Why:** Creating a reference library first ensures character looks consistent across all scenes.

**Example:** 30-second video with character appearing in multiple scenes

---

### Pattern 3: Multi-Scene Content

**Use when:** Content is longer than single generation duration limits (usually 5-10 seconds)

**Workflow:**
```
1. Plan scenes → Break content into 5-10 second segments
2. Generate scenes → Each scene separately
3. Frame chaining → Use last frame of Scene N as first frame of Scene N+1
4. Stitch → Combine into final video
```

**Frame Chaining Technique:**
```
Scene 1: Generate video (t2v or i2v) → Extract last frame
Scene 2: Use last frame from Scene 1 as input (i2v) → Extract last frame
Scene 3: Use last frame from Scene 2 as input (i2v) → Continue...
```

**Why:** Frame chaining maintains visual continuity between scenes (lighting, setting, character appearance)

---

## Complete Examples

### Example 1: Bee Character Project

**Brief:** Bee character helps mom get child to take vitamins

**Workflow Design:**
1. Break into 6 scenes (each 5 seconds)
2. For each scene: scene text → t2i → i2v

**Scene Breakdown:**
```
Scene 1: "Bee enters kitchen where mom and child are"
Scene 2: "Bee notices child refusing vitamins"
Scene 3: "Bee demonstrates taking vitamins is fun"
Scene 4: "Child becomes interested"
Scene 5: "Child takes vitamins happily"
Scene 6: "Bee and child celebrate together"
```

**Execution:**
- Write scene descriptions (planning)
- For Scene 1:
  - t2i prompt: "Cartoon bee character flying into bright kitchen, mother and child at table, warm lighting, child-friendly illustration style"
  - Generate image
  - i2v prompt: "Bee flies from left side into center of frame, wings buzzing, smooth gentle motion"
  - Generate 5-second video
- Repeat for scenes 2-6
- Stitch 6 videos together

**Result:** 30-second video with consistent bee character and clear story

---

### Example 2: Italian Model at Gym

**Brief:** Create video of Italian model going to the gym

**Workflow Design:**
1. Create character spec (text description)
2. Generate character portrait (t2i)
3. Create reference library (i2i variations)
4. Plan gym scenes (6 scenes)
5. Generate scene images with character refs (t2i)
6. Animate each scene (i2v)

**Character Spec:**
```
Name: Valentina
Age: 27
Appearance: Athletic build, long dark hair, Mediterranean features
Style: Fitness wear, athletic aesthetic
```

**Workflow Execution:**
- t2i: Generate Valentina portrait using character spec
- i2i: Generate reference angles (front, 3/4, side) and expressions
- Plan scenes: [arriving at gym, stretching, treadmill, weights, water break, leaving]
- For each scene:
  - t2i with character refs: Scene image with consistent Valentina
  - i2v: Animate the scene (exercise motion, camera movement)
- Stitch together

**Result:** 30-second video with consistent character across all scenes

---

## Quick Reference

### When to Use Which Modality

- **text-to-image (t2i):** Static images, character creation, scene setup
- **image-to-video (i2v):** Animate existing images, controlled motion
- **text-to-video (t2v):** Quick videos, less control needs
- **image-to-image (i2i):** Variations, style transfer, reference creation

### Common Workflow Decisions

**Want more control?**
→ Multi-step workflow (t2i → i2v gives more control than t2v)

**Want quick results?**
→ Single-step (t2v for simple videos)

**Need consistent character?**
→ Create character references first (t2i → i2i → use refs in all scenes)

**Content longer than 10 seconds?**
→ Multi-scene with frame chaining

**Need specific starting frame?**
→ Generate image first (t2i), then animate (i2v)

---

## Next Steps

**For detailed prompting technique:**
→ [Prompt Generation Guide (Comprehensive)](archive/prompt-generation-guide-v5.5.md)

**For formula/block structure:**
→ [Prompt Formula Framework](archive/prompt-formula-framework-v2.md)

**For creating cloops templates:**
→ [Template Authoring Guide](template-authoring-guide.md)

---

**End of Quick Start Guide v1.0**
