from fastapi import FastAPI
from pydantic import BaseModel

from raglab.gateway import LLMResonse
from raglab.gateway.factory import get_provider
from raglab.config import settings

app = FastAPI(title="RAGLab")


class GenerateRequest(BaseModel):
    provider: str 
    model: str = settings.default_model
    prompt: str 

@app.post("/generate", response_model=LLMResonse)
def generate(request: GenerateRequest) -> LLMResonse:
    raise NotImplementedError