import json

from .base_agent import BaseAgent
from ..utils import extract_json

CRITIC_SYSTEM = """You are a Critic/QA Agent inside a multi-agent market research system. You \
review a draft market research report for completeness, structure, and quality. Respond with \
ONLY a JSON object: {"approved": true|false, "feedback": "..."}. Approve unless there is a \
clear, specific, fixable issue (e.g. a missing required section, or a section that is empty). \
Keep feedback short and actionable. Do not nitpick style."""


class CriticAgent(BaseAgent):
    name = "CriticAgent"

    def run(self, report_markdown: str) -> dict:
        self.log("Reviewing report quality")

        user_prompt = f"Draft report:\n\n{report_markdown}\n\nReview it now."

        mock_fallback = json.dumps({"approved": True, "feedback": ""})

        raw = self.llm.complete(CRITIC_SYSTEM, user_prompt, max_tokens=500, mock_fallback=mock_fallback)

        try:
            verdict = extract_json(raw)
        except Exception:
            verdict = {"approved": True, "feedback": ""}

        if verdict.get("approved"):
            self.log("✅ Report approved")
        else:
            self.log(f"✏️  Revision requested: {verdict.get('feedback', '')}")

        return verdict
