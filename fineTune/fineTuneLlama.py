# Currently a sample fine-tuning script to set up Python virtual environment and test out PyTorch, Transformers, and datasets for tuning


from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("squad")

# Load the tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained("huggingface/llama-3b")
model = LlamaForCausalLM.from_pretrained("huggingface/llama-3b")

# Preprocess the data
def preprocess_function(examples):
    inputs = [q.strip() for q in examples['question']]
    targets = [a['text'][0].strip() for a in examples['answers']]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding='max_length')
    labels = tokenizer(targets, max_length=512, truncation=True, padding='max_length')
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Set training arguments
training_args = TrainingArguments(
    output_dir="./finetuned_llama_qna",
    evaluation_strategy="steps",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
)

# Initialize the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Fine-tune the model
trainer.train()

# Save the finetuned model
trainer.save_model("./finetuned_llama_qna")
