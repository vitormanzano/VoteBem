# VoteBem
Projeto Integrador V

## Setup

### Requisitos
<ul>
  <li>
    Python 3.12
    <p> Download: https://www.python.org/downloads/ </p>
  </li>
  <li>
    Docker + Docker compose v2
    <p> Download: https://www.docker.com/get-started/ </p>
  </li>
  <li>
    .env na raiz do projeto.
  </li>
</ul>

### 1. Inicializar projeto.
Na raiz do repositório, execute:

```bash
docker pull postgres:16
```
Faz upload da imagem do postgres:16

```bash
python setup.py
```
Esse comando irá:
<ul>
  <li>Subir o container Docker com PostgreSQL e aguardar até que ele possa receber conexões.</li>
  <li>Criar a venv em .venv/ e instalar as dependências do ETL.</li>
  <li>
    Executar o pipeline: baixa os datasets do TSE e popula as tabelas.
    <p>Flags opcionais: --skip-docker (Não sobe o Postgres) e --skip-pipeline (Não roda o ETL).</p>
  </li>
</ul>
