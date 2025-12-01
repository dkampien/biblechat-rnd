import * as fs from 'node:fs';
import * as path from 'node:path';
import type { BundleData, StoryDataJson, StorageService, DebugMdData, ReplayData, Page } from '../types/index.js';

/**
 * Ensure a directory exists, creating it recursively if needed
 */
export function ensureDir(dirPath: string): void {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Copy a file to a destination
 */
export function copyFile(src: string, dest: string): void {
  fs.copyFileSync(src, dest);
}

/**
 * Write JSON data to a file
 */
export function writeJson(filePath: string, data: unknown): void {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

/**
 * Read JSON data from a file
 */
export function readJson<T>(filePath: string): T {
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content) as T;
}

/**
 * Get the output directory for a template
 */
export function getOutputDir(templateName: string): string {
  return path.join(process.cwd(), 'output', templateName);
}

/**
 * Get the bundle directory for a specific story
 */
export function getBundleDir(templateName: string, storyId: string): string {
  return path.join(getOutputDir(templateName), storyId);
}

/**
 * Write a complete bundle to the output directory
 *
 * @param storyId - Unique identifier for the story
 * @param templateName - Name of the template (e.g., "comic-books-standard")
 * @param data - Bundle data containing images, pages, and metadata
 */
export function writeBundle(
  storyId: string,
  templateName: string,
  data: BundleData
): string {
  const bundleDir = getBundleDir(templateName, storyId);
  ensureDir(bundleDir);

  // Copy page images with sequential numbering
  data.images.forEach((imagePath, index) => {
    const ext = path.extname(imagePath) || '.jpg';
    const destPath = path.join(bundleDir, `${index + 1}${ext}`);
    copyFile(imagePath, destPath);
  });

  // Copy thumbnail if provided
  let thumbnailFile: string | undefined;
  if (data.thumbnailImage) {
    const ext = path.extname(data.thumbnailImage) || '.jpg';
    thumbnailFile = `thumbnail${ext}`;
    copyFile(data.thumbnailImage, path.join(bundleDir, thumbnailFile));
  }

  // Create story-data.json
  const storyData: StoryDataJson = {
    storyId,
    title: data.title,
    thumbnailFile,
    totalPages: data.pages.length,
    pages: data.pages.map((page, index) => {
      const ext = path.extname(data.images[index] || '.jpg');
      return {
        pageNumber: index + 1,
        imageFile: `${index + 1}${ext}`,
        narration: page.narration,
      };
    }),
  };

  writeJson(path.join(bundleDir, 'story-data.json'), storyData);

  console.log(`Bundle written to: ${bundleDir}`);
  return bundleDir;
}

/**
 * Check if a bundle already exists for a story
 */
export function bundleExists(templateName: string, storyId: string): boolean {
  const bundleDir = getBundleDir(templateName, storyId);
  const storyDataPath = path.join(bundleDir, 'story-data.json');
  return fs.existsSync(storyDataPath);
}

/**
 * Clean up temporary files
 */
export function cleanupTemp(): void {
  const tempDir = path.join(process.cwd(), 'temp');
  if (fs.existsSync(tempDir)) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    console.log('Temporary files cleaned up');
  }
}

/**
 * Write debug.md to the bundle directory
 */
export function writeDebugMd(
  templateName: string,
  storyId: string,
  data: DebugMdData
): void {
  const bundleDir = getBundleDir(templateName, storyId);
  ensureDir(bundleDir);
  const debugPath = path.join(bundleDir, 'debug.md');

  // Build markdown content
  const lines: string[] = [
    `# Debug: ${data.title}`,
    '',
    '## Step 1: Narrative',
    '```',
    data.narrative,
    '```',
    '',
    '## Step 2: Pages',
    '```json',
    JSON.stringify(data.pages, null, 2),
    '```',
    '',
    '## Step 3: Image Prompts',
    '',
  ];

  // Add each image prompt
  data.imagePrompts.forEach((prompt, i) => {
    lines.push(`### Page ${i + 1}`);
    lines.push('```');
    lines.push(prompt);
    lines.push('```');
    lines.push('');
  });

  lines.push('## Step 4: Thumbnail');
  lines.push('```');
  lines.push(data.thumbnailPrompt);
  lines.push('```');

  fs.writeFileSync(debugPath, lines.join('\n'));
  console.log(`Debug data written to: ${debugPath}`);
}

/**
 * Read debug.md and parse replay data (steps 2, 3, 4)
 */
export function readDebugMd(
  templateName: string,
  storyId: string
): ReplayData | null {
  const bundleDir = getBundleDir(templateName, storyId);
  const debugPath = path.join(bundleDir, 'debug.md');

  if (!fs.existsSync(debugPath)) {
    return null;
  }

  const content = fs.readFileSync(debugPath, 'utf-8');

  // Parse Step 2: Pages (JSON)
  const pagesMatch = content.match(/## Step 2: Pages\s*```json\s*([\s\S]*?)\s*```/);
  if (!pagesMatch) {
    throw new Error('Could not parse pages from debug.md');
  }
  const pages: Page[] = JSON.parse(pagesMatch[1]);

  // Parse Step 3: Image Prompts
  const imagePrompts: string[] = [];
  const promptRegex = /### Page \d+\s*```\s*([\s\S]*?)\s*```/g;
  let match;
  while ((match = promptRegex.exec(content)) !== null) {
    imagePrompts.push(match[1].trim());
  }

  // Parse Step 4: Thumbnail
  const thumbMatch = content.match(/## Step 4: Thumbnail\s*```\s*([\s\S]*?)\s*```/);
  if (!thumbMatch) {
    throw new Error('Could not parse thumbnail from debug.md');
  }
  const thumbnailPrompt = thumbMatch[1].trim();

  return { pages, imagePrompts, thumbnailPrompt };
}

/**
 * Check if debug.md exists for a story
 */
export function debugMdExists(templateName: string, storyId: string): boolean {
  const bundleDir = getBundleDir(templateName, storyId);
  const debugPath = path.join(bundleDir, 'debug.md');
  return fs.existsSync(debugPath);
}

/**
 * Create a storage service instance for a specific template
 */
export function createStorageService(templateName: string): StorageService {
  return {
    writeBundle: (storyId: string, data: BundleData) => {
      writeBundle(storyId, templateName, data);
    },
  };
}
