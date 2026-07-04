import json
from detect.xgboostpred import predict_attack
from detect.anomalyscore import detect_anomaly

def capture_before_state(investigation_report):
    before_state = {
        "attack": investigation_report["attack"],
        "confidence": investigation_report["confidence"],
        "anomaly_score": investigation_report["anomaly_score"],
        "severity": investigation_report["severity"],
        "threat_type": investigation_report["threat_type"]
    }
    return before_state

def capture_after_state(updated_sample):
    zero_day_result = detect_anomaly(updated_sample , True)
    detection_result = predict_attack(updated_sample)

    attack = detection_result["attack"]
    confidence = detection_result["confidence"]
    anomaly_score = zero_day_result["anomaly_score"]
    
    if confidence > 0.75:
        threat_type = "Known Attack"
    elif anomaly_score > 0.85:
        attack = "Unknown"
        confidence = 0
        threat_type = "Potential Zero-Day Threat"
    else:
        threat_type = "Suspicious Activity"

    after_state = {
        "attack": attack,
        "confidence": confidence,
        "anomaly_score": anomaly_score,
        "threat_type": threat_type,
    }
    return after_state

def verify_execution(expected_changes):
    with open("prompts/system_state.json", "r") as f:
        system_state = json.load(f)
    for key, value in expected_changes.items():
        if system_state.get(key) != value:
            return False
    return True

def verify_response(before_state ,  after_state ,  execution_success):
    before_score = before_state["anomaly_score"]
    after_score = after_state["anomaly_score"]

    if before_score == 0:
        improvement = 0
    else:
        improvement = ((before_score - after_score) / before_score) * 100

    if not execution_success:
        verification = "Response Execution Failed"
        outcome = "Expected actions were not applied"

    elif ( after_state["attack"] == "Benign"  and after_state["anomaly_score"] < 0.5  and after_score <= before_score):
        verification = "Success"
        outcome = "Threat Mitigated"

    elif (after_state["anomaly_score"] < before_state["anomaly_score"]):
        verification = "Partial Success"
        outcome = "Threat Reduced"

    else:
        verification = "Failed"
        outcome = "Threat Still Active"

    return {
        "verification": verification,
        "before_score": before_score,
        "after_score": after_score,
        "improvement": round(improvement, 2),
        "outcome": outcome
    }
