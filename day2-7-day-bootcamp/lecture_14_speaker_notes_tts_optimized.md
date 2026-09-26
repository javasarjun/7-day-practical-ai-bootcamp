# Lecture 14 — Why Prompt Engineering Matters
## Speaker Notes (TTS-optimized: flowing paragraphs, fewer breath points)

### Slide 1 — Why Prompt Engineering Matters

Welcome to Day 2 of the bootcamp. In Day 1, we built our first AI assistant, connecting Python to a local model through Ollama, creating a terminal chatbot, and then turning it into a Streamlit chatbot. Today, we are going to focus on something that looks simple at first but has a huge impact on the quality of AI applications, and that is prompting. A prompt is not just a question we send to the model; it is the instruction that shapes what the model does, how it responds, and how useful the output becomes. So in this lecture, I want to explain why prompt engineering matters before we start building the Prompt Engineering Playground.

---

### Slide 2 — Same Model, Different Prompt, Different Result

One thing beginners quickly notice is this: the same model can give very different answers depending on how we ask. If we simply say, "Summarize this," the model may still answer, but the result can be too long, too short, too vague, or not formatted the way we need. But if we say, "Summarize this in three bullet points, keep it beginner-friendly, and end with one key takeaway," now the model has a much clearer job. The model did not change; the task became clearer. That is the main idea behind prompt engineering: we are not trying to trick the model, we are trying to communicate better with it.

---

### Slide 3 — A Prompt Controls More Than the Question

A good prompt usually controls more than just the question. It can define the role, for example, "Act as a Python tutor," or "Act as a resume reviewer." It can define the task, for example, "Explain this concept," "rewrite this email," or "analyze this resume." It can provide context, which tells the model what information matters for the answer, and it can include rules, which guide what the model should do or avoid. And it can define the output format, which is very important when we are building apps, because our app may need a clean list, a table, JSON, a score, or a structured report. So when we write prompts for applications, we are really designing the behavior of the AI feature.

---

### Slide 4 — Why This Matters in Real AI Apps

Prompt engineering matters because real users expect consistent and useful output. If an AI app gives a different format every time, the app becomes harder to use and harder to improve. For example, if our resume analyzer sometimes gives paragraphs, sometimes gives bullets, and sometimes forgets the score, the user experience feels messy. But if we design the prompt properly, we can tell the model exactly what sections to return, which makes the output easier to read, easier to test, and easier to display in the UI. That is why prompting is not just a writing skill; for AI builders, it becomes part of application design, one of the places where we define how the AI feature should behave.

---

### Slide 5 — Day 2 Prompt Engineering Playground

In Day 2, we will build a Prompt Engineering Playground. We will compare weak prompts and strong prompts so students can clearly see the difference in output quality. Then we will create reusable prompt templates using a simple structure: role, task, context, rules, and output format. After that, we will save prompts into a small prompt library, and finally, we will run saved prompts on new inputs. This will help us move from random prompting to reusable prompt workflows. In the next lecture, we will start by comparing a weak prompt and a strong prompt side by side.
