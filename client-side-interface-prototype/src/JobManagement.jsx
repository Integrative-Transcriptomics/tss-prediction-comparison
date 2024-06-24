// JobManagement.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';

function JobManagement() {
  // to access the projectName we access the passed state from the first page with useLocation
  const location = useLocation();
  // if the projectName is undefined for whatever reason the default projectName is empty
  const { projectName } = location.state || { projectName: 'Default Project Name' };

  return (
    <div>
      <h1>Job Management</h1>
      <p>Project Name: {projectName}</p>
    </div>
  );
}

export default JobManagement;