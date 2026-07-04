import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import joblib
from detect.autoencoder import AutoEncoder
from sklearn.metrics import ( accuracy_score, precision_score, recall_score, f1_score,roc_auc_score,confusion_matrix,classification_report)

# Load Data
scaler = joblib.load("models/scaler.pkl")
X_test = pd.read_csv("data/processed/X_test.csv")
X_test = scaler.transform(X_test)
X_test = X_test.astype(np.float32)
y_test = pd.read_csv("data/processed/y_test.csv").values.flatten()

# Binary Labels ; Benign = 0 ; Attack = 1
y_true = (y_test != 0).astype(int)
print("Normal:", np.sum(y_true == 0))
print("Attack:", np.sum(y_true == 1))

# Load Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoEncoder( input_dim=X_test.shape[1]).to(device)
model.load_state_dict(torch.load("models/autoencoder.pth",map_location=device))

# Evaluation  and Threshold
model.eval()
threshold = joblib.load("models/threshold.pkl")
print(
    f"Threshold (98%): "
    f"{threshold:.6f}"
)

# Reconstruction Error
X_tensor = torch.tensor( X_test, dtype=torch.float32).to(device)
with torch.no_grad():
    reconstructed = model(X_tensor)
errors = torch.mean((X_tensor - reconstructed) ** 2,dim=1).cpu().numpy()

# Prediction and save prediction
y_pred = (errors > threshold).astype(int)
np.save("models/ae_predictions.npy",y_pred)
print("AE predictions saved")

# Metrics
print("\nAccuracy:",
      accuracy_score(y_true, y_pred))
print("Precision:",
      precision_score(y_true, y_pred))
print("Recall:",
      recall_score(y_true, y_pred))
print("F1:",
      f1_score(y_true, y_pred))
print("ROC-AUC:",
      roc_auc_score(y_true,errors))
print("\nConfusion Matrix")
cm = confusion_matrix(y_true,y_pred)
pd.DataFrame(cm).to_csv("data/plots/confusion_matrix.csv",index=False)
print( cm)
print("\nClassification Report")
print(classification_report(y_true,y_pred))

#Class wise recall
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

print("\nPer-Class Detection Rate")

for cls in range(1, 9):  # skip benign
    idx = (y_test == cls)
    total = np.sum(idx)
    detected = np.sum(y_pred[idx] == 1)
    recall = detected / total
    print(
        f"{class_names[cls]:12s} "
        f"Recall: {recall:.4f} "
        f"({detected}/{total})"
    )

