import json

with open("src/data/generated_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def is_valid(post):
    text = post["text"].strip()
    return (
        len(text) > 20
        and text[-1] in ".!?\""
        and not text.endswith(("Just", "only", "but", "so", "and", "that", "with"))
    )

cleaned = [p for p in data if is_valid(p)]

with open("src/data/generated_posts_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned: {len(cleaned)} posts saved.")
