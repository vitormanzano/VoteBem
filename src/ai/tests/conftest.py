"""Configuração compartilhada do pytest para os testes do módulo de IA.

Ajusta sys.path para permitir imports diretos (config, db, embeddings,
chat.*, retrieval.*, ingest.*) quando os testes rodam de qualquer
diretório.
"""
import sys
from pathlib import Path

# adiciona src/ai/ ao path antes que qualquer teste importe módulos do projeto
_AI_ROOT = Path(__file__).resolve().parent.parent
if str(_AI_ROOT) not in sys.path:
    sys.path.insert(0, str(_AI_ROOT))
