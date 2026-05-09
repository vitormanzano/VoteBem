"""Roteador — classifica a pergunta e devolve uma das 4 categorias."""
import json
import re

from llm import chat_completion

ROUTER_SYSTEM = """Você classifica a pergunta do usuário em UMA destas categorias:

- "estruturado": perguntas sobre dados objetivos do candidato — perfil, partido, patrimônio, bens, ocupação, situação jurídica, certidões, cassações, votos obtidos, ano em que concorreu, listagem de candidatos por ano.
- "proposta": perguntas sobre propostas de governo, plano de governo, ideias do candidato sobre temas (saúde, educação, economia, segurança, meio ambiente etc.), comparação de propostas entre candidatos.
- "recusar": pedidos de opinião política, recomendação de voto, juízo de valor sobre candidatos ("quem é o melhor?").
- "fora_escopo": perguntas que não tratam de candidatos à Presidência do Brasil entre 2010 e 2022.

Responda APENAS um JSON minimal: {"categoria": "<uma das opções>"}.
Sem comentários, sem markdown, sem texto fora do JSON."""

_VALIDAS = {"estruturado", "proposta", "recusar", "fora_escopo"}


def classify(pergunta: str) -> str:
    completion = chat_completion(
        messages=[
            {"role": "system", "content": ROUTER_SYSTEM},
            {"role": "user", "content": pergunta},
        ],
        temperature=0.0,
        max_tokens=40,
    )
    raw = (completion.choices[0].message.content or "").strip()

    m = re.search(r"\{.*?\}", raw, flags=re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(0))
            cat = (data.get("categoria") or "").lower().strip()
            if cat in _VALIDAS:
                return cat
        except json.JSONDecodeError:
            pass

    return "estruturado"
