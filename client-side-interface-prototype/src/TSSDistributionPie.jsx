import React from 'react';
import ReactECharts from 'echarts-for-react';

const TSSDistributionPie = () => {
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

  const types = ['iTSS', 'asTSS', 'pTSS/sTSS', 'pTSS', 'sTSS', 'orphan'];
  const distributionPredator = types.map(type => {
    return {
      name: type,
      value: dataTSSPredator.filter(d => d.TSS_type === type).length
    };
  });

  const distributionTSSpred = types.map(type => {
    return {
      name: type,
      value: dataTSSpred.filter(d => d.TSS_type === type).length
    };
  });

  const option = {
    title: {
      text: 'TSS Type Distribution',
      subtext: 'Comparison between TSS-Predator and TSSpred',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: 'TSS-Predator',
        type: 'pie',
        radius: '50%',
        center: ['25%', '60%'],
        data: distributionPredator,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      },
      {
        name: 'TSSpred',
        type: 'pie',
        radius: '50%',
        center: ['75%', '60%'],
        data: distributionTSSpred,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  return (
    <div>
      <h2>TSS Type Distribution</h2>
      <ReactECharts option={option} style={{ height: '600px', width: '100%' }} />
    </div>
  );
};

export default TSSDistributionPie;
