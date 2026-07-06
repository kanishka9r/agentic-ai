import os
import json
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_plan(combined_result):
    with open("prompts/planning_prompt.txt","r") as f:
        prompt_template = f.read()

    with open("prompts/mitigation_library.json","r") as f:
        mitigation_library = json.load(f)    

    attack = combined_result.get("attack", "Unknown")
    mitigation_actions = mitigation_library.get(attack, mitigation_library.get("Unknown Threat", []))    

    prompt = prompt_template.format(
        attack=combined_result.get("attack", "Unknown"),
        threat_explanation=combined_result.get("threat_explanation", ""),
        possible_impact=combined_result.get("possible_impact", ""),
        severity=combined_result.get("severity", ""),
        similar_incident=combined_result.get("similar_incident", ""),
        mitigation_actions="\n".join(mitigation_actions)
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
        plan = json.loads(response.text)
    except json.JSONDecodeError:
        print("Invalid JSON returned by Gemini.")
        return None
    
    #validation
    approved_actions = set(mitigation_actions)
    validated_actions = []
    for step in plan.get("recommended_actions", []):
        if step.get("action") in approved_actions:
            validated_actions.append(step)
    plan["recommended_actions"] = validated_actions
    return plan




