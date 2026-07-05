from langraph.workflow import app
from langraph.state import create_state
import pandas as pd

X = pd.read_csv("data/processed/X_val.csv")

sample = X.iloc[[635]]

state = create_state()
state["traffic"] = sample
result = app.invoke(state)

print(result)
