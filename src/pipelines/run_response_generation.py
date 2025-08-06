import json
from pathlib import Path
from src.schemas.models import Post
from src.modules.responders.generate_response import generate_responses_batch


'''Parameters:
    - data: Full dataset already parsed into Post objects.
    - trends: Optional list of trends to process. If None, extract from data.
    - top_k_sdgs: Number of top SDGs to generate responses for per trend.
    - use_llm: Whether to use LLM or fallback template-based response.'''



TREND_LIST_PATH = "../data/input/trend_titles.json"  #by using trend titles
USE_FILTERED_TRENDS = False  #Using the trend's title
INPUT_PATH = "../data/output/emotion_output.json"
OUTPUT_PATH = "../data/output"
TOP_K_SDGS = 1
USE_LLM = True

def main():
    print(f"Loading data from {INPUT_PATH} ...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if USE_FILTERED_TRENDS:
        with open(TREND_LIST_PATH, "r", encoding="utf-8") as f:
            trend_titles = json.load(f)
        raw_data = [item for item in raw_data if item["trend"] in trend_titles]

    posts = [Post(**item) for item in raw_data]

    print(f" Generating responses for each trend with top {TOP_K_SDGS} SDGs ...")
    responses = generate_responses_batch(
        data=posts,
        top_k_sdgs=TOP_K_SDGS,
        use_llm=USE_LLM
    )

    final_output = [item.model_dump() for item in responses]

    print(f" Saving responses to {OUTPUT_PATH}")
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(" All done! Responses saved successfully.")


if __name__ == "__main__":
    main()
