#!/usr/bin/env python3
"""Reproduce the portfolio metrics using only local, deterministic inputs."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_citations() -> dict:
    records = load_json(ROOT / "benchmarks" / "citation_audit.json")
    passed = []
    failed = []
    for record in records:
        parsed = urlparse(record["url"])
        structurally_valid = parsed.scheme == "https" and bool(parsed.netloc)
        audited = bool(record["supported"] and record["evidence"].strip() and structurally_valid)
        (passed if audited else failed).append(record["id"])
    return {
        "score_percent": round(100 * len(passed) / len(records), 1),
        "passed": len(passed),
        "total": len(records),
        "failed_ids": failed,
        "definition": "Human-audited claim/source pairs marked supported, with evidence notes and a valid HTTPS source URL.",
    }


def evaluate_sections() -> dict:
    report = (ROOT / "outputs" / "sample_report_ev_2wheeler.md").read_text(encoding="utf-8")
    criteria = load_json(ROOT / "benchmarks" / "section_rubric.json")
    passed = [item["id"] for item in criteria if item["needle"].casefold() in report.casefold()]
    failed = [item["id"] for item in criteria if item["id"] not in passed]
    return {
        "score_percent": round(100 * len(passed) / len(criteria), 1),
        "passed": len(passed),
        "total": len(criteria),
        "failed_ids": failed,
        "definition": "Required report elements present in the checked-in sample, using a versioned 23-item rubric.",
    }


def benchmark_runtime(runs: int = 3) -> dict:
    os.environ.pop("ANTHROPIC_API_KEY", None)
    from src import config
    from src.agents import research_agent
    from src.orchestrator import ResearchOrchestrator

    config.ANTHROPIC_API_KEY = ""
    config.MOCK_MODE = True

    def fixture_search(query: str, max_results: int = 5):
        return [{"title": "Benchmark fixture", "body": f"Deterministic evidence for {query}", "href": "https://example.com/benchmark"}]

    research_agent.search_web = fixture_search
    durations = []
    with tempfile.TemporaryDirectory(prefix=".benchmark-tmp-", dir=ROOT) as output_dir:
        for _ in range(runs):
            started = time.perf_counter()
            ResearchOrchestrator("Electric Two-Wheeler Market in India", verbose=False).run(output_dir)
            durations.append(time.perf_counter() - started)

    average = statistics.mean(durations)
    return {
        "average_seconds": round(average, 4),
        "runs": runs,
        "under_three_minutes": average < 180,
        "definition": "Average end-to-end orchestration runtime in deterministic offline mock mode; excludes external API and network latency.",
    }


def build_results(runs: int) -> dict:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "citation_validity": evaluate_citations(),
        "section_completeness": evaluate_sections(),
        "runtime": benchmark_runtime(runs),
    }


def markdown(results: dict) -> str:
    citation = results["citation_validity"]
    section = results["section_completeness"]
    runtime = results["runtime"]
    return f"""# Reproducible Benchmark Results

Run `python benchmarks/run_benchmark.py --write` from the repository root to regenerate these results.

| Metric | Result | Reproducible basis |
|---|---:|---|
| Citation validity | **{citation['score_percent']:.0f}%** ({citation['passed']}/{citation['total']}) | {citation['definition']} |
| Section completeness | **{section['score_percent']:.0f}%** ({section['passed']}/{section['total']}) | {section['definition']} |
| Average report runtime | **{runtime['average_seconds']:.4f} seconds** | {runtime['runs']} deterministic offline runs; under 3 minutes: **{runtime['under_three_minutes']}** |

## Transparency notes

- Citation 10 is intentionally recorded as unresolved because the candidate forecasts use incompatible scopes and base years. The audit therefore reports 9 valid claim/source pairs out of 10, not a perfect score.
- Completeness is 20 of 23 rubric items. The sample lacks dedicated Recommendations, Methodology, and Glossary sections; these gaps remain visible in `benchmarks/section_rubric.json`.
- Runtime covers the complete Planner → Research → Analyst → Writer → Critic orchestration path with deterministic fixtures. It validates orchestration performance, not internet or model-provider latency.
- The checked-in JSON result contains the precise machine-readable values used in this table.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=3, help="Number of runtime trials.")
    parser.add_argument("--write", action="store_true", help="Write results.json and BENCHMARKS.md.")
    args = parser.parse_args()
    results = build_results(args.runs)
    if args.write:
        (ROOT / "benchmarks" / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        (ROOT / "BENCHMARKS.md").write_text(markdown(results), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
