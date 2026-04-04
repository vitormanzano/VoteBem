-- Script de criação do banco de dados

-- 1. ELEICAO — sem dependências
CREATE TABLE IF NOT EXISTS ELEICAO (
    nr_eleicao      INT          PRIMARY KEY,
    nr_turno        INT,
    ds_eleicao      VARCHAR      NOT NULL,
    cd_tipo_eleicao VARCHAR,
    dt_eleicao      DATE
);

-- 2. PARTIDO — sem dependências
CREATE TABLE IF NOT EXISTS PARTIDO (
    nr_partido INT          PRIMARY KEY,
    sg_partido VARCHAR(20)  NOT NULL,
    nm_partido VARCHAR      NOT NULL
);

-- 3. CANDIDATO — sem dependências
CREATE TABLE IF NOT EXISTS CANDIDATO (
    nr_cpf_candidato    VARCHAR     PRIMARY KEY,
    nm_candidato        VARCHAR     NOT NULL,
    nm_urna_candidato   VARCHAR,
    dt_nascimento       DATE,
    ds_genero           VARCHAR,
    ds_grau_instrucao   VARCHAR,
    ds_estado_civil     VARCHAR,
    ds_ocupacao         VARCHAR,
    sg_uf_nascimento    VARCHAR(2),
    nm_municipio_nascimento VARCHAR
);

-- 4. COLIGACAO — depende de ELEICAO
CREATE TABLE IF NOT EXISTS COLIGACAO (
    sq_coligacao    BIGINT      PRIMARY KEY,
    nr_eleicao      INT         REFERENCES ELEICAO(nr_eleicao),
    nm_coligacao    VARCHAR,
    sg_uf           VARCHAR(2),
    tp_agremiacao   VARCHAR
);

-- 5. CANDIDATURA — depende de CANDIDATO, ELEICAO, PARTIDO, COLIGACAO
CREATE TABLE IF NOT EXISTS CANDIDATURA (
    sq_candidato            BIGINT      PRIMARY KEY,
    nr_cpf_candidato        VARCHAR     REFERENCES CANDIDATO(nr_cpf_candidato),
    nr_eleicao              INT         REFERENCES ELEICAO(nr_eleicao),
    nr_partido              INT         REFERENCES PARTIDO(nr_partido),
    sq_coligacao            BIGINT      REFERENCES COLIGACAO(sq_coligacao),
    nm_urna_candidato       VARCHAR,
    cd_cargo                VARCHAR,
    ds_cargo                VARCHAR,
    sg_uf                   VARCHAR(2),
    nr_candidato            INT,
    cd_situacao_candidatura VARCHAR,
    ds_situacao_candidatura VARCHAR,
    nr_votos                INT,
    cd_sit_tot_turno        VARCHAR
);

-- 6. BEM_CANDIDATO — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS BEM_CANDIDATO (
    id_bem          BIGINT          PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato    BIGINT          REFERENCES CANDIDATURA(sq_candidato),
    nr_ordem_bem    INT,
    cd_tipo_bem     VARCHAR,
    ds_tipo_bem     VARCHAR,
    vr_bem          DECIMAL(15, 2)
);

-- 7. REDE_SOCIAL — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS REDE_SOCIAL (
    id_rede_social      BIGINT  PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato        BIGINT  REFERENCES CANDIDATURA(sq_candidato),
    ds_url              VARCHAR,
    cd_tipo_rede_social VARCHAR
);

-- 8. PROPOSTA_GOVERNO — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS PROPOSTA_GOVERNO (
    id_proposta             BIGINT      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato            BIGINT      REFERENCES CANDIDATURA(sq_candidato),
    nm_arquivo              VARCHAR,
    ds_caminho_arquivo      VARCHAR,
    tx_conteudo_extraido    TEXT,
    st_processado           BOOLEAN     DEFAULT FALSE,
    dt_processamento        TIMESTAMP
);

-- 9. RESUMO_PROPOSTA — depende de PROPOSTA_GOVERNO
CREATE TABLE IF NOT EXISTS RESUMO_PROPOSTA (
    id_resumo       BIGINT      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_proposta     BIGINT      REFERENCES PROPOSTA_GOVERNO(id_proposta),
    ds_tema         VARCHAR,
    tx_resumo       TEXT,
    dt_geracao      TIMESTAMP
);

-- 10. CERTIDAO_CRIMINAL — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS CERTIDAO_CRIMINAL (
    id_certidao         BIGINT  PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato        BIGINT  REFERENCES CANDIDATURA(sq_candidato),
    nm_arquivo          VARCHAR,
    ds_caminho_arquivo  VARCHAR,
    dt_emissao          DATE,
    dt_validade         DATE
);

-- 11. MOTIVO_CASSACAO — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS MOTIVO_CASSACAO (
    id_cassacao     BIGINT  PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato    BIGINT  REFERENCES CANDIDATURA(sq_candidato),
    cd_motivo       VARCHAR,
    ds_motivo       VARCHAR,
    dt_decisao      DATE,
    ds_orgao        VARCHAR
);

-- 12. NOTA_FISCAL — depende de CANDIDATURA
CREATE TABLE IF NOT EXISTS NOTA_FISCAL (
    id_nota         BIGINT          PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sq_candidato    BIGINT          REFERENCES CANDIDATURA(sq_candidato),
    nr_nota_fiscal  VARCHAR,
    nm_fornecedor   VARCHAR,
    cd_tipo_despesa VARCHAR,
    vr_despesa      DECIMAL(15, 2),
    dt_despesa      DATE
);
