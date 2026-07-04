import chromadb
import uuid
from datetime import datetime

# ChromaDB connection
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="incidents")

def retrieve_similar_incidents(memory_query):
    query_text = f"""Attack: {memory_query['attack']} Analysis: {memory_query['analysis']} """
    results = collection.query(query_texts=[query_text] , n_results=1)
    if not results["documents"][0]:
        return None
    distance = results["distances"][0][0]
    if distance > 0.8 :
        return None
    return results["documents"][0][0]

def store_verified_incident(investigation_report,plan,verification_result):
    document = f"""
    Attack: {investigation_report['attack']}
    Attack Behavior:
    {investigation_report['attack_behavior']}
    Possible Impact:
    {investigation_report['possible_impact']}
    Response:
    {", ".join(
       step["action"]
       for step in plan["recommended_actions"]
    )}
    Outcome:
    {verification_result["outcome"]}
    """
    metadata = {
        "severity": investigation_report["severity"],
        "verification": verification_result["verification"],
        "timestamp": datetime.now().isoformat()
    }
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[document],
        metadatas=[metadata]
    )