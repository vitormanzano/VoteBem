import os
from pathlib import Path

from dotenv import load_dotenv

_HERE = Path(__file__).resolve().parent
load_dotenv(_HERE / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB_NAME") or os.getenv("POSTGRES_DB", "VoteBem")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

EMBED_MODEL = os.getenv("EMBED_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))

AI_HOST = os.getenv("AI_HOST", "0.0.0.0")
AI_PORT = int(os.getenv("AI_PORT", "8001"))

# etl/data/storage/ é onde load_proposta_governo.py copiou os PDFs
STORAGE_DIR = _HERE.parents[1] / "etl" / "data" / "storage"

TEMAS = [
    "Saúde",
    "Educação",
    "Segurança Pública",
    "Economia",
    "Meio Ambiente",
    "Política Externa",
    "Direitos Humanos",
    "Infraestrutura",
    "Trabalho e Emprego",
    "Ciência e Tecnologia",
]
