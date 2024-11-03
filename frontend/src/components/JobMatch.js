import React, { useState, useRef, useEffect } from 'react';
import '../styles/JobMatch.css';

function Ai() {
  return (
    <div className="button-shaped-box" style={{ border: '1px solid black' }}>
      AI-Powered
    </div>
  );
}

function JobMatch() {
  const [bgColor, setBgColor] = useState('#111111');
  const [isFormVisible, setIsFormVisible] = useState(false);
  const formRef = useRef(null); // Ref for the form to handle outside clicks

  const handleMouseMove = (e) => {
    const { currentTarget, clientX, clientY } = e;
    const { left, top, width, height } = currentTarget.getBoundingClientRect();

    const x = ((clientX - left) / width) * 100;
    const y = ((clientY - top) / height) * 100;

    setBgColor(`radial-gradient(circle at ${x}% ${y}%, #4c4e50, #111111)`);
  };

  const handleButtonClick = () => {
    setIsFormVisible(true);
  };

  const handleOutsideClick = (event) => {
    if (formRef.current && !formRef.current.contains(event.target)) {
      setIsFormVisible(false); // Hide the form if clicking outside of it
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleOutsideClick);
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    const selectedSkills = Array.from(event.target.skills)
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value);

    console.log('Selected Skills:', selectedSkills);
    setIsFormVisible(false); // Optionally close the form after submission
  };

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
        className={`job-button ${isFormVisible ? 'form-visible' : ''}`}
        style={{ background: bgColor }}
        onMouseMove={handleMouseMove}
        onClick={isFormVisible ? null : handleButtonClick}
        ref={formRef} // Reference for outside click detection
      >
        {isFormVisible ? (
          <form onSubmit={handleSubmit} className="skill-form">
            <h2>Select Your Skill Sets</h2>
            <label>
              <input type="checkbox" name="skills" value="JavaScript" />
              JavaScript
            </label>
            <label>
              <input type="checkbox" name="skills" value="Python" />
              Python
            </label>
            <label>
              <input type="checkbox" name="skills" value="Java" />
              Java
            </label>
            <button type="submit">Submit</button>
          </form>
        ) : (
          'Find Your Match'
        )}
      </div>
    </section>
  );
}

export default JobMatch;
