from invest.investigation import investigate
from mem.memory import retrieve_similar_incidents
from mem.memory import store_verified_incident
from plan.planning import generate_plan
from respons.alert import create_security_alert
from respons.response import execute_plan, get_expected_plan
from verify.verification import verify_execution
from detect.xgboostpred import predict_attack
from detect.anomalyscore import detect_anomaly

def detection_node(state):
    result = predict_attack(state["traffic"])
    state["attack"] = result["attack"]
    state["confidence"] = result["confidence"]
    return state

def zero_day_node(state):
    result = detect_anomaly(state["traffic"])
    state["anomaly_score"] = result["anomaly_score"]
    return state

def investigation_node(state):
    if state["confidence"] > 0.85:
        state["threat_type"] = "Known Attack"
    elif state["anomaly_score"] > 0.5:
        state["attack"] = "Unknown"
        state["confidence"] = 0
        state["threat_type"] = "Potential Zero-Day Threat"
    else:
        state["threat_type"] = "Suspicious Activity"

    report = investigate(attack=state["attack"], confidence=state["confidence"], anomaly_score=state["anomaly_score"] , threat_type = state["threat_type"])
    state["investigation"] = report
    return state

def memory_node(state):
    memory_query = {
        "attack": state["attack"],
        "analysis":
            f"{state['investigation']['attack_behavior']} "
            f"{state['investigation']['possible_impact']}"
    }
    state["memory"] = retrieve_similar_incidents(memory_query)
    return state

def planning_node(state):
    combined_result = state["investigation"].copy()
    combined_result["attack"] = state["attack"]
    combined_result["confidence"] = state["confidence"]
    combined_result["similar_incident"] = state["memory"]
    plan = generate_plan(combined_result)
    state["plan"] = plan
    return state

def response_node(state):
    alert = create_security_alert(state["attack"] , state["investigation"], state["plan"])
    execute_plan(state["plan"])
    state["response"] = {"alert": alert,}
    return state

def verification_node(state):
    expected_changes = get_expected_plan(state["plan"])
    execution_success = verify_execution(expected_changes)
    state["verification"] = execution_success["verification"]
    state["status"] = execution_success["outcome"]
    store_verified_incident(state["attack"] , state["investigation"] , state["plan"] , execution_success)
    
    return state