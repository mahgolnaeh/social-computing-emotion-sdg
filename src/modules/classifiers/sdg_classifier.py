from typing import Optional
from src.schemas.sdg_output import SDGClassificationResult
from src.utils.llm_client import LLMClient
from src.configs.conf import API_KEY_OAI
from src.configs.model_selector import get_model_and_params


class SDGClassifier:
    def __init__(self):
        self.model_name, self.model_params = get_model_and_params("sdg_classification")
        self.client = LLMClient(model=self.model_name, api_key=API_KEY_OAI)

    def build_prompt(self, text: str) -> str:
        return (
            "You are an expert analyst specializing in UN Sustainable Development Goals (SDGs).\n"
            "Analyze social media posts and classify them according to the 17 SDGs.\n\n"
            "**IMPORTANT: Return ONLY a valid JSON object with the specified format. No additional text or explanations.**\n\n"
            "**Choose only from the list of goals shown below. Do not create new labels.**\n\n"
            " 17 UN SDGs Reference:\n"
            "- No Poverty\n- Zero Hunger\n- Good Health and Well-being\n- Quality Education\n"
            "- Gender Equality\n- Clean Water and Sanitation\n- Affordable and Clean Energy\n"
            "- Decent Work and Economic Growth\n- Industry, Innovation and Infrastructure\n"
            "- Reduced Inequality\n- Sustainable Cities and Communities\n"
            "- Responsible Consumption and Production\n- Climate Action\n- Life Below Water\n"
            "- Life on Land\n- Peace, Justice and Strong Institutions\n- Partnerships for the Goals\n\n"
            "Classification Rules:\n"
            "- Consider implicit meanings and emotional undertones\n"
            "- Focus on core issues mentioned in the text\n"
            "- One post can map to multiple SDGs (maximum 2)\n"
            "- Only output the exact JSON format specified\n"
            "- Do not include any explanatory text\n\n"
            f"Post: \"{text}\"\n\n"
            "Required output format (ONLY this, no other text):\n"
            "{\"sdg\": [\"SDG Title 1\", \"SDG Title 2\"]}\n"
            "or for single SDG:\n"
            "{\"sdg\": [\"SDG Title\"]}"
        )

    async def classify(self, text: str) -> Optional[SDGClassificationResult]:
        prompt = self.build_prompt(text)
        response = await self.client.call(prompt=prompt, **self.model_params)

        try:
            # Strip any potential explanatory text, keep only JSON
            response = response.strip()
            if not response.startswith('{'):
                # Find the first JSON-like structure
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    response = response[start:end]
                else:
                    raise ValueError("No JSON structure found in response")

            result = SDGClassificationResult.model_validate_json(response)
            return result
        except Exception as e:
            print(f"❌ Validation failed for response: {response}")
            print(f"⚠️ Error: {e}")
            return None