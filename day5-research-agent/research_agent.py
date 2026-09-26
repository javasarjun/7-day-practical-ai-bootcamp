import os
import re
from datetime import datetime

from llm_service import ask_ai
from search_tool import search_sources
from agent_prompts import (
    build_research_plan_prompt,
    build_source_analysis_prompt,
    build_report_prompt,
    build_review_prompt,
)


class ResearchAgent:
    def __init__(self, topic):
        self.topic = topic
        self.steps = []

    def log_step(self, step_name, details):
        self.steps.append(
            {
                "step": step_name,
                "details": details,
            }
        )

    def call_llm(self, prompt):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a careful, practical AI research agent. "
                    "Use only provided information. Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        return ask_ai(messages)

    def create_plan(self):
        prompt = build_research_plan_prompt(self.topic)
        plan = self.call_llm(prompt)

        self.log_step("Plan", "Created a research plan for the topic.")
        return plan

    def search(self):
        sources = search_sources(self.topic, max_results=4)

        self.log_step(
            "Search",
            f"Retrieved {len(sources)} local sample sources."
        )

        return sources

    def analyze_sources(self, sources):
        prompt = build_source_analysis_prompt(self.topic, sources)
        findings = self.call_llm(prompt)

        self.log_step("Analyze", "Analyzed retrieved sources.")
        return findings

    def write_report(self, plan, findings, sources):
        prompt = build_report_prompt(
            topic=self.topic,
            plan=plan,
            findings=findings,
            sources=sources,
        )

        report = self.call_llm(prompt)

        self.log_step("Write", "Generated research report.")
        return report

    def review_report(self, report):
        prompt = build_review_prompt(self.topic, report)
        review = self.call_llm(prompt)

        self.log_step("Review", "Reviewed report for clarity and accuracy.")
        return review

    def save_report(self, final_report):
        os.makedirs("reports", exist_ok=True)

        safe_topic = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            self.topic.lower()
        ).strip("_")

        safe_topic = safe_topic[:50] or "research_report"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"reports/{safe_topic}_{timestamp}.md"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_report)

        self.log_step("Save", f"Saved report to {file_path}.")

        return file_path

    def run(self):
        plan = self.create_plan()
        sources = self.search()
        findings = self.analyze_sources(sources)
        report = self.write_report(plan, findings, sources)
        review = self.review_report(report)

        final_report = f"""
{report}

---

# Agent Review Notes

{review}
"""

        file_path = self.save_report(final_report)

        return {
            "topic": self.topic,
            "plan": plan,
            "sources": sources,
            "findings": findings,
            "report": report,
            "review": review,
            "final_report": final_report,
            "file_path": file_path,
            "steps": self.steps,
        }
