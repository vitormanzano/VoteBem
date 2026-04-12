# Modelo Conceitual para o Banco de Dados usando PostgreSQL
<p> O arquivo dbdiagram.md é o código para gerar o MER no site dbdiagram.io </p>
## Tabelas

### Eleicao

<p><strong>cd_eleicao:</strong> Número identificador da eleição no TSE. Chave primária composta.</p>
<p><strong>nr_turno:</strong> Número do turno da eleição. Primeiro ou segundo. Chave primária composta.</p>
<p><strong>ano_eleicao:</strong> Ano em que ocorreu a eleição.</p>
<p><strong>cd_tipo_eleicao:</strong> Código do tipo da eleição no TSE. Ex: "2" para eleição ordinária.</p>
<p><strong>nm_tipo_eleicao:</strong> Nome do tipo da eleição. Ex: Eleição Ordinária.</p>
<p><strong>ds_eleicao:</strong> Descrição completa da eleição. Ex: "ELEIÇÃO GERAL FEDERAL 2022".</p>
<p><strong>dt_eleicao:</strong> Data em que a eleição foi realizada.</p>
<p><strong>Chave primária:</strong> Chave primária composta por (cd_eleicao, nr_turno).</p>

### Partido

<p><strong>nr_partido:</strong> Número do partido na urna eletrônica. Chave primária. Ex: 13 para o PT, 22 para o PL.</p>
<p><strong>sg_partido:</strong> Sigla do partido. Ex: "PT", "PL", "MDB".</p>
<p><strong>nm_partido:</strong> Nome completo do partido. Ex: "PARTIDO DOS TRABALHADORES".</p>

### Candidato

<p><strong>nr_cpf_candidato:</strong> CPF do candidato. Chave primária que identifica a pessoa física de forma única entre todas as eleições.</p>
<p><strong>nm_candidato:</strong> Nome civil completo do candidato, como consta nos documentos oficiais.</p>
<p><strong>nm_social_candidato:</strong> Nome social do candidato.</p>
<p><strong>nm_urna_candidato:</strong> Nome que aparece na urna eletrônica. Ex: "LULA", "BOLSONARO".</p>
<p><strong>dt_nascimento:</strong> Data de nascimento do candidato.</p>
<p><strong>sg_uf_nascimento:</strong> Sigla do estado onde nasceu. Ex: "SP", "BA".</p>
<p><strong>cd_genero:</strong> Código do gênero do candidato.</p>
<p><strong>ds_genero:</strong> Gênero declarado. Ex: "MASCULINO", "FEMININO".</p>
<p><strong>cd_grau_instrucao:</strong> Código do grau de instrução do candidato.</p>
<p><strong>ds_grau_instrucao:</strong> Escolaridade declarada. Ex: "SUPERIOR COMPLETO", "ENSINO MÉDIO COMPLETO".</p>
<p><strong>cd_estado_civil:</strong> Código do estado civil do candidato.</p>
<p><strong>ds_estado_civil:</strong> Estado civil declarado. Ex: "CASADO(A)", "SOLTEIRO(A)".</p>
<p><strong>cd_cor_raca:</strong> Código da cor/raça do candidato.</p>
<p><strong>ds_cor_raca:</strong> Cor/raça declarada do candidato.</p>

### Coligacao

<p><strong>sq_coligacao:</strong> Código identificador único da coligação no TSE. Chave primária.</p>
<p><strong>cd_eleicao:</strong> Referência à eleição em que a coligação foi formada. Chave estrangeira para Eleicao.</p>
<p><strong>nr_turno:</strong> Turno da eleição. Chave estrangeira composta com cd_eleicao para Eleicao.</p>
<p><strong>nm_coligacao:</strong> Nome dado à coligação. Ex: "BRASIL DA ESPERANÇA".</p>
<p><strong>ds_composicao_coligacao:</strong> Descrição dos partidos que compõem a coligação. Ex: "PT / PCdoB / PV".</p>
<p><strong>tp_agremiacao:</strong> Tipo da agremiação. Ex: "COLIGAÇÃO", "FEDERAÇÃO", "PARTIDO ISOLADO".</p>
<p><strong>sg_uf:</strong> Estado ao qual a coligação pertence. Para presidência, é "BR".</p>

### Candidatura

<p><strong>sq_candidato:</strong> Chave primária gerada pelo TSE. Identifica unicamente aquela candidatura específica.</p>
<p><strong>nr_cpf_candidato:</strong> Referência ao candidato (pessoa física) que disputou essa eleição. Chave estrangeira para Candidato.</p>
<p><strong>cd_eleicao:</strong> Referência à eleição em que essa candidatura ocorreu.</p>
<p><strong>nr_partido:</strong> Referência ao partido pelo qual o candidato concorreu. Chave estrangeira para Partido.</p>
<p><strong>sq_coligacao:</strong> Referência à coligação da qual o candidato fazia parte. Chave estrangeira para Coligacao.</p>
<p><strong>nm_urna_candidato:</strong> Nome de urna usado especificamente nessa candidatura.</p>
<p><strong>cd_cargo:</strong> Código do cargo disputado no TSE. Ex: "1" para Presidente, "2" para Vice-Presidente.</p>
<p><strong>ds_cargo:</strong> Descrição do cargo. Ex: "PRESIDENTE", "VICE-PRESIDENTE".</p>
<p><strong>sg_uf:</strong> Estado onde concorreu. Para presidência, é "BR".</p>
<p><strong>nr_candidato:</strong> Número do candidato na urna eletrônica nessa eleição.</p>
<p><strong>cd_situacao_candidatura:</strong> Código da situação da candidatura no TSE.</p>
<p><strong>ds_situacao_candidatura:</strong> Descrição da situação. Ex: "APTO", "INAPTO", "CASSADO".</p>
<p><strong>cd_ocupacao:</strong> Código da ocupação do candidato no TSE.</p>
<p><strong>ds_ocupacao:</strong> Ocupação declarada ao TSE. Ex: "SERVIDOR PÚBLICO", "EMPRESÁRIO".</p>
<p><strong>foto_url:</strong> Caminho relativo (a partir de data/raw) para a foto oficial do candidato.</p>
<p><strong>st_reeleicao:</strong> Indica se o candidato concorre à reeleição. "S" = sim, "N" = não.</p>
<p><strong>vr_despesa_max_campanha:</strong> Valor máximo de despesa de campanha permitido para o candidato.</p>

### Resultado_Turno

<p><strong>sq_candidato:</strong> Referência à candidatura. Chave estrangeira para Candidatura. Chave primária composta.</p>
<p><strong>cd_eleicao:</strong> Referência à eleição do turno. Chave estrangeira composta com nr_turno para Eleicao.</p>
<p><strong>nr_turno:</strong> Número do turno (1 ou 2). Chave primária composta.</p>
<p><strong>nr_votos:</strong> Total de votos nominais recebidos pelo candidato nesse turno. Default 0.</p>
<p><strong>cd_sit_tot_turno:</strong> Código do resultado final do turno.</p>
<p><strong>ds_sit_tot_turno:</strong> Descrição do resultado final. Ex: "ELEITO", "NÃO ELEITO", "2º TURNO".</p>
<p><strong>Chave primária:</strong> Chave primária composta por (sq_candidato, nr_turno).</p>

### Bem_Candidato

<p><strong>sq_candidato:</strong> Referência à candidatura à qual esse bem pertence. Chave estrangeira para Candidatura. Chave primária composta.</p>
<p><strong>nr_ordem_bem:</strong> Número de ordem do bem dentro da declaração. Ex: 1º bem, 2º bem. Chave primária composta.</p>
<p><strong>cd_tipo_bem:</strong> Código do tipo de bem no TSE. Ex: "11" para imóvel.</p>
<p><strong>ds_tipo_bem:</strong> Descrição do tipo. Ex: "CASA", "APARTAMENTO", "VEÍCULO", "APLICAÇÃO FINANCEIRA".</p>
<p><strong>ds_bem:</strong> Descrição detalhada do bem declarado.</p>
<p><strong>vr_bem:</strong> Valor declarado do bem em reais.</p>
<p><strong>Chave primária:</strong> Chave primária composta por (sq_candidato, nr_ordem_bem).</p>

### Rede_Social

<p><strong>sq_candidato:</strong> Referência à candidatura dona dos perfis. Chave estrangeira para Candidatura. Chave primária composta.</p>
<p><strong>nr_ordem:</strong> Número de ordem da rede social na lista. Chave primária composta.</p>
<p><strong>ds_url:</strong> URL completa do perfil. Ex: "https://instagram.com/nomedocandidato".</p>
<p><strong>tipo_rede_social:</strong> Tipo da rede social identificado. Ex: "INSTAGRAM", "FACEBOOK", "X", "YOUTUBE".</p>
<p><strong>Chave primária:</strong> Chave primária composta por (sq_candidato, nr_ordem).</p>

### Proposta_Governo

<p><strong>sq_candidato:</strong> Referência à candidatura dona da proposta. Chave primária e chave estrangeira para Candidatura (relação 1:1).</p>
<p><strong>nm_arquivo:</strong> Nome original do arquivo PDF no TSE.</p>
<p><strong>ds_caminho_arquivo:</strong> Caminho onde o PDF está armazenado no servidor da plataforma.</p>
<p><strong>tx_conteudo_extraido:</strong> Texto completo extraído do PDF para ser processado pela IA.</p>
<p><strong>st_processado:</strong> Indica se a IA já processou esse PDF. "true" = processado, "false" = pendente.</p>
<p><strong>dt_processamento:</strong> Data e hora em que o processamento pela IA foi concluído.</p>

### Resumo_Proposta

<p><strong>id_resumo:</strong> Identificador auto-gerado. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à proposta de governo que originou esse resumo. Chave estrangeira para Proposta_Governo.</p>
<p><strong>ds_tema:</strong> Tema identificado pela IA. Ex: "Saúde", "Educação", "Segurança Pública".</p>
<p><strong>tx_resumo:</strong> Texto do resumo gerado pela IA em linguagem simples para aquele tema.</p>
<p><strong>dt_geracao:</strong> Data e hora em que a IA gerou esse resumo.</p>

### Certidao_Criminal

<p><strong>id_certidao:</strong> Identificador presente no nome do arquivo. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura dona da certidão. Chave estrangeira para Candidatura.</p>
<p><strong>nm_arquivo:</strong> Nome original do arquivo PDF da certidão no TSE.</p>
<p><strong>ds_caminho_arquivo:</strong> Caminho onde o PDF está armazenado no servidor da plataforma.</p>

### Motivo_Cassacao

<p><strong>sq_candidato:</strong> Referência à candidatura cassada. Chave estrangeira para Candidatura. Chave primária composta.</p>
<p><strong>ds_tp_motivo:</strong> Tipo do motivo da cassação.</p>
<p><strong>ds_motivo:</strong> Descrição do motivo. Ex: "ABUSO DE PODER ECONÔMICO". Chave primária composta.</p>
<p><strong>Chave primária:</strong> Chave primária composta por (sq_candidato, ds_motivo).</p>

### Despesa_Candidato

<p><strong>id_despesa:</strong> Identificador auto-gerado. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura que realizou o gasto. Chave estrangeira para Candidatura.</p>
<p><strong>nr_documento:</strong> Número do documento da despesa.</p>
<p><strong>cpf_cnpj_fornecedor:</strong> CPF ou CNPJ do fornecedor.</p>
<p><strong>nm_fornecedor:</strong> Nome do fornecedor ou empresa que prestou o serviço.</p>
<p><strong>dt_despesa:</strong> Data em que a despesa foi realizada.</p>
<p><strong>vr_despesa:</strong> Valor da despesa em reais.</p>
<p><strong>ds_tipo_despesa:</strong> Categoria da despesa. Ex: "PUBLICIDADE", "TRANSPORTE".</p>
<p><strong>ds_fonte_recurso:</strong> Fonte do recurso utilizado. Ex: "FUNDO PARTIDÁRIO", "FUNDO ESPECIAL".</p>
<p><strong>ds_especie_recurso:</strong> Espécie do recurso. Ex: "TRANSFERÊNCIA ELETRÔNICA".</p>
<p><strong>ds_despesa:</strong> Descrição detalhada da despesa.</p>
<p><strong>Restrição UNIQUE:</strong> (sq_candidato, nr_documento, cpf_cnpj_fornecedor, dt_despesa).</p>

### Nota_Fiscal

<p><strong>id_nota:</strong> Identificador auto-gerado. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura que realizou o gasto. Chave estrangeira para Candidatura.</p>
<p><strong>nr_nota_fiscal:</strong> Número da nota fiscal emitida pelo fornecedor.</p>
<p><strong>nr_serie:</strong> Número de série da nota fiscal.</p>
<p><strong>cpf_cnpj_emitente:</strong> CPF ou CNPJ do emitente da nota fiscal.</p>
<p><strong>dt_emissao:</strong> Data de emissão da nota fiscal.</p>
<p><strong>vr_nota_fiscal:</strong> Valor da nota fiscal em reais.</p>
<p><strong>nr_chave_acesso:</strong> Chave de acesso da nota fiscal eletrônica (NF-e).</p>
<p><strong>nm_url_acesso:</strong> URL para acesso/consulta da nota fiscal.</p>
<p><strong>Restrição UNIQUE:</strong> (sq_candidato, nr_nota_fiscal, cpf_cnpj_emitente).</p>
