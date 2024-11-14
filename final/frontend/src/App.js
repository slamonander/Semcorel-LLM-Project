// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Greeting from "./Greeting";
import SpeakPage from './SpeakPage';
import TypePage from './TypePage';
import Coco from './Coco';
import Test from './Test';
import './index.css';
import './Test.css';
import './Coco.css';

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
          <Coco className="coco" />
        )}

      <Routes>
        <Route path="/" element={
          <div className="button-container">
            <button className="btn" onClick={() => navigate('/speak')}>
              <span className="material-icons icon">mic</span><br />Speak
            </button>
            <button className="btn-error" onClick={() => navigate('/type')}>
            </button>
            <button className="btn" onClick={() => navigate('/test')}>
              <span className="material-icons icon">keyboard</span><br />Type
            </button>
          </div>
        } />
        <Route path="/speak" element={<SpeakPage />} />
        <Route path="/type" element={<TypePage />} />
        <Route path="/test" element={<Test/>}/>
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
