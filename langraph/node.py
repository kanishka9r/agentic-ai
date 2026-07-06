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
    result = predict_attack(state.get("traffic"))
    
    return {
        "attack": result.get("attack", "Unknown"),
        "confidence": result.get("confidence", 0.0)
    }

def zero_day_node(state):
    result = detect_anomaly(state.get("traffic"))
    return {
        "anomaly_score": result.get("anomaly_score", 0.0)
    }

def investigation_node(state):
    attack = state.get("attack")
    confidence = state.get("confidence", 0)
    anomaly_score = state.get("anomaly_score", 0)
    
    if confidence > 0.85:
        threat_type = "Known Attack"
    elif anomaly_score > 0.5:
        attack = "Unknown"
        confidence = 0
        threat_type = "Potential Zero-Day Threat"
    else:
        threat_type = "Suspicious Activity"

    report = investigate(attack=attack, confidence=confidence, anomaly_score=anomaly_score, threat_type=threat_type)
    if report is None:
        return {"status": "Agent Failure"}
        
    return {
        "attack": attack,
        "confidence": confidence,
        "threat_type": threat_type,
        "investigation": report
    }

def memory_node(state):
    investigation = state.get("investigation")
    if investigation is None:
        return {}

    combined_result = {
        "attack": state.get("attack", "Unknown"),
        "analysis":
            f"{investigation.get('attack_behavior', '')} "
            f"{investigation.get('possible_impact', '')}"
    }
    return {
        "memory": retrieve_similar_incidents(combined_result)
    }

def planning_node(state):
    investigation = state.get("investigation")
    if investigation is None:
        return {}

    combined_result = investigation.copy()
    combined_result["attack"] = state.get("attack", "Unknown")
    combined_result["confidence"] = state.get("confidence", 0.0)
    combined_result["similar_incident"] = state.get("memory")
    
    plan = generate_plan(combined_result)
    if plan is None:
        return {"status": "Agent Failure"}
        
    return {
        "plan": plan
    }

def response_node(state):
    plan = state.get("plan")
    investigation = state.get("investigation")
    if plan is None or investigation is None:
        return {}

    alert = create_security_alert(state.get("attack", "Unknown"), investigation, plan)
    execute_plan(plan)
    return {
        "response": {"alert": alert}
    }

def verification_node(state):
    plan = state.get("plan")
    if plan is None:
        return {"retry_count": 1}

    expected_changes = get_expected_plan(plan)
    execution_success = verify_execution(expected_changes)
    
    store_verified_incident(state.get("attack", "Unknown"), state.get("investigation", {}), plan, execution_success)

    retry_increment = 0 if execution_success.get("outcome") == "Threat Mitigated" else 1

    return {
        "verification": execution_success.get("verification", "Unknown"),
        "status": execution_success.get("outcome", "Unknown"),
        "retry_count": retry_increment
    }