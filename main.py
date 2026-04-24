from fastapi import FastAPI
from pydantic import BaseModel

from raglab.config import settings
from raglab.gateway import LLMResponse
from raglab.gateway.factory import get_provider

app = FastAPI(title="RAGLab")


class GenerateRequest(BaseModel):
    provider: str
    model: str = settings.default_model
    prompt: str


@app.post("/generate", response_model=LLMResponse)
def generate(request: GenerateRequest) -> LLMResponse:
    provider = get_provider(request.provider)
    return provider.generate(request.prompt, request.model)