"""
Web search tool used by the Research Agent.

Uses the free `ddgs` (DuckDuckGo Search) package — no API key required. Falls back to a
clearly-labelled mock result if the network/package is unavailable, so the pipeline never
crashes and always produces a demonstrable result.
"""


def search_web(query: str, max_results: int = 5):
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))

        results = [
            {
                "title": r.get("title", "Untitled"),
                "body": r.get("body", ""),
                "href": r.get("href", ""),
            }
            for r in raw_results
        ]
        if results:
            return results
    except Exception as exc:
        print(f"[web_search] Live search unavailable ({exc}); using mock result.")

    return [
        {
            "title": "Mock Search Result",
            "body": (
                f"Simulated search snippet for query: '{query}'. "
                "No live internet/search backend was available for this run."
            ),
            "href": "https://example.com/mock-result",
        }
    ]
