import re
from collections import Counter


SAMPLE_KNOWLEDGE = [
    {
        "title": "Practical AI Skills",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://practical-ai-skills",
        "content": """
Practical AI skills include prompt engineering, building AI applications,
working with APIs, using RAG, creating AI agents, evaluating outputs,
and understanding responsible AI. These skills are valuable for developers,
analysts, managers, students, and entrepreneurs.
""",
    },
    {
        "title": "AI Agents",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://ai-agents",
        "content": """
AI agents combine a language model with tools, workflow logic, memory,
and instructions. Agents can plan tasks, call tools, process results,
and produce final outputs. Good agents need guardrails and human oversight.
""",
    },
    {
        "title": "RAG Systems",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://rag-systems",
        "content": """
Retrieval-Augmented Generation helps AI systems answer using external
documents or knowledge bases. A RAG system usually extracts text, chunks it,
creates embeddings, retrieves relevant chunks, and sends context to the LLM.
""",
    },
    {
        "title": "Prompt Engineering",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://prompt-engineering",
        "content": """
Prompt engineering improves AI output by giving the model a clear role,
task, context, rules, examples, and output format. Strong prompts reduce
vague answers and make responses more reliable and useful.
""",
    },
    {
        "title": "AI for Business Productivity",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://ai-business-productivity",
        "content": """
Businesses can use AI to summarize documents, draft emails, analyze feedback,
generate reports, support customer service, automate repetitive tasks,
and improve knowledge management.
""",
    },
    {
        "title": "Responsible AI",
        "source": "AI Bootcamp Knowledge Base",
        "url": "local://responsible-ai",
        "content": """
Responsible AI focuses on privacy, safety, fairness, security, transparency,
and human oversight. AI systems should avoid unsupported claims, protect
sensitive information, and clearly communicate uncertainty.
""",
    },
]


STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "what", "how", "why",
    "can", "are", "use", "using", "into", "from", "about", "will",
    "should", "could", "would", "have", "has", "was", "were", "you",
    "your", "their", "they", "them", "our", "its", "is", "to", "of",
    "in", "on", "a", "an"
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return [
        word
        for word in words
        if len(word) > 2 and word not in STOP_WORDS
    ]


def search_knowledge(query, max_results=4):
    """
    Simple local knowledge search tool.

    For Day 6, this keeps the lab stable.
    Later, this can be replaced with real web search, RAG, or an API.
    """

    query_terms = tokenize(query)
    query_counter = Counter(query_terms)

    scored_items = []

    for item in SAMPLE_KNOWLEDGE:
        searchable_text = item["title"] + " " + item["content"]
        source_terms = tokenize(searchable_text)
        source_counter = Counter(source_terms)

        score = 0

        for term, count in query_counter.items():
            score += source_counter.get(term, 0) * count

        if score > 0:
            scored_items.append(
                {
                    **item,
                    "score": score,
                }
            )

    scored_items.sort(key=lambda item: item["score"], reverse=True)

    if not scored_items:
        return SAMPLE_KNOWLEDGE[:max_results]

    return scored_items[:max_results]
