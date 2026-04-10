# Vexoo AI Assignment

## Setup
pip install transformers datasets peft accelerate

## Run

### Part 1
python ingestion.py

### Part 2
python train.py

## Features
- Sliding window ingestion
- Knowledge pyramid
- Multi-layer retrieval
- LoRA-based fine-tuning
- GSM8K dataset training

## Notes
- Used distilgpt2 for low-resource training
- Reduced dataset size for local execution