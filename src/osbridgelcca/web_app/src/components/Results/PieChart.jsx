// import React, { useEffect, useRef } from 'react';
// import * as d3 from 'd3';

// const PieChart = () => {
//   const chartRef = useRef();
//   const tooltipRef = useRef();

//   // Hardcoded values converted to lakhs
//   const data = [
//     {
//       label: "Road user cost",
//       cost: 123.93, // 698062500.0 / 100000
//       color: "#FF8C00",
//       disabled: false
//     },
//     {
//       label: "Time cost estimate", 
//       cost: 2.32, // 231856.47562499996 / 100000
//       color: "#483D8B",
//       disabled: false
//     },
//     {
//       label: "Embodied carbon emissions",
//       cost: 8.53, // 852863.5179648 / 100000
//       color: "#B22222",
//       disabled: false
//     },
//     {
//       label: "Initial construction cost",
//       cost: 61.83, // 6182839.35 / 100000
//       color: "#996633",
//       disabled: false
//     },
//     {
//       label: "Additional CO2 e costs due to rerouting",
//       cost:29.04, // 930.652416 / 100000
//       color: "#8B0000",
//       disabled: false
//     },
//     {
//       label: "Periodic Maintenance costs",
//       cost: 1.24, // 112349.87834103756 / 100000
//       color: "#F6FB05",
//       disabled: false
//     },
//     {
//       label: "Periodic maintenance carbon emissions",
//       cost: 16.99, // 2817743.7305447874 / 100000
//       color: "#A52A2A",
//       disabled: false
//     },
//     {
//       label: "Annual routine inspection costs",
//       cost: 12.73, // 45.21627618069613 / 100000
//       color: "#4682B4",
//       disabled: false
//     },
//     {
//       label: "Repair and rehabilitation costs",
//       cost: 1.77, // 2042725.0607461378 / 100000
//       color: "#008000",
//       disabled: false
//     },
//     {
//       label: "Demolition and deconstruction costs",
//       cost:  0.77, // 53916.66345914902 / 100000
//       color: "#800080",
//       disabled: false
//     },
//     {
//       label: "Recycling costs",
//       cost: 0, // 64094739.32469964 / 100000
//       color: "#FFD700",
//       disabled: false
//     },
//     {
//       label: "Total Life Cycle Cost",
//       cost: 259.15, // 61512192.81077006 / 100000
//       color: "#FF4500",
//       disabled: false
//     }
//   ];

//   useEffect(() => {
//     const width = 600;
//     const height = 400;
//     const radius = Math.min(width, height) / 2 - 40;
//     const enlargedRadius = radius * 1.1;

//     // Clear previous chart
//     d3.select(chartRef.current).selectAll("*").remove();
    
//     // Create SVG
//     const svg = d3.select(chartRef.current)
//       .append("svg")
//       .attr("width", width)
//       .attr("height", height)
//       .append("g")
//       .attr("transform", `translate(${width/2},${height/2})`);

//     // Create tooltip
//     const tooltip = d3.select(tooltipRef.current);

//     // Create pie layout
//     const pie = d3.pie()
//       .value(d => d.cost)
//       .sort(null);

//     // Create arc generator
//     const arc = d3.arc()
//       .innerRadius(0)
//       .outerRadius(radius);

//     // Create arc generator for enlarged slices
//     const enlargedArc = d3.arc()
//       .innerRadius(0)
//       .outerRadius(enlargedRadius);

//     let currentData = [...data];

//     // Calculate initial percentages
//     const totalCost = currentData.reduce((sum, d) => sum + d.cost, 0);
//     currentData.forEach(d => {
//       d.percent = (d.cost / totalCost) * 100;
//     });

//     const arcs = pie(currentData);

//     // Arc tween for smooth transitions
//     function arcTween(d) {
//       const interpolate = d3.interpolate(
//         this._current || { startAngle: d.startAngle, endAngle: d.startAngle },
//         d
//       );
//       this._current = interpolate(1);
//       return t => arc(interpolate(t));
//     }

//     // Handle mouseover for slices
//     function handleMouseOver(event, d) {
//       // Enlarge and highlight the hovered slice
//       d3.select(this)
//         .transition()
//         .duration(200)
//         .attr("stroke-width", 2)
//         .attr("fill", d3.color(d.data.color).brighter(0.5))
//         .attr("d", enlargedArc);

//       // Update label position for enlarged slice
//       svg.selectAll(".pie-label")
//         .filter(label => label.data.label === d.data.label)
//         .transition()
//         .duration(200)
//         .attr("transform", `translate(${enlargedArc.centroid(d)})`);

//       // Grey out all other slices
//       svg.selectAll(".arc")
//         .filter(arc => arc.data.label !== d.data.label)
//         .transition()
//         .duration(200)
//         .style("opacity", 0.3)
//         .attr("fill", "#cccccc");

//       // Show tooltip
//       tooltip
//         .html(`
//           <strong>${d.data.label}</strong><br>
//           Cost: ₹${d.data.cost.toFixed(2)}L<br>
//           Percent: ${d.data.percent.toFixed(1)}%
//         `)
//         .style("left", (event.pageX + 10) + "px")
//         .style("top", (event.pageY - 10) + "px")
//         .classed("visible", true);
//     }

//     // Handle mousemove for slices
//     function handleMouseMove(event) {
//       tooltip
//         .style("left", (event.pageX + 10) + "px")
//         .style("top", (event.pageY - 10) + "px");
//     }

//     // Handle mouseout for slices
//     function handleMouseOut() {
//       svg.selectAll(".arc")
//         .transition()
//         .duration(200)
//         .style("opacity", 1)
//         .attr("fill", d => d.data.color)
//         .attr("stroke-width", 1)
//         .attr("d", arc);
      
//       svg.selectAll(".pie-label")
//         .transition()
//         .duration(200)
//         .attr("transform", d => `translate(${arc.centroid(d)})`);
      
//       tooltip.classed("visible", false);
//     }

//     // Create initial arcs
//     svg.selectAll(".arc")
//       .data(arcs)
//       .enter()
//       .append("path")
//       .attr("class", "arc")
//       .attr("fill", d => d.data.color)
//       .attr("stroke", "#fff")
//       .attr("stroke-width", 1)
//       .style("opacity", 0)
//       .each(function(d) {
//         this._current = {
//           startAngle: d.startAngle,
//           endAngle: d.startAngle
//         };
//       })
//       .transition()
//       .duration(800)
//       .ease(d3.easeCubicInOut)
//       .attrTween("d", arcTween)
//       .style("opacity", 1)
//       .on("end", function() {
//         // Add hover events after animation
//         d3.select(this)
//           .on("mouseover", handleMouseOver)
//           .on("mousemove", handleMouseMove)
//           .on("mouseout", handleMouseOut);
//       });

//     // Create initial labels
//     svg.selectAll(".pie-label")
//       .data(arcs)
//       .enter()
//       .append("text")
//       .attr("class", "pie-label")
//       .attr("dy", "0.35em")
//       .attr("text-anchor", "middle")
//       .style("font-weight", "bold")
//       .style("fill", "#fff")
//       .style("opacity", 0)
//       .attr("transform", d => `translate(${arc.centroid(d)})`)
//       .text(d => d.data.percent > 5 ? `${d.data.percent.toFixed(1)}%` : "")
//       .transition()
//       .duration(400)
//       .delay(400)
//       .ease(d3.easeCubicInOut)
//       .style("opacity", 1);

//   }, []);

//   return (
// <div
//   className="w-full max-w-4xl mx-auto p-6 rounded-lg shadow-lg"
//   style={{ backgroundColor: '#f2e8e7' }}
// >

//       <h2 className="text-2xl font-bold text-center mb-6">Life-Cycle Costs for 50 years</h2>
//       <div className="flex flex-col lg:flex-row items-center justify-center">
//         <div ref={chartRef} className="flex-shrink-0"></div>
//         <div className="mt-6 lg:mt-0 lg:ml-8 flex flex-wrap justify-center lg:justify-start">
//           {data.map((item, index) => (
//             <div key={index} className="flex items-center m-2 text-sm">
//               <div 
//                 className="w-4 h-4 mr-2 rounded-sm" 
//                 style={{backgroundColor: item.color}}
//               ></div>
//               <span>{item.label}</span>
//             </div>
//           ))}
//         </div>
//       </div>
//       <div 
//         ref={tooltipRef}
//         className="absolute bg-black bg-opacity-80 text-white p-2 rounded pointer-events-none opacity-0 transition-opacity duration-200 text-xs"
//         style={{position: 'fixed', zIndex: 1000}}
//       ></div>
//     </div>
//   );
// };

// export default PieChart;
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const PieChart = () => {
  const chartRef = useRef();
  const tooltipRef = useRef();

  // Hardcoded values converted to lakhs
  const data = [
    {
      label: "Road user cost",
      cost: 123.93,
      color: "#FF8C00",
      disabled: false
    },
    {
      label: "Time cost estimate", 
      cost: 2.32,
      color: "#483D8B",
      disabled: false
    },
    {
      label: "Embodied carbon emissions",
      cost: 8.53,
      color: "#B22222",
      disabled: false
    },
    {
      label: "Initial construction cost",
      cost: 61.83,
      color: "#996633",
      disabled: false
    },
    {
      label: "Additional CO2 e costs due to rerouting",
      cost: 29.04,
      color: "#8B0000",
      disabled: false
    },
    {
      label: "Periodic Maintenance costs",
      cost: 1.24,
      color: "#F6FB05",
      disabled: false
    },
    {
      label: "Periodic maintenance carbon emissions",
      cost: 16.99,
      color: "#A52A2A",
      disabled: false
    },
    {
      label: "Annual routine inspection costs",
      cost: 12.73,
      color: "#4682B4",
      disabled: false
    },
    {
      label: "Repair and rehabilitation costs",
      cost: 1.77,
      color: "#008000",
      disabled: false
    },
    {
      label: "Demolition and deconstruction costs",
      cost: 0.77,
      color: "#800080",
      disabled: false
    },
    {
      label: "Recycling costs",
      cost: 0,
      color: "#FFD700",
      disabled: false
    },
    {
      label: "Total Life Cycle Cost",
      cost: 259.15,
      color: "#FF4500",
      disabled: false
    }
  ];

  useEffect(() => {
    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();
    
    // Get container dimensions
    const containerRect = chartRef.current.getBoundingClientRect();
    const containerWidth = Math.max(containerRect.width, 400);
    const containerHeight = Math.max(containerRect.height, 300);
    
    const width = Math.min(containerWidth * 0.8, 500);
    const height = Math.min(containerHeight * 0.8, 350);
    const radius = Math.min(width, height) / 2 - 20;
    const enlargedRadius = radius * 1.05;

    // Create SVG
    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", containerWidth)
      .attr("height", containerHeight)
      .append("g")
      .attr("transform", `translate(${containerWidth/2},${containerHeight/2})`);

    // Create tooltip
    const tooltip = d3.select(tooltipRef.current);

    // Create pie layout
    const pie = d3.pie()
      .value(d => d.cost)
      .sort(null);

    // Create arc generator
    const arc = d3.arc()
      .innerRadius(0)
      .outerRadius(radius);

    // Create arc generator for enlarged slices
    const enlargedArc = d3.arc()
      .innerRadius(0)
      .outerRadius(enlargedRadius);

    let currentData = [...data];

    // Calculate initial percentages
    const totalCost = currentData.reduce((sum, d) => sum + d.cost, 0);
    currentData.forEach(d => {
      d.percent = (d.cost / totalCost) * 100;
    });

    const arcs = pie(currentData);

    // Arc tween for smooth transitions
    function arcTween(d) {
      const interpolate = d3.interpolate(
        this._current || { startAngle: d.startAngle, endAngle: d.startAngle },
        d
      );
      this._current = interpolate(1);
      return t => arc(interpolate(t));
    }

    // Handle mouseover for slices
    function handleMouseOver(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr("stroke-width", 2)
        .attr("fill", d3.color(d.data.color).brighter(0.5))
        .attr("d", enlargedArc);

      svg.selectAll(".pie-label")
        .filter(label => label.data.label === d.data.label)
        .transition()
        .duration(200)
        .attr("transform", `translate(${enlargedArc.centroid(d)})`);

      svg.selectAll(".arc")
        .filter(arc => arc.data.label !== d.data.label)
        .transition()
        .duration(200)
        .style("opacity", 0.3)
        .attr("fill", "#cccccc");

      tooltip
        .html(`
          <strong>${d.data.label}</strong><br>
          Cost: ₹${d.data.cost.toFixed(2)}L<br>
          Percent: ${d.data.percent.toFixed(1)}%
        `)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px")
        .classed("visible", true);
    }

    function handleMouseMove(event) {
      tooltip
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
    }

    function handleMouseOut() {
      svg.selectAll(".arc")
        .transition()
        .duration(200)
        .style("opacity", 1)
        .attr("fill", d => d.data.color)
        .attr("stroke-width", 1)
        .attr("d", arc);
      
      svg.selectAll(".pie-label")
        .transition()
        .duration(200)
        .attr("transform", d => `translate(${arc.centroid(d)})`);
      
      tooltip.classed("visible", false);
    }

    // Create initial arcs
    svg.selectAll(".arc")
      .data(arcs)
      .enter()
      .append("path")
      .attr("class", "arc")
      .attr("fill", d => d.data.color)
      .attr("stroke", "#fff")
      .attr("stroke-width", 1)
      .style("opacity", 0)
      .each(function(d) {
        this._current = {
          startAngle: d.startAngle,
          endAngle: d.startAngle
        };
      })
      .transition()
      .duration(800)
      .ease(d3.easeCubicInOut)
      .attrTween("d", arcTween)
      .style("opacity", 1)
      .on("end", function() {
        d3.select(this)
          .on("mouseover", handleMouseOver)
          .on("mousemove", handleMouseMove)
          .on("mouseout", handleMouseOut);
      });

    // Create initial labels
    svg.selectAll(".pie-label")
      .data(arcs)
      .enter()
      .append("text")
      .attr("class", "pie-label")
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .style("font-weight", "bold")
      .style("fill", "#fff")
      .style("font-size", "10px")
      .style("opacity", 0)
      .attr("transform", d => `translate(${arc.centroid(d)})`)
      .text(d => d.data.percent > 3 ? `${d.data.percent.toFixed(1)}%` : "")
      .transition()
      .duration(400)
      .delay(400)
      .ease(d3.easeCubicInOut)
      .style("opacity", 1);

  }, []);

  return (
    <div className="w-full h-full flex flex-col overflow-hidden" style={{ backgroundColor: '#f2e8e7' }}>
      <h2 className="text-lg font-bold text-center py-2 flex-shrink-0">Life-Cycle Costs for 50 years</h2>
      <div className="flex-1 flex items-center justify-center overflow-hidden">
        <div className="w-full h-full flex items-center justify-center">
          <div 
            ref={chartRef} 
            className="w-full h-full max-w-full max-h-full"
            style={{ minHeight: '200px' }}
          ></div>
        </div>
      </div>
      <div 
        ref={tooltipRef}
        className="absolute bg-black bg-opacity-80 text-white p-2 rounded pointer-events-none opacity-0 transition-opacity duration-200 text-xs"
        style={{position: 'fixed', zIndex: 1000}}
      ></div>
    </div>
  );
};

export default PieChart;