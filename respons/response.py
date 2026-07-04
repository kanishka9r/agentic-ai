from .action import *
from .expected import *

action_map = {
    # Benign
    "No Action Required": no_action_required,
    "Continue Monitoring":enable_monitoring,
    "Log Activity": log_activity,

    # BruteForce
    "Block Source IP": block_source_ip,
    "Enable Rate Limiting": enable_rate_limiting,
    "Reset Compromised Credentials": reset_credentials,
    "Generate Alert": generate_alert,

    # DDoS
    "Block Malicious Traffic": block_malicious_traffic,
    "Enable DDoS Protection": enable_ddos_protection,
    "Apply Traffic Filtering": apply_traffic_filtering,

    # DoS
    "Apply Rate Limiting": apply_rate_limiting,
    "Restrict Excessive Connections":restrict_connections,

    # Malware
    "Isolate Device": isolate_device,
    "Terminate Malicious Process": terminate_malicious_process,
    "Perform Malware Scan": perform_malware_scan,

    # Mirai
    "Block Outbound Traffic": block_outbound_traffic,
    "Monitor Device": enable_monitoring,

    # Recon
    "Block Suspicious Scanner": block_suspicious_scanner,
    "Restrict Network Access": restrict_network_access,
    "Increase Monitoring": enable_monitoring,

    # Spoofing
    "Block Suspicious Traffic": block_suspicious_traffic,
    "Verify Device Identity": verify_identity,
    "Enable Packet Validation": enable_packet_validation,

    # WebAttack
    "Block Malicious Requests": block_malicious_requests,
    "Enable Web Application Firewall": enable_web_application_firewall,
    "Monitor Web Traffic": enable_monitoring,

    # Unknown Threat
    "Escalate Investigation": escalate_investigation
}   

def execute_plan(plan):
    for step in plan["recommended_actions"]:
        action = step["action"]
        action_map[action]()
        
def get_expected_plan(plan):
    expected_changes = {}
    for step in plan["recommended_actions"]:
        expected_changes.update(expected_change_map[step["action"]])
    return expected_changes
