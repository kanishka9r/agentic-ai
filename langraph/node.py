from invest.investigation import investigate
from mem.memory import retrieve_similar_incidents
from mem.memory import store_verified_incident
from plan.planning import generate_plan
from respons.alert import create_security_alert
from respons.response import execute_plan, get_expected_plan
from verify.verification import capture_before_state
from verify.verification import verify_response
from verify.verification import capture_after_state
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
    state["status"] = result["status"]
    state["anomaly_score"] = result["anomaly_score"]
    return state

def investigation_node(state):
    analysis = investigate(state["traffic"])
    state["investigation"] = analysis
    return state

def memory_node(state):
    memory_query = {
        "attack": state["investigation"]["attack"],
        "analysis":
            f"{state['investigation']['attack_behavior']} "
            f"{state['investigation']['possible_impact']}"
    }
    state["memory"] = retrieve_similar_incidents(memory_query)
    return state

def planning_node(state):
    combined_result = state["investigation"].copy()
    combined_result["similar_incident"] = state["memory"]
    plan = generate_plan(combined_result)
    state["plan"] = plan
    return state

def response_node(state):
    alert = create_security_alert(state["investigation"], state["plan"])
    response = execute_plan(state["plan"])
    state["response"] = {
        "alert": alert,
        "execution": response
    }
    return state

def verification_node(state):
    before_state = capture_before_state(state["investigation"])
    after_state = capture_after_state(state["traffic"])
    expected_changes = get_expected_plan(state["plan"])
    execution_success = verify_execution(expected_changes)
    verification = verify_response(before_state,after_state,execution_success)
    state["verification"] = verification
    state["status"] = verification["outcome"]
    store_verified_incident(state["investigation"], state["plan"], verification)
    
    return state