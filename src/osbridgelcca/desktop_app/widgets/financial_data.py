from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon, QIntValidator
from .utils.data import *
import sys
import os

class FinancialData(QWidget):
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

        # --- Financial Data Form ---
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(20)
        field_width = 200

        # 1. Real Discount Rate (with info icon)
        label1_widget = QWidget()
        label1_layout = QHBoxLayout(label1_widget)
        label1_layout.setContentsMargins(0, 0, 0, 0)
        label1_layout.setSpacing(4)
        label1 = QLabel("Discount Rate (Inflation Adjusted)")
        label1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label1_layout.addWidget(label1)
        info_icon = QLabel()
        info_icon.setPixmap(QIcon("resources/info.svg").pixmap(16, 16))
        label1_layout.addWidget(info_icon)
        label1_layout.addStretch(1)
        input1 = QLineEdit()
        self.widgets.append(input1)
        input1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input1.setFixedWidth(field_width)
        input1.setText("6.70")
        input1.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        unit1 = QLabel("(%)")
        suggested1 = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label1_widget, 0, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input1, 0, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit1, 0, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(suggested1, 0, 3, alignment=Qt.AlignVCenter)

        # 2. Inflation Rate
        label2 = QLabel("Inflation Rate")
        label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input2 = QLineEdit()
        self.widgets.append(input2)
        input2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input2.setFixedWidth(field_width)
        input2.setText("5.15")
        input2.setStyleSheet(input1.styleSheet())
        unit2 = QLabel("(%)")
        suggested2 = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label2, 1, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input2, 1, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit2, 1, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(suggested2, 1, 3, alignment=Qt.AlignVCenter)

        # 3. Interest Rate
        label2 = QLabel("Interest Rate")
        label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input2 = QLineEdit()
        self.widgets.append(input2)
        input2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input2.setFixedWidth(field_width)
        input2.setText("7.75")
        input2.setStyleSheet(input1.styleSheet())
        unit2 = QLabel("(%)")
        suggested2 = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label2, 2, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input2, 2, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit2, 2, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(suggested2, 2, 3, alignment=Qt.AlignVCenter)

        # 4. Investment Ratio
        label3 = QLabel("Investment Ratio")
        label3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input3 = QLineEdit()
        self.widgets.append(input3)
        input3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input3.setFixedWidth(field_width)
        input3.setText("0.5000")
        input3.setStyleSheet(input1.styleSheet())
        suggested3 = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label3, 3, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input3, 3, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(QWidget(), 3, 2)  # Empty cell for unit
        grid_layout.addWidget(suggested3, 3, 3, alignment=Qt.AlignVCenter)

        # 5. Design Life
        label4 = QLabel("Design Life")
        label4.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input4 = QLineEdit()
        input4.setValidator(QIntValidator(input4))
        self.widgets.append(input4)
        input4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input4.setFixedWidth(field_width)
        input4.setText("50")
        input4.setStyleSheet(input1.styleSheet())
        unit4 = QLabel("(years)")
        suggested4 = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label4, 4, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input4, 4, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit4, 4, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(suggested4, 4, 3, alignment=Qt.AlignVCenter)

        # 6. Time for construction of Base Project
        label5 = QLabel("Time for construction of Base Project")
        label5.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input5 = QLineEdit()
        self.widgets.append(input5)
        input5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input5.setFixedWidth(field_width)
        input5.setText("")
        input5.setStyleSheet(input1.styleSheet())
        unit5 = QLabel("(years)")
        grid_layout.addWidget(label5, 5, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input5, 5, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit5, 5, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(QWidget(), 5, 3)  # Empty cell for suggested

        # 7. Analysis Period
        label5 = QLabel("Analysis Period")
        label5.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        input5 = QLineEdit()
        input5.setValidator(QIntValidator(input5))
        self.widgets.append(input5)
        input5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input5.setFixedWidth(field_width)
        input5.setText("50")
        input5.setStyleSheet(input1.styleSheet())
        unit5 = QLabel("(years)")
        suggested = QLabel("Suggested", parent=self.general_widget, styleSheet="color: #B3AEAE; font-size: 10px;")
        grid_layout.addWidget(label5, 6, 0, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(input5, 6, 1, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(unit5, 6, 2, alignment=Qt.AlignVCenter)
        grid_layout.addWidget(suggested, 6, 3)  # Empty cell for suggested

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
        back_button.clicked.connect(lambda: self.back.emit(KEY_FINANCIAL))
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.collect_data)
        
        next_button.clicked.connect(lambda: self.next.emit(KEY_FINANCIAL))
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

    def collect_data(self):
        from pprint import pprint
        data = {
            KEY_DISCOUNT_RATE_IA: 0.0 if not self.widgets[0].text() else float(self.widgets[0].text())/100,
            KEY_INFLATION_RATE: 0.0 if not self.widgets[1].text() else float(self.widgets[1].text())/100,
            KEY_INTEREST_RATE: 0.0 if not self.widgets[2].text() else float(self.widgets[2].text())/100,
            KEY_INVESTMENT_RATIO: 0.0 if not self.widgets[3].text() else float(self.widgets[3].text()),
            KEY_DESIGN_LIFE: 0 if not self.widgets[4].text() else int(self.widgets[4].text()),
            KEY_CONSTR_TIME: 0.0 if not self.widgets[5].text() else float(self.widgets[5].text()),
            KEY_ANALYSIS_PERIOD: 0 if not self.widgets[6].text() else int(self.widgets[6].text()),
        }

        print("\nCollected Data from Financial UI:")
        pprint(data)

        # Save UI Data to Backend
        self.database_manager.financial_data = data

        # calculate Time Cost
        self.database_manager.calculate_time_cost()

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

#         self.main_h_layout.addWidget(FinancialData(), 2)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec())