TASKS
- [ ] Understand current adloops structure and the diagram
- [ ] Convert the existing template to production template
- [ ] Finish exploring and designing the contentloops system 
    - [ ] Datasources, databases, storage buckets, interactivity, 



## GENERAL
- System interactivity by CLI, flags. Or interactive CLI?



## ADLOOPS
- No mixing constraints. I can have a hook with a baked overlay and a body with a manual overlay.



        
Legend
- Components
    - hooks
    - bodies
    - ctas
    - overlays
    - audios
    - voices
- Video mixes
- Templates

ADLOOPS FLOW
1. The template triggers mix creation
2. Mix creation assembels components into parts
3. Part generation
4. Video rendergin
5. Content tagging
6. Experiment creation


TEMPLATES
- ADLOOPS template
- CONTENTLOOPS template



----

Content type - comicsbooks from bible stories

Content purpose
- in-app content
- adloops feed 

Output bundle
- generated assets

Content variant
- standard comics
- kids comics



TEMPLATES
- Content type (ex comics)
    - manual template plan (v4) - I need to rewrite this into a production ready variant, multiple llm calls, and other workflow details
    - production template plan - the produciton ready variant
    - production template implementation - the code implementation


Production template plan
    - Workflow steps
        - Generation step subworkflow (replicate, comfyui)


COMPLETE MENTAL MODEL HIEARCHY OF THE ENTIRE THING
- ADLOOPS (FINAL AD DELIVERABLE)
    - COMPONENTS (EG HOOKS, BODIES)
        - CLOOPS (COMPONENT SUPPLIER?)
            - TEMPLATE PLAN
                - eg WORKFLOW STEPS
                    - eg PROMPT GEN STEP (has substeps)
                        - eg step 3 fill block values, assemble prompt, format output properly
                    - eg GEENRATION STEP SUBWORKFLOW (REPLICATE, COMFYUI)
            - TEMPLATE CODE IMPLEMENTATION


Start from the simplest to complex - added to system prompt. 


----


cloops_exploration-session
cloops_system-level-decisions


----



Notes (post-implementation)
- How would I explain this system to the CTO?
- What happened to the scheduling part? How would it work?
- What happened about the firestore storage?  
- Adloops manifest 
- How it would behave with another input source eg the csv parsing data?


----


User Story
- I want a batch of 20 comics for kids to use in ads. Full naration bundled 

Notes
- Should the system also work outside adloops?
- Can the system manage ads variants and in-app variants? What info is packaged? Different steps? 
- How can the system manage already made stories? Can it redo existing story?
- Need fal api key


----

- Validate againht user story. 
    - Add: I want to see the prompt that was used for a specific image. This means adding naming conventions to the files?

- How does the system choses how many stories to extract?
- Does the system, take books and stories in an order? So the cursor concept works?
- Datasource conflict 


How does the system analyzez the story? It extracts the full text or based on the summary and key moments?



---


NEXT PHASE OF THE PROJECT

Ok so I reviewed the notes and added some my own notes right now as I was reviewing. 

- We have "faces" in adloops that are not used. We can make a template from that. We can give that assets as inputs (pics) and make a hook video asset with that person in various "settings" eg selfie, podcast, street etc. How would I structure the template for all these? 
- We need to automate the existing carousel produciton. Im not sure how I can cover all types of carousels. They showed me a "god wants to tell you to put a verse on your lockscren". And a "god wants to show you a message".
- Theme and content type - I don't remember what I meant here.
- "you need to handle content pipelines" - I guess this means working with the marketing team / production teams closer and automate their needs
- Scaled marketing on content generation - I don't remember what I meant here either. 
- CTO - "I want to spend 500 dollars on each country with 150% at 12 mos". The discussion shifted here a bit toward "localization". 
- CTO - "I want to make the app truly localaized, 40 languages". Im not sure what this means either.  
- CTO - "I want to spend any amount of money without caring about the content" - Not sure what he meant here either. Could be related to content costs? 
- Content localization on ads - random note.
- Also the cto gave me a new possible use case. Not sure if this applies tho. I showed him the comic templates and he asked if the output assets could be reused without regenerating them. But im not sure if this is the cloops responsibility or adloops. 

- CTO wants a more hand on approach on content. Involvement with the team. He acknowledges that I can build stuff but is not convinced I can do production code. 
- Can I scan adloops and make a local copy to prove my point? -> should I integrate cloops in adloops by myself, should this be the problem?

he want results
---





New template creation process. 

OUTLINE
1. Proudction plan (workflow needed, steps, ai models etc.)
2. Implement the template (code config, workflow, system-prompt, schemas)
3. Test with dry run (validate LLM calls)
4. Test with debug (review full prompt chain)
5. Full run (generate assets and verify output)

Need an outline for the production plan. 
Current reference: template-authoring-guide.md


how to find toktok virals


CLOOPS Template creation process
AI CONTENT PROMPTING GUIDE -> bundle with prompt-generation-guide-v5.5.md, prompt-formula-framework-v2.md etc.

