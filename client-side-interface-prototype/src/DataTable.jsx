import React from 'react';
import './Visualization.css'; // Behalte die Stile bei

const DataTable = ({ data, title, isVisible, toggleVisibility }) => (
  <div>
    <h2>
      {title} 
      <button onClick={toggleVisibility}>
        {isVisible ? 'Hide' : 'Show'}
      </button>
    </h2>
    {isVisible && (
      <table className="styled-table">
        <thead>
          <tr>
            {Object.keys(data[0]).map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </div>
);

export default DataTable;
