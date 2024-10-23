from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
import torch
from datasets import load_dataset

max_seq_length = 2048 # We can update this (check the seq_length of the longest query and set to that value to prevent unnecessary GPU/VRAM usage)
dtype = None # None for auto detection
load_in_4bit = True # Use 4bit quantization to reduce memory usage [Optimizing performance!]

# 4bit pre quantized models Unsloth supports for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/Llama-3.2-1B-bnb-4bit",           
    "unsloth/Llama-3.2-1B-Instruct-bnb-4bit",

]

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.2-1B-Instruct", # This is the model we will be using directly from unsloth's library
    max_seq_length = max_seq_length,              # We could use hugging face's model instead but that would require a login/key as its gated
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_..." [This is incase we decide to swap to a hugging face model]
)


# LoRA adapter (requires us to mess around with less parameters)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # r can be between 1-128, the higher the number the better fine-tuning we get, but requires much more prompting
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # 0 is optimized
    bias = "none",    # "none" is optimized

    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False, 
    loftq_config = None, 
)

#### This is converting our current json file into the correct template for Unsloth

tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3.1", ## llama 3.2 uses the same model
)

def formatting_prompts_func(examples):
    convos = examples["conversations"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }
pass

dataset = load_dataset('json', data_files='semCorel.json', split = "train")
dataset = standardize_sharegpt(dataset)
dataset = dataset.map(formatting_prompts_func, batched = True,)
