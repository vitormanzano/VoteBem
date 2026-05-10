"""Pós-processadores que reforçam RFIA06 (formatos pt-BR) na saída do LLM.

As ferramentas em retrieval/tools.py já entregam valores formatados
(via _fmt_brl), mas o LLM às vezes copia o número cru ou re-formata.
Estes normalizadores são uma rede de segurança aplicada na resposta final.
"""
import re

# ---------------------------------------------------------------------------
# Valores monetários — força R$ X.XXX,XX
# ---------------------------------------------------------------------------

_RE_REAL = re.compile(r"R\$\s*([0-9][0-9.,]*)", flags=re.IGNORECASE)


def _fmt_real(numero: float) -> str:
    s = f"{numero:,.2f}"
    return f"R$ {s.replace(',', 'X').replace('.', ',').replace('X', '.')}"


def _parse_numero_ambiguo(s: str) -> float | None:
    """Tenta inferir o valor float a partir de uma string em formato BR ou US."""
    raw = s.strip().rstrip(".,")
    if not raw or not any(ch.isdigit() for ch in raw):
        return None

    tem_ponto = "." in raw
    tem_virgula = "," in raw
    try:
        if tem_ponto and tem_virgula:
            # último separador é o decimal
            if raw.rfind(",") > raw.rfind("."):
                # BR: 1.234.567,89
                return float(raw.replace(".", "").replace(",", "."))
            # US: 1,234,567.89
            return float(raw.replace(",", ""))
        if tem_virgula:
            after = raw.split(",")[-1]
            if len(after) <= 2 and raw.count(",") == 1:
                # decimal BR: 1234,56
                return float(raw.replace(",", "."))
            return float(raw.replace(",", ""))
        if tem_ponto:
            after = raw.split(".")[-1]
            if len(after) <= 2 and raw.count(".") == 1:
                # decimal US: 1234.56
                return float(raw)
            # separador de milhar BR sem decimal: 1.234.567
            return float(raw.replace(".", ""))
        return float(raw)
    except ValueError:
        return None


def normalize_brl(texto: str) -> str:
    """Normaliza qualquer 'R$ ...' para o formato R$ X.XXX,XX."""

    def _sub(m: re.Match) -> str:
        valor = _parse_numero_ambiguo(m.group(1))
        return _fmt_real(valor) if valor is not None else m.group(0)

    return _RE_REAL.sub(_sub, texto)


# ---------------------------------------------------------------------------
# Datas — converte ISO yyyy-mm-dd para DD/MM/AAAA
# ---------------------------------------------------------------------------

_RE_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def normalize_dates(texto: str) -> str:
    def _sub(m: re.Match) -> str:
        ano, mes, dia = m.group(1), m.group(2), m.group(3)
        return f"{dia}/{mes}/{ano}"

    return _RE_ISO.sub(_sub, texto)


# ---------------------------------------------------------------------------
# Validação de citações [N] inválidas (Tier B)
# ---------------------------------------------------------------------------

_RE_CITACAO = re.compile(r"\s*\[(\d+)\]")


def validar_citacoes(texto: str, max_ref: int) -> str:
    """Remove citações [N] inválidas (N fora de 1..max_ref).

    O LLM ocasionalmente inventa números de referência (ex: cita [119] quando
    só há 6 fontes). Esta função apaga essas citações inventadas mantendo
    o texto ao redor; espaços duplicados são colapsados.
    """
    if not texto:
        return texto

    def _sub(m: re.Match) -> str:
        n = int(m.group(1))
        if 1 <= n <= max_ref:
            return m.group(0)
        return ""

    cleaned = _RE_CITACAO.sub(_sub, texto)
    # colapsa espaços duplos e ajusta pontuação
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    return cleaned


# ---------------------------------------------------------------------------
# Pós-processador único usado pelo main.py
# ---------------------------------------------------------------------------

def normalize(texto: str, max_ref_citacao: int = 0) -> str:
    if not texto:
        return texto
    texto = normalize_brl(texto)
    texto = normalize_dates(texto)
    if max_ref_citacao > 0:
        texto = validar_citacoes(texto, max_ref_citacao)
    return texto
