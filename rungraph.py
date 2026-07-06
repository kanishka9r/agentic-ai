from langraph.workflow import app
from langraph.state import create_state
import pandas as pd
from respons.action import reset_system_state

X = pd.read_csv("data/processed/X_val.csv")

sample = X.iloc[[635]]

reset_system_state()
state = create_state()
state["traffic"] = sample
result = app.invoke(state)

print(result)
