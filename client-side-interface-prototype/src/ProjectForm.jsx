import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ConditionList from './ConditionList';
import TssMasterTable from './TssMasterTable';
import GFF from './GFF';
import Feedback from './Feedback'; // Neue zusammengefasste Komponente

function ProjectForm() {
  const [projectName, setProjectName] = useState('');
  const [conditions, setConditions] = useState([{ id: 1, ref: React.createRef(), name: "" }]);
  const gffRef = useRef(null);
  const tssMasterTableRef = useRef(null);
  const navigate = useNavigate();
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [previousProjectName, setPreviousProjectName] = useState('');
  const [isUploadComplete, setIsUploadComplete] = useState(true);

  const handleProjectNameChange = (e) => setProjectName(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setFeedbackMessage('');

    if (!validateForm()) return;

    const formData = createFormData();
    try {
      setIsUploadComplete(false);
      setFeedbackMessage('Files are currently uploading, please wait a few seconds...');

      const response = await fetch('/api/upload', { method: 'POST', body: formData });

      if (response.ok) {
        setPreviousProjectName(projectName);
        setFeedbackMessage('Files successfully uploaded, please load the Project-Manager');
      } else {
        console.error('File upload failed');
      }
    } catch (error) {
      console.error('Error uploading files:', error);
    } finally {
      setIsUploadComplete(true);
    }
  };

  const validateForm = () => {
    if (!projectName.trim()) {
      setErrorMessage('Project Name cannot be empty.');
      return false;
    }
    if (projectName === previousProjectName) {
      setErrorMessage('The Project Name cannot be uploaded twice.');
      return false;
    }
    if (!validateConditions()) return false;
    if (!validateFiles()) return false;
    return true;
  };

  const validateConditions = () => {
    for (const condition of conditions) {
      const conditionRef = condition.ref.current;
      if (!condition.name.trim()) {
        setErrorMessage(`Condition ${condition.id} name cannot be empty.`);
        return false;
      }
      if (!conditionRef || conditionRef.forwardFiles.length === 0 || conditionRef.reverseFiles.length === 0) {
        setErrorMessage(`No files uploaded for Condition ${condition.id}.`);
        return false;
      }
      if (conditionRef.forwardFiles.length !== conditionRef.reverseFiles.length) {
        setErrorMessage(`The number of forward and reverse files for ${condition.name} do not match.`);
        return false;
      }
    }
    return true;
  };

  const validateFiles = () => {
    if (!tssMasterTableRef.current || !tssMasterTableRef.current.file) {
      setErrorMessage('Please upload a master table from TSSpredator for the comparison.');
      return false;
    }
    if (!gffRef.current || !gffRef.current.file) {
      setErrorMessage('Please upload a GFF file for the TSS classification.');
      return false;
    }
    return true;
  };

  const createFormData = () => {
    const formData = new FormData();
    formData.append('projectName', projectName);
    formData.append('gff', gffRef.current.file, 'gff-file.gff');
    formData.append('master_table', tssMasterTableRef.current.file, 'master-table.tsv');
    conditions.forEach((condition, index) => {
      const conditionRef = condition.ref.current;
      if (conditionRef) {
        appendConditionFiles(formData, conditionRef, condition.name, index);
      }
    });
    return formData;
  };

  const appendConditionFiles = (formData, conditionRef, conditionName, index) => {
    conditionRef.forwardFiles.forEach((file, idx) => {
      formData.append(`condition_${index + 1}_forward_${idx + 1}`, file, file.name);
      formData.append(`condition_${index + 1}_forward_${idx + 1}_name`, conditionName);
    });
    conditionRef.reverseFiles.forEach((file, idx) => {
      formData.append(`condition_${index + 1}_reverse_${idx + 1}`, file, file.name);
      formData.append(`condition_${index + 1}_reverse_${idx + 1}_name`, conditionName);
    });
  };

  const handleLoadJobManagement = () => navigate('/job-management');

  return (
    <div className="project-form">
      <h1>TSSplorer</h1>
      <p className="subheading">TSS prediction and comparison Tool</p>
      
      <div className="form-group">
        <label>Project Name:</label>
        <input type="text" value={projectName} onChange={handleProjectNameChange} placeholder="Your Project name" />
      </div>

      <ConditionList conditions={conditions} setConditions={setConditions} />

      <TssMasterTable ref={tssMasterTableRef} />
      <GFF ref={gffRef} />

      <div className='buttons-container'>
        <button className="start-button" onClick={handleSubmit} disabled={!isUploadComplete}>Start TSS Prediction</button>
        <button className="load-job-button" onClick={handleLoadJobManagement}>Load Project-Manager</button>
      </div>

      <Feedback errorMessage={errorMessage} feedbackMessage={feedbackMessage} />
    </div>
  );
}

export default ProjectForm;
