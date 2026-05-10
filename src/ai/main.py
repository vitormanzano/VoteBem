import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
from chat import tier_a, tier_b, router, comparison
from chat.formatting import normalize

RECUSA_OPINIAO = (
    "O VoteBem é estritamente informativo e não emite recomendações de voto. "
    "Posso comparar dados objetivos dos candidatos para você."
)
FORA_ESCOPO = (
    "Só posso responder perguntas sobre os candidatos à Presidência do Brasil "
    "entre 2010 e 2022."
)

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
    ref: int | None = None
    sq_candidato: int | None = None
    nome: str | None = None
    ano: int | None = None
    trecho: str | None = None


class ChatResponse(BaseModel):
    resposta: str
    fontes: list[Fonte] = []
    categoria: str | None = None


class CompararRequest(BaseModel):
    sq_candidatos: list[int] = Field(..., min_length=2, max_length=4)
    temas: list[str] | None = None


class TemaComparado(BaseModel):
    tema: str
    texto: str
    candidatos_sem_proposta: list[str] = []


class CandidatoResumido(BaseModel):
    sq_candidato: int
    nome: str
    ano: int | None = None
    temas_disponiveis: list[str] = []


class CompararResponse(BaseModel):
    candidatos: list[CandidatoResumido]
    comparacoes: list[TemaComparado]


@app.get("/health")
def health():
    return {"status": "ok", "model": config.GROQ_MODEL}


@app.post("/ai/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        categoria = router.classify(req.pergunta)

        if categoria == "recusar":
            return ChatResponse(resposta=RECUSA_OPINIAO, categoria=categoria)

        if categoria == "fora_escopo":
            return ChatResponse(resposta=FORA_ESCOPO, categoria=categoria)

        if categoria == "proposta":
            resposta, fontes = tier_b.run(req.pergunta)
            return ChatResponse(
                resposta=normalize(resposta, max_ref_citacao=len(fontes)),
                fontes=[Fonte(**f) for f in fontes],
                categoria=categoria,
            )

        resposta = tier_a.run(req.pergunta)
        return ChatResponse(resposta=normalize(resposta), fontes=[], categoria=categoria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/propostas/comparar", response_model=CompararResponse)
def comparar(req: CompararRequest):
    temas = req.temas or config.TEMAS
    invalidos = [t for t in temas if t not in config.TEMAS]
    if invalidos:
        raise HTTPException(
            status_code=400,
            detail=f"Temas inválidos: {invalidos}. Válidos: {config.TEMAS}",
        )
    try:
        candidatos, comparacoes = comparison.comparar(req.sq_candidatos, temas)
        # normaliza valores monetários e datas em cada bloco da comparação
        comparacoes = [
            {**c, "texto": normalize(c.get("texto", ""))} for c in comparacoes
        ]
        return CompararResponse(
            candidatos=[CandidatoResumido(**c) for c in candidatos],
            comparacoes=[TemaComparado(**c) for c in comparacoes],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
