// import React, { useEffect, useRef } from 'react';
// import * as d3 from 'd3';

// const ReusableBarChart = ({ 
//   data, 
//   title ,
//   backgroundColor = "#F0E6E6",
//   margin = { top: 60, right: 40, bottom: 60, left: 200 },
//   scaleMultiplier = 1.1,
//   customMaxValue = null,
//   barPadding = 0,
//   animationDuration = 1500,
//   axisAnimationDuration = 1000,
//   textAnimationDuration = 800,
//   textAnimationDelay = 100
// }) => {
//   const chartRef = useRef();
//   const tooltipRef = useRef();
//   const containerRef = useRef();

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
//   }, [data]);

//   const renderChart = () => {
//     if (!containerRef.current || !data || data.length === 0) return;

//     const processedData = [...data];
//     const dimColor = 'rgba(200,200,200,0.4)';

//     // Display adjustment for zero/very small values
//     const costList = data.map(d => d.value).filter(v => v > 0);
//     const minCost = Math.min(...costList);
    
//     const finalData = processedData.map(d => ({
//       ...d,
//       displayValue: d.value === 0 || d.value < 0.001 ? minCost / 2 : d.value
//     }));

//     // Clear previous chart
//     d3.select(chartRef.current).selectAll("*").remove();

//     // Get container dimensions
//     const containerRect = containerRef.current.getBoundingClientRect();
//     const containerWidth = containerRect.width;
//     const containerHeight = containerRect.height;

//     // Calculate dimensions
//     const width = containerWidth - margin.left - margin.right;
//     const height = containerHeight - margin.top - margin.bottom;

//     // Create SVG that fills the container
//     const svg = d3.select(chartRef.current)
//       .append("svg")
//       .attr("width", containerWidth)
//       .attr("height", containerHeight)
//       .style("background-color", backgroundColor)
//       .append("g")
//       .attr("transform", `translate(${margin.left},${margin.top})`);

//     // Draw plot background
//     svg.append("rect")
//       .attr("width", width)
//       .attr("height", height)
//       .attr("fill", backgroundColor);

//     // Create tooltip
//     const tooltip = d3.select(tooltipRef.current);

//     // Scale configuration
//     const maxValue = d3.max(finalData, d => d.displayValue);
//     const scaleMax = customMaxValue || (maxValue * scaleMultiplier);
    
//     // Define scales
//     const x = d3.scaleLinear()
//       .domain([0, scaleMax])
//       .range([0, width]);

//     const y = d3.scaleBand()
//       .domain(finalData.map(d => d.name))
//       .range([0, height])
//       .paddingInner(barPadding);

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
//       .data(finalData)
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
//     const fixedTextPosition = 10;

//     // Add text labels with fixed position and always black color
//     const textLabels = svg.selectAll(".bar-label")
//       .data(finalData)
//       .enter()
//       .append("text")
//       .attr("class", "bar-label")
//       .attr("x", fixedTextPosition)
//       .attr("y", d => y(d.name) + y.bandwidth() / 2)
//       .attr("dy", "0.35em")
//       .style("font-family", "Arial, sans-serif")
//       .style("font-size", "12px")
//       .style("text-anchor", "start")
//       .style("opacity", 0)
//       .style("user-select", "none")
//       .attr("fill", "black")
//       .text(d => d.name);

//     // Event handlers
//     function handleMouseOver(event, d) {
//       bars.transition().duration(100).attr("fill", barD => 
//         barD === d ? barD.color : dimColor
//       );

//       textLabels.attr("fill", "black");

//       tooltip
//         .html(`<b>${d.name}</b>: ${d.value.toFixed(4)} Lakh`)
//         .style("opacity", 1);
//     }

//     function handleMouseOut() {
//       bars.transition().duration(100).attr("fill", d => d.color);
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
//       .duration(animationDuration)
//       .ease(d3.easeElastic.amplitude(0.5).period(0.5))
//       .attr("width", d => x(d.displayValue));

//     // Animate axes
//     svg.selectAll(".axis")
//       .transition()
//       .duration(axisAnimationDuration)
//       .delay(axisAnimationDuration)
//       .style("opacity", 1);

//     // Animate text labels
//     textLabels.transition()
//       .duration(textAnimationDuration)
//       .delay((d, i) => textAnimationDuration + (i * textAnimationDelay))
//       .style("opacity", 1)
//       .attr("fill", "black");

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
//         <div className={`text-center text-lg font-bold `} style={{ backgroundColor }}>
//           {title}
//         </div>
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

// export default ReusableBarChart;
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const ReusableBarChart = ({ 
  data, 
  title,
  backgroundColor = "#F0E6E6",
  margin = { top: 25, right: 100, bottom: 80, left: 200 },
  scaleMultiplier = 1.1,
  customMaxValue = null,
  barPadding = 0.15,
  animationDuration = 1500,
  axisAnimationDuration = 1000,
  textAnimationDuration = 800,
  textAnimationDelay = 100
}) => {
  const chartRef = useRef();
  const tooltipRef = useRef();
  const containerRef = useRef();

  useEffect(() => {
    const resizeObserver = new ResizeObserver(() => {
      renderChart();
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      resizeObserver.disconnect();
    };
  }, [data]);

  const renderChart = () => {
    if (!containerRef.current || !data || data.length === 0) return;

    const processedData = [...data];
    const dimColor = 'rgba(200,200,200,0.4)';

    // Display adjustment for zero/very small values
    const costList = data.map(d => d.value).filter(v => v > 0);
    const minCost = Math.min(...costList);
    
    const finalData = processedData.map(d => ({
      ...d,
      displayValue: d.value === 0 || d.value < 0.001 ? minCost / 2 : d.value
    }));

    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();

    // Get container dimensions
    const containerRect = containerRef.current.getBoundingClientRect();
    const containerWidth = containerRect.width;
    const containerHeight = containerRect.height;

    // Calculate dimensions with proper margins
    const width = Math.max(0, containerWidth - margin.left - margin.right);
    const height = Math.max(0, containerHeight - margin.top - margin.bottom);

    if (width <= 0 || height <= 0) return;

    // Create SVG that fills the container
    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", containerWidth)
      .attr("height", containerHeight)
      .style("background-color", backgroundColor)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Draw plot background
    svg.append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("fill", backgroundColor);

    // Create tooltip
    const tooltip = d3.select(tooltipRef.current);

    // Scale configuration
    const maxValue = d3.max(finalData, d => d.displayValue);
    const scaleMax = customMaxValue || (maxValue * scaleMultiplier);
    
    // Define scales
    const x = d3.scaleLinear()
      .domain([0, scaleMax])
      .range([0, width]);

    const y = d3.scaleBand()
      .domain(finalData.map(d => d.name))
      .range([0, height])
      .paddingInner(barPadding);

    // Add axes with better formatting
    const xAxis = svg.append("g")
      .attr("class", "x axis")
      .attr("transform", `translate(0,${height})`)
      .style("opacity", 0)
      .call(d3.axisBottom(x)
        .tickFormat(d3.format(".0f"))
        .ticks(Math.min(8, Math.floor(width / 60)))
      );

    // Add x-axis label with proper positioning
    xAxis.append("text")
      .attr("x", width / 2)
      .attr("y", 45)
      .attr("fill", "black")
      .attr("text-anchor", "middle")
      .style("font-size", "13px")
      .style("font-weight", "bold")
      .text("Cost in Lakhs");

    const yAxis = svg.append("g")
      .attr("class", "y axis")
      .style("opacity", 0)
      .call(d3.axisLeft(y));

    // Remove Y-axis tick labels and lines
    yAxis.selectAll("text").remove();
    yAxis.selectAll("line").remove();

    // Create bars
    const bars = svg.selectAll(".bar")
      .data(finalData)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", 0)
      .attr("y", d => y(d.name))
      .attr("width", 0)
      .attr("height", y.bandwidth())
      .attr("fill", d => d.color)
      .style("transition", "fill 0.3s ease");

    // Fixed starting position for text labels
    const fixedTextPosition = 10;

    // Add text labels with fixed position and always black color
    const textLabels = svg.selectAll(".bar-label")
      .data(finalData)
      .enter()
      .append("text")
      .attr("class", "bar-label")
      .attr("x", fixedTextPosition)
      .attr("y", d => y(d.name) + y.bandwidth() / 2)
      .attr("dy", "0.35em")
      .style("font-family", "Arial, sans-serif")
      .style("font-size", "10px")
      .style("text-anchor", "start")
      .style("opacity", 0)
      .style("user-select", "none")
      .attr("fill", "black")
      .text(d => d.name);

    // Event handlers
    function handleMouseOver(event, d) {
      bars.transition().duration(100).attr("fill", barD => 
        barD === d ? barD.color : dimColor
      );

      textLabels.attr("fill", "black");

      tooltip
        .html(`<b>${d.name}</b>: ${d.value.toFixed(2)} Lakh`)
        .style("opacity", 1);
    }

    function handleMouseOut() {
      bars.transition().duration(100).attr("fill", d => d.color);
      textLabels.attr("fill", "black");
      tooltip.style("opacity", 0);
    }

    function handleMouseMove(event) {
      tooltip
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 30) + "px");
    }

    // Animate bars
    bars.transition()
      .duration(animationDuration)
      .ease(d3.easeElastic.amplitude(0.5).period(0.5))
      .attr("width", d => x(d.displayValue));

    // Animate axes
    svg.selectAll(".axis")
      .transition()
      .duration(axisAnimationDuration)
      .delay(axisAnimationDuration)
      .style("opacity", 1);

    // Animate text labels
    textLabels.transition()
      .duration(textAnimationDuration)
      .delay((d, i) => textAnimationDuration + (i * textAnimationDelay))
      .style("opacity", 1)
      .attr("fill", "black");

    // Add hover events
    bars.on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut)
        .on("mousemove", handleMouseMove);

    textLabels.on("mouseover", handleMouseOver)
              .on("mouseout", handleMouseOut)
              .on("mousemove", handleMouseMove);
  };

  return (
    <div ref={containerRef} className="w-full h-full bg-white rounded-lg overflow-hidden">
      <div className="w-full h-full flex flex-col">
        <div className={`text-center text-sm font-bold py-1 flex-shrink-0`} style={{ backgroundColor }}>
          {title}
        </div>
        <div ref={chartRef} className="w-full flex-1 min-h-0"></div>
      </div>
      <div 
        ref={tooltipRef}
        className="fixed bg-white border border-gray-300 rounded p-2 pointer-events-none opacity-0 transition-opacity duration-200 text-xs shadow-lg z-50"
        style={{whiteSpace: 'nowrap'}}
      ></div>
    </div>
  );
};

export default ReusableBarChart;