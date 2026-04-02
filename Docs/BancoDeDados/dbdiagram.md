Table CANDIDATO {
  nr_cpf_candidato varchar [primary key]
  nm_candidato varchar [not null]
  nm_urna_candidato varchar
  dt_nascimento date
  ds_genero varchar
  ds_grau_instrucao varchar
  ds_estado_civil varchar
  ds_ocupacao varchar
  sg_uf_nascimento varchar(2)
  nm_municipio_nascimento varchar
}

Table ELEICAO {
  nr_eleicao int [primary key]
  ds_eleicao varchar [not null]
  cd_tipo_eleicao varchar
  dt_eleicao date
}

Table PARTIDO {
  nr_partido int [primary key]
  sg_partido varchar(20) [not null]
  nm_partido varchar [not null]
}

Table COLIGACAO {
  sq_coligacao bigint [primary key]
  nr_eleicao int [ref: > ELEICAO.nr_eleicao]
  nm_coligacao varchar
  sg_uf varchar(2)
  tp_agremiacao varchar
}

Table CANDIDATURA {
  sq_candidato bigint [primary key]
  nr_cpf_candidato varchar [ref: > CANDIDATO.nr_cpf_candidato]
  nr_eleicao int [ref: > ELEICAO.nr_eleicao]
  nr_partido int [ref: > PARTIDO.nr_partido]
  sq_coligacao bigint [ref: > COLIGACAO.sq_coligacao]
  nm_urna_candidato varchar
  cd_cargo varchar
  ds_cargo varchar
  sg_uf varchar(2)
  nr_candidato int
  cd_situacao_candidatura varchar
  ds_situacao_candidatura varchar
  nr_votos int
  cd_sit_tot_turno varchar
}

Table BEM_CANDIDATO {
  id_bem bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  nr_ordem_bem int
  cd_tipo_bem varchar
  ds_tipo_bem varchar
  vr_bem decimal(15,2)
}

Table REDE_SOCIAL {
  id_rede_social bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  ds_url varchar
  cd_tipo_rede_social varchar
}

Table PROPOSTA_GOVERNO {
  id_proposta bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  nm_arquivo varchar
  ds_caminho_arquivo varchar
  tx_conteudo_extraido text
  st_processado boolean [default: false]
  dt_processamento datetime
}

Table RESUMO_PROPOSTA {
  id_resumo bigint [primary key, increment]
  id_proposta bigint [ref: > PROPOSTA_GOVERNO.id_proposta]
  ds_tema varchar
  tx_resumo text
  dt_geracao datetime
}

Table CERTIDAO_CRIMINAL {
  id_certidao bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  nm_arquivo varchar
  ds_caminho_arquivo varchar
  dt_emissao date
  dt_validade date
}

Table MOTIVO_CASSACAO {
  id_cassacao bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  cd_motivo varchar
  ds_motivo varchar
  dt_decisao date
  ds_orgao varchar
}

Table NOTA_FISCAL {
  id_nota bigint [primary key, increment]
  sq_candidato bigint [ref: > CANDIDATURA.sq_candidato]
  nr_nota_fiscal varchar
  nm_fornecedor varchar
  cd_tipo_despesa varchar
  vr_despesa decimal(15,2)
  dt_despesa date
}
