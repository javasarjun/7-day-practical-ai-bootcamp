import json
import os
from datetime import datetime

import streamlit as st

from llm_service import ask_ai
from prompt_templates import (
    build_weak_prompt,
    build_strong_prompt,
    build_role_prompt,
    build_reasoning_summary_prompt,
)


PROMPT_LIBRARY_FILE = "prompt_library.json"


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


def load_prompt_library():
    if not os.path.exists(PROMPT_LIBRARY_FILE):
        return []

    try:
        with open(PROMPT_LIBRARY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_prompt_to_library(name, task_type, prompt):
    library = load_prompt_library()

    library.append(
        {
            "name": name,
            "task_type": task_type,
            "prompt": prompt,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    with open(PROMPT_LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(library, file, indent=2)


# -----------------------------
# Sidebar
# -----------------------------

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

st.sidebar.markdown("---")
st.sidebar.subheader("Prompt Settings")

temperature_style = st.sidebar.selectbox(
    "Response Style",
    ["Balanced", "Creative", "Precise"],
)

if temperature_style == "Creative":
    style_instruction = "Be creative and engaging."
elif temperature_style == "Precise":
    style_instruction = "Be precise, concise, and factual."
else:
    style_instruction = "Balance clarity, usefulness, and detail."


# -----------------------------
# User Input
# -----------------------------

user_input = st.text_area(
    "Enter your text, topic, or request:",
    height=220,
    placeholder=(
        "Example: Summarize this article, write an email, "
        "explain this code, or research this topic..."
    ),
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


# -----------------------------
# Build Prompts
# -----------------------------

weak_prompt = ""
strong_prompt = ""
reusable_prompt = ""

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

    # This converts the generated prompt into a reusable template.
    # Instead of saving the exact user input, we replace it with {user_input}.
    reusable_prompt = strong_prompt.replace(user_input, "{user_input}")


# -----------------------------
# Display Weak vs Strong Prompt
# -----------------------------

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


# -----------------------------
# Compare AI Responses
# -----------------------------

st.markdown("---")

run_button = st.button("Compare AI Responses", type="primary")

if run_button:
    if not user_input:
        st.warning("Please enter some input first.")
    else:
        weak_messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": weak_prompt,
            },
        ]

        strong_messages = [
            {
                "role": "system",
                "content": "You are a helpful, reliable, and practical AI assistant.",
            },
            {
                "role": "user",
                "content": strong_prompt,
            },
        ]

        response_col1, response_col2 = st.columns(2)

        with response_col1:
            st.subheader("Response from Weak Prompt")

            with st.spinner("Generating weak prompt response..."):
                weak_response = ask_ai(weak_messages)
                st.markdown(weak_response)

        with response_col2:
            st.subheader("Response from Strong Prompt")

            with st.spinner("Generating strong prompt response..."):
                strong_response = ask_ai(strong_messages)
                st.markdown(strong_response)


# -----------------------------
# Save Prompt to Library
# -----------------------------

st.markdown("---")
st.subheader("Save Prompt to Library")

st.write(
    "You can save the strong prompt as a reusable template. "
    "The app replaces your test input with `{user_input}`."
)

prompt_name = st.text_input(
    "Prompt Name",
    placeholder="Example: Professional Email Writer Prompt",
)

prompt_to_save = st.text_area(
    "Prompt to Save",
    value=reusable_prompt,
    height=320,
    placeholder="Generate a strong prompt first or paste your own reusable prompt here...",
)

if st.button("Save Prompt"):
    if not prompt_to_save.strip():
        st.warning("Please enter or generate a prompt before saving.")
    elif not prompt_name.strip():
        st.warning("Please enter a prompt name.")
    else:
        save_prompt_to_library(
            prompt_name.strip(),
            task_type,
            prompt_to_save.strip(),
        )
        st.success("Prompt saved to prompt_library.json")


# -----------------------------
# Display Saved Prompt Library
# -----------------------------

st.markdown("---")
st.subheader("Saved Prompt Library")

library = load_prompt_library()

if library:
    for index, item in enumerate(library, start=1):
        with st.expander(f"{index}. {item['name']} — {item['task_type']}"):
            st.caption(f"Created at: {item.get('created_at', 'N/A')}")
            st.code(item["prompt"], language="text")
else:
    st.info("No prompts saved yet.")

# -----------------------------
# Use Saved Prompt
# -----------------------------

st.markdown("---")
st.subheader("Use a Saved Prompt")

library = load_prompt_library()

if library:
    prompt_options = [
        f"{index + 1}. {item['name']} — {item['task_type']}"
        for index, item in enumerate(library)
    ]

    selected_prompt_label = st.selectbox(
        "Choose a saved prompt",
        prompt_options
    )

    selected_index = prompt_options.index(selected_prompt_label)
    selected_prompt = library[selected_index]["prompt"]

    st.write("Selected prompt template:")
    st.code(selected_prompt, language="text")

    saved_prompt_input = st.text_area(
        "Enter input for this saved prompt",
        height=180,
        placeholder="Example: Explain Python functions to a beginner."
    )

    if st.button("Run Saved Prompt"):
        if not saved_prompt_input.strip():
            st.warning("Please enter input for the saved prompt.")
        else:
            final_prompt = selected_prompt.replace(
                "{user_input}",
                saved_prompt_input.strip()
            )

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful, reliable, and practical AI assistant."
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]

            st.subheader("Final Prompt Sent to AI")
            st.code(final_prompt, language="text")

            st.subheader("AI Response")

            with st.spinner("Running saved prompt..."):
                response = ask_ai(messages)
                st.markdown(response)
else:
    st.info("Save at least one prompt before using the saved prompt runner.")
