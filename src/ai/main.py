import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
from chat import tier_a

app = FastAPI(title="VoteBem AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    pergunta: str = Field(..., min_length=1, max_length=2000)


class Fonte(BaseModel):
    sq_candidato: int | None = None
    nome: str | None = None
    ano: int | None = None
    trecho: str | None = None


class ChatResponse(BaseModel):
    resposta: str
    fontes: list[Fonte] = []


@app.get("/health")
def health():
    return {"status": "ok", "model": config.GROQ_MODEL}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        resposta = tier_a.run(req.pergunta)
        return ChatResponse(resposta=resposta, fontes=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
