import json
from typing import List
from src.configs.conf import API_KEY_OAI
from src.configs.model_selector import get_model_and_params
from src.schemas.generated_post import GeneratedPost
from src.utils.llm_client import LLMClient


class PostGenerator:
    def __init__(self):
        self.model_name, self.model_params = get_model_and_params("generation")
        self.client = LLMClient(model=self.model_name, api_key=API_KEY_OAI)

    async def generate_posts_for_trend(self, trend: str, num_posts: int = 10) -> List[GeneratedPost]:
        prompt = (
            f"You are an expert social media observer and simulator.\n\n"
            f"Generate {num_posts} realistic, diverse, concise, and emotionally expressive social media posts "
            f"that reflect real users’ thoughts and feelings about the following trend:\n"
            f"Trend: {trend}\n\n"
            f"- Each post should sound like something a real person might post online (e.g., on Twitter).\n"
            f"- Vary the tone and perspective (e.g., hopeful, frustrated, sarcastic, worried).\n"
            f"- Include slang, emotion, and cultural realism if appropriate.\n"
            f"- Keep each post under 280 characters.\n"
            f"- DO NOT number or label the posts.\n"
            f"- Return the result as a **JSON list of strings**.\n"
        )

        raw_response = await self.client.call(prompt=prompt, **self.model_params)
        # Expecting LLM to return a list of strings (posts)
        if isinstance(raw_response, list):
            return [GeneratedPost(trend=trend, text=post) for post in raw_response]
        elif isinstance(raw_response, str):
            lines = [line.strip("-•\n ") for line in raw_response.splitlines() if line.strip()]
            return [GeneratedPost(trend=trend, text=line) for line in lines if len(line) > 10]
        else:
            raise ValueError("Unexpected format in LLM response while generating posts.")

    @staticmethod
    def _try_parse_response(raw_response: str, trend: str) -> List[GeneratedPost]:
        try:
            posts = json.loads(raw_response)
            if not isinstance(posts, list):
                raise ValueError("Not a list.")
            return [GeneratedPost(trend=trend, text=p) for p in posts if isinstance(p, str)]
        except Exception as e:
            print(f"⚠️ JSON parse failed: {e}")
            print("🔁 Fallback to line-by-line parsing.")
            lines = [line.strip("-•\n ") for line in raw_response.splitlines() if line.strip()]
            return [GeneratedPost(trend=trend, text=line) for line in lines if len(line) > 10]


'''f"Generate {num_posts} realistic and diverse social media posts "
            f"that reflect real users’ thoughts and feelings about the following trend:\n"
            f"Trend: {trend}\n\n"
            f"Each post should be concise, emotionally authentic, and look like it could be a real tweet."
            '''