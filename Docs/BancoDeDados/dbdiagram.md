Table ELEICAO {
  cd_eleicao bigint [not null]
  nr_turno int [not null]
  ano_eleicao int [not null]
  cd_tipo_eleicao int
  nm_tipo_eleicao varchar
  ds_eleicao varchar
  dt_eleicao date

  indexes {
    (cd_eleicao, nr_turno) [pk]
  }
}

Table PARTIDO {
  nr_partido int [primary key]
  sg_partido varchar(20) [not null]
  nm_partido varchar [not null]
}

Table CANDIDATO {
  nr_cpf_candidato varchar(11) [primary key]
  nm_candidato varchar [not null]
  nm_social_candidato varchar
  nm_urna_candidato varchar
  dt_nascimento date
  sg_uf_nascimento varchar(2)
  cd_genero int
  ds_genero varchar
  cd_grau_instrucao int
  ds_grau_instrucao varchar
  cd_estado_civil int
  ds_estado_civil varchar
  cd_cor_raca int
  ds_cor_raca varchar
}

Table COLIGACAO {
  sq_coligacao bigint [primary key]
  cd_eleicao bigint [not null, ref: > ELEICAO.cd_eleicao]
  nr_turno int [not null, ref: > ELEICAO.nr_turno]
  nm_coligacao varchar
  ds_composicao_coligacao varchar
  tp_agremiacao varchar
  sg_uf varchar(2)
}

Table CANDIDATURA {
  sq_candidato bigint [primary key]
  nr_cpf_candidato varchar(11) [not null, ref: > CANDIDATO.nr_cpf_candidato]
  cd_eleicao bigint [not null]
  nr_partido int [ref: > PARTIDO.nr_partido]
  sq_coligacao bigint [ref: > COLIGACAO.sq_coligacao]
  nm_urna_candidato varchar
  cd_cargo int
  ds_cargo varchar
  sg_uf varchar(2)
  nr_candidato int
  cd_situacao_candidatura int
  ds_situacao_candidatura varchar
  cd_ocupacao int
  ds_ocupacao varchar
  foto_url varchar
  st_reeleicao varchar(1)
  vr_despesa_max_campanha decimal(15,2)
}

Table RESULTADO_TURNO {
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  cd_eleicao bigint [not null, ref: > ELEICAO.cd_eleicao]
  nr_turno int [not null, ref: > ELEICAO.nr_turno]
  nr_votos int [default: 0]
  cd_sit_tot_turno int
  ds_sit_tot_turno varchar

  indexes {
    (sq_candidato, nr_turno) [pk]
  }
}

Table BEM_CANDIDATO {
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  nr_ordem_bem int [not null]
  cd_tipo_bem int
  ds_tipo_bem varchar
  ds_bem varchar
  vr_bem decimal(15,2)

  indexes {
    (sq_candidato, nr_ordem_bem) [pk]
  }
}

Table REDE_SOCIAL {
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  nr_ordem int [not null]
  ds_url varchar
  tipo_rede_social varchar

  indexes {
    (sq_candidato, nr_ordem) [pk]
  }
}

Table PROPOSTA_GOVERNO {
  sq_candidato bigint [primary key, ref: > CANDIDATURA.sq_candidato]
  nm_arquivo varchar
  ds_caminho_arquivo varchar
  tx_conteudo_extraido text
  st_processado boolean [default: false]
  dt_processamento timestamp
}

Table RESUMO_PROPOSTA {
  id_resumo bigint [primary key, increment]
  sq_candidato bigint [not null, ref: > PROPOSTA_GOVERNO.sq_candidato]
  ds_tema varchar [not null]
  tx_resumo text [not null]
  dt_geracao timestamp
}

Table CERTIDAO_CRIMINAL {
  id_certidao bigint [primary key, increment]
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  nm_arquivo varchar [not null]
  ds_caminho_arquivo varchar
  dt_emissao date
  dt_validade date
}

Table MOTIVO_CASSACAO {
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  ds_tp_motivo varchar
  ds_motivo varchar [not null]
  nr_processo varchar

  indexes {
    (sq_candidato, ds_motivo) [pk]
  }
}

Table DESPESA_CANDIDATO {
  id_despesa bigint [primary key, increment]
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  nr_documento varchar
  cpf_cnpj_fornecedor varchar
  nm_fornecedor varchar
  dt_despesa date
  vr_despesa decimal(15,2)
  ds_tipo_despesa varchar
  ds_fonte_recurso varchar
  ds_especie_recurso varchar
  ds_despesa text
}

Table NOTA_FISCAL {
  id_nota bigint [primary key, increment]
  sq_candidato bigint [not null, ref: > CANDIDATURA.sq_candidato]
  nr_nota_fiscal varchar
  nr_serie varchar
  cpf_cnpj_emitente varchar
  dt_emissao date
  vr_nota_fiscal decimal(15,2)
  nr_chave_acesso varchar
  nm_url_acesso varchar
}
