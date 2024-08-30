import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import DataTable from './DataTable';
import TSSDistributionChart from './TSSDistributionChart';
import HeaderWithTooltip from './HeaderWithTooltip';
import UpSetPlot from './UpSetPlot';
import './Visualization.css';

// The Visualization component is the main component for visualizing TSS data, including tables, charts, and plots.
function Visualization() {
  // Extract the conditionId from the URL parameters using useParams hook
  const { conditionId } = useParams();
  const [conditionName, setConditionName] = useState('');
  const [forwardCsvData, setForwardCsvData] = useState(null);
  const [reverseCsvData, setReverseCsvData] = useState(null);
  const [commonCsvData, setCommonCsvData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isForwardVisible, setIsForwardVisible] = useState(false);
  const [isReverseVisible, setIsReverseVisible] = useState(false);
  const [isCommonVisible, setIsCommonVisible] = useState(false);

  useEffect(() => {
    // Fetch the condition name based on the conditionId when the component mounts or conditionId changes
    const fetchConditionName = async () => {
      try {
        const response = await fetch(`/api/get_condition_name?condition=${conditionId}`);
        if (!response.ok) throw new Error('Failed to fetch condition name');
        const data = await response.json();
        setConditionName(data.Name);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchConditionName();
  }, [conditionId]);

  useEffect(() => {
    // Fetch the job IDs and associated CSV data for forward, reverse, and common TSS data
    const fetchJobIds = async () => {
      try {
        const response = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
        if (!response.ok) throw new Error('Failed to fetch job IDs');
        const data = await response.json();
        fetchCsvData(data.forward, setForwardCsvData);
        fetchCsvData(data.reverse, setReverseCsvData);
        fetchCommonCsvData(conditionId);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    // Fetch and set the CSV data for a given job ID
    const fetchCsvData = async (jobId, setCsvData) => {
      try {
        const response = await fetch(`/api/get_tss?jobid=${jobId}`);
        if (!response.ok) throw new Error('Failed to fetch TSS data');
        const data = await response.text();
        setCsvData(data);
      } catch (error) {
        setError(error.message);
        setCsvData('');
      } finally {
        setLoading(false);
      }
    };

    // Fetch and set the common CSV data for the given condition
    const fetchCommonCsvData = async (conditionId) => {
      try {
        const response = await fetch(`/api/get_common?condition=${conditionId}`);
        if (!response.ok) throw new Error('Failed to fetch common TSS data');
        const data = await response.text();
        setCommonCsvData(data);
      } catch (error) {
        setError(error.message);
        setCommonCsvData('');
      } finally {
        setLoading(false);
      }
    };

    fetchJobIds();
  }, [conditionId]);

  // Function to parse CSV data into an array of objects
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

  // Parse the CSV data if it exists
  const forwardParsedData = forwardCsvData ? parseCsv(forwardCsvData) : [];
  const reverseParsedData = reverseCsvData ? parseCsv(reverseCsvData) : [];
  const commonParsedData = commonCsvData ? parseCsv(commonCsvData) : [];

  // Function to render a data table component with visibility toggling
  const renderDataTable = (data, title, isVisible, toggleVisibility, key) => {
    if (data.length > 0) {
      return (
        <DataTable 
          key={key}  // Key is required for lists in React to maintain unique identity
          data={data} 
          title={title} 
          isVisible={isVisible} 
          toggleVisibility={toggleVisibility} 
        />
      );
    }
    return null;
  };

  // Table configuration for the different data types
  const tables = [
    { data: forwardParsedData, title: 'Forward Job Data', isVisible: isForwardVisible, toggleVisibility: () => setIsForwardVisible(!isForwardVisible) },
    { data: reverseParsedData, title: 'Reverse Job Data', isVisible: isReverseVisible, toggleVisibility: () => setIsReverseVisible(!isReverseVisible) },
    { data: commonParsedData, title: 'Common TSS Data', isVisible: isCommonVisible, toggleVisibility: () => setIsCommonVisible(!isCommonVisible) },
  ];

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="visualization-container">
      <div className="visualization-content">
        <h1>Visualization Page</h1>
        <p>This is the visualization content for Condition: {conditionName}</p>

        {/* Render the TSS Distribution Chart with a header and tooltip */}
        <HeaderWithTooltip 
          title="Distribution of TSS Types Across Genes"
          tooltipText="This bar plot shows the distribution of different TSS types across various genes.
                      You can use the two sliders to view an interval of genes of your choice.
                      By clicking on the buttons of the different TSS types, you can switch their display off and on."
        />

        <TSSDistributionChart forwardCsvData={forwardCsvData} reverseCsvData={reverseCsvData} />

        {/* Render each of the tables for forward, reverse, and common data */}
        {tables.map(({ data, title, isVisible, toggleVisibility }, index) => 
          renderDataTable(data, title, isVisible, toggleVisibility, index)
        )}

        {/* Render the UpSet plot with a header and tooltip */}
        <HeaderWithTooltip 
          title="TSS Intersection Analysis"
          tooltipText="This UpSet plot visualizes the overlaps of TSSs across different categories, showing how many TSSs are present in various combinations of these categories.
                      The vertical bars at the top represent the size of these overlaps, while the horizontal bars indicate the total number of TSSs in each category."
        />

        <UpSetPlot conditionId={conditionId} />
      </div>
    </div>
  );
}

export default Visualization;
