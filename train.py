import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import os

print("Loading dataset...")
df = pd.read_csv("data/spam.csv", encoding="latin-1")[["v1","v2"]]
df.columns = ["label","message"]
df["label"] = df["label"].map({"ham":0, "spam":1})

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

df["clean"] = df["message"].apply(clean_text)
df["length"] = df["clean"].apply(len)

X = df["clean"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=1
)

vectorizer = CountVectorizer(max_features=4000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
print(f"Accuracy: {acc*100:.2f}%")

os.makedirs("models", exist_ok=True)
pickle.dump(model, open("models/classifier.pkl","wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl","wb"))

print("Model saved successfully!")