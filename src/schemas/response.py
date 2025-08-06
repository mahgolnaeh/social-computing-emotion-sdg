from typing import Optional,Literal
from pydantic import BaseModel


class Response(BaseModel):
    message: str
    type: Literal["emotional_support", "informative", "motivational"]
    sdg_link: Optional[str] = None