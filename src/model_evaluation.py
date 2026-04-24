# src/model_evaluation.py

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    ConfusionMatrixDisplay
)

print("🔹 Day 5: Model Evaluation Started")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/dataset_cleaned.csv")
MODELS_DIR = os.path.join(BASE_DIR, "../models")
RESULTS_DIR = os.path.join(BASE_DIR, "../results")

os.makedirs(RESULTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Load model & vectorizer
model = joblib.load(os.path.join(MODELS_DIR, "classifier_model.pkl"))
vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))

X_test_tfidf = vectorizer.transform(X_test)

# Predictions
y_pred = model.predict(X_test_tfidf)

# Metrics
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Save metrics
with open(os.path.join(RESULTS_DIR, "evaluation_metrics.txt"), "w") as f:
    f.write(f"Accuracy: {acc:.4f}\n")
    f.write(f"Precision: {prec:.4f}\n")
    f.write(f"Recall: {rec:.4f}\n")
    f.write(f"F1-score: {f1:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=["Safe", "Malicious"])
disp.plot()
plt.title("Confusion Matrix – Prompt Injection Detection")
plt.savefig(os.path.join(RESULTS_DIR, "confusion_matrix.png"))
plt.close()

print("✅ Day 5 Completed Successfully")
