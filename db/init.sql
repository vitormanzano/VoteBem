-- =============================================
-- VoteBem - Schema PostgreSQL
-- =============================================

DROP TABLE IF EXISTS RESUMO_PROPOSTA CASCADE;
DROP TABLE IF EXISTS PROPOSTA_GOVERNO CASCADE;
DROP TABLE IF EXISTS NOTA_FISCAL CASCADE;
DROP TABLE IF EXISTS DESPESA_CANDIDATO CASCADE;
DROP TABLE IF EXISTS MOTIVO_CASSACAO CASCADE;
DROP TABLE IF EXISTS CERTIDAO_CRIMINAL CASCADE;
DROP TABLE IF EXISTS REDE_SOCIAL CASCADE;
DROP TABLE IF EXISTS BEM_CANDIDATO CASCADE;
DROP TABLE IF EXISTS RESULTADO_TURNO CASCADE;
DROP TABLE IF EXISTS CANDIDATURA CASCADE;
DROP TABLE IF EXISTS COLIGACAO CASCADE;
DROP TABLE IF EXISTS CANDIDATO CASCADE;
DROP TABLE IF EXISTS PARTIDO CASCADE;
DROP TABLE IF EXISTS ELEICAO CASCADE;

CREATE TABLE ELEICAO (
    cd_eleicao      BIGINT      NOT NULL,
    nr_turno        INT         NOT NULL,
    ano_eleicao     INT         NOT NULL,
    cd_tipo_eleicao INT,
    nm_tipo_eleicao VARCHAR,
    ds_eleicao      VARCHAR,
    dt_eleicao      DATE,
    PRIMARY KEY (cd_eleicao, nr_turno)
);

CREATE TABLE PARTIDO (
    nr_partido  INT             PRIMARY KEY,
    sg_partido  VARCHAR(20)     NOT NULL,
    nm_partido  VARCHAR         NOT NULL
);

CREATE TABLE CANDIDATO (
    nr_cpf_candidato    VARCHAR(11)     PRIMARY KEY,
    nm_candidato        VARCHAR         NOT NULL,
    nm_social_candidato VARCHAR, 
    nm_urna_candidato   VARCHAR,         
    dt_nascimento       DATE,
    sg_uf_nascimento    VARCHAR(2),
    cd_genero           INT,
    ds_genero           VARCHAR,
    cd_grau_instrucao   INT,
    ds_grau_instrucao   VARCHAR,
    cd_estado_civil     INT,
    ds_estado_civil     VARCHAR,
    cd_cor_raca         INT,
    ds_cor_raca         VARCHAR
);

CREATE TABLE COLIGACAO (
    sq_coligacao            BIGINT      PRIMARY KEY,
    cd_eleicao              BIGINT      NOT NULL,
    nr_turno                INT         NOT NULL,
    nm_coligacao            VARCHAR,
    ds_composicao_coligacao VARCHAR,
    tp_agremiacao           VARCHAR,
    sg_uf                   VARCHAR(2),
    FOREIGN KEY (cd_eleicao, nr_turno) REFERENCES ELEICAO(cd_eleicao, nr_turno)
);

CREATE TABLE CANDIDATURA (
    sq_candidato                BIGINT      PRIMARY KEY,
    nr_cpf_candidato            VARCHAR(11) NOT NULL REFERENCES CANDIDATO(nr_cpf_candidato),
    cd_eleicao                  BIGINT      NOT NULL,
    nr_partido                  INT         REFERENCES PARTIDO(nr_partido),
    sq_coligacao                BIGINT      REFERENCES COLIGACAO(sq_coligacao),
    nm_urna_candidato           VARCHAR,
    cd_cargo                    INT,
    ds_cargo                    VARCHAR,
    sg_uf                       VARCHAR(2),
    nr_candidato                INT,
    cd_situacao_candidatura     INT,
    ds_situacao_candidatura     VARCHAR,
    cd_ocupacao                 INT,
    ds_ocupacao                 VARCHAR,
    foto_url                    VARCHAR,
    st_reeleicao                VARCHAR(1),
    vr_despesa_max_campanha     DECIMAL(15,2)
);

CREATE TABLE RESULTADO_TURNO (
    sq_candidato        BIGINT      NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    cd_eleicao          BIGINT      NOT NULL,
    nr_turno            INT         NOT NULL,
    nr_votos            INT         DEFAULT 0,
    cd_sit_tot_turno    INT,
    ds_sit_tot_turno    VARCHAR,
    PRIMARY KEY (sq_candidato, nr_turno),
    FOREIGN KEY (cd_eleicao, nr_turno) REFERENCES ELEICAO(cd_eleicao, nr_turno)
);

CREATE TABLE BEM_CANDIDATO (
    sq_candidato        BIGINT          NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    nr_ordem_bem        INT             NOT NULL,
    cd_tipo_bem         INT,
    ds_tipo_bem         VARCHAR,
    ds_bem              VARCHAR,
    vr_bem              DECIMAL(15,2),
    PRIMARY KEY (sq_candidato, nr_ordem_bem)
);

CREATE TABLE REDE_SOCIAL (
    sq_candidato    BIGINT      NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    nr_ordem        INT         NOT NULL,
    ds_url          VARCHAR,
    tipo_rede_social VARCHAR,
    PRIMARY KEY (sq_candidato, nr_ordem)
);

CREATE TABLE PROPOSTA_GOVERNO (
    sq_candidato            BIGINT      PRIMARY KEY REFERENCES CANDIDATURA(sq_candidato),
    nm_arquivo              VARCHAR,
    ds_caminho_arquivo      VARCHAR,
    tx_conteudo_extraido    TEXT,
    st_processado           BOOLEAN     DEFAULT FALSE,
    dt_processamento        TIMESTAMP
);

CREATE TABLE RESUMO_PROPOSTA (
    id_resumo       BIGINT      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato    BIGINT      NOT NULL REFERENCES PROPOSTA_GOVERNO(sq_candidato),
    ds_tema         VARCHAR     NOT NULL,
    tx_resumo       TEXT        NOT NULL,
    dt_geracao      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CERTIDAO_CRIMINAL (
    id_certidao         BIGINT      PRIMARY KEY,
    sq_candidato        BIGINT      NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    nm_arquivo          VARCHAR     NOT NULL,
    ds_caminho_arquivo  VARCHAR,
    dt_emissao          DATE,
    dt_validade         DATE
);

CREATE TABLE MOTIVO_CASSACAO (
    sq_candidato BIGINT NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    ds_tp_motivo VARCHAR,
    ds_motivo VARCHAR NOT NULL,
    PRIMARY KEY (sq_candidato, ds_motivo)
);

CREATE TABLE DESPESA_CANDIDATO (
    id_despesa          BIGINT          PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato        BIGINT          NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    nr_documento        VARCHAR,
    cpf_cnpj_fornecedor VARCHAR,
    nm_fornecedor       VARCHAR,
    dt_despesa          DATE,
    vr_despesa          DECIMAL(15,2),
    ds_tipo_despesa     VARCHAR,
    ds_fonte_recurso    VARCHAR,
    ds_especie_recurso  VARCHAR,
    ds_despesa          TEXT,
    UNIQUE (sq_candidato, nr_documento, cpf_cnpj_fornecedor, dt_despesa)
);

CREATE TABLE NOTA_FISCAL (
    id_nota                 BIGINT          PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato            BIGINT          NOT NULL REFERENCES CANDIDATURA(sq_candidato),
    nr_nota_fiscal          VARCHAR,
    nr_serie                VARCHAR,
    cpf_cnpj_emitente       VARCHAR,
    dt_emissao              DATE,
    vr_nota_fiscal          DECIMAL(15,2),
    nr_chave_acesso         VARCHAR,
    nm_url_acesso           VARCHAR,
    UNIQUE (sq_candidato, nr_nota_fiscal, cpf_cnpj_emitente)
);

-- Indíces
CREATE INDEX idx_candidato_nome ON CANDIDATO(nm_candidato);
CREATE INDEX idx_candidatura_urna ON CANDIDATURA(nm_urna_candidato);

-- Busca por partido
CREATE INDEX idx_candidatura_partido ON CANDIDATURA(nr_partido);

-- Busca por ano eleitoral
CREATE INDEX idx_eleicao_ano ON ELEICAO(ano_eleicao);

-- Historico eleitoral (candidaturas de um mesmo CPF)
CREATE INDEX idx_candidatura_cpf ON CANDIDATURA(nr_cpf_candidato);

-- Resultados por turno
CREATE INDEX idx_resultado_turno_sq ON RESULTADO_TURNO(sq_candidato);

-- Evolucao patrimonial
CREATE INDEX idx_bem_candidato_sq ON BEM_CANDIDATO(sq_candidato);

--  Situacao juridica
CREATE INDEX idx_certidao_sq ON CERTIDAO_CRIMINAL(sq_candidato);
CREATE INDEX idx_cassacao_sq ON MOTIVO_CASSACAO(sq_candidato);

-- Despesas
CREATE INDEX idx_despesa_sq ON DESPESA_CANDIDATO(sq_candidato);
CREATE INDEX idx_nota_sq ON NOTA_FISCAL(sq_candidato);
