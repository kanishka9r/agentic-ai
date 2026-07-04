import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from detect.autoencoder import AutoEncoder

# Load Components
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
    )

scaler = joblib.load("models/scaler.pkl")
ae_threshold = joblib.load("models/threshold.pkl")
ocsvm = joblib.load("models/ocsvm.pkl")

# determine feature count
sample_data = pd.read_csv("data/processed/X_test.csv",nrows=1)
input_dim = sample_data.shape[1]
autoencoder = AutoEncoder(input_dim).to(device)
autoencoder.load_state_dict(torch.load( "models/autoencoder.pth",map_location=device))
autoencoder.eval()


# Zero-Day Agent
def detect_anomaly(features , already_scaled = False):
    # Scale features
    if already_scaled:
        features_scaled = features.values
    else:
        features_scaled = scaler.transform(features)

    # Autoencoder
    tensor = torch.tensor(features_scaled,dtype=torch.float32).to(device)

    with torch.no_grad():
        reconstructed = autoencoder(tensor)
    ae_error = torch.mean( (tensor - reconstructed) ** 2, dim=1).cpu().numpy()[0]
    ae_pred = int(ae_error > ae_threshold)

    # OCSVM
    oc_pred = int(ocsvm.predict(features_scaled)[0] == -1)
    oc_score = float(-ocsvm.decision_function(features_scaled)[0])

    # Hybrid Score
    ae_score_norm = min(ae_error / ae_threshold,1.0)
    oc_min = -315.49829497628366
    oc_max = 393.7218142318461
    oc_score_norm = (oc_score -oc_min) / (oc_max - oc_min)
    oc_score_norm = np.clip(oc_score_norm,0,1)
    hybrid_score = ( ae_score_norm +oc_score_norm) / 2

    # Hybrid Decision (OR)
    is_anomaly = (ae_pred == 1 or oc_pred == 1)
    status = (
        "Potential Threat"
        if is_anomaly
        else "Normal"
    )
    return {
        "status": status,
        "anomaly_score": round(float(hybrid_score), 4)
    }