## 7. Complete Workflow Examples

### Example 1: Controlled Video (Two-Step)

**Goal:** 8-second video with visual control

**Workflow:**
```
text-to-image → image-to-video
```

**Why this workflow:**
- Step 1 (text-to-image): Create exact visual you want
- Step 2 (image-to-video): Animate with controlled motion
- Control over both visuals and motion separately

**Step breakdown:**
1. **text-to-image** - Generate product image with specific composition, lighting, style
2. **image-to-video** - Animate the image with rotation and camera movement

**Result:** 8-second controlled video

---

### Example 2: Character Consistency (30 seconds)

**Goal:** AI influencer gym video with consistent character across 6 scenes

**Workflow:**
```
1. Character persona (LLM)
2. Character appearance (text-to-image - portrait)
3. Reference library (image-to-image - variations)
4. Activity breakdown (LLM → 6 scenes)
5. Scene images (text-to-image + character refs)
6. Scene animations (image-to-video × 6)
7. Stitch videos (editing)
```

**Why this workflow:**
- Steps 1-3: Build character foundation for consistency
- Step 4: Plan content structure
- Steps 5-6: Generate consistent scenes using character references
- Step 7: Combine into final video

**Step breakdown:**
1. **LLM** - Define character persona, background, personality
2. **text-to-image** - Create character portrait
3. **image-to-image** - Generate reference angles, expressions, poses
4. **LLM** - Break activity into 6 scenes
5. **text-to-image** - Create scene images using character references (× 6)
6. **image-to-video** - Animate each scene (× 6)
7. **Editing** - Stitch 6 clips together

**Result:** 30-second video (6 clips × 5 seconds) with consistent character

**Note:** For prompt details and formulas, see Prompt Generation Reference

---

--------


1. Craft character persona (LLM)
2. Craft character main reference / appearence
3. Generate character reference collection / reference library
4. Establish overall content idea and break down to scenes (LLM 6 scenes)
5. Transform scene descriptions to text to image prompts 
6. Generate images from the t2i prompts (all scenes)
7. Generate video scene from previous image output (all scenes)
8. Stich all video scenes for the final video (in davinci)

Prompts needed
1. character persona (text output)
2. character appearence / main reference (image output)
3. character consistency for reference library (image output)
4. scene breakdown (text output)
5. t2i - all scenes (image output)
6. i2v - all scenes (video output)

----


- Remove sections 7 with examples. Add back details in section 4?
- Workflow techniques conflict? Need to define techniques better?
- In the 5.5 what are the workflow components? vs our conclusion?
- In 5.5 we have some stuff I don't know where they fit, or what to do with them. They seem important but help me place them and rephrase them accordingly if needede. 
    - Workflow hierarchy line 202
    - System hierarchy on line 670 and also key relationships that seem to be similar to our workflow components
    - Applying this framework line 712. Single generation vs multi step workflows. Haven't we talked about these earlier? I know intent is very importat but its about workflows or prompting?

-----

Techniques
- Relighting
- Intpainting
- Lipsync
- Upscaling
- Product placement
- Lora training

- Frame chaining
- Multi-scene content
- Character consistentcy

----

possible next steps
1. Continue reviewing workflow guide
    - workflow planning process
2. Review prompt generation guide v6
3. Create the glue doc - how the 3 guides work togehter
4. Deal with the quick start guide. Delete.




 **Workflow = Chaining modalities to achieve a final output**

Think of workflows like ComfyUI node graphs - each step uses a specific modality, feeding outputs to the next step.

Workflows are built by combining reusable techniques to achieve larger outcomes.

### Workflow Components

**Workflow**
- The complete pipeline from start to final output (e.g., "30-second character video")
- Can be simple (one step) or complex (multiple techniques)
- Workflows chain techniques together: each technique's output → next technique's input


----


  1. Understanding AI Models
  2. Modalities: Model Capabilities
  3. AI Generation Workflows
  4. Prompts & Modalities
  5. Formulas & Blocks
  6. Detail Levels
  7. Prompting Best Practices
  8. Complete Workflow Examples
  - System Hierarchy
  - Applying This Framework


  ⏺ Workflow Architecture Guide

  1. Introduction
  2. Understanding Modalities (Capability Reference)
  3. Single vs Multi-Step Workflows
  4. Workflow Planning Process
  5. Continuity Techniques
  6. Multi-Scene Content Planning
  7. Common Workflow Patterns
  8. Complete Workflow Examples
  9. Next Steps

  ---
  Prompt Generation Reference

  1. Introduction
  2. Understanding AI Models
  3. How Modalities Require Different Prompts
  4. The Prompting Approach (Focus, Phrasing, Formula)
  5. Detail Levels
  6. Best Practices
  7. Applying This Framework
  8. Modality-Specific Examples
  9. Next Steps
  