import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/processed/ciciot23_9class.csv")
print("Dataset Shape:", df.shape)

X = df.drop("label", axis=1)
y = df["label"]

le = LabelEncoder()
y = le.fit_transform(y)
print("\nClass Mapping:")

for i, cls in enumerate(le.classes_):
    print(f"{cls} -> {i}")
# Save label encoder
with open("data/processed/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# TRAIN / TEMP SPLIT :- 70% TRAIN , 30% TEMP
X_train, X_temp, y_train, y_temp = train_test_split(X,y,test_size=0.30,random_state=42,stratify=y)

# TEMP -> VALIDATION + TEST:-  15% VAL , 15% TEST
X_val, X_test, y_val, y_test = train_test_split(X_temp,y_temp,test_size=0.50,random_state=42,stratify=y_temp)

# SHAPES
print("\nTrain:", X_train.shape, y_train.shape)
print("Validation:", X_val.shape, y_val.shape)
print("Test:", X_test.shape, y_test.shape)

# SAVE
X_train.to_csv("data/processed/X_train.csv", index=False)
pd.Series(y_train).to_csv("data/processed/y_train.csv", index=False)

X_val.to_csv("data/processed/X_val.csv", index=False)
pd.Series(y_val).to_csv("data/processed/y_val.csv", index=False)

X_test.to_csv("data/processed/X_test.csv", index=False)
pd.Series(y_test).to_csv("data/processed/y_test.csv", index=False)

print("\nFiles Saved Successfully")