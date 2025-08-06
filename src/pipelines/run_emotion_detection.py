import json
import asyncio
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
from src.modules.classifiers.emotion_detector import detect_emotion
from src.utils.utilities import load_json_data
import logging



# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


INPUT_PATH = "../data/output/sdg_output.json"
OUTPUT_PATH = "../data/output/emotion_output.json"
FAILED_PATH = "../data/logs/emotion_failed.json"
N_PARALLEL = 5

async def process_post(sem, post: dict):
    async with sem:
        result = await detect_emotion(post["text"])
        if result:
            post["emotion"] = result.emotion
            return post
        else:
            return {"trend": post["trend"], "text": post["text"], "emotion": None}

async def main():
    print(f"📥 Loading posts from {INPUT_PATH}...")
    data = load_json_data(INPUT_PATH)
    print(f"🔍 Processing {len(data)} posts for emotion detection...")

    sem = asyncio.Semaphore(N_PARALLEL)
    tasks = [process_post(sem, post) for post in data]
    results = await tqdm_asyncio.gather(*tasks)

    successful = [r for r in results if r["emotion"] is not None]
    failed = [r for r in results if r["emotion"] is None]

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(successful, f, indent=2, ensure_ascii=False)

    with open(FAILED_PATH, "w", encoding="utf-8") as f:
        json.dump(failed, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(successful)} emotions detected")
    print(f"❌ {len(failed)} posts failed to classify")
    print(f"📁 Output saved to: {OUTPUT_PATH}")
    print(f"📁 Failed saved to: {FAILED_PATH}")

    # Close the client connection
    from src.modules.classifiers.emotion_detector import client
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
