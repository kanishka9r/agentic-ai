import joblib
import pandas as pd

# Load model
model = joblib.load("models/xgb_model.pkl")

# Label mapping
label_map = {
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

def predict_attack(features):
    pred = model.predict(features)[0]
    probs = model.predict_proba(features)[0]
    confidence = float(max(probs))
    return {
        "attack": label_map[pred],
        "confidence": round(confidence, 4)
    }

if __name__ == "__main__":
    #load data
    X_val = pd.read_csv("data/processed/X_val.csv")
    y_val = pd.read_csv("data/processed/y_val.csv").squeeze()
   
    for i in range(10):
        sample = X_val.iloc[[i]]
        result = predict_attack(sample)
        actual = y_val.iloc[i]
  
        print(
        f"Actual: {label_map[actual]} | "
        f"Predicted: {result['attack']} | "
        f"Confidence: {result['confidence']}"
    )