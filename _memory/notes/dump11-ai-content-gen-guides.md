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

----


CHARACTER CONSISTENCY "TECHNIQUE"
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


NEXT
- Revoew the quick start guide and delete
[x] Review workflow guide
    [x] Re-write workflow planning process
- Review prompt gen guide v6
    - Review modalities prompting
- Review the system prompt for custom gpt (the glue doc)

----





