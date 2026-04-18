
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

SYSTEM = """You are Pocket-Agent, a strict tool-calling assistant.
Emit ONLY <tool_call>JSON</tool_call> for tool requests, plain text refusal otherwise.
Tools: weather(location,unit), calendar(action,date,title?), convert(value,from_unit,to_unit), currency(amount,from,to), sql(query)
Default weather unit is C. Currency uses ISO3 codes. Refuse chitchat, fake tools, ambiguous refs."""

_model = None
_tokenizer = None

def _load():
    global _model, _tokenizer
    if _model is not None:
        return
    base_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    _tokenizer = AutoTokenizer.from_pretrained("./tinyllama-tool-adapter")
    _tokenizer.pad_token = _tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(base_name, torch_dtype=torch.float16)
    _model = PeftModel.from_pretrained(base, "./tinyllama-tool-adapter")
    _model.eval()
    if torch.cuda.is_available():
        _model = _model.cuda()

def run(prompt: str, history: list[dict]) -> str:
    _load()
    chat = f"<|system|>\n{SYSTEM}</s>\n"
    for turn in history:
        chat += f"<|user|>\n{turn['user']}</s>\n"
        chat += f"<|assistant|>\n{turn['assistant']}</s>\n"
    chat += f"<|user|>\n{prompt}</s>\n<|assistant|>\n"
    inputs = _tokenizer(chat, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    with torch.no_grad():
        out = _model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,
            temperature=1.0,
            repetition_penalty=1.1,
            pad_token_id=_tokenizer.eos_token_id,
        )
    return _tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
