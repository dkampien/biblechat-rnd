import type {
  StoryInput,
  TemplateConfig,
  Services,
  WorkflowContext,
  Page,
  PagePrompt,
} from '../../src/types/index.js';
import { injectVariables } from '../../src/utils/config.js';

// ===== Workflow Implementation =====

export async function run(
  input: StoryInput,
  config: TemplateConfig,
  services: Services,
  ctx: WorkflowContext
): Promise<void> {
  // Track state through the workflow
  let narrative: string | undefined;
  let pages: Page[] | undefined;
  let prompts: PagePrompt[] | undefined;
  let thumbnailPrompt: string | undefined;
  let images: string[] | undefined;
  let thumbnailImage: string | undefined;

  // ===== Step 1: Narrative =====
  console.log('\n--- NARRATIVE ---');
  {
    const systemPrompt = ctx.prompts['step1-narrative'] || 'Generate a narrative adaptation.';
    const userMessage = `
Story Title: ${input.title}
Summary: ${input.summary}
Key Moments: ${input.keyMoments.join(', ')}

Create a narrative adaptation of this story.
`;

    const result = await services.llm.call<{ narrative: string }>({
      systemPrompt,
      userMessage,
      schema: ctx.schemas['narrative'],
    });

    narrative = result.narrative;
    console.log(`✓ Narrative generated (${narrative.length} chars)`);
  }

  // ===== Step 2: Planning =====
  console.log('\n--- PLANNING ---');
  {
    const { pageCount, panelsPerPage } = config.settings;

    let systemPrompt = ctx.prompts['step2-planning'] || `
Plan the visual story with ${pageCount.min}-${pageCount.max} pages, each with ${panelsPerPage} panels.
`;

    // Inject settings variables
    systemPrompt = injectVariables(systemPrompt, {
      'pageCount.min': pageCount.min,
      'pageCount.max': pageCount.max,
      panelsPerPage,
    });

    const userMessage = `
Narrative:
${narrative}

Plan out the visual story with pages and panels.
`;

    const result = await services.llm.call<{ pages: Page[] }>({
      systemPrompt,
      userMessage,
      schema: ctx.schemas['planning'],
    });

    pages = result.pages;
    console.log(`✓ Planning complete (${pages.length} pages)`);
  }

  // ===== Step 3: Prompts =====
  console.log('\n--- PROMPTS ---');
  {
    const styleVars = {
      ...config.style,
      ...config.settings,
    };

    let systemPrompt = ctx.prompts['step3-prompts'] || `
Generate image prompts for each page. Style: {artStyle}, {inkStyle}.
`;

    systemPrompt = injectVariables(systemPrompt, styleVars);

    const pagesJson = JSON.stringify(pages, null, 2);
    const userMessage = `
Pages to generate prompts for:
${pagesJson}

Generate a detailed image prompt for each page.
`;

    const result = await services.llm.call<{ prompts: PagePrompt[] }>({
      systemPrompt,
      userMessage,
      schema: ctx.schemas['prompts'],
    });

    prompts = result.prompts;
    console.log(`✓ Prompts generated (${prompts.length} prompts)`);

    // Log each prompt for review
    prompts.forEach((p) => {
      console.log(`  Page ${p.pageNumber}: ${p.prompt.slice(0, 60)}...`);
    });
  }

  // ===== Step 4: Thumbnail =====
  console.log('\n--- THUMBNAIL ---');
  {
    const styleVars = {
      ...config.style,
      ...config.settings,
    };

    let systemPrompt = ctx.prompts['step4-thumbnail'] || `
Generate a thumbnail prompt for the story cover. Style: {artStyle}.
`;

    systemPrompt = injectVariables(systemPrompt, styleVars);

    const userMessage = `
Story: ${input.title}
Summary: ${input.summary}
Narrative: ${narrative?.slice(0, 500)}...

Create a thumbnail prompt that would make someone want to read this story.
`;

    const result = await services.llm.call<{ prompt: string }>({
      systemPrompt,
      userMessage,
      schema: ctx.schemas['thumbnail'],
    });

    thumbnailPrompt = result.prompt;
    console.log(`✓ Thumbnail prompt generated`);
    console.log(`  ${thumbnailPrompt.slice(0, 80)}...`);
  }

  // ===== Step 5: Generation (skip in dry run) =====
  if (ctx.dry) {
    console.log('\n[DRY RUN] Skipping image generation\n');
    return;
  }

  console.log('\n--- GENERATION ---');
  {
    if (!prompts || prompts.length === 0) {
      throw new Error('No prompts available for generation');
    }

    // Generate page images
    const promptStrings = prompts.map((p) => p.prompt);
    images = await services.replicate.generateImages(promptStrings, config.generation);
    console.log(`✓ Generated ${images.length} page images`);

    // Generate thumbnail
    if (thumbnailPrompt) {
      thumbnailImage = await services.replicate.generateImage(thumbnailPrompt, config.generation);
      console.log(`✓ Generated thumbnail image`);
    }
  }

  // ===== Step 6: Bundle =====
  console.log('\n--- BUNDLE ---');
  {
    if (!pages || !images) {
      throw new Error('Missing pages or images for bundle');
    }

    const storyId = input.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');

    services.storage.writeBundle(storyId, {
      title: input.title,
      images,
      pages,
      thumbnailImage,
    });

    console.log(`✓ Bundle written`);
  }
}
