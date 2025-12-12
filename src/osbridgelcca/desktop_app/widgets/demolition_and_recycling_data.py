from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon
from .utils.data import *
import sys
import os

class DemolitionAndRecyclingData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    def __init__(self, database, parent=None):
        super().__init__()
        self.parent = parent
        self.database_manager = database
        self.widgets = []

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
                background-color: transparent;
                outline: none;
            }
            #scroll_content_widget {
                background-color: #FFF9F9;
                border: 1px solid #000000;
                padding-bottom: 20px;
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

            QPushButton#top_button_left_panel {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_left_panel:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_left_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }

            /* Updated Styling for navigation buttons to match the Add Material/Component buttons */
            QPushButton#nav_button {
                background-color: #FFFFFF; /* White background */
                border: 1px solid #E0E0E0; /* Light grey border */
                border-radius: 8px; /* Slightly more rounded corners */
                color: #3F3E5E; /* Dark text color */
                padding: 6px 15px; /* Increased padding */
                text-align: center;
                min-width: 80px; /* Ensure a minimum width */
            }
            QPushButton#nav_button:hover {
                background-color: #F8F8F8; /* Very subtle light grey on hover */
                border-color: #C0C0C0; /* Darker border on hover */
            }
            QPushButton#nav_button:pressed {
                background-color: #E8E8E8; /* Darker grey on pressed */
                border-color: #A0A0A0; /* Even darker border */
            }
            /* (Removed: QComboBox and material grid element CSS) */
        """)

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        # --- Add General Info Form at the top of the scroll area ---
        self.general_widget = QWidget()
        self.general_layout = QVBoxLayout(self.general_widget)
        self.general_layout.setContentsMargins(10, 20, 10, 10)
        self.general_layout.setSpacing(10)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(20)

        field_width = 200 # More compact width for input fields

        # 1. Demolition and Disposal Rate
        label = QLabel("Demolition and Disposal Cost\n(Percentage of Initial Construction Cost)")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 0, 0, 1, 1)
        demolition_widget = QWidget(self.general_widget)
        demolition_layout = QHBoxLayout(demolition_widget)
        demolition_layout.setContentsMargins(0,0,0,0)
        demolition_layout.setSpacing(10)
        demolition_input = QLineEdit()
        self.widgets.append(demolition_input)
        demolition_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        demolition_input.setFixedWidth(field_width)
        demolition_input.setText("10")
        demolition_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        demolition_layout.addWidget(demolition_input)
        demolition_layout.addWidget(QLabel("(%)"))
        suggested_label = QLabel("Suggested")
        suggested_label.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        demolition_layout.addWidget(suggested_label)
        demolition_layout.addStretch(1)
        grid_layout.addWidget(demolition_widget, 0, 1, 1, 1, alignment=Qt.AlignLeft)

        # 2. Structural Steel Scrap Rate
        label = QLabel("Structural Steel Scrap Rate")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 1, 0, 1, 1)
        scrap_value_widget = QWidget(self.general_widget)
        scrap_value_layout = QHBoxLayout(scrap_value_widget)
        scrap_value_layout.setContentsMargins(0,0,0,0)
        scrap_value_layout.setSpacing(10)
        scrap_value_input = QLineEdit()
        self.widgets.append(scrap_value_input)
        scrap_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        scrap_value_input.setFixedWidth(field_width)
        scrap_value_input.setText("26000")
        scrap_value_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        scrap_value_layout.addWidget(scrap_value_input)
        scrap_value_layout.addWidget(QLabel("(INR/MT)"))
        suggested_label2 = QLabel("Suggested")
        suggested_label2.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        scrap_value_layout.addWidget(suggested_label2)
        scrap_value_layout.addStretch(1)
        grid_layout.addWidget(scrap_value_widget, 1, 1, 1, 1, alignment=Qt.AlignLeft)

        # 3. Structural Steel Recylability
        label = QLabel("Structural Steel Recylability")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 2, 0, 1, 1)
        steel_scrap_widget = QWidget(self.general_widget)
        steel_scrap_layout = QHBoxLayout(steel_scrap_widget)
        steel_scrap_layout.setContentsMargins(0,0,0,0)
        steel_scrap_layout.setSpacing(10)
        steel_scrap_input = QLineEdit()
        self.widgets.append(steel_scrap_input)
        steel_scrap_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        steel_scrap_input.setFixedWidth(field_width)
        steel_scrap_input.setText("95")
        steel_scrap_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        steel_scrap_layout.addWidget(steel_scrap_input)
        steel_scrap_layout.addWidget(QLabel("(%)"))
        suggested_label3 = QLabel("Suggested")
        suggested_label3.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        steel_scrap_layout.addWidget(suggested_label3)
        steel_scrap_layout.addStretch(1)
        grid_layout.addWidget(steel_scrap_widget, 2, 1, 1, 1, alignment=Qt.AlignLeft)

        # 4. Steel Rebar Scrap Rate
        label = QLabel("Steel Rebar Scrap Rate")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 3, 0, 1, 1)
        scrap_value_widget = QWidget(self.general_widget)
        scrap_value_layout = QHBoxLayout(scrap_value_widget)
        scrap_value_layout.setContentsMargins(0,0,0,0)
        scrap_value_layout.setSpacing(10)
        scrap_value_input = QLineEdit()
        self.widgets.append(scrap_value_input)
        scrap_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        scrap_value_input.setFixedWidth(field_width)
        scrap_value_input.setText("32500")
        scrap_value_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        scrap_value_layout.addWidget(scrap_value_input)
        scrap_value_layout.addWidget(QLabel("(INR/MT)"))
        suggested_label2 = QLabel("Suggested")
        suggested_label2.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        scrap_value_layout.addWidget(suggested_label2)
        scrap_value_layout.addStretch(1)
        grid_layout.addWidget(scrap_value_widget, 3, 1, 1, 1, alignment=Qt.AlignLeft)

        # 4. Steel Rebar Recylability
        label = QLabel("Steel Rebar Recylability")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 4, 0, 1, 1)
        steel_scrap_widget = QWidget(self.general_widget)
        steel_scrap_layout = QHBoxLayout(steel_scrap_widget)
        steel_scrap_layout.setContentsMargins(0,0,0,0)
        steel_scrap_layout.setSpacing(10)
        steel_scrap_input = QLineEdit()
        self.widgets.append(steel_scrap_input)
        steel_scrap_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        steel_scrap_input.setFixedWidth(field_width)
        steel_scrap_input.setText("75")
        steel_scrap_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        steel_scrap_layout.addWidget(steel_scrap_input)
        steel_scrap_layout.addWidget(QLabel("(%)"))
        suggested_label3 = QLabel("Suggested")
        suggested_label3.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        steel_scrap_layout.addWidget(suggested_label3)
        steel_scrap_layout.addStretch(1)
        grid_layout.addWidget(steel_scrap_widget, 4, 1, 1, 1, alignment=Qt.AlignLeft)

        # 5. Pre Stressed Tendons Scrap Rate
        label = QLabel("Pre Stressed Tendons Scrap Rate")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 5, 0, 1, 1)
        steel_scrap_widget = QWidget(self.general_widget)
        steel_scrap_layout = QHBoxLayout(steel_scrap_widget)
        steel_scrap_layout.setContentsMargins(0,0,0,0)
        steel_scrap_layout.setSpacing(10)
        steel_scrap_input = QLineEdit()
        self.widgets.append(steel_scrap_input)
        steel_scrap_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        steel_scrap_input.setFixedWidth(field_width)
        steel_scrap_input.setText("32500")
        steel_scrap_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        steel_scrap_layout.addWidget(steel_scrap_input)
        steel_scrap_layout.addWidget(QLabel("(INR/MT)"))
        suggested_label3 = QLabel("Suggested")
        suggested_label3.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        steel_scrap_layout.addWidget(suggested_label3)
        steel_scrap_layout.addStretch(1)
        grid_layout.addWidget(steel_scrap_widget, 5, 1, 1, 1, alignment=Qt.AlignLeft)

        # 6. Pre Stressed Tendons Recylability
        label = QLabel("Pre Stressed Tendons Recylability")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 6, 0, 1, 1)
        steel_scrap_widget = QWidget(self.general_widget)
        steel_scrap_layout = QHBoxLayout(steel_scrap_widget)
        steel_scrap_layout.setContentsMargins(0,0,0,0)
        steel_scrap_layout.setSpacing(10)
        steel_scrap_input = QLineEdit()
        self.widgets.append(steel_scrap_input)
        steel_scrap_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        steel_scrap_input.setFixedWidth(field_width)
        steel_scrap_input.setText("60")
        steel_scrap_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        steel_scrap_layout.addWidget(steel_scrap_input)
        steel_scrap_layout.addWidget(QLabel("(%)"))
        suggested_label3 = QLabel("Suggested")
        suggested_label3.setStyleSheet("color: #B3AEAE; font-size: 10px;")
        steel_scrap_layout.addWidget(suggested_label3)
        steel_scrap_layout.addStretch(1)
        grid_layout.addWidget(steel_scrap_widget, 6, 1, 1, 1, alignment=Qt.AlignLeft)

        self.general_layout.addLayout(grid_layout)
        self.general_layout.addStretch(1)
        self.scroll_content_layout.addWidget(self.general_widget, alignment=Qt.AlignLeft)

        # Create the navigation buttons layout
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(10,10,10,10)

        # Adjust these stretch factors to control the position
        self.button_h_layout.addStretch(6) # Larger stretch on the left to push it more right

        back_button = QPushButton("Back")
        back_button.setObjectName("nav_button")
        back_button.clicked.connect(lambda: self.back.emit(KEY_DEMOLITION_RECYCLE))
        self.button_h_layout.addWidget(back_button)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.collect_data)
        calculate_button.setObjectName("nav_button")
        self.button_h_layout.addWidget(calculate_button)

        # Add initial spacing before the navigation buttons
        self.scroll_content_layout.addLayout(self.button_h_layout)

        # --- Add a corner spacer to the scroll_content_layout ---
        self.button_h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)


    def collect_data(self):
        from pprint import pprint
        data = {
            KEY_DEMOLITION_DISPOSAL_COST: 0.0 if not self.widgets[0].text() else float(self.widgets[0].text())/100,
            KEY_STRUCT_STEEL_SCRAP_RATE: 0.0 if not self.widgets[1].text() else float(self.widgets[1].text()),
            KEY_STRUCT_STEEL_RECYLABILITY: 0.0 if not self.widgets[2].text() else float(self.widgets[2].text())/100,
            KEY_STEEL_REBAR_SCRAP_RATE: 0.0 if not self.widgets[3].text() else float(self.widgets[3].text()),
            KEY_STEEL_REBAR_RECYLABILITY: 0.0 if not self.widgets[4].text() else float(self.widgets[4].text())/100,
            KEY_PS_TENDONS_SCRAP_RATE: 0.0 if not self.widgets[5].text() else float(self.widgets[5].text()),
            KEY_PS_TENDONS_RECYLABILITY: 0.0 if not self.widgets[6].text() else float(self.widgets[6].text())/100
        }
        
        print("\nCollected Data from Demolition & Recycling UI:")
        pprint(data) 

        # Save UI Data to Backend
        self.database_manager.demolition_and_recycling_data = data

        # Demolition and Disposal Cost
        self.database_manager.demolition_and_disposal_cost()

        # Demolition and Disposal related Carbon Emission
        self.database_manager.demolition_disposal_carbon_emission_cost()

        # Carbon Emission due to Rerouting during Demolition and Disposal
        self.database_manager.demolition_disposal_rerouting_carbon_emission_cost()

        # Recycling Cost
        self.database_manager.recycling_cost()

        
        print("Results:\n")
        pprint(self.database_manager.results)

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

        self.main_h_layout.addWidget(DemolitionAndRecyclingData(), 2)

        self.setWindowState(Qt.WindowMaximized)

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)
