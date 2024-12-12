// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Greeting from "./Greeting";
import SpeakPage from './SpeakPage';
// import Coco from './Coco';
import TypePage from './TypePage';
import './index.css';
import './TypePage.css';
// import './Coco.css';
import Avatar from './Avatar';

function App() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="container">
      {/* Conditionally render Header only on the home page */}
      {location.pathname === '/' && (
        <Greeting />
      )}
      {/* Add Circle component here */}
      {location.pathname === '/' && (
          <Avatar/>
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
