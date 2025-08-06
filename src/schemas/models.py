from typing import List, Optional
from pydantic import BaseModel
from src.schemas.response import Response

class Post(BaseModel):
    text: str
    trend: str
    sdg: List[str]
    emotion: Optional[str] = None


class ResponseForTrend(BaseModel):
    trend: str
    sdg: str
    emotion: str
    response: Response
