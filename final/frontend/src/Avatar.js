// src/components/Avatar.js
import React from "react";
import "./Avatar.css";

const Avatar = () => {
  return (
    <div className="avatar">
      <div className="face-icon">
        <div className="avatar-eye left-avatar"></div>
        <div className="avatar-eye right-avatar"></div>      
      </div>
    </div>
  );
};
export default Avatar;
// <div className="mouth"></div> {/* Adding the mouth for smile */} 