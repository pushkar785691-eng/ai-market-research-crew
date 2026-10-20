import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import extract_json, slugify
from src.agents.planner_agent import PlannerAgent
from src.agents.critic_agent import CriticAgent


class FakeLLM:
    """A stand-in LLM client that always returns the mock_fallback, so tests don't need
    network access or an API key."""

    mock = True

    def complete(self, system, user, max_tokens=2000, mock_fallback=None):
        return mock_fallback


def test_extract_json_plain():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_with_fences():
    raw = "```json\n[1, 2, 3]\n```"
    assert extract_json(raw) == [1, 2, 3]


def test_extract_json_with_preamble():
    raw = 'Sure, here you go:\n{"approved": true, "feedback": ""}'
    assert extract_json(raw) == {"approved": True, "feedback": ""}


def test_slugify():
    assert slugify("Electric Two-Wheeler Market in India") == "electric-two-wheeler-market-in-india"


def test_planner_agent_returns_list():
    agent = PlannerAgent(FakeLLM(), verbose=False)
    questions = agent.run("Electric Two-Wheeler Market in India")
    assert isinstance(questions, list)
    assert len(questions) >= 3


def test_critic_agent_default_approves():
    agent = CriticAgent(FakeLLM(), verbose=False)
    verdict = agent.run("# Some Report\n\nContent here.")
    assert verdict["approved"] is True
