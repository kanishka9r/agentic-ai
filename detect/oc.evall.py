import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# Load Data
scaler = joblib.load("models/scaler.pkl")
X_test = pd.read_csv("data/processed/X_test.csv")
X_test = scaler.transform(X_test)
y_test = pd.read_csv( "data/processed/y_test.csv").values.flatten()

# Binary Labels
y_true = (y_test != 0).astype(int)
print(
    "Normal:",
    np.sum(y_true == 0)
)
print(
    "Attack:",
    np.sum(y_true == 1)
)

# Load Model
ocsvm = joblib.load("models/ocsvm.pkl")

# Prediction
preds = ocsvm.predict(X_test)

# sklearn: +1 = normal ; -1 = anomaly
y_pred = ( preds == -1).astype(int)
np.save("models/ocsvm_predictions.npy", y_pred)
print("OC-SVM predictions saved")

# anomaly score
scores = -ocsvm.decision_function(X_test)

# Metrics
print("\nAccuracy:",accuracy_score( y_true, y_pred))
print("Precision:",precision_score( y_true, y_pred ))
print( "Recall:",recall_score( y_true, y_pred))
print("F1:",f1_score( y_true,   y_pred))
print("ROC-AUC:",roc_auc_score( y_true, scores))
print("\nConfusion Matrix")
cm = confusion_matrix(y_true,y_pred)
pd.DataFrame(cm).to_csv("data/plots/confusion_matrix_oc.csv",index=False)
print( cm)
print( "\nClassification Report")
print(classification_report( y_true, y_pred))

# Per Class Recall
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

for cls in range(1, 9):
    idx = (y_test == cls)
    total = np.sum(idx)
    detected = np.sum(
        y_pred[idx] == 1
    )
    recall = detected / total
    print(
        f"{class_names[cls]:12s} "
        f"Recall: {recall:.4f} "
        f"({detected}/{total})"
    )

print(scores.min())
print(scores.max())
print(scores.mean())