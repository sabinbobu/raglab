from .base import LLMProvider


def get_provider(name: str) -> LLMProvider:
    raise NotImplementedError
