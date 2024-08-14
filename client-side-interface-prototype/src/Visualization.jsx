import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as echarts from 'echarts';
import UpSetPlot from './UpSetPlot'; // Import the UpSetPlot component
import './Visualization.css';

function Visualization() {
  const { conditionId } = useParams();
  const [jobIds, setJobIds] = useState(null);
  const [forwardCsvData, setForwardCsvData] = useState(null);
  const [reverseCsvData, setReverseCsvData] = useState(null);
  const [commonCsvData, setCommonCsvData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isForwardVisible, setIsForwardVisible] = useState(false);
  const [isReverseVisible, setIsReverseVisible] = useState(false);
  const [isCommonVisible, setIsCommonVisible] = useState(false);

  useEffect(() => {
    const fetchJobIds = async () => {
      try {
        const response = await fetch(`/api/get_jobids?condition_id=${conditionId}`);
        if (!response.ok) throw new Error('Failed to fetch job IDs');
        const data = await response.json();
        fetchCsvData(data.forward, setForwardCsvData);
        fetchCsvData(data.reverse, setReverseCsvData);
        fetchCommonCsvData(data.forward); // Assuming common TSS is related to forward job ID
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };
    const fetchCsvData = async (jobId, setCsvData) => {
      try {
        const response = await fetch(`/api/get_tss?jobid=${jobId}`);
        if (!response.ok) throw new Error('Failed to fetch TSS data');
        const data = await response.text();
        setCsvData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    const fetchCommonCsvData = async (jobId) => {
      try {
        const response = await fetch(`/api/get_common?jobid=${jobId}`);
        if (!response.ok) throw new Error('Failed to fetch common TSS data');
        const data = await response.text();
        setCommonCsvData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchJobIds();
  }, [conditionId]);

  useEffect(() => {
    if (forwardCsvData && reverseCsvData) {
      const chartDom = document.getElementById('echarts');
      const myChart = echarts.init(chartDom);
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
      const forwardParsedData = forwardCsvData ? parseCsv(forwardCsvData) : [];
      const reverseParsedData = reverseCsvData ? parseCsv(reverseCsvData) : [];
      const processData = (parsedData) => {
        const fileData = {};
        parsedData.forEach(row => {
          const fileName = row['gene name'];
          const tssType = row['TSS type'];
          if (!fileData[fileName]) fileData[fileName] = {};
          if (!fileData[fileName][tssType]) fileData[fileName][tssType] = 0;
          fileData[fileName][tssType] += 1;
        });
        return fileData;
      };
      const forwardData = processData(forwardParsedData);
      const reverseData = processData(reverseParsedData);

      // Get all gene names and sort them to ensure consistent order
      const fileNames = Array.from(new Set([...Object.keys(forwardData), ...Object.keys(reverseData)]));

      // Sort genes by total count (descending) and take the top 10
      const topGeneNames = fileNames
        .map(fileName => {
          const totalCount = Object.values(forwardData[fileName] || {}).reduce((sum, count) => sum + count, 0)
            + Object.values(reverseData[fileName] || {}).reduce((sum, count) => sum + count, 0);
          return { fileName, totalCount };
        })
        .sort((a, b) => b.totalCount - a.totalCount)
        .slice(0, 10)
        .map(item => item.fileName);

      const tssTypes = Array.from(new Set([...forwardParsedData.map(row => row['TSS type']), ...reverseParsedData.map(row => row['TSS type'])]));
      const seriesData = tssTypes.map(tssType => {
        return {
          name: tssType,
          type: 'bar',
          stack: 'total',
          label: { show: true },
          emphasis: { focus: 'series' },
          data: topGeneNames.map(fileName => (forwardData[fileName]?.[tssType] || 0) + (reverseData[fileName]?.[tssType] || 0))
        };
      });
      const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: {},
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: { type: 'category', data: topGeneNames },
        series: seriesData
      };
      myChart.setOption(option);
    }
  }, [forwardCsvData, reverseCsvData]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

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

  const forwardParsedData = forwardCsvData ? parseCsv(forwardCsvData) : [];
  const reverseParsedData = reverseCsvData ? parseCsv(reverseCsvData) : [];
  const commonParsedData = commonCsvData ? parseCsv(commonCsvData) : [];

  const renderTable = (data, title, isVisible, toggleVisibility) => (
    <div>
      <h2>
        {title} 
        <button onClick={toggleVisibility}>
          {isVisible ? 'Hide' : 'Show'}
        </button>
      </h2>
      {isVisible && (
        <table className="styled-table">
          <thead>
            <tr>
              {Object.keys(data[0]).map((header, index) => (
                <th key={index}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );

  return (
    <div className="visualization-container">
      <div className="visualization-content">
        <h1>Visualization Page</h1>
        <p>This is the visualization content for Condition ID: {conditionId}</p>
        
        <div id="echarts" style={{ width: '160%', height: '600px' }}></div>
  
        {forwardParsedData.length > 0 && renderTable(forwardParsedData, 'Forward Job Data', isForwardVisible, () => setIsForwardVisible(!isForwardVisible))}
        {reverseParsedData.length > 0 && renderTable(reverseParsedData, 'Reverse Job Data', isReverseVisible, () => setIsReverseVisible(!isReverseVisible))}
        {commonParsedData.length > 0 && renderTable(commonParsedData, 'Common TSS Data', isCommonVisible, () => setIsCommonVisible(!isCommonVisible))}
        
        <UpSetPlot conditionId={conditionId} /> {/* Add UpSetPlot component here */}
      </div>
    </div>
  );
}

export default Visualization;
