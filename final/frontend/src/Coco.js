// src/CoCo.js
import React from 'react';
import './Coco.css';
import './CocoSmall.css'; // Import alternate style

const Coco = ({ className }) => {
  return (
    <div className="coco-container">
        <div className={`coco ${className}`}>
        <div className="eye left-eye"></div>
        <div className="eye right-eye"></div>
        </div>
    </div>
  );
};

export default Coco;
