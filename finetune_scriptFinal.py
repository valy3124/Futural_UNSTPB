import os
import torch
import wandb
from huggingface_hub import login
from unsloth import FastLanguageModel, is_bfloat16_supported
from datasets import load_dataset
from transformers import TrainingArguments, TextStreamer, EarlyStoppingCallback
from trl import SFTTrainer

# cache to local tmp
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/transformers"

# Load secrets securely from environment variables
HF_TOKEN = "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"
WANDB_KEY = "d035f761ca6b32a943804ada89ea3298e388b0c0"

# Login to HF + W&B
login(HF_TOKEN)
wandb.login(key=WANDB_KEY)

# Start W&B run
run = wandb.init(
    project="fine-tune-deepseek-licenta-CLUSTERFINAL",
    job_type="training",
    anonymous="allow"
)

# Load base model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/DeepSeek-R1-Distill-Llama-8B",
    max_seq_length=1024,
    dtype=torch.float16,
    load_in_4bit=True,
    token=HF_TOKEN
)

# Quick sanity-check prompt
FastLanguageModel.for_inference(model)
test_prompt = """Below is a question that you need to answer using your available tools and knowledge.

### Question:
Which is the closest hospital by distance? I'm currently on Solokoa kalea in Abadiño.

### Answer:
{}
"""
inputs = tokenizer([test_prompt.format("")], return_tensors="pt").to("cuda")
text_streamer = TextStreamer(tokenizer)
_ = model.generate(**inputs, streamer=text_streamer, max_new_tokens=512, use_cache=True)

# Load and preprocess dataset
dataset = load_dataset("valy3124/durangaldea-2q", split="train", trust_remote_code=True)

EOS = tokenizer.eos_token
def format_instruction(example):
    prompt = """
Below is a question about locations in Durangaldea. Your task is to provide a clear and accurate answer using the <API> call whenever necessary. There are two types of questions you may encounter, each with a specific API call format.

Type 1: Closest Location
Use this API format to find the closest place of a given category from a specific location:

<API>get_closest_distance_time(category, mode, location, metric_to_extract) -> result</API>  

Parameters:
- category: One of ["hospitals", "pharmacies", "supermarkets"]
- mode: Transportation mode, one of ["drive", "walk", "bike"]
- location: City and street name in Durangaldea (e.g., "Durango, Artekalea Kalea")
- metric_to_extract: "distance" or "time"

The result is returned as a JSON object with:
{{ "distance": <float km>, "time": <float minutes> }}

Type 2: Filtered Location List
Use this API format when the question asks for [X] locations within [Y] km or minutes:
Example:
"Give me 3 locations where I can reach a supermarket in under 2 km using walk."
<API>get_closest_distance_time(category, mode, metric_to_extract, max_metric, nr_locations) -> result</API>  

Parameters:
- category: One of ["hospitals", "pharmacies", "supermarkets"]
- mode: One of ["drive", "walk", "bike"]
- metric_to_extract: "distance" or "time"
- max_metric: Maximum allowed metric (e.g., 2000 for 2 km)
- nr_locations: Number of locations to return (e.g., 3)

Result JSON:
{{
  "addresses": [
    "Street 1, City",
    "Street 2, City",
    …
  ]
}}

Instructions:
Before answering, identify the question type and build a logical response. Use plain language to explain API call results.

### Question:
{}

### Answer:
{}"""
    return {"text": prompt.format(example["question"], example["answer"]) + EOS}

print("Dataset columns:", dataset.column_names)
dataset = dataset.map(format_instruction, remove_columns=dataset.column_names)

# train/validation split
splits = dataset.train_test_split(test_size=0.05, seed=42)
train_ds, eval_ds = splits["train"], splits["test"]

# apply PEFT (LoRA)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=[
        "q_proj","k_proj","v_proj","o_proj",
        "gate_proj","up_proj","down_proj",
    ],
    lora_alpha=16,
    lora_dropout=0.0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=1000,
    use_rslora=False,
    loftq_config=None,
)

# Training arguments with evaluation & checkpointing
model_name = "durangaldea-assistantFinalPD"
local_path = f"/tmp/{model_name}"
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    num_train_epochs=2,
    learning_rate=2e-4,
    fp16=True,
    bf16=False,
    logging_steps=100,
    evaluation_strategy="steps",
    eval_steps=500,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    save_total_limit=3,
    lr_scheduler_type="cosine",
    optim="adamw_8bit",
    weight_decay=0.01,
    seed=1000,
    output_dir=local_path,
    push_to_hub=True,
    hub_model_id=f"valy3124/{model_name}",
    report_to="wandb",
)

# SFT Trainer with early stopping
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    dataset_text_field="text",
    max_seq_length=2048,
    dataset_num_proc=2,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    args=training_args,
)

# Start training
trainer.train()

# Save & push
trainer.save_model(local_path)
trainer.push_to_hub()

# Finish W&B run
wandb.finish()

