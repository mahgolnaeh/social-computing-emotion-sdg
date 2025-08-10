"""
trend_fetcher.py
Clean posts, map to trends, and write JSON.
"""

import json
import re
from pathlib import Path
from typing import List, Optional

import pandas as pd

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# NOTE: This file lives at: src/modules/fetchers/trend_fetcher.py
# -> __file__.resolve().parents[2] takes us back to: src/
SRC_DIR = Path(__file__).resolve().parents[2]

# Centralize commonly used directories under src/
DATA_INPUT_DIR = (SRC_DIR / "data" / "input").resolve()   # <-- changed: single source of truth for input dir
OUTPUT_DIR = DATA_INPUT_DIR                                # <-- changed: write outputs next to inputs

# Use Path objects for files that live under data/input/
INPUT_CSV_FILENAME = "twitter_dataset.csv"  # change if your CSV name differs
INPUT_CSV_PATH = (DATA_INPUT_DIR / INPUT_CSV_FILENAME).resolve()  # build absolute path safely

TEXT_COLUMN: str = "Text"  # change if your CSV uses a different column name

# Trend list is stored in src/data/input/flat_trends_list.json
TREND_LIST_PATH = (DATA_INPUT_DIR / "flat_trends_list.json").resolve()

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)   # remove URLs
    text = re.sub(r"@\w+", "", text)             # remove @mentions
    text = re.sub(r"#(\w+)", r"\1", text)        # keep hashtag word, drop '#'
    text = re.sub(r"[^a-z0-9\s]", "", text)      # remove non-alphanumerics (incl. emojis/punct)
    text = re.sub(r"\s+", " ", text).strip()     # normalize spaces
    return text


def parse_trend_list(file_path: Path) -> List[str]:
    """Load trends from JSON; if malformed, fall back to line-by-line quoted strings."""
    trends: List[str] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Trend list JSON must contain a list")
        return [str(item).lower() for item in data if isinstance(item, str)]
    except Exception:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().rstrip(",")
                if line.startswith('"') and line.endswith('"'):
                    candidate = line[1:-1].strip()
                    if candidate:
                        trends.append(candidate.lower())
        return trends


def assign_trend(text: str, trends: List[str]) -> str:
    """Very simple token-overlap heuristic."""
    tokens = set(text.split())
    best_trend: Optional[str] = None
    max_matches = 0
    for trend in trends:
        trend_tokens = set(trend.split())
        matches = len(tokens & trend_tokens)
        if matches > max_matches:
            best_trend = trend
            max_matches = matches
    return best_trend if best_trend is not None else "unknown"


# -----------------------------------------------------------------------------
# Main processing
# -----------------------------------------------------------------------------

def main() -> None:
    # --- Sanity checks on paths (all absolute now thanks to .resolve()) ---
    if not INPUT_CSV_PATH.exists():
        raise FileNotFoundError(f"CSV input file not found: {INPUT_CSV_PATH}")
    if not TREND_LIST_PATH.exists():
        raise FileNotFoundError(f"Trend list file not found: {TREND_LIST_PATH}")

    # --- Load trend titles ---
    trends = parse_trend_list(TREND_LIST_PATH)
    if not trends:
        raise ValueError("No trend titles found; cannot assign trends")

    # --- Read CSV and validate column name ---
    df = pd.read_csv(INPUT_CSV_PATH)
    if TEXT_COLUMN not in df.columns:
        raise ValueError(
            f"CSV is missing expected text column '{TEXT_COLUMN}'. "
            f"Available columns: {list(df.columns)}"
        )

    # --- Process rows ---
    processed_posts = []
    for _, row in df.iterrows():
        cleaned = clean_text(row[TEXT_COLUMN])
        trend = assign_trend(cleaned, trends)
        processed_posts.append({"trend": trend, "text": cleaned})

    # --- Write output next to input data ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  #ensure dir exists
    output_file = (OUTPUT_DIR / f"{Path(INPUT_CSV_FILENAME).stem}.json").resolve()
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_posts, f, ensure_ascii=False, indent=2)

    print(f"✅ Processed {len(processed_posts)} posts.")
    print(f"💾 Output saved to: {output_file}")


if __name__ == "__main__":
    main()
