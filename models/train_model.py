import pandas as pd
import nltk
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Ensure required NLTK resources are available
nltk.download("stopwords")
from nltk.corpus import stopwords

# Check if stopwords exist
try:
    stop_words = stopwords.words("english")
except:
    stop_words = None

# Sample dataset (extend it with real data)
data = {
    "description": [
        "Pizza Hut payment",
        "Grocery store bill",
        "Netflix subscription",
        "Fuel at Shell",
        "Amazon shopping",
        "Salary credited",
        "Starbucks coffee",
        "Rent payment",
    ],
    "category": [
        "Food",
        "Groceries",
        "Entertainment",
        "Transport",
        "Shopping",
        "Income",
        "Food",
        "Housing",
    ],
}

df = pd.DataFrame(data)

# Ensure the models directory exists
os.makedirs("models", exist_ok=True)

# Text processing and model training
vectorizer = TfidfVectorizer(stop_words=stop_words)
model = Pipeline([("tfidf", vectorizer), ("clf", MultinomialNB())])

model.fit(df["description"], df["category"])

# Save model in models/ folder
model_filename = os.path.join("./", "expense_classifier.pkl")
joblib.dump(model, model_filename)

print(f"✅ Model trained and saved successfully at {model_filename}!")
