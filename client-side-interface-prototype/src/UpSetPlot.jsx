import React, { useEffect, useState } from 'react';
import UpSetJS, { extractCombinations } from '@upsetjs/react';

const UpSetPlot = ({ conditionId }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching job IDs...');
        const jobIdsResponse = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
        if (!jobIdsResponse.ok) {
          throw new Error('Failed to fetch job IDs');
        }
        const jobIdsData = await jobIdsResponse.json();
        console.log('Job IDs fetched:', jobIdsData);
        const commonJobId = jobIdsData.forward; // Assuming common TSS is related to forward job ID
        
        console.log('Fetching common TSS data...');
        const commonTssResponse = await fetch(`/api/get_common?jobid=${commonJobId}`);
        if (!commonTssResponse.ok) {
          throw new Error('Failed to fetch common TSS data');
        }
        const csvText = await commonTssResponse.text();
        console.log('Common TSS data fetched:', csvText);
        const parsedData = parseCsv(csvText);
        console.log('Parsed data:', parsedData);
        setData(parsedData);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    const parseCsv = (csvText) => {
      const lines = csvText.split('\n').filter(line => line.trim() !== '');
      const headers = lines[0].split(',');
      return lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.reduce((obj, header, index) => {
          obj[header] = values[index];
          return obj;
        }, {});
      });
    };

    fetchData();
  }, [conditionId]);

  if (loading) return <div>Loading UpSet Plot...</div>;
  if (error) return <div>Error: {error}</div>;

  const combinedData = data.map(d => ({
    name: d.Pos, // Assuming 'Pos' is a field in the common TSS data
    sets: d['TSS type'] ? d['TSS type'].split('/') : [] // Ensure 'TSS type' exists and split correctly
  })).filter(d => d.name && d.sets.length > 0); // Filter out invalid entries

  console.log('Combined data for UpSet plot:', combinedData);

  if (combinedData.length === 0) return <div>No data available for UpSet Plot</div>;

  const { sets, combinations } = extractCombinations(combinedData);

  console.log('Sets:', sets);
  console.log('Combinations:', combinations);

  return (
    <div>
      <UpSetJS sets={sets} combinations={combinations} width={800} height={400} />
    </div>
  );
};

export default UpSetPlot;
