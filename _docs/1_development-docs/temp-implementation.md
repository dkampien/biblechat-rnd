# Implementation Plan - d2c Template POC

**Date**: October 23, 2025
**Status**: Draft - Ready for next conversation

---

## Phase 1: Update Type Definitions (30 min)
**Files**: `src/types/script.types.ts`

**Changes:**
- Update `VideoScript` interface:
  - Rename `overallScript` → `videoScript`
  - Ensure `scenes[].content` → `scenes[].description` (or keep as is and map)
- Add template variable types (for future: `variety_instruction`, `dialogue_instruction`)

**Notes:**
- Check if field rename breaks anything downstream
- May need to update state management types too

---

## Phase 2: Update Template Definition (1 hour)
**File**: `src/config/templates.ts`

**Changes for d2c template:**

### systemPromptCall1 (from playground testing):
```
{{ variety_instruction }}

You are creating a comfort video. A person speaks directly to camera in a warm home setting.

Generate TWO fields:

1. videoScript - Describe Scene 1 visuals in simple terms:
   - The person (age, clothing, expression)
   - The setting (home basics)
   - Body language and mood
   Keep it natural and simple. No technical camera/lighting jargon.

2. voiceScript - 50-60 words of dialogue with this structure:
   - First ~20 words: Acknowledge their specific struggle
   - Next ~20 words: Reassure them they're not alone, it's okay to feel this way
   - Final ~20 words: Gently invite them to try BibleChat for support

Tone: Warm, conversational, empathetic. Speak directly to "you."
```

### systemPromptCall2 (from playground testing):
```
{{ dialogue_instruction }}

You are optimizing visual descriptions for Veo 3.1 video generation.

Input:
- videoScript (Scene 1 baseline description)
- voiceScript (50-60 words continuous dialogue)

Generate 3 scene prompts following this strategy:

Scene 1 - Full descriptive prompt:
- Use videoScript as foundation
- Simplify: Remove overly specific props (no "wedding photo" or "spreadsheet on laptop")
- Keep: Person, setting type, mood, expression, body language, lighting quality
- Add: "actively speaking to camera"
- If including dialogue: Add first ~20 words from voiceScript in format 'saying: "[dialogue]"'
- Format for Veo: Natural language, 40-80 words

Scene 2 - Minimal continuation:
- Do NOT describe setting (image parameter handles this)
- Only: Expression/emotion shift from Scene 1
- If including dialogue: Add middle ~20 words from voiceScript
- Format: "Person continues speaking with [expression change], saying: '[dialogue]'"
- 10-30 words maximum

Scene 3 - Minimal continuation:
- Same as Scene 2 rules
- If including dialogue: Add final ~20 words from voiceScript
- Focus on final emotional shift

Remember: Scenes 2-3 use frame chaining - the image parameter provides visual context, so verbose descriptions cause conflicts.
```

**Notes:**
- For POC: Hardcode `variety_instruction` and `dialogue_instruction` values
- Future: Make these configurable via template variables

---

## Phase 3: Update Script Generator (2 hours)
**File**: `src/lib/script-generator.ts`

**Changes:**

### CALL 1 Updates:
- Update Zod schema (lines ~113-119):
  ```typescript
  const ContentSchema = z.object({
    videoScript: z.string().min(50),  // renamed from overallScript
    voiceScript: z.string().min(40).max(100),  // NEW FIELD
    scenes: z.array(z.object({
      sceneNumber: z.number().int().min(1).max(3),
      description: z.string().min(10)  // or keep as 'content'
    })).length(3)
  });
  ```

### CALL 2 Updates:
- Update user prompt to include both videoScript and voiceScript:
  ```typescript
  const userPrompt = `videoScript: ${contentResponse.videoScript}

  voiceScript: ${contentResponse.voiceScript}

  Generate 3 Veo-optimized scene prompts following the strategy above.`;
  ```

**Notes:**
- Template variables: Start with hardcoded strings, extract to config later
- Consider if scenes[].description needs to exist in CALL 1 output or can be skipped

---

## Phase 4: Update Video Generator (1 hour)
**File**: `src/lib/video-generator.ts`

**Changes:**
- Add `negative_prompt` parameter (lines ~92-104):
  ```typescript
  const input: any = {
    prompt: scene.prompt,
    aspect_ratio: this.config.videoGeneration.aspectRatio,
    duration: this.config.videoGeneration.duration,
    negative_prompt: "background music"  // NEW
  };
  ```

- Ensure `generate_audio: true` for POC (or check config)

**Notes:**
- Verify model is `google-deepmind/veo-3.1` (not veo-3)
- Check if negative_prompt needs to be configurable

---

## Phase 5: Test & Validate (2 hours)

**Step 1: Dry-run test**
```bash
npm run generate -- --dry-run --limit 1
```
- Verify output structure in `output/dry-run/`
- Check fields: videoScript, voiceScript, scenes[].prompt
- Validate prompt format (Scene 1 full, 2-3 minimal)

**Step 2: Full generation test**
```bash
npm run generate -- --limit 1
```
- Generate 1 complete video (3 scenes)
- Check for background music (should be absent)
- Verify visual quality
- Check voice changes between scenes (acceptable for POC)

**Step 3: Validate outputs**
- [ ] videoScript is Scene 1 visual baseline
- [ ] voiceScript is 50-60 words
- [ ] Scene 1 prompt is detailed
- [ ] Scenes 2-3 prompts are minimal
- [ ] No background music in videos
- [ ] Dialogue matches voiceScript split

**Step 4: Check costs and timing**
- Cost per video: ~$4.80 (3 clips × $1.60)
- Time per video: ~3.5 minutes (3 × 70s)

---

## Phase 6: Frame Chaining (Optional - 3 hours)
**If time permits**

**File**: `src/lib/video-generator.ts`

**Implementation:**
1. Add frame extraction after each scene generation:
   ```typescript
   // Extract last frame
   await execCommand(`ffmpeg -i ${scenePath} -vf "select='eq(n,191)'" -frames:v 1 ${lastFramePath}`);
   ```

2. Pass `image` parameter to subsequent scenes:
   ```typescript
   if (scene.sceneNumber > 1) {
     input.image = previousSceneLastFrame;
   }
   ```

3. Test visual continuity with/without frame chaining

**Notes:**
- Requires ffmpeg integration
- Need to manage frame file paths
- `last_frame` parameter testing deferred

---

## Estimated Total: 6-9 hours

**Critical path**: Phases 1-5 (minimum viable POC)
**Optional**: Phase 6 (frame chaining enhancement)

**Priority order:**
1. Phase 2 (Templates) - Core of the solution
2. Phase 3 (Script Generator) - Enables template execution
3. Phase 4 (Video Generator) - Adds negative_prompt
4. Phase 1 (Types) - Clean up types to match
5. Phase 5 (Testing) - Validate everything works
6. Phase 6 (Frame Chaining) - Enhancement

---

## Key References

**Validated prompts from playground:**
- CALL 1: See Phase 2 → systemPromptCall1
- CALL 2: See Phase 2 → systemPromptCall2

**Testing results:**
- See `_docs/2_reference-docs/workflow-problems-and-solutions-2.md`
- Tests 6-12 validate the approach

**Template design:**
- See `_docs/2_reference-docs/template-design-full.md`

**Current codebase:**
- `src/config/templates.ts` - Current template definitions
- `src/lib/script-generator.ts` - LLM call logic
- `src/lib/video-generator.ts` - Veo API integration

---

## Notes for Next Session

**Context to review:**
1. This implementation plan
2. Template design docs (template-design-full.md)
3. Workflow doc updates (workflow-problems-and-solutions-2.md)
4. Playground-validated prompts (saved in this doc)

**First step recommendation:**
Start with Phase 2 (updating templates) since that's the core change. Test in dry-run mode immediately to catch any issues early.

**Question to consider:**
Should we keep `scenes[].description` field from CALL 1, or eliminate it entirely since videoScript serves as the baseline? Current implementation has it, but new design might not need it.
