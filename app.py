"""
Streamlit UI for the Agentic Market Research System.

Run with:
    streamlit run app.py
"""

import streamlit as st

from src.agents.analyst_agent import AnalystAgent
from src.agents.critic_agent import CriticAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.research_agent import ResearchAgent
from src.agents.writer_agent import WriterAgent
from src.llm_client import LLMClient
from src.config import MOCK_MODE

st.set_page_config(page_title="Agentic Market Research", page_icon="🤖", layout="wide")

st.title("🤖 Agentic Market Research System")
st.caption("Multiple specialized AI agents collaborate to research a market and generate a structured report.")

if MOCK_MODE:
    st.info("Running in **mock mode** (no ANTHROPIC_API_KEY set) — output is illustrative placeholder text. Add a key in `.env` for live results.", icon="ℹ️")

topic = st.text_input("Market / topic to research", value="Electric Two-Wheeler Market in India")
use_critic = st.checkbox("Enable Critic Agent revision loop", value=True)
run_button = st.button("🚀 Run Research Pipeline", type="primary")

if run_button and topic.strip():
    llm = LLMClient()
    planner, researcher, analyst, writer, critic = (
        PlannerAgent(llm, verbose=False),
        ResearchAgent(llm, verbose=False),
        AnalystAgent(llm, verbose=False),
        WriterAgent(llm, verbose=False),
        CriticAgent(llm, verbose=False),
    )

    with st.status("Running multi-agent pipeline...", expanded=True) as status:
        st.write("🧭 **Planner Agent** — breaking topic into sub-questions...")
        sub_questions = planner.run(topic)
        st.write(sub_questions)

        st.write("🔎 **Research Agent** — gathering findings for each sub-question...")
        findings = []
        progress = st.progress(0)
        for i, q in enumerate(sub_questions):
            findings.append(researcher.run(q))
            progress.progress((i + 1) / len(sub_questions))
        with st.expander("Show raw findings"):
            for f in findings:
                st.markdown(f"**{f['question']}**\n\n{f['summary']}")

        st.write("📊 **Analyst Agent** — synthesizing structured insights...")
        analysis = analyst.run(topic, findings)
        st.json(analysis)

        st.write("✍️ **Writer Agent** — drafting the report...")
        report = writer.run(topic, analysis)

        if use_critic:
            st.write("🧐 **Critic Agent** — reviewing report quality...")
            for _ in range(2):
                verdict = critic.run(report)
                if verdict.get("approved", True):
                    st.write("✅ Report approved")
                    break
                st.write(f"✏️ Revision requested: {verdict.get('feedback')}")
                report = writer.run(topic, analysis, revision_feedback=verdict.get("feedback"))

        status.update(label="Pipeline complete!", state="complete")

    st.divider()
    st.subheader("📄 Final Report")
    st.markdown(report)
    st.download_button("⬇️ Download Report (.md)", report, file_name="market_research_report.md")
