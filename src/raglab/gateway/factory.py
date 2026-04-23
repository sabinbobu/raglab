from raglab.config import settings
from raglab.gateway.base import LLMProvider
from raglab.gateway.openai import OpenAIProvider
from raglab.gateway.anthropic import AnthropicProvider


def get_provider(name: str) -> LLMProvider:
    if name == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key)
    if name == "anthropic":
        return AnthropicProvider(api_key=settings.anthropic_api_key)
    raise ValueError(f"Unknown provider: {name!r}")