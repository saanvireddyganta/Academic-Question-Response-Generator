import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model.model_utils import generate_answer
q = "Explain tokenization in natural language processing."
print("QUESTION:", q)
print("ANSWER:", generate_answer(q, 55)["generated_text"])
print("SMOKE TEST PASSED")
