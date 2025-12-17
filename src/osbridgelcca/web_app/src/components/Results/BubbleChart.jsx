import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const BubbleChart = () => {
  const chartRef = useRef();
  const tooltipRef = useRef();

  // Hardcoded carbon emission values and costs
  const data = [
    { 
      name: 'A', 
      value: 16.65, // Initial Carbon Emission Cost percentage
      x: 409, 
      y: 271, 
      label: 'Initial Carbon Emission Cost',
      cost: 8.53 // 852863.5179648 / 100000
    },
    { 
      name: 'B', 
      value: 0.018, // Carbon Emission due to Re-Routing percentage  
      x: 382, 
      y: 113, 
      label: 'Carbon Emission due to Re-Routing',
      cost: 0.009 // 930.652416 / 100000
    },
    { 
      name: 'C', 
      value: 51.89, // Maintenance Emission Costs percentage
      x: 259, 
      y: 216, 
      label: 'Maintenance Emission Costs',
      cost: 28.18 // 2817743.7305447874 / 100000
    }
  ];

  useEffect(() => {
    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();

    const svgWidth = 750;
    const svgHeight = 550;
    
    const radiusScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([30, 78]);

    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);

    // Background circle
    svg.append("circle")
      .attr("cx", 350)
      .attr("cy", 200)
      .attr("r", 180)
      .attr("fill", "#ffffff")
      .attr("opacity", 0.9);

    const tooltip = d3.select(tooltipRef.current);

    const groups = svg.selectAll("g")
      .data(data)
      .enter()
      .append("g")
      .attr("transform", d => `translate(${d.x}, ${d.y})`);

    // Create circles with animation
    groups.append("circle")
      .attr("r", 0)
      .attr("fill", "#808000")
      .transition()
      .delay((_, i) => i * 300)
      .duration(1000)
      .attr("r", d => radiusScale(d.value));

    // Event listeners with hover effects
    groups.selectAll("circle")
      .on("mouseover", function (event, d) {
        tooltip
          .html(`<strong>${d.label}</strong><br><b>${d.cost} Lakh; ${d.value} %</b>`)
          .style("left", (event.pageX - 120) + "px")
          .style("top", (event.pageY - 90) + "px")
          .classed("visible", true);

        // Highlight hovered and grey out others
        groups.selectAll("circle")
          .transition()
          .duration(300)
          .style("fill", c => c === d ? "#808000" : "#ccc");

        d3.select(this)
          .transition()
          .duration(300)
          .attr("r", radiusScale(d.value) * 1.1);
      })
      .on("mousemove", function (event) {
        tooltip
          .style("left", (event.pageX - 120) + "px")
          .style("top", (event.pageY - 90) + "px");
      })
      .on("mouseout", function (event, d) {
        tooltip.classed("visible", false);

        // Restore original color and size for all
        groups.selectAll("circle")
          .transition()
          .duration(10)
          .style("fill", "#808000")
          .attr("r", c => radiusScale(c.value));
      });

    // Add text labels
    groups.append("text")
      .text(d => d.name)
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .style("fill", "white")
      .style("opacity", 0)
      .style("font-size", "12px")
      .transition()
      .delay((_, i) => i * 300 + 500)
      .duration(700)
      .style("opacity", 1)
      .style("font-size", "18px");

  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto bg-[#f8f1ef] p-6 rounded-lg shadow-lg relative">
      <div className="relative" style={{width: '800px', height: '550px'}}>
        <div ref={chartRef}></div>
        <div className="absolute right-5 bottom-5 text-sm leading-relaxed">
          <div className="text-[#808000] whitespace-nowrap">A - Initial Carbon Emission Cost</div>
          <div className="text-[#808000] whitespace-nowrap">B - Carbon Emission due to Re-Routing</div>
          <div className="text-[#808000] whitespace-nowrap">C - Maintenance Emission Costs</div>
        </div>
      </div>
      <div 
        ref={tooltipRef}
        className="absolute bg-white p-3 rounded-2xl shadow-lg pointer-events-none opacity-0 transition-all duration-300 text-sm border-0"
        style={{
          transform: 'translateY(-10px)',
          zIndex: 1000
        }}
      >
        <style jsx>{`
          .visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
          }
          .tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 10px 10px 0 10px;
            border-style: solid;
            border-color: white transparent transparent transparent;
            filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
          }
          .tooltip strong {
            color: #5c8a00;
            font-size: 16px;
          }
          .tooltip b {
            font-size: 18px;
          }
        `}</style>
      </div>
    </div>
  );
};

export default BubbleChart;