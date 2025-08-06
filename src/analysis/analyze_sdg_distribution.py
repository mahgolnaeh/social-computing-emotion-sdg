import json
from collections import Counter
from typing import List
from src.schemas.emotion_output import EmotionAnnotatedPost


def load_posts(path: str) -> List[EmotionAnnotatedPost]:
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return [EmotionAnnotatedPost(**item) for item in raw_data]


def count_sdgs(posts: List[EmotionAnnotatedPost]) -> Counter:
    counter = Counter()
    for post in posts:
        counter.update(post.sdg)  # SDG is a List[str]
    return counter


def save_results(counter: Counter, path: str):
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    data = [{"sdg": sdg, "count": count} for sdg, count in sorted_items]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def print_results(counter: Counter):
    print("\n SDG Category Frequency:\n")
    for sdg, count in counter.most_common():
        print(f"  {sdg:40} : {count}")


def main():
    INPUT_PATH = "../data/output/emotion_output.json"
    OUTPUT_PATH = "../data/output/sdg_distribution.json"

    posts = load_posts(INPUT_PATH)
    counter = count_sdgs(posts)

    print_results(counter)
    save_results(counter, OUTPUT_PATH)
    print(f"\n SDG distribution saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
