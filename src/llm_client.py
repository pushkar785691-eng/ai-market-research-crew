"""
Thin wrapper around the Anthropic Messages API.

Design goal: every agent should be able to call `llm.complete(system, user, mock_fallback=...)`
and get a usable string back, whether or not an API key is configured. This lets the whole
multi-agent pipeline be demoed instantly with zero setup (MOCK_MODE), while still being a
real, working integration when ANTHROPIC_API_KEY is set.
"""

from . import config


class LLMClient:
    def __init__(self, model: str | None = None):
        self.model = model or config.CLAUDE_MODEL
        self.mock = config.MOCK_MODE
        self._client = None

        if not self.mock:
            try:
                import anthropic

                self._client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[LLMClient] Falling back to mock mode: {exc}")
                self.mock = True

    def complete(self, system: str, user: str, max_tokens: int = 2000, mock_fallback: str | None = None) -> str:
        """Call the model and return plain text. Falls back to `mock_fallback` (or a generic
        placeholder) when running without an API key so the pipeline always produces output."""

        if self.mock:
            return mock_fallback if mock_fallback is not None else (
                "[MOCK MODE] No ANTHROPIC_API_KEY configured — this is placeholder output. "
                "Set ANTHROPIC_API_KEY in .env to get real model responses."
            )

        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[LLMClient] API call failed ({exc}); using mock fallback for this step.")
            return mock_fallback if mock_fallback is not None else f"[ERROR] LLM call failed: {exc}"
