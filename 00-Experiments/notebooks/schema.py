from pydantic import BaseModel, Field
from typing import Literal, List

class LeadScore(BaseModel):
    priority: Literal["High", "Medium", "Low"] = Field(description="The priority level of the lead based on their potential value.")
    score: int = Field(description="A numeric score from 1 to 10.", ge=1, le=10)
    reasoning: str = Field(description="A brief professional explanation of why this priority was assigned.")



class PersonaEnrichment(BaseModel):
    persona: str = Field(description="A short, catchy name for the buyer persona (e.g., 'The Cost-Conscious Optimizer').")
    persona_description: str = Field(description="A brief psychological and professional profile of this lead.")
    key_motivations: List[str] = Field(description="List of 3 things this person likely cares most about in their role.")



class EmailDraft(BaseModel):
    subject: str = Field(description="A catchy, personalized subject line.")
    body: str = Field(description="The personalized email body. Use HTML tags for better formatting.")
    sender_name: str = Field(description="The name of the sender (e.g., 'NexusAI Sales Team').")


class SimulatedResponse(BaseModel):
    reply_text: str = Field(description="The content of the email reply from the lead.")
    sentiment: str = Field(description="The general tone of the reply (Positive, Neutral, Negative).")



class ResponseCategory(BaseModel):
    category: Literal["Interested", "Not Interested", "Neutral", "Auto-Reply"] = Field(
        description="The classification of the lead's response."
    )
    reasoning: str = Field(description="A brief explanation of why this category was chosen.")