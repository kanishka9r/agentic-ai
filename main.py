import pandas as pd
import json
from invest.investigation import investigate
from mem.memory import retrieve_similar_incidents
from mem.memory import store_verified_incident
from plan.planning import generate_plan
from respons.alert import create_security_alert
from respons.response import execute_plan
from respons.response import get_expected_plan
from respons.action import reset_system_state
from verify.verification import capture_before_state
from verify.verification import verify_response
from verify.verification import capture_after_state
from verify.verification import verify_execution


X = pd.read_csv("data/processed/X_val.csv")
y = pd.read_csv("data/processed/y_val.csv")
updated_sample = pd.read_csv("data/processed/verification_sample.csv")
class_names = {
    0: "Benign",
    1: "BruteForce",
    2: "DDoS",
    3: "DoS",
    4: "Malware",
    5: "Mirai",
    6: "Recon",
    7: "Spoofing",
    8: "WebAttack"
}
target = 4
idx = y[y.iloc[:, 0] == target].sample(1, random_state=42).index[0]
sample = X.iloc[[idx]]
print(f"Testing: {class_names[target]}")
print("\n")

reset_system_state()

investigation_report = investigate(sample)
if investigation_report is None:
    print("Pipeline stopped because Investigation Agent failed.")
    exit()
before_state = capture_before_state(investigation_report)

memory_query = {
        "attack": investigation_report["attack"],
        "analysis":
            f"{investigation_report["attack_behavior"]} "
            f"{investigation_report["possible_impact"]}"
    }
memory_results = retrieve_similar_incidents(memory_query)

combined_result = {**investigation_report,"similar_incident": memory_results}
plan = generate_plan(combined_result)
if plan is None:
    print("Pipeline stopped because Planning Agent failed.")
    exit()

expected_changes = get_expected_plan(plan)
execute_plan(plan)

alert = create_security_alert(investigation_report,plan)

after_state = capture_after_state(updated_sample)
execution_success = verify_execution(expected_changes)
verification_result = verify_response(before_state,after_state , execution_success)

with open("prompts/system_state.json", "r") as f:
    current_state = json.load(f)

print("\n=== Investigation Report ===")
print(investigation_report)

print("\n=== Memory Result ===")
print(memory_results)

print("\n=== Final Plan ===")
print(plan)

print("\n=== Alert ===")
print(alert)

print("\n=== Verification Result ===")
print(verification_result)

print("\n=== Current System State ===")
print(json.dumps(current_state, indent=4))