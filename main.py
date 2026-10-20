#!/usr/bin/env python3
"""
Agentic Market Research System — CLI entry point.

Usage:
    python main.py --topic "Electric Two-Wheeler Market in India"
    python main.py --topic "Global Plant-Based Meat Market" --no-critic
"""

import argparse

from src.orchestrator import ResearchOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Run the multi-agent market research pipeline.")
    parser.add_argument(
        "--topic",
        type=str,
        default="Electric Two-Wheeler Market in India",
        help="The market/topic to research.",
    )
    parser.add_argument("--output", type=str, default="outputs", help="Output directory for the report.")
    parser.add_argument("--no-critic", action="store_true", help="Skip the critic/revision loop.")
    parser.add_argument("--quiet", action="store_true", help="Suppress agent progress logs.")
    args = parser.parse_args()

    orchestrator = ResearchOrchestrator(
        topic=args.topic,
        verbose=not args.quiet,
        use_critic=not args.no_critic,
    )
    report_path = orchestrator.run(output_dir=args.output)

    print("\n" + "=" * 60)
    print(f"Done. Report saved to: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
