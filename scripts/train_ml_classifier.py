import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Load processed keystroke vectors
df = pd.read_csv("keystroke_ml/processed/keystroke_vectors.csv")

# Separate features and labels
X = df.drop(columns = ["label"])
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, test_size = 0.2, random_state = 42)

# Train a Random Forest classifer
clf = RandomForestClassifier(n_estimators = 100, class_weight = "balanced", random_state = 42)
clf.fit(X_train, y_train)

#Evaluate
y_pred = clf.predict(X_test)
print("\n=== Classification Report ====")
print(classification_report(y_test, y_pred, digits = 4))

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok = True)
joblib.dump(clf, "models/keystroke_rf_model.joblib")