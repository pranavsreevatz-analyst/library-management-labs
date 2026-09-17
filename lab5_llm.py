import json
from pathlib import Path
from time import perf_counter

from ai_client import MODEL, generate


prompt = """
Explain why borrowing an already borrowed library book
should fail. Answer in no more than three sentences.
"""

results = []

for temperature in [0.0, 0.8]:
    for trial in range(1, 4):
        start = perf_counter()
        result = generate(prompt, temperature=temperature)

        row = {
            "model": MODEL,
            "temperature": temperature,
            "trial": trial,
            "seconds": round(perf_counter() - start, 2),
            "input_tokens": result.get("prompt_eval_count"),
            "output_tokens": result.get("eval_count"),
            "answer": result["response"],
        }

        results.append(row)
        print(json.dumps(row, indent=2))

Path("lab5_results.json").write_text(
    json.dumps(results, indent=2),
    encoding="utf-8",
)