# Demo — Day 2 Prompt Engineering Playground
url: http://localhost:8501
viewport: 1280x800
headless: false

### Beat 1 — Intro
narration: Welcome back. We just finished building the Prompt Engineering Playground, so let's actually run it and watch a weak prompt and a strong prompt go head to head.

### Beat 2 — Pick a task
do: select | label=Choose Prompt Type | value=Email Writing
narration: Over here in the sidebar, I'll choose Email Writing as our task type.

### Beat 3 — Enter a request
do: fill | label=Enter your text, topic, or request: | value=Write an email to my manager asking for an extension on the project deadline because we found unexpected bugs during testing.
narration: Then I'll type a real request, an email to my manager asking for a deadline extension because we hit some bugs in testing.

### Beat 4 — Weak vs strong prompt
narration: And right away, look at this. On the left we get the weak prompt, just a vague instruction. On the right, the strong prompt, with a clear role, a set of rules, and an output format.

### Beat 5 — Compare the responses
do: click | button=Compare AI Responses
do: wait_for | text=Response from Strong Prompt
narration: Now I'll hit Compare, and the app sends both prompts to the very same model. Watch the two answers come back, side by side.

### Beat 6 — The difference
narration: And there it is. Same model, but the strong prompt gives us a clean subject line, a professional tone, and real structure, while the weak one is loose and generic. That contrast is the whole point of prompt engineering.
