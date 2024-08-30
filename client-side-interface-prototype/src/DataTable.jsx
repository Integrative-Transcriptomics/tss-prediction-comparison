import React from 'react';
import './Visualization.css'; // Import the CSS file for styling the table

// The DataTable component is a reusable table component for displaying data in a structured format.
const DataTable = ({ data, title, isVisible, toggleVisibility }) => (
  <div>
    {/* The table title and a button to toggle the visibility of the table */}
    <h2>
      {title} 
      <button onClick={toggleVisibility}>
        {/* Button label changes based on the visibility state */}
        {isVisible ? 'Hide' : 'Show'}
      </button>
    </h2>
    {/* Render the table only if it is visible */}
    {isVisible && (
      <table className="styled-table">
        <thead>
          <tr>
            {/* Render the table headers dynamically based on the keys of the first data object */}
            {Object.keys(data[0]).map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {/* Render each row of data */}
          {data.map((row, index) => (
            <tr key={index}>
              {/* Render each cell in the row based on the values of the data object */}
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
