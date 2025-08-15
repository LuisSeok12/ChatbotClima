from openai import OpenAI
from dotenv import load_dotenv
import os, time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1) Envie os arquivos JSONL
train_file = client.files.create(
    file=open("train.jsonl", "rb"),
    purpose="fine-tune"
)
valid_file = client.files.create(
    file=open("valid.jsonl", "rb"),
    purpose="fine-tune"
)

print("Train file id:", train_file.id)
print("Valid file id:", valid_file.id)

# 2) Crie o job de fine-tuning (SFT)
job = client.fine_tuning.jobs.create(
    model="gpt-4o-mini-2024-07-18",   # modelo base recomendado p/ SFT
    training_file=train_file.id,
    validation_file=valid_file.id,     # opcional, mas recomendado
    method={"type": "supervised"},
    hyperparameters={"n_epochs": 3}
)
