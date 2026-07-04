import os
import joblib
import numpy as np
import pandas as pd
from sklearn.svm import OneClassSVM

# Config
train_path = "data/processed/normal_only.csv"
model_path = "models/ocsvm.pkl"
os.makedirs("models", exist_ok=True)

# Load Training Data
X_train = pd.read_csv(train_path).sample(n=50000,random_state=42).values
print("Training Shape:", X_train.shape)

# Train OC-SVM
ocsvm = OneClassSVM(kernel="rbf",gamma="scale",nu=0.10)

print("\nTraining OC-SVM...")
ocsvm.fit(X_train)

#Save Model
joblib.dump(ocsvm,model_path)
print("\nModel Saved:",model_path)
