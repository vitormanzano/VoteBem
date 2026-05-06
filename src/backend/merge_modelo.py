"""
merge_modelo.py - Mescla LoRA com modelo base
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"
LORA_DIR = "./modelo_votebem"
OUTPUT_DIR = "./modelo_votebem_merged"

print("Carregando modelo base...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    device_map="cpu",
    trust_remote_code=True,
)

print("Carregando LoRA e mesclando...")
model = PeftModel.from_pretrained(model, LORA_DIR)
model = model.merge_and_unload()

print(f"Salvando em: {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("Pronto! Agora rode: python registrar_ollama.py")