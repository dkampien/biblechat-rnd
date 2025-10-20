/**
 * Script Generator
 * OpenAI integration for generating video scripts
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { z } from 'zod';
import OpenAI from 'openai';
import { zodResponseFormat } from 'openai/helpers/zod';
import { ProblemCategory, TemplateType, VideoScript, Scene, SceneStatus, UserProblem } from '../types/script.types';
import { Template } from '../types/script.types';
import { Config } from '../types/config.types';
import { ScriptGenerationError } from '../utils/errors';
import { logger } from '../utils/logger';
import { withRetry, generateVideoId, generateScriptPath } from '../utils/helpers';

/**
 * ScriptGenerator class for LLM-based script generation
 */
export class ScriptGenerator {
  private client: OpenAI;
  private templates: Map<TemplateType, Template>;
  private config: Config;

  constructor(config: Config, templates: Map<TemplateType, Template>) {
    this.config = config;
    this.templates = templates;
    this.client = new OpenAI({
      apiKey: config.apis.openai.apiKey
    });
  }

  /**
   * Generate a video script for a problem and template (two-step process)
   */
  async generateScript(
    userProblem: UserProblem,
    template: TemplateType
  ): Promise<VideoScript> {
    try {
      logger.info(`Generating script: ${userProblem.category} × ${template}`);
      logger.debug(`Problem: "${userProblem.problem}"`);

      // Get template
      const templateDef = this.templates.get(template);
      if (!templateDef) {
        throw new ScriptGenerationError(
          `Template not found: ${template}`,
          { category: userProblem.category, template }
        );
      }

      // CALL 1: Generate content (overallScript + scenes[].content)
      logger.info('  Step 1/2: Generating content...');
      const contentResponse = await this.generateContent(userProblem, templateDef);

      // CALL 2: Generate prompts (scenes[].prompt from scenes[].content)
      logger.info('  Step 2/2: Generating prompts...');
      const scenesWithPrompts = await this.generatePrompts(
        contentResponse.scenes,
        templateDef
      );

      // Build VideoScript object
      const videoScript = this.buildVideoScript(
        contentResponse.overallScript,
        scenesWithPrompts,
        userProblem.category,
        template
      );

      // Save script to disk
      const scriptPath = generateScriptPath(
        this.config.paths.scriptsDir,
        userProblem.category,
        template
      );
      await this.saveScript(videoScript, scriptPath);

      logger.success(`Script generated and saved: ${path.basename(scriptPath)}`);

      return videoScript;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      logger.error(`Script generation failed for ${userProblem.category} × ${template}:`, errorMessage);

      throw new ScriptGenerationError(
        `Failed to generate script: ${errorMessage}`,
        { category: userProblem.category, template }
      );
    }
  }

  /**
   * CALL 1: Generate content (overallScript + scenes[].content)
   */
  private async generateContent(
    userProblem: UserProblem,
    template: Template
  ): Promise<{ overallScript: string; scenes: Array<{ sceneNumber: number; content: string }> }> {
    try {
      const systemPrompt = template.systemPromptCall1;

      const userPrompt = `Category: ${userProblem.category}
Problem: ${userProblem.problem}

Generate a 3-scene video script addressing this specific problem.`;

      logger.debug(`Calling OpenAI API (Call 1) - model: ${this.config.apis.openai.model}`);

      // Define Zod schema for Call 1 response
      const ContentSchema = z.object({
        overallScript: z.string().min(50),
        scenes: z.array(z.object({
          sceneNumber: z.number().int().min(1).max(3),
          content: z.string().min(10)
        })).length(3)
      });

      // Make API call with retry
      const response = await withRetry(
        async () => {
          const completion = await this.client.chat.completions.create({
            model: this.config.apis.openai.model,
            messages: [
              { role: 'system', content: systemPrompt },
              { role: 'user', content: userPrompt }
            ],
            response_format: zodResponseFormat(ContentSchema, 'content_generation'),
            temperature: this.config.apis.openai.temperature,
            max_tokens: this.config.apis.openai.maxTokens
          });

          const message = completion.choices[0]?.message;
          if (!message?.content) {
            throw new ScriptGenerationError('No response from OpenAI (Call 1)', {
              category: userProblem.category,
              template: template.id
            });
          }

          return ContentSchema.parse(JSON.parse(message.content));
        },
        {
          maxRetries: 3,
          backoff: 'exponential',
          baseDelay: 1000,
          onRetry: (attempt, error) => {
            logger.warn(`Content generation retry ${attempt}:`, error.message);
          }
        }
      );

      logger.debug(`Content generated: ${response.scenes.length} scenes`);
      return response;
    } catch (error) {
      throw new ScriptGenerationError(
        `Content generation failed (Call 1): ${error instanceof Error ? error.message : String(error)}`,
        { category: userProblem.category, template: template.id }
      );
    }
  }

  /**
   * CALL 2: Generate prompts from content
   */
  private async generatePrompts(
    scenes: Array<{ sceneNumber: number; content: string }>,
    template: Template
  ): Promise<Array<{ sceneNumber: number; content: string; prompt: string }>> {
    try {
      const systemPrompt = template.systemPromptCall2;

      const scenesWithPrompts = [];

      for (const scene of scenes) {
        const userPrompt = `Scene ${scene.sceneNumber} content:\n${scene.content}\n\nGenerate an optimized Veo 3 prompt for this scene.`;

        logger.debug(`Generating prompt for scene ${scene.sceneNumber}...`);

        // Define Zod schema for Call 2 response
        const PromptSchema = z.object({
          prompt: z.string().min(20)
        });

        const response = await withRetry(
          async () => {
            const completion = await this.client.chat.completions.create({
              model: this.config.apis.openai.model,
              messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userPrompt }
              ],
              response_format: zodResponseFormat(PromptSchema, 'prompt_generation'),
              temperature: 0.7,
              max_tokens: 500
            });

            const message = completion.choices[0]?.message;
            if (!message?.content) {
              throw new ScriptGenerationError('No response from OpenAI (Call 2)', {
                sceneNumber: scene.sceneNumber,
                template: template.id
              });
            }

            return PromptSchema.parse(JSON.parse(message.content));
          },
          {
            maxRetries: 3,
            backoff: 'exponential',
            baseDelay: 1000,
            onRetry: (attempt, error) => {
              logger.warn(`Prompt generation retry ${attempt} (scene ${scene.sceneNumber}):`, error.message);
            }
          }
        );

        scenesWithPrompts.push({
          sceneNumber: scene.sceneNumber,
          content: scene.content,
          prompt: response.prompt
        });

        logger.debug(`Prompt generated for scene ${scene.sceneNumber}`);
      }

      return scenesWithPrompts;
    } catch (error) {
      throw new ScriptGenerationError(
        `Prompt generation failed (Call 2): ${error instanceof Error ? error.message : String(error)}`,
        { template: template.id }
      );
    }
  }

  /**
   * Build VideoScript object from generated content
   */
  private buildVideoScript(
    overallScript: string,
    scenes: Array<{ sceneNumber: number; content: string; prompt: string }>,
    category: ProblemCategory,
    template: TemplateType
  ): VideoScript {
    const videoId = generateVideoId(category, template);
    const timestamp = new Date().toISOString();

    // Convert scenes to proper Scene objects
    const processedScenes: Scene[] = scenes.map(scene => ({
      sceneNumber: scene.sceneNumber,
      content: scene.content,
      prompt: scene.prompt,
      status: 'pending' as SceneStatus,
      videoClipPath: undefined,
      predictionId: undefined,
      error: undefined
    }));

    return {
      id: videoId,
      category,
      template,
      timestamp,
      overallScript,  // Use LLM-generated overallScript (don't generate locally)
      scenes: processedScenes
    };
  }

  /**
   * Save script to disk as JSON
   */
  private async saveScript(script: VideoScript, scriptPath: string): Promise<void> {
    try {
      // Ensure directory exists
      const dir = path.dirname(scriptPath);
      await fs.mkdir(dir, { recursive: true });

      // Write JSON file
      const content = JSON.stringify(script, null, 2);
      await fs.writeFile(scriptPath, content, 'utf-8');

      logger.debug(`Script saved to: ${scriptPath}`);
    } catch (error) {
      throw new ScriptGenerationError(
        `Failed to save script: ${error instanceof Error ? error.message : String(error)}`,
        { scriptPath }
      );
    }
  }
}
