from src.llm_factory import get_llm
from src.schema import LeadScore, PersonaEnrichment, EmailDraft, SimulatedResponse, ResponseCategory
from src.prompts import *
from src.utils import send_email_to_mailhog

def scorer_node(state):
    llm = get_llm(0).with_structured_output(LeadScore)
    res = llm.invoke([("system", LEAD_SCORER_SYSTEM_PROMPT), ("human", str(state['lead_data']))])
    return {"priority": res.priority, "priority_score": res.score, "priority_reason": res.reasoning}

def enricher_node(state):
    llm = get_llm(0.7).with_structured_output(PersonaEnrichment)
    res = llm.invoke([("system", PERSONA_ENRICHER_SYSTEM_PROMPT), ("human", str(state['lead_data']))])
    return {"persona": res.persona, "persona_description": res.persona_description}

def drafter_node(state):
    llm = get_llm(0.8).with_structured_output(EmailDraft)
    context = f"Lead: {state['lead_data']}, Priority: {state['priority']}, Persona: {state['persona']}"
    res = llm.invoke([("system", OUTREACH_DRAFTER_SYSTEM_PROMPT), ("human", context)])
    return {"email_subject": res.subject, "email_body": res.body}

def sender_node(state):
    success = send_email_to_mailhog(state['lead_data']['Email'], state['email_subject'], state['email_body'])
    return {"status": "Sent" if success else "Failed"}

def simulator_node(state):
    llm = get_llm(0.9).with_structured_output(SimulatedResponse)
    context = f"Email Received: {state['email_body']}, Persona: {state['persona']}"
    res = llm.invoke([("system", RESPONSE_SIMULATOR_SYSTEM_PROMPT), ("human", context)])
    return {"simulated_reply": res.reply_text}

def categorizer_node(state):
    llm = get_llm(0).with_structured_output(ResponseCategory)
    res = llm.invoke([("system", RESPONSE_CATEGORIZER_SYSTEM_PROMPT), ("human", state['simulated_reply'])])
    return {"response_category": res.category}