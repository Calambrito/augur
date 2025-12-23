import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score

rf_model = joblib.load("rf_model.pkl")

X_test = pd.read_csv("X_test_rf.csv")
y_test = pd.read_csv("y_test_rf.csv")

y_pred = rf_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Random Forest Test Results:")
print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
