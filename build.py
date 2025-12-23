import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import joblib


df = pd.read_csv("flow4.csv")
TARGET = "success_score"

X = df.drop(columns=[TARGET])
y = df[TARGET]


X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.20, random_state=42
)


pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

pipeline.fit(X_train, y_train)
joblib.dump(pipeline, "model.pkl")


X_temp.to_csv("X_temp.csv", index=False)
y_temp.to_csv("y_temp.csv", index=False)

print("Build complete.")
print(f"Training samples: {len(X_train)}")
