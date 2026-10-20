from benchmarks.run_benchmark import benchmark_runtime, evaluate_citations, evaluate_sections


def test_citation_validity_is_reproducible():
    result = evaluate_citations()
    assert result["passed"] == 9
    assert result["total"] == 10
    assert result["score_percent"] == 90.0


def test_section_completeness_is_reproducible():
    result = evaluate_sections()
    assert result["passed"] == 20
    assert result["total"] == 23
    assert result["score_percent"] == 87.0


def test_offline_pipeline_average_is_under_three_minutes():
    result = benchmark_runtime(runs=3)
    assert result["under_three_minutes"] is True
    assert result["average_seconds"] < 180
