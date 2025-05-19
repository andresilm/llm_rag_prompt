from fastapi import APIRouter
from pydantic import Field, BaseModel
from starlette import status

from app.cohere_client import cohere_client
from app.prompt.cohere import Cohere
from app.prompt.context import PromptContext
from app.prompt.local_llm import LocalLMStudioLLM

router = APIRouter(prefix='/prompt', tags=['Prompt'])

context = PromptContext(cohere_client)
prompt = LocalLMStudioLLM(model='llama-3-8b-spanish-rag-v2.1', port=1234)


class PromptRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    question: str = Field(min_length=1)


@router.post('/', status_code=status.HTTP_200_OK)
async def ask_to_cohere(request: PromptRequest):
    relevant_chunk = context.get_context(request.question)
    return prompt.ask_question(request.question, relevant_chunk)
