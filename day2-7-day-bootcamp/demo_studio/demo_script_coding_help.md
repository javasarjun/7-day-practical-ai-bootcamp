# Demo — Coding Help: Weak vs Strong
url: http://localhost:8501
viewport: 1280x800
headless: false

### Beat 1 — Intro
narration: Let's try the playground on a task every developer hits, asking an AI for help understanding some code.

### Beat 2 — Choose Coding Help
do: select | label=Choose Prompt Type | value=Coding Help
narration: I'll switch the task type over to Coding Help.

### Beat 3 — Ask a question
do: fill | textbox=Enter your text, topic, or | value=Explain Python functions to a beginner with an example.
narration: And I'll ask it to explain Python functions to a beginner, with an example.

### Beat 4 — Weak vs strong prompt
narration: Look at the difference in the two prompts again. The weak one just forwards our question. The strong one tells the model to act as a coding tutor, explain the concept first, give clean commented code, then walk through it, and even warn about common mistakes. We have basically handed it a lesson plan.

### Beat 5 — Generate the responses
do: click | button=Compare AI Responses
do: wait_for | text=Response from Strong Prompt
narration: Let's hit Compare and send both to the model.

### Beat 6 — The difference
narration: And you can feel the difference immediately. The weak prompt gives a short, generic answer. The strong prompt comes back like an actual tutor, a clear explanation, a real code example with comments, and a note on the mistakes beginners make. For a teaching tool, that structure is everything, and it came purely from a better prompt.
