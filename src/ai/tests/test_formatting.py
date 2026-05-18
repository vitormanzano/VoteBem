"""Testes do pós-processador chat/formatting.py.

Cobrem normalize_brl, normalize_dates e validar_citacoes — funções
puras que recebem string e devolvem string. Reforçam o cumprimento
do RFIA06 (formatos pt-BR) e do validador de citações usado no Tier B.
"""
import pytest

from chat.formatting import (
    normalize,
    normalize_brl,
    normalize_dates,
    validar_citacoes,
)


# ---------------------------------------------------------------------------
# normalize_brl
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("entrada,esperado", [
    # formato US sem separador de milhar (ponto como decimal)
    ("R$ 7961288.89", "R$ 7.961.288,89"),
    # formato US com separador de milhar (vírgula como milhar, ponto decimal)
    ("R$ 7,961,288.89", "R$ 7.961.288,89"),
    # já em formato BR — não deve alterar
    ("R$ 7.987.921,57", "R$ 7.987.921,57"),
    # número inteiro sem casas decimais
    ("R$ 1234", "R$ 1.234,00"),
    # decimal BR sem milhar
    ("R$ 1234,56", "R$ 1.234,56"),
    # decimal US com 1 casa
    ("R$ 50000.5", "R$ 50.000,50"),
    # valor pequeno
    ("R$ 5,50", "R$ 5,50"),
    # zero
    ("R$ 0", "R$ 0,00"),
])
def test_normalize_brl_casos_basicos(entrada, esperado):
    assert normalize_brl(entrada) == esperado


def test_normalize_brl_dentro_de_frase():
    txt = "O patrimônio é R$ 7961288.89 conforme TSE."
    assert normalize_brl(txt) == "O patrimônio é R$ 7.961.288,89 conforme TSE."


def test_normalize_brl_multiplos_valores():
    txt = "Bens: R$ 1234.56, créditos: R$ 7,000,000.00"
    out = normalize_brl(txt)
    assert "R$ 1.234,56" in out
    assert "R$ 7.000.000,00" in out


def test_normalize_brl_sem_valores_monetarios():
    txt = "Sem dinheiro mencionado, só texto."
    assert normalize_brl(txt) == txt


def test_normalize_brl_string_vazia():
    assert normalize_brl("") == ""


# ---------------------------------------------------------------------------
# normalize_dates
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("entrada,esperado", [
    ("Eleição em 2022-10-30.", "Eleição em 30/10/2022."),
    ("De 2024-01-01 até 2024-12-31.", "De 01/01/2024 até 31/12/2024."),
    ("Texto sem data.", "Texto sem data."),
])
def test_normalize_dates_iso_para_br(entrada, esperado):
    assert normalize_dates(entrada) == esperado


def test_normalize_dates_nao_altera_data_br():
    """Data já no formato DD/MM/AAAA deve ser preservada."""
    txt = "Inscrita em 15/08/2022."
    assert normalize_dates(txt) == txt


# ---------------------------------------------------------------------------
# validar_citacoes
# ---------------------------------------------------------------------------

def test_validar_citacoes_mantem_referencias_validas():
    txt = "Lula propõe [1] saúde universal e [2] economia popular."
    assert validar_citacoes(txt, max_ref=6) == txt


def test_validar_citacoes_remove_referencia_inventada():
    txt = "Lula propõe [119] saúde e [1] economia."
    out = validar_citacoes(txt, max_ref=6)
    assert "[119]" not in out
    assert "[1]" in out


def test_validar_citacoes_remove_multiplas_invalidas():
    txt = "Cita [7] e [99] mas só temos 6."
    out = validar_citacoes(txt, max_ref=6)
    assert "[7]" not in out
    assert "[99]" not in out


def test_validar_citacoes_ajusta_pontuacao_adjacente():
    txt = "Texto com [3] no meio. E ponto final [99]."
    out = validar_citacoes(txt, max_ref=6)
    assert "[3]" in out
    assert "[99]" not in out
    # não deve haver espaço pendurado antes do ponto final
    assert " ." not in out


def test_validar_citacoes_max_ref_zero_remove_tudo():
    """Com max_ref=0 nenhuma referência é válida; todas são removidas.
    Quem quer desligar a validação deve usar normalize() sem o
    parâmetro max_ref_citacao (default 0 ali pula o validador)."""
    txt = "Cita [1] e [99]."
    out = validar_citacoes(txt, max_ref=0)
    assert "[1]" not in out
    assert "[99]" not in out


def test_normalize_desliga_validacao_de_citacoes_por_default():
    """normalize() sem max_ref_citacao deve preservar todas as citações."""
    txt = "Cita [1] e [99] sem mexer."
    assert normalize(txt) == txt


def test_validar_citacoes_string_vazia():
    assert validar_citacoes("", max_ref=6) == ""


# ---------------------------------------------------------------------------
# normalize (orquestrador)
# ---------------------------------------------------------------------------

def test_normalize_aplica_brl_e_datas():
    txt = "Em 2022-10-30 declarou R$ 7961288.89."
    out = normalize(txt)
    assert "30/10/2022" in out
    assert "R$ 7.961.288,89" in out


def test_normalize_com_validacao_de_citacoes():
    txt = "Patrimônio R$ 1234.56 conforme [1] e [99]."
    out = normalize(txt, max_ref_citacao=3)
    assert "R$ 1.234,56" in out
    assert "[1]" in out
    assert "[99]" not in out


def test_normalize_string_vazia():
    assert normalize("") == ""
    assert normalize(None) is None
