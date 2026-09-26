import streamlit as st

from research_agent import ResearchAgent


st.set_page_config(
    page_title="Day 5 Research Agent",
    page_icon="🕵️",
    layout="wide",
)

st.title("🕵️ Day 5: Autonomous Research Agent")
st.write(
    "Enter a topic and let the agent plan, search, analyze, write, review, and save a research report."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Agent Workflow")
st.sidebar.write(
    """
This agent follows a simple workflow:

1. Plan  
2. Search  
3. Analyze  
4. Write  
5. Review  
6. Save  
"""
)

st.sidebar.markdown("---")
st.sidebar.subheader("Beginner Note")
st.sidebar.write(
    """
This lab uses a local sample search tool instead of live web search.

That keeps the lab reliable and easy to run. Later, this tool can be replaced with a real search API.
"""
)


# -----------------------------
# Input
# -----------------------------

topic = st.text_input(
    "Enter a research topic",
    placeholder="Example: How can small businesses use AI for customer support?",
)

run_agent = st.button("Run Research Agent", type="primary")


# -----------------------------
# Run Agent
# -----------------------------

if run_agent:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Agent is working..."):
            agent = ResearchAgent(topic.strip())
            result = agent.run()

        st.success("Research agent completed the task.")

        # -----------------------------
        # Agent Steps
        # -----------------------------

        st.subheader("Agent Steps")

        for step in result["steps"]:
            st.write(f"✅ **{step['step']}** — {step['details']}")

        # -----------------------------
        # Research Plan
        # -----------------------------

        with st.expander("View Research Plan"):
            st.markdown(result["plan"])

        # -----------------------------
        # Sources
        # -----------------------------

        with st.expander("View Retrieved Sources"):
            for index, source in enumerate(result["sources"], start=1):
                st.markdown(f"### Source {index}: {source['title']}")
                st.write(f"Source: {source['source']}")
                st.write(f"URL: {source['url']}")
                st.write(f"Search Score: {source.get('score', 'N/A')}")
                st.write(source["content"])

        # -----------------------------
        # Findings
        # -----------------------------

        with st.expander("View Source Analysis"):
            st.markdown(result["findings"])

        # -----------------------------
        # Final Report
        # -----------------------------

        st.subheader("Final Research Report")
        st.markdown(result["final_report"])

        # -----------------------------
        # Download
        # -----------------------------

        st.download_button(
            label="Download Research Report",
            data=result["final_report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

        st.caption(f"Report saved locally at: {result['file_path']}")


# -----------------------------
# Teaching Note
# -----------------------------

st.markdown("---")
st.caption(
    "Day 5 Lab: This is a beginner-friendly agent. The search tool is local/mock, not live internet search."
)
