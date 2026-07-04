import pandas as pd
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.metrics import ( accuracy_score, classification_report, precision_score, recall_score, f1_score)
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import joblib

os.makedirs("models", exist_ok=True)

# LOAD DATA
X_train = pd.read_csv("data/processed/X_train.csv")
y_train = pd.read_csv("data/processed/y_train.csv").squeeze()

X_val = pd.read_csv("data/processed/X_val.csv")
y_val = pd.read_csv("data/processed/y_val.csv").squeeze()

print("Train:", X_train.shape, y_train.shape)
print("Validation:", X_val.shape, y_val.shape)

# MODEL
model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    eval_metric="mlogloss"
)

# CLASS WEIGHT
class_weights =  {
    0: 1.0,   # Benign
    1: 10.0,  # BruteForce
    2: 1.0,   # DDoS
    3: 1.0,   # DoS
    4: 20.0,  # Malware
    5: 1.0,   # Mirai
    6: 2.0,   # Recon
    7: 2.0,   # Spoofing
    8: 10.0   # WebAttack
}

#SAMPLE WEIGHTS
sample_weights = np.array([class_weights[y] for y in y_train])

# TRAIN
print("\nTraining XGBoost...")
model.fit(X_train, y_train , sample_weight=sample_weights)

# PREDICT
y_pred = model.predict(X_val)

#CONFUSION MATRIX
cm = confusion_matrix(y_val, y_pred)
class_names = [
    "Benign",
    "BruteForce",
    "DDoS",
    "DoS",
    "Malware",
    "Mirai",
    "Recon",
    "Spoofing",
    "WebAttack"
]
cm_norm = cm.astype(float) / cm.sum(axis=1)[:, None]
cm_df = pd.DataFrame(cm_norm,index=class_names,columns=class_names)

# Create plots folder
os.makedirs("data/plots", exist_ok=True)
# Plot
plt.figure(figsize=(12, 10))
sns.heatmap(cm_df,annot=True,fmt=".2f",cmap="Blues",vmin=0,vmax=1)
plt.title("Confusion Matrix")
plt.ylabel("Actual Class")
plt.xlabel("Predicted Class")
plt.tight_layout()

# Save
plt.savefig("data/plots/confusion_matrix.png",dpi=300,bbox_inches="tight")
plt.close()

print("\nConfusion Matrix saved:")
print("data/plots/confusion_matrix.png")

# METRICS
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val,y_pred,average="weighted")
recall = recall_score( y_val, y_pred, average="weighted")
f1 = f1_score(y_val,y_pred,average="weighted")
report = classification_report(y_val,y_pred)

# PRINT
print("\nAccuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)
print("\nClassification Report:\n")
print(report)


feature_importance = pd.DataFrame({"Feature": X_train.columns,"Importance": model.feature_importances_})
feature_importance = feature_importance.sort_values( by="Importance", ascending=False)

print("\nTop 20 Features:")
print(feature_importance.head(20))

joblib.dump(model, "models/xgb_model.pkl")