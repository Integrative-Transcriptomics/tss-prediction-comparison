import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function JobManagement() {
  const location = useLocation();
  const { formData } = location.state || { formData: null };

  const [projectName, setProjectName] = useState('');
  const [conditions, setConditions] = useState([]);
  const [gffFiles, setGffFiles] = useState([]);
  const [masterTableFiles, setMasterTableFiles] = useState([]);

  useEffect(() => {
    const fetchProjectData = async () => {
      try {
        if (formData) {
          const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error('Failed to fetch project data.');
          }

          const data = await response.json();
          setProjectName(data.projectName || '');
          setConditions(data.conditions || []);
          setGffFiles(data.gffFiles || []);
          setMasterTableFiles(data.masterTableFiles || []);
        }
      } catch (error) {
        console.error('Error fetching project data:', error);
      }
    };

    fetchProjectData();
  }, [formData]);

  return (
    <div>
      <h1>Job Management</h1>
      <p>Project Name: {projectName}</p>
      
      <div>
        <h2>Conditions:</h2>
        <ul>
          {conditions.map((condition, index) => (
            <li key={index}>{condition.name}</li>
          ))}
        </ul>
      </div>
      
      <div>
        <h2>GFF Files:</h2>
        <ul>
          {gffFiles.map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
      </div>
      
      <div>
        <h2>Master Table Files:</h2>
        <ul>
          {masterTableFiles.map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default JobManagement;
