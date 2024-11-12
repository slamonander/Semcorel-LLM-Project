// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import SpeakPage from './SpeakPage';
import TypePage from './TypePage';
import Coco from './Coco';
import './index.css';

function App() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="container">
      {/* Conditionally render Header only on the home page */}
      {location.pathname === '/' && (
        <header className="header-bubble">
          <h1>Hello</h1>
          <center><p className="tagline">How can I help you today?</p></center>
        </header>
      )}

      {/* Add Circle component here */}
      {location.pathname === '/' && (
          <Coco />
        )}

      <Routes>
        <Route path="/" element={
          <div className="button-container">
            <button className="btn" onClick={() => navigate('/speak')}>
              <span className="material-icons icon">mic</span><br />Speak
            </button>
            <button className="btn" onClick={() => navigate('/type')}>
              <span className="material-icons icon">keyboard</span><br />Type
            </button>
          </div>
        } />
        <Route path="/speak" element={<SpeakPage />} />
        <Route path="/type" element={<TypePage />} />
      </Routes>
    </div>
  );
}


const AppWrapper = () => (
  <Router>
    <App />
  </Router>
);

export default AppWrapper;
