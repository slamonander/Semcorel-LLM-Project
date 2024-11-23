// src/components/Greeting.js
import React from "react";
import "./Greeting.css";

const Greeting = ({ name }) => {
  return (
    <div className="greeting-container">
      <header className = "logo-header">
        <h1>COCO</h1>
      </header>
      <div className="speech-bubble">
        <h1>Hello<span id="exclamation-mark">!</span></h1>
        <p>How can I help you today?</p>
      </div>
    </div>
  ); 
};
export default Greeting;

// Adding Monserrat font from Google
const link = document.createElement('link');
link.href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap";
link.rel="stylesheet";
document.head.appendChild(link);
