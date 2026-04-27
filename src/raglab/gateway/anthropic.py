import time

from anthropic import Anthropic

from raglab.config import MODEL_PRICING
from raglab.gateway.base import LLMResponse


class AnthropicProvider:
    def __init__(self, api_key: str) -> None:
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, model: str) -> LLMResponse:
        start = time.perf_counter()

        response = self.client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        latency_ms = (time.perf_counter() - start) * 1000

        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
        cost_usd = (
            input_tokens * pricing["input"] + output_tokens * pricing["output"]
        ) / 1_000_000

        return LLMResponse(
            text=response.content[0].text or "",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            latency_ms=round(latency_ms, 2),
            model=model,
            provider="anthropic",
        )
