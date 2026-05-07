"""
merge_modelo.py - Mescla LoRA com modelo base (AMD/ROCm fix)
"""
import torch
import transformers.modeling_utils as mu

# Monkey-patch para corrigir bug do Phi-3.5 com tied weights
def _safe_get_tied(module):
    try:
        tied_weight_keys = []
        if hasattr(module, "_tied_weights_keys") and isinstance(module._tied_weights_keys, list):
            tied_weight_keys.extend(module._tied_weights_keys)
        for name, submodule in module.named_children():
            for key in _safe_get_tied(submodule):
                tied_weight_keys.append(f"{name}.{key}")
        return tied_weight_keys
    except Exception:
        return []

mu._get_tied_weight_keys = _safe_get_tied

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
model.save_pretrained(OUTPUT_DIR, safe_serialization=False, max_shard_size="2GB")
tokenizer.save_pretrained(OUTPUT_DIR)
print("Pronto! Agora rode: python registrar_ollama.py")
# já substituído acima, só adiciona o max_shard_size
