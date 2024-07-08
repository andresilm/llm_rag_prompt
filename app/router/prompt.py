from fastapi import APIRouter
from pydantic import Field, BaseModel
from starlette import status

from app.cohere_client import cohere_client
from app.prompt.cohere_prompt import CoherePrompt
from app.prompt.context import PromptContext

router = APIRouter(prefix='/cohere', tags=['Prompt'])

context = PromptContext(cohere_client)
prompt = CoherePrompt(cohere_client)


class PromptRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    question: str = Field(min_length=1)


@router.post('/', status_code=status.HTTP_200_OK)
async def ask_to_cohere(request: PromptRequest):

    relevant_chunk = context.get_context(request.question)
    return prompt.ask_question(request.question, relevant_chunk)
