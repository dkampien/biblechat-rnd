/**
 * Template Definitions
 * Defines video templates with system prompts for script generation
 */

import { Template, TemplateType } from '../types/script.types';

// Direct-to-Camera Template
const directToCameraTemplate: Template = {
  id: "direct-to-camera",
  name: "Direct-to-Camera",
  description: "Person speaking directly to viewer with empathetic progression",

  systemPromptCall1: `You are creating a comforting video script for someone struggling with a specific problem.

Format: Direct-to-camera speaking style
Tone: Empathetic, conversational, warm
Structure: 3 scenes showing emotional progression

You will receive:
- Category: The general problem area (e.g., "Anxiety or fear")
- Problem: A specific user problem (e.g., "Being scared that the guy I'm falling for is going to leave me")

Your task:
1. Generate an "overallScript" - a prose description of the video concept
   - Write in clear, professional prose (no arrows, no shorthand)
   - Describe the emotional journey: what the video will say and how it progresses
   - Do NOT include template names or technical details
   - 2-4 sentences

2. Generate 3 scenes with "content" field (DOP-style instructions)
   - Each scene should include:
     * Visual description (setting, subject, framing, lighting)
     * The dialogue the person speaks (in quotes)
     * Body language and expression
     * Camera details (close-up, framing, etc.)
   - Keep it short but comprehensive (2-3 sentences)
   - Make sure dialogue is natural, conversational, and speaks directly to the viewer

Guidelines:
- Use second person ("you") in dialogue
- Each scene should be ~10 seconds of spoken content
- Show emotional progression across the 3 scenes
- Ensure consistent person and setting across all scenes
- The person should be warm, relatable, and compassionate`,

  systemPromptCall2: `You are optimizing scene descriptions for Veo 3 text-to-video generation.

Your task:
Given a scene description (DOP-style instructions), create a Veo 3-optimized prompt.

Requirements:
1. Extract the dialogue from the scene description
2. Format it using Veo 3's dialogue syntax: person saying "exact dialogue here"
3. Include visual details: setting, lighting, framing, expression
4. Emphasize that the person is ACTIVELY SPEAKING with mouth moving
5. Keep it concise but vivid (50-100 words)
6. Ensure the dialogue in the prompt matches the dialogue in the content (do not invent or modify)

Example:
Input content: "Person in 30s, warm living room, facing camera. Speaks with concerned expression: 'I know the fear of losing someone feels overwhelming.' Body language open. Window light. Close-up."

Output prompt: "Close-up of warm, empathetic person in their 30s sitting in cozy living room, facing camera, saying: 'I know the fear of losing someone feels overwhelming.' Concerned but warm expression, open body language, natural window light, intimate framing."

Focus on making the video show someone actively delivering comforting dialogue.`,

  promptRules: {
    description: "Direct-to-camera requires person actively speaking dialogue",
    instructions: [
      "Extract dialogue from scene content",
      "Use Veo 3 format: person saying \"dialogue\"",
      "Emphasize mouth moving, active speaking",
      "Include expression, setting, lighting",
      "Keep concise (50-100 words)"
    ],
    veo3Format: "person saying \"exact dialogue\""
  },

  sceneStructure: [
    {
      sceneNumber: 1,
      purpose: "Acknowledge the struggle",
      guidanceForLLM: "Show empathy, validate their feelings, use concerned/warm expression"
    },
    {
      sceneNumber: 2,
      purpose: "Offer comfort and hope",
      guidanceForLLM: "Transition to reassurance, gentle smile, warm and encouraging"
    },
    {
      sceneNumber: 3,
      purpose: "Share scripture and closing",
      guidanceForLLM: "Peaceful, uplifting, confident expression with hope"
    }
  ]
};

// Text + Visuals Template
const textVisualsTemplate: Template = {
  id: "text-visuals",
  name: "Text + Visuals",
  description: "Text overlays on calming background footage",

  systemPromptCall1: `You are creating a reflective video script with text overlays for someone struggling with a specific problem.

Format: Short text snippets displayed over calming visuals
Tone: Peaceful, inspirational, contemplative
Structure: 3 scenes with text progression

You will receive:
- Category: The general problem area
- Problem: A specific user problem

Your task:
1. Generate an "overallScript" - a prose description of the video concept
   - Write in clear, professional prose
   - Describe the message and visual journey
   - 2-4 sentences

2. Generate 3 scenes with "content" field (DOP-style instructions)
   - Each scene should include:
     * The text to display (in quotes, max 2 sentences)
     * Visual description (natural setting, mood, movement)
     * Lighting and atmosphere details
   - No people or faces
   - Focus on serene, calming environments

Guidelines:
- Text should be brief and powerful (1-2 sentences max)
- Visuals should be nature, peaceful settings, soft focus
- Each visual should be ~10 seconds
- Show emotional progression through text + visual pairing`,

  systemPromptCall2: `You are optimizing scene descriptions for Veo 3 text-to-video generation.

Your task:
Given a scene description (text + visual details), create a Veo 3-optimized prompt.

Requirements:
1. Focus on the VISUAL ONLY (no text - platform handles text overlay)
2. Describe natural, calming environments
3. NO people, NO faces in frame
4. Include: setting, movement, lighting, atmosphere, mood
5. Keep it concise but vivid (40-80 words)
6. Emphasize peaceful, serene qualities

Example:
Input content: "Text: 'You are not alone in this.' Visual: Ocean waves at sunset, golden light, peaceful."

Output prompt: "Slow tracking shot of gentle ocean waves rolling onto sandy beach at golden hour sunset, warm amber and pink sky reflecting on water surface, peaceful and serene atmosphere, soft focus on foreground, calming natural movement."

Focus on creating calming, beautiful visuals without any people.`,

  promptRules: {
    description: "Text-visuals requires no people, calming natural environments",
    instructions: [
      "NO people or faces in frame",
      "Focus on natural, calming environments",
      "Describe movement, lighting, atmosphere",
      "Platform handles text overlay separately",
      "Keep concise (40-80 words)"
    ]
  },

  sceneStructure: [
    {
      sceneNumber: 1,
      purpose: "Opening acknowledgment",
      guidanceForLLM: "Acknowledge struggle with short, empathetic text. Calming natural visual."
    },
    {
      sceneNumber: 2,
      purpose: "Scripture/comfort text",
      guidanceForLLM: "Biblical verse or comfort message. Serene, peaceful visual."
    },
    {
      sceneNumber: 3,
      purpose: "Closing message",
      guidanceForLLM: "Hopeful, uplifting closing text. Inspiring, bright visual."
    }
  ]
};

// Template registry
const templates = new Map<TemplateType, Template>([
  ["direct-to-camera", directToCameraTemplate],
  ["text-visuals", textVisualsTemplate]
]);

/**
 * Get template by ID
 */
export function getTemplate(id: TemplateType): Template {
  const template = templates.get(id);
  if (!template) {
    throw new Error(`Template not found: ${id}`);
  }
  return template;
}

/**
 * Get all templates
 */
export function getAllTemplates(): Template[] {
  return Array.from(templates.values());
}

/**
 * Check if template exists
 */
export function hasTemplate(id: string): boolean {
  return templates.has(id as TemplateType);
}

export { templates };
