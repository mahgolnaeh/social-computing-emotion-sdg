import json
from pathlib import Path
from typing import List
from src.utils.utilities import load_json_data, clean_text
from pydantic import BaseModel


class CleanedPost(BaseModel):
    trend: str
    text: str


def clean_and_validate_posts(raw_posts: List[dict]) -> List[CleanedPost]:
    cleaned = []
    seen = set()

    for item in raw_posts:
        try:
            trend = item.get("trend", "").strip()
            text = clean_text(item.get("text", "").strip())

            if not trend or not text or len(text) < 15:
                continue

            key = (trend.lower(), text)
            if key in seen:
                continue

            seen.add(key)
            cleaned.append(CleanedPost(trend=trend, text=text))

        except Exception as e:
            print(f"❌ Error processing item: {item} → {e}")

    return cleaned


def save_cleaned_json(posts: List[CleanedPost], path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump([p.model_dump() for p in posts], f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(posts)} cleaned posts to {path}")


if __name__ == "__main__":
    input_paths = [
        "src/data/generated_posts.json",
        "src/data/generate_post_output_gpt-4.1-mini.json"
    ]

    all_raw = []
    for path in input_paths:
        print(f"📂 Loading file: {path}")
        all_raw.extend(load_json_data(path))

    final = clean_and_validate_posts(all_raw)
    save_cleaned_json(final, Path("src/data/cleaned_posts.json"))
