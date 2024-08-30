import React from 'react';
import Condition from './Condition';

function ConditionList({ conditions, setConditions }) {
  const addCondition = () => {
    const index = conditions.length + 1;
    setConditions([...conditions, { id: index, ref: React.createRef(), name: "" }]);
  };

  const deleteCondition = () => {
    if (conditions.length > 1) {
      setConditions(conditions.slice(0, -1));
    }
  };

  const updateConditionName = (id, newName) => {
    setConditions(conditions.map(
      condition => id === condition.id ? { ...condition, name: newName } : condition
    ));
  };

  return (
    <div className="form-group">
      <label>Data Upload:</label>
      {conditions.map(condition => (
        <div className="condition-input-group" key={condition.id}>
          <Condition key={condition.id} id={condition.id} ref={condition.ref} name={condition.name} />
          <input
            type="text"
            onChange={(e) => updateConditionName(condition.id, e.target.value)}
            placeholder={`Name of Condition ${condition.id} (has to match the corresponding condition in the mastertable)`}
          />
        </div>
      ))}
      <button className="button" onClick={addCondition}>+</button>
      <button className="button" onClick={deleteCondition}>-</button>
    </div>
  );
}

export default ConditionList;
