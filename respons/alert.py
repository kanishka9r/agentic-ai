import json
from datetime import datetime

def create_security_alert(attack , investigation_report, plan):
    alert = {
        "timestamp": datetime.now().isoformat(),
        "attack": attack,
        "severity": investigation_report["severity"],
        "status": "Response Executed",
        "actions_taken": [
            step["action"]
            for step in plan["recommended_actions"]
        ]
    }

    try:
        with open("prompts/alerts.json", "r") as f:
            alerts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = [] 

    alerts.append(alert)
    with open("prompts/alerts.json", "w") as f:
        json.dump(alerts, f, indent=4)

    return alert