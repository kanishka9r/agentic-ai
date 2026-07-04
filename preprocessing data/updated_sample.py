import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from detect.autoencoder import AutoEncoder


# Load Models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ae_threshold = joblib.load("models/threshold.pkl")
ocsvm = joblib.load("models/ocsvm.pkl")

normal_df = pd.read_csv("data/processed/normal_only.csv")
input_dim = normal_df.shape[1]

autoencoder = AutoEncoder(input_dim).to(device)
autoencoder.load_state_dict(torch.load("models/autoencoder.pth", map_location=device))
autoencoder.eval()

# Compute Hybrid Score
scores = []

oc_min = -315.49829497628366
oc_max = 393.7218142318461

for idx in range(len(normal_df)):
    sample = normal_df.iloc[[idx]]
    tensor = torch.tensor(sample.values, dtype=torch.float32).to(device)

    with torch.no_grad():
        reconstructed = autoencoder(tensor)
    ae_error = torch.mean((tensor - reconstructed) ** 2,dim=1).cpu().numpy()[0]
    ae_score = min(ae_error / ae_threshold, 1.0)
    oc_score = float(-ocsvm.decision_function(sample.values)[0])
    oc_score = (oc_score - oc_min) / (oc_max - oc_min)
    oc_score = np.clip(oc_score, 0, 1)
    hybrid = (ae_score + oc_score) / 2
    scores.append(hybrid)

scores = np.array(scores)

# find representative sample
median_score = np.median(scores)
best_index = np.argmin(np.abs(scores - median_score))

print("Median anomaly score :", round(median_score, 4))
print("Representative index :", best_index)
print("Representative score :", round(scores[best_index], 4))

# Save representative benign sample
representative_sample = normal_df.iloc[[best_index]]
representative_sample.to_csv(
    "data/processed/verification_sample.csv",
    index=False
)

print("\nRepresentative benign sample saved.")
