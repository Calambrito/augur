import pandas as pd
import numpy as np

df = pd.read_csv("flow2.csv")

C = 3.0
m = df["reviews"].median()

base_score = (df["reviews"]/(df["reviews"] + m)) * df["rating"] + (m/(df["reviews"] + m)) * C

competitor_factor = 1 + (df["competitor_count"] / 10)

df["success_score"] = base_score * competitor_factor

df = df.drop(columns=["competitor_count", "name", "rating", "reviews"], errors="ignore")
df.to_csv("flow3.csv", index=False)