from fastapi import FastAPI
import uvicorn

from app.prompt.cohere import Prompt


app = FastAPI()
prompt = Prompt()

app.include_router(prompt.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
