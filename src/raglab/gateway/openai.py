from .base import LLMProvider, LLMResponse

class OpenAIProvider:
    def __init__(self, api_key: str):
        self.client = None # OpenAI client will go here
        raise NotImplementedError

    def generate(self, prompt: str, model: str) -> LLMResponse:
        raise NotImplementedError