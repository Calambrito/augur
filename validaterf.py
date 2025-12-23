import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

rf_model = joblib.load("rf_model.pkl")

X_temp = pd.read_csv("X_temp_rf.csv")
y_temp = pd.read_csv("y_temp_rf.csv").values.ravel()

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)

X_test.to_csv("X_test_rf.csv", index=False)
y_test_df = pd.DataFrame(y_test, columns=["success_score"])
y_test_df.to_csv("y_test_rf.csv", index=False)

y_val_pred = rf_model.predict(X_val)

mse = mean_squared_error(y_val, y_val_pred)
r2 = r2_score(y_val, y_val_pred)

print("Random Forest Validation Results:")
print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
