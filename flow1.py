import pandas as pd

area_data = {
    "Gulshan": {"population": 253050, "price_per_sqft": 27000},
    "Banani": {"population": 24718, "price_per_sqft": 22000},
    "Baridhara": {"population": 45000, "price_per_sqft": 26000},
    "Bashundhara": {"population": 274200, "price_per_sqft": 11000},
    "Uttara": {"population": 1500000, "price_per_sqft": 10000},
    "Mirpur": {"population": 550000, "price_per_sqft": 7500},
    "Dhanmondi": {"population": 101937, "price_per_sqft": 18000},
    "Mohammadpur": {"population": 355843, "price_per_sqft": 7000},
    "Badda": {"population": 536621, "price_per_sqft": 8500},
    "Rampura": {"population": 224079, "price_per_sqft": 9000},
    "Khilgaon": {"population": 380740, "price_per_sqft": 8000},
    "Malibagh": {"population": 111771, "price_per_sqft": 8500},
    "Old Dhaka": {"population": 400000, "price_per_sqft": 6000},
    "Motijheel": {"population": 210006, "price_per_sqft": 10000},
    "Tejgaon": {"population": 148000, "price_per_sqft": 9500},
    "Farmgate": {"population": 80000, "price_per_sqft": 10500},
    "Niketan": {"population": 35000, "price_per_sqft": 20000}
}

df = pd.read_csv("flow0.csv")

df["competitor_count"] = (
    df.groupby(["location", "cuisine"])["name"]
      .transform("count") - 1
)

df["area_population"] = df["location"].map(lambda x: area_data[x]["population"])
df["house_price_per_sqft"] = df["location"].map(lambda x: area_data[x]["price_per_sqft"])

df = df.drop("location", axis=1)

df.to_csv("flow1.csv", index=False)
