import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

df = pd.read_csv("data/dataset_cleaned.csv")


if "clean_text" not in df.columns or "label" not in df.columns:
    raise ValueError("Dataset must have mentioned columns")

x= df["clean_text"]
y= df["label"]
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)
 


tfidf = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=5000,
    stop_words="english"
)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


with open("models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

with open("models/X_train_tfidf.pkl", "wb") as f:
    pickle.dump(X_train_tfidf, f)

with open("models/X_test_tfidf.pkl", "wb") as f:
    pickle.dump(X_test_tfidf, f)

print("Day 3 completed ✅")
