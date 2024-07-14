import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Condition from './Condition';
import TssMasterTable from './TssMasterTable';
import GFF from './GFF';

// The main functional component for the project form.
function ProjectForm() {
  // State for managing the project name input.
  const [projectName, setProjectName] = useState('');
  
  // State for managing the list of conditions. Each condition has a name, a unique id and a reference for handling file uploads.
  const [conditions, setConditions] = useState([{ name: 'Condition 1', id: 1, ref: React.createRef() }]);
  
  // Reference for the GFF component to access its file state.
  const gffRef = useRef(null);
  
  // Reference for the TSS Master Table component to access its file state.
  const tssMasterTableRef = useRef(null);

  // Use the useNavigate hook to navigate to a different page.
  const navigate = useNavigate();

  // State to manage the feedback message displayed after submitting.
  const [feedbackMessage, setFeedbackMessage] = useState('');

  // State to manage the error message displayed if no project name was given
  const [errorMessage, setErrorMessage] = useState('');

  // Function to add a new condition to the list. It creates a new condition with a name, a unique id and a reference.
  const addCondition = () => {
    const index = conditions.length + 1;
    // back-ticks not single quotes for variables inside strings
    setConditions([...conditions, { name: `Condition ${index}`, id: index, ref: React.createRef() }]);
  };

  // Function to remove the last condition from the list. Ensures there is at least one condition left.
  const deleteCondition = () => {
    if (conditions.length > 1) {
      const newConditions = [...conditions];
      newConditions.pop();
      setConditions(newConditions);
    }
  };

  // Function to handle changes to the project name input field.
  const handleProjectNameChange = (e) => {
    setProjectName(e.target.value);
  };

  // Function to handle form submission and upload files to the server.
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the default form submission behavior.

    // clear previous error messages
    setErrorMessage('');

    // Error message if project name is empty
    if (!projectName.trim()) {
      setErrorMessage('Project Name cannot be empty.');
      return
    }

    // Error message if 

    // Set the feedback message
    setFeedbackMessage('Files successfully uploaded, please load the Project-Manager');

    // Create a FormData object to send files and data via a multipart/form-data request.
    const formData = new FormData();

    // Append the name of the project to the FormData object if it exists.
    if (!projectName.trim()) {
      console.error('Project Name cannot be empty.');
    } else {
      formData.append('projectName', projectName);
    }

    // Append the GFF file to the FormData object if it exists.
    if (gffRef.current && gffRef.current.file) {
      formData.append('gff', gffRef.current.file, 'gff-file.gff');
    }

    // Append the TSS Master Table file to the FormData object if it exists.
    if (tssMasterTableRef.current && tssMasterTableRef.current.file) {
      formData.append('master_table', tssMasterTableRef.current.file, 'master-table.tsv');
    }

    // Append the forward and reverse files for each condition to the FormData object.
    conditions.forEach((condition, index) => {
      const conditionRef = condition.ref.current;
      if (conditionRef) {
        conditionRef.forwardFiles.forEach((file, idx) => {
          formData.append(`condition_${index + 1}_forward_${idx + 1}`, file, file.name);
        });
        conditionRef.reverseFiles.forEach((file, idx) => {
          formData.append(`condition_${index + 1}_reverse_${idx + 1}`, file, file.name);
        });
      }
    });

    try {
      // Send the FormData object to the backend using a POST request.
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      // Check if the response is successful.
      if (response.ok) {
        console.log('Files successfully uploaded');
      } else {
        console.error('File upload failed');
      }
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  const handleLoadJobManagement = () => {
    // Navigate to the Job Management page using the navigate function from the useNavigate hook.
    navigate('/job-management');
  };

  return (
    <div className="project-form">
      <h1>TSS Prediction Tool</h1>
      
      {/* Project Name Input */}
      <div className="form-group">
        <label>Project Name:</label>
        <input
          type="text"
          value={projectName}
          onChange={handleProjectNameChange}
          placeholder="Your Project name"
        />
      </div>
      
      {/* Condition File Upload Section */}
      <div className="form-group">
        <label>Data Upload:</label>
        
        {/* Render each Condition component in the conditions array */}
        {conditions.map((condition) => (
          <Condition key={condition.id} id={condition.id} ref={condition.ref} />
        ))}
        
        {/* Buttons to add or remove conditions */}
        <button className="button" onClick={addCondition}>+</button>
        <button className="button" onClick={deleteCondition}>-</button>
      </div>
      
      {/* TSS Master Table File Upload */}
      <div>
        <TssMasterTable ref={tssMasterTableRef} />
      </div>
      
      {/* GFF File Upload */}
      <div>
        <GFF ref={gffRef} />
      </div>
      
      {/* Buttons Container */}
      <div className='buttons-container'> 
      {/* Submit Button */}
      <button className="start-button" onClick={handleSubmit}>Start TSS Prediction</button>
      {/* Job Management Page Button */}
      <button className="load-job-button" onClick={handleLoadJobManagement}>Load Project-Manager</button>
    </div>
    {/* Feedback Message */}
    {feedbackMessage && <div className="feedback-message">{feedbackMessage}</div>}
    {/* Error message: Project Name cannot be empty*/}
    {errorMessage && <div className="error-message">{errorMessage} </div>}
  </div>
  );
}

export default ProjectForm;
