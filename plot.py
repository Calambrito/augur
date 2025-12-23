import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np

model = joblib.load("model.pkl")

X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

scaler = StandardScaler()
scaler.fit(X_train)
X_test_scaled = scaler.transform(X_test)

y_pred = model.predict(X_test_scaled)

idx = np.arange(len(y_test))

plt.figure()
plt.scatter(idx, y_test, color="red", alpha=0.6, label="Actual Success Score")
plt.scatter(idx, y_pred, color="green", alpha=0.6, label="Predicted Success Score")

plt.xlabel("Test Sample Index")
plt.ylabel("Success Score")
plt.title("Actual vs Predicted Success Scores (Test Set)")
plt.legend()
plt.tight_layout()
plt.show()
