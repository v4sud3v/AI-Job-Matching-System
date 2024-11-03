import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.data import find
import pickle
import os

def download_nltk_resources():
    """Download required NLTK resources if not already present"""
    try:
        find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        find('tokenizers/punkt_tab')

    except LookupError:
        nltk.download('punkt_tab')
    
    try:
        find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

def extract_keywords(text):
    """Extract keywords from text after removing stopwords"""
    tokens = word_tokenize(str(text).lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(keywords)

def str_to_tuple(range_str):
    """Convert string ranges to tuples"""
    try:
        if pd.isna(range_str):
            return None
        if isinstance(range_str, str):
            start, end = map(int, range_str.split(','))
            return (start, end)
        return range_str
    except Exception as e:
        print(f"Error converting {range_str}: {e}")
        return None

def train_job_matcher(data_path='processed_job_data.csv', model_path='job_matcher_model.pkl'):
    """Train and save the job matching model"""
    print("Starting model training process...")
    
    # Download required NLTK resources
    download_nltk_resources()
    
    # Load and preprocess data
    print("Loading and preprocessing data...")
    data = pd.read_csv(data_path)
    data = data.dropna()
    
    # Create a working copy
    df = data.copy()
    
    # Convert ranges to tuples
    print("Converting salary and experience ranges...")
    df['SalaryRange'] = df['SalaryRange'].apply(str_to_tuple)
    df['ExperienceRange'] = df['ExperienceRange'].apply(str_to_tuple)
    
    # Process skills
    print("Processing skills...")
    if 'processed_skills' not in df.columns:
        df['processed_skills'] = df['skills'].apply(extract_keywords)
    
    # Create and fit TF-IDF vectorizer
    print("Creating TF-IDF vectors...")
    tfidf = TfidfVectorizer()
    tfidf.fit(df['processed_skills'])
    
    # Save the model
    print("Saving model...")
    model_data = {
        'tfidf': tfidf,
        'df': df,
        'skills_column': 'processed_skills'
    }
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    # Set paths
    DATA_PATH = 'processed_job_data.csv'  # Update this path as needed
    MODEL_PATH = 'job_matcher_model.pkl'
    
    # Check if model already exists
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}")
        user_input = input("Do you want to retrain the model? (yes/no): ")
        if user_input.lower() != 'yes':
            print("Training cancelled. Using existing model.")
            exit()
    
    # Train model
    train_job_matcher(DATA_PATH, MODEL_PATH)