// import React, { useEffect, useRef } from 'react';
// import * as d3 from 'd3';

// const RadialChartsComponent = () => {
//   const svgRef = useRef();

//   useEffect(() => {
//     // Hardcoded LCA values
//     const lcaData = {
//       totalInitialConstructionCost: 6182839.35,
//       totalInitialCarbonEmissionCost: 852863.5179648,
//       timeCost: 231856.47562499996,
//       roadUserCost: 698062500.0,
//       additionalCarbonEmissionCost: 930.652416,
//       periodicMaintenanceCost: 112349.87834103756,
//       periodicMaintenanceCarbonEmissionCost: 2817743.7305447874,
//       totalRoutineInspectionCost: 45.21627618069613,
//       repairRehabilitationCost: 2042725.0607461378,
//       demolitionDisposalCost: 53916.66345914902,
//       recyclingCost: 64094739.32469964,
//       reconstructionCost: 61512192.81077006
//     };

//     // Calculate lifecycle stages
//     const initialStage = 28.5;
//     const useStage = 48.11
//     const endOfLifeStage =100;
//     const beyondLifeStage =0;

//     const totalCost = 100;

//     // Calculate percentages
//     const percentage = [
//       (initialStage / totalCost) * 100,
//       (useStage / totalCost) * 100,
//       (endOfLifeStage / totalCost) * 100,
//       (beyondLifeStage / totalCost) * 100
//     ];

//     // Colors and labels (exact same as Python code)
//     const colors = [ '#273B5C', '#961818', '#5A003B','#708090'];
//     const stageLabel = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage'];

//     // Data array (same order as Python code)
//     const data = [
//       { name: stageLabel[3], value: percentage[3] / 100, color: colors[3] },
//       { name: stageLabel[2], value: percentage[2] / 100, color: colors[2] },
//       { name: stageLabel[1], value: percentage[1] / 100, color: colors[1] },
//       { name: stageLabel[0], value: percentage[0] / 100, color: colors[0] }
//     ];

//     // Window properties (exact same as Python code)
//     const width = 500;
//     const height = 400;
//     const barWidth = 20;
//     const spacing = 10;
//     const center = { x: width / 2, y: height / 2 };


//     // Clear previous content
//     d3.select(svgRef.current).selectAll("*").remove();
//    const svg = d3.select(svgRef.current)
//   .attr("viewBox", `0 0 ${width} ${height}`)
//   .attr("preserveAspectRatio", "xMidYMid meet")
//   .attr("width", "100%")
//   .attr("height", "100%");


//     const g = svg.append("g")
//       .attr("transform", `translate(${center.x},${center.y})`);

//     // Create tooltip
//     const tooltip = d3.select("body").select(".tooltip");
//     let tooltipDiv;
//     if (tooltip.empty()) {
//       tooltipDiv = d3.select("body").append("div")
//         .attr("class", "tooltip")
//         .style("position", "absolute")
//         .style("text-align", "center")
//         .style("padding", "8px")
//         .style("background", "white")
//         .style("border-radius", "8px")
//         .style("box-shadow", "0 2px 6px rgba(0,0,0,0.2)")
//         .style("pointer-events", "none")
//         .style("opacity", 0)
//         .style("font-size", "14px")
//         .style("transform", "translateX(-50%)")
//         .style("z-index", "1000");
//     } else {
//       tooltipDiv = tooltip;
//     }

//     // Generate arcs (exact same logic as Python code)
//     data.forEach((d, i) => {
//       const innerRadius = 50 + i * (barWidth + spacing);
//       const outerRadius = innerRadius + barWidth;

//       // Arc generator
//       const arcGen = d3.arc()
//         .innerRadius(innerRadius)
//         .outerRadius(outerRadius)
//         .startAngle(0)
//         .cornerRadius(10);

//       // Create path
//       const path = g.append("path")
//         .datum(d)
//         .attr("fill", d.color)
//         .attr("d", arcGen({ endAngle: 0 }))
//         .attr("class", "arc");

//       // Animation (exact same as Python - 1200ms duration)
//       path.transition()
//         .duration(1200)
//         .attrTween("d", function(d) {
//           const interpolate = d3.interpolate(0, (d.value * 2 * Math.PI) + 0.03);
//           return function(t) {
//             return arcGen({ endAngle: interpolate(t) });
//           };
//         });

//       // Static percentage labels (exact same positioning as Python)
//       const labelX = center.x - 8;
//       const labelY = center.y + (data.length - 1 - i) * (barWidth + spacing) - 150;

//       svg.append("text")
//         .attr("x", labelX)
//         .attr("y", labelY + 5)
//         .attr("text-anchor", "end")
//         .attr("class", "label")
//         .style("font-size", "14px")
//         .style("fill", "#333")
//         .text(`${(d.value * 100).toFixed(2)}%`);

//       // Hover events (exact same as Python code)
//       path.on("mouseover", function(event, hoveredData) {
//         d3.selectAll(".arc")
//           .attr("fill", p => p === hoveredData ? p.color : "#ccc");

//         tooltipDiv.style("opacity", 1)
//           .html(`
//             <div style="text-align:center; font-family:sans-serif;">
//               <span style="font-weight: 500;">${hoveredData.name}</span>
//               <br>
//               <span style="color: #638B48; font-size: 13.5px;">
//                 Economic Cost: 
//                 <span style="font-weight: 600;">
//                   ${(hoveredData.value * 100).toFixed(1)}%;
//                   ${(hoveredData.value * 225.5).toFixed(2)}
//                 </span>
//               </span>
//               <br>
//               <span style="font-weight: bold; color: #638B48;">Lakhs</span>
//             </div>
//           `)
//           .style("left", (event.pageX) + "px")
//           .style("top", (event.pageY - 50) + "px");
//       })
//       .on("mousemove", function(event) {
//         tooltipDiv.style("left", (event.pageX) + "px")
//           .style("top", (event.pageY - 70) + "px");
//       })
//       .on("mouseout", function() {
//         d3.selectAll(".arc")
//           .attr("fill", d => d.color);
//         tooltipDiv.style("opacity", 0);
//       });
//     });

//   }, []);

//   return (
//   <div className="w-full h-full">
//     <div style={{ 
//       background: '#f2e8e7', 
//       fontFamily: 'sans-serif', 
//       display: 'flex', 
//       flexDirection: 'column', 
//       justifyContent: 'flex-start', 
//       alignItems: 'center', 
//       height: '100%',  // ✅ This replaces minHeight: '100vh'
//       margin: 0 
//     }}>
//       <h2   className="font-bold" style={{ 
//         marginTop: '20px', 
//         marginBottom: '10px', 
//         fontSize: '20px', 
     
//         textAlign: 'center'
       
//       }}>
//         <span style={{ color: '#638B48' }}>Economic cost</span> distribution across various stages for bridges for 50 years
//       </h2>
//       <svg ref={svgRef} className="w-full h-full"></svg>
//     </div>
//   </div>
// );
// }
// export default RadialChartsComponent;
import React from 'react';
import RadialChart from './RadialChart';

const RadialChartsComponent = () => {
  const colors = ['#273B5C', '#961818', '#5A003B', '#708090'];
  const stageLabels = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage'];
  
  const percentages = [28.5, 48.11, 100, 0]; // Initial, Use, End of Life, Beyond Life
  
  const data = [
    { name: stageLabels[3], value: percentages[3] / 100, color: colors[3] },
    { name: stageLabels[2], value: percentages[2] / 100, color: colors[2] },
    { name: stageLabels[1], value: percentages[1] / 100, color: colors[1] },
    { name: stageLabels[0], value: percentages[0] / 100, color: colors[0] }
  ];

  return (
    <RadialChart
      data={data}
      title="Economic cost distribution across various stages for bridges for 50 years"
      titleColor="#638B48"
      tooltipClass="economic-50-tooltip"
      tooltipColorLabel="Economic Cost"
      tooltipColor="#638B48"
      showValueInTooltip={true}
      valueMultiplier={225.5}
      decimalPlaces={2}
    />
  );
};

export default RadialChartsComponent;