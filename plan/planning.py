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

    attack = combined_result["attack"]
    mitigation_actions = mitigation_library.get(attack, mitigation_library["Unknown Threat"])    

    prompt = prompt_template.format(
        attack=combined_result["attack"],
        threat_explanation=combined_result["threat_explanation"],
        possible_impact=combined_result["possible_impact"],
        severity=combined_result["severity"],
        similar_incident=combined_result["similar_incident"],
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
        if step["action"] in approved_actions:
            validated_actions.append(step)
    plan["recommended_actions"] = validated_actions
    return plan




