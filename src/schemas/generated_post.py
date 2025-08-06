from pydantic import BaseModel

class GeneratedPost(BaseModel):
    trend: str
    text: str
