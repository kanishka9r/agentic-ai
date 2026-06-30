import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

input_file = "../data/processed/ciciot23_9class.csv"
output_file = "../data/processed/normal_only.csv"
scaler_file = "../models/scaler.pkl"

# Load dataset
df = pd.read_csv(input_file)
print("Original Shape:", df.shape)

# Check class distribution
print("\nClass Distribution:")
print(df["label"].value_counts())

# Keep only benign traffic
normal_df = df[df["label"] == "Benign"].copy()
print("\nBenign Shape:", normal_df.shape)

# Remove label column
normal_df = normal_df.drop(columns=["label"])
print("Features Only Shape:", normal_df.shape)

# Scale features
scaler = StandardScaler()
normal_scaled = scaler.fit_transform(normal_df)

# Convert back to DataFrame
normal_scaled_df = pd.DataFrame(normal_scaled,columns=normal_df.columns)

# Create folders if needed
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Save scaled data
normal_scaled_df.to_csv(output_file, index=False)

# Save scaler
joblib.dump(scaler, scaler_file)

print(f"\nScaled data saved to: {output_file}")
print(f"Scaler saved to: {scaler_file}")
print(normal_scaled_df.mean().head())
print(normal_scaled_df.std().head())