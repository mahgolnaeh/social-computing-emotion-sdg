# src/utils/model_loader.py
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[1] / "configs" / "model_configs.json"

def get_model_config(model_name: str) -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        configs = json.load(f)
    if model_name not in configs:
        raise ValueError(f"Model config for '{model_name}' not found.")
    return configs[model_name]
