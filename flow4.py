import pandas as pd

df = pd.read_csv("flow3.csv")

df = df.dropna(subset=["success_score"])

df = pd.get_dummies(df, columns=["cuisine"], prefix="cuisine")

df.to_csv("flow4.csv", index=False)
