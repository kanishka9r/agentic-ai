import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os
import joblib
from detect.autoencoder import AutoEncoder

os.makedirs("models", exist_ok=True)

# Load and split data
df = pd.read_csv("data/processed/normal_only.csv")
X = df.values.astype(np.float32)
X_train, X_val = train_test_split( X, test_size=0.2,random_state=42)
print("Train:", X_train.shape)
print("Validation:", X_val.shape)

# Dataset
batch_size = 1024
train_dataset = TensorDataset(torch.tensor(X_train))
train_loader = DataLoader(train_dataset , batch_size=batch_size , shuffle=True)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print (device)

# Model
input_dim = X_train.shape[1]
model = AutoEncoder(input_dim).to(device)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
epochs = 20
losses = []

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for (batch,) in train_loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        reconstructed = model(batch)
        loss = criterion(reconstructed, batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    losses.append(avg_loss)

    print(  f"Epoch [{epoch+1}/{epochs}] " f"Loss: {avg_loss:.6f}")

#Validation
model.eval()

X_val_tensor = torch.tensor(X_val,dtype=torch.float32).to(device)

with torch.no_grad():
    reconstructed = model( X_val_tensor)
errors = torch.mean((X_val_tensor - reconstructed) ** 2,  dim=1 ).cpu().numpy()

#Threshold
threshold = np.percentile( errors, 98)
print(f"\nThreshold: {threshold:.6f}")

#Prediction
preds = errors > threshold
print(f"Flagged: {preds.sum()}")
print(f"FP Rate: {preds.mean():.4f}")

#Save threshold
joblib.dump(threshold,"models/threshold.pkl")

#Save Model
torch.save( model.state_dict(), "models/autoencoder.pth")

# Plot Loss Curve
plt.figure(figsize=(8, 5))
plt.plot(range(1, epochs + 1), losses, marker='o')
plt.title("Autoencoder Training Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.grid(True)

plt.savefig("data/plots/loss_curve.png", dpi=300 ,  bbox_inches="tight")
plt.show()
plt.close()

# Error Distribution Plot
plt.figure(figsize=(8,5))
plt.hist(errors[errors < np.percentile(errors,99.9)],bins=100)
plt.axvline(threshold,color='red',linestyle='--',label=f'Threshold={threshold:.4f}')
plt.legend()
plt.title("Error Distribution")
plt.xlabel("Reconstruction Error")
plt.ylabel("Count")
plt.savefig( "data/plots/error_distribution.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()