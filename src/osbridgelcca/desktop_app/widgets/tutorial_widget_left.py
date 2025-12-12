from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, QSize, Qt, Signal
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QPushButton, QWidget, QLabel, QVBoxLayout)
import sys

class TutorialWidget(QWidget):
    closed = Signal()
    def __init__(self):
        super().__init__()
        self.setObjectName("left_panel_widget")
        self.setStyleSheet("""
           #left_panel_widget {
                background-color: #F8F8F8; /* Light gray/off-white background */
                border-radius: 8px; /* Slightly rounded corners for the entire body_widget */
                border: none;
            }
            #left_panel_widget QLabel {
                color: #333333; /* Darker text for content */
                font-size: 12px;
                /* No border or padding here, managed by layout margins */
            }
            #left_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #555555;
            }                          
            
            /* Styling for the scroll area */
            QScrollArea {
                border: 1px solid #000000; /* No border for the scroll area itself */
                background-color: transparent; /* Make background transparent to show widget's background */
                outline: none;            
            }
            QScrollArea > QWidget { /* This targets the widget *inside* the scroll area */
                background-color: transparent; /* Inherit parent background */
            }

            /* Scrollbar styling */
            QScrollBar:vertical {
                border: 1px solid #E0E0E0; /* Lighter border for scrollbar area */
                background: #F0F0F0; /* Light gray track */
                width: 12px; /* Width of the vertical scrollbar */
                margin: 18px 0px 18px 0px; /* Space for arrows */
                border-radius: 6px; /* Rounded track */
            }

            QScrollBar::handle:vertical {
                background: #C0C0C0; /* Medium gray handle */
                border: 1px solid #A0A0A0; /* Darker border for handle */
                min-height: 20px;
                border-radius: 5px; /* Rounded handle */
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
                image: url(resources/arrow_up.png); /* You might need to provide these icons */
            }
            QScrollBar::down-arrow:vertical {
                image: url(resources/arrow_down.png);
            }

            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: #D0D0D0;
            }  

            #left_panel_widget QPushButton#back_button { 
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                padding: 6px 8px;
                margin: 8px;
                color: #000000;
                font-size: 13px;
                border-radius: 8px;
            }
            #left_panel_widget QPushButton#back_button:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #BBBBBB,
                    stop: 0.26 #E8E8E8,
                    stop: 1 #EDEDED
                    );
                border-color: #806C6C;
            }
            #left_panel_widget QPushButton#back_button:pressed {
                background-color: #FFFFFF;
                border-color: #606060;
            }
            
            #left_panel_widget QPushButton#next_button { 
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                padding: 6px 8px;
                color: #000000;
                margin: 8px;
                font-size: 13px;
                border-radius: 8px;
            }
            #left_panel_widget QPushButton#next_button:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #BBBBBB,
                    stop: 0.26 #E8E8E8,
                    stop: 1 #EDEDED
                    );
                border-color: #806C6C;
            }
            #left_panel_widget QPushButton#next_button:pressed {
                background-color: #FFFFFF;
                border-color: #606060;
            }

            QPushButton#top_button_left_panel {
                background-color: #F0E6E6;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;        
            }
            QPushButton#top_button_left_panel:hover {
                background-color: #FDEFEF;
                border-color: #808080;
            }
            QPushButton#top_button_left_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }
            QPushButton#top_button_left_panel:hover QIcon {
                color: red;
            }
        """)
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0) # Add some padding inside the red area
        left_panel_vlayout.setSpacing(0) # Spacing between major sections

        top_h_layout_left_panel = QHBoxLayout()
        self.top_button_left_panel = QPushButton("Tutorials     ")
        self.top_button_left_panel.setIcon(QIcon("resources/close.png"))
        self.top_button_left_panel.setIconSize(QSize(13, 13))
        self.top_button_left_panel.setObjectName("top_button_left_panel")
        self.top_button_left_panel.setLayoutDirection(Qt.RightToLeft)
        self.top_button_left_panel.clicked.connect(self.close_widget)
        top_h_layout_left_panel.addWidget(self.top_button_left_panel)

        top_h_layout_left_panel.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        left_panel_vlayout.addLayout(top_h_layout_left_panel)

        bordered_spacer_widget = QWidget()
        bordered_spacer_widget.setObjectName("bordered_spacer_widget") # Give it an object name for CSS
        bordered_spacer_widget.setFixedHeight(50)
        bordered_spacer_widget.setStyleSheet("""
            #bordered_spacer_widget {
                background-color: #F0E6E6;
                border-left: 1px solid #000000;
                border-top: 1px solid #000000;
                border-right: 1px solid #000000;
            }
        """)
        left_panel_vlayout.addWidget(bordered_spacer_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        scroll_content_layout = QVBoxLayout(scroll_content_widget)

        middle_header_label = QLabel("""
            <center>
            1/4<br>
            Welcome to<br>
            BLCCA Studio</b>
            </center>
        """)
        middle_header_label.setStyleSheet("""
            QLabel{
                    font-size: 17px;
            }
            """)
        middle_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_content_layout.addWidget(middle_header_label)
        

        middle_body_label = QTextEdit()
        middle_body_label.setReadOnly(True)
        tutorial_text = """
                BLCCA Studio has a lot of features to offer. In the next few minutes, you will learn how to use BLCCA Studio efficiently, from setting up and managing projects to navigating the user interface. This tutorial will guide you through essential features, including customization options shortcuts, and export capabilities, ensuring a seamless workflow. Whether you're a beginner or an advanced user, this guide will help you unlock the full potential of BLCCA Studio and enhance your productivity.
                """

        middle_body_label.setHtml(tutorial_text)
        middle_body_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        middle_body_label.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding-top: 20px;
                border-top: 2px solid #806C6C;
            }
        """)
        scroll_content_layout.addWidget(middle_body_label)
        scroll_content_widget.setStyleSheet("background-color: #FFF9F9;") 
        left_panel_vlayout.addWidget(scroll_area)
        
        bottom_widget = QWidget()
        bottom_widget.setObjectName("bottom_widget")
        bottom_widget.setStyleSheet("""
            #bottom_widget {
                background-color: #F0E6E6;
                border-left: 1px solid #000000;
                border-bottom: 1px solid #000000;
                border-right: 1px solid #000000;
            }
        """)
        bottom_h_layout = QHBoxLayout(bottom_widget)
        back_button = QPushButton("Back")
        back_button.setObjectName("back_button")
        next_button = QPushButton("Next")
        next_button.setObjectName("next_button")
        bottom_h_layout.addWidget(back_button)
        bottom_h_layout.addWidget(next_button)
        left_panel_vlayout.addWidget(bottom_widget)

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
#         self.main_h_layout.addWidget(TutorialWidget(), 1)

#         self.main_h_layout.addStretch(4)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec()) 