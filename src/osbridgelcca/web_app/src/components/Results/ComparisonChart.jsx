import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const ComparisonChart = () => {
  const svgRef = useRef();

  useEffect(() => {
    // Hardcoded data based on your values (converted to lakhs)
    const data = [
      {
        label: "Initial Construction Cost",
        psc: 61.83,
        steel: 58.45
      },
      {
        label: "Initial Carbon Emission Cost", 
        psc: 8.53,
        steel: 7.92
      },
      {
        label: "Time Cost",
        psc: 2.32,
        steel: 2.18
      },
      {
        label: "Road User Cost",
        psc: 6980.63,
        steel: 6580.25
      },
      {
        label: "Carbon Emission due to Re-Routing",
        psc: 0.01,
        steel: 0.009
      },
      {
        label: "Periodic Maintenance Costs",
        psc: 1.12,
        steel: 1.05
      },
      {
        label: "Maintenance Emission Cost",
        psc: 28.18,
        steel: 26.42
      },
      {
        label: "Routine Inspection Cost",
        psc: 0.0005,
        steel: 0.0004
      },
      {
        label: "Repair & Rehabilitation Cost",
        psc: 20.43,
        steel: 18.95
      },
      {
        label: "Demolition & Disposal Cost",
        psc: 0.54,
        steel: 0.48
      },
      {
        label: "Recycling Cost",
        psc: 640.95,
        steel: 595.12
      },
      {
        label: "Total Life-Cycle Cost",
        psc: 7744.64,
        steel: 7291.42
      }
    ];

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();

    const margin = { top: 60, right: 130, bottom: 50, left: 280 };
    const width = 1000 - margin.left - margin.right;
    const barHeight = 18;
    const categoryGap = 15;
    const barGap = 2;
    const height = data.length * (barHeight * 2 + barGap + categoryGap) + margin.top + margin.bottom;

    const svg = d3.select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height)
      .style("background-color", "#f8eaea");

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Find min and max values
    const minValue = d3.min(data, d => Math.min(d.psc, d.steel));
    const maxValue = d3.max(data, d => Math.max(d.psc, d.steel));

    const x = d3.scaleLinear()
      .domain([minValue * 1.1, maxValue * 1.1])
      .nice()
      .range([0, width]);

    const y = d3.scaleBand()
      .domain(data.map(d => d.label))
      .range([0, height - margin.top - margin.bottom])
      .padding(0.4);

    // Add y-axis
    g.append("g")
      .call(d3.axisLeft(y).tickSize(0))
      .selectAll(".domain").remove();

    // Add x-axis
    g.append("g")
      .attr("transform", `translate(0, ${height - margin.top - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(10).tickFormat(d => d + " Lakh"));

    // Add vertical zero line
    g.append("line")
      .attr("x1", x(0))
      .attr("x2", x(0))
      .attr("y1", 0)
      .attr("y2", height - margin.top - margin.bottom)
      .attr("stroke", "#000")
      .attr("stroke-width", 1);

    // Create tooltip
    const tooltip = d3.select("body").select(".comparison-tooltip");
    let tooltipDiv;
    if (tooltip.empty()) {
      tooltipDiv = d3.select("body").append("div")
        .attr("class", "comparison-tooltip")
        .style("position", "absolute")
        .style("background-color", "#fff")
        .style("padding", "8px 12px")
        .style("border-radius", "5px")
        .style("box-shadow", "0 0 10px rgba(0,0,0,0.2)")
        .style("font-size", "14px")
        .style("pointer-events", "none")
        .style("opacity", 0)
        .style("z-index", "10")
        .style("transition", "none");
    } else {
      tooltipDiv = tooltip;
    }

    const colors = {
      psc: "#87cefa",
      steel: "#8b0000"
    };

    function showTooltip(event, label, value, type) {
      tooltipDiv
        .html(`<strong>${label} (${type === 'psc' ? 'PSC' : 'Steel'})</strong>: ${value} Lakh`)
        .style("left", (event.pageX - 150) + "px")
        .style("top", (event.pageY - 50) + "px")
        .style("opacity", 1);
    }

    function hideTooltip() {
      tooltipDiv.style("opacity", 0);
    }

    function getBarYPosition(d, barIndex) {
      return y(d.label) + barIndex * (barHeight + barGap);
    }

    // Draw bars for PSC Bridge with animation
    g.selectAll(".bar-psc")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar-psc")
      .attr("x", x(0))
      .attr("y", d => getBarYPosition(d, 0))
      .attr("width", 0)
      .attr("height", barHeight)
      .attr("fill", colors.psc)
      .attr("rx", 3)
      .attr("ry", 3)
      .on("mousemove", function(event, d) {
        showTooltip(event, d.label, d.psc, 'psc');
        d3.select(this).attr("fill", "#4682b4");
      })
      .on("mouseleave", function() {
        hideTooltip();
        d3.select(this).attr("fill", colors.psc);
      })
      .transition()
      .duration(1000)
      .delay((d, i) => i * 100)
      .attr("x", d => x(Math.min(0, d.psc)))
      .attr("width", d => Math.abs(x(d.psc) - x(0)));

    // Draw bars for Steel Bridge with animation
    g.selectAll(".bar-steel")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar-steel")
      .attr("x", x(0))
      .attr("y", d => getBarYPosition(d, 1))
      .attr("width", 0)
      .attr("height", barHeight)
      .attr("fill", colors.steel)
      .attr("rx", 3)
      .attr("ry", 3)
      .on("mousemove", function(event, d) {
        showTooltip(event, d.label, d.steel, 'steel');
        d3.select(this).attr("fill", "#a52a2a");
      })
      .on("mouseleave", function() {
        hideTooltip();
        d3.select(this).attr("fill", colors.steel);
      })
      .transition()
      .duration(1000)
      .delay((d, i) => i * 100)
      .attr("x", d => x(Math.min(0, d.steel)))
      .attr("width", d => Math.abs(x(d.steel) - x(0)));

    // Add value labels for PSC Bridge
    g.selectAll(".label-psc")
      .data(data)
      .enter()
      .append("text")
      .attr("class", "label-psc")
      .attr("x", d => d.psc >= 0 ? x(d.psc) + 5 : x(d.psc) - 5)
      .attr("y", d => getBarYPosition(d, 0) + barHeight / 2 + 4)
      .text(d => d.psc + " Lakh")
      .attr("font-size", "12px")
      .attr("fill", "black")
      .attr("text-anchor", d => d.psc >= 0 ? "start" : "end");

    // Add value labels for Steel Bridge
    g.selectAll(".label-steel")
      .data(data)
      .enter()
      .append("text")
      .attr("class", "label-steel")
      .attr("x", d => d.steel >= 0 ? x(d.steel) + 5 : x(d.steel) - 5)
      .attr("y", d => getBarYPosition(d, 1) + barHeight / 2 + 4)
      .text(d => d.steel + " Lakh")
      .attr("font-size", "12px")
      .attr("fill", "black")
      .attr("text-anchor", d => d.steel >= 0 ? "start" : "end");

    // Legend
    const legend = g.append("g")
      .attr("transform", `translate(${width - 140}, -40)`);

    legend.append("rect")
      .attr("x", 0)
      .attr("width", 20)
      .attr("height", 20)
      .attr("fill", colors.psc)
      .attr("rx", 3)
      .attr("ry", 3);

    legend.append("text")
      .attr("x", 30)
      .attr("y", 15)
      .text("PSC Bridge")
      .style("font-size", "14px");

    legend.append("rect")
      .attr("x", 130)
      .attr("width", 20)
      .attr("height", 20)
      .attr("fill", colors.steel)
      .attr("rx", 3)
      .attr("ry", 3);

    legend.append("text")
      .attr("x", 160)
      .attr("y", 15)
      .text("Steel Bridge")
      .style("font-size", "14px");

    // Add title
    g.append("text")
      .attr("x", width / 2)
      .attr("y", -20)
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .style("font-weight", "bold")
      .text("Bridge Life-Cycle Cost Comparison");

  }, []);

  return (
    <div className="w-full h-full" style={{ background: '#f8eaea' }}>
      <svg ref={svgRef} className="w-full h-full"></svg>
    </div>
  );
};

export default ComparisonChart;