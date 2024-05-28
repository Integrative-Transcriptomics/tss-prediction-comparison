import React, { useState } from 'react';
import Condition from './Condition';

function ProjectForm() {
  const [projectName, setProjectName] = useState('');
  const [conditions, setConditions] = useState([{ id: 1 }]);

  const addCondition = () => {
    setConditions([...conditions, { id: conditions.length + 1 }]);
  };

  const handleProjectNameChange = (e) => {
    setProjectName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Start TSS Prediction button clicked');
    console.log('Project Name:', projectName);
    console.log('Conditions:', conditions);
    // Add logic here to handle form submission
    console.log('Starting TSS Prediction with project:', projectName);
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
          <Condition key={condition.id} id={condition.id} />
        ))}
        <button type="button" onClick={addCondition}>+</button>
      </div>
      <button className="start-button" onClick={handleSubmit}>Start TSS Prediction</button>
    </div>
  );
}

export default ProjectForm;
