import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import copy

FILE_PATH = r"data.csv"
df = pd.read_csv(FILE_PATH)

# using the d3js graphing library to plot the graph, it is downloaded locally and saved in the same directory as that of this graph script
with open(r"..\dependencies\d3js.js", "r", encoding="utf-8") as f:
    d3_js = f.read()


# Extract names and costs
name = []
cost = []
for ___, row in df.iterrows():
    for index, i in enumerate(row):
        if index == 2:
            name.append(i)
        elif index == 3:
            cost.append(i)

# Clean data
temp_name = []
temp_cost = []
for index, i in enumerate(cost):
    if isinstance(i, float):
        temp_name = name[1:index]
        temp_cost = cost[1:index]
        break

# Normalize costs to Lakhs
for i in range(len(temp_cost)):
    temp_cost[i] = float(temp_cost[i]) / 100000.0

# Display adjustment for zero values
temp_cost_display = []
cost_list = copy.deepcopy(temp_cost)
cost_list.remove(min(temp_cost))
for j in temp_cost:
    if j == 0.0:
        temp_cost_display.append(min(cost_list) / 2)
    else:
        temp_cost_display.append(j)

# Styling
color_list = ['#638B48', '#6F6F6F', '#638B48', '#E09365', '#6F6F6F', '#638B48',
              '#6F6F6F', '#638B48', '#638B48', '#638B48', '#638B48', '#ffffff']


# Embed values into HTML string using f-string
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>D3.js Interactive Horizontal Bar Graph</title>
    <script>{d3_js}</script>
    <style>
        /* General body styling */
        body {{
            font-family: Arial, sans-serif;
        }}

        /* Container for the graph, centers it on the page */
        #myGraph {{
            width: 80%;
            margin: auto;
            position: relative; /* Essential for positioning the tooltip absolutely within this div */
        }}

        /* Styling for individual bar elements */
        .bar {{
            transition: fill 0.3s ease; /* Provides a smooth color transition on hover */
        }}

        /* Styling for axis text labels (e.g., tick values) */
        .axis text {{
            font-size: 11px;
            fill: #333; /* Dark grey color for readability */
        }}

        /* Styling for axis lines and paths (omitting fill, using stroke for lines) */
        .axis path,
        .axis line {{
            fill: none;
            stroke: #ccc; /* Light grey stroke for a subtle appearance */
            shape-rendering: crispEdges; /* Ensures lines appear sharp, not blurry */
        }}

        /* Styling for the custom tooltip that appears on hover */
        .tooltip {{
            position: absolute; /* Allows precise positioning relative to the graph container */
            text-align: center;
            padding: 8px;
            font-size: 12px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            pointer-events: none; /* Prevents the tooltip from blocking mouse events on elements beneath it */
            color: black;
            opacity: 0; /* Initially hidden, fades in on hover */
            transition: opacity 0.2s; /* Smooth fade in/out effect */
            white-space: nowrap; /* Ensures the tooltip text stays on a single line */
        }}

        /* CSS for creating the triangular spike (arrow) at the bottom of the tooltip */
        .tooltip::after {{
            content: ''; /* Required for pseudo-elements */
            position: absolute;
            left: 50%; /* Centers the spike horizontally under the tooltip */
            top: 100%; /* Positions the spike's base at the very bottom of the tooltip box */
            width: 0;
            height: 0;
            border-left: 8px solid transparent; /* Creates the left half of the triangle */
            border-right: 8px solid transparent; /* Creates the right half of the triangle */
            border-top: 8px solid white; /* Forms the white body of the triangle, matching tooltip background */
            transform: translateX(-50%); /* Adjusts horizontal position to perfectly center the spike */
            z-index: 1; /* Ensures the spike is on top of other elements if they overlap */
        }}

        /* Styling for bar labels (names displayed on or next to bars) */
        .bar-label {{
            user-select: none;         /* Prevents the text from being selected by the user */
            -moz-user-select: none;    /* Firefox specific prefix for user-select */
            -webkit-user-select: none; /* Chrome, Safari specific prefix for user-select */
            -ms-user-select: none;     /* IE/Edge specific prefix for user-select */
        }}
    </style>
</head>
<body>

<h2 style="text-align: center;">Life Cycle Cost for 50 Years</h2>
<div id="myGraph"></div>

<script>
    // Original dataset containing names, values (scores), and their corresponding colors.
    const originalData = [
        {{ name: '{temp_name[0]}', value: {temp_cost_display[0]}, color: '{color_list[0]}' }},
        {{ name: '{temp_name[1]}', value: {temp_cost_display[1]}, color: '{color_list[1]}' }},
        {{ name: '{temp_name[2]}', value: {temp_cost_display[2]}, color: '{color_list[2]}' }},
        {{ name: '{temp_name[3]}', value: {temp_cost_display[3]}, color: '{color_list[3]}' }},
        {{ name: '{temp_name[4]}', value: {temp_cost_display[4]}, color: '{color_list[4]}' }},
        {{ name: '{temp_name[5]}', value: {temp_cost_display[5]}, color: '{color_list[5]}' }},
        {{ name: '{temp_name[6]}', value: {temp_cost_display[6]}, color: '{color_list[6]}' }},
        {{ name: '{temp_name[7]}', value: {temp_cost_display[7]}, color: '{color_list[7]}' }},
        {{ name: '{temp_name[8]}', value: {temp_cost_display[8]}, color: '{color_list[8]}' }},
        {{ name: '{temp_name[9]}', value: {temp_cost_display[9]}, color: '{color_list[9]}' }},
        {{ name: '{temp_name[10]}', value: {temp_cost_display[10]}, color: '{color_list[10]}' }},
        {{ name: '{temp_name[11]}', value: {temp_cost_display[11]}, color: '{color_list[11]}' }},
    ];

    // Create a reversed copy of the data for plotting, so the first item appears at the bottom.
    const data = [...originalData].reverse();
    // Define a dim color to be used for non-hovered bars.
    const dimColor = 'rgba(200,200,200,0.4)';

    // Define margins for the chart to create space around the plot area.
    const margin = {{ top: 50, right: 60, bottom: 50, left: 100 }};
    // Select the main graph container div.
    const myGraphDiv = d3.select("#myGraph");
    // Calculate the width of the graph div to make the chart responsive.
    const divWidth = myGraphDiv.node().getBoundingClientRect().width;
    // Calculate the inner width of the chart (excluding margins).
    const width = divWidth - margin.left - margin.right;

    // Define the desired height for each bar, including its padding.
    const itemHeight = 30;
    // Set a minimum inner chart height to prevent the chart from collapsing for very few items.
    const minChartHeight = 200;
    // Calculate the chart's inner height based on the number of data items.
    const calculatedChartHeight = data.length * itemHeight;
    // Ensure the chart's height is at least the minimum height.
    const height = Math.max(minChartHeight, calculatedChartHeight);

    // Append the SVG element to the graph container.
    const svg = myGraphDiv
        .append("svg")
        .attr("width", width + margin.left + margin.right) // Set total SVG width
        .attr("height", height + margin.top + margin.bottom) // Set total SVG height dynamically
        .style("background-color", "#F0E6E6") // Set the background color for the entire SVG (paper_bgcolor)
        .append("g") // Append a group element to contain the chart elements
        .attr("transform", `translate(${{margin.left}},${{margin.top}})`); // Translate to apply margins

    // Draw a rectangle for the plot background (plot_bgcolor).
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "#F0E6E6"); // Set the background color for the main plotting area

    // Define the x-axis scale (for values/scores).
    const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) * 1.1]) // Domain from 0 to max value with 10% extra space for labels
        .range([0, width]); // Maps domain values to pixel range

    // Define the y-axis scale (for names/categories).
    const y = d3.scaleBand()
        .domain(data.map(d => d.name)) // Domain uses the names from the data
        .range([height, 0]) // Maps domain to pixel range (from bottom to top)
        .paddingInner(0.2); // Adds padding between bars to increase distance

    // Add the X-axis to the SVG.
    svg.append("g")
        .attr("class", "x axis") // Assigns a CSS class for styling
        .attr("transform", `translate(0,${{height}})`) // Positions the axis at the bottom of the chart
        .style("opacity", 0) // Start with opacity 0
        .call(d3.axisBottom(x)) // Calls the D3 axis generator
        .append("text") // Append text for the X-axis title
        .attr("x", width / 2) // Center the title horizontally
        .attr("y", 40) // Position below the axis line
        .attr("fill", "black")
        .attr("text-anchor", "middle") // Anchors the text in the middle
        .style("font-size", "16px") // Set font size for the title
        .text("Cost in Lakhs"); // Set the text content for the X-axis title

    // Add the Y-axis to the SVG.
    svg.append("g")
        .attr("class", "y axis") // Assigns a CSS class for styling
        .style("opacity", 0) // Start with opacity 0
        .call(d3.axisLeft(y)) // Calls the D3 axis generator
        .append("text") // Append text for the Y-axis title
        .attr("transform", "rotate(-90)") // Rotates the title vertically
        .attr("y", -60) // Positions the title to the left of the axis
        .attr("x", -(height / 2)) // Centers the title vertically on the axis
        .attr("dy", "1em") // Adjusts vertical position slightly
        .attr("fill", "black")
        .attr("text-anchor", "middle") // Anchors the text in the middle
        .style("font-size", "16px") // Set font size for the title
        .text(""); // Set the text content for the Y-axis title

    // Remove Y-axis tick labels, keeping only the Y-axis title.
    svg.select(".y.axis").selectAll("text").filter(function() {{
        return d3.select(this).text() !== "Name"; // Selects all text elements except the "Name" title
    }}).remove(); // Removes the selected tick labels
    svg.select(".y.axis").selectAll("line").remove(); // Also remove the tick lines from the Y-axis

    // Create a div element for the custom tooltip.
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip"); // Assigns a CSS class for styling

    // Create the horizontal bars for the chart.
    const bars = svg.selectAll(".bar")
        .data(data) // Binds data to the rect elements
        .enter() // Enters for new data points
        .append("rect") // Appends a rectangle for each data point
        .attr("class", "bar") // Assigns a CSS class for styling
        .attr("x", 0) // Sets the x-position of the bar (starts from left)
        .attr("y", d => y(d.name)) // Sets the y-position based on the band scale
        .attr("width", 0) // Start with width 0
        .attr("height", y.bandwidth()) // Sets the height based on the band scale
        .attr("fill", d => d.color); // Sets the initial fill color of the bar

    // Define padding for text positioning calculations within/outside bars.
    const textPadding = 5;

    // Add text labels on the bars (names).
    const textLabels = svg.selectAll(".bar-label")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "bar-label") // Assigns a CSS class for styling and interaction
        .attr("y", d => y(d.name) + y.bandwidth() / 2) // Centers the text vertically within the bar
        .attr("dy", "0.35em") // Adjusts vertical alignment for perfect centering
        .style("font-family", "Arial, sans-serif")
        .style("font-size", "12px")
        .style("text-anchor", "start") // Aligns text to the start (left)
        .style("opacity", 0) // Start with opacity 0
        .text(d => d.name); // Sets the text content to the name

    // Animate the bars growing from left to right
    bars.transition()
        .duration(1500) // Animation duration in milliseconds
        .ease(d3.easeElastic.amplitude(0.5).period(0.5)) // Elastic easing for a bouncy effect
        .attr("width", d => x(d.value)); // Animate to final width

    // Animate the axes appearing
    svg.selectAll(".axis")
        .transition()
        .duration(1000)
        .delay(1000) // Start after bars begin growing
        .style("opacity", 1);

    // Animate the text labels appearing
    textLabels.transition()
        .duration(800)
        .delay((d, i) => 800 + (i * 100)) // Stagger the appearance of labels
        .style("opacity", 1)
        .attr("fill", function(d) {{
            const textWidth = this.getBBox().width;
            const barWidth = x(d.value);

            if (barWidth > textWidth + textPadding) {{
                if (d.color === '#638B48' || d.color === '#6F6F6F') {{
                    return 'white';
                }} else {{
                    return 'black';
                }}
            }} else {{
                return 'black';
            }}
        }});

    // Position the text labels either inside or outside the bars.
    textLabels.attr("x", function(d) {{
        const textWidth = this.getBBox().width; // Get the actual width of the text
        const barWidth = x(d.value); // Get the bar's width
        
        // Place text inside if there's enough room.
        if (barWidth > textWidth + textPadding) {{
            return textPadding; // Position from the left edge of the bar
        }} else {{ // Otherwise, place text outside the bar.
            return barWidth + textPadding; // Position after the bar ends, with padding
        }}
    }});

    // Function to handle mouseover events (shared by bars and text labels)
    function handleMouseOver(event, d_hovered_element) {{
        // Dim all bars except the one being hovered over.
        bars.transition().duration(100).attr("fill", bar_d => {{
            return bar_d === d_hovered_element ? bar_d.color : dimColor;
        }});

        // Update font color logic for text labels on hover.
        textLabels.transition().duration(100).attr("fill", function(bar_d) {{
            const textWidth = this.getBBox().width;
            const barWidth = x(bar_d.value);

            // If this is the label for the hovered bar.
            if (bar_d === d_hovered_element) {{
                // Apply its original color logic (white for dark, black for light, based on position).
                if (barWidth > textWidth + textPadding) {{
                    if (bar_d.color === '#638B48' || bar_d.color === '#6F6F6F') {{
                        return 'white';
                    }} else {{
                        return 'black';
                    }}
                }} else {{
                    return 'black'; // Text outside always black.
                }}
            }} else {{ // If this is the label for a non-hovered bar.
                return 'black'; // Make it black.
            }}
        }});

        // Update tooltip content with the hovered bar's data.
        tooltip.html(`<b>${{d_hovered_element.name}}</b>: ${{d_hovered_element.value}} Lakh`);
        // Make the tooltip visible.
        tooltip.style("opacity", 1);
    }}

    // Function to handle mouseout events (shared by bars and text labels)
    function handleMouseOut() {{
        // Restore all bars to their original base colors when the mouse leaves.
        bars.transition().duration(100).attr("fill", bar_d => bar_d.color);

        // Restore original conditional text label colors when the mouse leaves.
        textLabels.transition().duration(100).attr("fill", function(bar_d) {{
            const textWidth = this.getBBox().width;
            const barWidth = x(bar_d.value);

            // Apply original color logic (white for dark, black for light, based on position).
            if (barWidth > textWidth + textPadding) {{
                if (bar_d.color === '#638B48' || bar_d.color === '#6F6F6F') {{
                    return 'white';
                }} else {{
                    return 'black';
                }}
            }} else {{
                return 'black'; // Text outside always black.
            }}
        }});

        // Hide the tooltip.
        tooltip.style("opacity", 0);
    }}

    // Function to handle mousemove events (shared by bars and text labels)
    function handleMouseMove(event, d) {{
        const barX = x(d.value); // Get the x-position (width) of the current bar
        const barY = y(d.name);  // Get the y-position (top) of the current bar

        // Get the bounding rectangle of the main graph div for relative positioning.
        const graphRect = myGraphDiv.node().getBoundingClientRect();
        // Get the bounding rectangle of the tooltip to know its dimensions.
        const tooltipRect = tooltip.node().getBoundingClientRect();

        // Calculate the left position of the tooltip to center it above the bar's end.
        let tooltipLeft = graphRect.left + margin.left + barX - (tooltipRect.width / 2);
        // Calculate the top position of the tooltip to place its spike tip at the bar's edge.
        // tooltipRect.height is the height of the tooltip box itself.
        // Adding 8 pixels to account for the spike's height and minimal gap.
        let tooltipTop = graphRect.top + margin.top + barY - (tooltipRect.height + 8);
        
        // Adjust tooltip position to prevent it from going off the screen horizontally.
        if (tooltipLeft < 0) tooltipLeft = 0; // If it goes off left, snap to left edge
        if (tooltipLeft + tooltipRect.width > window.innerWidth) tooltipLeft = window.innerWidth - tooltipRect.width; // If it goes off right, snap to right edge

        // Apply the calculated positions to the tooltip.
        tooltip.style("left", tooltipLeft + "px")
               .style("top", tooltipTop + "px");
    }}


    // Add hover interactivity to the bars.
    bars.on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut)
        .on("mousemove", handleMouseMove);

    // Add hover interactivity to the text labels.
    textLabels.on("mouseover", handleMouseOver)
              .on("mouseout", handleMouseOut)
              .on("mousemove", handleMouseMove);

</script>

</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Life Cycle Cost for 50 Years")

        view = QWebEngineView()
        view.setHtml(html_content)
        self.setCentralWidget(view)
        self.resize(700, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
