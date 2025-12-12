from math import comb
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon, QIntValidator
from .utils.data import *
import sys
import os

class BridgeAndTrafficData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    def __init__(self, database, parent=None):
        super().__init__()
        self.parent = parent
        self.database_manager = database
        self.data = bridge_traffic_data.get(KEY_BRIDGE_TRAFFIC)
        self.widgets = []
        self.vehicle_distribution = []
        self.accident_distribution = []

        self.text_box_width = 200
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

            /* QComboBox global style with country_arrow.png as dropdown arrow */
            QComboBox {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                color: #000000;
                padding: 3px 10px;
            }
            QComboBox::drop-down {
                border: none;
                color: #000000;
                padding-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(resources/country_arrow.png);
                width: 18px;
                height: 18px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #DDDCE0;
                border-radius: 5px;
                color: #000000;
                background-color: #FFFFFF;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                color: #000000;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #FDEFEF;
                color: #000000;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FDEFEF;
            }
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

        # Number of Lanes
        label = QLabel("Alternate Road Carriageway")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 0, 0, 1, 1)

        valuer_combo = QComboBox(self.general_widget)
        self.widgets.append(valuer_combo)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItems(self.data[KEY_LANES][KEY_OPTIONS])
        grid_layout.addWidget(valuer_combo, 0, 1, 1, 1)

        info_icon = QLabel(" ")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 0, 2, 1, 1)

        # Additional Re-Route Distance
        label = QLabel("Additional Re-Route Distance")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 1, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        self.widgets.append(input_widget)
        input_widget.setFixedWidth(self.text_box_width)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 1, 1, 1, 1)
        info_icon = QLabel("(km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 1, 2, 1, 1)

        # Additional Travel Time
        label = QLabel("Additional Travel Time")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 2, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        self.widgets.append(input_widget)
        input_widget.setFixedWidth(self.text_box_width)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 2, 1, 1, 1)
        info_icon = QLabel("(min)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 2, 2, 1, 1)

        # Road Roughness
        label = QLabel("Road Roughness")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 3, 0, 1, 1)

        valuer_combo = QComboBox(self.general_widget)
        self.widgets.append(valuer_combo)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItems(self.data[KEY_ROADROUGHNESS][KEY_OPTIONS] + ["Custom"])
        valuer_combo.currentIndexChanged.connect(lambda index,combo=valuer_combo: self.custom_combo_input(index, combo))
        grid_layout.addWidget(valuer_combo, 3, 1, 1, 1)

        info_icon = QLabel("(mm/km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 3, 2, 1, 1)

        # Road Rise
        label = QLabel("Road Rise")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 4, 0, 1, 1)

        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItems(self.data[KEY_ROAD_RISE_AND_FALL][KEY_OPTIONS] + ["Custom"])
        valuer_combo.currentIndexChanged.connect(lambda index,combo=valuer_combo: self.custom_combo_input(index, combo))
        self.widgets.append(valuer_combo)
        grid_layout.addWidget(valuer_combo, 4, 1, 1, 1)

        info_icon = QLabel("(m/km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 4, 2, 1, 1)

        # Road Fall
        label = QLabel("Road Fall")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 5, 0, 1, 1)

        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItems(self.data[KEY_ROAD_RISE_AND_FALL][KEY_OPTIONS] + ["Custom"])
        valuer_combo.currentIndexChanged.connect(lambda index,combo=valuer_combo: self.custom_combo_input(index, combo))
        self.widgets.append(valuer_combo)
        grid_layout.addWidget(valuer_combo, 5, 1, 1, 1)

        info_icon = QLabel("(m/km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 5, 2, 1, 1)

        # Type of Road
        label = QLabel("Type of Road")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 6, 0, 1, 1)

        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItems(self.data[KEY_TYPE_OF_ROAD][KEY_OPTIONS])
        grid_layout.addWidget(valuer_combo, 6, 1, 1, 1)
        self.widgets.append(valuer_combo)     

        info_icon = QLabel(" ")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 6, 2, 1, 1)

        # Crash Rate
        label = QLabel("Crash Rate")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 7, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setFixedWidth(self.text_box_width)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        self.widgets.append(input_widget)
        grid_layout.addWidget(input_widget, 7, 1, 1, 1)
        info_icon = QLabel("(accidents/million km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 7, 2, 1, 1)


        # Category of accidents=Start==============================================================

        # Composition of Various Vehicles
        composition_row_widget = QWidget(self.general_widget)
        composition_row_layout = QHBoxLayout(composition_row_widget)
        composition_row_layout.setContentsMargins(0, 0, 0, 0)
        composition_row_layout.setSpacing(20)  # Space between label and box
        
        # The white box (vehicle_widget) as before
        vehicle_widget = QWidget(self.general_widget)
        vehicle_widget.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 1px solid #DDDCE0;")
        vehicle_layout = QGridLayout(vehicle_widget)
        vehicle_layout.setContentsMargins(8, 8, 8, 8)
        
        vehicle_type_label = QLabel("Type of Accident")
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setStyleSheet("""
            QLabel {
                border: 0px;
                padding: 3px 10px;
            }
        """)

        per_dist_label = QLabel("Percentage Accident Distribution")
        per_dist_label.setAlignment(Qt.AlignCenter)
        per_dist_label.setStyleSheet("""
            QLabel {
                border: 0px;
                padding: 3px 10px;
            }
        """)

        vehicle_layout.addWidget(vehicle_type_label, 0, 0)
        vehicle_layout.addWidget(per_dist_label, 0, 1)

        vehicles = [
            KEY_MINOR_INJURY,
            KEY_MAJOR_INJURY,
            KEY_FATAL
        ]

        for i, vehicle in enumerate(vehicles):
            v_label = QLabel(f"{vehicle}:")
            v_label.setFixedHeight(40)
            v_label.setAlignment(Qt.AlignCenter)
            v_label.setStyleSheet("background-color: #FFFFFF; border: 1px solid #FFFFFF; border-radius: 10px; padding: 10px 10px 10px 1px;")
            v0_input = QLineEdit()
            self.vehicle_distribution.append(v0_input)
            v0_input.setFixedWidth(self.text_box_width*2)
            v0_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #DDDCE0;
                    border-radius: 10px;
                    padding: 3px 10px;
                    background: #FFFFFF;
                }
            """)
            vehicle_layout.addWidget(v_label, i+1, 0)
            vehicle_layout.addWidget(v0_input, i+1, 1)

        v_label1 = QLabel("")
        v_label1.setStyleSheet(" padding: 10px 10px 10px 1px;")

        composition_row_layout.addWidget(vehicle_widget, alignment=Qt.AlignTop)

        # Add the composition_row_widget to the main grid, spanning columns 0-2
        grid_layout.addWidget(v_label1, 8, 4, 1, 4)
        grid_layout.addWidget(composition_row_widget, 8, 0, 1, 4)

        # Category of accidents=End==============================================================

        # Vehicle =Start================================================================
        
        # Composition of Various Vehicles
        composition_row_widget = QWidget(self.general_widget)
        composition_row_layout = QHBoxLayout(composition_row_widget)
        composition_row_layout.setContentsMargins(0, 0, 0, 0)
        composition_row_layout.setSpacing(20)  # Space between label and box
        
        # The white box (vehicle_widget) as before
        vehicle_widget = QWidget(self.general_widget)
        vehicle_widget.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 1px solid #DDDCE0;")
        vehicle_layout = QGridLayout(vehicle_widget)
        vehicle_layout.setContentsMargins(8, 8, 8, 8)

        vehicle_type_label = QLabel("Type of Vehicle")
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setStyleSheet("""
            QLabel {
                border: 0px;
                padding: 3px 10px;
            }
        """)

        composition_label = QLabel("Composition of Various Vehicles")
        composition_label.setAlignment(Qt.AlignCenter)
        composition_label.setStyleSheet("""
            QLabel {
                border: 0px;
                padding: 3px 10px;
            }
        """)

        per_dist_label = QLabel("Percentage Accident Distribution")
        per_dist_label.setAlignment(Qt.AlignCenter)
        per_dist_label.setStyleSheet("""
            QLabel {
                border: 0px;
                padding: 3px 10px;
            }
        """)

        vehicle_layout.addWidget(vehicle_type_label, 0, 0)
        vehicle_layout.addWidget(composition_label, 0, 1)
        vehicle_layout.addWidget(per_dist_label, 0, 2)

        vehicles = [
            KEY_TWO_WHEELER,
            KEY_SMALL_CARS,
            KEY_BIG_CARS,
            KEY_ORDINARY_BUS,
            KEY_DELUXE_BUS,
            KEY_LCV,
            KEY_MCV,
            KEY_HCV
        ]
        self.average_daily_traffic = []

        for i, vehicle in enumerate(vehicles):
            v_label = QLabel(f"{vehicle}:")
            v_label.setFixedHeight(40)
            v_label.setAlignment(Qt.AlignCenter)
            v_label.setStyleSheet("background-color: #FFFFFF; border: 1px solid #FFFFFF; border-radius: 10px; padding: 10px 10px 10px 1px;")
            v0_input = QLineEdit()
            v0_input.setValidator(QIntValidator(v0_input))
            self.average_daily_traffic.append(v0_input)
            v0_input.setFixedWidth(self.text_box_width)
            v0_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #DDDCE0;
                    border-radius: 10px;
                    padding: 3px 10px;
                    background: #FFFFFF;
                }
            """)
            v1_input = QLineEdit()
            self.vehicle_distribution.append(v1_input)
            v1_input.setFixedWidth(self.text_box_width)
            v1_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #DDDCE0;
                    border-radius: 10px;
                    padding: 3px 10px;
                    background: #FFFFFF;
                }
            """)
            vehicle_layout.addWidget(v_label, i+1, 0)
            vehicle_layout.addWidget(v0_input, i+1, 1)
            vehicle_layout.addWidget(v1_input, i+1, 2)
        
        v_label1 = QLabel("(Vehicles/Day)")
        v_label1.setStyleSheet(" padding: 10px 10px 10px 1px;")

        composition_row_layout.addWidget(vehicle_widget, alignment=Qt.AlignTop)

        # Add the composition_row_widget to the main grid, spanning columns 0-2
        grid_layout.addWidget(v_label1, 9, 4, 1, 4)
        grid_layout.addWidget(composition_row_widget, 9, 0, 1, 4)

        # Vehicle Data=End==============================================================

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
        back_button.clicked.connect(lambda: self.back.emit(KEY_BRIDGE_TRAFFIC))
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.collect_data)
        next_button.clicked.connect(lambda: self.next.emit(KEY_BRIDGE_TRAFFIC))
        self.button_h_layout.addWidget(next_button)

        # Add initial spacing before the navigation buttons
        self.scroll_content_layout.addLayout(self.button_h_layout)

        # --- Add a corner spacer to the scroll_content_layout ---
        self.button_h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)
    
    def custom_combo_input(self, index, combo):
        if combo.itemText(index) == "Custom":
            combo.setEditable(True)
            combo.lineEdit().setText("")
            combo.lineEdit().setPlaceholderText("Type here...")
    
    def collect_data(self):
        from pprint import pprint
        traffic_data = {
            KEY_TWO_WHEELER: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[0].text()),
            KEY_SMALL_CARS: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[1].text()),
            KEY_BIG_CARS: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[2].text()),
            KEY_ORDINARY_BUS: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[3].text()),
            KEY_DELUXE_BUS: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[3].text()),
            KEY_LCV: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[4].text()),
            KEY_HCV: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[5].text()),
            KEY_MCV: 0 if not self.average_daily_traffic[0].text() else int(self.average_daily_traffic[6].text())
        }
        # Collect other data
        data = {
            KEY_ALTER_ROAD_CARRIAGEWAY: self.widgets[0].currentText(), # String
            KEY_ADDIT_REROUTING_DISTANCE: 0.0 if not self.widgets[1].text() else float(self.widgets[1].text()),
            KEY_ADDIT_TRAVEL_TIME: 0.0 if not self.widgets[2].text() else float(self.widgets[2].text())/60, # hours
            KEY_ROAD_ROUGHNESS: self.widgets[3].currentText(),
            KEY_ROAD_RISE: self.widgets[4].currentText(),
            KEY_ROAD_FALL: self.widgets[5].currentText(),
            KEY_ROAD_TYPE: self.widgets[6].currentText(),
            KEY_CRASH_RATE: 0.0 if not self.widgets[7].text() else float(self.widgets[7].text())
        }
        # Vehicle Distribution
        vehicle_dist = {
            KEY_TWO_WHEELER: 0.0 if not self.vehicle_distribution[0].text() else float(self.vehicle_distribution[0].text()),
            KEY_SMALL_CARS: 0.0 if not self.vehicle_distribution[1].text() else float(self.vehicle_distribution[1].text()),
            KEY_BIG_CARS: 0.0 if not self.vehicle_distribution[2].text() else float(self.vehicle_distribution[2].text()),
            KEY_ORDINARY_BUS: 0.0 if not self.vehicle_distribution[3].text() else float(self.vehicle_distribution[3].text()),
            KEY_DELUXE_BUS: 0.0 if not self.vehicle_distribution[4].text() else float(self.vehicle_distribution[4].text()),
            KEY_LCV: 0.0 if not self.vehicle_distribution[5].text() else float(self.vehicle_distribution[5].text()),
            KEY_MCV: 0.0 if not self.vehicle_distribution[6].text() else float(self.vehicle_distribution[6].text()),
            KEY_HCV: 0.0 if not self.vehicle_distribution[7].text() else float(self.vehicle_distribution[7].text())
        }
        # Accident distribution
        accident_dist = {
            KEY_MINOR_INJURY: 0.0 if not self.accident_distribution[0].text() else float(self.accident_distribution[0].text()),
            KEY_MAJOR_INJURY: 0.0 if not self.accident_distribution[1].text() else float(self.accident_distribution[1].text()),
            KEY_FATAL: 0.0 if not self.accident_distribution[2].text() else float(self.accident_distribution[2].text())
        }
        print("\nCollected Traffic Composition Data from UI:\nDaily Avg Traffic...\n")
        pprint(traffic_data)
        print("\nUI Data...\n")
        pprint(data)
        print("\nAccident Distribution...\n")
        pprint(accident_dist)

        # Save UI Data to Backend
        self.database_manager.traffic_data = data
        self.database_manager.daily_average_traffic_data = traffic_data
        self.database_manager.accident_distribution = accident_dist
        self.database_manager.vehicle_distribution = vehicle_dist

        # Carbon Emission due to Rerouting during Initial Construction
        self.database_manager.init_carbon_emission_rerouting()
    
    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

#----------------Standalone-Test-Code--------------------------------

# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setStyleSheet("border: none")

#         self.central_widget = QWidget()
#         self.central_widget.setObjectName("central_widget")
#         self.setCentralWidget(self.central_widget)

#         self.main_h_layout = QHBoxLayout(self.central_widget)
#         self.main_h_layout.addStretch(1)

#         self.main_h_layout.addWidget(BridgeAndTrafficData(), 2)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec())