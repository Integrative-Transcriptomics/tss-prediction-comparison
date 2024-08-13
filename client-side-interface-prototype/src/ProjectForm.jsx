import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Condition from './Condition';
import TssMasterTable from './TssMasterTable';
import GFF from './GFF';

// The main functional component for the project form.
function ProjectForm() {
  // State for managing the project name input.
  const [projectName, setProjectName] = useState('');
  
  // State for managing the list of conditions. Each condition has a name, a unique id and a reference for handling file uploads.
  const [conditions, setConditions] = useState([{ id: 1, ref: React.createRef(), name: 'Condition 1' }]);
  
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
    setConditions([...conditions, { id: index, ref: React.createRef(), name: `Condition ${index}` }]);
  };

  // Function for updating the condition name given the chosen conditions id and the new chosen name
  const updateConditionName = (id, newName) => {
    // declare new conditions array so that the state isnt directly mutated and map over the current conditions
    const updatedConditions = conditions.map(
      condition => {
        if(id === condition.id) {
          // update the name of the current condition 
          return {...condition, name: newName};
        }
        // dont change the unaffected conditions
        return condition;
      }
    )
    setConditions(updatedConditions);
  }
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

    // Set the feedback message
    setFeedbackMessage('');

    // Error message if project name is empty
    if (!projectName.trim()) {
      setErrorMessage('Project Name cannot be empty.');
      return
    }

    // Check for matching forward and reverse file counts
    for (const condition of conditions) {
      const conditionRef = condition.ref.current;
      if (conditionRef) {
         // Check if the number of forward and reverse files are equal
        if (conditionRef.forwardFiles.length !== conditionRef.reverseFiles.length) {
          setErrorMessage(`The number of forward and reverse files for ${condition.name} do not match.`);
          return;
        }
          
        // Check if there are any files uploaded for this condition
        if (conditionRef.forwardFiles.length === 0 && conditionRef.reverseFiles.length === 0) {
           setErrorMessage(`No files uploaded for Condition ${condition.id}.`);
           return;
        }
      }
    }

    if (!tssMasterTableRef.current || !tssMasterTableRef.current.file) { 
      setErrorMessage('Please upload a master table from TSSpredator for the comparison.');
      return;
    }

    if (!gffRef.current || !gffRef.current.file) {
      setErrorMessage('Please upload a GFF file for the TSS classification.');
      return;
    }

    // Create a FormData object to send files and data via a multipart/form-data request.
    const formData = new FormData();

    // Append the name of the project to the FormData object.
      formData.append('projectName', projectName);
    
    // Append the GFF file to the FormData object.
      formData.append('gff', gffRef.current.file, 'gff-file.gff');

    // Append the TSS Master Table file to the FormData object.
      formData.append('master_table', tssMasterTableRef.current.file, 'master-table.tsv');

    // Append the forward and reverse files for each condition to the FormData object.
    conditions.forEach((condition, index) => {
      const conditionRef = condition.ref.current;
      if (conditionRef) {
        conditionRef.forwardFiles.forEach((file, idx) => {
          formData.append(`condition_${index + 1}_forward_${idx + 1}`, file, file.name);
          formData.append(`condition_${index + 1}_forward_${idx + 1}_name`, condition.name);
        });
        conditionRef.reverseFiles.forEach((file, idx) => {
          formData.append(`condition_${index + 1}_reverse_${idx + 1}`, file, file.name);
          formData.append(`condition_${index + 1}_reverse_${idx + 1}_name`, condition.name);

        });
      }
    });

    try {

      // Indicate that the files are being uploaded.
      setFeedbackMessage('Files are currently uploading, please wait a few seconds...');

      // Send the FormData object to the backend using a POST request.
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      // Check if the response is successful.
      if (response.ok) {
        const result = await response.json();

        // If the server sends a success message, set the feedback message.
        console.log('Files successfully uploaded');
        setFeedbackMessage('Files successfully uploaded, please load the Project-Manager');
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
      <h1>TSSplorer</h1>
      <p className="subheading"> TSS prediction and comparison Tool</p>
      
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
        
        {/* Render each Condition component and its corresponding input field */}
        {conditions.map(
          (condition) =>
            <div className="condition-input-group" key = {condition.id}>
              <Condition key={condition.id} id={condition.id} ref={condition.ref} name ={condition.name}/>
              <input 
                type = "text"  
                onChange={(e) => updateConditionName(condition.id, e.target.value)}
                placeholder={`Name of Condition ${condition.id} (has to match the corresponding condition in the mastertable)`} 
              >
              </input>
            </div>
          )
        }

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
