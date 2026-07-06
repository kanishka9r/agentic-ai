import chromadb
import uuid
from datetime import datetime

# ChromaDB connection
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="incidents")

def retrieve_similar_incidents(memory_query):
    query_text = f"""Attack: {memory_query['attack']} Analysis: {memory_query['analysis']} """
    results = collection.query(query_texts=[query_text] , n_results=1)
    if not results.get("documents") or not results["documents"][0]:
        return None
    distance = results["distances"][0][0]
    if distance > 0.8 :
        return None
    return results["documents"][0][0]

def store_verified_incident(attack , investigation_report,plan,verification_result):
    document = f"""
    Attack:
    {attack}
    Attack Behavior:
    {investigation_report.get('attack_behavior', '')}
    Possible Impact:
    {investigation_report.get('possible_impact', '')}
    Response:
    {", ".join(
       step.get("action", "")
       for step in plan.get("recommended_actions", [])
    )}
    Outcome:
    {verification_result.get("outcome", "")}
    """
    metadata = {
        "severity": investigation_report.get("severity", "Unknown"),
        "verification": verification_result.get("verification", "Unknown"),
        "timestamp": datetime.now().isoformat()
    }
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[document],
        metadatas=[metadata]
    )