from .base_agent import BaseAgent
from ..tools.web_search import search_web

RESEARCH_SYSTEM = """You are a Research Agent inside a multi-agent market research system. \
You are given a specific sub-research question plus raw web search snippets. Extract only \
the facts relevant to the question and summarize them as 3-5 concise bullet points. Mention \
the source name inline where relevant. If the snippets don't contain enough information, say \
so plainly rather than inventing numbers. Do not add commentary outside the bullet points."""


class ResearchAgent(BaseAgent):
    name = "ResearchAgent"

    def run(self, sub_question: str) -> dict:
        self.log(f"Researching: {sub_question}")

        results = search_web(sub_question, max_results=5)
        context = "\n".join(
            f"- {r['title']}: {r['body']} (Source: {r['href']})" for r in results
        )

        user_prompt = (
            f"Sub-question: {sub_question}\n\n"
            f"Search results:\n{context}\n\n"
            "Summarize the key factual findings relevant to this sub-question."
        )

        mock_fallback = (
            f"- Available data points to steady growth relevant to: '{sub_question}'.\n"
            "- Multiple simulated sources indicate increasing competitive activity and innovation.\n"
            "- (Mock mode: connect ANTHROPIC_API_KEY and internet access for live, grounded findings.)"
        )

        summary = self.llm.complete(RESEARCH_SYSTEM, user_prompt, mock_fallback=mock_fallback)
        return {"question": sub_question, "sources": results, "summary": summary}
