from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon
import sys
import os

class BridgeAndTrafficData(QWidget):
    closed = Signal()
    def __init__(self, parent=None):
        super().__init__()
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
                padding: 3px 10px;
            }
            QComboBox::drop-down {
                border: none;
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
                background-color: #FFFFFF;
                outline: none;
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

        top_h_layout_left_panel = QHBoxLayout()
        top_button_left_panel = QPushButton("Bridge and Traffic Data    ")
        top_h_layout_left_panel.addWidget(top_button_left_panel)
        top_button_left_panel.setIcon(QIcon("resources/close.png"))
        top_button_left_panel.setIconSize(QSize(13, 13))
        top_button_left_panel.setObjectName("top_button_left_panel")
        top_button_left_panel.clicked.connect(self.close_widget)
        top_button_left_panel.setLayoutDirection(Qt.RightToLeft)
        top_h_layout_left_panel.addWidget(top_button_left_panel)

        top_h_layout_left_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Preferred))
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

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
        label = QLabel("Number of Lanes")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 0, 0, 1, 1)
        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItem("1")
        valuer_combo.addItem("2")
        valuer_combo.addItem("3")
        valuer_combo.addItem("4")
        valuer_combo.addItem("5+")
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

        # Road Roughness
        label = QLabel("Road Roughness")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 3, 0, 1, 1)
        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItem("option a")
        valuer_combo.addItem("option b")
        valuer_combo.addItem("option c")
        valuer_combo.addItem("option d")
        grid_layout.addWidget(valuer_combo, 3, 1, 1, 1)
        info_icon = QLabel("(mm/km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 3, 2, 1, 1)

        # Road Rise and Fall (RF)
        label = QLabel("Road Rise and Fall (RF)")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 4, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setFixedWidth(self.text_box_width)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 4, 1, 1, 1)

        info_icon = QLabel("(m/km)")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 4, 2, 1, 1)

        # Type of Road
        label = QLabel("Type of Road")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 5, 0, 1, 1)
        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItem("option a")
        valuer_combo.addItem("option b")
        valuer_combo.addItem("option c")
        valuer_combo.addItem("option d")
        grid_layout.addWidget(valuer_combo, 5, 1, 1, 1)
        

        info_icon = QLabel(" ")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 5, 2, 1, 1)

        # Annual Increase in Traffic
        label = QLabel("Annual Increaase in Traffic if Re-Routing duration increases more than a year  ")
        label.setFixedWidth(200)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 6, 0, 1, 1)
        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.setFixedWidth(self.text_box_width)
        valuer_combo.setPlaceholderText("Select")
        valuer_combo.addItem("option a")
        valuer_combo.addItem("option b")
        valuer_combo.addItem("option c")
        valuer_combo.addItem("option d")
        grid_layout.addWidget(valuer_combo, 6, 1, 1, 1)

        info_icon = QLabel("(%)")
        info_icon.setStyleSheet("color: grey; font-size: 14px; padding-top: 14px;")
        info_icon.setAlignment(Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(info_icon, 6, 2, 1, 1)

        # Composition of Various Vehicles
        # Remove the old label and vehicle_widget from the grid
        # Instead, create a horizontal layout for this row
        composition_row_widget = QWidget(self.general_widget)
        composition_row_layout = QHBoxLayout(composition_row_widget)
        composition_row_layout.setContentsMargins(0, 0, 0, 0)
        composition_row_layout.setSpacing(20)  # Space between label and box

        # The label
        composition_label = QLabel("Composition of Various Vehicles")
        composition_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        composition_row_layout.addWidget(composition_label, alignment=Qt.AlignTop)

        # The white box (vehicle_widget) as before
        vehicle_widget = QWidget(self.general_widget)
        vehicle_widget.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 1px solid #DDDCE0")
        vehicle_widget.setFixedWidth(400)
        vehicle_widget.setFixedHeight(250)
        vehicle_layout = QGridLayout(vehicle_widget)
        vehicle_layout.setContentsMargins(0, 0, 0, 0)
        # vehicle_layout.setHorizontalSpacing(7)
        # vehicle_layout.setVerticalSpacing(8)

        vehicles = ["Cars", "Buses", "HCV", "MCV", "LCV"]
        for i, vehicle in enumerate(vehicles):
            v_label = QLabel(f"{vehicle}:")
            v_label.setFixedHeight(40)
            v_label.setFixedWidth(50)
            v_label.setStyleSheet("background-color: #FFFFFF; border: 1px solid #FFFFFF; border-radius: 10px; padding: 10px 10px 10px 1px;")
            v_input = QLineEdit()
            v_input.setFixedWidth(self.text_box_width)
            v_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #DDDCE0;
                    border-radius: 10px;
                    padding: 3px 10px;
                    background: #FFFFFF;
                }
            """)
            vehicle_layout.addWidget(v_label, i, 0)
            vehicle_layout.addWidget(v_input, i, 1)
        
        v_label1 = QLabel("(PCU/D)")
        v_label1.setStyleSheet(" padding: 10px 10px 10px 1px;")

        composition_row_layout.addWidget(vehicle_widget, alignment=Qt.AlignTop)

        # Add the composition_row_widget to the main grid, spanning columns 0-2
        grid_layout.addWidget(v_label1, 7, 3, 1, 3)
        grid_layout.addWidget(composition_row_widget, 7, 0, 1, 3)

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
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        self.button_h_layout.addWidget(next_button)

        # Add initial spacing before the navigation buttons
        self.scroll_content_layout.addLayout(self.button_h_layout)

        # --- Add a corner spacer to the scroll_content_layout ---
        self.button_h_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.scroll_content_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        left_panel_vlayout.addWidget(self.scroll_area)
    
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