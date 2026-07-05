import operator
from typing import TypedDict, Annotated, Any, Dict, Optional

class AgentState(TypedDict):
    traffic: Optional[Any]
    attack: Optional[str]
    confidence: Optional[float]
    anomaly_score: Optional[float]
    threat_type: Optional[str]
    investigation: Optional[Dict[str, Any]]
    memory: Optional[Any]
    plan: Optional[Dict[str, Any]]
    response: Optional[Dict[str, Any]]
    verification: Optional[str]
    status: Optional[str]
    retry_count: Annotated[int, operator.add]

def create_state():
    return {
        "traffic": None,
        "attack": None,
        "confidence": None,
        "anomaly_score": None,
        "threat_type": None,
        "investigation": None,
        "memory": None,
        "plan": None,
        "response": None,
        "verification": None,
        "status": None,
        "retry_count": 0
    }