import re
from collections import Counter


SAMPLE_SOURCES = [
    {
        "title": "AI in Education",
        "source": "Sample Knowledge Base",
        "url": "local://ai-in-education",
        "content": """
Artificial intelligence is being used in education to personalize learning,
generate practice questions, summarize lessons, support tutoring, and help
teachers save time. However, schools must consider student privacy, bias,
accuracy, and responsible use policies.
""",
    },
    {
        "title": "AI for Small Business",
        "source": "Sample Knowledge Base",
        "url": "local://ai-small-business",
        "content": """
Small businesses can use AI for customer support, marketing content,
sales emails, document automation, inventory forecasting, and business
analysis. The best use cases usually save time, reduce repetitive work,
or improve customer experience.
""",
    },
    {
        "title": "AI Agents Overview",
        "source": "Sample Knowledge Base",
        "url": "local://ai-agents-overview",
        "content": """
AI agents are systems that use a language model plus tools, memory, and
workflow logic to complete multi-step tasks. A simple agent can plan,
call tools, review results, and produce a final answer. Agents need
guardrails because they can make mistakes or take unnecessary steps.
""",
    },
    {
        "title": "Responsible AI Basics",
        "source": "Sample Knowledge Base",
        "url": "local://responsible-ai",
        "content": """
Responsible AI focuses on safety, fairness, transparency, privacy,
security, and human oversight. AI systems should avoid unsupported claims,
protect sensitive data, and make it clear when information is uncertain.
""",
    },
    {
        "title": "RAG and Knowledge Assistants",
        "source": "Sample Knowledge Base",
        "url": "local://rag-knowledge-assistants",
        "content": """
Retrieval-Augmented Generation, or RAG, improves AI answers by retrieving
relevant information from documents before generating a response. RAG is
useful for company knowledge bases, policy documents, manuals, training
material, and internal support tools.
""",
    },
    {
        "title": "AI in Customer Support",
        "source": "Sample Knowledge Base",
        "url": "local://ai-customer-support",
        "content": """
AI can improve customer support by answering common questions, routing
tickets, summarizing customer issues, suggesting replies, and helping
agents respond faster. Human review is important for complex, emotional,
or high-risk customer situations.
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


def search_sources(query, max_results=4):
    """
    Simple local search tool.

    This is not real web search.
    It ranks sample sources based on keyword overlap with the query.
    """

    query_terms = tokenize(query)
    query_counter = Counter(query_terms)

    scored_sources = []

    for source in SAMPLE_SOURCES:
        searchable_text = (
            source["title"] + " " + source["content"]
        )

        source_terms = tokenize(searchable_text)
        source_counter = Counter(source_terms)

        score = 0

        for term, count in query_counter.items():
            score += source_counter.get(term, 0) * count

        if score > 0:
            scored_sources.append(
                {
                    **source,
                    "score": score,
                }
            )

    scored_sources.sort(key=lambda item: item["score"], reverse=True)

    if not scored_sources:
        return SAMPLE_SOURCES[:max_results]

    return scored_sources[:max_results]
