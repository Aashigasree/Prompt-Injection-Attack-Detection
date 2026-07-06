
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("🔹 Day 4: Model Training Started")

# --------------------------------------------------
# 1. Path handling (SAFE & PROFESSIONAL)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "../data/dataset_cleaned.csv")
MODELS_DIR = os.path.join(BASE_DIR, "../models")

os.makedirs(MODELS_DIR, exist_ok=True)

# --------------------------------------------------
# 2. Load cleaned dataset
# --------------------------------------------------
df = pd.read_csv(DATA_PATH)

# Columns from Day 2
X = df["clean_text"]
y = df["label"]

# --------------------------------------------------
# 3. Train-test split (same as Day 3)
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------------------
# 4. Load TF-IDF vectorizer from Day 3
# --------------------------------------------------
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
tfidf = joblib.load(VECTORIZER_PATH)

X_train_tfidf = tfidf.transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# --------------------------------------------------
# 5. Logistic Regression
# --------------------------------------------------
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_tfidf, y_train)

lr_preds = lr_model.predict(X_test_tfidf)

lr_accuracy = accuracy_score(y_test, lr_preds)
lr_precision = precision_score(y_test, lr_preds)
lr_recall = recall_score(y_test, lr_preds)
lr_f1 = f1_score(y_test, lr_preds)

print("\n🔹 Logistic Regression Results")
print(f"Accuracy  : {lr_accuracy:.4f}")
print(f"Precision : {lr_precision:.4f}")
print(f"Recall    : {lr_recall:.4f}")
print(f"F1-score  : {lr_f1:.4f}")

# --------------------------------------------------
# 6. Random Forest
# --------------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X_train_tfidf, y_train)

rf_preds = rf_model.predict(X_test_tfidf)

rf_accuracy = accuracy_score(y_test, rf_preds)
rf_precision = precision_score(y_test, rf_preds)
rf_recall = recall_score(y_test, rf_preds)
rf_f1 = f1_score(y_test, rf_preds)

print("\n🔹 Random Forest Results")
print(f"Accuracy  : {rf_accuracy:.4f}")
print(f"Precision : {rf_precision:.4f}")
print(f"Recall    : {rf_recall:.4f}")
print(f"F1-score  : {rf_f1:.4f}")

# --------------------------------------------------
# 7. Select & save best model (based on F1-score)
# --------------------------------------------------
if lr_f1 >= rf_f1:
    best_model = lr_model
    best_model_name = "Logistic Regression"
else:
    best_model = rf_model
    best_model_name = "Random Forest"

MODEL_PATH = os.path.join(MODELS_DIR, "classifier_model.pkl")
joblib.dump(best_model, MODEL_PATH)

print("\n✅ Best Model Selected:", best_model_name)
print("📁 Model saved at:", MODEL_PATH)
print("🎯 Day 4 COMPLETED SUCCESSFULLY")
