def build_research_plan_prompt(topic):
    return f"""
You are a research planning assistant.

Create a simple research plan for the topic below.

Topic:
{topic}

Rules:
- Keep it practical
- Create 4 to 6 research questions
- Mention what information should be collected
- Do not claim you already searched anything

Output format:

## Research Goal

## Key Questions

## Information Needed

## Expected Final Output
"""


def build_source_analysis_prompt(topic, sources):
    source_text = ""

    for index, source in enumerate(sources, start=1):
        source_text += f"""
Source {index}
Title: {source["title"]}
Source: {source["source"]}
URL: {source["url"]}
Content:
{source["content"]}
"""

    return f"""
You are a research analyst.

Your task:
Analyze the sources below for the research topic.

Research topic:
{topic}

Sources:
{source_text}

Rules:
- Use only the provided sources
- Do not invent facts
- Identify useful insights
- Mention limitations if sources are incomplete
- Keep the analysis clear and practical

Output format:

## Key Findings

## Useful Details

## Risks or Limitations

## Source Notes
"""


def build_report_prompt(topic, plan, findings, sources):
    source_list = ""

    for index, source in enumerate(sources, start=1):
        source_list += f"""
{index}. {source["title"]} — {source["source"]} — {source["url"]}
"""

    return f"""
You are a professional research report writer.

Write a clear research report using the research plan and findings below.

Research topic:
{topic}

Research plan:
{plan}

Findings:
{findings}

Sources:
{source_list}

Rules:
- Use only the information provided
- Do not invent statistics or citations
- Keep the report beginner-friendly
- Include a practical recommendations section
- Include the source list at the end

Output format:

# Research Report: {topic}

## Executive Summary

## Key Findings

## Practical Use Cases

## Risks and Limitations

## Recommendations

## Source List

## Final Takeaway
"""


def build_review_prompt(topic, report):
    return f"""
You are a careful report reviewer.

Review the research report below.

Topic:
{topic}

Report:
{report}

Check for:
- Clarity
- Unsupported claims
- Missing source references
- Practical usefulness
- Beginner-friendliness

Output format:

## Review Summary

## What Looks Good

## What Could Be Improved

## Safety or Accuracy Notes
"""
