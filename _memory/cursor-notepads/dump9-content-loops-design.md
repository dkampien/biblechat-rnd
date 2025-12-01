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

Let's discuss the system a bit more. Let me run you through a user story.
  I first wanted comicbooks to use as in-app content. So in that case, I had stories, pages as images with
  3 panels per image. I also had a story-data.json for the dev guys to implement the comics easier in app.
  Also a thumbnail image. 

  Then I needed a variant of comicbooks for kids. I changed the style, ran 15 stories and I also needed an
  audio for each story that I did through eleven labs. So in the final bundle I had the stories folder
  with pages, story data, voice mp3. 

  Now, Adloops needs ads. So I would need to generate comicbook assets for ads made in adloops. 

  Is it more clear now?


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