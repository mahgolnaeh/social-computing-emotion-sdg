from typing import Literal, List
from pydantic import BaseModel, Field

VALID_EMOTIONS = [
    "Joy", "Sadness", "Anger", "Fear", "Disgust",
    "Anxiety", "Frustration", "Hope", "Confusion"
]

class EmotionClassificationResult(BaseModel):
    emotion: Literal[
        "Joy", "Sadness", "Anger", "Fear", "Disgust",
        "Anxiety", "Frustration", "Hope", "Confusion"
    ] = Field(..., description="Detected emotion from the post text")

class EmotionAnnotatedPost(BaseModel):
    trend: str
    text: str
    sdg: List[str]
    emotion: Literal[
        "Joy", "Sadness", "Anger", "Fear", "Disgust",
        "Anxiety", "Frustration", "Hope", "Confusion"
    ]
