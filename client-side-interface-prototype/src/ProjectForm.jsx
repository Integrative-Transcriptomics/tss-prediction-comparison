import React, { useState, useRef, useEffect } from 'react';
import Condition from './Condition';
import TssMasterTable from './TssMasterTable';
import GFF from './GFF';

function ProjectForm() {
  const [projectName, setProjectName] = useState('');
  const [conditions, setConditions] = useState([{ id: 1, ref: React.createRef() }]);
  const gffRef = useRef(null);
  const tssMasterTableRef = useRef(null);

  const addCondition = () => {
    setConditions([...conditions, { id: conditions.length + 1, ref: React.createRef() }]);
  };

  const deleteCondition = () => {
    if (conditions.length > 1) {
      const newConditions = [...conditions];
      newConditions.pop();
      setConditions(newConditions);
    }
  };

  const handleProjectNameChange = (e) => {
    setProjectName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create FormData object
    const formData = new FormData();

    // Append the GFF file
    if (gffRef.current && gffRef.current.file) {
      formData.append('gff', gffRef.current.file, 'gff-file.gff');
    }

    // Append the master table file
    if (tssMasterTableRef.current && tssMasterTableRef.current.file) {
      formData.append('master_table', tssMasterTableRef.current.file, 'master-table.tsv');
    }

    // Append the conditions files
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
      // Send the data to the backend
      const response = await fetch('http://your-backend-url/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Files successfully uploaded');
      } else {
        console.error('File upload failed');
      }
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  return (
    <div className="project-form">
      <h1>TSS prediction tool</h1>
      <div className="form-group">
        <label>Project Name:</label>
        <input
          type="text"
          value={projectName}
          onChange={handleProjectNameChange}
          placeholder="Your Project name"
        />
      </div>
      <div className="form-group">
        <label>Data Upload:</label>
        {conditions.map((condition) => (
          <Condition key={condition.id} id={condition.id} ref={condition.ref} />
        ))}
        <button className="button" onClick={addCondition}>+</button>
        <button className="button" onClick={deleteCondition}>-</button>
      </div>
      <div>
        <TssMasterTable ref={tssMasterTableRef} />
      </div>
      <div>
        <GFF ref={gffRef} />
      </div>
      <button className="start-button" onClick={handleSubmit}>Start TSS Prediction</button>
    </div>
  );
}

export default ProjectForm;
