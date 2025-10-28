from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, QSize, Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import (QIcon)
from PySide6.QtWebEngineWidgets import QWebEngineView

from PySide6.QtWidgets import (QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QComboBox)
import sys

# using the d3js graphing library to plot the graph, it is downloaded locally and saved in the same directory as that of this graph script
with open(r"dependencies/d3js.js", "r", encoding="utf-8") as f:
    d3_js = f.read()

class ResultsWidget(QWidget):
    closed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("central_panel_widget")
        self.setStyleSheet("""
           #central_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
            #central_panel_widget QLabel {
                color: #333333;
                font-size: 12px;
            }
            #central_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #555555;
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
            QPushButton#top_button_right_panel {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_right_panel:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_right_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }
            QPushButton#top_button_right_panel:hover QIcon {
                color: red;
            }

                                    
            QPushButton#top_button_right_panel_pressed {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                border-bottom: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_right_panel_pressed:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_right_panel_pressed:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }
            QPushButton#top_button_right_panel_pressed:hover QIcon {
                color: red;
            }

            /* Results cards */
            QWidget#result_card {
                background-color: #FDEFEF;
                border: 1px solid #000000;
                border-radius: 8px;
                height: 150px;
            }
            QPushButton#close_card_button {
                border: none;
                background: transparent;
                padding: 2px;
            }
            QPushButton#close_card_button:hover {
                background: rgba(0,0,0,0.05);
                border-radius: 4px;
            }
            
            /* Bottom navigation buttons */
            QPushButton#bottom_nav_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                color: #333333;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#bottom_nav_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
            QPushButton#bottom_nav_button:pressed {
                background-color: #F0F0F0;
                border-color: #A0A0A0;
            }
                                       
        """)
        
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.pressed=0
        self.current_page = 0  # 0: initial view, 1: pie chart, 2: 100-year graphs, 3: bubble graphs
        self.max_page = 3

        # --- Top Section ---
        top_h_layout_left_panel = QHBoxLayout()
        self.top_button_right_panel = QPushButton("Data Window   ")
        self.top_button_right_panel.setObjectName("top_button_right_panel")
        self.top_button_right_panel.setIcon(QIcon("resources/close.png"))
        self.top_button_right_panel.setIconSize(QSize(13, 13))
        self.top_button_right_panel.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.top_button_right_panel.clicked.connect(self.close_widget)
        
        self.top_button_left_panel = QPushButton("Results Window ")
        self.top_button_left_panel.setObjectName("top_button_right_panel")
        self.top_button_left_panel.setIcon(QIcon("resources/close.png"))
        self.top_button_left_panel.setIconSize(QSize(13, 13))
        self.top_button_left_panel.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.top_button_left_panel.clicked.connect(self.switch_to_results_widget)
        
        top_h_layout_left_panel.addWidget(self.top_button_right_panel)
        top_h_layout_left_panel.addWidget(self.top_button_left_panel)

        top_h_layout_left_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

        # --- Main Content Area ---
        self.main_content_widget = QWidget()
        self.main_content_widget.setObjectName("main_content_widget")
        self.main_content_widget.setStyleSheet("""
            #main_content_widget {
                background-color: #FDEFEF;
                border: 1px solid #000000;
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
                background-color: #FDEFEF;
            }
        """)
        
        # Add a simple label to show this is the results area
        content_layout = QVBoxLayout(self.scroll_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        self.welcome_label = QLabel("Results Area")
        self.welcome_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                padding: 20px;
            }
        """)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.welcome_label)

        # Container with three closable cards (initially hidden)
        self.cards_container = QWidget()
        self.cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Create a flow layout for responsive card arrangement
        self.cards_layout = QHBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetNoConstraint)
        
        titles = [
            "<span style='color:#638B48; font-weight:600;'>Economic cost</span> distribution across various stages for bridges for 50 years",
            "<span style='color:#B55353; font-weight:600;'>Social cost</span> distribution across stages for PSC bridges for 50 years",
            "<span style='color:#2F6DB2; font-weight:600;'>Environmental cost</span> distribution across stages for PSC bridges for 50 years",
        ]
        
        # Create and add cards with debug information
        self.cards_list = []  # Store references to cards
        for i, title in enumerate(titles):
            card = self._create_result_card(title, [30, 45, 15, 10])
            self.cards_list.append(card)
            self.cards_layout.addWidget(card)
            print(f"Created card {i}: {title[:30]}...")
            print(f"Card {i} visible: {card.isVisible()}")
            print(f"Card {i} parent: {card.parent()}")
        
        self.cards_container.setVisible(False)
        content_layout.addWidget(self.cards_container)
        
        print(f"Cards container created with {len(self.cards_list)} cards")
        print(f"Cards container visible: {self.cards_container.isVisible()}")
        print(f"Cards container parent: {self.cards_container.parent()}")
        
        # Shared legend below all cards
        self.legend_widget = self._build_legend_widget()
        self.legend_widget.setVisible(False)
        content_layout.addWidget(self.legend_widget, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Bar graph below legend
        self.bar_graph_widget = self._build_bar_graph()
        self.bar_graph_widget.setVisible(False)
        content_layout.addWidget(self.bar_graph_widget, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Pie chart widget (for page 1)
        self.pie_chart_widget = self._build_pie_chart()
        self.pie_chart_widget.setVisible(False)
        content_layout.addWidget(self.pie_chart_widget, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # 100-year widgets (for page 2)
        self.cards_container_100 = QWidget()
        self.cards_container_100.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.cards_layout_100 = QHBoxLayout(self.cards_container_100)
        self.cards_layout_100.setContentsMargins(0, 0, 0, 0)
        self.cards_layout_100.setSpacing(20)
        self.cards_layout_100.setSizeConstraint(QHBoxLayout.SizeConstraint.SetNoConstraint)
        
        titles_100 = [
            "<span style='color:#638B48; font-weight:600;'>Economic cost</span> distribution across various stages for bridges for 100 years",
            "<span style='color:#B55353; font-weight:600;'>Social cost</span> distribution across stages for PSC bridges for 100 years",
            "<span style='color:#2F6DB2; font-weight:600;'>Environmental cost</span> distribution across stages for PSC bridges for 100 years",
        ]
        
        self.cards_list_100 = []
        for i, title in enumerate(titles_100):
            card = self._create_result_card(title, [30, 45, 15, 10])
            self.cards_list_100.append(card)
            self.cards_layout_100.addWidget(card)
        
        self.cards_container_100.setVisible(False)
        content_layout.addWidget(self.cards_container_100)
        
        self.legend_widget_100 = self._build_legend_widget()
        self.legend_widget_100.setVisible(False)
        content_layout.addWidget(self.legend_widget_100, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.bar_graph_widget_100 = self._build_bar_graph_100()
        self.bar_graph_widget_100.setVisible(False)
        content_layout.addWidget(self.bar_graph_widget_100, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Bubble graph widgets (for page 3)
        self.bubble_cards_container = QWidget()
        self.bubble_cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.bubble_cards_layout = QHBoxLayout(self.bubble_cards_container)
        self.bubble_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.bubble_cards_layout.setSpacing(20)
        
        bubble_titles = [
            "<span style='color:#638B48; font-weight:600;'>Carbon Emission Cost</span> Through-out Life-Cycle Stages for 50 years",
            "<span style='color:#B55353; font-weight:600;'>Carbon Emission Cost</span> Through-out Life-Cycle Stages for 100 years",
        ]
        
        self.bubble_cards_list = []
        for i, title in enumerate(bubble_titles):
            card = self._create_bubble_card(title)
            self.bubble_cards_list.append(card)
            self.bubble_cards_layout.addWidget(card)
        
        self.bubble_cards_container.setVisible(False)
        content_layout.addWidget(self.bubble_cards_container)
        
        # Bottom navigation buttons
        self.bottom_buttons_widget = self._build_bottom_buttons()
        self.bottom_buttons_widget.setVisible(False)
        content_layout.addWidget(self.bottom_buttons_widget, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Set the scroll content widget to the scroll area
        self.scroll_area.setWidget(self.scroll_content_widget)
        
        # Add scroll area to main layout
        left_panel_vlayout.addWidget(self.scroll_area)
        
        # Connect resize event to handle dynamic layout
        self.resizeEvent = self.handle_resize


        

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    def _build_radial_bar_html(self, percentages):
        # Stage labels and color palette copied from the original script
        stage_label = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage']
        colors = ['#273B5C', '#2E5743', '#996515', '#36454F']

        # Ensure exactly four entries
        values = (percentages + [0, 0, 0, 0])[:4]

        # Size tuned to fit the card nicely with proper height for full visibility
        width = 360
        height = 220
        body_bg = "#FDEFEF"

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<style>
  html, body {{
    overflow: hidden; /* prevent scrollbars in embedded view */
  }}
  body {{
    background: {body_bg};
    font-family: sans-serif;
    margin: 0;
  }}
  .tooltip {{
    position: absolute; text-align: center; padding: 8px; background: white;
    border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); pointer-events: none;
    opacity: 0; font-size: 12px; transform: translateX(-50%);
  }}
</style>
</head>
<body>
  <svg width="{width}" height="{height}"></svg>
  <div class="tooltip"></div>
  <script>{d3_js}</script>
  <script>
    const data = [
      {{ name: '{stage_label[3]}', value: {values[3]}/100, color: '{colors[3]}' }},
      {{ name: '{stage_label[2]}', value: {values[2]}/100, color: '{colors[2]}' }},
      {{ name: '{stage_label[1]}', value: {values[1]}/100, color: '{colors[1]}' }},
      {{ name: '{stage_label[0]}', value: {values[0]}/100, color: '{colors[0]}' }}
    ];
    const barWidth = 10, spacing = 8; const center = {{ x: {width}/2, y: {height}/2 +10 }};
    const svg = d3.select('svg');
    const g = svg.append('g').attr('transform', `translate(${{center.x}},${{center.y}})`);
    const tooltip = d3.select('.tooltip');
    data.forEach((d, i) => {{
      const innerRadius = 40 + i * (barWidth + spacing);
      const outerRadius = innerRadius + barWidth;
      const arcGen = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius).startAngle(0).cornerRadius(10);
      const path = g.append('path').datum(d).attr('fill', d.color).attr('d', arcGen({{ endAngle: 0 }})).attr('class', 'arc');
      path.transition().duration(1200).attrTween('d', function(d) {{ const interpolate = d3.interpolate(0, (d.value * 2 * Math.PI)+0.03); return function(t) {{ return arcGen({{ endAngle: interpolate(t) }}); }}; }});
      const labelX = center.x - 6; const labelY = center.y + (data.length - 1 - i) * (barWidth + spacing) - 80;
      svg.append('text').attr('x', labelX).attr('y', labelY + 5).attr('text-anchor', 'end').attr('class', 'label').text(`${{(d.value * 100).toFixed(2)}}%`);
      path.on('mouseover', function(event, hoveredData) {{ d3.selectAll('.arc').attr('fill', p => p === hoveredData ? p.color : '#ccc'); tooltip.style('opacity', 1).html(`<div style="text-align:center; font-family:sans-serif;"><span style="font-weight: 500;">${{hoveredData.name}}</span><br><span style="color: #638B48; font-size: 13.5px;">Economic Cost: <span style="font-weight: 600;">${{(hoveredData.value * 100).toFixed(1)}}%;</span></span></div>`).style('left', (event.pageX) + 'px').style('top', (event.pageY - 50) + 'px'); }}).on('mousemove', function(event) {{ tooltip.style('left', (event.pageX) + 'px').style('top', (event.pageY - 70) + 'px'); }}).on('mouseout', function() {{ d3.selectAll('.arc').attr('fill', d => d.color); tooltip.style('opacity', 0); }});
    }});
  </script>
</body>
</html>
"""
        return html

    def _build_legend_widget(self) -> QWidget:
        stage_label = ['Initial Stage', 'Use Stage', 'End of Life Stage', 'Beyond Life Stage']
        colors = ['#273B5C', '#2E5743', '#996515', '#36454F']
        legend = QWidget()
        layout = QHBoxLayout(legend)
        layout.setContentsMargins(8, 0, 8, 6)
        layout.setSpacing(16)
        for name, color in zip(stage_label, colors):
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(6)
            swatch = QWidget()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(f"background:{color}; border-radius:3px;")
            label = QLabel(name)
            item_layout.addWidget(swatch)
            item_layout.addWidget(label)
            layout.addWidget(item)
        layout.addStretch(1)
        return legend

    def _build_bottom_buttons(self) -> QWidget:
        """Create bottom navigation buttons widget"""
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(20, 15, 20, 15)
        buttons_layout.setSpacing(15)
        
        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("bottom_nav_button")
        self.back_button.setFixedSize(80, 35)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        
        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("bottom_nav_button")
        self.next_button.setFixedSize(80, 35)
        self.next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_button.clicked.connect(self.go_next)
        
        # Add buttons to layout
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.back_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addStretch(1)
        
        return buttons_widget

    def _build_bar_graph(self) -> QWidget:
        """Create bar graph widget showing life-cycle costs"""
        bar_graph_widget = QWidget()
        bar_graph_layout = QVBoxLayout(bar_graph_widget)
        bar_graph_layout.setContentsMargins(20, 15, 20, 15)
        bar_graph_layout.setSpacing(10)
        
        # Title for the bar graph
        title_label = QLabel("Life-Cycle Costs for 50 years")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bar_graph_layout.addWidget(title_label)
        
        # Create the bar graph using QWebEngineView
        graph_view = QWebEngineView()
        graph_view.setHtml(self._build_bar_graph_html())
        graph_view.setZoomFactor(0.8)
        graph_view.setMinimumHeight(300)
        graph_view.setMaximumHeight(400)
        graph_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        graph_view.setMinimumWidth(500)  # Ensure minimum width for readability
        bar_graph_layout.addWidget(graph_view)
        
        # Store reference for resize handling
        self.bar_graph_view = graph_view
        
        return bar_graph_widget

    def _build_bar_graph_html(self) -> str:
        """Generate HTML for the horizontal bar graph using exact data from bargraph.py"""
        # Extract names and costs from the original bargraph.py data
        name = [
            "Initial Construction Cost", "Initial Carbon Emission Cost", "Time Cost", 
            "Road User Cost", "Periodic Maintenance Costs", "Maintenance Emission Costs",
            "Routine Inspection Costs", "Repair & Rehabilitation Costs", "Reconstruction Costs",
            "Demolition & Disposal Cost", "Recycling Cost", "Total Life-Cycle Cost"
        ]
        cost = [
            61.83, 29.03, 0.0, 123.93, 1.44, 0.0, 0.0, 0.0, 0.0, 18.69, 0.0, 0.0
        ]
        
        # Clean data (include all values except total, but handle zeros specially)
        temp_name = []
        temp_cost = []
        for i in range(len(cost)):
            if i < 11:  # Exclude only the total, include all other values including zeros
                temp_name.append(name[i])
                temp_cost.append(cost[i])
        
        # Display adjustment for zero values (from original code)
        temp_cost_display = []
        cost_list = temp_cost.copy()
        if cost_list:
            # Find minimum non-zero value for display adjustment
            non_zero_costs = [c for c in cost_list if c > 0]
            if non_zero_costs:
                min_non_zero = min(non_zero_costs)
                for j in temp_cost:
                    if j == 0.0:
                        temp_cost_display.append(min_non_zero / 2)
                    else:
                        temp_cost_display.append(j)
            else:
                temp_cost_display = temp_cost
        else:
            temp_cost_display = temp_cost
        
        # Color list from original bargraph.py
        color_list = ['#638B48', '#6F6F6F', '#638B48', '#E09365', '#6F6F6F', '#638B48',
                      '#6F6F6F', '#638B48', '#638B48', '#638B48', '#638B48', '#ffffff']
        
        # Calculate total cost
        total_cost = sum(temp_cost)
        
        # Create data array for D3
        data = []
        for i, (n, c, col) in enumerate(zip(temp_name, temp_cost_display, color_list[:len(temp_name)])):
            data.append({"name": n, "value": c, "color": col})
        
        # Debug: Print the data being processed
        print(f"Original cost data: {cost}")
        print(f"Filtered names: {temp_name}")
        print(f"Filtered costs: {temp_cost}")
        print(f"Display costs: {temp_cost_display}")
        print(f"Number of bars to display: {len(temp_name)}")
        print(f"Data array for D3: {data}")
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset='UTF-8'>
    <title>D3.js Interactive Horizontal Bar Graph</title>
    <style>
        /* General body styling */
        body {{
            font-family: Arial, sans-serif;
        }}

        /* Container for the graph, centers it on the page */
        #myGraph {{
            width: 100%;
            height: 100%;
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

<script>{d3_js}</script>
<script>
    // Original dataset containing names, values (scores), and their corresponding colors.
    const originalData = {data};

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
        return html

    def handle_resize(self, event):
        """Handle window resize events to make layout more responsive"""
        # Get the current width of the widget
        current_width = self.width()
        
        # Only adjust card layout if cards are visible and we have the necessary attributes
        if (hasattr(self, 'cards_container') and 
            hasattr(self, 'cards_layout') and 
            self.cards_container.isVisible() and 
            self.cards_container.layout() is not None):
            
            current_layout = self.cards_container.layout()
            
            if current_width < 1000:  # If window is narrow
                # Stack cards vertically
                if isinstance(current_layout, QHBoxLayout):
                    # Convert to vertical layout
                    new_layout = QVBoxLayout()
                    new_layout.setContentsMargins(0, 0, 0, 0)
                    new_layout.setSpacing(20)
                    
                    # Move all cards to new layout
                    while current_layout.count():
                        item = current_layout.takeAt(0)
                        if item.widget():
                            new_layout.addWidget(item.widget())
                    
                    # Replace the layout
                    self.cards_container.setLayout(new_layout)
                    self.cards_layout = new_layout
                    
                    # Ensure all cards remain visible after layout change
                    for i in range(new_layout.count()):
                        item = new_layout.itemAt(i)
                        if item and item.widget():
                            item.widget().setVisible(True)
                    
            else:  # If window is wide
                # Arrange cards horizontally
                if isinstance(current_layout, QVBoxLayout):
                    # Convert to horizontal layout
                    new_layout = QHBoxLayout()
                    new_layout.setContentsMargins(0, 0, 0, 0)
                    new_layout.setSpacing(20)
                    new_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetNoConstraint)
                    
                    # Move all cards to new layout
                    while current_layout.count():
                        item = current_layout.takeAt(0)
                        if item.widget():
                            new_layout.addWidget(item.widget())
                    
                    # Replace the layout
                    self.cards_container.setLayout(new_layout)
                    self.cards_layout = new_layout
                    
                    # Ensure all cards remain visible after layout change
                    for i in range(new_layout.count()):
                        item = new_layout.itemAt(i)
                        if item and item.widget():
                            item.widget().setVisible(True)
        
        # Call the parent's resize event handler
        super().resizeEvent(event)
        
        # After resize, ensure cards remain visible
        if hasattr(self, 'cards_container') and self.cards_container.isVisible():
            self.ensure_cards_visible()
    
    def ensure_cards_visible(self):
        """Ensure all cards are visible and properly displayed"""
        print("=== ensure_cards_visible called ===")
        
        if hasattr(self, 'cards_container'):
            print(f"Cards container exists: {self.cards_container}")
            print(f"Cards container visible: {self.cards_container.isVisible()}")
            print(f"Cards container parent: {self.cards_container.parent()}")
            
            # Make sure the cards container itself is visible
            self.cards_container.setVisible(True)
            print(f"Cards container set visible: {self.cards_container.isVisible()}")
            
            # Check cards list if available
            if hasattr(self, 'cards_list'):
                print(f"Cards list has {len(self.cards_list)} cards")
                for i, card in enumerate(self.cards_list):
                    print(f"Card {i} in list - visible: {card.isVisible()}, parent: {card.parent()}")
                    card.setVisible(True)
                    print(f"Card {i} set visible: {card.isVisible()}")
            
            # Ensure all child cards in layout are visible
            if hasattr(self, 'cards_layout'):
                layout = self.cards_layout
                print(f"Layout has {layout.count()} items")
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        print(f"Layout item {i}: {widget}, visible: {widget.isVisible()}")
                        widget.setVisible(True)
                        print(f"Layout item {i} set visible: {widget.isVisible()}")
        else:
            print("ERROR: cards_container does not exist!")
        
        print("=== ensure_cards_visible finished ===")

    def _create_result_card(self, title: str, percentages=None) -> QWidget:
        if percentages is None:
            percentages = [30, 45, 15, 10]
        card = QWidget()
        card.setObjectName("result_card")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setMinimumWidth(300)
        card.setMaximumHeight(280)
        
        print(f"Creating card with title: {title[:30]}...")
        print(f"Card object: {card}")
        print(f"Card visible by default: {card.isVisible()}")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 8, 10, 10)
        card_layout.setSpacing(6)

        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        close_btn = QPushButton()
        close_btn.setObjectName("close_card_button")
        close_btn.setIcon(QIcon("resources/close.png"))
        close_btn.setIconSize(QSize(13, 13))
        header_layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

        def remove_card():
            card.setParent(None)
            card.deleteLater()
        close_btn.clicked.connect(remove_card)

        card_layout.addLayout(header_layout)

        # Embed radial bar graph inside the card using QWebEngineView
        graph = QWebEngineView(card)
        graph.setHtml(self._build_radial_bar_html(percentages))
        graph.setZoomFactor(0.6)
        graph.setMinimumHeight(180)
        card_layout.addWidget(graph)
        
        print(f"Card created successfully with graph. Final card visible: {card.isVisible()}")
        print(f"Card size: {card.size()}, Card geometry: {card.geometry()}")

        return card

    def switch_to_results_widget(self):
        self.main_content_widget.setStyleSheet("""
            #main_content_widget {
                background-color: #FDEFEF;
                border: 1px solid #000000;
                border-top: none;
            }
        """)
        
        if self.pressed==0:
            print("=== Switching to results widget ===")
            self.top_button_right_panel.setObjectName("top_button_right_panel_pressed")
            self.welcome_label.setVisible(False)
            
            # Initialize navigation system
            self.current_page = 0
            self.bottom_buttons_widget.setVisible(True)
            self.update_page_display()
            
            self.pressed=1
            print("=== Finished switching to results widget ===")
        else:
            print("=== Switching back to welcome ===")
            self.top_button_right_panel.setObjectName("top_button_right_panel")
            self.hide_all_page_widgets()
            self.bottom_buttons_widget.setVisible(False)
            self.welcome_label.setVisible(True)
            self.pressed=0
            print("=== Finished switching back to welcome ===")
    
    def go_next(self):
        """Handle next button click"""
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_page_display()
    
    def go_back(self):
        """Handle back button click"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_display()
    
    def update_page_display(self):
        """Update the display based on current page"""
        # Hide all widgets first
        self.hide_all_page_widgets()
        
        # Update button states
        self.back_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.max_page)
        
        if self.current_page == 0:
            # Show initial 50-year graphs
            self.cards_container.setVisible(True)
            self.legend_widget.setVisible(True)
            self.bar_graph_widget.setVisible(True)
            self.ensure_cards_visible()
        elif self.current_page == 1:
            # Show pie chart with the original 3 radial cards
            self.cards_container.setVisible(True)
            self.legend_widget.setVisible(True)
            self.pie_chart_widget.setVisible(True)
            self.ensure_cards_visible()
        elif self.current_page == 2:
            # Show 100-year graphs
            self.cards_container_100.setVisible(True)
            self.legend_widget_100.setVisible(True)
            self.bar_graph_widget_100.setVisible(True)
        elif self.current_page == 3:
            # Show bubble graphs
            self.bubble_cards_container.setVisible(True)
    
    def hide_all_page_widgets(self):
        """Hide all page-specific widgets"""
        # Page 0 widgets
        self.cards_container.setVisible(False)
        self.legend_widget.setVisible(False)
        self.bar_graph_widget.setVisible(False)
        
        # Page 1 widgets
        self.pie_chart_widget.setVisible(False)
        
        # Page 2 widgets
        self.cards_container_100.setVisible(False)
        self.legend_widget_100.setVisible(False)
        self.bar_graph_widget_100.setVisible(False)
        
        # Page 3 widgets
        self.bubble_cards_container.setVisible(False)

    def _build_pie_chart(self) -> QWidget:
        """Create pie chart widget"""
        pie_chart_widget = QWidget()
        pie_chart_layout = QVBoxLayout(pie_chart_widget)
        pie_chart_layout.setContentsMargins(20, 15, 20, 15)
        pie_chart_layout.setSpacing(10)
        
        # Title for the pie chart
        title_label = QLabel("Cost Breakdown - Pie Chart")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie_chart_layout.addWidget(title_label)
        
        # Create the pie chart using QWebEngineView
        pie_view = QWebEngineView()
        pie_view.setHtml(self._build_pie_chart_html())
        pie_view.setZoomFactor(0.8)
        pie_view.setMinimumHeight(400)
        pie_view.setMaximumHeight(500)
        pie_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        pie_view.setMinimumWidth(600)
        pie_chart_layout.addWidget(pie_view)
        
        return pie_chart_widget

    def _build_pie_chart_html(self) -> str:
        """Generate HTML for pie chart using code from Pie chart.py"""
        # Sample data based on the pie chart.py format
        data_with_colors = [
            {
                "label": "Road user cost",
                "cost": 123.93,
                "percent": 47.5,
                "color": "#FF8C00",
                "disabled": False
            },
            {
                "label": "Time cost estimate",
                "cost": 2.32,
                "percent": 0.9,
                "color": "#483D8B",
                "disabled": False
            },
            {
                "label": "Embodied carbon emissions",
                "cost": 8.53,
                "percent": 3.3,
                "color": "#B22222",
                "disabled": False
            },
            {
                "label": "Initial construction cost",
                "cost": 61.83,
                "percent": 23.7,
                "color": "#996633",
                "disabled": False
            },
            {
                "label": "Additional CO2 e costs due to rerouting",
                "cost": 29.03,
                "percent": 11.1,
                "color": "#8B0000",
                "disabled": False
            },
            {
                "label": "Periodic Maintenance costs",
                "cost": 1.44,
                "percent": 0.4,
                "color": "#F6FB05",
                "disabled": False
            },
            {
                "label": "Periodic maintenance carbon emissions",
                "cost": 16.99,
                "percent": 6.4,
                "color": "#A52A2A",
                "disabled": False
            },
            {
                "label": "Annual routine inspection costs",
                "cost": 14.32,
                "percent": 5.5,
                "color": "#4682B4",
                "disabled": False
            },
            {
                "label": "Repair and rehabilitation costs",
                "cost": 1.99,
                "percent": 0.8,
                "color": "#008000",
                "disabled": False
            },
            {
                "label": "Demolition and deconstruction costs",
                "cost": 0.77,
                "percent": 0.3,
                "color": "#800080",
                "disabled": False
            }
        ]
        
        import json
        data_js = json.dumps(data_with_colors)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cost Breakdown Pie Chart</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background: #FDEFEF;
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
                        .attr("d", arc)
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
                    // Reset all slices
                    svg.selectAll(".arc")
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .attr("fill", arc => arc.data.color)
                        .attr("stroke-width", 1)
                        .attr("d", arc);
                    
                    tooltip.classed("visible", false);
                }}
                
                // Start the chart
                initializeChart();
            </script>
        </body>
        </html>
        """
        return html

    def _build_bar_graph_100(self) -> QWidget:
        """Create 100-year bar graph widget"""
        bar_graph_widget = QWidget()
        bar_graph_layout = QVBoxLayout(bar_graph_widget)
        bar_graph_layout.setContentsMargins(20, 15, 20, 15)
        bar_graph_layout.setSpacing(10)
        
        # Title for the bar graph
        title_label = QLabel("Life-Cycle Costs for 100 years")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bar_graph_layout.addWidget(title_label)
        
        # Create the bar graph using QWebEngineView
        graph_view = QWebEngineView()
        graph_view.setHtml(self._build_bar_graph_100_html())
        graph_view.setZoomFactor(0.8)
        graph_view.setMinimumHeight(300)
        graph_view.setMaximumHeight(400)
        graph_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        graph_view.setMinimumWidth(500)
        bar_graph_layout.addWidget(graph_view)
        
        return bar_graph_widget

    def _build_bar_graph_100_html(self) -> str:
        """Generate HTML for the 100-year horizontal bar graph"""
        # Use similar data but adjusted for 100 years
        name = [
            "Initial Construction Cost", "Initial Carbon Emission Cost", "Time Cost", 
            "Road User Cost", "Periodic Maintenance Costs", "Maintenance Emission Costs",
            "Routine Inspection Costs", "Repair & Rehabilitation Costs", "Reconstruction Costs",
            "Demolition & Disposal Cost", "Recycling Cost"
        ]
        # Doubled costs for 100 years simulation
        cost = [
            61.83, 29.03, 0.0, 247.86, 2.88, 0.0, 0.0, 0.0, 0.0, 18.69, 0.0
        ]
        
        # Clean data 
        temp_name = name[:11]  # Exclude total
        temp_cost = cost[:11]
        
        # Display adjustment for zero values
        temp_cost_display = []
        if temp_cost:
            non_zero_costs = [c for c in temp_cost if c > 0]
            if non_zero_costs:
                min_non_zero = min(non_zero_costs)
                for j in temp_cost:
                    if j == 0.0:
                        temp_cost_display.append(min_non_zero / 2)
                    else:
                        temp_cost_display.append(j)
            else:
                temp_cost_display = temp_cost
        else:
            temp_cost_display = temp_cost
        
        # Color list
        color_list = ['#638B48', '#6F6F6F', '#638B48', '#E09365', '#6F6F6F', '#638B48',
                      '#6F6F6F', '#638B48', '#638B48', '#638B48', '#638B48']
        
        # Create data array for D3
        data = []
        for i, (n, c, col) in enumerate(zip(temp_name, temp_cost_display, color_list[:len(temp_name)])):
            data.append({"name": n, "value": c, "color": col})
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset='UTF-8'>
            <title>D3.js Interactive Horizontal Bar Graph - 100 Years</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #FDEFEF;
                }}
                #myGraph {{
                    width: 100%;
                    height: 100%;
                    position: relative;
                }}
                .bar {{
                    transition: fill 0.3s ease;
                }}
                .axis text {{
                    font-size: 11px;
                    fill: #333;
                }}
                .axis path, .axis line {{
                    fill: none;
                    stroke: #ccc;
                    shape-rendering: crispEdges;
                }}
                .tooltip {{
                    position: absolute;
                    text-align: center;
                    padding: 8px;
                    font-size: 12px;
                    background: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    pointer-events: none;
                    color: black;
                    opacity: 0;
                    transition: opacity 0.2s;
                    white-space: nowrap;
                }}
                .bar-label {{
                    user-select: none;
                    -moz-user-select: none;
                    -webkit-user-select: none;
                    -ms-user-select: none;
                }}
            </style>
        </head>
        <body>
        <h2 style="text-align: center;">Life Cycle Cost for 100 Years</h2>
        <div id="myGraph"></div>
        <script>{d3_js}</script>
        <script>
            const originalData = {data};
            const data = [...originalData].reverse();
            const dimColor = 'rgba(200,200,200,0.4)';
            const margin = {{ top: 50, right: 60, bottom: 50, left: 100 }};
            const myGraphDiv = d3.select("#myGraph");
            const divWidth = myGraphDiv.node().getBoundingClientRect().width;
            const width = divWidth - margin.left - margin.right;
            const itemHeight = 30;
            const minChartHeight = 200;
            const calculatedChartHeight = data.length * itemHeight;
            const height = Math.max(minChartHeight, calculatedChartHeight);

            const svg = myGraphDiv
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .style("background-color", "#F0E6E6")
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            svg.append("rect")
                .attr("width", width)
                .attr("height", height)
                .attr("fill", "#F0E6E6");

            const x = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.value) * 1.1])
                .range([0, width]);

            const y = d3.scaleBand()
                .domain(data.map(d => d.name))
                .range([height, 0])
                .paddingInner(0.2);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", `translate(0,${{height}})`)
                .style("opacity", 0)
                .call(d3.axisBottom(x))
                .append("text")
                .attr("x", width / 2)
                .attr("y", 40)
                .attr("fill", "black")
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .text("Cost in Lakhs");

            svg.append("g")
                .attr("class", "y axis")
                .style("opacity", 0)
                .call(d3.axisLeft(y))
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", -60)
                .attr("x", -(height / 2))
                .attr("dy", "1em")
                .attr("fill", "black")
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .text("");

            svg.select(".y.axis").selectAll("text").filter(function() {{
                return d3.select(this).text() !== "Name";
            }}).remove();
            svg.select(".y.axis").selectAll("line").remove();

            const tooltip = d3.select("body").append("div")
                .attr("class", "tooltip");

            const bars = svg.selectAll(".bar")
                .data(data)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", 0)
                .attr("y", d => y(d.name))
                .attr("width", 0)
                .attr("height", y.bandwidth())
                .attr("fill", d => d.color);

            const textPadding = 5;
            const textLabels = svg.selectAll(".bar-label")
                .data(data)
                .enter()
                .append("text")
                .attr("class", "bar-label")
                .attr("y", d => y(d.name) + y.bandwidth() / 2)
                .attr("dy", "0.35em")
                .style("font-family", "Arial, sans-serif")
                .style("font-size", "12px")
                .style("text-anchor", "start")
                .style("opacity", 0)
                .text(d => d.name);

            bars.transition()
                .duration(1500)
                .ease(d3.easeElastic.amplitude(0.5).period(0.5))
                .attr("width", d => x(d.value));

            svg.selectAll(".axis")
                .transition()
                .duration(1000)
                .delay(1000)
                .style("opacity", 1);

            textLabels.transition()
                .duration(800)
                .delay((d, i) => 800 + (i * 100))
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

            textLabels.attr("x", function(d) {{
                const textWidth = this.getBBox().width;
                const barWidth = x(d.value);
                if (barWidth > textWidth + textPadding) {{
                    return textPadding;
                }} else {{
                    return barWidth + textPadding;
                }}
            }});

            function handleMouseOver(event, d_hovered_element) {{
                bars.transition().duration(100).attr("fill", bar_d => {{
                    return bar_d === d_hovered_element ? bar_d.color : dimColor;
                }});
                tooltip.html(`<b>${{d_hovered_element.name}}</b>: ${{d_hovered_element.value}} Lakh`);
                tooltip.style("opacity", 1);
            }}

            function handleMouseOut() {{
                bars.transition().duration(100).attr("fill", bar_d => bar_d.color);
                tooltip.style("opacity", 0);
            }}

            function handleMouseMove(event, d) {{
                const barX = x(d.value);
                const barY = y(d.name);
                const graphRect = myGraphDiv.node().getBoundingClientRect();
                const tooltipRect = tooltip.node().getBoundingClientRect();
                let tooltipLeft = graphRect.left + margin.left + barX - (tooltipRect.width / 2);
                let tooltipTop = graphRect.top + margin.top + barY - (tooltipRect.height + 8);
                if (tooltipLeft < 0) tooltipLeft = 0;
                if (tooltipLeft + tooltipRect.width > window.innerWidth) tooltipLeft = window.innerWidth - tooltipRect.width;
                tooltip.style("left", tooltipLeft + "px")
                       .style("top", tooltipTop + "px");
            }}

            bars.on("mouseover", handleMouseOver)
                .on("mouseout", handleMouseOut)
                .on("mousemove", handleMouseMove);

            textLabels.on("mouseover", handleMouseOver)
                      .on("mouseout", handleMouseOut)
                      .on("mousemove", handleMouseMove);
        </script>
        </body>
        </html>
        """
        return html

    def _create_bubble_card(self, title: str) -> QWidget:
        """Create a bubble chart card"""
        card = QWidget()
        card.setObjectName("result_card")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setMinimumWidth(420)
        card.setMaximumHeight(380)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 8, 10, 10)
        card_layout.setSpacing(6)

        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        close_btn = QPushButton()
        close_btn.setObjectName("close_card_button")
        close_btn.setIcon(QIcon("resources/close.png"))
        close_btn.setIconSize(QSize(13, 13))
        header_layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

        def remove_card():
            card.setParent(None)
            card.deleteLater()
        close_btn.clicked.connect(remove_card)

        card_layout.addLayout(header_layout)

        # Embed bubble graph inside the card using QWebEngineView
        graph = QWebEngineView(card)
        graph.setHtml(self._build_bubble_graph_html())
        graph.setZoomFactor(0.8)
        graph.setMinimumHeight(320)
        card_layout.addWidget(graph)

        return card

    def _build_bubble_graph_html(self) -> str:
        """Generate HTML for bubble graph using code from Bubble graph.py"""
        # Sample data based on bubble graph.py
        val_a, val_b, val_c = 53.71, 40.4, 6.4
        cost_a, cost_b, cost_c = 29.03, 19.36, 16.99
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Bubble Chart Layout</title>
          <script>{d3_js}</script>
          <style>
            body {{
              font-family: sans-serif;
              background: #FDEFEF;
              margin: 0;
              overflow: hidden;
            }}
            #chart-container {{
              position: relative;
              width: 100%;
              height: 100%;
            }}
            #legend {{
              position: absolute;
              right: 20px;
              bottom: 20px;
              font-size: 11px;
              line-height: 1.6;
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
              font-size: 12px;
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
              font-size: 14px;
            }}
            .tooltip b {{
              font-size: 16px;
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
              {{ name: 'A', value: {val_a}, x: 250, y: 170, label:'Initial Carbon Emission Cost' , cost: {cost_a}}}, 
              {{ name: 'B', value: {val_b}, x: 200, y: 90, label:'Carbon Emission due to Re-Routing' , cost: {cost_b}}}, 
              {{ name: 'C', value: {val_c}, x: 150, y: 150, label:'Maintenance Emission Costs' , cost: {cost_c}}}
            ];

            const svgWidth = 400, svgHeight = 250;
            const radiusScale = d3.scaleLinear()
              .domain([0, d3.max(data, d => d.value)])
              .range([20, 45]);

            const svg = d3.select("#chart")
              .append("svg")
              .attr("width", svgWidth)
              .attr("height", svgHeight);

            svg.append("circle")
              .attr("cx", 200)
              .attr("cy", 125)
              .attr("r", 120)
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

            groups.selectAll("circle")
              .on("mouseover", function (event, d) {{
                tooltip
                  .html(`<strong>${{d.label}}</strong><br><b>${{d.cost}} Lakh; ${{d.value}} %</b>`)
                  .style("left", (event.pageX - 80) + "px")
                  .style("top", (event.pageY - 60) + "px")
                  .classed("visible", true);

                groups.selectAll("circle")
                  .transition()
                  .duration(200)
                  .style("fill", c => c === d ? "#808000" : "#ccc");

                d3.select(this)
                  .transition()
                  .duration(200)
                  .attr("r", radiusScale(d.value) * 1.1);
              }})
              .on("mousemove", function (event) {{
                tooltip
                  .style("left", (event.pageX - 80) + "px")
                  .style("top", (event.pageY - 60) + "px");
              }})
              .on("mouseout", function (event, d) {{
                tooltip.classed("visible", false);
                groups.selectAll("circle")
                  .transition()
                  .duration(100)
                  .style("fill", "#808000")
                  .attr("r", c => radiusScale(c.value));
              }});

            groups.append("text")
              .text(d => d.name)
              .attr("text-anchor", "middle")
              .attr("dy", ".35em")
              .style("fill", "white")
              .style("opacity", 0)
              .style("font-size", "10px")
              .transition()
              .delay((_, i) => i * 300 + 500)
              .duration(700)
              .style("opacity", 1)
              .style("font-size", "14px");
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

        self.main_h_layout.addWidget(ResultsWidget(), 2)

        self.setWindowState(Qt.WindowMaximized)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec()) 