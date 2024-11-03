import pickle
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

def extract_keywords(text):
    """Extract keywords from text after removing stopwords"""
    tokens = word_tokenize(str(text).lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(keywords)

def format_range_output(range_tuple):
    """Format range tuple for display"""
    if isinstance(range_tuple, tuple):
        return range_tuple
    return None

class JobPredictor:
    def __init__(self, model_path='job_matcher_model.pkl'):
        """Initialize the job predictor with a trained model"""
        self.model_path = model_path
        self.tfidf = None
        self.df = None
        self.skills_column = None
        

        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('stopwords')
        # Load the model
        self.load_model()
    
    def load_model(self):
        """Load the trained model from file"""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.tfidf = model_data['tfidf']
            self.df = model_data['df']
            self.skills_column = model_data['skills_column']
            print("Model loaded successfully")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def predict(self, input_skills, qualifications, salary_range, experience_range, preference):
        """Find the best job match using the loaded model"""
        try:
            # Filter based on qualifications and preference
            filtered_df = self.df[(
                self.df['Qualifications'] == qualifications) &
                ((self.df['Preference'] == preference) | (self.df['Preference'] == 'Both'))
            ]
            
            # Filter based on salary range
            filtered_df = filtered_df[
                filtered_df['SalaryRange'].apply(
                    lambda x: x is not None and salary_range[0] <= x[0] and x[1] <= salary_range[1]
                )
            ]
            
            # Filter based on experience range
            filtered_df = filtered_df[
                filtered_df['ExperienceRange'].apply(
                    lambda x: x is not None and experience_range[0] <= x[0] and x[1] <= experience_range[1]
                )
            ]
            
            if filtered_df.empty:
                return "No matching job found based on the given criteria."
            
            # Calculate TF-IDF similarity
            filtered_tfidf = self.tfidf.transform(filtered_df[self.skills_column])
            input_vector = self.tfidf.transform([extract_keywords(input_skills)])
            similarities = cosine_similarity(input_vector, filtered_tfidf)
            best_match_index = similarities.argmax()
            
            return filtered_df.iloc[best_match_index]
        
        except Exception as e:
            return f"An error occurred while finding matches: {str(e)}"

# Example usage removed, as it's not needed in a Flask context
