from fastapi import APIRouter
from pydantic import Field, BaseModel
from starlette import status

import cohere
from app.prompt.cohere import CoherePrompt, COHERE_API_KEY
from app.prompt.context import PromptContext

router = APIRouter(prefix='/cohere', tags=['Prompt'])
client = cohere.Client(COHERE_API_KEY)
context = PromptContext(client)


class PromptRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    question: str = Field(min_length=1)


@router.post('/', status_code=status.HTTP_200_OK)
async def ask_to_cohere(request: PromptRequest):
    prompt = CoherePrompt(client)
    relevant_chunk = context.get_context(request.question)
    return prompt.ask_question(request.question, relevant_chunk)
