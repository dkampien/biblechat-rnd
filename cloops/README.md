# CLoops

Template-based content generation system.

## Setup

```bash
npm install
cp .env.example .env  # Add API keys
```

## Commands

```bash
# Run a template
cloops run <template>              # Full run
cloops run <template> --dry        # Skip image generation
cloops run <template> --debug      # Save debug.md with LLM responses
cloops run <template> --replay     # Load from debug.md, skip LLM
cloops run <template> -i <id>      # Run specific backlog item

# List & status
cloops templates                   # List available templates
cloops status <template>           # Show backlog status

# Cleanup
cloops cleanup                     # Remove temp files
```

## Examples

```bash
# Test LLM calls without generating images
npm run dev -- run comic-books-standard --dry

# Full run with debug output
npm run dev -- run comic-books-standard --debug

# Iterate on image prompts
npm run dev -- run comic-books-standard --debug          # Generate + save debug.md
# Edit image prompts in output/.../debug.md
npm run dev -- run comic-books-standard --replay -i id   # Regenerate images only
```

## Docs

- [Tech Spec](_docs/1_development-docs/core-docs/2-cloops-tech-spec.md)
- [Template Authoring Guide](_docs/2_reference-docs/template-authoring-guide.md)
