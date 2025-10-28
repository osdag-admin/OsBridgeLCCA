"""
<Author>: Prerna Praveen Vidyarthi
<Intern>: FOSSEE Summer Fellowship 2025
<Github>: https://github.com/prerna2024-cyber
<Email>: vidyarthiprerna637@gmail.com
"""
from PySide6.QtCore import (QSize, Qt, QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QAction,QFont, QFontDatabase, QIcon)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QMenu, QMenuBar, QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QComboBox)

from widgets.title_bar import CustomTitleBar
from widgets.project_details_right_widget import ProjectDetailsWidget
from widgets.tutorial_widget_left import TutorialWidget
from widgets.structure_works_data.foundation_widget import Foundation
from widgets.structure_works_data.super_structure_widget import SuperStructure
from widgets.structure_works_data.sub_structure_widget import SubStructure
from widgets.structure_works_data.auxiliary_works_widget import AuxiliaryWorks
from widgets.financial_data import FinancialData
from widgets.carbon_emission_data.carbon_emission_data import CarbonEmissionData
from widgets.carbon_emission_data.carbon_emission_cost_data import CarbonEmissionCostData
from widgets.bridge_and_traffic_data import BridgeAndTrafficData
from widgets.maintenance_repair_data import MaintenanceRepairData
from widgets.demolition_and_recycling_data import DemolitionAndRecyclingData
from widgets.project_details_left_widget import ProjectDetailsLeft

from PySide6.QtWidgets import QStackedWidget

class UiMainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        # Load and set the Alata Regular font
        font_id = QFontDatabase.addApplicationFont("resources/AlataRegular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app_font = QFont(font_family, 10)
            QApplication.setFont(app_font)
        else:
            print("Failed to load Alata font")

        MainWindow.setWindowTitle("Custom Title Bar App")
        MainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width()*1//8)
        y = (screen.height()*1//8)
        MainWindow.setGeometry(x, y, screen.width()*3//4, screen.height()*3//4)

        # Set window stylesheet
        MainWindow.setStyleSheet("""
            QMainWindow {
                border: none;
            }
            QMenuBar {
                background-color: #FAFAFA;
                border-bottom: 1px solid #d0d0d0;
                border-left: 1px solid #285A23;
                border-right: 1px solid #285A23;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
                border-bottom: 2px solid #FAFAFA;
                margin: 2px;
            }
            QMenuBar::item:selected {
                border-bottom: 2px solid #806C6C;
            }
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
            QMenu::item {
                padding: 4px 4px 4px 12px;
                text-align: left;
                color: #514E4E;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QMenu::separator {
                height: 1px;
                background-color: #d0d0d0;
                margin: 4px 0px;
            }
            QMenu::icon {
                padding-left: 5px;
                width: 16px;
                height: 16px;
            }
            QMenu::indicator {
                width: 16px;
                height: 16px;
            }
            QMenu::right-arrow {
                margin-right: 5px;
            }
        """)

        # Create a central widget and main layout for the window
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("border: none;")
        self.central_widget.setObjectName("central_widget")
        MainWindow.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add the custom title bar to the top of the main layout
        self.title_bar = CustomTitleBar(MainWindow)
        main_layout.addWidget(self.title_bar)

        # Create and add menu bar directly to the central widget's main_layout
        # DO NOT use MainWindow.setMenuBar() when using FramelessWindowHint
        self.menubar = QMenuBar()
        self.menubar.setObjectName(u"menubar")
        main_layout.addWidget(self.menubar) # This is the crucial line for custom frame

        # Create menus
        self.menuFile = QMenu("&File", self.menubar)
        self.menuHome = QMenu("&Home", self.menubar)
        self.menuReport = QMenu("&Report", self.menubar)
        self.menuHelp = QMenu("&Help", self.menubar)

        # Add menus to menubar
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuHome)
        self.menubar.addMenu(self.menuReport)
        self.menubar.addMenu(self.menuHelp)

        # Create and add actions to File menu with icons
        self.actionNew = QAction(QIcon("resources/new.svg"), "New", MainWindow)
        self.actionOpen = QAction(QIcon("resources/open.svg"), "Open", MainWindow)
        self.actionSave = QAction(QIcon("resources/save.svg"), "Save", MainWindow)
        self.actionSaveAs = QAction(QIcon("resources/save_as.svg"), "Save As...", MainWindow)
        self.actionCreateCopy = QAction(QIcon("resources/create_copy.svg"), "Create a Copy", MainWindow)
        self.actionPrint = QAction(QIcon("resources/print.svg"), "Print", MainWindow)
        self.actionRename = QAction(QIcon("resources/rename.svg"), "Rename", MainWindow)
        self.actionExport = QAction(QIcon("resources/export.svg"), "Export", MainWindow)
        self.actionVersionHistory = QAction(QIcon("resources/version_history.svg"), "Version History", MainWindow)
        self.actionInfo = QAction(QIcon("resources/info.svg"), "Info", MainWindow)

        # Add actions to File menu
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionCreateCopy)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRename)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionVersionHistory)
        self.menuFile.addAction(self.actionInfo)

        # Create and add actions to Help menu with icons
        self.actionDocumentation = QAction(QIcon("resources/contact.svg"), "Contact us", MainWindow)
        self.actionFeedback = QAction(QIcon("resources/feedback.svg"), "Feedback", MainWindow)
        self.actionVideoTutorial = QAction(QIcon("resources/video_tutorial.svg"), "Video Tutorials", MainWindow)
        self.actionJoinCommunity = QAction(QIcon("resources/join_community.svg"), "Join our Community", MainWindow)

        # Add actions to Help menu
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionFeedback)
        self.menuHelp.addSeparator()

        self.menuHelp.addAction(self.actionVideoTutorial)
        self.menuHelp.addAction(self.actionJoinCommunity)

        # Main content area below the menubar
        self.main_content_area = QWidget()
        # This widget needs to stretch to fill the remaining space
        main_layout.addWidget(self.main_content_area, 1) # Add stretch factor of 1
        self.main_content_area.setObjectName("main_content_area")
        self.main_content_area.setStyleSheet("""
            #main_content_area {
                background-color: #FAFAFA;
                border: 1px solid #285A23;
                border-top: 1px solid #BBBBBB;
                
            }
            QLabel {
                color: #9F8888;
                font-size: 14px;
                border: none;
                padding: 5px;
            }
            QPushButton {
                background-color: #EDEDED;
                border: 1px solid #d0d0d0;
                padding: 6px 16px;
                color: #514E4E;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #BBBBBB,
                    stop: 0.26 #E8E8E8,
                    stop: 1 #EDEDED
                    );
                border-color: #806C6C;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # Main vertical layout for content inside main_content_area
        content_layout = QVBoxLayout(self.main_content_area)
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)  # Add spacing between all buttons
        button_layout.setContentsMargins(5, 5, 5, 5)  # Add some margin around the layout

        # ------------------------------------------------------------

        # Add buttons to left container
        self.edit_button = QPushButton()
        self.edit_button.setObjectName(u"edit_button")
        self.edit_button.setIcon(QIcon("resources/edit_button.png"))
        self.edit_button.setFixedSize(60, 30)
        self.edit_button.setIconSize(QSize(25, 25))
        self.edit_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                margin-right: 20px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #FAFAFA;
                border: 1px solid #888888;
            }
        """)
        button_layout.addWidget(self.edit_button)

        self.file_button= QPushButton()
        self.file_button.setObjectName(u"file_button")
        self.file_button.setFixedSize(50, 30)
        self.file_button.setIcon(QIcon("resources/file_button.png"))
        self.file_button.setIconSize(QSize(30, 30))
        self.file_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                margin-right: 20px;
            }
            QPushButton:hover {
                border: 1px solid #888888;
                background-color: #FAFAFA;
            }
        """)
        button_layout.addWidget(self.file_button)

        # Create save menu button
        self.save_button = QPushButton()
        self.save_button.setObjectName(u"save_button")
        self.save_button.setFixedSize(40, 30)
        self.save_button.setIcon(QIcon("resources/save_button.png"))
        self.save_button.setIconSize(QSize(25, 25))
        self.save_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
            }
            QPushButton:hover {
                background-color: #FAFAFA;
                border: 1px solid #888888;
            }
            QPushButton::menu-indicator {
                image: url(resources/arrow_down.png);
                width: 8px;
                height: 30px;
                subcontrol-position: right center;
                subcontrol-origin: padding;
                margin-right: 2px;
                margin-left: 2px;
                border-left: 1px solid #BBBBBB;
            }
        """)

        # Create save menu
        self.save_menu = QMenu(self.save_button)
        self.save_menu.setStyleSheet("""
            QMenu {
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                padding: 2px;
                color: #9F8888;
            }

            QMenu::item {
                padding: 2px 2px;
                margin: 0px;
                border: none;
                min-height: 18px;
                font-size: 11px;
            }

            QMenu::item:selected {
                background-color: #FAFAFA;
            }

            QMenu::icon {
                width: 0px;
            }
        """)
        self.save_action = QAction("Save", self.save_menu)
        self.save_as_action = QAction("Save As", self.save_menu)
        self.save_menu.addAction(self.save_action)
        self.save_menu.addAction(self.save_as_action)
        self.save_button.setMenu(self.save_menu)

        button_layout.addWidget(self.save_button)

        # ------------------------------------------------------------

        button_layout.addStretch()

        # Add label
        self.windows = QLabel("Windows:")
        button_layout.addWidget(self.windows)

        # add buttons to the right
        self.tutorial_tab = QPushButton("Tutorials")
        self.project_details_tab = QPushButton("Project Details")
        self.results_tab = QPushButton("Results")
        self.compare = QPushButton("Compare")

        # Add buttons to layout
        button_layout.addWidget(self.tutorial_tab)
        button_layout.addWidget(self.project_details_tab)
        button_layout.addWidget(self.results_tab)
        button_layout.addWidget(self.compare)

        button_layout.addStretch()

        # Add the button layout to the main content layout
        content_layout.addLayout(button_layout)

        # ------------------------------------------------------------
        body_widget = QWidget()
        body_widget.setObjectName("body_widget")
        body_widget.setStyleSheet("""
            #body_widget {
                border-top: 1px solid #d0d0d0;
            }
        """)
        # ------------------------------------------------------------
        body_layout = QHBoxLayout(body_widget)
        body_layout.setSpacing(40)

        # Placeholders for dynamic widgets
        self.left_panel_placeholder = QWidget()
        self.left_panel_placeholder.setLayout(QVBoxLayout())
        self.right_panel_placeholder = QWidget()
        self.right_panel_placeholder.setLayout(QVBoxLayout())
        body_layout.addWidget(self.left_panel_placeholder, 1)
        body_layout.addWidget(self.right_panel_placeholder, 4)
        content_layout.addWidget(body_widget)

        # Store references to current widgets
        self.current_left_widget = None
        self.current_right_widget = None

        # Button click handlers
        def show_tutorial_widget():
            if self.current_left_widget:
                self.left_panel_placeholder.layout().removeWidget(self.current_left_widget)
                self.current_left_widget.setParent(None)
            self.current_left_widget = TutorialWidget()
            self.left_panel_placeholder.layout().addWidget(self.current_left_widget)
            self.current_left_widget.closed.connect(lambda: self.remove_left_widget())

        def show_project_details_widget(widget_name=None):
            if self.current_right_widget:
                self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                self.current_right_widget.setParent(None)
            self.widget_map = {
                "Structure Works Data": Foundation,
                "Foundation": Foundation,
                "Super-Structure": SuperStructure,
                "Sub-Structure": SubStructure,
                "Miscellaneous": AuxiliaryWorks,
                "Financial Data": FinancialData,
                "Carbon Emission Data": CarbonEmissionData,
                "Carbon Emission Cost Data": CarbonEmissionCostData,
                "Bridge and Traffic Data": BridgeAndTrafficData,
                "Maintenance and Repair": MaintenanceRepairData,
                "Demolition and Recycling": DemolitionAndRecyclingData
            }
            if widget_name and widget_name in self.widget_map:
                self.current_right_widget = self.widget_map[widget_name]()
                self.remove_left_widget()
                self.detail_stack = QStackedWidget()
                self.current_left_widget = ProjectDetailsLeft(self.widget_map, parent=self)
                self.current_left_widget.handle_button_selection(button_name=widget_name)
                self.left_panel_placeholder.layout().addWidget(self.current_left_widget)
                self.current_left_widget.closed.connect(lambda: self.remove_left_widget())
            else:
                self.current_right_widget = ProjectDetailsWidget()
            self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
            self.current_right_widget.closed.connect(lambda: self.remove_right_widget())
            # Connect param_buttons if present
            if hasattr(self.current_right_widget, 'param_buttons'):
                for btn in self.current_right_widget.param_buttons:
                    btn.clicked.connect(lambda checked, b=btn: show_project_details_widget(b.text().strip()))
        def remove_right_widget():
            if self.current_right_widget:
                self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                self.current_right_widget.setParent(None)
                self.current_right_widget = None
        self.remove_right_widget = remove_right_widget

        def remove_left_widget():
            if self.current_left_widget:
                self.left_panel_placeholder.layout().removeWidget(self.current_left_widget)
                self.current_left_widget.setParent(None)
                self.current_left_widget = None
        self.remove_left_widget = remove_left_widget

        self.tutorial_tab.clicked.connect(show_tutorial_widget)
        self.project_details_tab.clicked.connect(lambda: show_project_details_widget())
    
    def show_project_detail_widgets(self, widget_name):
        if self.current_right_widget:
            self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
            self.current_right_widget.setParent(None)
        if widget_name and widget_name in self.widget_map:
            self.current_right_widget = self.widget_map[widget_name]()
            self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
        
