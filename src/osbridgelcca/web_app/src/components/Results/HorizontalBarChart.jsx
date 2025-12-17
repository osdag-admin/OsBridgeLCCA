
// import React, { useEffect, useRef } from 'react';
// import * as d3 from 'd3';

// const HorizontalBarChart = () => {
//   const chartRef = useRef();
//   const tooltipRef = useRef();
//   const containerRef = useRef();

//   // Hardcoded values converted to lakhs
//    const originalData = [
//      { name: 'Initial construction cost', value: 67.013, color: '#638B48' },
//      { name: 'Embodied carbon emissions', value: 11.020, color: '#6F6F6F' },
//        { name: 'Time cost estimate', value: 16.75, color:'#638B48'  },
//     { name: 'Road user cost', value: 82.617, color:'#E09365' },
//     { name: 'Additional Carbon emission costs due to re-routing', value: 19.35, color: '#6F6F6F' },
//      { name: 'Annual routine inspection costs', value: 13.800, color: '#638B48' },
   
  
//     { name: 'Periodic Maintenance costs', value: 1.495, color: '#638B48' },
//     { name: 'Periodic maintenance carbon emissions', value: 17.67, color: '#6F6F6F' },
   
//     { name: 'Repair and rehabilitation costs', value: 0, color: '#638B48' },
//     { name: 'Demolition and deconstruction costs', value: 0.83, color: '#638B48' },
//     {name: 'Recycling costs', value: -3.347, color: '#638B48' },
//     {name:'TotalLifeCycleCost',value: 212.15, color: '#FFFFFF' }
//   ];
  

//   useEffect(() => {
//     const resizeObserver = new ResizeObserver(() => {
//       renderChart();
//     });

//     if (containerRef.current) {
//       resizeObserver.observe(containerRef.current);
//     }

//     return () => {
//       resizeObserver.disconnect();
//     };
//   }, []);

//   const renderChart = () => {
//     if (!containerRef.current) return;

//     // FIXED: Keep original order instead of reversing
//     const data = [...originalData]; // Removed .reverse()
//     const dimColor = 'rgba(200,200,200,0.4)';

//     // Display adjustment for zero/very small values
//     const costList = originalData.map(d => d.value).filter(v => v > 0);
//     const minCost = Math.min(...costList);
    
//     const processedData = data.map(d => ({
//       ...d,
//       displayValue: d.value === 0 || d.value < 0.001 ? minCost / 2 : d.value
//     }));

//     // Clear previous chart
//     d3.select(chartRef.current).selectAll("*").remove();

//     // Get container dimensions
//     const containerRect = containerRef.current.getBoundingClientRect();
//     const containerWidth = containerRect.width;
//     const containerHeight = containerRect.height;

//     // Define margins and dimensions
//     const margin = { top: 60, right: 40, bottom: 60, left: 200 };
//     const width = containerWidth - margin.left - margin.right;
//     const height = containerHeight - margin.top - margin.bottom;

//     // Create SVG that fills the container
//     const svg = d3.select(chartRef.current)
//       .append("svg")
//       .attr("width", containerWidth)
//       .attr("height", containerHeight)
//       .style("background-color", "#F0E6E6")
//       .append("g")
//       .attr("transform", `translate(${margin.left},${margin.top})`);

//     // Draw plot background
//     svg.append("rect")
//       .attr("width", width)
//       .attr("height", height)
//       .attr("fill", "#F0E6E6");

//     // Create tooltip
//     const tooltip = d3.select(tooltipRef.current);

//     // SCALE CONFIGURATION - You can modify these values
//     const maxValue = d3.max(processedData, d => d.displayValue);
//     const scaleMultiplier = 1.1; // Change this to adjust scale range
//     const customMaxValue = maxValue * scaleMultiplier; // Or set a fixed value like 300
    
//     // Define scales
//     const x = d3.scaleLinear()
//       .domain([0, customMaxValue]) // You can change this to [0, 300] for fixed scale
//       .range([0, width]);

//     const y = d3.scaleBand()
//       .domain(processedData.map(d => d.name))
//       .range([0, height])
//       .paddingInner(0.2);

//     // Add axes
//     const xAxis = svg.append("g")
//       .attr("class", "x axis")
//       .attr("transform", `translate(0,${height})`)
//       .style("opacity", 0)
//       .call(d3.axisBottom(x));

//     xAxis.append("text")
//       .attr("x", width / 2)
//       .attr("y", 40)
//       .attr("fill", "black")
//       .attr("text-anchor", "middle")
//       .style("font-size", "16px")
//       .text("Cost in Lakhs");

//     const yAxis = svg.append("g")
//       .attr("class", "y axis")
//       .style("opacity", 0)
//       .call(d3.axisLeft(y));

//     // Remove Y-axis tick labels and lines
//     yAxis.selectAll("text").filter(function() {
//       return d3.select(this).text() !== "Name";
//     }).remove();
//     yAxis.selectAll("line").remove();

//     // Create bars
//     const bars = svg.selectAll(".bar")
//       .data(processedData)
//       .enter()
//       .append("rect")
//       .attr("class", "bar")
//       .attr("x", 0)
//       .attr("y", d => y(d.name))
//       .attr("width", 0)
//       .attr("height", y.bandwidth())
//       .attr("fill", d => d.color)
//       .style("transition", "fill 0.3s ease");

//     // Fixed starting position for text labels
//     const fixedTextPosition = 10; // Fixed position from left edge

//     // Add text labels with fixed position and always black color
//     const textLabels = svg.selectAll(".bar-label")
//       .data(processedData)
//       .enter()
//       .append("text")
//       .attr("class", "bar-label")
//       .attr("x", fixedTextPosition) // Fixed position from left
//       .attr("y", d => y(d.name) + y.bandwidth() / 2)
//       .attr("dy", "0.35em")
//       .style("font-family", "Arial, sans-serif")
//       .style("font-size", "12px")
//       .style("text-anchor", "start")
//       .style("opacity", 0)
//       .style("user-select", "none")
//       .attr("fill", "black") // Always black
//       .text(d => d.name);

//     // Event handlers
//     function handleMouseOver(event, d) {
//       bars.transition().duration(100).attr("fill", barD => 
//         barD === d ? barD.color : dimColor
//       );

//       // Keep text labels black during hover
//       textLabels.attr("fill", "black");

//       tooltip
//         .html(`<b>${d.name}</b>: ${d.value.toFixed(4)} Lakh`)
//         .style("opacity", 1);
//     }

//     function handleMouseOut() {
//       bars.transition().duration(100).attr("fill", d => d.color);

//       // Keep text labels black
//       textLabels.attr("fill", "black");

//       tooltip.style("opacity", 0);
//     }

//     function handleMouseMove(event) {
//       tooltip
//         .style("left", (event.pageX + 10) + "px")
//         .style("top", (event.pageY - 30) + "px");
//     }

//     // Animate bars
//     bars.transition()
//       .duration(1500)
//       .ease(d3.easeElastic.amplitude(0.5).period(0.5))
//       .attr("width", d => x(d.displayValue));

//     // Animate axes
//     svg.selectAll(".axis")
//       .transition()
//       .duration(1000)
//       .delay(1000)
//       .style("opacity", 1);

//     // Animate text labels
//     textLabels.transition()
//       .duration(800)
//       .delay((d, i) => 800 + (i * 100))
//       .style("opacity", 1)
//       .attr("fill", "black"); // Ensure they remain black after animation

//     // Add hover events
//     bars.on("mouseover", handleMouseOver)
//         .on("mouseout", handleMouseOut)
//         .on("mousemove", handleMouseMove);

//     textLabels.on("mouseover", handleMouseOver)
//               .on("mouseout", handleMouseOut)
//               .on("mousemove", handleMouseMove);
//   };

//   return (
//     <div ref={containerRef} className="w-full h-full bg-white rounded-lg">
      
//       <div className="w-full h-full" style={{ minHeight: '400px' }}>
//         <div className="text-center bg-[#F0E6E6] text-lg font-bold  pt-5">
//           Life-Cycle Costs for 50 years
//           </div>
//         <div ref={chartRef} className="w-full h-full"></div>
//       </div>
//       <div 
//         ref={tooltipRef}
//         className="fixed bg-white border border-gray-300 rounded p-2 pointer-events-none opacity-0 transition-opacity duration-200 text-xs shadow-lg z-50"
//         style={{whiteSpace: 'nowrap'}}
//       ></div>
//     </div>
//   );
// };

// export default HorizontalBarChart;\
import React from 'react';
 import ReusableBarChart from './ReusableBarChart';


const HorizontalBarChart = () => {
  const data = [
    { name: 'Initial construction cost', value: 67.013, color: '#638B48' },
    { name: 'Embodied carbon emissions', value: 11.020, color: '#6F6F6F' },
    { name: 'Time cost estimate', value: 16.75, color:'#638B48' },
    { name: 'Road user cost', value: 82.617, color:'#E09365' },
    { name: 'Additional Carbon emission costs due to re-routing', value: 19.35, color: '#6F6F6F' },
    { name: 'Annual routine inspection costs', value: 13.800, color: '#638B48' },
    { name: 'Periodic Maintenance costs', value: 1.495, color: '#638B48' },
    { name: 'Periodic maintenance carbon emissions', value: 17.67, color: '#6F6F6F' },
    { name: 'Repair and rehabilitation costs', value: 0, color: '#638B48' },
    { name: 'Demolition and deconstruction costs', value: 0.83, color: '#638B48' },
    { name: 'Recycling costs', value: -3.347, color: '#638B48' },
    { name:'TotalLifeCycleCost', value: 212.15, color: '#FFFFFF' }
  ];

  return (
    <ReusableBarChart
      data={data}
      title="Life-Cycle Costs for 100 years"
      backgroundColor="#F0E6E6"
      scaleMultiplier={1.1}
    />
  );
};

export default HorizontalBarChart;