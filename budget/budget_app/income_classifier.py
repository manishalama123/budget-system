import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Load income CSV
df = pd.read_csv('budget_app/income_classification.csv')  # adjust path if needed

# Create model pipeline
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train and save
def train_model():
    model.fit(df['description'], df['category'])
    joblib.dump(model, 'income_classifier_model.pkl')

# Uncomment this line once to train and save the model
# train_model()

# Load trained model
model = joblib.load('income_classifier_model.pkl')

# Predict function
def predict_category(text):
    return model.predict([text])[0]
