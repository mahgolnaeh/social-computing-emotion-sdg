import json
import asyncio
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
from src.modules.classifiers.sdg_classifier import SDGClassifier
from src.utils.utilities import load_json_data


INPUT_PATH = "src/data/cleaned_posts.json"
OUTPUT_PATH = "src/data/sdg_output2.json"
FAILED_PATH = "src/data/sdg_failed2.json"
N_PARALLEL = 5


async def classify_post(sem, classifier: SDGClassifier, post: dict):
    async with sem:
        result = await classifier.classify(post["text"])
        return {
            "trend": post["trend"],
            "text": post["text"],
            "sdg": result.sdg if result else None
        }


async def main():
    print(f"Loading data from {INPUT_PATH}...")
    data = load_json_data(INPUT_PATH)
    print(f"Loaded {len(data)} posts for classification")
    
    classifier = SDGClassifier()
    sem = asyncio.Semaphore(N_PARALLEL)

    tasks = [
        classify_post(sem, classifier, post)
        for post in data
    ]

    print("Starting classification...")
    results = await tqdm_asyncio.gather(*tasks)

    successful = [r for r in results if r["sdg"] is not None]
    print(f"\nProcessed {len(results)} posts")
    
    with open("src/data/classified_posts.json", "w", encoding="utf-8") as f:
        json.dump(successful, f, indent=2, ensure_ascii=False)

    failed = [r for r in results if r["sdg"] is None]

    # Save results
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(successful, f, indent=2, ensure_ascii=False)

    with open(FAILED_PATH, "w", encoding="utf-8") as f:
        json.dump(failed, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(successful)} classified, ❌ {len(failed)} failed.")
    print(f"Results saved to {OUTPUT_PATH}")
    print(f"Failed cases saved to {FAILED_PATH}")
    await classifier.client.close()  # Close HTTP connection pool


if __name__ == "__main__":
    asyncio.run(main())
