import React from 'react';
import './Visualization.css'; // Import the CSS file for styling the header and tooltip

// The HeaderWithTooltip component renders a header with a tooltip that provides additional information.
const HeaderWithTooltip = ({ title, tooltipText }) => (
  <div className="header-with-tooltip">
    {/* The header title */}
    <h2 style={{ display: 'inline-block', marginRight: '10px' }}>
      {title}
    </h2>
    {/* Tooltip icon and text */}
    <div className="tooltip">
      <span className="tooltip-icon">?</span>
      <div className="tooltip-text">
        {tooltipText}
      </div>
    </div>
  </div>
);

export default HeaderWithTooltip;
