import json
import os
import time

from .agents.analyst_agent import AnalystAgent
from .agents.critic_agent import CriticAgent
from .agents.planner_agent import PlannerAgent
from .agents.research_agent import ResearchAgent
from .agents.writer_agent import WriterAgent
from .llm_client import LLMClient
from .utils import slugify


class ResearchOrchestrator:
    """Coordinates the Planner -> Research -> Analyst -> Writer -> Critic agent pipeline
    and owns the shared run state / trace."""

    MAX_REVISIONS = 2

    def __init__(self, topic: str, verbose: bool = True, use_critic: bool = True):
        self.topic = topic
        self.verbose = verbose
        self.use_critic = use_critic

        llm = LLMClient()
        self.planner = PlannerAgent(llm, verbose)
        self.researcher = ResearchAgent(llm, verbose)
        self.analyst = AnalystAgent(llm, verbose)
        self.writer = WriterAgent(llm, verbose)
        self.critic = CriticAgent(llm, verbose)

        self.state = {
            "topic": topic,
            "sub_questions": [],
            "findings": [],
            "analysis": {},
            "report": "",
            "revisions": 0,
        }

    def log(self, message: str):
        if self.verbose:
            print(f"[Orchestrator] {message}")

    def run(self, output_dir: str = "outputs") -> str:
        start = time.time()
        self.log(f"Starting research pipeline for: '{self.topic}'")

        # 1. Plan
        self.state["sub_questions"] = self.planner.run(self.topic)

        # 2. Research each sub-question
        findings = []
        for question in self.state["sub_questions"]:
            findings.append(self.researcher.run(question))
        self.state["findings"] = findings

        # 3. Analyze
        self.state["analysis"] = self.analyst.run(self.topic, findings)

        # 4. Write
        report = self.writer.run(self.topic, self.state["analysis"])

        # 5. Critique & revise loop
        if self.use_critic:
            for _ in range(self.MAX_REVISIONS):
                verdict = self.critic.run(report)
                if verdict.get("approved", True):
                    break
                report = self.writer.run(self.topic, self.state["analysis"], revision_feedback=verdict.get("feedback"))
                self.state["revisions"] += 1

        self.state["report"] = report

        # 6. Persist
        os.makedirs(output_dir, exist_ok=True)
        slug = slugify(self.topic)
        report_path = os.path.join(output_dir, f"{slug}_report.md")
        trace_path = os.path.join(output_dir, f"{slug}_trace.json")

        with open(report_path, "w") as f:
            f.write(report)
        with open(trace_path, "w") as f:
            json.dump(self.state, f, indent=2)

        elapsed = round(time.time() - start, 1)
        self.log(f"Report saved to {report_path} ({elapsed}s, {self.state['revisions']} revision(s))")

        return report_path
