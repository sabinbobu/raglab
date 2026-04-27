from fastapi import FastAPI
from pydantic import BaseModel

from raglab.config import settings
from raglab.gateway import LLMResponse

app = FastAPI(title="RAGLab")


class GenerateRequest(BaseModel):
    provider: str
    model: str = settings.default_model
    prompt: str


@app.post("/generate", response_model=LLMResponse)
def generate(request: GenerateRequest) -> LLMResponse:
    raise NotImplementedError
