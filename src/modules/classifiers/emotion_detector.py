from typing import Optional
import os
from dotenv import load_dotenv
from src.schemas.emotion_output import EmotionClassificationResult
from src.utils.llm_client import LLMClient
from src.configs.model_selector import get_model_and_params

# Load environment variables
load_dotenv()

model_name, model_params = get_model_and_params("classification")

# Get API key from environment variable
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

client = LLMClient(model=model_name, api_key=api_key)

async def detect_emotion(text: str) -> Optional[EmotionClassificationResult]:
    prompt = (
        "Analyze the emotional tone of the following social media post "
        "and respond with a single JSON object that includes only one of these emotions:\n\n"
        "Joy, Sadness, Anger, Fear, Disgust, Anxiety, Frustration, Hope, Confusion\n\n"
        f"Post: {text}\n\n"
        "Return only this format:\n"
        '{"emotion": "YourChosenEmotion"}'
    )

    response = await client.call(prompt=prompt, structured=True)

    if isinstance(response, dict):
        try:
            return EmotionClassificationResult(**response)
        except Exception:
            return None
    return None
