"""
Week 1 - Baseline, step 1: download PolyAI/banking77 and save CSVs.
Run from repo root:  python ml/baseline/download_banking77.py
Requires: python -m pip install datasets pandas
"""
import json
from pathlib import Path

from datasets import load_dataset

OUT = Path("data/banking77")
OUT.mkdir(parents=True, exist_ok=True)

print("Downloading PolyAI/banking77 (first run ~30 MB, be patient)...")
ds = load_dataset("PolyAI/banking77")

ds["train"].to_pandas().to_csv(OUT / "train.csv", index=False)
ds["test"].to_pandas().to_csv(OUT / "test.csv", index=False)
names = ds["train"].features["label"].names
(OUT / "label_names.json").write_text(json.dumps(names))

print("Saved files:", sorted(p.name for p in OUT.iterdir()))
print(f"Train rows: {len(ds['train'])} | Test rows: {len(ds['test'])} | Intents: {len(names)}")