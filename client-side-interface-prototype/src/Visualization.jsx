import React from 'react';
import { useParams } from 'react-router-dom';
import UpSetPlot from './UpSetPlot';

function Visualization() {
  // Get the condition from the URL parameters
  const { conditionId } = useParams();

  return (
    <div>
      <h1>Visualization Page</h1>
      <p>This is a placeholder for visualization content for Condition ID: {conditionId}</p>
      <UpSetPlot />
    </div>
  );
}

export default Visualization;