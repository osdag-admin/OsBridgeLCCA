from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, QSize, Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QComboBox)
from .utils.data import *
import sys

class ProjectDetailsWidget(QWidget):
    closed = Signal()
    def __init__(self, parent=None):
        super().__init__()
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
            QPushButton#general_info, QPushButton#parameter_button, QPushButton#output_button {
                background-color: #FDEFEF;
                border: 1px solid #000000;
                text-align: left;
                padding: 3px 10px;
                color: #000000;
                font-size: 14px;
            }
            QPushButton#general_info:hover, QPushButton#parameter_button:hover, QPushButton#output_button:hover {
                background-color: #F0E6E6;
                border: 1px solid #000000;
            }
            QPushButton#general_info:pressed, QPushButton#parameter_button:pressed, QPushButton#output_button:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
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
        """)
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        # --- Top Section ---
        top_h_layout_left_panel = QHBoxLayout()
        self.top_button_right_panel = QPushButton("Project Details Window      ")
        self.top_button_right_panel.setObjectName("top_button_right_panel")
        self.top_button_right_panel.setIcon(QIcon("resources/close.png"))
        self.top_button_right_panel.setIconSize(QSize(13, 13))
        self.top_button_right_panel.setLayoutDirection(Qt.RightToLeft)
        self.top_button_right_panel.clicked.connect(self.close_widget)
        top_h_layout_left_panel.addWidget(self.top_button_right_panel)
        top_h_layout_left_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

        # --- Scroll Area Setup ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)
        scroll_content_layout = QVBoxLayout(scroll_content_widget)
        scroll_content_layout.addStretch(1)

        # --- General Information Section Button ---
        self.general_info_button = QPushButton("   General Information")
        self.general_info_button.setObjectName("general_info")
        self.general_info_button.setCursor(Qt.PointingHandCursor)
        self.unactive_arrow_icon = QIcon("resources/play-button-arrowhead.png")
        self.active_arrow_icon = QIcon("resources/arrow_down.png")
        self.general_info_button.setIcon(self.unactive_arrow_icon)
        self.general_info_button.setIconSize(QSize(10, 10))
        self.general_info_button.setLayoutDirection(Qt.LeftToRight)
        scroll_content_layout.insertWidget(0, self.general_info_button)

        # --- General Information Form Widget ---
        self.general_button_active = False
        self.general_widget = QWidget()
        self.general_widget.setObjectName("general_info_form_widget")
        self.general_widget.setStyleSheet(f"""
            #general_info_form_widget QLineEdit,
            #general_info_form_widget QTextEdit,
            #general_info_form_widget QComboBox {{
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                background-color: #FFFFFF;
            }}
            #general_info_form_widget QTextEdit::viewport {{
                background-color: #FFFFFF;
            }}
            #general_info_form_widget QLineEdit:focus,
            #general_info_form_widget QTextEdit:focus,
            #general_info_form_widget QComboBox:focus {{
                border: 1px solid #DDDCE0;
                background-color: #FFFFFF;
            }}
            #general_info_form_widget QTextEdit:focus::viewport {{
                background-color: #FFFFFF;
            }}
            #left_label {{
                margin-right: 20px;
            }}
            #info_button {{
                margin-right: {self.general_info_button.width()//2}px;
            }}
        """)
        grid_layout = QGridLayout(self.general_widget)
        grid_layout.setContentsMargins(30, 20, 30, 20)
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)
        # Company Name
        label = QLabel("Company Name")
        label.setObjectName("left_label")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 0, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        grid_layout.addWidget(input_widget, 0, 1, 1, 2)
        # Project Title
        label = QLabel("Project Title")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 1, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        grid_layout.addWidget(input_widget, 1, 1, 1, 2)
        # Project Description
        label = QLabel("Project Description")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 2, 0, 1, 1)
        input_widget = QTextEdit(self.general_widget)
        input_widget.setPlaceholderText("Enter project description here...")
        grid_layout.addWidget(input_widget, 2, 1, 1, 2)
        # Name of Valuer
        label = QLabel("Name of Valuer")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 3, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 3, 1, 1, 1)
        # Job Number
        label = QLabel("Job Number")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 4, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 4, 1, 1, 1)
        # Client
        label = QLabel("Client")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 5, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 5, 1, 1, 1)
        # Country ComboBox
        label = QLabel("Country")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 6, 0, 1, 1)
        valuer_combo = QComboBox(self.general_widget)
        valuer_combo.addItem("India")
        valuer_combo.addItem("USA")
        valuer_combo.addItem("UK")
        valuer_combo.setStyleSheet("""
            QComboBox{
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
        grid_layout.addWidget(valuer_combo, 6, 1, 1, 1)
        info_icon = QLabel("ⓘ")
        info_icon.setStyleSheet("color: grey; font-size: 14px;")
        info_icon.setObjectName("info_button")
        info_icon.setToolTip("Social Cost of Carbon varies as per selected region")
        info_icon.setCursor(Qt.PointingHandCursor)
        info_icon.setAlignment(Qt.AlignRight)
        grid_layout.addWidget(info_icon, 6, 2, 1, 1)
        # Base Year
        label = QLabel("Base Year")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.addWidget(label, 7, 0, 1, 1)
        input_widget = QLineEdit(self.general_widget)
        input_widget.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
            }
        """)
        grid_layout.addWidget(input_widget, 7, 1, 1, 1)
        scroll_content_layout.insertWidget(1, self.general_widget)
        self.general_widget.show()
        self.general_widget.adjustSize()
        self.original_general_widget_height = self.general_widget.sizeHint().height()
        self.general_widget.hide()
        self.general_widget_animation = QPropertyAnimation(self.general_widget, b"maximumHeight")
        self.general_widget_animation.setDuration(300)
        self.general_widget_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.general_widget.setMaximumHeight(0)
        self.general_widget.hide()
        # Input Parameters Section
        self.input_param_unactive_icon = QIcon("resources/play-button-arrowhead.png")
        self.input_param_active_icon = QIcon("resources/arrow_down.png")
        self.input_param_button_css_inactive = """
            QPushButton#parameter_button {
              background-color: transparent;
                border: 1px solid #000000;
                text-align: left;
                padding: 3px 10px;
                color: #000000;
                font-size: 16px;
            }
            QPushButton#parameter_button:hover {
                background-color: #F0E6E6;
            }
            QPushButton#parameter_button:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }
        """
        self.input_param_button_css_active = """
            QPushButton#parameter_button {
                background-color: transparent;
                text-align: left;
                padding: 3px 10px;
                color: #000000;
                font-size: 16px;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
            }
            QPushButton#parameter_button:hover {
                background-color: #F0E6E6;
            }
            QPushButton#parameter_button:pressed {
                background-color: #FFF3F3;
            }
        """
        self.input_param_widget = QWidget()
        self.input_param_widget.setObjectName("input_param_widget")
        self.input_param_widget.setStyleSheet("""
                #input_param_widget{
                        background-color: #FDEFEF;
                        border: 1px solid #000000;
                }
        """)
        self.input_param_layout = QVBoxLayout(self.input_param_widget)
        self.input_param_layout.setContentsMargins(0, 0, 0, 0)
        self.input_param_layout.setSpacing(0)
        self.input_param_button = QPushButton("   Input Parameters")
        self.input_param_button.setStyleSheet(self.input_param_button_css_inactive)
        self.input_param_button.setObjectName("parameter_button")
        self.input_param_button.setCursor(Qt.PointingHandCursor)
        self.input_param_button.clicked.connect(self.input_button_toggle)
        self.input_param_button.setIcon(self.input_param_unactive_icon)
        self.input_param_button.setIconSize(QSize(10, 10))
        self.input_param_button.setLayoutDirection(Qt.LeftToRight)
        self.input_param_layout.addWidget(self.input_param_button)
        self.input_param_option_widget = QWidget()
        self.input_param_option_widget.hide()
        self.input_option_active = False
        self.input_param_option_widget.setObjectName("input_param_option_widget")
        self.input_param_option_layout = QVBoxLayout(self.input_param_option_widget)
        self.input_param_option_layout.setContentsMargins(8, 8, 8, 8)
        self.input_param_option_layout.setSpacing(2)
        button_labels = [
            KEY_STRUCTURE_WORKS_DATA,
            KEY_FINANCIAL,
            KEY_CARBON_EMISSION,
            KEY_BRIDGE_TRAFFIC,
            KEY_MAINTAINANCE_REPAIR,
            KEY_DEMOLITION_RECYCLE
        ]
        self.selected_icon = QIcon("resources/selected_icon.png")
        self.param_buttons = []
        for label in button_labels:
            btn = QPushButton(f"   {label}")
            btn.setObjectName("parameter_button")
            btn.setIcon(QIcon("resources/play-button-arrowhead.png"))
            btn.setIconSize(QSize(10, 10))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setLayoutDirection(Qt.LeftToRight)
            btn.setStyleSheet("""
                QPushButton#parameter_button {
                    background-color: none;
                    border: none;
                    text-align: left;
                    padding: 2px 10px;
                    color: #000;
                    font-size: 12px;
                    margin-left: 40px
                }
                QPushButton#parameter_button:hover {
                    background-color: #F0E6E6;
                }
            """)
            btn.clicked.connect(lambda checked, b=btn: self.select_param_button(b))
            self.input_param_option_layout.addWidget(btn)
            self.param_buttons.append(btn)
        self.input_param_layout.addWidget(self.input_param_option_widget)
        scroll_content_layout.insertWidget(2, self.input_param_widget)
        self.output_button = QPushButton("   Outputs")
        self.output_button.setObjectName("output_button")
        self.output_button.setIcon(QIcon("resources/play-button-arrowhead.png"))
        self.output_button.setIconSize(QSize(10, 10))
        self.output_button.setLayoutDirection(Qt.LeftToRight)
        scroll_content_layout.insertWidget(3, self.output_button)
        left_panel_vlayout.addWidget(self.scroll_area)
        self.bottom_widget = QWidget()
        self.bottom_widget.setObjectName("bottom_widget")
        self.bottom_widget.setStyleSheet("""
            #bottom_widget {
                background-color: #F0E6E6;
                border-left: 1px solid #000000;
                border-bottom: 1px solid #000000;
                border-right: 1px solid #000000;
            }
        """)
        left_panel_vlayout.addWidget(self.bottom_widget)
        self.general_info_button.clicked.connect(self.expand_general_area)

    def expand_general_area(self):
        try:
            self.general_widget_animation.finished.disconnect()
        except RuntimeError:
            pass
        if self.general_button_active:
            self.general_info_button.setIcon(self.unactive_arrow_icon)
            self.general_widget_animation.setStartValue(self.general_widget.height())
            self.general_widget_animation.setEndValue(0)
            self.general_widget_animation.finished.connect(self.general_widget.hide)
            self.general_button_active = False
        else:
            self.general_info_button.setIcon(self.active_arrow_icon)
            self.general_widget.show()
            self.general_widget_animation.setStartValue(0)
            self.general_widget_animation.setEndValue(self.original_general_widget_height)
            self.general_widget_animation.finished.connect(lambda: self.general_widget.setMaximumHeight(16777215))
            self.general_button_active = True
        self.general_widget_animation.start()

    def input_button_toggle(self):
        if self.input_option_active:
            self.input_param_option_widget.hide()
            self.input_param_button.setStyleSheet(self.input_param_button_css_inactive)
            self.input_param_button.setIcon(self.input_param_unactive_icon)
            self.input_option_active = False
        else:
            self.input_param_option_widget.show()
            self.input_option_active = True
            self.input_param_button.setStyleSheet(self.input_param_button_css_active)
            self.input_param_button.setIcon(self.input_param_active_icon)

    def select_param_button(self, selected_btn):
        for btn in self.param_buttons:
            if btn == selected_btn:
                btn.setIcon(self.selected_icon)
            else:
                btn.setIcon(QIcon("resources/play-button-arrowhead.png"))

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

#         self.main_h_layout.addWidget(ProjectDetailsWidget(), 2)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec()) 