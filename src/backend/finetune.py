"""
finetune.py - Fine-tuning do Phi-3-mini com dados politicos
"""
import torch
import json
import os
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType

MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"
OUTPUT_DIR = "./modelo_votebem"
DATASET_PATH = "./dataset_politico.json"
MAX_SEQ_LENGTH = 512

def carregar_dataset(tokenizer):
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
    print(f"Dataset carregado: {len(dados)} exemplos")

    def tokenizar(exemplo):
        result = tokenizer(
            exemplo["text"],
            truncation=True,
            max_length=MAX_SEQ_LENGTH,
            padding="max_length",
        )
        result["labels"] = result["input_ids"].copy()
        return result

    dataset = Dataset.from_list(dados)
    dataset = dataset.map(tokenizar, remove_columns=["text"])
    return dataset

def treinar():
    print("Verificando GPU...")
    if not torch.cuda.is_available():
        raise RuntimeError("GPU nao encontrada.")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    print(f"Carregando modelo: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="eager",
    )
    model.config.use_cache = False

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = carregar_dataset(tokenizer)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=5,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=20,
        save_steps=100,
        save_total_limit=2,
        warmup_steps=20,
        lr_scheduler_type="cosine",
        report_to="none",
        optim="paged_adamw_8bit",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    print("\nIniciando treinamento...")
    trainer.train()

    print("\nSalvando modelo...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Modelo salvo em: {OUTPUT_DIR}")
    print("Proximo passo: python merge_modelo.py")

if __name__ == "__main__":
    treinar()