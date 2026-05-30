"""Testes do pipeline de ingestão (chunking, limpeza, extração de ano).

Cobrem funções puras de ingest/extract_pdfs.py — não envolvem leitura
de PDF nem banco de dados.
"""
from ingest.extract_pdfs import ano_from_nome, chunk_text, clean_text


# ---------------------------------------------------------------------------
# clean_text
# ---------------------------------------------------------------------------

def test_clean_text_normaliza_unicode():
    """NFKC deve normalizar ligaduras e variantes tipográficas."""
    # caractere com diacrítico em forma decomposta deve virar composta
    composto = "ação"
    decomposto = "ação"
    assert clean_text(decomposto) == composto


def test_clean_text_colapsa_espacos_duplicados():
    txt = "Texto    com   muitos    espaços"
    assert clean_text(txt) == "Texto com muitos espaços"


def test_clean_text_reduz_quebras_de_linha_excessivas():
    """Mais de 2 \\n consecutivos viram exatamente \\n\\n."""
    txt = "Parágrafo um.\n\n\n\n\nParágrafo dois."
    out = clean_text(txt)
    assert "\n\n\n" not in out
    assert "Parágrafo um." in out
    assert "Parágrafo dois." in out


def test_clean_text_remove_caracteres_de_controle():
    """Caracteres de controle (exceto tab/newline) devem ser removidos."""
    txt = "Antes\x00\x07Depois"
    assert "\x00" not in clean_text(txt)
    assert "\x07" not in clean_text(txt)


def test_clean_text_preserva_quebras_de_linha():
    """Quebras simples (\\n) são preservadas; tabs são colapsadas em espaço."""
    txt = "Linha 1\nLinha 2\tcom tab"
    out = clean_text(txt)
    assert "\n" in out
    # tab é tratado como espaço em branco e colapsado pela regex [ \t]+ → ' '
    assert "Linha 2 com tab" in out


def test_clean_text_string_vazia():
    assert clean_text("") == ""


def test_clean_text_repara_ligadura_com_espaco_espurio():
    """A extração de PDF insere um espaço após o glifo de ligadura (ﬁ),
    partindo a palavra; clean_text deve recompor a palavra."""
    txt = "objetivos estratégicos deﬁ nidos no plano"
    assert clean_text(txt) == "objetivos estratégicos definidos no plano"


def test_clean_text_repara_ligaduras_diversas():
    """ﬁ, ﬂ e ﬃ no meio ou no início da palavra são todas recompostas."""
    assert clean_text("eﬁ ciência") == "eficiência"
    assert clean_text("aﬂ ige") == "aflige"          # ﬂ
    assert clean_text("ﬁ nanceira") == "financeira"  # ligadura inicia a palavra
    assert clean_text("eﬃ ciente") == "efficiente"   # ﬃ → ffi


def test_clean_text_ligadura_sem_espaco_apenas_normaliza():
    """Ligadura sem espaço espúrio só sofre normalização NFKC, sem juntar nada."""
    assert clean_text("deﬁnidos") == "definidos"


# ---------------------------------------------------------------------------
# chunk_text
# ---------------------------------------------------------------------------

def test_chunk_text_string_vazia_retorna_lista_vazia():
    assert chunk_text("") == []


def test_chunk_text_texto_curto_devolve_um_chunk():
    txt = "Texto pequeno que cabe em um único chunk."
    chunks = chunk_text(txt, size=2000, overlap=200)
    assert len(chunks) == 1
    assert chunks[0] == txt


def test_chunk_text_texto_longo_e_dividido():
    """Texto bem maior que size deve gerar mais de 1 chunk."""
    txt = ("Frase. " * 1000)  # 7000 chars aprox
    chunks = chunk_text(txt, size=1000, overlap=100)
    assert len(chunks) > 1
    # cada chunk razoavelmente próximo do tamanho-alvo
    for c in chunks[:-1]:
        assert len(c) <= 1000 + 100  # margem para corte em fronteira


def test_chunk_text_overlap_preserva_continuidade():
    """Chunks consecutivos devem compartilhar conteúdo (overlap)."""
    # texto grande com palavras-marca espaçadas
    palavras = ["MARCA_" + str(i) for i in range(200)]
    txt = " ".join(palavras)
    chunks = chunk_text(txt, size=300, overlap=80)
    assert len(chunks) >= 2
    # alguma palavra do fim do chunk i deve aparecer no início do chunk i+1
    # (não validamos exato porque o cut respeita fronteiras)
    assert any(
        any(p in chunks[i + 1][:200] for p in chunks[i].split()[-5:])
        for i in range(len(chunks) - 1)
    )


def test_chunk_text_prefere_quebra_em_paragrafo():
    """Se há \\n no meio do range, o cut deve preferir essa fronteira."""
    txt = "A" * 600 + "\n" + "B" * 600
    chunks = chunk_text(txt, size=1000, overlap=100)
    # primeiro chunk deve terminar próximo da quebra de parágrafo
    assert chunks[0].rstrip().endswith("A") or "\n" in chunks[0][-50:]


# ---------------------------------------------------------------------------
# ano_from_nome
# ---------------------------------------------------------------------------

def test_ano_from_nome_extrai_ano_inicial():
    assert ano_from_nome("2022BR280001607829.pdf") == 2022
    assert ano_from_nome("2010BR280000000019.pdf") == 2010
    assert ano_from_nome("2014BR280000000001.pdf") == 2014


def test_ano_from_nome_sem_prefixo_numerico_retorna_zero():
    assert ano_from_nome("arquivo.pdf") == 0
    assert ano_from_nome("BR2022xx.pdf") == 0


def test_ano_from_nome_string_vazia():
    assert ano_from_nome("") == 0
