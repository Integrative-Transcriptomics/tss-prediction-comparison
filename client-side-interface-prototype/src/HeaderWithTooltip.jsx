import React from 'react';
import './Visualization.css'; // Behalte die Stile bei

const HeaderWithTooltip = ({ title, tooltipText }) => (
  <div className="header-with-tooltip">
    <h2 style={{ display: 'inline-block', marginRight: '10px' }}>
      {title}
    </h2>
    <div className="tooltip">
      <span className="tooltip-icon">?</span>
      <span className="tooltip-text">
        {tooltipText}
      </span>
    </div>
  </div>
);

export default HeaderWithTooltip;
