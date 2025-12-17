// 
import React from 'react';
import RadialChart from './RadialChart';

const EconomicCost100Years = () => {
  const colors = ['#273B5C', '#961818', '#5A003B', '#36454F'];
  const stageLabels = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage'];
  
  const percentages = [90, 75, 63, 52]; // Initial, Use, End of Life, Beyond Life
  
  const data = [
    { name: stageLabels[3], value: percentages[3] / 100, color: colors[3] },
    { name: stageLabels[2], value: percentages[2] / 100, color: colors[2] },
    { name: stageLabels[1], value: percentages[1] / 100, color: colors[1] },
    { name: stageLabels[0], value: percentages[0] / 100, color: colors[0] }
  ];

  return (
    <RadialChart
      data={data}
      title="Economic cost distribution across various stages for bridges for 100 years"
      titleColor="#638B48"
      tooltipClass="economic-100-tooltip"
      tooltipColorLabel="Economic Cost"
      tooltipColor="#638B48"
      decimalPlaces={0}
    />
  );
};

export default EconomicCost100Years;