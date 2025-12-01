import type { BacklogItem, StoryInput } from '../types/index.js';

/**
 * Abstract interface for datasources
 *
 * Datasources provide input items for template execution.
 * Different implementations can read from various sources
 * (JSON backlog, CSV files, databases, APIs, etc.)
 */
export interface Datasource {
  /**
   * Get the next pending item from the datasource
   * Returns null if no items are available
   */
  getNextItem(): BacklogItem | null;

  /**
   * Get a specific item by ID
   * Returns null if item not found
   */
  getItem(itemId: string): BacklogItem | null;

  /**
   * Mark an item as in progress
   */
  markInProgress(itemId: string): void;

  /**
   * Mark an item as completed
   */
  markComplete(itemId: string): void;

  /**
   * Mark an item as failed with an error message
   */
  markFailed(itemId: string, error: string): void;

  /**
   * Get all items with their current status
   */
  getAllItems(): BacklogItem[];

  /**
   * Get counts by status
   */
  getStatus(): DatasourceStatus;
}

/**
 * Status summary for a datasource
 */
export interface DatasourceStatus {
  total: number;
  pending: number;
  inProgress: number;
  completed: number;
  failed: number;
}

/**
 * Factory function type for creating datasources
 */
export type DatasourceFactory = (templateId: string) => Datasource;
