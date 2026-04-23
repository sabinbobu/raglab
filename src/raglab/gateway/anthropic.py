from .base import LLMProvider, LLMResponse

class AnthropicProvider:
    def __init__(self, api_key: str):
        self.client = None # Anthropic client will go here
        raise NotImplementedError

    def generate(self, prompt: str, model: str) -> LLMResponse:
        raise NotImplementedError