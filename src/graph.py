from langgraph.graph import StateGraph, START, END
from src.schema import AgentState
from src.agents import *

def create_nexus_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("scorer", scorer_node)
    workflow.add_node("enricher", enricher_node)
    workflow.add_node("drafter", drafter_node)
    workflow.add_node("sender", sender_node)
    workflow.add_node("simulator", simulator_node)
    workflow.add_node("categorizer", categorizer_node)

    workflow.add_edge(START, "scorer")
    workflow.add_edge("scorer", "enricher")
    workflow.add_edge("enricher", "drafter")
    workflow.add_edge("drafter", "sender")
    workflow.add_edge("sender", "simulator")
    workflow.add_edge("simulator", "categorizer")
    workflow.add_edge("categorizer", END)

    return workflow.compile()