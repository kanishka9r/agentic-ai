from langgraph.graph import StateGraph, END
from .state import AgentState
from .node import (
    detection_node,
    zero_day_node,
    investigation_node,
    memory_node,
    planning_node,
    response_node,
    verification_node
)

def risk_router(state):
    if (
        state["attack"] == "Benign"
        and state["anomaly_score"] < 0.2
    ):
        return "end"
    return "investigation"

def verification_router(state):
    if state["status"] == "Threat Mitigated":
        return "end"
    if state.get("retry_count", 0) >= 3:
        return "end"
    return "investigation"

graph = StateGraph(AgentState)
graph.add_node("detection", detection_node)
graph.add_node("zero_day", zero_day_node)
graph.add_node("investigation", investigation_node)
graph.add_node("memory", memory_node)
graph.add_node("planning", planning_node)
graph.add_node("response", response_node)
graph.add_node("verification", verification_node)

graph.set_entry_point("detection")
graph.add_edge("detection", "zero_day")

graph.add_conditional_edges("zero_day", risk_router,
    {
        "end": END,
        "investigation": "investigation"
    }
)

graph.add_edge("investigation", "memory")
graph.add_edge("memory", "planning")
graph.add_edge("planning", "response")
graph.add_edge("response", "verification")

graph.add_conditional_edges("verification",
    verification_router,
    {
        "end": END,
        "investigation": "investigation"
    }
)

app = graph.compile()