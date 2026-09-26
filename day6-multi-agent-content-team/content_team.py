import os
import re
from datetime import datetime

from llm_service import ask_ai
from knowledge_tool import search_knowledge
from agent_prompts import (
    build_planner_prompt,
    build_research_prompt,
    build_writer_prompt,
    build_editor_prompt,
    build_qa_prompt,
)


class ContentTeam:
    def __init__(self, topic, content_type, audience, tone, max_sources=4):
        self.topic = topic
        self.content_type = content_type
        self.audience = audience
        self.tone = tone
        self.max_sources = max_sources

        self.state = {
            "topic": topic,
            "content_type": content_type,
            "audience": audience,
            "tone": tone,
            "steps": [],
        }

    def log_step(self, agent_name, details):
        self.state["steps"].append(
            {
                "agent": agent_name,
                "details": details,
            }
        )

    def call_agent(self, agent_name, prompt):
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are the {agent_name}. "
                    "You are part of a careful multi-agent content team. "
                    "Use only the provided information. "
                    "Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        return ask_ai(messages)

    def planner_agent(self):
        prompt = build_planner_prompt(
            topic=self.topic,
            content_type=self.content_type,
            audience=self.audience,
            tone=self.tone,
        )

        plan = self.call_agent("Planner Agent", prompt)
        self.state["plan"] = plan

        self.log_step(
            "Planner Agent", "Created content goal, outline, and research instructions.")
        return plan

    def researcher_agent(self, plan):
        sources = search_knowledge(self.topic, max_results=self.max_sources)

        prompt = build_research_prompt(
            topic=self.topic,
            plan=plan,
            sources=sources,
        )

        research_notes = self.call_agent("Research Agent", prompt)

        self.state["sources"] = sources
        self.state["research_notes"] = research_notes

        self.log_step(
            "Research Agent", f"Retrieved {len(sources)} sources and created research notes.")
        return sources, research_notes

    def writer_agent(self, plan, research_notes):
        prompt = build_writer_prompt(
            topic=self.topic,
            content_type=self.content_type,
            audience=self.audience,
            tone=self.tone,
            plan=plan,
            research_notes=research_notes,
        )

        draft = self.call_agent("Writer Agent", prompt)
        self.state["draft"] = draft

        self.log_step("Writer Agent", "Created first content draft.")
        return draft

    def editor_agent(self, draft):
        prompt = build_editor_prompt(
            topic=self.topic,
            content_type=self.content_type,
            audience=self.audience,
            tone=self.tone,
            draft=draft,
        )

        edited_content = self.call_agent("Editor Agent", prompt)
        self.state["edited_content"] = edited_content

        self.log_step("Editor Agent", "Improved clarity, structure, and flow.")
        return edited_content

    def qa_agent(self, edited_content, research_notes):
        prompt = build_qa_prompt(
            topic=self.topic,
            content_type=self.content_type,
            audience=self.audience,
            final_content=edited_content,
            research_notes=research_notes,
        )

        qa_review = self.call_agent("QA Agent", prompt)
        self.state["qa_review"] = qa_review

        self.log_step(
            "QA Agent", "Reviewed final content for quality and accuracy.")
        return qa_review

    def save_output(self, final_output):
        os.makedirs("outputs", exist_ok=True)

        safe_topic = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            self.topic.lower(),
        ).strip("_")

        safe_topic = safe_topic[:50] or "multi_agent_content"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"outputs/{safe_topic}_{timestamp}.md"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_output)

        self.state["file_path"] = file_path
        self.log_step("Save", f"Saved final output to {file_path}.")

        return file_path

    def run(self):
        plan = self.planner_agent()
        sources, research_notes = self.researcher_agent(plan)
        draft = self.writer_agent(plan, research_notes)
        edited_content = self.editor_agent(draft)
        qa_review = self.qa_agent(edited_content, research_notes)

        final_output = f"""
# Multi-Agent Content Output

## Topic

{self.topic}

---

# Final Edited Content

{edited_content}

---

# QA Review

{qa_review}
"""

        file_path = self.save_output(final_output)

        return {
            "topic": self.topic,
            "content_type": self.content_type,
            "audience": self.audience,
            "tone": self.tone,
            "plan": plan,
            "sources": sources,
            "research_notes": research_notes,
            "draft": draft,
            "edited_content": edited_content,
            "qa_review": qa_review,
            "final_output": final_output,
            "file_path": file_path,
            "steps": self.state["steps"],
        }
