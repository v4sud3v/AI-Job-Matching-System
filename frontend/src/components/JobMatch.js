import React, { useState, useRef, useEffect } from 'react';
import '../styles/JobMatch.css';

function Ai() {
  return (
    <div className="button-shaped-box" style={{ border: '0.5px solid black' }}>
      AI-Powered
    </div>
  );
}

function JobMatch() {
  const [bgColor, setBgColor] = useState('#111111');
  const [isFieldsVisible, setIsFieldsVisible] = useState(false);
  const [formData, setFormData] = useState({
    skills: '',
    qualifications: '',
    minSalary: '',
    maxSalary: '',
    minExperience: '',
    maxExperience: '',
    preference: ''
  });
  const [resultMessage, setResultMessage] = useState(''); // State to store result message
  const fieldsRef = useRef(null);

  const handleMouseMove = (e) => {
    const { currentTarget, clientX, clientY } = e;
    const { left, top, width, height } = currentTarget.getBoundingClientRect();
    const x = ((clientX - left) / width) * 100;
    const y = ((clientY - top) / height) * 100;
    setBgColor(`radial-gradient(circle at ${x}% ${y}%, #4c4e50, #111111)`);
  };

  const handleButtonClick = () => {
    setIsFieldsVisible(true);
    setResultMessage(''); // Clear the result box when "Find Your Match" is clicked
  };

  const handleOutsideClick = (event) => {
    if (fieldsRef.current && !fieldsRef.current.contains(event.target)) {
      setIsFieldsVisible(false); // Hide the input fields when clicking outside
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const result = await response.json();

      // Format the result message
      const formattedMessage = Object.entries(result)
        .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
        .join('<br/>');

      setResultMessage(formattedMessage); // Update result message
      setIsFieldsVisible(false); // Hide the form after submit
      setFormData({
        skills: '',
        qualifications: '',
        minSalary: '',
        maxSalary: '',
        minExperience: '',
        maxExperience: '',
        preference: ''
      });
    } catch (error) {
      console.error('Error:', error);
      setResultMessage('An error occurred while predicting the job match.'); // Update on error
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleOutsideClick);
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, []);

  return (
    <section className="job-match">
      <h1 style={{ fontSize: '6em', fontWeight: '100' }}>
        <div className="ai-powered-wrap">
          Your <span style={{ marginRight: '10px' }}></span><span><Ai /></span>
        </div>
        <br />Job Match
      </h1>
      <br />
      <div 
        className={`job-button ${isFieldsVisible ? 'form-visible' : ''}`}
        style={{ background: bgColor }}
        onMouseMove={handleMouseMove}
        onClick={!isFieldsVisible ? handleButtonClick : null}
        ref={fieldsRef}
      >
        {isFieldsVisible ? (
          <div className="skill-form">
            <h2>Select Your Job Preferences</h2>
            <label>
              Skills
              <input
                type="text"
                name="skills"
                value={formData.skills}
                onChange={handleInputChange}
                placeholder="e.g., public speaking, social media"
              />
            </label>
            <label>
              Qualifications
              <input
                type="text"
                name="qualifications"
                value={formData.qualifications}
                onChange={handleInputChange}
                placeholder="e.g., BCA"
              />
            </label>
            <label>
              Minimum Salary (K)
              <input
                type="number"
                name="minSalary"
                value={formData.minSalary}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Maximum Salary (K)
              <input
                type="number"
                name="maxSalary"
                value={formData.maxSalary}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Minimum Experience (years)
              <input
                type="number"
                name="minExperience"
                value={formData.minExperience}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Maximum Experience (years)
              <input
                type="number"
                name="maxExperience"
                value={formData.maxExperience}
                onChange={handleInputChange}
              />
            </label>
            <label>
              Preference
              <select
                name="preference"
                value={formData.preference}
                onChange={handleInputChange}
              >
                <option value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Any">Any</option>
              </select>
            </label>
            <button onClick={handleSubmit}>Submit</button>
          </div>
        ) : (
          'Find Your Match'
        )}
      </div>

      {/* Display the result box if there is a result message */}
      {resultMessage && (
        <div className="result-box" dangerouslySetInnerHTML={{ __html: resultMessage }} />
      )}
    </section>
  );
}

export default JobMatch;
