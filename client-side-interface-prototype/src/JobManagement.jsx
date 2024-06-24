// JobManagement.jsx
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function JobManagement() {
  // to access the projectName we access the passed state from the first page with useLocation
  const location = useLocation();
  // if the projectName is undefined for whatever reason the default projectName is empty
  const { projectName } = location.state || { projectName: 'Default Project Name' };

  const navigatetoVisualization = useNavigate();

  const handleVisualization = () => {
    navigatetoVisualization('/visualization');
  }

  return (
    <div>
      <h1>Job Management</h1>
      <p>Project Name: {projectName}</p>
      <button onClick={handleVisualization}>Go to Visualization</button>
    </div>
  );
}

export default JobManagement;

