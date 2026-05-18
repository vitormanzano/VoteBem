-- =============================================
-- Migration 001 — Adiciona pgvector e PROPOSTA_CHUNK
-- =============================================
-- Idempotente: pode ser rodada várias vezes sem efeito colateral.
-- Aplicar em bancos que já tinham sido inicializados antes da
-- introdução do pgvector no init.sql.
--
-- Como rodar:
--   docker exec -i VoteBem psql -U $POSTGRES_USER -d $POSTGRES_DB_NAME \
--       < db/migrations/001_pgvector.sql
-- =============================================

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS PROPOSTA_CHUNK (
    id              BIGSERIAL   PRIMARY KEY,
    sq_candidato    BIGINT      NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    ano_eleicao     INT         NOT NULL,
    idx             INT         NOT NULL,
    texto           TEXT        NOT NULL,
    embedding       VECTOR(384) NOT NULL,
    UNIQUE (sq_candidato, idx)
);

CREATE INDEX IF NOT EXISTS idx_proposta_chunk_sq
    ON PROPOSTA_CHUNK(sq_candidato);
CREATE INDEX IF NOT EXISTS idx_proposta_chunk_ano
    ON PROPOSTA_CHUNK(ano_eleicao);
CREATE INDEX IF NOT EXISTS idx_proposta_chunk_embedding
    ON PROPOSTA_CHUNK USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);
