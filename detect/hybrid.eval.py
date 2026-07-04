import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

#Load Data
y_test = pd.read_csv("data/processed/y_test.csv").values.flatten()
y_true = (y_test != 0).astype(int)

ae_pred = np.load("models/ae_predictions.npy")
ocsvm_pred = np.load("models/ocsvm_predictions.npy")

# Hybrid Prediction
hybrid_pred = ((ae_pred == 1) |(ocsvm_pred == 1)).astype(int)

# Metrics
print("\nAccuracy:",accuracy_score( y_true, hybrid_pred))
print("Precision:",precision_score(y_true,hybrid_pred))
print("Recall:",recall_score(y_true,hybrid_pred))
print("F1:",f1_score(y_true,hybrid_pred))
print("\nConfusion Matrix")
cm = confusion_matrix(y_true,hybrid_pred)
pd.DataFrame(cm).to_csv(
    "data/plots/confusion_matrix_hybrid.csv",
    index=False
)
print( cm)
print("\nClassification Report")
print(classification_report(y_true,hybrid_pred))

#Per Call Recall
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
print(
    "\nPer-Class Detection Rate"
)

for cls in range(1, 9):
    idx = (y_test == cls)
    total = np.sum(idx)
    detected = np.sum(
        hybrid_pred[idx] == 1
    )
    recall = detected / total
    print(
        f"{class_names[cls]:12s} "
        f"Recall: {recall:.4f} "
        f"({detected}/{total})"
    )