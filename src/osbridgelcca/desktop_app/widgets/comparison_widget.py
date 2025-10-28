from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, QSize, Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import (QIcon)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QCheckBox)
import sys

class ComparisonWidget(QWidget):
    closed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("comparison_panel_widget")
        self.setStyleSheet("""
           #comparison_panel_widget {
                background-color: #FDEFEF;
                border-radius: 8px;
            }
            #comparison_panel_widget QLabel {
                color: #FDEFEF;
                font-size: 12px;
            }
            #comparison_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #FDEFEF;
            }
            QScrollArea {
                border: 1px solid #000000;
                background-color: transparent;
                outline: none;
            }
            #scroll_content_widget {
                background-color: #FFF9F9;
            }
            QScrollBar:vertical {
                border: 1px solid #E0E0E0;
                background: #F0F0F0;
                width: 12px;
                margin: 18px 0px 18px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border: 1px solid #A0A0A0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: bottom;
                subcontrol-position: bottom;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QScrollBar::sub-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: top;
                subcontrol-position: top;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                width: 10px;
                height: 10px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::up-arrow:vertical {
                image: url(resources/arrow_up.png);
            }
            QScrollBar::down-arrow:vertical {
                image: url(resources/arrow_down.png);
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: #D0D0D0;
            }
            QPushButton#top_button_comparison_panel {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_comparison_panel:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_comparison_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }
            QPushButton#top_button_comparison_panel:hover QIcon {
                color: red;
            }

            /* Comparison cards */
            QWidget#comparison_card {
                background-color: #F0F8FF;
                border: 2px solid #4682B4;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton#close_comparison_card_button {
                border: none;
                background: transparent;
                padding: 2px;
            }
            QPushButton#close_comparison_card_button:hover {
                background: rgba(0,0,0,0.05);
                border-radius: 4px;
            }
            
            /* Comparison section headers */
            QWidget#comparison_section {
                background-color: #E6F3FF;
                border: 1px solid #87CEEB;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
            
            /* Comparison buttons */
            QPushButton#comparison_button {
                background-color: #4682B4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#comparison_button:hover {
                background-color: #5A9BD4;
            }
            QPushButton#comparison_button:pressed {
                background-color: #36648B;
            }
                                       
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Top Section ---
        top_h_layout = QHBoxLayout()
        self.top_button_comparison_panel = QPushButton("Comparison Window   ")
        self.top_button_comparison_panel.setObjectName("top_button_comparison_panel")
        self.top_button_comparison_panel.setIcon(QIcon("resources/close.png"))
        self.top_button_comparison_panel.setIconSize(QSize(13, 13))
        self.top_button_comparison_panel.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.top_button_comparison_panel.clicked.connect(self.close_widget)
        
        top_h_layout.addWidget(self.top_button_comparison_panel)
        top_h_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(top_h_layout)

        # --- Main Content Area ---
        self.main_content_widget = QWidget()
        self.main_content_widget.setObjectName("main_content_widget")
        self.main_content_widget.setStyleSheet("""
            #main_content_widget {
                background-color: #FDEFEF;
                border: 1px solid #4682B4;
                border-top: none;
            }
        """)
        
        # Create scroll area for the main content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F0F0F0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar:horizontal {
                background: #F0F0F0;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #C0C0C0;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #A0A0A0;
            }
        """)
        
        # Create scrollable content widget
        self.scroll_content_widget = QWidget()
        self.scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_content_widget.setStyleSheet("""
            #scroll_content_widget {
                background-color: #F0F8FF;
            }
        """)
        
        # Main content layout
        content_layout = QVBoxLayout(self.scroll_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # File selection section
        self.file_selection_widget = self._create_file_selection()
        content_layout.addWidget(self.file_selection_widget)
        
        # Comparison chart area
        self.comparison_chart_widget = self._create_comparison_chart()
        content_layout.addWidget(self.comparison_chart_widget)
        
        # Set the scroll content widget to the scroll area
        self.scroll_area.setWidget(self.scroll_content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(self.scroll_area)

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    def _create_file_selection(self) -> QWidget:
        """Create the file selection section matching the image"""
        selection_widget = QWidget()
        selection_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                margin: 5px;
            }
        """)
        
        selection_layout = QVBoxLayout(selection_widget)
        selection_layout.setContentsMargins(20, 15, 20, 15)
        selection_layout.setSpacing(15)
        
        # Top section with description and browse button
        top_layout = QHBoxLayout()
        
        # Description text
        desc_label = QLabel("Select files to compare various\ncomponents of life-cycle cost analysis")
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
                line-height: 1.4;
            }
        """)
        top_layout.addWidget(desc_label)
        
        top_layout.addStretch(1)
        
        # Browse button
        browse_button = QPushButton("Browse...")
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        top_layout.addWidget(browse_button)
        
        selection_layout.addLayout(top_layout)
        
        # File checkboxes section
        files_layout = QVBoxLayout()
        files_layout.setSpacing(8)
        
        # PSC Bridge checkbox
        psc_layout = QHBoxLayout()
        psc_checkbox = QCheckBox()
        psc_checkbox.setChecked(True)
        psc_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:checked::before {
                content: "✓";
                color: white;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
                line-height: 16px;
            }
        """)
        
        psc_label = QLabel("PSC Bridge.os")
        psc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
                margin-left: 8px;
            }
        """)
        
        psc_import_label = QLabel("Imported")
        psc_import_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888888;
                margin-left: 10px;
            }
        """)
        
        psc_layout.addWidget(psc_checkbox)
        psc_layout.addWidget(psc_label)
        psc_layout.addWidget(psc_import_label)
        psc_layout.addStretch(1)
        
        # Steel Bridge checkbox
        steel_layout = QHBoxLayout()
        steel_checkbox = QCheckBox()
        steel_checkbox.setChecked(True)
        steel_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-color: #4CAF50;
            }
            QCheckBox::indicator:checked::before {
                content: "✓";
                color: white;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
                line-height: 16px;
            }
        """)
        
        steel_label = QLabel("Steel Bridge.os")
        steel_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
                margin-left: 8px;
            }
        """)
        
        steel_import_label = QLabel("Imported")
        steel_import_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888888;
                margin-left: 10px;
            }
        """)
        
        steel_layout.addWidget(steel_checkbox)
        steel_layout.addWidget(steel_label)
        steel_layout.addWidget(steel_import_label)
        steel_layout.addStretch(1)
        
        files_layout.addLayout(psc_layout)
        files_layout.addLayout(steel_layout)
        
        selection_layout.addLayout(files_layout)
        
        return selection_widget



    def _create_comparison_chart(self) -> QWidget:
        """Create the comparison chart area matching the image"""
        chart_widget = QWidget()
        chart_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                margin: 5px;
            }
        """)
        
        chart_layout = QVBoxLayout(chart_widget)
        chart_layout.setContentsMargins(20, 15, 20, 15)
        chart_layout.setSpacing(15)
        
        # Chart area - full width
        # Horizontal bar chart using QWebEngineView
        chart_view = QWebEngineView()
        chart_view.setHtml(self._build_comparison_chart_html())
        chart_view.setZoomFactor(0.9)
        chart_view.setMinimumHeight(400)
        chart_view.setMaximumHeight(600)
        chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        chart_layout.addWidget(chart_view)
        
        return chart_widget
    
    def _create_legend(self) -> QWidget:
        """Create the legend widget matching the image"""
        legend_widget = QWidget()
        legend_widget.setStyleSheet("""
            QWidget {
                background-color: #FDEFEF;
                border: 1px solid #DDDDDD;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        legend_layout = QVBoxLayout(legend_widget)
        legend_layout.setContentsMargins(10, 10, 10, 10)
        legend_layout.setSpacing(8)
        
        # PSC Bridge legend item
        psc_layout = QHBoxLayout()
        psc_color = QWidget()
        psc_color.setFixedSize(16, 16)
        psc_color.setStyleSheet("background-color: #87CEEB; border: 1px solid #5F9EA0;")
        
        psc_label = QLabel("PSC Bridge")
        psc_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #333333;
            }
        """)
        
        psc_layout.addWidget(psc_color)
        psc_layout.addWidget(psc_label)
        psc_layout.addStretch(1)
        
        # Steel Bridge legend item
        steel_layout = QHBoxLayout()
        steel_color = QWidget()
        steel_color.setFixedSize(16, 16)
        steel_color.setStyleSheet("background-color: #8B0000; border: 1px solid #654321;")
        
        steel_label = QLabel("Steel Bridge")
        steel_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #333333;
            }
        """)
        
        steel_layout.addWidget(steel_color)
        steel_layout.addWidget(steel_label)
        steel_layout.addStretch(1)
        
        legend_layout.addLayout(psc_layout)
        legend_layout.addLayout(steel_layout)
        
        return legend_widget
    
    def _create_download_options(self) -> QWidget:
        """Create the download options widget matching the image"""
        download_widget = QWidget()
        download_layout = QVBoxLayout(download_widget)
        download_layout.setContentsMargins(0, 0, 0, 0)
        download_layout.setSpacing(5)
        
        # Download options
        options = ["Download as PNG", "Download as JPG", "Download as PDF", "View as Table"]
        
        for option in options:
            option_label = QLabel(option)
            option_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #0066CC;
                    padding: 4px;
                    text-decoration: underline;
                }
                QLabel:hover {
                    background-color: #FDEFEF;
                    color: #0052A3;
                }
            """)
            option_label.setCursor(Qt.CursorShape.PointingHandCursor)
            download_layout.addWidget(option_label)
        
        return download_widget

    def _build_comparison_chart_html(self) -> str:
        """Generate HTML for horizontal bar chart using exact code from Horizontal Bar Graph 2.py"""
        # Sample data matching the original structure - you can replace this with actual CSV data later
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
        
        # Sample data (you can replace these with actual values from CSV)
        psc_cost = [61.83, 8.53, 2.32, 123.93, 29.03, 1.44, 16.99, 14.32, 1.99, 0.77, 0.0]
        steel_cost = [61.83, 11.02, 1.68, 123.93, 29.03, 1.44, 16.99, 14.32, 1.99, 0.77, 0.0]
        
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
        import json
        js_data_string = json.dumps(js_data)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bridge Cost Comparison</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #FDEFEF;

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

const margin = {{top: 60, right: 150, bottom: 80, left: 300}};
const width = 1200 - margin.left - margin.right;
const barHeight = 18;
const categoryGap = 15;
const barGap = 2;
const height = data.length * (barHeight * 2 + barGap + categoryGap) + margin.top + margin.bottom;

const svg = d3.select("#chart")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height)
  .append("g")
  .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

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
  .attr("transform", `translate(0, ${{height - margin.top - margin.bottom}})`)
  .call(d3.axisBottom(x).ticks(8).tickFormat(d => d + " Lakh"))
  .selectAll("text")
  .style("text-anchor", "end")
  .attr("dx", "-.8em")
  .attr("dy", ".15em")
  .attr("transform", "rotate(-25)");

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
  .attr("transform", `translate(${{width - 140}}, -40)`);

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
        return html



#----------------Standalone-Test-Code--------------------------------

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("border: none")

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.addStretch(1)

        self.main_h_layout.addWidget(ComparisonWidget(), 2)

        self.setWindowState(Qt.WindowState.WindowMaximized)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
