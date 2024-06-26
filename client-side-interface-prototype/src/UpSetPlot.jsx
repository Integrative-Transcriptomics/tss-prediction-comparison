import React from 'react';
import ReactECharts from 'echarts-for-react';

const UpSetPlot = () => {
  // Beispieldaten
  const dataTSSPredator = [
    { TSS_site: 25675, TSS_type: 'iTSS' },
    { TSS_site: 31366, TSS_type: 'asTSS' },
    { TSS_site: 31650, TSS_type: 'pTSS/sTSS' },
    { TSS_site: 32000, TSS_type: 'asTSS' },
    { TSS_site: 405, TSS_type: 'iTSS' },
    { TSS_site: 50000, TSS_type: 'pTSS' },
    { TSS_site: 60000, TSS_type: 'sTSS' }
  ];

  const dataTSSpred = [
    { TSS_site: 25675, TSS_type: 'iTSS' },
    { TSS_site: 31366, TSS_type: 'asTSS' },
    { TSS_site: 405, TSS_type: 'iTSS' },
    { TSS_site: 400, TSS_type: 'pTSS/sTSS' },
    { TSS_site: 500, TSS_type: 'orphan' },
    { TSS_site: 50000, TSS_type: 'pTSS' },
    { TSS_site: 60000, TSS_type: 'sTSS' }
  ];

  // Berechnung der Gesamtanzahl der TSS
  const totalTSS = new Set([...dataTSSPredator.map(d => d.TSS_site), ...dataTSSpred.map(d => d.TSS_site)]).size;

  // Berechnung der Anzahl der überschneidenden TSS
  const overlapTSS = dataTSSPredator.filter(d1 => dataTSSpred.some(d2 => d2.TSS_site === d1.TSS_site)).length;

  // Berechnung der Anzahl der TSS mit demselben Typ
  const sameTypeTSS = dataTSSPredator.filter(d1 =>
    dataTSSpred.some(d2 => d2.TSS_site === d1.TSS_site && d2.TSS_type === d1.TSS_type)
  ).length;

  // Berechnung der Überschneidungen pro TSS-Typ
  const types = ['iTSS', 'asTSS', 'pTSS/sTSS', 'pTSS', 'sTSS', 'orphan'];
  const typeOverlap = types.map(type => {
    return {
      name: type,
      value: dataTSSPredator.filter(d1 => 
        dataTSSpred.some(d2 => d2.TSS_site === d1.TSS_site && d2.TSS_type === d1.TSS_type && d1.TSS_type === type)
      ).length
    };
  });

  // Aggregierte Daten für den UpSet Plot
  const aggregatedData = [
    { name: 'Total TSS', value: totalTSS },
    { name: 'Overlap TSS', value: overlapTSS },
    { name: 'Same Type TSS', value: sameTypeTSS },
    ...typeOverlap
  ];

  const option = {
    title: {
      text: 'UpSet Plot'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: aggregatedData.map(item => item.name),
      axisLabel: {
        rotate: 45,
        align: 'right'
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: 'Size',
        type: 'bar',
        data: aggregatedData.map(item => item.value),
        itemStyle: {
          color: '#3398DB'
        },
        barWidth: '60%'
      }
    ]
  };

  return (
    <div>
      <h2>UpSet Plot</h2>
      <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />
    </div>
  );
};

export default UpSetPlot;

