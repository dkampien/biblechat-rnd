


---

PLAN
1. Audit both existing automix implementation
    - understand what automix should do
    - pick best base (video vs image vs fresh)
    - cover frontend + backend
2. Synthesise what an automix should be 
3. Design our clean automix (design a feature)
4. Document the integration plan 


NOTE FOR LATER
1. Template abstraction
    - When to use when building a new template
    - "Not too abstract or too concrete"
2. Template creation lifecycle (critical)
    - Manual template plan (iterate to v4, v5...)
    - Production template plan (finalized spec)
    - Production template implementation (code)
    - Update template authoring guide when we build a new template

OTHER
- Developer env and branching strategy, Git repo strategy, what API to expose for cloops?
    - How do I work on adloops and cloops? Have a backlog? What phases? -> Update ai engineering workflow to take into account working on huge existing codebases, instead of new ones. Work in cycles or sprints? How do I split cloops and adloops? Do I name sprints?
- Template direction. How to create a new template? Give images with the "target" idea?
- Does the automix feature interact with any other externql services or other parts of the sustem?
Ask about in gemini - take this repo and scan

CURRENT RELEVANT FILES
- cloops-integration-handoff
- cloops_system-architecture-diagram
- cloops-adloops-integration-plan


----

api/endpoint 

generate media 




-----

PLAN 


use cases (user stories)
- de la 3 la 6*
- vreau sa ii dau din ce sectiuni din bible api -ranges of stories-
    - count de range add
    - 

in loc de cli trebuie sa il fac network wise adica sa fie https exposed 

- template based or agnostic?

- interfata pentru output for each template sa stie ce sa returneze. 




What we did
- Designed api from existing cli
- Update cli to range 
- Deployed api to firebase as function

Notes
- Why does it include comic data in the request body?


trebuia sa init fire folosind firebase functions through sdk is in folderu functions. in ads library automaiton cum e acolon 
