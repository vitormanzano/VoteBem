# VoteBem

Projeto Integrador V

## Setup

### Requisitos

- Python 3.12  
  Download: [python.org/downloads](https://www.python.org/downloads/)

- Docker + Docker Compose v2  
  Download: [docker.com/get-started](https://www.docker.com/get-started/)

- .NET 10.0 SDK  
  Download: [dotnet.microsoft.com/en-us/download/dotnet/10.0](https://dotnet.microsoft.com/en-us/download/dotnet/10.0)

- Conta Groq + API key  
  Site: [console.groq.com](https://console.groq.com)

## Passos

### 1. Clonar repositório

No terminal, na pasta desejada para guardar o projeto, rode:

```bash
git clone https://github.com/seu-usuario/VoteBem.git
cd VoteBem
```

Clona o repositório e muda o diretório para a raiz do projeto.

### 2. Ambiente Python
Agora vamos criar o ambiente python para o projeto
** macOS / Linux: **
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r etl/requirements.txt
pip install -r src/ai/requirements.txt
```

** Windows (PowerShell): **jj
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r etl\requirements.txt
pip install -r src\ai\requirements.txt
```
Cria um ambiente isolado e instala as dependências necessárias para os módulos de etl e IA (src/ai).

> [!WARNING]
> OBS: A ativação do venv pode ser bloqueado no Windows, caso isso aconteça, esse comando pode ser útil:
> ```powershell
> Set-ExecutionPlicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> 
> Antes de apenas rodar o comando, pesquise sobre!

### 3. Variáveis de ambiente
Existem dois .env no projeto e uma configuração para user-secrets do .NET (backend)

#### 3.1 .env raiz - Usado pelo Docker e ETL
```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB_NAME=VoteBem
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

#### 3.2 src/ai/.env - Usado pela IA
```dotenv
# Groq
GROQ_API_KEY=sua_key
GROQ_MODEL=llama-3.3-70b-versatile
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB_NAME=VoteBem
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
# Embeddings
EMBED_MODEL=paraphrase-multilingual-MiniLM-L12-v2
EMBED_DIM=384
# FastAPI
AI_HOST=0.0.0.0
AI_PORT=8001
```

#### 3.3 user-secrets .NET
> [!TIP]
> `cd src/backend/Votebem`
>

dentro de `./VoteBem/src/backend/VoteBem` rode: 

```bash

dotnet user-secrets set "ConnectionStrings:PostgresConnection" "Host=localhost;Username=postgres;Password=postgres;Database=VoteBem"
dotnet user-secrets set "Ai:BaseUrl" "http://127.0.0.1:8001"
```

### 4. Subir banco de dados
> [!TIP]
> `cd ../../../`
>

Dentro de `./Votebem` rode:
```bash
docker compose up -d
```

Sobe Postgres 16 com a extensão pgvector habilitada

4.A Restore do dump
Em `db/dumps/votebem.dump` Existe um dump do pipeline da IA (~5.6 MB): Dados do TSE, chunks com embeddings e resumos por tema.

** macOS / Linux: **
```bash
scripts/resotre_db.sh
``` 

** Windows (PowerShell): **
```powershell
./scripts/restore_db.ps1
```

O Script copia o dump para o container, executa `pg_restore --clean`, e mostra a contagem final de candidaturas/chunks/resumos. Se tudo deu certo, pode ir para a seção 7 direto

#### 4.B Setup do zero
Popular banco do zero:

```bash
python setup.py
```

Se já tinha banco antigo (sem pgvector), aplique a migração não-destrutiva:

```bash
docker exec -i VoteBem sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < db/migrations/001_pgvector.sql
```

### 5. Ingestão das propostas
Extrai texto de cada pdf em `etl/data/storage/propostas/`, chunkifica, gera embeddings com `MiniLM-L12-v2`e popula `proposta_chunk`:

```bash
.venv/bin/python src/ai/ingest/extract_pdfs.py
```

Esperado: 42 propostas processadas

Validar:
```bash
docker exec VoteBem sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
SELECT ano_eleicao, COUNT(*) AS chunks FROM proposta_chunk GROUP BY ano_eleicao;"'
```

### 6. Geração offline de resumos por tema
Para cada candidato com chunks, gera 10 resumos (um por tema da taxanomia em `config.TEMAS`).

#### Comando com modelo 8B
```bash
# Gera para 2 próximos candidatos pendentes
.venv/bin/python src/ai/ingest/generate_summaries.py --limit 2 --model llama-3.1-8b-instant

# Ou tudo de uma vez (deixa rodando em background)
nohup .venv/bin/python -u src/ai/ingest/generate_summaries.py \
  --model llama-3.1-8b-instant > /tmp/batch_resumos.log 2>&1 &
disown
```

#### Comando com modelo 70B
```bash
.venv/bin/python src/ai/ingest/generate_summaries.py --only-sq 280001607829 --force
```
Sem `--model` usa o 70b do `.env`. `--force` substitui o resumo existente.

#### Progresso
```bash
docker exec VoteBem sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
SELECT c.nm_urna_candidato, e.ano_eleicao, COUNT(*) AS temas
  FROM resumo_proposta rp
  JOIN candidatura c ON c.sq_candidato=rp.sq_candidato
  JOIN eleicao e ON e.cd_eleicao=c.cd_eleicao
 GROUP BY c.nm_urna_candidato, e.ano_eleicao
 ORDER BY e.ano_eleicao, c.nm_urna_candidato;"'
```

### 7. Subir serviço de IA

** macOS / Linux: **
```bash
.venv/bin/uvicorn main:app --app-dir src/ai --host 127.0.0.1 --port 8001
```

** Windows (PowerShell): **
```powershell
.\.venv\Scripts\uvicorn.exe main:app --app-dir src\ai --host 127.0.0.1 --port 8001
```

Validar:

```bash
curl http://127.0.0.1:8001/health
```
Deve retornar : `# {"status":"ok","model":"llama-3.3-70b-versatile"}`

### 1. Inicializar projeto.
Na raiz do repositório, execute:

### Atalho para subir backend e frontend

** macOS / Linux: **
```bash
source start.sh
```

** Windows (PowerShell):  **
```powershell
./start.ps1
```

### 8. Subir o backend .NET (porta 5253)

```bash
cd src/backend/VoteBem
dotnet run --launch-profile http
```

O `AiController` faz proxy para o FastAPI nas chamadas de chat/comparação, e consulta o Postgres direto para os resumos pré-computados (`GET /ai/propostas/{sq}/resumos`).

### 9. Frontend
Sirva via http.

**macOS / Linux:**
```bash
dpython3 -m http.server 5500
# acessa http://localhost:5500/voto%20Consciente/chat.html
```

**Windows (PowerShell):**
```powershell
cd src\frontend\VoteBem
python -m http.server 5500
# acessa http://localhost:5500/voto%20Consciente/chat.html
```
