# Relatório: Adaptação do VoteBem para GPU AMD

**Projeto:** VoteBem — Voto Consciente  
**Data:** Maio de 2025  
**Hardware:** AMD Radeon RX 6600 (Navi 23, RDNA2, 8GB VRAM)  
**Sistema:** Zorin OS (baseado em Ubuntu 24.04 Noble)

---

## Contexto

O tutorial original do projeto foi desenvolvido exclusivamente para GPUs NVIDIA (CUDA). A adaptação foi necessária para rodar o pipeline de fine-tuning e inferência em uma GPU AMD, que utiliza a stack ROCm no lugar de CUDA.

---

## 1. Instalação do ROCm

O instalador oficial da AMD (`amdgpu-install`) não reconhece o Zorin OS como distribuição suportada. A solução foi adicionar os repositórios AMD manualmente:

```bash
wget https://repo.radeon.com/amdgpu-install/6.2/ubuntu/jammy/amdgpu-install_6.2.60200-1_all.deb
sudo apt install -y rocm-hip-sdk rocm-dev
sudo usermod -a -G render,video $USER
echo 'export HSA_OVERRIDE_GFX_VERSION=10.3.0' >> ~/.bashrc
```

A variável `HSA_OVERRIDE_GFX_VERSION=10.3.0` foi necessária para que o ROCm reconhecesse a arquitetura Navi 23 (gfx1030).

---

## 2. PyTorch com ROCm

O PyTorch foi instalado com suporte a ROCm 6.2 dentro do ambiente virtual do projeto:

```bash
pip install torch==2.5.1 torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/rocm6.2
```

> **Atenção:** O `pip install -r requirements.txt` do llama.cpp sobrescreveu o PyTorch ROCm pelo CPU durante a conversão GGUF. Foi necessário reinstalar o PyTorch ROCm após essa etapa.

---

## 3. Adaptações no `finetune.py`

O script original usava recursos exclusivos de NVIDIA que foram substituídos:

| Original (NVIDIA) | Adaptado (AMD) |
|---|---|
| `load_in_4bit=True` (bitsandbytes) | Removido — não suportado no ROCm |
| `optim="paged_adamw_8bit"` | `optim="adamw_torch"` |
| `target_modules=["q_proj","v_proj"]` | `target_modules=["qkv_proj","o_proj"]` |
| `torch_dtype=` | `dtype=` |
| `device_map="auto"` | `device_map="cuda:0"` |

O Phi-3.5 usa uma arquitetura de atenção combinada (`qkv_proj`) em vez de projeções separadas, o que exigiu a correção dos módulos-alvo do LoRA.

Também foram adicionados `gradient_checkpointing_enable()` e `gradient_accumulation_steps=8` para reduzir o consumo de VRAM durante o treinamento.

---

## 4. Merge do modelo

O `merge_modelo.py` falhou com um bug do transformers relacionado a `tied_weights` no Phi-3.5. A correção foi aplicar um monkey-patch na função `_get_tied_weight_keys` antes de salvar o modelo.

O salvamento foi feito com `safe_serialization=False` e `max_shard_size="2GB"` para evitar picos de memória que encerravam o processo. Foi necessário aumentar o swap do sistema para 8GB durante essa etapa.

---

## 5. Conversão para GGUF

O Ollama não suporta carregar modelos Phi-3.5 diretamente em formato safetensors. A conversão para GGUF foi feita via llama.cpp:

```bash
python3 ~/llama.cpp/convert_hf_to_gguf.py modelo_votebem_merged \
    --outfile votebem.gguf --outtype f16
```

Foi necessário copiar manualmente o `tokenizer.model` do cache do HuggingFace para a pasta do modelo antes da conversão.

---

## 6. Registro no Ollama

Devido a problemas de qualidade no modelo fine-tunado (outputs corrompidos causados pelos crashes de OOM durante o merge), optou-se por usar o modelo base `phi3.5` com um system prompt customizado:

```
FROM phi3.5
SYSTEM """Você é um assistente informativo do sistema Voto Consciente.
Responda perguntas sobre candidatos e eleições brasileiras com dados objetivos.
Nunca invente informações. Nunca faça recomendações políticas.
Responda sempre em português do Brasil.
Seja conciso e direto."""
PARAMETER temperature 0.1
PARAMETER repeat_penalty 1.3
PARAMETER num_predict 300
PARAMETER stop "<|end|>"
```

---

## Resultado

O sistema foi colocado em funcionamento com o backend FastAPI, banco PostgreSQL via Docker e interface de chat HTML conectada ao modelo via Ollama. O chat responde perguntas sobre candidatos e eleições brasileiras em português, com dados baseados no TSE.

---

## Pontos de Melhoria Futuros

- Refazer o fine-tuning com mais RAM disponível (ou em máquina com mais memória) para o merge não crashar
- Adicionar mais exemplos ao dataset de treinamento para reduzir alucinações
- Aumentar o swap permanentemente no sistema para evitar OOM em operações pesadas
