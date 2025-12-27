from pydantic import BaseModel, Field
from typing import Literal

class LeadScore(BaseModel):
    priority: Literal["High", "Medium", "Low"] = Field(description="The priority level of the lead based on their potential value.")
    score: int = Field(description="A numeric score from 1 to 10.", ge=1, le=10)
    reasoning: str = Field(description="A brief professional explanation of why this priority was assigned.")