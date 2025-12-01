#!/usr/bin/env node

import { Command } from 'commander';
import { loadTemplate, listTemplates, templateExists, getTemplateInfo } from './template/loader.js';
import { createBacklogDatasource } from './datasource/backlog.js';
import { runTemplate } from './engine/runner.js';
import { cleanupTemp } from './services/storage.js';
import type { RunOptions } from './types/index.js';

const program = new Command();

program
  .name('cloops')
  .description('Template-based content generation system for AdLoops')
  .version('1.0.0');

// ===== RUN Command =====

program
  .command('run <template>')
  .description('Run a template to generate content')
  .option('-d, --dry', 'Dry run (skip image generation)', false)
  .option('-i, --item <id>', 'Run a specific item by ID')
  .action(async (templateName: string, options: { dry: boolean; item?: string }) => {
    try {
      // Validate template exists
      if (!templateExists(templateName)) {
        console.error(`Error: Template "${templateName}" not found.`);
        console.error(`Available templates: ${listTemplates().join(', ') || 'none'}`);
        process.exit(1);
      }

      // Load template (async - loads workflow.ts dynamically)
      const template = await loadTemplate(templateName);
      console.log(`Loaded template: ${template.name}`);

      // Create datasource
      const datasource = createBacklogDatasource(templateName);

      // Get item to process
      let item;
      if (options.item) {
        item = datasource.getItem(options.item);
        if (!item) {
          console.error(`Error: Item "${options.item}" not found in backlog.`);
          process.exit(1);
        }
      } else {
        item = datasource.getNextItem();
        if (!item) {
          console.log('No pending items in backlog.');
          process.exit(0);
        }
      }

      console.log(`Processing item: ${item.id} (${item.input.title})`);

      // Mark as in progress
      datasource.markInProgress(item.id);

      // Run the template
      const runOptions: RunOptions = {
        dry: options.dry,
        item: item.id,
      };

      try {
        await runTemplate(template, item.input, runOptions);

        // Mark complete if not dry run
        if (!options.dry) {
          datasource.markComplete(item.id);
        }

        console.log('\nDone!');
      } catch (error) {
        // Mark as failed
        const errorMessage = error instanceof Error ? error.message : String(error);
        datasource.markFailed(item.id, errorMessage);
        throw error;
      }
    } catch (error) {
      console.error('Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// ===== TEMPLATES Command =====

program
  .command('templates')
  .description('List available templates')
  .action(() => {
    const templates = listTemplates();

    if (templates.length === 0) {
      console.log('No templates found.');
      console.log('Create a template in the templates/ directory with config.json and workflow.ts files.');
      return;
    }

    console.log('Available templates:\n');
    templates.forEach((name) => {
      try {
        const info = getTemplateInfo(name);
        console.log(`  ${name}`);
        console.log(`    Datasource: ${info.datasource}`);
        console.log(`    Model: ${info.model}`);
        console.log(`    Workflow: ${info.hasWorkflow ? '✓' : '✗'}`);
        console.log('');
      } catch {
        console.log(`  ${name} (error loading info)`);
      }
    });
  });

// ===== STATUS Command =====

program
  .command('status <template>')
  .description('Show backlog status for a template')
  .action((templateName: string) => {
    try {
      if (!templateExists(templateName)) {
        console.error(`Error: Template "${templateName}" not found.`);
        process.exit(1);
      }

      const datasource = createBacklogDatasource(templateName);
      const status = datasource.getStatus();
      const items = datasource.getAllItems();

      console.log(`\nBacklog status for: ${templateName}\n`);
      console.log(`  Total:       ${status.total}`);
      console.log(`  Pending:     ${status.pending}`);
      console.log(`  In Progress: ${status.inProgress}`);
      console.log(`  Completed:   ${status.completed}`);
      console.log(`  Failed:      ${status.failed}`);

      if (items.length > 0) {
        console.log('\nItems:');
        items.forEach((item) => {
          const statusIcon =
            item.status === 'completed' ? '✓' :
            item.status === 'failed' ? '✗' :
            item.status === 'in_progress' ? '⋯' : '○';
          console.log(`  ${statusIcon} ${item.id}: ${item.input.title} [${item.status}]`);
          if (item.error) {
            console.log(`      Error: ${item.error}`);
          }
        });
      }

      console.log('');
    } catch (error) {
      console.error('Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// ===== CLEANUP Command =====

program
  .command('cleanup')
  .description('Clean up temporary files')
  .action(() => {
    cleanupTemp();
    console.log('Cleanup complete.');
  });

// Parse and execute
program.parse();
