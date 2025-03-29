import joblib
import nltk
import os
import re

# Ensure NLTK resources are available
nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer

# Define category-related keywords
category_keywords = {
    "Food": ["pizza", "restaurant", "coffee", "burger", "meal", "kfc", "mcdonalds", "mess", "canteen"],
    "Transport": ["uber", "fuel", "bus", "metro", "shell", "train"],
    "Entertainment": ["netflix", "spotify", "movies", "concert", "game"],
    "Groceries": ["supermarket", "grocery", "walmart", "bigbasket", "blinkit"],
    "Shopping": ["amazon", "flipkart", "ebay", "store", "nike", "zudio"],
    "Income": ["salary", "credited", "income"],
    "Housing": ["rent", "mortgage", "house"],
}

# Ensure the model exists
model_filename = os.path.join("./", "expense_classifier.pkl")
if not os.path.exists(model_filename):
    print("⚠️ Model file not found. Train the model first using train_model.py.")
    exit()

# Load the trained model
model = joblib.load(model_filename)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def categorize_transaction(description):
    description = description.lower()
    
    # Check for direct keyword match
    for category, keywords in category_keywords.items():
        if any(word in description for word in keywords):
            return category

    # Use ML model for prediction
    predicted_category = model.predict([description])[0]
    
    return predicted_category

# Example transactions
transactions = [
    "Dominos pizza bill",
    "Monthly metro pass",
    "Cinema tickets",
    "Amazon purchase",
    "John Doe payment",
]

print("\n🟢 Transaction Categorization:")
for transaction in transactions:
    category = categorize_transaction(transaction)
    print(f"📌 Transaction: '{transaction}' | Predicted Category: {category}")
