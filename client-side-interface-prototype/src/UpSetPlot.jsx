import React, { useEffect, useState } from 'react';
import UpSetJS, { extractCombinations } from '@upsetjs/react';

const UpSetPlot = ({ conditionId }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch job IDs based on condition ID
        const jobIdsResponse = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
        const jobIdsData = await jobIdsResponse.json();
        const jobId = jobIdsData.forward; 

        // Fetch combined TSS data
        const combinedTssResponse = await fetch(`/api/get_combined_tss?condition=${conditionId}`);
        const combinedTssCsvText = await combinedTssResponse.text();
        const parsedTssData = parseCsv(combinedTssCsvText);

        // Fetch master table data using the job ID
        const masterTableResponse = await fetch(`/api/get_master_table?jobid=${jobId}`);
        const masterTableCsvText = await masterTableResponse.text();
        const parsedMasterTableData = parseCsv(masterTableCsvText);

        // Process the data for UpSet plot
        const upSetData = processUpSetData(parsedTssData, parsedMasterTableData);
        setData(upSetData);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    const parseCsv = (csvText) => {
      const lines = csvText.split('\n').filter(line => line.trim() !== '');
      const headers = lines[0].split(',').map(header => header.trim());
      return lines.slice(1).map(line => {
        const values = line.split(',').map(value => value.trim());
        return headers.reduce((obj, header, index) => {
          obj[header] = values[index];
          return obj;
        }, {});
      });
    };

    const processUpSetData = (combinedTssData, masterTableData) => {
      const tolerance = 5;
      const aggregatedDataByPosition = new Map();

      const findOrCreatePosition = (pos, tssType, source) => {
        for (let [existingPos, data] of aggregatedDataByPosition.entries()) {
          if (Math.abs(existingPos - pos) <= tolerance) {
            data[source][tssType] = (data[source][tssType] || 0) + 1;
            return;
          }
        }
        aggregatedDataByPosition.set(pos, { master: {}, combined: {} });
        aggregatedDataByPosition.get(pos)[source][tssType] = 1;
      };

      masterTableData.forEach(entry => {
        let tssType = entry['TSS type'];
        if (tssType === 'orphan') tssType = 'orph';
        if (tssType === 'pTSS/sTSS') tssType = 'p/sTSS';
        const pos = parseInt(entry.Pos, 10);
        findOrCreatePosition(pos, tssType, 'master');
      });

      combinedTssData.forEach(entry => {
        let tssType = entry['TSS type'];
        if (tssType === 'orphan') tssType = 'orph';
        if (tssType === 'pTSS/sTSS') tssType = 'p/sTSS';
        const pos = parseInt(entry.Pos, 10);
        findOrCreatePosition(pos, tssType, 'combined');
      });

      const upSetData = [];
      const tssTypes = ['orph', 'asTSS', 'iTSS', 'p/sTSS'];

      tssTypes.forEach(type => {
        const masterKey = `${type} predator`;
        const combinedKey = `${type} plorer`;

        const masterCount = Array.from(aggregatedDataByPosition.values()).reduce((acc, val) => acc + (val.master[type] || 0), 0);
        const combinedCount = Array.from(aggregatedDataByPosition.values()).reduce((acc, val) => acc + (val.combined[type] || 0), 0);

        upSetData.push({
          name: masterKey,
          sets: [masterKey],
          size: masterCount,
        });

        upSetData.push({
          name: combinedKey,
          sets: [combinedKey],
          size: combinedCount,
        });

        const intersectionCount = Array.from(aggregatedDataByPosition.values()).reduce((acc, val) => {
          return acc + Math.min(val.master[type] || 0, val.combined[type] || 0);
        }, 0);

        upSetData.push({
          name: `${type} intersection`,
          sets: [masterKey, combinedKey],
          size: intersectionCount,
        });
      });

      return upSetData;
    };

    fetchData();
  }, [conditionId]);

  if (loading) return <div>Loading UpSet Plot...</div>;
  if (error) return <div>Error: {error}</div>;

  const { sets, combinations } = extractCombinations(data);

  return (
    <div>
      <UpSetJS
        sets={sets}
        combinations={combinations}
        width={1000}  // Set the width of the plot
        height={600}  // Set the height of the plot
        options={{
          labels: {
            rotation: 0,  // No rotation
            fontSize: 12,  // Adjust font size if necessary
          },
        }}
      />
    </div>
  );
};

export default UpSetPlot;
