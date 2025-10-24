# Cycle 4: Implementation Plan

**Date**: October 24, 2025
**Status**: Ready for implementation

---

## Overview

- **Objective:** Implement redesigned template framework with Veo 3.1 frame chaining, extract all problems from dataset, and update to gpt-5-mini model for POC completion.

- **Key Risks / Assumptions:**
  - gpt-5-mini API assumed compatible with current OpenAI integration
  - Frame extraction via ffmpeg assumed functional (not tested yet)
  - Schema changes may require state file reset (clean start)
  - All problems extraction may reveal data quality issues in CSV

- **Related Docs:**
  - `@_docs/1_development-docs/cycle-4/0-exploration.md` - Discussion and decisions
  - `@_docs/1_development-docs/cycle-4/1-requirements.md` - Formal specifications
  - `@_docs/1_development-docs/temp-implementation.md` - Tested system prompts
  - `@_docs/2_reference-docs/template-design-full.md` - Template framework
  - `@_docs/2_reference-docs/workflow-problems-and-solutions-2.md` - Technical decisions

---

## Completion Status

- **Phase 1:** Schema & Types — ❌ Not started
- **Phase 2:** External Docs & Model Updates — ❌ Not started
- **Phase 3:** Template System Prompts — ❌ Not started
- **Phase 4:** Script Generator Updates — ❌ Not started
- **Phase 5:** Data Processor Updates — ❌ Not started
- **Phase 6:** Video Generation (Veo 3.1 + Frame Chaining) — ❌ Not started
- **Phase 7:** Output Assemblers — ❌ Not started
- **Phase 8:** Integration & Validation — ❌ Not started

---

## Phase 1: Schema & Types Updates

Foundation phase - all other phases depend on correct type definitions.

### Step 1.1: Update VideoScript interface `[ ]`
- **Priority:** Critical
- **Task:** Update `VideoScript` interface to replace `overallScript` with `videoScript`, add `voiceScript` field, remove deprecated scene fields.
- **Files:**
  - `src/types/script.types.ts`
- **Step Dependencies:** None
- **User Instructions / Validation:**
  ```bash
  npm run build
  # Should compile without errors
  ```
- **Implementation Notes:**
  ```typescript
  interface VideoScript {
    id: string;
    category: string;
    template: string;
    timestamp: string;
    videoScript: string;     // renamed from overallScript
    voiceScript: string;     // NEW FIELD
    scenes: Scene[];
  }

  interface Scene {
    sceneNumber: number;
    prompt: string;
    // REMOVED: content, description
  }
  ```

### Step 1.2: Create Manifest types `[ ]`
- **Priority:** Critical
- **Task:** Create new `output.types.ts` file defining flexible manifest structure with universal core and template-specific content.
- **Files:**
  - `src/types/output.types.ts` (create new)
- **Step Dependencies:** Step 1.1
- **User Instructions / Validation:**
  ```bash
  npm run build
  # Check no type errors
  ```
- **Implementation Notes:**
  ```typescript
  interface Manifest {
    videoId: string;
    problemCategory: string;
    contentTemplate: string;
    timestamp: string;
    userProblem: string;
    content: D2CManifestContent;
    scenes: ManifestScene[];
    finalVideoPath: string;
  }

  interface D2CManifestContent {
    videoScript: string;
    voiceScript: string;
  }
  ```

### Step 1.3: Update Prediction types for Veo 3.1 `[ ]`
- **Priority:** High
- **Task:** Add `image` and `last_frame` optional parameters to Veo input type, add `negative_prompt`.
- **Files:**
  - `src/types/prediction.types.ts`
- **Step Dependencies:** None
- **User Instructions / Validation:**
  ```bash
  npm run build
  # Check video-generator.ts compiles
  ```
- **Implementation Notes:**
  ```typescript
  interface VeoInput {
    prompt: string;
    duration: number;
    aspect_ratio: string;
    generate_audio: boolean;
    resolution?: string;
    negative_prompt?: string;  // NEW
    image?: string;            // NEW
    last_frame?: string;       // NEW (not using yet)
    seed?: number;
  }
  ```

---

## Phase 2: External Docs & Model Updates

Research and configure new models before implementing logic changes.

### Step 2.1: Fetch gpt-5-mini documentation `[ ]`
- **Priority:** Critical
- **Task:** Use context7 MCP server to fetch OpenAI Responses API documentation for gpt-5-mini. Document API changes, breaking changes, and pricing.
- **Files:**
  - Create notes file or update exploration.md with findings
- **Step Dependencies:** None
- **User Instructions / Validation:**
  - Use context7 MCP to query OpenAI docs
  - Focus on Responses API (not Chat Completions)
  - Document: endpoint format, authentication, response structure, pricing
- **Implementation Notes:**
  - Look for breaking changes from gpt-4o-mini
  - Verify structured output (Zod) compatibility
  - Note any new parameters or capabilities

### Step 2.2: Update config for gpt-5-mini `[ ]`
- **Priority:** Critical
- **Task:** Update model string in configuration to use gpt-5-mini.
- **Files:**
  - `config.json` or `src/config/config.ts`
- **Step Dependencies:** Step 2.1 (verify model name)
- **User Instructions / Validation:**
  ```bash
  # Check config loads correctly
  npm run generate -- --dry-run --limit 1
  ```
- **Implementation Notes:**
  - Update: `"model": "gpt-5-mini"`
  - Verify API client uses Responses API endpoint
  - May need to update script-generator.ts if API interface changed

### Step 2.3: Update config for Veo 3.1 `[ ]`
- **Priority:** High
- **Task:** Update Veo model string to `google-deepmind/veo-3.1` and add `negative_prompt` to config.
- **Files:**
  - `config.json`
- **Step Dependencies:** None
- **User Instructions / Validation:**
  ```bash
  grep -r "veo-3.1" config.json
  grep -r "negativePrompt" config.json
  ```
- **Implementation Notes:**
  ```json
  {
    "videoGeneration": {
      "model": "google-deepmind/veo-3.1",
      "negativePrompt": "background music"
    }
  }
  ```

### Step 2.4: Add new output directories to config `[ ]`
- **Priority:** Medium
- **Task:** Add `videosDir` and `manifestsDir` paths to configuration.
- **Files:**
  - `config.json`
- **Step Dependencies:** None
- **User Instructions / Validation:**
  ```bash
  # Verify paths added
  cat config.json | grep -A 10 "paths"
  ```
- **Implementation Notes:**
  ```json
  {
    "paths": {
      "videosDir": "./output/videos",
      "manifestsDir": "./output/manifests"
    }
  }
  ```

---

## Phase 3: Template System Prompts

Update d2c template with tested prompts from temp-implementation.md.

### Step 3.1: Update d2c systemPromptCall1 `[ ]`
- **Priority:** Critical
- **Task:** Replace systemPromptCall1 with tested version that generates `videoScript` + `voiceScript`.
- **Files:**
  - `src/config/templates.ts`
- **Step Dependencies:** Phase 1 complete (types updated)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Check output has videoScript and voiceScript fields
  ```
- **Implementation Notes:**
  - Copy prompt from `temp-implementation.md` lines 28-48
  - Hardcode template variables for POC (variety_instruction can be omitted or simple)
  - Ensure prompt generates exactly: videoScript, voiceScript

### Step 3.2: Update d2c systemPromptCall2 `[ ]`
- **Priority:** Critical
- **Task:** Replace systemPromptCall2 with tested version implementing Scene 1 full / Scenes 2-3 minimal strategy.
- **Files:**
  - `src/config/templates.ts`
- **Step Dependencies:** Step 3.1
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Check Scene 1 prompt is detailed (40-80 words)
  # Check Scenes 2-3 prompts are minimal (10-30 words)
  ```
- **Implementation Notes:**
  - Copy prompt from `temp-implementation.md` lines 50-83
  - Ensures Scene 1 has full description, Scenes 2-3 minimal
  - Includes dialogue in all scene prompts

### Step 3.3: Update promptRules and sceneStructure `[ ]`
- **Priority:** Low
- **Task:** Update template metadata to reflect new prompt strategy.
- **Files:**
  - `src/config/templates.ts`
- **Step Dependencies:** Steps 3.1, 3.2
- **User Instructions / Validation:**
  - Code review - check metadata matches implementation
- **Implementation Notes:**
  - Update `promptRules` to mention simplified scenes 2-3
  - `sceneStructure` can stay as-is (general guidance)

---

## Phase 4: Script Generator Updates

Update LLM call logic to generate and validate new schema.

### Step 4.1: Update CALL 1 Zod schema `[ ]`
- **Priority:** Critical
- **Task:** Update Zod schema for CALL 1 to expect `videoScript` and `voiceScript` instead of `overallScript`.
- **Files:**
  - `src/lib/script-generator.ts`
- **Step Dependencies:** Phase 1 complete, Step 3.1 complete
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Should parse successfully, no validation errors
  ```
- **Implementation Notes:**
  ```typescript
  const Call1Schema = z.object({
    videoScript: z.string().min(50),
    voiceScript: z.string().min(40).max(100),
  });
  ```
  - Remove `overallScript` from schema
  - Remove `scenes[].content` validation if present

### Step 4.2: Update CALL 2 user prompt `[ ]`
- **Priority:** Critical
- **Task:** Pass both `videoScript` and `voiceScript` to CALL 2 for prompt generation.
- **Files:**
  - `src/lib/script-generator.ts`
- **Step Dependencies:** Step 4.1
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Check generated prompts use both fields appropriately
  ```
- **Implementation Notes:**
  ```typescript
  const userPrompt = `videoScript: ${contentResponse.videoScript}

  voiceScript: ${contentResponse.voiceScript}

  Generate 3 Veo-optimized scene prompts following the strategy above.`;
  ```

### Step 4.3: Update CALL 2 Zod schema `[ ]`
- **Priority:** High
- **Task:** Update CALL 2 schema to remove `content`/`description` fields, keep only `prompt`.
- **Files:**
  - `src/lib/script-generator.ts`
- **Step Dependencies:** Phase 1 complete
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Validation should pass with just prompt field
  ```
- **Implementation Notes:**
  ```typescript
  const Call2Schema = z.object({
    scenes: z.array(z.object({
      sceneNumber: z.number().int().min(1).max(3),
      prompt: z.string().min(10)
    })).length(3)
  });
  ```

### Step 4.4: Update VideoScript assembly `[ ]`
- **Priority:** High
- **Task:** Assemble final VideoScript object with new field names before returning.
- **Files:**
  - `src/lib/script-generator.ts`
- **Step Dependencies:** Steps 4.1, 4.2, 4.3
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Check output/dry-run JSON has correct structure
  ```
- **Implementation Notes:**
  - Combine CALL 1 response (videoScript, voiceScript) with CALL 2 response (scenes)
  - Ensure no deprecated fields included
  - Return properly typed VideoScript object

---

## Phase 5: Data Processor Updates

Enable all problems extraction with proper fallback handling.

### Step 5.1: Update extractProblems to use filter `[ ]`
- **Priority:** High
- **Task:** Change `.find()` to `.filter()` to extract all matching problems per category, not just first.
- **Files:**
  - `src/lib/data-processor.ts`
- **Step Dependencies:** None
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 5
  # Should process multiple problems, not just 1 per category
  # Check console logs show correct problem count
  ```
- **Implementation Notes:**
  ```typescript
  for (const category of filteredCategories) {
    const rows = allRows.filter(r =>  // CHANGED: find → filter
      r.lifeChallengeOption?.replace(/^"+|"+$/g, '').trim() === category &&
      r.onboardingV7_lifeChallenge?.trim()
    );

    for (const row of rows) {
      if (row.onboardingV7_lifeChallenge) {
        problems.push({
          category,
          problem: row.onboardingV7_lifeChallenge.trim()
        });
      }
    }

    // Fallback if NO problems for category
    if (rows.length === 0) {
      logger.warn(`No problems found for category: ${category}, using generic`);
      problems.push({
        category,
        problem: `Struggling with ${category.toLowerCase()}`
      });
    }
  }
  ```

### Step 5.2: Test with different --limit values `[ ]`
- **Priority:** Medium
- **Task:** Validate that --limit correctly caps total videos across all problems and templates.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** Step 5.1
- **User Instructions / Validation:**
  ```bash
  # Test various limits
  npm run generate -- --dry-run --limit 1
  npm run generate -- --dry-run --limit 5
  npm run generate -- --dry-run --limit 10

  # Verify correct number of videos generated
  # Formula: min(limit, problems.length) videos per template
  ```
- **Implementation Notes:**
  - Check main loop applies limit correctly
  - Verify distribution across templates works as expected

---

## Phase 6: Video Generation (Veo 3.1 + Frame Chaining)

Implement frame extraction, chaining, and video combining.

### Step 6.1: Add negative_prompt to Veo calls `[ ]`
- **Priority:** High
- **Task:** Add `negative_prompt` parameter to all Veo API calls.
- **Files:**
  - `src/lib/video-generator.ts`
- **Step Dependencies:** Step 2.3 (config updated)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Listen for background music - should be absent
  ```
- **Implementation Notes:**
  ```typescript
  const input: any = {
    prompt: scene.prompt,
    aspect_ratio: this.config.videoGeneration.aspectRatio,
    duration: this.config.videoGeneration.duration,
    negative_prompt: this.config.videoGeneration.negativePrompt,
    // ... other params
  };
  ```

### Step 6.2: Implement frame extraction utility `[ ]`
- **Priority:** Critical
- **Task:** Create utility function to extract last frame from video using ffmpeg.
- **Files:**
  - `src/lib/video-generator.ts` or new `src/utils/ffmpeg.ts`
- **Step Dependencies:** None (can be parallel with other steps)
- **User Instructions / Validation:**
  ```bash
  # Test extraction standalone
  ffmpeg -i test.mp4 -vf "select='eq(n,191)'" -frames:v 1 test_last.jpg
  ls -lh test_last.jpg  # Should exist
  ```
- **Implementation Notes:**
  ```typescript
  async extractLastFrame(videoPath: string, outputPath: string): Promise<void> {
    const command = `ffmpeg -i "${videoPath}" -vf "select='eq(n,191)'" -frames:v 1 "${outputPath}"`;
    // Execute command, handle errors
    // Retry once on failure
  }
  ```
  - Frame 191 = last frame of 8s @ 24fps video
  - Output as JPEG
  - Store in `videos/{videoId}/frames/`

### Step 6.3: Update directory structure creation `[ ]`
- **Priority:** High
- **Task:** Create `videos/{videoId}/scenes/` and `videos/{videoId}/frames/` directories before generation.
- **Files:**
  - `src/lib/video-generator.ts`
- **Step Dependencies:** Step 2.4 (config paths added)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Check directories created: output/videos/{videoId}/scenes/ and frames/
  ```
- **Implementation Notes:**
  ```typescript
  const videoDir = path.join(config.paths.videosDir, videoId);
  const scenesDir = path.join(videoDir, 'scenes');
  const framesDir = path.join(videoDir, 'frames');

  await fs.mkdir(scenesDir, { recursive: true });
  await fs.mkdir(framesDir, { recursive: true });
  ```

### Step 6.4: Implement frame chaining logic `[ ]`
- **Priority:** Critical
- **Task:** Add logic to use previous scene's last frame as `image` parameter for scenes 2 and 3.
- **Files:**
  - `src/lib/video-generator.ts`
- **Step Dependencies:** Steps 6.2, 6.3
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Check visual continuity between scenes manually
  # Scene 2 and 3 should maintain character/setting from previous
  ```
- **Implementation Notes:**
  ```typescript
  let previousLastFrame: string | undefined;

  for (const scene of script.scenes) {
    const input: any = {
      prompt: scene.prompt,
      // ... other params
    };

    // Add image parameter for scenes 2-3
    if (scene.sceneNumber > 1 && previousLastFrame) {
      input.image = previousLastFrame;
    }

    // Generate video
    const result = await this.generateVideoClip(input, videoId, scene.sceneNumber);

    // Extract last frame for next scene
    if (scene.sceneNumber < 3) {
      const lastFramePath = path.join(framesDir, `scene${scene.sceneNumber}_last.jpg`);
      await this.extractLastFrame(result.videoPath, lastFramePath);
      previousLastFrame = lastFramePath;
    }
  }
  ```
  - Scene 1: No image parameter
  - Scene 2: image = scene1_last.jpg
  - Scene 3: image = scene2_last.jpg

### Step 6.5: Implement video combining `[ ]`
- **Priority:** Critical
- **Task:** Concatenate 3 scene videos into single 24-second video using ffmpeg.
- **Files:**
  - `src/lib/video-generator.ts` or new `src/lib/video-assembler.ts`
- **Step Dependencies:** Step 6.4 (all scenes generated)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Check final.mp4 exists and is 24 seconds
  ffprobe output/videos/{videoId}/final.mp4
  ```
- **Implementation Notes:**
  ```typescript
  async combineScenes(videoId: string, scenePaths: string[]): Promise<string> {
    const videoDir = path.join(config.paths.videosDir, videoId);
    const concatFile = path.join(videoDir, 'concat.txt');
    const outputPath = path.join(videoDir, 'final.mp4');

    // Create concat.txt
    const concatContent = scenePaths.map(p => `file '${p}'`).join('\n');
    await fs.writeFile(concatFile, concatContent);

    // Run ffmpeg
    const command = `ffmpeg -f concat -safe 0 -i "${concatFile}" -c copy "${outputPath}"`;
    // Execute, handle errors, retry once on failure

    return outputPath;
  }
  ```

### Step 6.6: Update scene generation flow `[ ]`
- **Priority:** High
- **Task:** Refactor generateVideoClip to handle sequential generation with frame extraction between scenes.
- **Files:**
  - `src/lib/video-generator.ts`
- **Step Dependencies:** Steps 6.2, 6.4, 6.5
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Full video generation should work end-to-end
  # Check: 3 scenes + frames + final.mp4 all present
  ```
- **Implementation Notes:**
  - May need to restructure main generation method
  - Sequential: Scene 1 → extract → Scene 2 → extract → Scene 3 → combine
  - Error handling: retry frame extraction, log failures, continue without chaining if extraction fails

---

## Phase 7: Output Assemblers

Update manifest and dry-run outputs to match new schema.

### Step 7.1: Update OutputAssembler for new manifest structure `[ ]`
- **Priority:** High
- **Task:** Update manifest generation to use new field names and flexible content structure.
- **Files:**
  - `src/lib/output-assembler.ts`
- **Step Dependencies:** Phase 1 (types defined), Phase 4 (script structure updated)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  # Check output/manifests/{videoId}.json structure
  # Should have: videoId, problemCategory, contentTemplate, content.videoScript, content.voiceScript
  ```
- **Implementation Notes:**
  ```typescript
  const manifest: Manifest = {
    videoId: script.id,
    problemCategory: script.category,  // renamed
    contentTemplate: script.template,  // renamed
    timestamp: script.timestamp,
    userProblem: userProblem.problem,
    content: {
      videoScript: script.videoScript,
      voiceScript: script.voiceScript
    },
    scenes: script.scenes.map(s => ({
      sceneNumber: s.sceneNumber,
      prompt: s.prompt
    })),
    finalVideoPath: `output/videos/${script.id}/final.mp4`
  };
  ```

### Step 7.2: Create manifests directory and save manifests `[ ]`
- **Priority:** High
- **Task:** Ensure manifests directory exists and save manifest JSON files there.
- **Files:**
  - `src/lib/output-assembler.ts`
- **Step Dependencies:** Step 7.1, Step 2.4 (config paths)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1
  ls output/manifests/
  # Should see {videoId}.json file
  ```
- **Implementation Notes:**
  ```typescript
  const manifestsDir = this.config.paths.manifestsDir;
  await fs.mkdir(manifestsDir, { recursive: true });

  const manifestPath = path.join(manifestsDir, `${videoId}.json`);
  await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2));
  ```

### Step 7.3: Update DryRunAssembler to match manifest structure `[ ]`
- **Priority:** Medium
- **Task:** Simplify dry-run output to remove veoParams and deprecated fields, align with manifest structure.
- **Files:**
  - `src/lib/dry-run-assembler.ts`
- **Step Dependencies:** Phase 1 (types defined), Step 7.1 (manifest structure defined)
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 1
  # Check output/dry-run/{videoId}.json
  # Should be clean: just metadata + scenes[].prompt
  ```
- **Implementation Notes:**
  ```typescript
  const dryRunOutput = {
    videoId: script.id,
    userProblem: userProblem.problem,
    category: script.category,
    template: script.template,
    scenes: script.scenes.map(s => ({
      sceneNumber: s.sceneNumber,
      prompt: s.prompt
    }))
  };
  // REMOVED: veoParams, content fields
  ```

---

## Phase 8: Integration & Validation

End-to-end testing and validation of full pipeline.

### Step 8.1: Test dry-run mode end-to-end `[ ]`
- **Priority:** High
- **Task:** Run full dry-run with limit 5, validate all outputs correct.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** All previous phases complete
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --dry-run --limit 5

  # Check:
  # 1. Script generation works (output/scripts/)
  # 2. Dry-run outputs correct (output/dry-run/)
  # 3. videoScript + voiceScript present
  # 4. Scene 1 prompts detailed, 2-3 minimal
  # 5. No errors in console
  ```
- **Implementation Notes:**
  - Validate JSON structure matches requirements
  - Check prompt quality manually
  - Verify dialogue breakdown across scenes

### Step 8.2: Test single video generation `[ ]`
- **Priority:** Critical
- **Task:** Generate one complete video, validate all features working.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** Step 8.1 passes
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 1

  # Check:
  # 1. All 3 scenes generate successfully
  # 2. Frames extracted (output/videos/{videoId}/frames/)
  # 3. Scenes saved (output/videos/{videoId}/scenes/)
  # 4. Final video combined (output/videos/{videoId}/final.mp4)
  # 5. Manifest saved (output/manifests/{videoId}.json)
  # 6. No background music in video
  # 7. Visual continuity between scenes (manual review)
  # 8. Video is 24 seconds
  ```
- **Implementation Notes:**
  - Watch for frame extraction errors
  - Verify frame chaining by checking character consistency
  - Check audio quality and voice changes (acceptable for POC)
  - Time the generation (~4-5 minutes expected)

### Step 8.3: Test with multiple problems `[ ]`
- **Priority:** High
- **Task:** Generate 5-10 videos to test stability and data handling.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** Step 8.2 passes
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 10

  # Check:
  # 1. All videos generate (or failures logged properly)
  # 2. Different userProblems processed
  # 3. File organization correct
  # 4. No memory leaks or crashes
  # 5. State management working if interrupted
  ```
- **Implementation Notes:**
  - Monitor for any edge cases in problem text
  - Check if fallback problems generate acceptable content
  - Verify cost tracking aligns with expectations (~$5 per video)

### Step 8.4: Clean start test `[ ]`
- **Priority:** Medium
- **Task:** Delete state.json and run fresh generation to ensure clean start works.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** Step 8.3
- **User Instructions / Validation:**
  ```bash
  rm output/state.json
  npm run generate -- --limit 2

  # Should initialize fresh, no errors referencing old state
  ```
- **Implementation Notes:**
  - Schema changes may make old state incompatible
  - Document need for clean start in cycle notes

### Step 8.5: Resume test `[ ]`
- **Priority:** Low
- **Task:** Test --resume flag works with new schema.
- **Files:**
  - No changes, testing only
- **Step Dependencies:** Step 8.4
- **User Instructions / Validation:**
  ```bash
  npm run generate -- --limit 5
  # Interrupt with Ctrl+C after 2 videos

  npm run generate -- --resume
  # Should continue from where it stopped
  ```
- **Implementation Notes:**
  - If resume doesn't work due to schema changes, document as known issue
  - Can be fixed in future cycle if needed

---

## Post-Implementation Checklist

- [ ] `npm run build` - No TypeScript errors
- [ ] `npm run lint` - Code style passes
- [ ] Dry-run with --limit 1 produces valid output
- [ ] Full generation with --limit 1 completes successfully
- [ ] Frame chaining visually verified (character consistency)
- [ ] Manifest structure matches specification
- [ ] No background music in generated videos
- [ ] Output folder structure matches requirements
- [ ] Documentation updated if needed (CLAUDE.md, README)

---

## Retro Notes

*(To be filled in after implementation)*

**Wins:**
-

**Pitfalls:**
-

**Ideas for next cycle:**
-
