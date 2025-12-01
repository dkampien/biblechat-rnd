import * as fs from 'node:fs';
import * as path from 'node:path';
import type { Backlog, BacklogItem, ItemStatus } from '../types/index.js';
import type { Datasource, DatasourceStatus } from './types.js';

/**
 * JSON file-based backlog datasource
 *
 * Reads and writes to a JSON file in the data/backlogs/ directory.
 * Each template has its own backlog file.
 */
export class BacklogDatasource implements Datasource {
  private backlog: Backlog;
  private filePath: string;

  constructor(templateId: string) {
    this.filePath = path.join(process.cwd(), 'data', 'backlogs', `${templateId}.json`);
    this.backlog = this.load();
  }

  /**
   * Load backlog from file, creating empty backlog if file doesn't exist
   */
  private load(): Backlog {
    if (!fs.existsSync(this.filePath)) {
      // Create directory if needed
      const dir = path.dirname(this.filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      // Create empty backlog
      const emptyBacklog: Backlog = {
        templateId: path.basename(this.filePath, '.json'),
        items: [],
      };
      this.save(emptyBacklog);
      return emptyBacklog;
    }

    const content = fs.readFileSync(this.filePath, 'utf-8');
    return JSON.parse(content) as Backlog;
  }

  /**
   * Save backlog to file
   */
  private save(backlog?: Backlog): void {
    const data = backlog || this.backlog;
    fs.writeFileSync(this.filePath, JSON.stringify(data, null, 2));
  }

  /**
   * Find an item by ID
   */
  private findItem(itemId: string): BacklogItem | undefined {
    return this.backlog.items.find((item) => item.id === itemId);
  }

  /**
   * Update item status and save
   */
  private updateStatus(itemId: string, status: ItemStatus, error?: string): void {
    const item = this.findItem(itemId);
    if (!item) {
      throw new Error(`Item not found: ${itemId}`);
    }

    item.status = status;

    if (status === 'completed') {
      item.completedAt = new Date().toISOString();
      item.error = undefined;
    } else if (status === 'failed') {
      item.error = error;
    } else if (status === 'in_progress') {
      item.error = undefined;
    }

    this.save();
  }

  // ===== Datasource Interface Implementation =====

  getNextItem(): BacklogItem | null {
    const pending = this.backlog.items.find((item) => item.status === 'pending');
    return pending || null;
  }

  getItem(itemId: string): BacklogItem | null {
    return this.findItem(itemId) || null;
  }

  markInProgress(itemId: string): void {
    this.updateStatus(itemId, 'in_progress');
    console.log(`[Backlog] Item ${itemId} marked as in_progress`);
  }

  markComplete(itemId: string): void {
    this.updateStatus(itemId, 'completed');
    console.log(`[Backlog] Item ${itemId} marked as completed`);
  }

  markFailed(itemId: string, error: string): void {
    this.updateStatus(itemId, 'failed', error);
    console.log(`[Backlog] Item ${itemId} marked as failed: ${error}`);
  }

  getAllItems(): BacklogItem[] {
    return this.backlog.items;
  }

  getStatus(): DatasourceStatus {
    const items = this.backlog.items;
    return {
      total: items.length,
      pending: items.filter((i) => i.status === 'pending').length,
      inProgress: items.filter((i) => i.status === 'in_progress').length,
      completed: items.filter((i) => i.status === 'completed').length,
      failed: items.filter((i) => i.status === 'failed').length,
    };
  }
}

/**
 * Create a backlog datasource for a template
 */
export function createBacklogDatasource(templateId: string): Datasource {
  return new BacklogDatasource(templateId);
}
