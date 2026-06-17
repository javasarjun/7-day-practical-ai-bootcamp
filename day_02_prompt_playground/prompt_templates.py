def build_weak_prompt(task_type, user_input):
    return f"""
Do this task:

Task type: {task_type}

Input:
{user_input}
"""


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
- Point 3

## Key Takeaway
One sentence takeaway.
"""

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
- Make the email easy to read

User request:
{user_input}

Output format:
Subject: ...

Email:
...
"""

    if task_type == "Research":
        return f"""
You are a research assistant.

Your task:
Create a research brief based on the topic provided.

Rules:
- Explain the topic clearly
- Organize the answer into sections
- Mention assumptions if information is uncertain
- Include practical implications
- Do not pretend to have real-time data unless provided

Topic:
{user_input}

Output format:
## Overview
## Key Points
## Practical Use Cases
## Risks or Limitations
## Final Summary
"""

    if task_type == "Content Generation":
        return f"""
You are a content strategist.

Your task:
Create content based on the user's topic.

Rules:
- Make the content engaging
- Use a clear hook
- Keep the structure easy to follow
- Avoid generic filler
- Make it useful for beginners

Topic:
{user_input}

Output format:
## Hook
## Main Content
## Example
## Closing
"""

    if task_type == "Coding Help":
        return f"""
You are a coding tutor.

Your task:
Explain or solve the coding question in a beginner-friendly way.

Rules:
- Explain the concept first
- Provide clean code if needed
- Add comments inside the code
- Explain the code after the example
- Mention common mistakes

Question:
{user_input}

Output format:
## Concept
## Code Example
## Explanation
## Common Mistakes
"""

    if task_type == "Structured JSON Output":
        return f"""
You are a structured data extraction assistant.

Your task:
Extract information from the user's text and return only valid JSON.

Rules:
- Return only JSON
- Do not include markdown
- Do not include explanation
- If a field is missing, use an empty string
- Make sure the JSON is valid

Text:
{user_input}

JSON format:
{{
  "title": "",
  "summary": "",
  "main_points": [],
  "action_items": [],
  "sentiment": ""
}}
"""

    return f"""
You are a helpful AI assistant.

Task:
{task_type}

Input:
{user_input}

Give a clear and useful response.
"""


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
