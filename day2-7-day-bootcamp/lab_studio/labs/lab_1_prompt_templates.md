# Build Prompt Templates

### Step 1 — A file that only builds text
**File:** prompt_templates.py
**Lang:** python

```python
def build_weak_prompt(task_type, user_input):
    return f"""
Do this task:

Task type: {task_type}

Input:
{user_input}
"""
```

**Walkthrough:**
@ build_weak_prompt
Alright, let's open a brand new file, prompt templates dot py. And before we write a single line, I want you to notice what's not here. There are no imports at the top. No requests, no openai, nothing. That is on purpose. Think of this file as a little factory that only makes text. It does not talk to the model, it does not touch the network, it just takes a few values and hands back a string. Keeping it that pure is exactly what will make it easy to test later. So let's write our very first prompt builder, and we are going to make a weak one, on purpose.

@ "def build_weak_prompt(task_type, user_input):"
Two parameters. Task type is the kind of work we are doing, summarization, email writing, that sort of thing. And user input is literally what the person typed into the box. Quick gut check for you. Nothing in this function actually knows how to do the task well. We are just labeling it and passing it straight through. Hold on to that thought, because it is the whole point.

@ "Task type: {task_type}"
We build the string with an f-string. Those little curly braces are placeholders, and at runtime Python drops the real values right in. So if the task type is summarization and the user pasted an article, this becomes, do this task, task type summarization, here is the input. Clean, readable, and honestly, exactly the kind of lazy prompt most of us write on day one.

@ build_weak_prompt
Now step back and look at what is missing, because this is the lesson. There is no role, we never told the model who to be. There are no rules. There is no output format. We basically walked up to the model and said, figure it out. And it will try, but you will get something a little different every single time. That unpredictability is your enemy when you are building real software. This prompt is not wrong, it is just incomplete, and in a minute you are going to feel the difference.

### Step 2 — The strong prompt, explained in full
**File:** prompt_templates.py
**Lang:** python
**StartLine:** 12

```python
def build_strong_prompt(task_type, user_input):
    if task_type == "Summarization":
        return f"""
You are an expert summarization assistant.

Your task:
Summarize the text clearly and accurately.

Rules:
- Keep the summary simple
- Capture only the most important points
- Do not add information that is not present
- Use bullet points
- End with a one-sentence takeaway

Text:
{user_input}

Output format:
## Summary
- Point 1
- Point 2

## Key Takeaway
One sentence takeaway.
"""
    # ... more task types are added below in the same shape
```

**Walkthrough:**
@ build_strong_prompt
This is the function that matters, so slow down with me here. Same two parameters, but watch what changes. Instead of a vague instruction, we are going to hand the model a fully structured brief, the kind you would give a sharp new teammate on their first day so they do not have to guess. We will build out the summarization version completely, and once you see the shape, every other task type is just a variation on it.

@ "if task_type == "Summarization":"
We branch on the task type. If the user picked summarization, we return this specific prompt. You can already see where this is heading, each task is going to get its own tailored branch, because a good summary prompt and a good email prompt simply need different instructions.

@ "You are an expert summarization assistant."
First line, and it is doing a lot of work. We give the model a role. Telling it, you are an expert summarization assistant, genuinely changes how it writes. It gets more focused, more confident, less rambly. It is the same trick as telling a new hire, act as our summarization specialist, instead of just, hey, summarize this.

@ "Summarize the text clearly and accurately."
Then the task, stated plainly. No clever wording, just exactly what we want done. In prompting, clarity beats cleverness every single time.

@ "- Do not add information that is not present"
Now the rules, and this is where strong prompts earn their paycheck. We tell it to stay simple, keep only the important points, and, this one is huge, do not add information that is not in the text. That one rule is how you fight hallucination. Leave it out, and the model will happily invent a fact that was never there, just to be helpful.

@ "{user_input}"
Then we drop in the user's actual text. Everything above was instructions, this is the raw material it works on. Notice we keep the two clearly separated, so the model never confuses the rules with the content it is supposed to process.

@ "## Summary"
And the finishing touch. We literally show the model the format we want back, a summary section with bullets, then a key takeaway. This is the part beginners skip, and then they wonder why their app breaks. When you pin down the output shape, you can actually parse it, display it, and test it. So there is the full anatomy, role, task, rules, input, output format. Burn those five into your memory, they are the backbone of every strong prompt you will ever write.

### Step 3 — Other task types: only what changes
**File:** prompt_templates.py
**Lang:** python
**StartLine:** 40

```python
    if task_type == "Email Writing":
        return f"""
You are a professional email writing assistant.

Your task:
Write a clear, polite, and professional email based on the user's request.

Rules:
- Keep the tone professional
- Be concise
- Use a clear subject line
- Do not make unsupported claims

User request:
{user_input}

Output format:
Subject: ...

Email:
...
"""
```

**Walkthrough:**
@ "if task_type == "Email Writing":"
Here is the good news, you already learned the hard part. Every other task type is the same five-part skeleton, so from here I will only point out what changes. This is the email branch, same bones, different muscles.

@ "- Use a clear subject line"
The rules just get tuned for email. Keep it professional, be concise, and give it a clear subject line. Those little domain-specific touches are the difference between a generic blob of text and an email your user can actually send without editing.

@ "Subject: ..."
And the output format now asks for a subject line, then the body. Research, content generation, coding help, structured JSON, they all follow this exact recipe. You swap the role, rewrite the rules for that job, and reshape the output. Once it clicks, adding a brand new task type takes you about two minutes.

### Step 4 — Role prompting
**File:** prompt_templates.py
**Lang:** python
**StartLine:** 177

```python
def build_role_prompt(role, user_input):
    return f"""
You are acting as a {role}.

Your task:
Help the user with the following request.

Rules:
- Stay in the role
- Be practical
- Give clear guidance
- Avoid unnecessary jargon

User request:
{user_input}
"""
```

**Walkthrough:**
@ build_role_prompt
Role prompting is a fun one, and it is different enough to deserve its own function. Instead of locking in a task, we let the user pick the persona. Want the answer like a career coach? Like a senior engineer? Like a marketing lead? Same question, completely different advice, just by changing who is answering.

@ "You are acting as a {role}."
And it all hinges on this one line. Whatever role the user picked gets dropped right in here. That is it. That single substitution is what flips the model's entire perspective. It is honestly surprising how much mileage you get out of one well-placed sentence.

@ "- Stay in the role"
The rules just keep it honest. Stay in character, be practical, skip the jargon. Without that stay in the role line, the model tends to drift back into generic assistant voice about halfway through, so we gently hold it in place.

### Step 5 — The reasoning summary prompt
**File:** prompt_templates.py
**Lang:** python
**StartLine:** 195

```python
def build_reasoning_summary_prompt(user_input):
    return f"""
You are a helpful AI tutor.

Answer the user's question clearly.

Rules:
- Give the final answer
- Then provide a brief explanation of the key steps
- Do not over-explain
- Keep it beginner-friendly

Question:
{user_input}

Output format:
## Answer
## Brief Explanation
## Example
"""
```

**Walkthrough:**
@ build_reasoning_summary_prompt
Last template, the reasoning summary. This one is a little subtle, and I want to be careful about how I describe it, because there is a right way and a wrong way to ask a model to explain itself.

@ "- Then provide a brief explanation of the key steps"
We are not asking it to dump some hidden private chain of thought. We are asking for a short, friendly explanation of the key steps, the way a good tutor gives you the answer and then a quick why, so you actually walk away having learned something. The goal here is a clear, beginner-friendly answer, not a wall of text.

@ "## Answer"
Format keeps it tidy, answer first, then the brief explanation, then an example. And that is our whole toolkit of prompt builders done. But notice, right now these are just functions sitting in a file, returning strings. Nothing is calling them yet. So in the next lecture, we switch over to app dot py and start building the actual interface, the sidebar, the input box, and the wiring that turns a user's choice into one of these prompts.
