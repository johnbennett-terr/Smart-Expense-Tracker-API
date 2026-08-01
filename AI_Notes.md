# AI Notes:

## Stage 1: Research: 

- Decided to go with FastAPI/Python stack as it is the most comfortable for me due to prior experiences.
- Used Claude Sonnet-5 High effort model to help with formulating the Overall architecture flow, function differentiation,  JSON schemas and best practises to be followed for the project.
- From the first generated structural pipeline format idea, I made the following changes:
  - Use JSON files to persist memory across sessions instead of using pure in-memory list.
  - Despite AI suggesting all the bonus options to be fairly lightweight and doable within the 48 hour deadline, I chose to implement only Docker containarization using Docker file as it was something I was keen on implementing and was also relevant to what I had learnt during my systems design course last semester. Additionally, I found it to be the most impactful given the condition to pick atmost one.

## Stage 2: Development:

- Used Claude Code CLI Terminal interface to generate code for the application.
- Right from the first step, I had it build and commit incrementally rather than pushing a large codebase all at once. This flag allowed me to conduct early reviews and ensuring smooth flow of supervised development.
- The entire development took place through claude code (sonnet- 5; high) with manual intervention (discussed below) as and when needed after the requirement specification. This includes all the code files under /src and /tests and README.

## What I validated, tested and changed:

- I ran the entire application myself by cloning the repo. Followed the README: setup, installations, build and run and hit live endpoints to verify and validate the build. I performed this not just after the complete development bu throughout all the intermediate stages of development. Owing to the incremantal flag I had set right at the beginning.
- Caught and fixed a case-sensitivity bug in thr list_all() function withing the src/Storage.py file. This caused the filtered results based on category to be case-sensitive (e.g. if DB had 'Food' category and request was for 'food', it would return nothing).
- Caught and removed a duplicate redundant function ExpenseStorage.search() which inturn just called the list_all() function. Removed and adjusted accordingly.
- The initial requirements.txt filehad fastAPI and uvicorn with no version tags. So, I updated that. And also, for development tools like black and ruff, we segregated it from the requirements.txt file to run the current build into a seperate requirements-dev.txt file.

## Unused AI Suggestions:

- After the earlier round of fixes, Claude Code flagged that return type hints (e.g. -> Expense, -> list[Expense]) were still missing on the endpoint functions in main.py, as part of a broader best-practices checklist we'd set up earlier in the project. I decided not to add them as FastAPI already knows what endpoint's return will be through response_model=Expense. I t provided no functional benefit, merely a cosmetic one.
- Claude Code flagged the two different mechanisms to runt he build: docker env var and default through cli. It suggested a local run path PORT to be also configured instead of uvicorn choosing a default port. forcing a regular cli run to match docker's port just for consistency felt cosmetic and had no functional upside in rel word applications so it was skipped.
