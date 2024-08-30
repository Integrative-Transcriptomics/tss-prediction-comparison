import React from 'react';
import Condition from './Condition';

function ConditionList({ conditions, setConditions }) {
  // Function to add a new condition to the list.
  const addCondition = () => {
    const index = conditions.length + 1;
    // Add a new condition with a unique ID and a ref for forward and reverse file handling.
    setConditions([...conditions, { id: index, ref: React.createRef(), name: "" }]);
  };

  // Function to remove the last condition from the list.
  const deleteCondition = () => {
    if (conditions.length > 1) {
      // Remove the last condition in the array.
      setConditions(conditions.slice(0, -1));
    }
  };

  // Function to update the name of a specific condition.
  const updateConditionName = (id, newName) => {
    // Update the name of the condition matching the given ID.
    setConditions(conditions.map(
      condition => id === condition.id ? { ...condition, name: newName } : condition
    ));
  };

  return (
    <div className="form-group">
      <label>Data Upload:</label>
      {/* Render each condition in the list */}
      {conditions.map(condition => (
        <div className="condition-input-group" key={condition.id}>
          {/* Render the Condition component */}
          <Condition key={condition.id} id={condition.id} ref={condition.ref} name={condition.name} />
          {/* Input for the name of the condition */}
          <input
            type="text"
            onChange={(e) => updateConditionName(condition.id, e.target.value)}
            placeholder={`Name of Condition ${condition.id} (has to match the corresponding condition in the mastertable)`}
          />
        </div>
      ))}
      {/* Button to add a new condition */}
      <button className="button" onClick={addCondition}>+</button>
      {/* Button to remove the last condition */}
      <button className="button" onClick={deleteCondition}>-</button>
    </div>
  );
}

export default ConditionList;
