import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import * as echarts from 'echarts';

function Visualization() {
  // Get the condition from the URL parameters
  const { conditionId } = useParams();
  const [jobIds, setJobIds] = useState(null);
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

  useEffect(() => {
    if (forwardCsvData && reverseCsvData) {
      const chartDom = document.getElementById('echarts');
      const myChart = echarts.init(chartDom);

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

      const processData = (parsedData) => {
        const fileData = {};
        parsedData.forEach(row => {
          const fileName = row['gene name'];
          const tssType = row['TSS type'];
          if (!fileData[fileName]) {
            fileData[fileName] = {};
          }
          if (!fileData[fileName][tssType]) {
            fileData[fileName][tssType] = 0;
          }
          fileData[fileName][tssType] += 1;
        });
        return fileData;
      };

      const forwardData = processData(forwardParsedData);
      const reverseData = processData(reverseParsedData);

      const fileNames = Array.from(new Set([...Object.keys(forwardData), ...Object.keys(reverseData)]));
      const tssTypes = Array.from(new Set([...forwardParsedData.map(row => row['TSS type']), ...reverseParsedData.map(row => row['TSS type'])]));

      const seriesData = tssTypes.map(tssType => {
        return {
          name: tssType,
          type: 'bar',
          stack: 'total',
          label: {
            show: true
          },
          emphasis: {
            focus: 'series'
          },
          data: fileNames.map(fileName => (forwardData[fileName]?.[tssType] || 0) + (reverseData[fileName]?.[tssType] || 0))
        };
      });

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {},
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: fileNames
        },
        series: seriesData
      };

      myChart.setOption(option);
    }
  }, [forwardCsvData, reverseCsvData]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Visualization Page</h1>
      <p>This is the visualization content for Condition ID: {conditionId}</p>
      <div id="echarts" style={{ width: '100%', height: '600px' }}></div>
    </div>
  );
}

export default Visualization;
