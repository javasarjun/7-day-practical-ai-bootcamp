# Build the Playground UI

### Step 1 — The page shell
**File:** app.py
**Lang:** python
**StartLine:** 19

```python
st.set_page_config(
    page_title="Day 2 Prompt Engineering Playground",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Day 2: Prompt Engineering Playground")
st.write(
    "Test weak prompts, strong prompts, role-based prompts, "
    "structured outputs, and save reusable prompt templates."
)
```

**Walkthrough:**
@ "st.set_page_config("
Now let's switch over to app dot py and build something we can actually click. Every Streamlit app starts with set page config, and here is a rule worth remembering, this needs to be the very first Streamlit call in your file, before anything else draws to the screen. We give it a page title, that is the little name on the browser tab, an icon, and layout wide. That wide setting tells Streamlit to use the full width of the window instead of a narrow centered column. For a side-by-side comparison tool like ours, wide is exactly what we want.

@ "st.title("
Then title and write just drop a heading and a one-line description onto the page. Nothing fancy, but I want you to build this habit, get a skeleton on screen first. If you ran the app right this second, you would have a real, working page, just an empty one. Always get something rendering before you add any logic. It is so much easier to debug a page that already loads than to write a hundred lines and hope.

### Step 2 — The sidebar: choosing a task
**File:** app.py
**Lang:** python
**StartLine:** 63

```python
task_type = st.sidebar.selectbox(
    "Choose Prompt Type",
    [
        "Summarization",
        "Email Writing",
        "Research",
        "Content Generation",
        "Coding Help",
        "Structured JSON Output",
        "Role Prompting",
        "Reasoning Summary",
    ],
)
```

**Walkthrough:**
@ task_type = st.sidebar.selectbox
Now the controls. We tuck these into the sidebar, the panel on the left, so the main area stays clean for results. This first one is a selectbox, which is just a dropdown. And notice the dot sidebar sitting in the middle of the call, that is how you tell Streamlit, put this widget in the sidebar, not on the main page. Little detail, easy to forget.

@ "Summarization"
The second argument is the list of options, and look closely, these are not random. Every single one of these matches a branch we wrote inside build strong prompt last lecture, summarization, email writing, research, and so on, plus our two special modes at the bottom. This is a place to be careful, these strings have to stay exactly in sync with the function. One typo here, like a lowercase s, and that whole task silently falls through to the generic fallback. Bugs like that are sneaky because nothing crashes, you just get worse output.

@ task_type = st.sidebar.selectbox
And whatever the user picks lands in this variable, task type. I want you to think of this one value as the steering wheel for the entire app. It is what decides which prompt we build and, later, which template gets saved. We are going to lean on it everywhere.

### Step 3 — Response style as an instruction, not a setting
**File:** app.py
**Lang:** python
**StartLine:** 80

```python
response_style = st.sidebar.selectbox(
    "Response Style",
    ["Balanced", "Creative", "Precise"],
)

if response_style == "Creative":
    style_instruction = "Be creative and engaging."
elif response_style == "Precise":
    style_instruction = "Be precise, concise, and factual."
else:
    style_instruction = "Balance clarity, usefulness, and detail."
```

**Walkthrough:**
@ response_style = st.sidebar.selectbox
A second dropdown, this one for response style, balanced, creative, or precise. Now here is a really important teaching point, and it is a trap a lot of beginners fall into. You might assume this dropdown changes the model's temperature, that dial that controls randomness. It does not. We never pass a temperature to the model anywhere in this app.

@ "if response_style == "Creative":"
Instead, watch what we actually do. We translate the user's choice into a plain English sentence. Pick creative, and style instruction becomes, be creative and engaging. Pick precise, and it becomes, be precise, concise, and factual. And in a moment we will just staple that sentence onto the end of the prompt. So we are steering the model's behavior with words, not with parameters. Sit with that distinction for a second, instruction versus configuration, because it genuinely changes how you think about controlling these models. A huge amount of what feels like a setting is really just a well-placed sentence.

### Step 4 — User input and a control that appears only when needed
**File:** app.py
**Lang:** python
**StartLine:** 97

```python
user_input = st.text_area(
    "Enter your text, topic, or request:",
    height=220,
)

role = None

if task_type == "Role Prompting":
    role = st.selectbox(
        "Choose a role",
        [
            "Career Coach",
            "Senior Software Engineer",
            "Business Analyst",
            "Marketing Expert",
            "AI Tutor",
            "Product Manager",
        ],
    )
```

**Walkthrough:**
@ "user_input = st.text_area("
Next, the big input box where the user types their text, their topic, whatever they want to work on. We reach for text area here instead of text input because we want room for a whole paragraph, and that height of two twenty just makes it comfortably tall to type in.

@ "role = None"
Now watch this small but important pattern. We default role to None. Most of the time there is no role at all, so we set a safe default up front. That way the variable always exists, no matter which path the code takes next. Forgetting to do this is one of the most common sources of those, name is not defined, errors that trip up beginners.

@ "if task_type == "Role Prompting":"
And here is a really nice touch, conditional UI. This role dropdown only shows up when the user has actually picked role prompting. There is no reason to show a list of personas to someone who is doing a summarization. Revealing controls only when they are relevant is a small thing, but it is exactly what makes an app feel thoughtful instead of cluttered.

### Step 5 — Turning the user's choices into a prompt
**File:** app.py
**Lang:** python
**StartLine:** 126

```python
weak_prompt = ""
strong_prompt = ""

if user_input:
    weak_prompt = build_weak_prompt(task_type, user_input)

    if task_type == "Role Prompting":
        strong_prompt = build_role_prompt(role, user_input)
    elif task_type == "Reasoning Summary":
        strong_prompt = build_reasoning_summary_prompt(user_input)
    else:
        strong_prompt = build_strong_prompt(task_type, user_input)

    strong_prompt = strong_prompt + \
        f"\n\nStyle instruction: {style_instruction}"
```

**Walkthrough:**
@ "if user_input:"
Here is where the UI finally meets the builder functions we wrote last lecture. By the way, up at the top of the file we have imported them, from prompt templates import build weak prompt, build strong prompt, and the rest. And see how we initialized both prompts to empty strings just above? That is so they always exist even before anyone types. Then this guard, if user input, means we only bother building prompts once there is actually something to work with. No point generating anything for an empty box.

@ "weak_prompt = build_weak_prompt(task_type, user_input)"
The weak prompt is the easy one, a single call, every time. This is our baseline, the lazy version we are going to measure everything else against.

@ "if task_type == "Role Prompting":"
The strong prompt is where the real routing lives, and this if, elif, else is honestly the brain of the whole app. If they chose role prompting, we call build role prompt. If they chose reasoning summary, we call that builder. And for everything else, the six normal task types, we hand it to build strong prompt, which does its own branching inside. Notice the clean division of labor here, app dot py only decides which builder to call, and the builder handles all the messy details of what the prompt actually says. The UI routes, the templates construct. Keep those jobs separate and your code stays easy to change.

@ strong_prompt = strong_prompt
And finally, we tack on that style instruction we built a moment ago, the creative or precise sentence. We just append it to the end of the strong prompt. So both of the user's choices, the task type and the style, flow together into one finished prompt. Two dropdowns, one prompt.

### Step 6 — Showing weak and strong side by side
**File:** app.py
**Lang:** python
**StartLine:** 152

```python
col1, col2 = st.columns(2)

with col1:
    st.subheader("Weak Prompt")

    if weak_prompt:
        st.code(weak_prompt, language="text")
    else:
        st.info("Enter input to generate a weak prompt.")

with col2:
    st.subheader("Strong Prompt")

    if strong_prompt:
        st.code(strong_prompt, language="text")
    else:
        st.info("Enter input to generate a strong prompt.")
```

**Walkthrough:**
@ "col1, col2 = st.columns(2)"
Last piece for this lecture, let's actually show both prompts so the difference is right there in front of the user. St dot columns two splits the page into two equal halves and hands us back two column objects we can write into.

@ "with col1:"
This with col1 block sends everything indented underneath it into the left column. We put a subheader on top, and then the weak prompt itself.

@ "st.info("Enter input to generate a weak prompt.")"
And notice this little if, else. If we actually have a prompt, we show it. Otherwise we show a gentle hint telling the user to type something. Always handle the empty state. An app that shows a friendly message instead of a blank gap feels intentional and finished, and it quietly teaches the user what to do next.

@ "with col2:"
The right column is just the mirror image for the strong prompt. And there it is, our playground UI. The user picks a task and a style, types their input, and instantly sees the weak and the strong prompt built right next to each other. But notice what we have not done yet, we have not called the model even once. All we have done so far is build the prompts. In the next lecture, we will take these two prompts and actually send them off to be answered, so we can compare the responses.
