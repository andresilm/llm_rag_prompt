from fastapi import APIRouter
from pydantic import Field, BaseModel
from starlette import status

from app.main import prompt

router = APIRouter(prefix='/prompt', tags=['Users'])


class PromptRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    question: str = Field(min_length=1)


@router.post('/', status_code=status.HTTP_200_OK)
async def ask_question(request: PromptRequest):
    prompt.ask_question(request.question)
