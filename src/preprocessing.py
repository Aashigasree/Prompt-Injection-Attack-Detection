import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split



df=pd.read_csv("data/prompt_dataset.csv")
df.drop_duplicates(subset="prompt_text", inplace=True)
df["prompt_text"]=df["prompt_text"].str.strip()
df["prompt_text"]=df["prompt_text"].str.replace(r"\s+"," ",regex=True)


def remove(text):
    return re.sub(r"[^a-zA-Z0-9\s]","", str(text))
df["prompt_text"]=df["prompt_text"].apply(remove)

df["prompt_text"]=df["prompt_text"].str.lower()

def token(text):
    return text.split()
df["tokens"]=df["prompt_text"].apply(token)

def stop(tokens):
    return [w for w in tokens if w not in ENGLISH_STOP_WORDS]

df["tokens"]=df["tokens"].apply(stop)

def join(tokens):
    return " ".join(tokens)
df["clean_text"]=df["tokens"].apply(join)


X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


df[["clean_text", "label"]].to_csv(
    "data/dataset_cleaned.csv", index=False
)

print("Day 2 DONE ✅ Cleaned dataset saved.")
