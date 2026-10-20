import json

from .base_agent import BaseAgent
from ..utils import extract_json

PLANNER_SYSTEM = """You are a Market Research Planner Agent inside a multi-agent research \
system. Your only job is to take a broad market/topic name and break it down into 5 to 6 \
specific, non-overlapping sub-research questions that together give full coverage of the \
market (size & growth, competitive landscape, trends, regulation/policy, challenges/risks, \
future outlook).

Respond with ONLY a JSON array of strings (the sub-questions). No markdown, no preamble, \
no explanation."""


class PlannerAgent(BaseAgent):
    name = "PlannerAgent"

    def run(self, topic: str) -> list[str]:
        self.log(f"Breaking down research topic: {topic}")

        user_prompt = (
            f"Market/topic: {topic}\n\n"
            "Return a JSON array of 5-6 specific sub-research questions covering this market."
        )

        mock_fallback = json.dumps([
            f"What is the current market size and growth rate (CAGR) of the {topic}?",
            f"Who are the key players and what is the competitive landscape in the {topic}?",
            f"What are the major technology and product trends shaping the {topic}?",
            f"What government policies, subsidies, or regulations impact the {topic}?",
            f"What are the key challenges, risks, and barriers to adoption in the {topic}?",
            f"What is the growth forecast and future outlook for the {topic} over the next 5 years?",
        ])

        raw = self.llm.complete(PLANNER_SYSTEM, user_prompt, mock_fallback=mock_fallback)

        try:
            questions = extract_json(raw)
            if not isinstance(questions, list):
                raise ValueError("Expected a JSON list")
        except Exception:
            questions = [line.strip("-* ").strip() for line in raw.split("\n") if line.strip()]

        self.log(f"Generated {len(questions)} sub-questions")
        return questions
