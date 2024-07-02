import React from 'react';
import UpSetJS, { extractCombinations } from '@upsetjs/react';

const UpSetPlot = () => {
  // Beispieldaten
  const dataTSSPredator = [
    { TSS_site: 25675, TSS_type: 'iTSS' },
    { TSS_site: 31366, TSS_type: 'asTSS' },
    { TSS_site: 31650, TSS_type: 'pTSS/sTSS' },
    { TSS_site: 32000, TSS_type: 'asTSS' },
    { TSS_site: 50000, TSS_type: 'iTSS' },
    { TSS_site: 60000, TSS_type: 'sTSS' }
  ];

  const dataTSSpred = [
    { TSS_site: 25675, TSS_type: 'iTSS' },
    { TSS_site: 31366, TSS_type: 'asTSS' },
    { TSS_site: 405, TSS_type: 'iTSS' },
    { TSS_site: 400, TSS_type: 'pTSS/sTSS' },
    { TSS_site: 500, TSS_type: 'orphan' },
    { TSS_site: 5000, TSS_type: 'pTSS' },
    { TSS_site: 6000, TSS_type: 'sTSS' }
  ];

  // Kombinieren der Daten zu einem Set
  const combinedData = [
    ...dataTSSPredator.map(d => ({ name: d.TSS_site.toString(), sets: ['TSS-Predator'] })),
    ...dataTSSpred.map(d => ({ name: d.TSS_site.toString(), sets: ['TSSpred'] }))
  ];

  const { sets, combinations } = extractCombinations(combinedData);

  return (
    <div>
      <h2>UpSet Plot</h2>
      <UpSetJS sets={sets} combinations={combinations} width={800} height={600} />
    </div>
  );
};

export default UpSetPlot;
