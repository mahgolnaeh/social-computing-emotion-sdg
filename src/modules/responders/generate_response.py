from src.configs.conf import API_KEY_OAI
from src.mappers.tone_templates import get_emotion_template
from src.mappers.sdg_link_mapper import get_sdg_link
from src.utils.llm_client import LLMClient
from src.configs.model_selector import get_model_and_params
from collections import Counter
from typing import List, Optional
from src.schemas.models import Post, ResponseForTrend
from src.schemas.response import Response


def extract_trends(posts: List[Post]) -> List[str]:
    """Extract unique trends from the dataset."""
    trends = set()
    for post in posts:
        trends.add(post.trend.strip().lower())
    return list(trends)


def get_top_k_sdgs(posts: List[Post], k: int) -> List[str]:
    """Count SDGs across posts and return top-k most frequent ones."""
    sdg_counts = Counter()
    for post in posts:
        if post.sdg:
            for sdg in post.sdg:
                sdg_counts[sdg] += 1
    return [sdg for sdg, _ in sdg_counts.most_common(k)]


def get_dominant_emotion(posts: List[Post]) -> Optional[str]:
    """Get the most common emotion among a list of posts."""
    emotion_counts = Counter(post.emotion for post in posts if post.emotion)
    if emotion_counts:
        return emotion_counts.most_common(1)[0][0]
    return None


def generate_responses_batch(
    data: List[Post],
    trends: Optional[List[str]] = None,
    top_k_sdgs: int = 1,
    use_llm: bool = True
) -> List[ResponseForTrend]:
    """
    Generates supportive responses per trend for top-k SDGs.

    Parameters:
    - data: Full dataset already parsed into Post objects.
    - trends: Optional list of trends to process. If None, extract from data.
    - top_k_sdgs: Number of top SDGs to generate responses for per trend.
    - use_llm: Whether to use LLM or fallback template-based response.

    Returns:
    - List of ResponseForTrend objects (validated with Pydantic).
    """
    result = []
    selected_trends = trends or extract_trends(data)

    for trend in selected_trends:
        trend_posts = [p for p in data if p.trend.strip().lower() == trend.strip().lower()]
        if not trend_posts:
            continue

        top_sdgs = get_top_k_sdgs(trend_posts, top_k_sdgs)
        for sdg in top_sdgs:
            sdg_posts = [p for p in trend_posts if sdg in p.sdg]
            dominant_emotion = get_dominant_emotion(sdg_posts)
            if not dominant_emotion:
                continue

            response = generate_supportive_response(
                sdg=sdg,
                emotion=dominant_emotion,
                trends=[trend],
                use_llm=use_llm
            )

            result.append(ResponseForTrend(
                trend=trend,
                sdg=sdg,
                emotion=dominant_emotion,
                response=response
            ))

    return result

def generate_supportive_response(
    sdg: str,
    emotion: str,
    trends: List[str],
    use_llm: bool = False
) -> Response:
    """
    Generate a supportive message based on sdg, emotion, and trend context.
    If you use_llm=True, use OpenRouter LLM API. Otherwise, use static template logic.
    """
    # Get SDG link
    sdg_link = get_sdg_link(sdg)
    trends_text = ", ".join(trends[:2]) if trends else "recent trends"

    if use_llm:
        # 🔹 Use LLM model
        prompt = (
            f"You are a supportive assistant helping users cope with emotional reactions to social trends.\n"
            f"Users are feeling {emotion.lower()} in response to topics like: {trends_text}.\n"
            f"The context is related to the Sustainable Development Goal: '{sdg}'.\n"
            f"Craft a short, empathetic message that either provides emotional support, helpful information, or reassurance—"
            f"whichever is most appropriate for someone experiencing {emotion.lower()}.\n"
            f"Your tone should always be human, kind, and appropriate to the emotion."
            f"The message should be helpful, actionable, or emotionally supportive, based on the user's emotional needs.\n"

        )

        model_name, params = get_model_and_params("response_generation")
        client = LLMClient(model=model_name,api_key=API_KEY_OAI)
        try:
            response_text = client.call_sync(prompt=prompt, **params).strip()
        except Exception as e:
            response_text = "Sorry, something went wrong generating a response."
        response_type = "emotional_support" if emotion in ["Fear", "Anxiety", "Sadness", "Confusion"] else "motivational"

        return Response(
            message=response_text,
            type=response_type,
            sdg_link=sdg_link
        )

    else:
        # 🔹 Use template-based method
        tone = get_emotion_template(emotion)
        if not tone:
            tone = "Your feelings are valid, and you're not alone."

        message = (
            f"{tone} Topics like {trends_text} reflect the challenges connected to '{sdg}'. "
            f"Explore ways to contribute or learn more here: {sdg_link if sdg_link else 'https://sdgs.un.org'}"
        )

        response_type = "emotional_support" if emotion in ["Fear", "Anxiety", "Sadness", "Confusion"] else "motivational"

        return Response(
            message=message,
            type=response_type,
            sdg_link=sdg_link
        )

