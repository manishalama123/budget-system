# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB

# # Step 1: Sample data for training (same data as before)
# train_inputs = [
#     "coffee with friends",   
#     "cab to airport",     
#     "t-shirt shopping",
#     "paid rent",
#     "paid electricity bill", 
#     "flight ticket booking", 
#     "movie night",          # New entry
#     "grocery shopping"      # New entry
# ]

# train_labels = [
#     "food", 
#     "transportation", 
#     "shopping", 
#     "bills",
#     "bills", 
#     "transportation", 
#     "other",                # New label for "movie night"
#     "shopping"              # New label for "grocery shopping"
# ]


# # Step 2: Initialize the vectorizer and train the model
# vectorizer = CountVectorizer()  # Converts text into numeric form
# X_train = vectorizer.fit_transform(train_inputs)

# model = MultinomialNB()  # Naive Bayes model for text classification
# model.fit(X_train, train_labels)

# # Step 3: Define a function for predicting the category
# def predict_category(description):
#     # Transform the input description into the format the model understands
#     X_desc = vectorizer.transform([description])
    
#     # Predict the category using the trained model
#     predicted_category = model.predict(X_desc)
    
#     return predicted_category[0]  # Return the predicted category as a string
# classifier.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Load the CSV data
df = pd.read_csv('budget_app/personal_expense_classification.csv')

# Create a pipeline for text classification
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model (only do this once)
def train_model():
    # We train on the 'description' column as input and 'category' as the target
    model.fit(df['description'], df['category'])
    
    # Save the model to a file for later use
    joblib.dump(model, 'expense_classifier_model.pkl')

# Load the trained model once
model = joblib.load('expense_classifier_model.pkl')



def predict_category(text):
    predicted_category = model.predict([text])[0]
    print("Prediction from model:", predicted_category)
    return predicted_category


#  to train the model:
# train_model()

