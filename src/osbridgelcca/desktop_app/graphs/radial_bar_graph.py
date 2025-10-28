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

# hexal color code for various concentric circles, used inside the HTML js script text(its inside the string html_content)
colors = ['#273B5C', '#2E5743', '#996515', '#36454F']

# labels used displaying purpose, used inside the HTML js script text(its inside the string html_content)
stage_label = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage']
stage_label_condition = ['initialstage', 'usestage', 'endoflifestage', 'beyondlifestage']
percentage = []

# for loop to extract the values, modify according to the style
# Fixed: Using .iloc for positional access instead of deprecated row[index] syntax
for ___, row in df.iterrows():
    if isinstance(row.iloc[8], str):
        if row.iloc[8].lower().replace(" ", "") in stage_label_condition:
            percentage.append(float(row.iloc[9]))
percentage = percentage[:4]

# html + js + css script to generate the radial bar graph, we used python's format to plug the values which we have extracted from the csv file
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title></title>
  <style>
    body {{
      background: #f2e8e7;
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: start;
      align-items: center;
      height: 100vh;
      margin: 0;
    }}
    h2 {{
      margin-top: 30px;
      margin-bottom: 10px;
      font-size: 24px;
      color: #243f64;
    }}
    .tooltip {{
      position: absolute;
      text-align: center;
      padding: 8px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
      pointer-events: none;
      opacity: 0;
      font-size: 14px;
      transform: translateX(-50%);
    }}
    .tooltip:after {{
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: white transparent transparent transparent;
    }}
    text.label {{
      font-size: 14px;
      fill: #333;
    }}
  </style>
</head>
<body>

<h2><span style="color: #638B48">Economic cost</span> distribution across various stages for bridges for 50 years</h2>
<svg width="500" height="400"></svg>
<div class="tooltip"></div>

<script>{d3_js}</script>
<script>
 //constant data, extracted from csv file
  const data = [
    {{ name: '{stage_label[3]}', value: {percentage[3] / 100}, color: '{colors[3]}' }},
    {{ name: '{stage_label[2]}', value: {percentage[2] / 100}, color: '{colors[2]}' }},
    {{ name: '{stage_label[1]}', value: {percentage[1] / 100}, color: '{colors[1]}' }},
    {{ name: '{stage_label[0]}', value: {percentage[0] / 100}, color: '{colors[0]}' }}
  ];

//window property
  const width = 500, height = 400;
  const barWidth = 20;
  const spacing = 10;
  const center = {{ x: width / 2 + 50, y: height / 2 }};

  const svg = d3.select("svg");
  const g = svg.append("g")
    .attr("transform", `translate(${{center.x}},${{center.y}})`);

  const tooltip = d3.select(".tooltip");
// code for generating arcs
  data.forEach((d, i) => {{
    const innerRadius = 50 + i * (barWidth + spacing);
    const outerRadius = innerRadius + barWidth;

   //code to generate arc
    const arcGen = d3.arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius)
      .startAngle(0)
      .cornerRadius(10);  

    // the below is used to fix the colors for the circular bar
    const path = g.append("path")
      .datum(d)
      .attr("fill", d.color)
      .attr("d", arcGen({{ endAngle: 0 }}))
      .attr("class", "arc");

// code below is for creating animation in the start, the entire animation runs for 1200ms
    path.transition()
      .duration(1200)
      .attrTween("d", function(d) {{
        const interpolate = d3.interpolate(0, (d.value * 2 * Math.PI) + 0.03);
        return function(t) {{
          return arcGen({{ endAngle: interpolate(t) }});
        }};
      }});

    // the below 2 lines are used to place the static percentage values to the left of the radial bar graph
    const labelX = center.x - 8;
    const labelY = center.y + (data.length - 1 - i) * (barWidth + spacing) -150;

    // the below code fixes the position of the static percentage label
    svg.append("text")
      .attr("x", labelX)
      .attr("y", labelY + 5)
      .attr("text-anchor", "end")
      .attr("class", "label")
      .text(`${{(d.value * 100).toFixed(2)}}%`);

// the below entire code is to provide hover event response, that is when we hover over a radial bar or arc, we get a small pop up info window 
    path.on("mouseover", function(event, hoveredData) {{
        d3.selectAll(".arc")
          .attr("fill", p => p === hoveredData ? p.color : "#ccc");

            tooltip.style("opacity", 1)
.html(`
  <div style="text-align:center; font-family:sans-serif;">
    <span style="font-weight: 500;">${{hoveredData.name}}</span>
    <br>
    <span style="color: #638B48; font-size: 13.5px;">
      Economic Cost: 
      <span style="font-weight: 600;">
        ${{(hoveredData.value * 100).toFixed(1)}}%;
        ${{(hoveredData.value * 225.5).toFixed(2)}}
      </span>
    </span>
    <br>
    <span style="font-weight: bold; color: #638B48;">Lakhs</span>
  </div>
`).style("left", (event.pageX) + "px")
               .style("top", (event.pageY - 50) + "px");
      }})
      .on("mousemove", function(event) {{
        tooltip.style("left", (event.pageX) + "px")
               .style("top", (event.pageY - 70) + "px");
      }})
      .on("mouseout", function() {{
        d3.selectAll(".arc")
          .attr("fill", d => d.color);
        tooltip.style("opacity", 0);
      }});
  }});
</script>

</body>
</html>
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Economic Cost Distribution")

        view = QWebEngineView()
        view.setHtml(html_content)
        self.setCentralWidget(view)
        self.resize(700, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())