"""Testes do parsing de saída do router (chat/router.py).

Não testamos a chamada ao LLM (depende de cota e é não determinística),
apenas a robustez do extrator de categoria a partir da resposta crua
do modelo. O classifier é testado por integração no run_eval.py.
"""
import json
import re

from chat.router import _VALIDAS


def _extrai_categoria(raw: str) -> str:
    """Reproduz a lógica de classify() sem chamar o LLM."""
    m = re.search(r"\{.*?\}", raw, flags=re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(0))
            cat = (data.get("categoria") or "").lower().strip()
            if cat in _VALIDAS:
                return cat
        except json.JSONDecodeError:
            pass
    return "estruturado"  # fallback


def test_router_categorias_validas_definidas():
    """As 4 categorias esperadas estão registradas."""
    assert _VALIDAS == {"estruturado", "proposta", "recusar", "fora_escopo"}


def test_router_parse_json_simples():
    raw = '{"categoria": "estruturado"}'
    assert _extrai_categoria(raw) == "estruturado"


def test_router_parse_com_espacos_e_uppercase():
    raw = '  {"categoria":  "RECUSAR"}  '
    assert _extrai_categoria(raw) == "recusar"


def test_router_parse_json_dentro_de_markdown():
    """LLM às vezes encapsula a resposta em ```json ... ```"""
    raw = '```json\n{"categoria": "proposta"}\n```'
    assert _extrai_categoria(raw) == "proposta"


def test_router_parse_categoria_invalida_cai_para_estruturado():
    raw = '{"categoria": "qualquerOutraCoisa"}'
    assert _extrai_categoria(raw) == "estruturado"


def test_router_parse_resposta_sem_json_cai_para_estruturado():
    raw = "Não consegui classificar."
    assert _extrai_categoria(raw) == "estruturado"


def test_router_parse_json_malformado_cai_para_estruturado():
    raw = '{"categoria": "estruturado"'  # falta fechar
    assert _extrai_categoria(raw) == "estruturado"


def test_router_parse_categoria_vazia_cai_para_estruturado():
    raw = '{"categoria": ""}'
    assert _extrai_categoria(raw) == "estruturado"


def test_router_parse_todas_categorias_validas():
    for cat in _VALIDAS:
        raw = json.dumps({"categoria": cat})
        assert _extrai_categoria(raw) == cat
