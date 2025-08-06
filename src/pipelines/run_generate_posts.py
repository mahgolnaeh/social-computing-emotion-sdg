import asyncio
import json
import os
from pathlib import Path
from typing import List, TextIO
from src.configs.model_selector import get_model_and_params
from src.utils.utilities import load_json_data, preprocess_text_list

from src.modules.generators.post_generator import PostGenerator
from src.schemas.generated_post import GeneratedPost

model_name, request_params= get_model_and_params("generation")

# Update paths to use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "data", "trend_titles.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", f"generate_post_output_{model_name.split('/')[-1]}.json")

async def main():
    # Load and preprocess trend titles
    trend_list = load_json_data(INPUT_PATH)
    if not trend_list:
        print("❌ No trend titles found. Exiting.")
        return

    # Process trend_list as a list of strings directly
    trend_list = preprocess_text_list(trend_list)

    generator = PostGenerator()

    all_posts: List[GeneratedPost] = []

    for trend in trend_list:
        try:
            posts = await generator.generate_posts_for_trend(trend)
            all_posts.extend(posts)
        except Exception as e:
            print(f"❌ Failed to generate posts for trend: {trend} → {e}")

    # Serialize and save results
    output_path = Path(OUTPUT_PATH)
    with open(output_path, "w", encoding="utf-8") as f:  # type: TextIO
        json.dump([post.model_dump() for post in all_posts], f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(all_posts)} posts across {len(trend_list)} trends.")
    print(f"📁 Output saved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
