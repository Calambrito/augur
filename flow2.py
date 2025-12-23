import pandas as pd
import numpy as np
import re

df = pd.read_csv("flow1.csv")

def normalize_and_encode_price(price):
    if pd.isna(price) or price == "":
        return np.nan
    price = str(price).strip()
    if price == "$":
        return 1
    if price == "$$":
        return 2
    if price == "$$$":
        return 3
    numbers = re.findall(r"\d+", price)
    if len(numbers) == 2:
        low, high = map(int, numbers)
        mid = (low + high) / 2
        if mid < 250:
            return 1
        elif mid <= 750:
            return 2
        else:
            return 3
    return np.nan

df["price"] = df["price"].apply(normalize_and_encode_price)

df["price"] = df["price"].fillna(df["price"].median())

df.to_csv("flow2.csv", index=False)
