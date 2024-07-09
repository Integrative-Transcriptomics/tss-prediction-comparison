import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Visualization() {
  // Get the condition from the URL parameters
  const { conditionId } = useParams();
  const [forwardCsvData, setForwardCsvData] = useState(null);
  const [reverseCsvData, setReverseCsvData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJobIds = async () => {
      try {
        const response = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch job IDs');
        }
        const data = await response.json();
        fetchCsvData(data.forward, setForwardCsvData);
        fetchCsvData(data.reverse, setReverseCsvData);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    const fetchCsvData = async (jobId, setCsvData) => {
      try {
        const response = await fetch(`/api/get_tss?jobid=${jobId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch TSS data');
        }
        const data = await response.text(); // Fetch as text to parse CSV
        setCsvData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchJobIds();
  }, [conditionId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!forwardCsvData && !reverseCsvData) {
    return <div>No data available</div>;
  }

  // Function to parse CSV data into an array of objects
  const parseCsv = (csvText) => {
    const lines = csvText.split('\n').filter(line => line.trim() !== ''); // Filter out empty lines
    const headers = lines[0].split(',');
    return lines.slice(1).map(line => {
      const values = line.split(',');
      return headers.reduce((obj, header, index) => {
        obj[header] = values[index];
        return obj;
      }, {});
    });
  };

  const forwardParsedData = forwardCsvData ? parseCsv(forwardCsvData) : [];
  const reverseParsedData = reverseCsvData ? parseCsv(reverseCsvData) : [];

  return (
    <div>
      <h1>Visualization Page</h1>
      <p>This is the visualization content for Condition ID: {conditionId}</p>
      
      {forwardParsedData.length > 0 ? (
        <div>
          <h2>Forward Job Data</h2>
          <table>
            <thead>
              <tr>
                {Object.keys(forwardParsedData[0]).map((header, index) => (
                  <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {forwardParsedData.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No forward data available</p>
      )}
      
      {reverseParsedData.length > 0 ? (
        <div>
          <h2>Reverse Job Data</h2>
          <table>
            <thead>
              <tr>
                {Object.keys(reverseParsedData[0]).map((header, index) => (
                  <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {reverseParsedData.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No reverse data available</p>
      )}
    </div>
  );
}

export default Visualization;
