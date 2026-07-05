import json

def verify_execution(expected_changes):
    with open("prompts/system_state.json", "r") as f:
        system_state = json.load(f)

    for key, value in expected_changes.items():
        if system_state.get(key) != value:
            return {
                "verification": "Failed",
                "outcome": "Response Execution Failed"
            }

    # verify the effect.
    threat_status = system_state.get("threat_status")

    if threat_status == "contained":
        return {
            "verification": "Success",
            "outcome": "Threat Mitigated"
        }
    elif threat_status == "under_investigation":
        return {
            "verification": "Partial Success",
            "outcome": "Threat Reduced"
        }
    else:
        return {
            "verification": "Failed",
            "outcome": "Threat Still Active"
        }