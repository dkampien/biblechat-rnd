## CONTENT CONCEPT IDEA
- Bible stories for kids 
- Useage: in-app for the kids variant of biblechat. (yes they have a kids vairant)
- Duration: TBD but around 4 or 5 mins. 
- Final output: video file 
- Structure and idea exploration: I would like to create videos from bible stories that will be consumed by kids. Im thinking to have a mascot (a pigeon) talking for couple of secs at the begining, then have the story unfolded, then maybe have the mascot appear again at the end (with closing remarks, story morale if applicable etc). The pigeon would be the one to narate the story so I would need voice as well.  
- Ideally: I have 3 age groups. 1-5, 6-12, 12+. Would be nice if there would be certain parameters that would be dynamic depending on who is watching, by age group. I would need params for the story tone (kids maybe need simplification), narator voice, narator language (optional for later, would be nice) and the visual style. 

EDIT: In production plan overview

---

## NOTES
- The universal_stories_pool is the metadata extracted via the bible api. But it does not get the full story.
- Remember to tackle the abstract to concrete concept
- Remember to recap the concept of the knowledge layer and the application layer. Only in prompt gen workflow step. 
- Add prottyping in agent builder and comfyui as part of the production plan? how does a manual plan look like? Is manual planning still relevant?
- Have the state of the agent builder (the prompts) in the template production plan
- Do lipsync over audio? or just the pigeon?
- Remember to fix the workflow audio bug 
- Good prompt for workflow alignment : "Print the workflow diagram as ascii as you currently understand it"

---

## AGENT BUILDER CONTEXT
**What we learned:**

1. OpenAI Agent Builder uses the `{{state.variable_name.field}}` syntax.
2. Only string fields work directly in templates.
3. Arrays and objects require a Transform node first.
4. When strict mode is enabled, schema validation requires all fields to be listed as required.

---


## ABOUT THE NEW TEMPLATE CREATION PROCESS
- Should have in context acg guides
- Some kind of process documentation or examples
- Then tell the idea

IDEA -> CONTENT CONCEPT !!! 

Should we have content idea concept template? 
- Core idea: Stories from the bible, animated
- Purpose (eg what does it solve for kids/parents): Entertnainment, Education, spiritual formation. 
- Use case / usage: in-app for biblechat kids
- Final output: videos. Duration unknown depends on the story length
- Structure: TBD
- Style: TBD

More info on this in dump9 and info hierarchy

Add workflow step structure tags, role, constraints, knowledge etc.

---


## CONTEXT REQUIRED (for various tasks)
- AGC GUIDES
- AGENTBUILDER KNOWLEDGE - current prompts?
- TEMPLATE PRODUCTION PLAN
- GOAL HANDOFF
- FILES FOR IMPLEMEMTATION
- CLOOPS SYSTEM ARCH
- EXTERNAL API SERVICES

---

## NEXT TASKS
Task indexes:
- This file
- Cloops repo backlog
- Scattered in various handoff docs

- [x] Solve the bible vids workflow audio sync issue
- [ ] Remember to update the readme file for cloops. 
- [ ] Remember to replace all api keys
- [ ] After first template draft is complete, remember to update your new template workflow
- [ ] Refine error handling for bible stories template. Is it cloops system level or template level?
- [ ] Check template output metadata structure
- [ ] Update LLM call schema for intro to something like mascotIntro, mascotOutro and have coresponding file names

Task ideas: 
- Update the workflow diagrams to reflect the current workflow. (side-note I might need reference)

---


## RESPONSES SCRATCHPAD

---

## FEEDBACK AND REQUIREMENTS
- Make it longer 5 min+
- Have the pigeon the same and re-generate only the audio
- How to check the prompts for each step?
cliffhanger sa ca fie ads
- Watch time de 20 de min pe zi o luna (30 zile)


---


##
Aproaches for making it longer. 
- framechaining 10 secs becoming 20 in visual generation (need 2 images chained)

A. More scenes. Video (scene duration) drives content duration. Driven by i2v model. Audios get padded. 
B. Add framechaining. Video (scene duration) drives content duration. Driven by how many clips we chain (framechaining). Audios get padded.
C. Add framechaining and start from audio first. Audio (audio duration) drives content duration and is generated from the start. Videos clips get trimmed.






How did we solve the visual description for comics? Where does the call from prompt gets its input?


10 char in a single request for elevenlabs

I may need another way to look at the problem. Or a way to properly decompose the problem.


Idea 1
- introduce a new step (LLM call) that breaks down the story into [] and calculates wps and nr of words per scene. Have a 20seconds scene via 2 prompts but one audio. 


Idea 1.
- Introduce a new step (LLM call), that breaks down the story into an additional layer of structure (don't know what or how yet, maybe acts or sequences, I don't know). That call, to output desired words per second and words per scene in a json format. And the LLM call that generates the story would read the output and will know to generate script with dynamic pacing. This might solve the robotic feel but still does not resolve the sync problem, right?



Idea 2
- Introduce a new step (LLM call) with better structure that also outputs wps. Have the downstream llm calls read that wps for each scene. Adapt within video i2i limit. Options 10, 8, 5. 



- number of scenes = more scenes, longer video
- clips per scene = extends scene duration
- prompting strategy for i2v = reduce seam/drift artifacts
- content structure = how we organize
- i2v_frames modality = different scene "rendering" mechanic


Eseentially, 

- 10 sec scenes is robotic and repetitive
  - Have framechaining and or dynamic pacing 
- llm calls are lqrge and can rot and take longer. 

sync strategies
- pad or trim (where I talked about this?)

Order
Script/Scenes
Prompts (t2i, i2v)
TTS + IMAGES
VIDEO
Assemply

- Initially we had the sync problem. audio outputs were N, video outputs were Z
- robotic pacing, repetition

Workflow steps
Steps order and dependencies 
If its llm call the levers 
Step specific levers - llm call system prompt, settings, 


----

temp files:
- duration-sync-framework
- appraoches-framework
- workflow-framework







---

sceneDuration = 10 seconds (hard constraints. also 5,8)
wordsPerMinute (WPM) = 120 WPM
wordsPerSecond (WPS) = 120 / 60 = 2
wordsPerScene (WPSn) = sceneDuration x wordsPerSecond = 10 * 2  = 20
targetVideoDuration = 300 sec+ (assign as min duration?)
sceneCount = targetDuration / sceneDuration = 300 / 10 = 30 scenes

syncStrategy = pad_audio, trim_video 
totalWords = sceneCount x wordsPerScene = 20 x 30 = ~600 words

---


## GOTCHAS 
- Hard limiting LLM words may limit its creativity. Can't do a specific tone and style.
- Elevenlabs has 10k chars per request. 5k in UI 
- visualDesc may overload the LLM in step 2? Separate? 


## BACKLOG IDEAS
- [ ] Implement cliffhangers
- [ ] Add time and story ID for template folder output. (So I can have multiple generation on the same template)
- [ ] Add logging metadata for LLM calls (template keys). So I can sort in openai logs dashboard. 
- [ ] Fix edgecase when audio is longer than video 
- [ ] Investigate audio popping issues
- [ ] Intorduce crossfade at video 
- [ ] Cleanup configs (leave only those that do something)


## NOTES & IDEAS
- Don't foret about scene pacing idea (2 vids under 1 audio)
- Naration style / tone still needs work
- How would you implement dynamic buffer on audio?
- Design a new datasource for a set of child stories plan (bible api manipulation?)
- Generate just the images and animate the images with remotion
- Have a custom made video feature. (FUTURE)




