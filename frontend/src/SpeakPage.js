// src/SpeakPage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

function SpeakPage() {
  const navigate = useNavigate();

  return (
    <div className="container">
      {/* Back button moved to the top right */}
      <button className="btn back-button" onClick={() => navigate('/')}>
        Back to Home
      </button>

      <div className="button-container">
        {/* Speak Question button */}
        <button className="btn" onClick={() => {/* Add functionality for Speak Question */}}>
          Speak Question
        </button>
      </div>
    </div>
  );
}

export default SpeakPage;
