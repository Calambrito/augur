import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import joblib

model = joblib.load("model.pkl")

X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Test results:")
print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
