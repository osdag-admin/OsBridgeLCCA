import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
import pandas as pd

FILE_PATH = r"data.csv"
df = pd.read_csv(FILE_PATH)

# using the d3js graphing library to plot the graph, it is downloaded locally and saved in the same directory as that of this graph script
with open(r"..\dependencies\d3js.js", "r", encoding="utf-8") as f:
    d3_js = f.read()

name = ['A - Initial Carbon Emission Cost\n', 'B - Carbon Emission due to Re-Routing', 'C - Maintenance Emission Costs',
        "Embodied carbon emissions", "Additional CO2 e costs due to rerouting", "Periodic maintenance carbon emissions"]
percentage_list = []
cost_list = []

for i, item in enumerate(name):
    count = 0
    if i < 3:
        for _, row in df.iterrows():
            if item in list(row):
                if count == 0:
                    temp_row = list(row)
                    percentage_list.append(float(temp_row[temp_row.index(item) + 1]))
                    count += 1
    else:
        for _, row in df.iterrows():
            if item in list(row):
                if count == 0:
                    temp_row = list(row)
                    cost_list.append(float(temp_row[temp_row.index(item) + 1]))
                    count += 1

percentage_list = [round(item, 2) for item in percentage_list]
print(percentage_list)
val_a, val_b, val_c = percentage_list

cost_list = [round(float(items) / 100000.0, 2) for items in cost_list]
cost_a, cost_b, cost_c = cost_list


html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bubble Chart Layout</title>
  <script>{d3_js}</script>
  <style>
    body {{
      font-family: sans-serif;
      background: #f8f1ef;
      margin: 0;
      overflow: hidden;
    }}
    #chart-container {{
      position: relative;
      width: 800px;
      height: 550px;
    }}
    #legend {{
      position: absolute;
      right: 20px;
      bottom: 20px;
      font-size: 14px;
      line-height: 1.8;
    }}
    #legend span {{
      display: block;
      white-space: nowrap;
    }}
    .legend-text {{
      color: #808000;
      display: inline;
    }}
    .tooltip {{
      position: absolute;
      padding: 12px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 0 12px rgba(0, 0, 0, 0.5);
      pointer-events: none;
      font-size: 14px;
      opacity: 0;
      transition: opacity 0.3s ease, transform 0.2s ease;
      transform: translateY(-10px);
    }}
    .tooltip.visible {{
      opacity: 1;
      transform: translateY(0);
    }}
    .tooltip::after {{
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      border-width: 10px 10px 0 10px;
      border-style: solid;
      border-color: white transparent transparent transparent;
      filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
    }}
    .tooltip strong {{
      color: #5c8a00;
      font-size: 16px;
    }}
    .tooltip b {{
      font-size: 18px;
    }}
  </style>
</head>
<body>
  <div id="chart-container">
    <div id="chart"></div>
    <div id="legend">
      <span><span class="legend-text">A - Initial Carbon Emission Cost</span></span>
      <span><span class="legend-text">B - Carbon Emission due to Re-Routing</span></span>
      <span><span class="legend-text">C - Maintenance Emission Costs</span></span>
    </div>
  </div>
  <div class="tooltip" id="tooltip"></div>

  <script>
    const data = [
      {{ name: 'A', value: {val_a}, x: 409, y: 271, label:'Initial Carbon Emission Cost' , cost: {cost_a}}}, 
      {{ name: 'B', value: {val_b}, x: 382, y: 113, label:'Carbon Emission due to Re-Routing' , cost: {cost_b}}}, 
      {{ name: 'C', value: {val_c}, x: 259, y: 216, label:'Maintenance Emission Costs' , cost: {cost_c}}}
    ];

    const svgWidth = 750, svgHeight = 550;
    const radiusScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([30, 78]);

    const svg = d3.select("#chart")
      .append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);

    svg.append("circle")
      .attr("cx", 350)
      .attr("cy", 200)
      .attr("r", 180)
      .attr("fill", "#ffffff")
      .attr("opacity", 0.9);

    const tooltip = d3.select("#tooltip");

    const groups = svg.selectAll("g")
      .data(data)
      .enter()
      .append("g")
      .attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);

    groups.append("circle")
      .attr("r", 0)
      .attr("fill", "#808000")
      .transition()
      .delay((_, i) => i * 300)
      .duration(1000)
      .attr("r", d => radiusScale(d.value));

    // Event listeners with greying effect
    groups.selectAll("circle")
      .on("mouseover", function (event, d) {{
        tooltip
          .html(`<strong>${{d.label}}</strong><br><b>${{d.cost}} Lakh; ${{d.value}} %</b>`)
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
      }})
      .on("mousemove", function (event) {{
        tooltip
          .style("left", (event.pageX - 120) + "px")
          .style("top", (event.pageY - 90) + "px");
      }})
      .on("mouseout", function (event, d) {{
        tooltip.classed("visible", false);

        // Restore original color and size for all
        groups.selectAll("circle")
          .transition()
          .duration(10)
          .style("fill", "#808000")
          .attr("r", c => radiusScale(c.value));
      }});

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
  </script>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bubble chart")
        self.setGeometry(100, 100, 900, 550)

        view = QWebEngineView()
        view.setHtml(html_content)
        self.setCentralWidget(view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
