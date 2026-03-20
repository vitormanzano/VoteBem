# Modelo Conceitual para o Banco de Dados usando PostgreSQL

## Tabelas

### Candidato

<p><strong>nr_cpf_candidato:</strong> CPF do candidato. Chave primária que identifica a pessoa física de forma única entre todas as eleições.</p>
<p><strong>nm_candidato:</strong> Nome civil completo do candidato, como consta nos documentos oficiais.</p>
<p><strong>nm_urna_candidato:</strong> Nome que aparece na urna eletrônica. Ex: "LULA", "BOLSONARO".</p>
<p><strong>dt_nascimento:</strong> Data de nascimento do candidato.</p>
<p><strong>ds_genero:</strong> Gênero declarado. Ex: "MASCULINO", "FEMININO".</p>
<p><strong>ds_grau_instrucao:</strong> Escolaridade declarada. Ex: "SUPERIOR COMPLETO", "ENSINO MÉDIO COMPLETO".</p>
<p><strong>ds_estado_civil:</strong> Estado civil declarado. Ex: "CASADO(A)", "SOLTEIRO(A)".</p>
<p><strong>ds_ocupacao:</strong> Ocupação declarada ao TSE. Ex: "SERVIDOR PÚBLICO", "EMPRESÁRIO".</p>
<p><strong>sg_uf_nascimento:</strong> Sigla do estado onde nasceu. Ex: "SP", "BA".</p>
<p><strong>nm_municipio_nascimento:</strong> Nome do município onde nasceu.</p>

### Eleicao

<p><strong>nr_eleicao:</strong> Número identificador da eleição no TSE. Chave primária. Geralmente o próprio ano. Ex: 2022, 2018.</p>
<p><strong>ds_eleicao:</strong> Descrição completa da eleição. Ex: "ELEIÇÃO GERAL FEDERAL 2022".</p>
<p><strong>cd_tipo_eleicao:</strong> Código do tipo da eleição no TSE. Ex: "2" para eleição ordinária.</p>
<p><strong>dt_eleicao:</strong> Data em que a eleição foi realizada.</p>

### Partido

<p><strong>nr_partido:</strong> Número do partido na urna eletrônica. Chave primária. Ex: 13 para o PT, 22 para o PL.</p>
<p><strong>sg_partido:</strong> Sigla do partido. Ex: "PT", "PL", "MDB".</p>
<p><strong>nm_partido:</strong> Nome completo do partido. Ex: "PARTIDO DOS TRABALHADORES".</p>

### Coligacao

<p><strong>sq_coligacao:</strong> Código identificador único da coligação no TSE. Chave primária.</p>
<p><strong>nr_eleicao:</strong> Referência à eleição em que a coligação foi formada. Chave estrangeira para Eleicao.</p>
<p><strong>nm_coligacao:</strong> Nome dado à coligação. Ex: "BRASIL DA ESPERANÇA".</p>
<p><strong>sg_uf:</strong> Estado ao qual a coligação pertence. Para presidência, é "BR".</p>
<p><strong>tp_agremiacao:</strong> Tipo da agremiação. Ex: "COLIGAÇÃO", "FEDERAÇÃO", "PARTIDO ISOLADO".</p>

### Candidatura

<p><strong>sq_candidato:</strong> Chave primária gerada pelo TSE. Identifica unicamente aquela candidatura específica.</p>
<p><strong>nr_cpf_candidato:</strong> Referência ao candidato (pessoa física) que disputou essa eleição. Chave estrangeira para Candidato.</p>
<p><strong>nr_eleicao:</strong> Referência à eleição em que essa candidatura ocorreu. Chave estrangeira para Eleicao.</p>
<p><strong>nr_partido:</strong> Referência ao partido pelo qual o candidato concorreu. Chave estrangeira para Partido.</p>
<p><strong>sq_coligacao:</strong> Referência à coligação da qual o candidato fazia parte. Chave estrangeira para Coligacao.</p>
<p><strong>nm_urna_candidato:</strong> Nome de urna usado especificamente nessa candidatura.</p>
<p><strong>cd_cargo:</strong> Código do cargo disputado no TSE. Ex: "1" para Presidente.</p>
<p><strong>ds_cargo:</strong> Descrição do cargo. Ex: "PRESIDENTE", "GOVERNADOR".</p>
<p><strong>sg_uf:</strong> Estado onde concorreu. Para presidência, é "BR".</p>
<p><strong>nr_candidato:</strong> Número do candidato na urna eletrônica nessa eleição.</p>
<p><strong>cd_situacao_candidatura:</strong> Código da situação da candidatura no TSE.</p>
<p><strong>ds_situacao_candidatura:</strong> Descrição da situação. Ex: "APTO", "INAPTO", "CASSADO".</p>
<p><strong>nr_votos:</strong> Total de votos recebidos nessa eleição.</p>
<p><strong>cd_sit_tot_turno:</strong> Resultado final. Ex: "ELEITO", "NÃO ELEITO", "2º TURNO".</p>

### Bem_Candidato

<p><strong>id_bem:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura à qual esse bem pertence. Chave estrangeira para Candidatura.</p>
<p><strong>nr_ordem_bem:</strong> Número de ordem do bem dentro da declaração. Ex: 1º bem, 2º bem.</p>
<p><strong>cd_tipo_bem:</strong> Código do tipo de bem no TSE. Ex: "11" para imóvel.</p>
<p><strong>ds_tipo_bem:</strong> Descrição do tipo. Ex: "CASA", "APARTAMENTO", "VEÍCULO", "APLICAÇÃO FINANCEIRA".</p>
<p><strong>vr_bem:</strong> Valor declarado do bem em reais.</p>

### Rede_Social

<p><strong>id_rede_social:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura dona dos perfis. Chave estrangeira para Candidatura.</p>
<p><strong>ds_url:</strong> URL completa do perfil. Ex: "https://instagram.com/nomedocandidato".</p>
<p><strong>cd_tipo_rede_social:</strong> Tipo da rede social identificado pela plataforma. Ex: "INSTAGRAM", "FACEBOOK", "X", "YOUTUBE".</p>

### Proposta_Governo

<p><strong>id_proposta:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura dona da proposta. Chave estrangeira para Candidatura.</p>
<p><strong>nm_arquivo:</strong> Nome original do arquivo PDF no TSE.</p>
<p><strong>ds_caminho_arquivo:</strong> Caminho onde o PDF está armazenado no servidor da plataforma.</p>
<p><strong>tx_conteudo_extraido:</strong> Texto completo extraído do PDF para ser processado pela IA.</p>
<p><strong>st_processado:</strong> Indica se a IA já processou esse PDF. "true" = processado, "false" = pendente.</p>
<p><strong>dt_processamento:</strong> Data e hora em que o processamento pela IA foi concluído.</p>

### Resumo_Proposta

<p><strong>id_resumo:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>id_proposta:</strong> Referência à proposta de governo que originou esse resumo. Chave estrangeira para Proposta_Governo.</p>
<p><strong>ds_tema:</strong> Tema identificado pela IA. Ex: "Saúde", "Educação", "Segurança Pública".</p>
<p><strong>tx_resumo:</strong> Texto do resumo gerado pela IA em linguagem simples para aquele tema.</p>
<p><strong>dt_geracao:</strong> Data e hora em que a IA gerou esse resumo.</p>

### Certidao_Criminal

<p><strong>id_certidao:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura dona da certidão. Chave estrangeira para Candidatura.</p>
<p><strong>nm_arquivo:</strong> Nome original do arquivo PDF da certidão no TSE.</p>
<p><strong>ds_caminho_arquivo:</strong> Caminho onde o PDF está armazenado no servidor da plataforma.</p>
<p><strong>dt_emissao:</strong> Data em que a certidão foi emitida.</p>
<p><strong>dt_validade:</strong> Data de validade da certidão. Usada para sinalizar certidões desatualizadas.</p>

### Motivo_Cassacao

<p><strong>id_cassacao:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura cassada. Chave estrangeira para Candidatura.</p>
<p><strong>cd_motivo:</strong> Código do motivo da cassação no TSE.</p>
<p><strong>ds_motivo:</strong> Descrição do motivo. Ex: "ABUSO DE PODER ECONÔMICO".</p>
<p><strong>dt_decisao:</strong> Data em que a decisão de cassação foi proferida.</p>
<p><strong>ds_orgao:</strong> Órgão que proferiu a decisão. Ex: "TSE", "TRE-SP".</p>

### Nota_Fiscal

<p><strong>id_nota:</strong> Identificador interno gerado pela plataforma. Chave primária.</p>
<p><strong>sq_candidato:</strong> Referência à candidatura que realizou o gasto. Chave estrangeira para Candidatura.</p>
<p><strong>nr_nota_fiscal:</strong> Número da nota fiscal emitida pelo fornecedor.</p>
<p><strong>nm_fornecedor:</strong> Nome do fornecedor ou empresa que prestou o serviço.</p>
<p><strong>cd_tipo_despesa:</strong> Código da categoria de despesa no TSE.</p>
<p><strong>vr_despesa:</strong> Valor da despesa em reais.</p>
<p><strong>dt_despesa:</strong> Data em que a despesa foi realizada.</p>
