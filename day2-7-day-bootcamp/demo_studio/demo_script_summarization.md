# Demo — Summarization: Weak vs Strong
url: http://localhost:8501
viewport: 1280x800
headless: false

### Beat 1 — Intro
narration: Let's actually run the Prompt Engineering Playground we built, and watch a weak prompt and a strong prompt go head to head on a real task.

### Beat 2 — Choose Summarization
do: select | label=Choose Prompt Type | value=Summarization
narration: Over here in the sidebar, I'll choose Summarization as our task.

### Beat 3 — Paste the text
do: fill | textbox=Enter your text, topic, or | value=Artificial intelligence is being used across industries to automate repetitive tasks, improve decision-making, personalize customer experiences, and generate content. However, companies must also consider privacy, bias, security, and accuracy when adopting AI tools.
narration: Then I'll paste in a short paragraph about how AI is used across industries, the text we want summarized.

### Beat 4 — Weak vs strong prompt
narration: And straight away, look at the two prompts the app just built for the very same request. On the left, the weak prompt, basically just, do this task, here is the input. On the right, the strong prompt, with a clear role, a set of rules, the text, and an exact output format. Same goal, two completely different sets of instructions.

### Beat 5 — Generate the responses
do: click | button=Compare AI Responses
do: wait_for | text=Response from Strong Prompt
narration: Now I'll hit Compare AI Responses, and the app sends both prompts to the very same model. Let's watch the two answers come back side by side.

### Beat 6 — The difference
narration: And there is the whole point of the lab, right in front of us. Same model, both times. The weak prompt gives us a loose, rambling summary. The strong prompt comes back clean, the key points as bullets and a one-sentence takeaway at the end, exactly the format we asked for. Nothing about the AI changed. The only thing that changed was how clearly we asked.
