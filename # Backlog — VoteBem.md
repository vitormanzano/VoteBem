# Backlog — VoteBem

## 1- Infraestrutura

Prioridade: Alta
Tasks:

- Configurar banco PostgreSQL
- Criar schema conforme MER
- Configurar variáveis de ambiente (.env)


Critérios de aceite:

-> Banco acessível localmente e remotamente
-> Schema criado sem erros
-> Variáveis sensíveis não expostas no código

## 2 - ETL — Importação de Dados do TSE (Python)

## 2.1 - Importação de dados eleitorais

Prioridade: Alta
Tasks:

- Implementar download automático dos arquivos CSV/ZIP do portal dadosabertos.tse.jus.br
-Implementar processamento e carga dos dados de candidatos no banco
-Implementar processamento e carga dos dados de bens declarados no banco
-Implementar processamento e carga dos dados de redes sociais no banco
-Implementar processamento e carga das certidões criminais no banco
-Implementar processamento e carga dos motivos de cassação no banco
-Implementar processamento e carga das notas fiscais de campanha no banco


Critérios de aceite:

-> Dados inseridos corretamente no banco
-> Dados consistentes (sem duplicação)
-> Logs de execução disponíveis


## 2.2 - Agendamento e tolerância

Prioridade: Média
Tasks: 

-Implementar agendamento da importação (diário em período eleitoral, semanal nos demais)
-Implementar tolerância a falhas — manter dados da última importação bem-sucedida em caso de erro


Critérios de aceite:

-> Execução automática funcional
-> Em caso de erro, sistema mantém dados anteriores


## 3 - Backend (API .NET)


## 3.1 - Listagem de candidatos

Prioridade: Alta
Tasks:

-Endpoint de listagem paginada de candidatos
-Filtros básicos

Critérios de aceite:
-> Paginção funcional


## 3.2 - Busca de candidatos
Prioridade: Alta
Tasks:

-Endpoint de busca de candidatos por nome / nome de urna
-Endpoint de busca de candidatos por partido
-Endpoint de busca de candidatos por ano eleitoral

Critérios de aceite:

->Dados completos e organizados


## 3.3 - Perfil do candidato

Prioridade: Alta
Tasks:

-Endpoint de perfil completo do candidato
-Endpoint de patrimônio declarado do candidato
-Endpoint de histórico eleitoral do candidato
-Endpoint de situação jurídica do candidato (certidões e cassações)
-Endpoint de notas fiscais de campanha do candidato
-Endpoint de redes sociais do candidato

Critérios de aceite:

->Dados completos e organizados


## 4 - IA 

## 4.1 - Processamento de propostas

Prioridade: Alta
Tasks:

-Implementar download dos PDFs de propostas de governo do TSE
-Implementar extração de texto dos PDFs
-Implementar classificação das propostas por temas via IA
-Implementar geração de resumos por tema em linguagem simples
-Implementar processamento assíncrono em background (sem impactar a API)

Critérios de aceite:

-> Texto extraído corretamente
-> Resumos compreensíveis e em linguagem acessível
-> Classificação consistente
->API não bloqueia durante processamento


## 5 - Chatbot (Python)

## 5.1 - Consulta inteligente

Prioridade: Alta
Tasks:

-Interface de chatbot em linguagem natural
-Consulta a dados estruturados via chatbot (perfil, patrimônio, situação jurídica)
-Integração com API

Critérios de aceite:

-> Respostas corretas baseadas em dados


## 5.2 - Comparação de candidatos

Prioridade: Alta
Tasks:

-Comparação de propostas de governo de 2 a 4 candidatos via chatbot
-Garantir neutralidade — chatbot nunca emite opiniões ou sugere candidatos
-Garantir que o chatbot informe explicitamente quando um dado não estiver disponível

Critérios de aceite:

-> Comparação clara e estruturada
-> Nenhuma recomendação política
-> Transparência nas respostas


## 6 - Frontend (HTML/CSS/JS)

## 6.1 - Listagem e busca

Prioridade: Alta
Tasks:

-Página de listagem e busca de candidatos
-Página de perfil do candidato

Critérios de aceite:
-> Interface responsiva
-> Dados organizados e legíveis


## 6.2 - Visualização de dados

Prioridade: Média
Tasks:

-Gráfico de composição do patrimônio por categoria
-Gráfico de evolução patrimonial entre eleições
-Gráfico de evolução de votos por eleição
-Linha do tempo do histórico eleitoral

Critérios de aceite:
-> Gráficos claros e interativos

## 6.3 - Chatbot UI
Prioridade: Alta
Tasks:

-Interface do chatbot

Critérios de aceite:

-> Respostas legíveis e em tempo real

## 6.4 - Responsividade e acessibilidade
Prioridade: Média
Tasks:


-Responsividade para desktop, tablet e mobile
-Acessibilidade (textos alternativos, rótulos, compatibilidade com leitores de tela)

Critérios de aceite: 

-> Funciona em mobile e tablet
-> Compatível com leitores de tela
-> Textos alternativos e rótulos condizentes

------------------------------------------------------------

MVPs

## MVP(Entrega 1)

Infraestrutura:
ETL básico (candidatos + bens)

Backend:
Listagem
Busca
Perfil básico

Frontend:
Listagem
Perfil


## Versão 2:

Gráficos
Dados jurídicos
Notas fiscais


## Versão 3:

IA (resumos)
Chatbot