"""Tier A — Tool calling para perguntas sobre dados estruturados (RF12).

O LLM recebe a lista de ferramentas, decide qual chamar com quais args,
recebe o resultado JSON, e formata a resposta final em pt-BR.
"""
import json

from llm import chat_completion
from chat.system_prompts import SYSTEM_PROMPT_BASE
from retrieval.tools import TOOL_FUNCTIONS

MAX_TOOL_ITERATIONS = 5

# Tool calling exige um modelo forte: o 8b erra a escolha de ferramenta e a
# interpretação do resultado (devolve R$ 0,00, conta errado, desiste cedo).
# Fixamos o 70b só aqui — são poucas chamadas, não pesa no rate limit do chat.
TIER_A_MODEL = "llama-3.3-70b-versatile"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_candidato_por_nome",
            "description": (
                "Busca candidaturas presidenciais por trecho de nome (urna ou civil). "
                "Use sempre que o usuário citar um candidato, para descobrir o sq_candidato "
                "antes de chamar outras ferramentas. Retorna até 20 resultados."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termo": {
                        "type": "string",
                        "description": "Trecho do nome do candidato (ex.: 'Lula', 'Marina', 'Ciro Gomes')",
                    }
                },
                "required": ["termo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_perfil",
            "description": (
                "Retorna dados pessoais e cadastrais de uma candidatura específica: "
                "nome, CPF, partido, ocupação, escolaridade, situação. Requer sq_candidato."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sq_candidato": {
                        "type": "integer",
                        "description": "Identificador da candidatura no TSE (obtenha via get_candidato_por_nome)",
                    }
                },
                "required": ["sq_candidato"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_bens",
            "description": (
                "Retorna patrimônio total declarado e composição por categoria de bens "
                "(imóveis, veículos, aplicações, etc.) para uma candidatura."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sq_candidato": {"type": "integer"},
                },
                "required": ["sq_candidato"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_situacao_juridica",
            "description": (
                "Retorna situação da candidatura, motivos de cassação e certidões "
                "criminais disponíveis para a candidatura."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sq_candidato": {"type": "integer"},
                },
                "required": ["sq_candidato"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_historico_eleitoral",
            "description": (
                "Retorna todas as candidaturas presidenciais (e votos por turno) "
                "de uma mesma pessoa, identificada pelo CPF. "
                "Use para perguntas tipo 'quantas vezes X concorreu'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nr_cpf_candidato": {
                        "type": "string",
                        "description": "CPF (11 dígitos, com ou sem pontuação)",
                    }
                },
                "required": ["nr_cpf_candidato"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_candidatos_por_ano",
            "description": (
                "Lista todos os candidatos PRESIDENTE de uma eleição (2010, 2014, 2018 ou 2022)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ano": {
                        "type": "integer",
                        "description": "Ano eleitoral (2010, 2014, 2018 ou 2022)",
                    }
                },
                "required": ["ano"],
            },
        },
    },
]


def _execute_tool_call(name: str, raw_args: str) -> str:
    """Executa a função e devolve string JSON pra colocar no message['content']."""
    try:
        args = json.loads(raw_args) if raw_args else {}
    except json.JSONDecodeError as e:
        return json.dumps({"erro": f"argumentos inválidos: {e}"}, ensure_ascii=False)

    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return json.dumps({"erro": f"função desconhecida: {name}"}, ensure_ascii=False)

    try:
        result = fn(**args)
    except TypeError as e:
        return json.dumps({"erro": f"argumentos inválidos para {name}: {e}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"erro": f"falha ao executar {name}: {e}"}, ensure_ascii=False)

    return json.dumps(result, ensure_ascii=False, default=str)


def run(pergunta: str) -> str:
    """Processa a pergunta com tool calling até obter resposta final."""
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT_BASE},
        {"role": "user", "content": pergunta},
    ]

    for _ in range(MAX_TOOL_ITERATIONS):
        completion = chat_completion(
            messages=messages,
            tools=TOOLS_SCHEMA,
            temperature=0.1,
            max_tokens=1024,
            model=TIER_A_MODEL,
        )
        msg = completion.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None) or []

        if not tool_calls:
            return (msg.content or "").strip()

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in tool_calls
            ],
        })

        for tc in tool_calls:
            content = _execute_tool_call(tc.function.name, tc.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": content,
            })

    # Se atingir o limite, força resposta final sem mais tools
    completion = chat_completion(
        messages=messages,
        tools=None,
        temperature=0.1,
        max_tokens=1024,
        model=TIER_A_MODEL,
    )
    return (completion.choices[0].message.content or "").strip()
