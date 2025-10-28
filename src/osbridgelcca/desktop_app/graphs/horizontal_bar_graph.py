import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
import pandas as pd

FILE_PATH = r"data1.csv"
df = pd.read_csv(FILE_PATH)

# using the d3js graphing library to plot the graph, it is downloaded locally and saved in the same directory as that of this graph script
with open(r"..\dependencies\d3js.js", "r", encoding="utf-8") as f:
    d3_js = f.read()

list_final = [
    "Initial construction cost",
    "Embodied carbon emissions",
    "Time cost estimate",
    "Road user cost",
    "Additional CO2 e costs due to rerouting",
    "Periodic Maintenance costs",
    "Periodic maintenance carbon emissions",
    "Annual routine inspection costs",
    "Repair and rehabilitation costs",
    "Demolition and deconstruction costs",
    "Recycling costs"
]

# Extract values from DataFrame
psc_cost = []
steel_cost = []
for item in list_final:
    count = 0
    for _, row in df.iterrows():
        if item in list(row):
            temp_row = list(row)
            if count == 0:
                psc_cost.append(float(temp_row[temp_row.index(item) + 1]))
            else:
                steel_cost.append(float(temp_row[temp_row.index(item) + 1]))
            count += 1

# Calculate Total Life-Cycle Cost
total_psc_cost = sum(psc_cost)
total_steel_cost = sum(steel_cost)

# Prepare data for D3.js
js_data = []
for i, label in enumerate(list_final):
    # Adjust labels for better display in the chart
    display_label = label.replace("Initial construction cost", "Initial Construction Cost") \
                         .replace("Embodied carbon emissions", "Initial Carbon Emission Cost") \
                         .replace("Time cost estimate", "Time Cost") \
                         .replace("Road user cost", "Road User Cost") \
                         .replace("Additional CO2 e costs due to rerouting", "Carbon Emission due to Re-Routing") \
                         .replace("Periodic Maintenance costs", "Periodic Maintenance Costs") \
                         .replace("Periodic maintenance carbon emissions", "Maintenance Emission Cost") \
                         .replace("Annual routine inspection costs", "Routine Inspection Cost") \
                         .replace("Repair and rehabilitation costs", "Repair & Rehabilitation Cost") \
                         .replace("Demolition and deconstruction costs", "Demolition & Disposal Cost") \
                         .replace("Recycling costs", "Recycling Cost")


    js_data.append({
        "label": display_label,
        "psc": psc_cost[i],
        "steel": steel_cost[i]
    })

# Add the "Total Life-Cycle Cost" entry
js_data.append({
    "label": "Total Life-Cycle Cost",
    "psc": total_psc_cost,
    "steel": total_steel_cost
})

# Convert Python list of dictionaries to a JavaScript array string
js_data_string = str(js_data).replace("'", '"') # Replace single quotes with double quotes for JSON compatibility

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bridge Cost Comparison</title>
  <script>{d3_js}</script>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f8eaea;
      margin: 0;
    }}
    .tooltip {{
      position: absolute;
      background-color: #fff;
      padding: 8px 12px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
      font-size: 14px;
      pointer-events: none;
      opacity: 0;
      z-index: 10;
      transition: none;
    }}
    .tooltip::after {{
      content: "";
      position: absolute;
      bottom: -10px;
      left: 50%;
      transform: translateX(-50%);
      border-width: 6px 6px 0 6px;
      border-style: solid;
      border-color: #fff transparent transparent transparent;
      box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }}
    .legend text {{
      font-size: 14px;
    }}
    .legend rect {{
      stroke: black;
      stroke-width: 1;
    }}
    #chart {{
      margin: 20px;
    }}
    .negative-value {{
      fill: white;
      font-size: 11px;
      font-weight: bold;
    }}
  </style>
</head>
<body>
<div id="chart"></div>
<div class="tooltip" id="tooltip"></div>
<script>
const data = {js_data_string};

const margin = {{top: 60, right: 130, bottom: 50, left: 280}};
const width = 1000 - margin.left - margin.right;
const barHeight = 18;
const categoryGap = 15;
const barGap = 2;
const height = data.length * (barHeight * 2 + barGap + categoryGap) + margin.top + margin.bottom;

const svg = d3.select("#chart")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height)
  .append("g")
  .attr("transform", `translate(${{margin.left}},${{margin.top}})`); /* <-- Here is the fix */

// Find min and max values to properly handle negative numbers
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
svg.append("g")
  .call(d3.axisLeft(y).tickSize(0))
  .selectAll(".domain").remove();

// Add x-axis with zero line
svg.append("g")
  .attr("transform", `translate(0, ${{height - margin.top - margin.bottom}})`) /* <-- Here is the fix */
  .call(d3.axisBottom(x).ticks(10).tickFormat(d => d + " Lakh"));

// Add vertical zero line
svg.append("line")
  .attr("x1", x(0))
  .attr("x2", x(0))
  .attr("y1", 0)
  .attr("y2", height - margin.top - margin.bottom)
  .attr("stroke", "#000")
  .attr("stroke-width", 1);

const tooltip = d3.select("#tooltip");

function showTooltip(event, label, value, type) {{
  tooltip
    .html(`<strong>${{label}} (${{type === 'psc' ? 'PSC' : 'Steel'}})</strong>: ${{value}} Lakh`)
    .style("left", (event.pageX - 150) + "px")
    .style("top", (event.pageY - 50) + "px")
    .style("opacity", 1);
}}

function hideTooltip() {{
  tooltip.style("opacity", 0);
}}

const colors = {{
  psc: "#87cefa",
  steel: "#8b0000"
}};

// Calculate y position for each bar pair
function getBarYPosition(d, barIndex) {{
  return y(d.label) + barIndex * (barHeight + barGap);
}}

// Draw bars for PSC Bridge with animation
svg.selectAll(".bar-psc")
  .data(data)
  .enter()
  .append("rect")
  .attr("class", "bar-psc")
  .attr("x", x(0)) // Start at zero line
  .attr("y", d => getBarYPosition(d, 0))
  .attr("width", 0) // Start with zero width
  .attr("height", barHeight)
  .attr("fill", colors.psc)
  .attr("rx", 3)
  .attr("ry", 3)
  .on("mousemove", function(event, d) {{
    showTooltip(event, d.label, d.psc, 'psc');
    d3.select(this).attr("fill", "#4682b4");
  }})
  .on("mouseleave", function() {{
    hideTooltip();
    d3.select(this).attr("fill", colors.psc);
  }})
  .transition() // Add transition for animation
  .duration(1000) // Animation duration in milliseconds
  .delay((d, i) => i * 100) // Staggered delay for each bar
  .attr("x", d => x(Math.min(0, d.psc)))
  .attr("width", d => Math.abs(x(d.psc) - x(0)));

// Draw bars for Steel Bridge with animation
svg.selectAll(".bar-steel")
  .data(data)
  .enter()
  .append("rect")
  .attr("class", "bar-steel")
  .attr("x", x(0)) // Start at zero line
  .attr("y", d => getBarYPosition(d, 1))
  .attr("width", 0) // Start with zero width
  .attr("height", barHeight)
  .attr("fill", colors.steel)
  .attr("rx", 3)
  .attr("ry", 3)
  .on("mousemove", function(event, d) {{
    showTooltip(event, d.label, d.steel, 'steel');
    d3.select(this).attr("fill", "#a52a2a");
  }})
  .on("mouseleave", function() {{
    hideTooltip();
    d3.select(this).attr("fill", colors.steel);
  }})
  .transition() // Add transition for animation
  .duration(1000) // Animation duration in milliseconds
  .delay((d, i) => i * 100) // Staggered delay for each bar
  .attr("x", d => x(Math.min(0, d.steel)))
  .attr("width", d => Math.abs(x(d.steel) - x(0)));

// Add value labels for PSC Bridge (right of bar)
svg.selectAll(".label-psc")
  .data(data)
  .enter()
  .append("text")
  .attr("class", "label-psc")
  .attr("x", d => d.psc >= 0 ? x(d.psc) + 5 : x(d.psc) - 5)
  .attr("y", d => getBarYPosition(d, 0) + barHeight / 2 + 4)
  .text(d => d.psc + " Lakh")
  .attr("font-size", "12px")
  .attr("fill", d => d.psc < 0 ? "black" : "black")
  .attr("text-anchor", d => d.psc >= 0 ? "start" : "end");

// Add value labels for Steel Bridge (right of bar)
svg.selectAll(".label-steel")
  .data(data)
  .enter()
  .append("text")
  .attr("class", "label-steel")
  .attr("x", d => d.steel >= 0 ? x(d.steel) + 5 : x(d.steel) - 5)
  .attr("y", d => getBarYPosition(d, 1) + barHeight / 2 + 4)
  .text(d => d.steel + " Lakh")
  .attr("font-size", "12px")
  .attr("fill", d => d.steel < 0 ? "black" : "black")
  .attr("text-anchor", d => d.steel >= 0 ? "start" : "end");

// Legend
const legend = svg.append("g")
  .attr("transform", `translate(${{width - 140}}, -40)`); /* <-- Here is the fix */

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
  .text("PSC Bridge");

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
  .text("Steel Bridge");

// Add title
svg.append("text")
  .attr("x", width / 2)
  .attr("y", -20)
  .attr("text-anchor", "middle")
  .style("font-size", "18px")
  .style("font-weight", "bold")
  .text("Bridge Life-Cycle Cost Comparison");
</script>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bridge Cost Comparison")
        self.setGeometry(100, 100, 1200, 900)

        view = QWebEngineView()
        view.setHtml(html_content)
        self.setCentralWidget(view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())