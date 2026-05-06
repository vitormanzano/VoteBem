"""
registrar_ollama.py - Registra modelo treinado no Ollama
"""
import subprocess
import os

MODEL_DIR = "./modelo_votebem_merged"
MODEL_NAME = "votebem"

modelfile_content = f"""FROM {os.path.abspath(MODEL_DIR)}

SYSTEM \"\"\"Você é um assistente informativo do sistema Voto Consciente.
Apresente apenas dados objetivos sobre candidatos à presidência do Brasil.
Nunca invente informações. Nunca faça recomendações ou opiniões políticas.
Responda sempre em português do Brasil.\"\"\"

PARAMETER temperature 0.1
PARAMETER top_p 0.9
"""

modelfile_path = os.path.join(MODEL_DIR, "Modelfile")
with open(modelfile_path, "w", encoding="utf-8") as f:
    f.write(modelfile_content)

print(f"Registrando '{MODEL_NAME}' no Ollama...")
result = subprocess.run(
    ["ollama", "create", MODEL_NAME, "-f", modelfile_path],
    capture_output=True, text=True
)

if result.returncode == 0:
    print(f"Modelo '{MODEL_NAME}' registrado!")
    print(f"\nTroque no main.py:")
    print(f'  "model": "votebem"')
else:
    print("Erro:")
    print(result.stderr)