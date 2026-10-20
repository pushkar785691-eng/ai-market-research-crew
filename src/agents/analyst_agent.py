import json

from .base_agent import BaseAgent
from ..utils import extract_json

ANALYST_SYSTEM = """You are a Market Analyst Agent inside a multi-agent research system. You \
receive raw research findings (question + summarized bullet points) gathered by a Research \
Agent and must synthesize them into a single structured JSON object with these exact keys:

{
  "market_size_and_growth": "...",
  "key_players": ["...", "..."],
  "trends": ["...", "..."],
  "regulatory_factors": "...",
  "risks_and_challenges": ["...", "..."],
  "forecast": "...",
  "opportunities": ["...", "..."]
}

Respond with ONLY the JSON object. No markdown fences, no extra commentary."""


class AnalystAgent(BaseAgent):
    name = "AnalystAgent"

    def run(self, topic: str, findings: list[dict]) -> dict:
        self.log("Synthesizing findings into structured market analysis")

        findings_text = "\n\n".join(
            f"Q: {f['question']}\nFindings:\n{f['summary']}" for f in findings
        )

        user_prompt = f"Market/topic: {topic}\n\nResearch findings:\n{findings_text}\n\nSynthesize into the required JSON structure."

        mock_fallback = json.dumps({
            "market_size_and_growth": f"The {topic} shows a steady upward growth trajectory (mock data — set an API key for real figures).",
            "key_players": ["Player A", "Player B", "Player C"],
            "trends": ["Rising adoption of new technology", "Increasing consumer demand", "Growing investment"],
            "regulatory_factors": "Supportive government policy and incentive schemes (simulated).",
            "risks_and_challenges": ["Supply chain constraints", "Price sensitivity", "Infrastructure gaps"],
            "forecast": "Continued double-digit growth expected over the next 5 years (mock estimate).",
            "opportunities": ["Untapped regional markets", "Product innovation", "Strategic partnerships"],
        })

        raw = self.llm.complete(ANALYST_SYSTEM, user_prompt, max_tokens=1500, mock_fallback=mock_fallback)

        try:
            analysis = extract_json(raw)
        except Exception:
            analysis = json.loads(mock_fallback)

        return analysis
