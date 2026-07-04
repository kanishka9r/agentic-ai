import chromadb
import uuid
import os
import shutil

if os.path.exists("memory_db"):
    shutil.rmtree("memory_db")
 
client = chromadb.PersistentClient(path="./memory_db")

# Create fresh collection
collection = client.get_or_create_collection(name="incidents")

# New incidents
incidents = [
    {
        "attack": "DDoS",
        "analysis": "Traffic flooding attack detected",
        "response": "Block Malicious Traffic, Apply Traffic Filtering, Enable DDoS Protection",
        "outcome": "Traffic blocked"
    },
    {
        "attack": "Mirai",
        "analysis": "Mirai botnet activity detected",
        "response": "Isolate Device, Block Outbound Traffic, Monitor Device",
        "outcome": "Threat mitigated"
    },
    {
        "attack": "Recon",
        "analysis": "Port scanning activity detected",
        "response": "Block Suspicious Scanner, Restrict Network Access, Increase Monitoring",
        "outcome": "Reconnaissance stopped"
    },
    {
        "attack": "Malware",
        "analysis": "Malicious payload execution detected",
        "response": "Isolate Device, Terminate Malicious Process, Perform Malware Scan",
        "outcome": "Malware contained"
    },
    {
        "attack": "BruteForce",
        "analysis": "Repeated authentication failures detected",
        "response": "Block Source IP, Enable Rate Limiting, Reset Compromised Credentials",
        "outcome": "Unauthorized access prevented"
    }
]
# Store incidents
for incident in incidents:
    document = f"""
Attack: {incident['attack']}
Analysis: {incident['analysis']}
Response: {incident['response']}
Outcome: {incident['outcome']}
"""
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[document]
    )

print("Memory database refilled successfully.")
print("Total incidents:", collection.count())


