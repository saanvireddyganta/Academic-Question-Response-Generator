import sys, csv, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model.model_utils import generate_answer
root = Path(__file__).resolve().parents[1]
out = root / "reports" / "test_results.csv"
out.parent.mkdir(parents=True, exist_ok=True)
qs = [
"Explain convolutional neural networks.", "What is a recurrent neural network?",
"Explain tokenization in NLP.", "What is attention in transformers?",
"Explain supervised machine learning.", "Difference between classification and regression?",
"What is overfitting?", "What is an operating system?",
"Explain the client server model.", "What is a database management system?"
]
rows=[]
for i,q in enumerate(qs,1):
    t=time.perf_counter(); a=generate_answer(q,55); elapsed=time.perf_counter()-t
    rows.append({"test_no":i,"question":q,"generated_answer":a["generated_text"],"latency_seconds":round(elapsed,3),"observation":"Review against course notes."})
    print(f"Completed {i}/10")
with out.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("Saved",out)
