from typing import List,Literal
from pydantic import BaseModel, Field

SDG_TITLES = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequality",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]


class SDGClassificationResult(BaseModel):
    sdg: List[Literal[*SDG_TITLES]] = Field(
        default=[],
        description="List of 0 to 2 SDGs from the official UN list"
    )