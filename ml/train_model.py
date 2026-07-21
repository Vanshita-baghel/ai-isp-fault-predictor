from utils.data_loader import load_data

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

df= load_data()
print(f"head:\n {df.head}")

features = [
    "cpu_utilization",
    "memory_utilization",
    "bandwidth_utilization",
    "latency_ms",
    "ber",
    "packet_loss",
    "crc_errors",
    "input_errors",
    "output_errors",
]

X= df[features]
y= df["failure"]

print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.2, random_state=42 ,stratify=y)

print(X_train.shape)
print(X_test.shape)

scaler= StandardScaler()

X_train_scaled= scaler.fit_transform(X_train)
X_test_scaled= scaler.transform(X_test)

#create model
model= LogisticRegression(max_iter=1000, random_state=42)

model.fit(X_train_scaled, y_train)

#Predict
y_pred= model.predict(X_test_scaled)

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

joblib.dump(
    model,
    "models/logistic_regression.pkl",
)

joblib.dump(
    scaler,
    "models/scaler.pkl",
)