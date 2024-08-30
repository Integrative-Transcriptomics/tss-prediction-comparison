import React, { useEffect } from 'react';
import * as echarts from 'echarts';

// The TSSDistributionChart component renders a bar chart using ECharts to visualize TSS data.
const TSSDistributionChart = ({ forwardCsvData, reverseCsvData }) => {
  useEffect(() => {
    if (forwardCsvData && reverseCsvData) {
      const chartDom = document.getElementById('echarts');
      const myChart = echarts.init(chartDom);

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

      // Parse the forward and reverse CSV data
      const forwardParsedData = parseCsv(forwardCsvData);
      const reverseParsedData = parseCsv(reverseCsvData);

      // Function to process the parsed data and organize it by TSS type
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

      // Combine and sort file names from forward and reverse data
      const fileNames = Array.from(new Set([...Object.keys(forwardData), ...Object.keys(reverseData)])).sort((a, b) => a.localeCompare(b));
      const tssTypes = Array.from(new Set([...forwardParsedData.map(row => row['TSS type']), ...reverseParsedData.map(row => row['TSS type'])]));
      
      // Prepare the series data for the chart
      const seriesData = tssTypes.map(tssType => ({
        name: tssType,
        type: 'bar',
        stack: 'total',
        label: { show: true },
        emphasis: { focus: 'series' },
        data: fileNames.map(fileName => (forwardData[fileName]?.[tssType] || 0) + (reverseData[fileName]?.[tssType] || 0))
      }));

      // Chart configuration options
      const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: {},
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: {
          type: 'category',
          data: fileNames,
          axisLabel: {
            interval: 0,
            rotate: 45
          }
        },
        dataZoom: [{
          type: 'slider',
          yAxisIndex: 0,
          filterMode: 'empty',
          start: 0,
          end: Math.min(100, 10 * (10 / fileNames.length))
        }],
        series: seriesData
      };

      // Set the chart options and render the chart
      myChart.setOption(option);
    }
  }, [forwardCsvData, reverseCsvData]);

  return <div id="echarts" style={{ width: '160%', height: '600px', overflowY: 'auto' }}></div>;
};

export default TSSDistributionChart;
