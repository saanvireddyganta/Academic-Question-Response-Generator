from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
dest = Path(__file__).resolve().parents[1] / "model" / "distilgpt2"
dest.mkdir(parents=True, exist_ok=True)
print("Downloading DistilGPT2...")
tok = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tok.save_pretrained(dest); model.save_pretrained(dest)
print("Model saved to", dest)
