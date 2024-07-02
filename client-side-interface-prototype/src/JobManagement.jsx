import React, { useState, useEffect } from 'react';

function JobManagement() {
  const [projectName, setProjectName] = useState('');
  const [conditions, setConditions] = useState([]);
  const [gffFiles, setGffFiles] = useState([]);
  const [masterTableFiles, setMasterTableFiles] = useState([]);


  // Dummy IDs for manually testing the fetch operation, adjust ids everytime you start a new prediction
  // condition 1, forward
  const uuid1 = 'f3b37787-e8f6-4921-859c-d00efffcbfe6';
  // condition 1, reverse
  const uuid2 = '34c8a237-ac10-4a34-abf9-493fbdd4b7cc';

  useEffect(() => {
    fetch('/api/get_file?jobid=' + uuid1) 
      .then(response => {
        if (response.ok) {
          console.log("TEST: Response is ok")
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        console.log('Data:', data); 
      })
      .catch(error => {
        console.error('fetch operation failed:', error);
      });
  }, []);

  return (
    <div>
      <h1>Job Management</h1>
      <p>Project Name: </p>
      
      <div>
        <h2>Conditions:</h2>
        
      </div>
      
      <div>
        <h2>GFF Files:</h2>
        
      </div>
      
      <div>
        <h2>Master Table Files:</h2>
        
      </div>
    </div>
  );
}

export default JobManagement;
