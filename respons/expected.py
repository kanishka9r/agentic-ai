expected_change_map = {
    # Benign
    "No Action Required": {},

    "Log Activity": {},

    "Continue Monitoring": {
        "monitoring": "enabled"
    },

    # BruteForce
    "Block Source IP": {
        "network_status": "blocked",
        "threat_status": "contained"
    },

    "Enable Rate Limiting": {
        "network_status": "restricted",
        "traffic_filtering": "enabled"
    },

    "Reset Compromised Credentials": {
        "credential_status": "reset",
        "threat_status": "contained"
    },

    "Generate Alert": {
        "alert_status": "generated"
    },

    # DDoS
    "Block Malicious Traffic": {
        "network_status": "blocked",
        "threat_status": "contained"
    },

    "Enable DDoS Protection": {
        "traffic_filtering": "enabled",
        "monitoring": "enabled"
    },

    "Apply Traffic Filtering": {
        "traffic_filtering": "enabled",
        "network_status": "restricted"
    },

    # DoS
    "Apply Rate Limiting": {
        "network_status": "restricted",
        "traffic_filtering": "enabled"
    },

    "Restrict Excessive Connections": {
        "network_status": "restricted",
        "monitoring": "enabled"
    },

    # Malware
    "Isolate Device": {
        "device_status": "isolated",
        "network_status": "restricted",
        "threat_status": "contained"
    },

    "Terminate Malicious Process": {
        "malware_status": "removed",
        "threat_status": "contained"
    },

    "Perform Malware Scan": {
        "malware_status": "scanning",
        "monitoring": "enabled"
    },

    # Mirai
    "Block Outbound Traffic": {
        "network_status": "blocked",
        "threat_status": "contained"
    },

    "Monitor Device": {
        "monitoring": "enabled"
    },

    # Recon
    "Block Suspicious Scanner": {
        "network_status": "blocked",
        "monitoring": "enabled"
    },

    "Restrict Network Access": {
        "network_status": "restricted",
        "device_status": "isolated"
    },

    "Increase Monitoring": {
        "monitoring": "enabled"
    },

    # Spoofing
    "Block Suspicious Traffic": {
        "network_status": "blocked",
        "traffic_filtering": "enabled"
    },

    "Verify Device Identity": {
        "identity_status": "verified",
        "threat_status": "contained"
    },

    "Enable Packet Validation": {
        "identity_status": "validated",
        "traffic_filtering": "enabled"
    },

    # WebAttack
    "Block Malicious Requests": {
        "network_status": "blocked",
        "traffic_filtering": "enabled"
    },

    "Enable Web Application Firewall": {
        "traffic_filtering": "enabled",
        "monitoring": "enabled"
    },

    "Monitor Web Traffic": {
        "monitoring": "enabled"
    },

    # Unknown Threat
    "Escalate Investigation": {
        "monitoring": "enabled",
        "alert_status": "generated",
        "threat_status": "under_investigation"
    }
}