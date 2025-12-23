import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

df = pd.read_csv("flow4.csv")

X = df.drop(columns=["success_score"])
y = df["success_score"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.2, random_state=42
)

X_temp.to_csv("X_temp_rf.csv", index=False)
y_temp.to_csv("y_temp_rf.csv", index=False)

rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

joblib.dump(rf_model, "rf_model.pkl")

print("Random Forest build complete.")
print(f"Training samples: {len(X_train)}")
