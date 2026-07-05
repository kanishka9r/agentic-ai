import os
from dotenv import load_dotenv #Read API key from .env
from google import genai
from detect.xgboostpred import predict_attack
from detect.anomalyscore import detect_anomaly
import json
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def investigate(attack , confidence , anomaly_score , threat_type):
    if attack == "Benign":
        severity = "Low" 
    elif anomaly_score > 0.9:
        severity = "Critical"
    elif anomaly_score > 0.5:
        severity = "High"
    else:
        severity = "Medium"

    with open("prompts/investigation_prompt.txt","r") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        threat_type=threat_type,
        attack=attack,
        confidence=confidence,
        anomaly_score=anomaly_score,
        severity=severity
    )
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            break  
        except Exception as e:
            if "503" in str(e):
                if attempt < 2:
                   print("Gemini server busy. Please wait...")
                   time.sleep(5)
                else:
                    print("Gemini server is still busy. Please try again later.")
                    return None
            elif "429" in str(e):
                    print("Gemini API quota exceeded. Please try again later.")
                    return None
            else:
                print("Gemini Error:", e)
                return None
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        print("Invalid JSON returned by Gemini.")
        return None
    
    return {
    "severity": severity,     
    "threat_type": threat_type,
    "threat_explanation":
        result["threat_explanation"],
    "possible_impact":
        result["possible_impact"],
    "attack_behavior":
        result["attack_behavior"],
    "llm_severity":
        result["severity"]
}