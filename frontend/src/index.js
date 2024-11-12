// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import AppWrapper from './App';  // Import AppWrapper
import './index.css';  // Import global styles (if you have any)

// This line will render the AppWrapper component inside the root div in index.html
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AppWrapper />
  </React.StrictMode>
);
