import streamlit as st

from content_team import ContentTeam


st.set_page_config(
    page_title="Day 6 Multi-Agent Content Team",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Day 6: Multi-Agent Content Team")
st.write(
    "Build content using a team of AI agents: Planner, Researcher, Writer, Editor, and QA."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Multi-Agent Workflow")
st.sidebar.write(
    """
This app uses a simple manual multi-agent workflow:

1. Planner Agent  
2. Research Agent  
3. Writer Agent  
4. Editor Agent  
5. QA Agent  
"""
)

st.sidebar.markdown("---")
st.sidebar.subheader("Teaching Point")
st.sidebar.write(
    """
A multi-agent system splits work across specialized agents.

Each agent has a role, receives input, produces output, and passes that output to the next agent.
"""
)

max_sources = st.sidebar.slider(
    "Max research sources",
    min_value=1,
    max_value=6,
    value=4,
)


# -----------------------------
# Inputs
# -----------------------------

topic = st.text_input(
    "Enter content topic",
    placeholder="Example: Why software developers should learn AI agents",
)

content_type = st.selectbox(
    "Choose content type",
    [
        "LinkedIn Post",
        "Blog Article",
        "Executive Brief",
        "YouTube Script",
        "Course Lesson Summary",
    ],
)

audience = st.selectbox(
    "Target audience",
    [
        "Beginners",
        "Software Developers",
        "Business Leaders",
        "Students",
        "Entrepreneurs",
        "Managers",
    ],
)

tone = st.selectbox(
    "Tone",
    [
        "Practical",
        "Beginner-Friendly",
        "Professional",
        "Persuasive",
        "Educational",
        "Conversational",
    ],
)


run_team = st.button("Run Multi-Agent Team", type="primary")


# -----------------------------
# Run Multi-Agent Team
# -----------------------------

if run_team:
    if not topic.strip():
        st.warning("Please enter a content topic.")
    else:
        with st.spinner("Multi-agent team is working..."):
            team = ContentTeam(
                topic=topic.strip(),
                content_type=content_type,
                audience=audience,
                tone=tone,
                max_sources=max_sources,
            )

            result = team.run()

        st.success("Multi-agent content team completed the task.")

        # -----------------------------
        # Agent Steps
        # -----------------------------

        st.subheader("Agent Execution Steps")

        for step in result["steps"]:
            st.write(f"✅ **{step['agent']}** — {step['details']}")

        # -----------------------------
        # Tabs
        # -----------------------------

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "Plan",
                "Research",
                "Draft",
                "Edited Content",
                "QA Review",
                "Final Output",
            ]
        )

        with tab1:
            st.subheader("Planner Agent Output")
            st.markdown(result["plan"])

        with tab2:
            st.subheader("Research Agent Output")
            st.markdown(result["research_notes"])

            st.markdown("---")
            st.subheader("Sources Used")

            for index, source in enumerate(result["sources"], start=1):
                with st.expander(f"Source {index}: {source['title']}"):
                    st.write(f"Source: {source['source']}")
                    st.write(f"URL: {source['url']}")
                    st.write(f"Search Score: {source.get('score', 'N/A')}")
                    st.write(source["content"])

        with tab3:
            st.subheader("Writer Agent Draft")
            st.markdown(result["draft"])

        with tab4:
            st.subheader("Editor Agent Output")
            st.markdown(result["edited_content"])

        with tab5:
            st.subheader("QA Agent Review")
            st.markdown(result["qa_review"])

        with tab6:
            st.subheader("Final Multi-Agent Output")
            st.markdown(result["final_output"])

            st.download_button(
                label="Download Final Content",
                data=result["final_output"],
                file_name="multi_agent_content.md",
                mime="text/markdown",
            )

            st.caption(f"Saved locally at: {result['file_path']}")


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")
st.caption(
    "Day 6 Lab: Beginner-friendly manual multi-agent workflow. No external framework required."
)
