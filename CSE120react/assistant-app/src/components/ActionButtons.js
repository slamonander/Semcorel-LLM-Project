// src/components/ActionButtons.js
import React from "react";
import { useNavigate } from "react-router-dom";
import "./ActionButtons.css";

const ActionButtons = () => {
  const navigate = useNavigate();

  const handleTypeClick = () => {
    navigate("/chat");
  };
  const handleTypeSpeach = () => {
    navigate("/speech-text");
  };
  return (
    <div className="action-buttons">
      <button className="button" onClick={handleTypeClick}>
        <span role="img" aria-label="type">
          📝
        </span>
        Type
      </button>
      <button className="button" onClick={handleTypeSpeach}>
        <span role="img" aria-label="speak">
          🎤
        </span>
        Speak
      </button>
    </div>
  );
};

export default ActionButtons;
