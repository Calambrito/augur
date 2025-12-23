import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

model = joblib.load("model.pkl")

X_temp = pd.read_csv("X_temp.csv")
y_temp = pd.read_csv("y_temp.csv").squeeze()

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42
)

y_pred = model.predict(X_val)

mse = mean_squared_error(y_val, y_pred)
r2 = r2_score(y_val, y_pred)

X_test.to_csv("X_test.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("Validation results:")
print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
