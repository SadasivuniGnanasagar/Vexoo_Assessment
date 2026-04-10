from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import torch

# -------------------
# Load Dataset
# -------------------
dataset = load_dataset("gsm8k", "main")

train_data = dataset["train"].select(range(50))   # reduced for laptop
test_data = dataset["test"].select(range(20))

# -------------------
# Model + Tokenizer
# -------------------
model_name = "distilgpt2"  # lightweight instead of LLaMA

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def tokenize(example):
    texts = []

    for q, a in zip(example["question"], example["answer"]):
        texts.append(q + " " + a)

    tokenized = tokenizer(
        texts,
        truncation=True,
        padding="max_length",
        max_length=128
    )

    
    tokenized["labels"] = tokenized["input_ids"].copy()

    return tokenized


train_data = train_data.map(tokenize, batched=True)
test_data = test_data.map(tokenize, batched=True)

# -------------------
# Model
# -------------------
model = AutoModelForCausalLM.from_pretrained(model_name)

# -------------------
# LoRA
# -------------------
lora_config = LoraConfig(
    r=4,
    lora_alpha=8,
    target_modules=["c_attn"],
    lora_dropout=0.1,
    bias="none"
)

model = get_peft_model(model, lora_config)

# -------------------
# Training args
# -------------------
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    logging_steps=10,
    save_strategy="no"
)

# -------------------
# Trainer
# -------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data
)

# -------------------
# Train
# -------------------
trainer.train()

print("\nTraining Done!")

# -------------------
# Evaluation
# -------------------
correct = 0

for example in test_data:
    inputs = tokenizer(example["question"], return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=20)
    pred = tokenizer.decode(outputs[0])

    if example["answer"].split()[0] in pred:
        correct += 1

accuracy = correct / len(test_data)

print("\nAccuracy:", accuracy)