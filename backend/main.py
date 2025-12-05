from fastapi import FastAPI
from pydantic import BaseModel


class AskRequest(BaseModel):
    prompt: str


class AskResponse(BaseModel):
    reply: str


app = FastAPI(title="KL1KK0 Backend", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest) -> AskResponse:
    # TODO: integrate LLM + retrieval + tools
    return AskResponse(
        reply=f'Stub: received "{payload.prompt}". Wire this endpoint to the LLM stack.'
    )
