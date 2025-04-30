// src/components/Greeting.js
import React from "react";
import "./Greeting.css";

const Greeting = ({ name }) => {
  return (
    <div className="greeting-container">
      <div className="speech-bubble">
        <h1>Hello! </h1>
        <p>How can I help you today?</p>
      </div>
    </div>
  );
};
export default Greeting;
