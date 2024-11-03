from flask import Flask, request, jsonify, send_from_directory
from predictor import JobPredictor
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")

# Initialize the JobPredictor
predictor = JobPredictor(model_path='job_matcher_model.pkl')

# Route to serve the React frontend from the root
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Optional: catch-all route to serve index.html for any unmatched routes (for React Router compatibility)
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

# API route for predicting job match
@app.route('/predict', methods=['POST'])
def predict_job():
    data = request.json

    # Extract data from request
    input_skills = data.get('skills', '')
    qualifications = data.get('qualifications', '')
    # Convert salary and experience fields to integers, with a default value of 0 if not provided
    min_salary = int(data.get('minSalary', 0) or 0)
    max_salary = int(data.get('maxSalary', 0) or 200)
    salary_range = (min_salary, max_salary)

    min_exp = int(data.get('minExperience', 0) or 0)
    max_exp = int(data.get('maxExperience', 0) or 25)
    experience_range = (min_exp, max_exp)
    preference = data.get('preference', 'Any')

    # Predict job match
    result = predictor.predict(
        input_skills=input_skills,
        qualifications=qualifications,
        salary_range=salary_range,
        experience_range=experience_range,
        preference=preference
    )

    # Format response
    if isinstance(result, str):
        return jsonify({'message': result}), 404
    else:
        job_details = {
            'Job Title': result['Job Title'],
            'Role': result['Role'],
            'Company': result['Company'],
            'Salary Range': f"${result['SalaryRange'][0]}K-${result['SalaryRange'][1]}K",
            'Experience Range': f"{result['ExperienceRange'][0]}-{result['ExperienceRange'][1]} years",
            'Skills': result['skills']
        }
        return jsonify(job_details)

if __name__ == "__main__":
    app.run(debug=True)
