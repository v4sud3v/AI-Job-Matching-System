import pickle
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.data import find

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
        
        # Ensure NLTK resources are available
        try:
            find('tokenizers/punkt')
            find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
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
            filtered_df = self.df[
                (self.df['Qualifications'] == qualifications) &
                ((self.df['Preference'] == preference) | (self.df['Preference'] == 'Both') | (preference == 'Both'))
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

if __name__ == "__main__":
    # Example usage
    try:
        # Initialize predictor
        predictor = JobPredictor()
        
        # Get user input
        print("\nEnter job search criteria:")
        input_skills = input("Enter your skills (e.g., 'public speaking, social media'): ")
        qualifications = input("Enter your qualification (e.g., 'BCA'): ")
        
        # Get salary range
        min_salary = int(input("Enter minimum salary($/annum) in K (e.g., 50): "))
        max_salary = int(input("Enter maximum salary($/annum) in K (e.g., 100): "))
        salary_range = (min_salary, max_salary)
        
        # Get experience range
        min_exp = int(input("Enter minimum experience in years (e.g., 2): "))
        max_exp = int(input("Enter maximum experience in years (e.g., 10): "))
        experience_range = (min_exp, max_exp)
        
        preference = input("Enter preference (Male/Female): ")
        
        # Get prediction
        best_match = predictor.predict(input_skills, qualifications, salary_range, experience_range, preference)
        
        # Display results
        if isinstance(best_match, str):
            print(best_match)
        else:
            print("\nBest matching job:")
            print(f"Title: {best_match['Job Title']}")
            print(f"Role: {best_match['Role']}")
            print(f"Company: {best_match['Company']}")
            
            salary_tuple = format_range_output(best_match['SalaryRange'])
            exp_tuple = format_range_output(best_match['ExperienceRange'])
            
            if salary_tuple:
                print(f"Salary Range: ${salary_tuple[0]}K-${salary_tuple[1]}K")
            if exp_tuple:
                print(f"Experience Range: {exp_tuple[0]}-{exp_tuple[1]} years")
            
            print(f"Skills: {best_match['skills']}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")