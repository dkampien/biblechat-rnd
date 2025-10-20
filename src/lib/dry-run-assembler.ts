/**
 * Dry-Run Assembler
 * Assembles dry-run output files for manual Veo testing
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { VideoScript, UserProblem } from '../types/script.types';
import { Config } from '../types/config.types';
import { logger } from '../utils/logger';

/**
 * Dry-run output format
 */
interface DryRunOutput {
  videoId: string;
  userProblem: string;
  category: string;
  template: string;
  scenes: Array<{
    sceneNumber: number;
    content: string;
    prompt: string;
    veoParams: {
      prompt: string;
      duration: number;
      aspect_ratio: string;
      generate_audio: boolean;
      resolution?: string;
    };
  }>;
}

/**
 * DryRunAssembler class
 */
export class DryRunAssembler {
  private config: Config;

  constructor(config: Config) {
    this.config = config;
  }

  /**
   * Assemble and save dry-run output for a video
   */
  async assembleDryRunOutput(
    script: VideoScript,
    userProblem: UserProblem
  ): Promise<void> {
    try {
      // Build dry-run output
      const dryRunOutput: DryRunOutput = {
        videoId: script.id,
        userProblem: userProblem.problem,
        category: script.category,
        template: script.template,
        scenes: script.scenes.map(scene => ({
          sceneNumber: scene.sceneNumber,
          content: scene.content,
          prompt: scene.prompt,
          veoParams: {
            prompt: scene.prompt,
            duration: this.config.videoGeneration.duration,
            aspect_ratio: this.config.videoGeneration.aspectRatio,
            generate_audio: this.config.videoGeneration.generateAudio ?? true,
            ...(this.config.videoGeneration.resolution && {
              resolution: this.config.videoGeneration.resolution
            })
          }
        }))
      };

      // Save to file
      const dryRunDir = path.join(this.config.paths.outputDir, 'dry-run');
      await fs.mkdir(dryRunDir, { recursive: true });

      const filename = `${script.id}.json`;
      const filepath = path.join(dryRunDir, filename);

      const content = JSON.stringify(dryRunOutput, null, 2);
      await fs.writeFile(filepath, content, 'utf-8');

      logger.debug(`Dry-run output saved: ${filename}`);
    } catch (error) {
      logger.error('Failed to save dry-run output:', error);
      throw error;
    }
  }
}
