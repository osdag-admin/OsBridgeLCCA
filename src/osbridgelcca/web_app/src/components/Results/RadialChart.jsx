import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const RadialChart = ({ 
  data, 
  title, 
  titleColor, 
  tooltipClass, 
  tooltipColorLabel,
  tooltipColor,
  showValueInTooltip = false,
  valueMultiplier = 1,
  decimalPlaces = 1,
  width = 500,
  height = 400,
  barWidth = 20,
  spacing = 10,
  backgroundColor = '#f2e8e7'
}) => {
  const svgRef = useRef();

  useEffect(() => {
    const center = { x: width / 2, y: height / 2 };

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();
    const svg = d3.select(svgRef.current)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .attr("width", "100%")
      .attr("height", "100%");

    const g = svg.append("g")
      .attr("transform", `translate(${center.x},${center.y})`);

    // Create tooltip
    const tooltip = d3.select("body").select(`.${tooltipClass}`);
    let tooltipDiv;
    if (tooltip.empty()) {
      tooltipDiv = d3.select("body").append("div")
        .attr("class", tooltipClass)
        .style("position", "absolute")
        .style("text-align", "center")
        .style("padding", "8px")
        .style("background", "white")
        .style("border-radius", "8px")
        .style("box-shadow", "0 2px 6px rgba(0,0,0,0.2)")
        .style("pointer-events", "none")
        .style("opacity", 0)
        .style("font-size", "14px")
        .style("transform", "translateX(-50%)")
        .style("z-index", "1000");
    } else {
      tooltipDiv = tooltip;
    }

    // Generate arcs
    data.forEach((d, i) => {
      const innerRadius = 50 + i * (barWidth + spacing);
      const outerRadius = innerRadius + barWidth;

      // Arc generator
      const arcGen = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius)
        .startAngle(0)
        .cornerRadius(10);

      // Create path
      const path = g.append("path")
        .datum(d)
        .attr("fill", d.color)
        .attr("d", arcGen({ endAngle: 0 }))
        .attr("class", "arc");

      // Animation
      path.transition()
        .duration(1200)
        .attrTween("d", function(d) {
          const interpolate = d3.interpolate(0, (d.value * 2 * Math.PI) + 0.03);
          return function(t) {
            return arcGen({ endAngle: interpolate(t) });
          };
        });

      // Static percentage labels
      const labelX = center.x - 8;
      const labelY = center.y + (data.length - 1 - i) * (barWidth + spacing) - 150;

      svg.append("text")
        .attr("x", labelX)
        .attr("y", labelY + 5)
        .attr("text-anchor", "end")
        .attr("class", "label")
        .style("font-size", "14px")
        .style("fill", "#333")
        .text(`${(d.value * 100).toFixed(decimalPlaces)}%`);

      // Hover events
      path.on("mouseover", function(event, hoveredData) {
        d3.selectAll(".arc")
          .attr("fill", p => p === hoveredData ? p.color : "#ccc");

        const tooltipContent = showValueInTooltip ? 
          `
            <div style="text-align:center; font-family:sans-serif;">
              <span style="font-weight: 500;">${hoveredData.name}</span>
              <br>
              <span style="color: ${tooltipColor}; font-size: 13.5px;">
                ${tooltipColorLabel}: 
                <span style="font-weight: 600;">
                  ${(hoveredData.value * 100).toFixed(1)}%;
                  ${(hoveredData.value * valueMultiplier).toFixed(2)}
                </span>
              </span>
              <br>
              <span style="font-weight: bold; color: ${tooltipColor};">Lakhs</span>
            </div>
          ` :
          `
            <div style="text-align:center; font-family:sans-serif;">
              <span style="font-weight: 500;">${hoveredData.name}</span>
              <br>
              <span style="color: ${tooltipColor}; font-size: 13.5px;">
                ${tooltipColorLabel}: 
                <span style="font-weight: 600;">
                  ${(hoveredData.value * 100).toFixed(decimalPlaces)}%
                </span>
              </span>
            </div>
          `;

        tooltipDiv.style("opacity", 1)
          .html(tooltipContent)
          .style("left", (event.pageX) + "px")
          .style("top", (event.pageY - 50) + "px");
      })
      .on("mousemove", function(event) {
        tooltipDiv.style("left", (event.pageX) + "px")
          .style("top", (event.pageY - 70) + "px");
      })
      .on("mouseout", function() {
        d3.selectAll(".arc")
          .attr("fill", d => d.color);
        tooltipDiv.style("opacity", 0);
      });
    });

  }, [data, title, titleColor, tooltipClass, tooltipColorLabel, tooltipColor, showValueInTooltip, valueMultiplier, decimalPlaces, width, height, barWidth, spacing]);

  return (
    <div className="w-full h-full">
      <div style={{ 
        background: backgroundColor, 
        fontFamily: 'sans-serif', 
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'flex-start', 
        alignItems: 'center', 
        height: '100%',
        margin: 0 
      }}>
        <h2 className="font-bold" style={{ 
          marginTop: '20px', 
          marginBottom: '10px', 
          fontSize: '10px', 
          textAlign: 'center'
        }}>
          <span style={{ color: titleColor }}>{title.split(' ')[0]} {title.split(' ')[1]}</span> {title.split(' ').slice(2).join(' ')}
        </h2>
        <svg ref={svgRef} className="w-full h-full"></svg>
      </div>
    </div>
  );
};

export default RadialChart;