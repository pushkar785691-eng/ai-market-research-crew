import json

from .base_agent import BaseAgent

WRITER_SYSTEM = """You are a Report Writer Agent inside a multi-agent market research system. \
You receive a structured JSON market analysis and must turn it into a polished, well-organized \
Markdown research report with these sections, in this order:

# <Topic> — Market Research Report
## Executive Summary
## Market Size & Growth
## Competitive Landscape
## Key Trends
## Regulatory & Policy Landscape
## Risks & Challenges
## Opportunities
## Forecast & Outlook
## Conclusion

Write in a professional, analytical tone suitable for an investor or business stakeholder. \
Respond with ONLY the Markdown report — no preamble."""


class WriterAgent(BaseAgent):
    name = "WriterAgent"

    def run(self, topic: str, analysis: dict, revision_feedback: str | None = None) -> str:
        self.log("Drafting structured research report" if not revision_feedback else "Revising report based on critic feedback")

        user_prompt = f"Market/topic: {topic}\n\nStructured analysis:\n{json.dumps(analysis, indent=2)}"
        if revision_feedback:
            user_prompt += f"\n\nA reviewer requested these revisions — address them:\n{revision_feedback}"

        mock_fallback = f"""# {topic} — Market Research Report

## Executive Summary
This report provides a structured overview of the {topic}, covering market size, competitive
landscape, trends, regulation, risks, and outlook. *(Mock mode — set ANTHROPIC_API_KEY for a
fully generated, data-grounded report.)*

## Market Size & Growth
{analysis.get('market_size_and_growth', 'N/A')}

## Competitive Landscape
{', '.join(analysis.get('key_players', []))}

## Key Trends
{chr(10).join('- ' + t for t in analysis.get('trends', []))}

## Regulatory & Policy Landscape
{analysis.get('regulatory_factors', 'N/A')}

## Risks & Challenges
{chr(10).join('- ' + r for r in analysis.get('risks_and_challenges', []))}

## Opportunities
{chr(10).join('- ' + o for o in analysis.get('opportunities', []))}

## Forecast & Outlook
{analysis.get('forecast', 'N/A')}

## Conclusion
The {topic} presents a promising growth opportunity, balanced by notable execution risks that
stakeholders should monitor closely.
"""

        report = self.llm.complete(WRITER_SYSTEM, user_prompt, max_tokens=3000, mock_fallback=mock_fallback)
        return report
