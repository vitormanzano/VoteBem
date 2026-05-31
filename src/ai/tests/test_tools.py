"""Testes das funções puras de retrieval/tools.py.

Cobrem _fmt_brl e _jsonify — não envolvem banco de dados.
As funções tool-callable (get_*) que executam SQL não são testadas
aqui porque exigiriam fixture de banco; ficam cobertas pelo runner
de avaliação (eval/run_eval.py) e pelos smoke tests manuais.
"""
from datetime import date, datetime
from decimal import Decimal

from retrieval.tools import _fmt_brl, _jsonify


# ---------------------------------------------------------------------------
# _fmt_brl
# ---------------------------------------------------------------------------

def test_fmt_brl_inteiro():
    assert _fmt_brl(1234) == "R$ 1.234,00"


def test_fmt_brl_decimal():
    assert _fmt_brl(Decimal("7987921.57")) == "R$ 7.987.921,57"


def test_fmt_brl_float_com_duas_casas():
    assert _fmt_brl(1234.56) == "R$ 1.234,56"


def test_fmt_brl_float_com_uma_casa():
    """Uma casa decimal deve virar duas (preenchimento com zero)."""
    assert _fmt_brl(50000.5) == "R$ 50.000,50"


def test_fmt_brl_zero():
    assert _fmt_brl(0) == "R$ 0,00"


def test_fmt_brl_none_retorna_none():
    assert _fmt_brl(None) is None


def test_fmt_brl_valor_grande():
    assert _fmt_brl(Decimal("1234567890.12")) == "R$ 1.234.567.890,12"


# ---------------------------------------------------------------------------
# _jsonify
# ---------------------------------------------------------------------------

def test_jsonify_decimal_vira_float():
    assert _jsonify(Decimal("3.14")) == 3.14


def test_jsonify_date_vira_iso_string():
    assert _jsonify(date(2022, 10, 30)) == "2022-10-30"


def test_jsonify_datetime_vira_iso_string():
    out = _jsonify(datetime(2022, 10, 30, 15, 45, 0))
    assert out.startswith("2022-10-30T15:45:00")


def test_jsonify_dict_recursivo():
    entrada = {"valor": Decimal("100.50"), "nome": "Lula"}
    out = _jsonify(entrada)
    assert out == {"valor": 100.50, "nome": "Lula"}


def test_jsonify_lista_recursiva():
    entrada = [Decimal("1"), Decimal("2"), "texto"]
    assert _jsonify(entrada) == [1.0, 2.0, "texto"]


def test_jsonify_estrutura_aninhada():
    entrada = {
        "candidatos": [
            {"nome": "Lula", "patrimonio": Decimal("100.0")},
            {"nome": "Bolsonaro", "patrimonio": Decimal("200.5")},
        ]
    }
    out = _jsonify(entrada)
    assert out["candidatos"][0]["patrimonio"] == 100.0
    assert out["candidatos"][1]["patrimonio"] == 200.5


def test_jsonify_tipos_primitivos_inalterados():
    assert _jsonify(42) == 42
    assert _jsonify("texto") == "texto"
    assert _jsonify(True) is True
    assert _jsonify(None) is None
