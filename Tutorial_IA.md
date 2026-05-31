# VoteBem — Tutorial: Rodando a IA localmente

Este guia é para membros do grupo que querem integrar o backend com a IA e fazer testes locais.

---

## Pré-requisitos

- Python 3.11 ou superior
- Docker Desktop instalado e rodando
- [Ollama](https://ollama.com/download) instalado

---

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/VoteBem.git
cd VoteBem
```

---

## 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

---

## 3. Instalar dependências do backend

```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv httpx
```

---

## 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Preencha o `.env` com os dados do banco:

```dotenv
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB_NAME=VoteBem
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

---

## 5. Subir o banco de dados

```bash
docker compose up -d
```

Se for a primeira vez, rode o setup para popular o banco:

```bash
pip install -r etl/requirements.txt
python setup.py
```

> Isso pode demorar entre 30 minutos e 2 horas na primeira vez.

---

## 6. Configurar o modelo de IA

**6.1. Baixar o modelo base:**

```bash
ollama pull phi3.5
```

**6.2. Registrar o modelo do VoteBem:**

```bash
ollama create votebem -f src/backend/modelo_votebem_merged/Modelfile
```

**6.3. Testar se está funcionando:**

```bash
ollama run votebem "Quais candidatos concorreram à presidência em 2022?"
```

Deve responder em português com dados sobre as eleições. Para sair, digite `/bye`.

---

## 7. Subir o backend

```bash
cd src/backend
uvicorn main:app --reload
```

Acesse `http://localhost:8000/health` — deve retornar `{"status": "ok"}`.

---

## 8. Abrir o frontend

Abra o arquivo abaixo no navegador:

```
src/frontend/VoteBem/voto Consciente/index.html
```

---

## Inicializar o projeto toda vez

Sempre que for trabalhar no projeto:

```bash
# Terminal 1 — banco
docker compose up -d

# Terminal 2 — backend
source .venv/bin/activate
cd src/backend
uvicorn main:app --reload
```

Depois abra o `index.html` no navegador.

---

## Solução de problemas

**`ollama create` falha com erro de arquivo não encontrado**
Verifique se o arquivo `src/backend/modelo_votebem_merged/Modelfile` existe no repositório.

**Backend retorna erro de conexão com o banco**
Certifique-se de que o Docker está rodando: `docker ps`

**Modelo não responde ou responde em outro idioma**
Verifique se o modelo foi registrado corretamente: `ollama list` — deve aparecer `votebem` na lista.

**Porta 8000 já em uso**
```bash
uvicorn main:app --reload --port 8001
```
