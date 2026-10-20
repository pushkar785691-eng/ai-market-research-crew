# Reproducible Benchmark Results

Run `python benchmarks/run_benchmark.py --write` from the repository root to regenerate these results.

| Metric | Result | Reproducible basis |
|---|---:|---|
| Citation validity | **90%** (9/10) | Human-audited claim/source pairs marked supported, with evidence notes and a valid HTTPS source URL. |
| Section completeness | **87%** (20/23) | Required report elements present in the checked-in sample, using a versioned 23-item rubric. |
| Average report runtime | **0.0013 seconds** | 3 deterministic offline runs; under 3 minutes: **True** |

## Transparency notes

- Citation 10 is intentionally recorded as unresolved because the candidate forecasts use incompatible scopes and base years. The audit therefore reports 9 valid claim/source pairs out of 10, not a perfect score.
- Completeness is 20 of 23 rubric items. The sample lacks dedicated Recommendations, Methodology, and Glossary sections; these gaps remain visible in `benchmarks/section_rubric.json`.
- Runtime covers the complete Planner → Research → Analyst → Writer → Critic orchestration path with deterministic fixtures. It validates orchestration performance, not internet or model-provider latency.
- The checked-in JSON result contains the precise machine-readable values used in this table.
