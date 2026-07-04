import json

def load_system_state():
    with open("prompts/system_state.json", "r") as f:
        return json.load(f)

def save_system_state(state):
    with open("prompts/system_state.json", "w") as f:
        json.dump(state, f, indent=4)

def apply_changes(changes):
    system_state = load_system_state()
    system_state.update(changes)
    save_system_state(system_state)
    return changes

def no_action_required():
    return {}

def log_activity():
    return {}

def enable_monitoring():
    return apply_changes({
        "monitoring": "enabled"
    })

def block_source_ip():
    return apply_changes({
        "network_status": "blocked",
        "threat_status": "contained"
    })

def enable_rate_limiting():
    return apply_changes({
        "network_status": "restricted",
        "traffic_filtering": "enabled"
    })

def reset_credentials():
    return apply_changes({
        "credential_status": "reset",
        "threat_status": "contained"
    })

def generate_alert():
    return apply_changes({
        "alert_status": "generated"
    })

def block_malicious_traffic():
    return apply_changes({
        "network_status": "blocked",
        "threat_status": "contained"
    })

def enable_ddos_protection():
    return apply_changes({
        "traffic_filtering": "enabled",
        "monitoring": "enabled"
    })

def apply_traffic_filtering():
    return apply_changes({
        "traffic_filtering": "enabled",
        "network_status": "restricted"
    })

def apply_rate_limiting():
    return apply_changes({
        "network_status": "restricted",
        "traffic_filtering": "enabled"
    })

def restrict_connections():
    return apply_changes({
        "network_status": "restricted",
        "monitoring": "enabled"
    })

def isolate_device():
    return apply_changes({
        "device_status": "isolated",
        "network_status": "restricted",
        "threat_status": "contained"
    })

def terminate_malicious_process():
    return apply_changes({
        "malware_status": "removed",
        "threat_status": "contained"
    })

def perform_malware_scan():
    return apply_changes({
        "malware_status": "scanning",
        "monitoring": "enabled"
    })

def block_outbound_traffic():
    return apply_changes({
        "network_status": "blocked",
        "threat_status": "contained"
    })

def block_suspicious_scanner():
    return apply_changes({
        "network_status": "blocked",
        "monitoring": "enabled"
    })

def restrict_network_access():
    return apply_changes({
        "network_status": "restricted",
        "device_status": "isolated"
    })

def block_suspicious_traffic():
    return apply_changes({
        "network_status": "blocked",
        "traffic_filtering": "enabled"
    })

def verify_identity():
    return apply_changes({
        "identity_status": "verified",
        "threat_status": "contained"
    })

def enable_packet_validation():
    return apply_changes({
        "identity_status": "validated",
        "traffic_filtering": "enabled"
    })

def block_malicious_requests():
    return apply_changes({
        "network_status": "blocked",
        "traffic_filtering": "enabled"
    })

def enable_web_application_firewall():
    return apply_changes({
        "traffic_filtering": "enabled",
        "monitoring": "enabled"
    })

def escalate_investigation():
    return apply_changes({
        "monitoring": "enabled",
        "alert_status": "generated",
        "threat_status": "under_investigation"
    }) 

def reset_system_state():
    default_state = {
        "network_status": "normal",
        "traffic_filtering": "disabled",
        "monitoring": "disabled",
        "alert_status": "none",
        "device_status": "active",
        "credential_status": "valid",
        "identity_status": "unverified",
        "malware_status": "none",
        "threat_status": "active"
    }
    with open("prompts/system_state.json", "w") as f:
        json.dump(default_state, f, indent=4)