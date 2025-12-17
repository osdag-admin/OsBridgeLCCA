// 
import React from 'react';
import RadialChart from './RadialChart';

const SocialCostRadialChart = () => {
  const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
  const stageLabels = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage'];
  
  const percentages = [54.92, 0, 0, 0]; // Initial, Use, End of Life, Beyond Life
  
  const data = [
    { name: stageLabels[3], value: percentages[3] / 100, color: colors[3] },
    { name: stageLabels[2], value: percentages[2] / 100, color: colors[2] },
    { name: stageLabels[1], value: percentages[1] / 100, color: colors[1] },
    { name: stageLabels[0], value: percentages[0] / 100, color: colors[0] }
  ];

  return (
    <RadialChart
      data={data}
      title="Social cost distribution across various stages for PSC bridges for 50 years"
      titleColor="#d2691e"
      tooltipClass="social-50-tooltip"
      tooltipColorLabel="Social Cost"
      tooltipColor="#d2691e"
      decimalPlaces={2}
    />
  );
};

export default SocialCostRadialChart;