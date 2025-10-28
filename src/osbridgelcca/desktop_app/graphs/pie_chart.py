import pandas as pd
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QSize

# using the d3js graphing library to plot the graph, it is downloaded locally and saved in the same directory as that of this graph script
with open(r"..\dependencies\d3js.js", "r", encoding="utf-8") as f:
    d3_js = f.read()

class D3PieChartViewer(QMainWindow):
    def __init__(self, data_js):
        super().__init__()
        self.setWindowTitle("Cost Breakdown Pie Chart")
        self.setMinimumSize(QSize(800, 600))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        # Generate HTML content
        html_content = self.generate_html(data_js)
        
        # Load the HTML content
        self.web_view.setHtml(html_content, QUrl.fromLocalFile(""))
        
    def generate_html(self, data_js):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cost Breakdown Pie Chart</title>
            <script>{d3_js}</script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                .chart-container {{
                    width: 100%;
                    max-width: 800px;
                    margin: 0 auto;
                }}
                .pie-label {{
                    font-size: 12px;
                    fill: #333;
                }}
                .legend-item {{
                    font-size: 12px;
                    display: flex;
                    align-items: center;
                    margin: 5px 10px;
                    cursor: pointer;
                }}
                .title {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .legend {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    margin-top: 20px;
                }}
                .legend-color {{
                    width: 15px;
                    height: 15px;
                    margin-right: 8px;
                    display: inline-block;
                }}
                .strikethrough {{
                    position: relative;
                    color: #999;
                }}
                .strikethrough::after {{
                    content: "";
                    position: absolute;
                    left: 0;
                    top: 50%;
                    width: 100%;
                    height: 1px;
                    background: black;
                }}
                .tooltip {{
                    position: absolute;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.2s ease;
                }}
                .tooltip.visible {{
                    opacity: 1;
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                <h2 class="title">Cost Breakdown (in Lakhs)</h2>
                <div id="chart"></div>
                <div id="legend" class="legend"></div>
            </div>
            
            <script>
                // Data from Python with specific colors
                const originalData = {data_js};
                let currentData = JSON.parse(JSON.stringify(originalData));
                
                // Chart dimensions
                const width = 600;
                const height = 400;
                const radius = Math.min(width, height) / 2 - 40;
                const enlargedRadius = radius * 1.1;
                
                // Create SVG
                const svg = d3.select("#chart")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g")
                    .attr("transform", `translate(${{width/2}},${{height/2}})`);
                
                // Create tooltip
                const tooltip = d3.select("body")
                    .append("div")
                    .attr("class", "tooltip");
                
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
                
                // Arc tween for smooth transitions
                function arcTween(d, i) {{
                    const interpolate = d3.interpolate(
                        this._current || {{ startAngle: d.startAngle, endAngle: d.startAngle }},
                        d
                    );
                    this._current = interpolate(1);
                    return t => arc(interpolate(t));
                }}
                
                // Arc tween for exit animation
                function arcTweenExit(d) {{
                    const interpolate = d3.interpolate(d, {{
                        startAngle: d.endAngle,
                        endAngle: d.endAngle
                    }});
                    return t => arc(interpolate(t));
                }}
                
                // Reset hover state
                function resetHoverState() {{
                    svg.selectAll(".arc")
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .attr("fill", arc => arc.data.color)
                        .attr("stroke-width", 1)
                        .attr("d", arc);
                    svg.selectAll(".pie-label")
                        .transition()
                        .duration(200)
                        .attr("transform", d => `translate(${{arc.centroid(d)}})`);
                    tooltip.classed("visible", false);
                }}
                
                // Function to update the pie chart
                function updatePieChart() {{
                    // Filter out disabled items
                    const activeData = currentData.filter(d => !d.disabled);
                    
                    // Calculate new percentages
                    const totalActiveCost = activeData.reduce((sum, d) => sum + d.cost, 0);
                    activeData.forEach(d => {{
                        d.percent = (d.cost / totalActiveCost) * 100;
                    }});
                    
                    // Update pie with new data
                    const arcs = pie(activeData);
                    
                    // Join new data with existing paths
                    const paths = svg.selectAll(".arc")
                        .data(arcs, d => d.data.label);
                    
                    // Handle exiting slices
                    paths.exit()
                        .transition()
                        .duration(400)
                        .ease(d3.easeCubicInOut)
                        .attrTween("d", arcTweenExit)
                        .style("opacity", 0)
                        .remove();
                    
                    // Update existing slices
                    paths.transition()
                        .duration(600)
                        .ease(d3.easeCubicInOut)
                        .attrTween("d", arcTween)
                        .attr("fill", d => d.data.color);
                    
                    // Add new slices
                    paths.enter()
                        .append("path")
                        .attr("class", "arc")
                        .attr("fill", d => d.data.color)
                        .attr("stroke", "#fff")
                        .attr("stroke-width", 1)
                        .style("opacity", 0)
                        .each(function(d) {{ this._current = d; }})
                        .transition()
                        .duration(600)
                        .ease(d3.easeCubicInOut)
                        .attrTween("d", arcTween)
                        .style("opacity", 1)
                        .on("end", function() {{
                            // Add hover events after animation
                            d3.select(this)
                                .on("mouseover", handleMouseOver)
                                .on("mousemove", handleMouseMove)
                                .on("mouseout", handleMouseOut);
                        }});
                    
                    // Update labels
                    const labels = svg.selectAll(".pie-label")
                        .data(arcs, d => d.data.label);
                    
                    labels.exit()
                        .transition()
                        .duration(200)
                        .style("opacity", 0)
                        .remove();
                    
                    labels.enter()
                        .append("text")
                        .attr("class", "pie-label")
                        .attr("dy", "0.35em")
                        .attr("text-anchor", "middle")
                        .style("font-weight", "bold")
                        .style("fill", "#fff")
                        .style("opacity", 0)
                        .merge(labels)
                        .transition()
                        .duration(400)
                        .ease(d3.easeCubicInOut)
                        .attr("transform", d => `translate(${{arc.centroid(d)}})`)
                        .text(d => d.data.percent > 5 ? `${{d.data.percent.toFixed(1)}}%` : "")
                        .style("opacity", 1);
                    
                    // Update legend percentages
                    d3.selectAll(".legend-text")
                        .text(d => `${{d.label}} (₹${{d.cost.toFixed(2)}}L, ${{d.percent.toFixed(1)}}%)`);
                }}
                
                // Handle mouseover for slices
                function handleMouseOver(event, d) {{
                    // Enlarge and highlight the hovered slice
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("stroke-width", 2)
                        .attr("fill", d3.color(d.data.color).brighter(0.5))
                        .attr("d", enlargedArc);
                    
                    // Update label position for enlarged slice
                    svg.selectAll(".pie-label")
                        .filter(label => label.data.label === d.data.label)
                        .transition()
                        .duration(200)
                        .attr("transform", `translate(${{enlargedArc.centroid(d)}})`);
                    
                    // Grey out all other slices
                    svg.selectAll(".arc")
                        .filter(arc => arc.data.label !== d.data.label)
                        .transition()
                        .duration(200)
                        .style("opacity", 0.3)
                        .attr("fill", "#cccccc");
                    
                    // Show tooltip
                    tooltip
                        .html(`
                            <strong>${{d.data.label}}</strong><br>
                            Cost: ₹${{d.data.cost.toFixed(2)}}L<br>
                            Percent: ${{d.data.percent.toFixed(1)}}%
                        `)
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 10) + "px")
                        .classed("visible", true);
                }}
                
                // Handle mousemove for slices
                function handleMouseMove(event, d) {{
                    tooltip
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 10) + "px");
                }}
                
                // Handle mouseout for slices
                function handleMouseOut(event, d) {{
                    resetHoverState();
                }}
                
                // Initialize the chart
                function initializeChart() {{
                    // Calculate initial percentages
                    const totalCost = currentData.reduce((sum, d) => sum + d.cost, 0);
                    currentData.forEach(d => {{
                        d.percent = (d.cost / totalCost) * 100;
                    }});
                    
                    const arcs = pie(currentData);
                    
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
                        .each(function(d) {{
                            this._current = {{
                                startAngle: d.startAngle,
                                endAngle: d.startAngle
                            }};
                        }})
                        .transition()
                        .duration(800)
                        .ease(d3.easeCubicInOut)
                        .attrTween("d", arcTween)
                        .style("opacity", 1)
                        .on("end", function() {{
                            // Add hover events after animation
                            d3.select(this)
                                .on("mouseover", handleMouseOver)
                                .on("mousemove", handleMouseMove)
                                .on("mouseout", handleMouseOut);
                        }});
                    
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
                        .style("opacity", 0)
                        .attr("transform", d => `translate(${{arc.centroid(d)}})`)
                        .text(d => d.data.percent > 5 ? `${{d.data.percent.toFixed(1)}}%` : "")
                        .transition()
                        .duration(400)
                        .delay(400)
                        .ease(d3.easeCubicInOut)
                        .style("opacity", 1);
                    
                    // Create legend
                    const legend = d3.select("#legend")
                        .selectAll(".legend-item")
                        .data(currentData)
                        .enter()
                        .append("div")
                        .attr("class", "legend-item")
                        .attr("id", d => `legend-item-${{d.label.replace(/\\s+/g, '-')}}`);
                    
                    legend.append("div")
                        .attr("class", "legend-color")
                        .style("background-color", d => d.color);
                    
                    legend.append("span")
                        .text(d => `${{d.label}} (₹${{d.cost.toFixed(2)}}L, ${{d.percent.toFixed(1)}}%)`)
                        .style("margin-left", "5px")
                        .attr("class", "legend-text");
                    
                    // Add interactivity
                    legend.on("click", function(event, d) {{
                        // Reset hover state before toggling
                        resetHoverState();
                        
                        // Toggle the item
                        toggleItem(d);
                        
                        // Prevent event propagation
                        event.stopPropagation();
                    }});
                    
                    // Add hover effects for legend
                    legend.on("mouseover", function(event, d) {{
                        if (!d.disabled) {{
                            // Highlight the corresponding slice
                            svg.selectAll(".arc")
                                .filter(arc => arc.data.label === d.label)
                                .attr("stroke-width", 2)
                                .attr("fill", d3.color(d.color).brighter(0.5));
                            
                            // Get the centroid of the slice
                            const arcData = svg.selectAll(".arc")
                                .filter(arc => arc.data.label === d.label)
                                .data()[0];
                            
                            if (arcData) {{
                                // Calculate the centroid position
                                const centroid = arc.centroid(arcData);
                                
                                // Get the SVG's position on the page
                                const svgRect = svg.node().parentNode.getBoundingClientRect();
                                
                                // Calculate the absolute position of the centroid
                                const centroidX = svgRect.left + width/2 + centroid[0];
                                const centroidY = svgRect.top + height/2 + centroid[1];
                                
                                // Show tooltip at the centroid position
                                tooltip
                                    .html(`
                                        <strong>${{d.label}}</strong><br>
                                        Cost: ₹${{d.cost.toFixed(2)}}L<br>
                                        Percent: ${{d.percent.toFixed(1)}}%
                                    `)
                                    .style("left", (centroidX + 10) + "px")
                                    .style("top", (centroidY - 30) + "px")
                                    .classed("visible", true);
                            }}
                        }}
                    }})
                    .on("mouseout", function(event, d) {{
                        if (!d.disabled) {{
                            // Reset highlight on the slice
                            svg.selectAll(".arc")
                                .filter(arc => arc.data.label === d.label)
                                .attr("stroke-width", 1)
                                .attr("fill", arc => arc.data.color);
                            
                            // Hide tooltip
                            tooltip.classed("visible", false);
                        }}
                    }});
                    
                    // Add click handler to SVG to reset hover state
                    svg.on("click", function(event) {{
                        resetHoverState();
                    }});
                }}
                
                // Function to toggle item state
                function toggleItem(item) {{
                    const index = currentData.findIndex(d => d.label === item.label);
                    if (index !== -1) {{
                        currentData[index].disabled = !currentData[index].disabled;
                        
                        const legendItem = d3.select(`#legend-item-${{item.label.replace(/\\s+/g, '-')}}`);
                        if (currentData[index].disabled) {{
                            legendItem.select(".legend-text").classed("strikethrough", true);
                        }} else {{
                            legendItem.select(".legend-text").classed("strikethrough", false);
                        }}
                        
                        updatePieChart();
                    }}
                }}
                
                // Start the chart
                initializeChart();
            </script>
        </body>
        </html>
        """
        return html

def main():
    print("generating graph")
    FILE_PATH = r"data1.csv"

    # --- Read CSV and Extract Data ---
    try:
        df = pd.read_csv(FILE_PATH)
        if df.empty:
            print(f"Warning: CSV file '{FILE_PATH}' is empty.")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{FILE_PATH}'.")
        df = pd.DataFrame()
    except Exception as e:
        print(f"Error reading CSV: {e}")
        df = pd.DataFrame()

    # Define labels and their specific colors
    label_colors = {
        "Road user cost": "#FF8C00",              
        "Time cost estimate": "#483D8B",          
        "Embodied carbon emissions": "#B22222",    
        "Initial construction cost": "#996633",    
        "Additional CO2 e costs due to rerouting": "#8B0000",  
        "Periodic Maintenance costs": "#F6FB05",  
        "Periodic maintenance carbon emissions": "#A52A2A",
        "Annual routine inspection costs": "#4682B4",  
        "Repair and rehabilitation costs": "#008000",  
        "Demolition and deconstruction costs": "#800080"
    }

    # Extract data
    values_dict = {}
    for item in label_colors.keys():
        found_value = False
        if not df.empty:
            for _, row in df.iterrows():
                row_list = [str(x) for x in row.values]
                if item in row_list:
                    idx = row_list.index(item)
                    if idx + 1 < len(row_list):
                        values_dict[item] = row_list[idx + 1]
                        found_value = True
                        break
        if not found_value:
            values_dict[item] = "0.0"

    cost_list = []
    for key in label_colors.keys():
        try:
            cost_list.append(float(values_dict.get(key, "0.0")))
        except:
            cost_list.append(0.0)

    total_cost = sum(cost_list)
    percentage_list = [(v / total_cost) * 100 if total_cost else 0 for v in cost_list]
    cost_list_lakhs = [v / 100000 for v in cost_list]

    # Create data with specific color mapping
    data_with_colors = [
        {
            "label": name,
            "cost": cost,
            "percent": percent,
            "color": label_colors[name],
            "disabled": False
        }
        for name, cost, percent in zip(label_colors.keys(), cost_list_lakhs, percentage_list)
    ]

    data_js = json.dumps(data_with_colors)

    # Create and show the application window
    app = QApplication([])
    viewer = D3PieChartViewer(data_js)
    viewer.show()
    app.exec()

if __name__ == "__main__":
    main()