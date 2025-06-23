import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QFrame, QSplitter,
                            QToolBar, QAction, QGroupBox, QMenu, QLineEdit,
                            QComboBox, QSizePolicy, QMessageBox, QTextEdit, QScrollArea,
                            QTabWidget, QStackedWidget)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

# Import all specific Project Details Dialog UIs
from ProjectDetails_BridgeANDTrafficData_Window import Ui_BridgeTraffic_Dialog
from ProjectDetails_Foundation_Window import Ui_Foundation_Dialog
from ProjectDetails_CarbonEmissionData_Window import Ui_CarbonEmission_Dialog
from ProjectDetails_DemolitionANDRecyclingData_Window import Ui_Demolition_Dialog
from ProjectDetails_FinancialData_Window import Ui_FinancialData_Dialog
from ProjectDetails_MaintenanceANDRepairData_Window import Ui_Maintenance_Dialog
from ProjectDetails_Miscellaneous_Window import Ui_Miscellaneous_Dialog
from ProjectDetails_SubStructure_Window import Ui_SubStructure_Dialog
from ProjectDetails_SuperStructure_Window import Ui_SuperStructure_Dialog

class MainWindow(QMainWindow): # Renamed to MainWindow, inheriting QMainWindow
    def __init__(self):
        super().__init__()
        self.setWindowTitle("<untitled draft> - BICCA Studio 1.0.0")
        self.setGeometry(100, 100, 1440, 1024)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Initialize tutorial page counter
        self.current_tutorial_page = 1
        self.total_tutorial_pages = 4

        # Tutorial content
        self.tutorial_pages = [
            {
                "page_number": "1/4",
                "title": "Welcome to\nBICCA Studio",
                "content": """
                BICCA Studio has a lot of features to offer. In the next few minutes, you'll learn how to use BICCA Studio efficiently, from setting up and managing projects, to navigating the user interface. This tutorial will guide you through essential features, including customization options, shortcuts, and export capabilities, ensuring a seamless workflow. Whether you're a beginner or an advanced user, this guide will help you unlock the full potential of BICCA Studio and enhance your productivity.
                """
            },
            {
                "page_number": "2/4",
                "title": "Welcome to\nBICCA Studio",
                "content": """
                The Project General Information page is the foundation of your project setup, allowing you to input essential details for accurate documentation and streamlined management. Here, you will provide key information starting with the Company Name, which represents the organization behind the project. Next is the Project Title, a concise name that defines the scope of work. The Project Description further elaborates on the objectives and purpose of the project. Additionally, you will need to enter the Name of the Valuer responsible for the valuation, along with the Job Number for easy reference. The Client field identifies the primary stakeholder of the project, while the Country specifies the project's geographical location. Finally, the Base Year establishes a reference period for analysis and reports.
                """
            },
            {
                "page_number": "3/4",
                "title": "Understanding\nInput Parameters",
                "content": """
                Input Parameters are crucial for accurate analysis and results. This section allows you to define various technical specifications, economic factors, and operational variables that will influence your project outcomes. You can specify factors such as time periods, growth rates, discount rates, and other numerical inputs that the software will use for calculations. Each parameter can be customized according to your specific requirements, ensuring that the analysis reflects real-world conditions accurately. The intuitive interface makes it easy to adjust these parameters as needed, and you can save different parameter sets for future use or comparisons.
                """
            },
            {
                "page_number": "4/4",
                "title": "Working with\nOutputs",
                "content": """
                The Outputs section displays the results of your analysis based on the information and parameters you've entered. Here you can view comprehensive reports, charts, and visualizations that present your data in meaningful ways. You can customize the output format according to your preferences or your client's requirements. BICCA Studio allows you to export these outputs in various formats including PDF, Excel, or as image files for easy sharing and presentation. Additionally, you can compare different scenarios by adjusting your inputs and generating new outputs, providing valuable insights for decision-making processes.
                """
            }
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- CORRECTED ORDER: Create UI elements BEFORE retranslateUi ---
        self.create_menu_bar()
        self.create_toolbar()
        self.create_window_tabs() # Custom tab buttons that control splitter visibility
        self.create_content_area() # Contains the QSplitter for panels
        self.create_status_bar() # Includes the persistent "Data" section

        self.retranslateUi(self) # Call retranslateUi *after* all widgets are created

        self.update_tutorial_content()

        # Set initial visible panels and button states for the custom tabs
        self.handle_tab_click("Tutorials", initial_load=True)
        self.handle_tab_click("Project Details", initial_load=True)

        # Connect QGroupBox toggled signals
        self.generalInfoGroup.toggled['bool'].connect(lambda checked: self.toggle_general_info_group_content(self.generalInfoGroup, checked))
        self.inputParamsGroup.toggled['bool'].connect(lambda checked: self.toggle_input_params_group_content(self.inputParamsGroup, checked))
        self.outputsGroup.toggled['bool'].connect(lambda checked: self.toggle_outputs_group_content(self.outputsGroup, checked))

        # Connect internal buttons to hide/show their respective sub-content
        self.pushButton.clicked.connect(lambda: self.toggle_sub_buttons_visibility(self.gridLayout_3, self.pushButton))
        self.pushButton_7.clicked.connect(lambda: self.toggle_sub_buttons_visibility(self.gridLayout_4, self.pushButton_7))

        # Initially hide the collapsible sub-sections' content
        self.gridLayout_3_widget.setVisible(False) # Hide the widget holding gridLayout_3
        self.gridLayout_4_widget.setVisible(False) # Hide the widget holding gridLayout_4

        # Manually trigger initial state for General Info, Input Params, Outputs groups
        self.toggle_general_info_group_content(self.generalInfoGroup, self.generalInfoGroup.isChecked())
        self.toggle_input_params_group_content(self.inputParamsGroup, self.inputParamsGroup.isChecked())
        self.toggle_outputs_group_content(self.outputsGroup, self.outputsGroup.isChecked())


    # Methods to open Project Details sub-windows
    def openBridgeTrafficWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_BridgeTraffic_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openFoundationWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_Foundation_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openCarbonEmissionWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_CarbonEmission_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openDemolitionWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_Demolition_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()
    
    def openFinancialWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_FinancialData_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openMaintenanceWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_Maintenance_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openMiscellaneousWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_Miscellaneous_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openSubStructureWindow(self):   
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_SubStructure_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def openSuperStructureWindow(self):
        self.window = QtWidgets.QDialog(self)
        self.ui = Ui_SuperStructure_Dialog()
        self.ui.setupUi(self.window)
        self.window.exec_()

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: white;
                color: black;
                border-bottom: 1px solid #e0e0e0;
            }
            QMenuBar::item {
                background-color: transparent;
                color: black;
                padding: 5px 25px;
            }
            QMenuBar::item:selected {
                background-color: #f0f0f0;
            }
        """)

        # Assign menus to self. attributes BEFORE retranslateUi is called
        self.menuFile = menubar.addMenu("File")
        self.menuHome = menubar.addMenu("Home")
        self.menuReports = menubar.addMenu("Reports")
        self.menuHelp = menubar.addMenu("Help")

        # Adding actions to the File menu (as per your original code)
        self.actionNew = QAction("New", self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Vector.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon2)
        self.menuFile.addAction(self.actionNew)

        self.actionOpen = QAction("Open", self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications/Qt/bin/../../../../../../../../../../Downloads/Vector (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon3)
        self.menuFile.addAction(self.actionOpen)

        self.actionSave = QAction("Save", self)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _save action floppy_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon4)
        self.menuFile.addAction(self.actionSave)

        self.actionSave_As = QAction("Save As...", self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _document save as template_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_As.setIcon(icon5)
        self.menuFile.addAction(self.actionSave_As)

        self.actionCreate_a_Copy = QAction("Create a Copy", self)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _file copy_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCreate_a_Copy.setIcon(icon6)
        self.menuFile.addAction(self.actionCreate_a_Copy)

        self.actionPrint = QAction("Print", self)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Vector (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon7)
        self.menuFile.addAction(self.actionPrint)

        self.actionRename = QAction("Rename", self)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Vector (3).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(icon8)
        self.menuFile.addAction(self.actionRename)

        self.actionExport = QAction("Export", self)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport.setIcon(icon9)
        self.menuFile.addAction(self.actionExport)

        self.actionVersion_History = QAction("Version History", self)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Vector (4).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVersion_History.setIcon(icon10)
        self.menuFile.addAction(self.actionVersion_History)

        self.actionInfo = QAction("Info", self)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Alert Circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInfo.setIcon(icon11)
        self.menuFile.addAction(self.actionInfo)

        # Adding actions to the Help menu
        self.actionContact_Us = QAction("Contact Us", self)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/Contact.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionContact_Us.setIcon(icon12)
        self.menuHelp.addAction(self.actionContact_Us)

        self.actionFeedback = QAction("Feedback", self)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _Person Feedback_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFeedback.setIcon(icon13)
        self.menuHelp.addAction(self.actionFeedback)

        self.actionVideo_Tutorials = QAction("Video Tutorials", self)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _youtube_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVideo_Tutorials.setIcon(icon14)
        self.menuHelp.addAction(self.actionVideo_Tutorials)

        self.actionJoin_our_Community = QAction("Join our Community", self)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("C:\\Users\\saans\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\qt5_applications\\Qt\\bin\\../../../../../../../../../../Downloads/🦆 icon _People Community_.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJoin_our_Community.setIcon(icon15)
        self.menuHelp.addAction(self.actionJoin_our_Community)

    def create_toolbar(self):
        self.toolBar = QToolBar("Main Toolbar") # Assign toolbar to self.toolBar
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(20, 20))
        self.toolBar.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e0e0;")
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        # Add the actions that should appear in the toolbar
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()

    def create_window_tabs(self):
        window_tabs_container = QWidget()
        window_tabs_container.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e0e0;")
        container_layout = QHBoxLayout(window_tabs_container)
        container_layout.setContentsMargins(10, 0, 10, 0)
        container_layout.setSpacing(0)

        windows_label = QLabel("Windows:")
        windows_label.setStyleSheet("font-weight: bold; margin-right: 5px;")
        container_layout.addWidget(windows_label)

        tabs = ["Tutorials", "Project Details", "Results", "Compare"]
        self.tab_buttons = {}
        for i, tab_name in enumerate(tabs):
            tab_btn = QPushButton(tab_name)
            tab_btn.setCheckable(True)
            tab_btn.setAutoExclusive(False)
            tab_btn.clicked.connect(lambda checked, name=tab_name: self.handle_tab_click(name))

            tab_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-bottom: none;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    padding: 5px 15px;
                    margin: 0px 2px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:checked {
                    background-color: white;
                    border-bottom: 1px solid white;
                }
            """)
            container_layout.addWidget(tab_btn)
            self.tab_buttons[tab_name] = tab_btn

        container_layout.addStretch(1)
        window_tabs_container.setFixedHeight(40)
        self.main_layout.addWidget(window_tabs_container)

    def handle_tab_click(self, clicked_tab_name, initial_load=False):
        """
        Handles clicks on custom window tabs.
        Toggles visibility of the corresponding panel in the splitter and updates tab styling.
        """
        clicked_button = self.tab_buttons.get(clicked_tab_name)
        if not clicked_button:
            return

        panel_to_toggle = None
        # Map tab names to actual panel widgets
        # Note: Tutorials panel is directly shown/hidden by its button
        # Project Details, Results, Compare are pages in the QStackedWidget
        panel_map = {
            "Tutorials": self.tutorials_panel,
            "Project Details": self.project_panel,
            "Results": self.results_panel,
            "Compare": self.compare_panel
        }
        
        # Determine if we're toggling the static tutorial panel or a dynamic panel in the stack
        if clicked_tab_name == "Tutorials":
            panel_to_toggle = self.tutorials_panel
            if initial_load:
                panel_to_toggle.show()
                clicked_button.setChecked(True)
            else:
                panel_to_toggle.setVisible(not panel_to_toggle.isVisible())
                clicked_button.setChecked(panel_to_toggle.isVisible())
        else:
            # For Project Details, Results, Compare: show the specific panel in QStackedWidget
            # and make sure the QStackedWidget itself is visible.
            target_index = -1
            if clicked_tab_name == "Project Details":
                target_index = self.dynamic_content_stack.indexOf(self.project_panel)
            elif clicked_tab_name == "Results":
                target_index = self.dynamic_content_stack.indexOf(self.results_panel)
            elif clicked_tab_name == "Compare":
                target_index = self.dynamic_content_stack.indexOf(self.compare_panel)

            if target_index != -1:
                if initial_load:
                    self.dynamic_content_stack.setCurrentIndex(target_index)
                    self.dynamic_content_stack.show() # Ensure the stack itself is visible
                    clicked_button.setChecked(True)
                else:
                    # Toggle logic for dynamic content panels:
                    # If the clicked tab's panel is ALREADY visible in the stack, hide the stack.
                    # Otherwise, show the clicked tab's panel in the stack.
                    if self.dynamic_content_stack.isVisible() and self.dynamic_content_stack.currentIndex() == target_index:
                        self.dynamic_content_stack.hide()
                        clicked_button.setChecked(False)
                    else:
                        self.dynamic_content_stack.setCurrentIndex(target_index)
                        self.dynamic_content_stack.show()
                        # Uncheck other dynamic content buttons when one is selected
                        for name, btn in self.tab_buttons.items():
                            if name in ["Project Details", "Results", "Compare"] and name != clicked_tab_name:
                                btn.setChecked(False)
                                btn.setStyleSheet("""
                                    QPushButton {
                                        background-color: #f0f0f0;
                                        border: 1px solid #cccccc;
                                        border-bottom: none;
                                        border-top-left-radius: 5px;
                                        border-top-right-radius: 5px;
                                        padding: 5px 15px;
                                        margin: 0px 2px;
                                        min-width: 80px;
                                    }
                                    QPushButton:hover {
                                        background-color: #e8e8e8;
                                    }
                                """)
                        clicked_button.setChecked(True)
            else:
                return # Should not happen if panel_map is correct

        # Update button stylesheets for all buttons
        for name, btn in self.tab_buttons.items():
            if btn.isChecked():
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        border: 1px solid #cccccc;
                        border-bottom: 1px solid white;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                        padding: 5px 15px;
                        margin: 0px 2px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: white;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        border: 1px solid #cccccc;
                        border-bottom: none;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                        padding: 5px 15px;
                        margin: 0px 2px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #e8e8e8;
                    }
                """)
        self.update_splitter_sizes()


    def create_content_area(self):
        self.content_splitter = QSplitter(Qt.Horizontal)
        self.content_splitter.setStyleSheet("QSplitter::handle { background-color: #e0e0e0; }")
        self.main_layout.addWidget(self.content_splitter)

        # --- Left side: Static Tutorials panel ---
        self.tutorials_panel = QWidget()
        self.tutorials_panel.setFixedWidth(300) # Fixed width as per Figma design
        self.tutorials_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # It's initially shown by handle_tab_click("Tutorials", initial_load=True)

        tutorials_layout = QVBoxLayout(self.tutorials_panel)
        tutorials_layout.setContentsMargins(0, 0, 0, 0)
        tutorials_layout.setSpacing(0)

        # Tutorial header
        tutorials_header = QWidget()
        tutorials_header.setStyleSheet("background-color: rgb(240,230,230); border-bottom: 1px solid #e0e0e0;")
        tutorials_header.setFixedHeight(40)
        tutorials_header_layout = QHBoxLayout(tutorials_header)
        tutorials_header_layout.setContentsMargins(5, 5, 5, 5)

        self.tutorials_header_label = QLabel("Tutorials")
        self.tutorials_header_label.setFont(QFont("Arial", 10, QFont.Bold))
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        close_btn.clicked.connect(self.close_tutorials)

        tutorials_header_layout.addWidget(self.tutorials_header_label)
        tutorials_header_layout.addStretch()
        tutorials_header_layout.addWidget(close_btn)
        tutorials_layout.addWidget(tutorials_header)

        # Tutorial Content Area with Scroll
        self.tutorials_scroll_area = QScrollArea(self.tutorials_panel)
        self.tutorials_scroll_area.setWidgetResizable(True)
        self.tutorials_scroll_area.setStyleSheet("QScrollArea { border: none; } QWidget#tutorialScrollContent { background-color: #f9f0f0; border-right: 1px solid #e0e0e0;}")

        self.tutorial_scroll_content = QWidget()
        self.tutorial_scroll_content.setObjectName("tutorialScrollContent")
        self.tutorials_content_layout = QVBoxLayout(self.tutorial_scroll_content)
        self.tutorials_content_layout.setContentsMargins(15, 15, 15, 15)
        self.tutorials_content_layout.setSpacing(10)

        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.page_label.setStyleSheet("font-weight: bold; padding: 5px; color: #888; background-color: transparent;")

        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.welcome_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.welcome_label.setStyleSheet("padding: 10px 0px; background-color: transparent;")

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setFont(QFont("Arial", 10))
        self.description_label.setStyleSheet("padding: 10px 0px; background-color: transparent;")
        self.description_label.setMinimumHeight(100)

        self.tutorials_content_layout.addWidget(self.page_label)
        self.tutorials_content_layout.addWidget(self.welcome_label)
        self.tutorials_content_layout.addWidget(self.description_label)
        self.tutorials_content_layout.addStretch()

        self.tutorials_scroll_area.setWidget(self.tutorial_scroll_content)
        tutorials_layout.addWidget(self.tutorials_scroll_area)

        # Navigation buttons for tutorial
        nav_buttons = QWidget()
        nav_buttons.setStyleSheet("background-color: #f9f0f0; border-right: 1px solid #e0e0e0;")
        nav_layout = QHBoxLayout(nav_buttons)
        nav_layout.setContentsMargins(10, 5, 10, 5)
        nav_layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        back_btn.clicked.connect(self.tutorial_back)

        next_btn = QPushButton("Next")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        next_btn.clicked.connect(self.tutorial_next)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)
        tutorials_layout.addWidget(nav_buttons)

        # --- Right side: QStackedWidget to hold Project Details, Results, Compare ---
        self.dynamic_content_stack = QStackedWidget()
        self.dynamic_content_stack.setStyleSheet("background-color: white;")
        self.dynamic_content_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.dynamic_content_stack.hide() # Initial visibility controlled by handle_tab_click

        # --- Project Details panel ---
        self.project_panel = QWidget()
        project_layout = QVBoxLayout(self.project_panel)
        project_layout.setContentsMargins(0, 0, 0, 0)

        # Project header
        project_header = QWidget()
        project_header.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #e0e0e0;")
        project_header.setFixedHeight(40)
        project_header_layout = QHBoxLayout(project_header)
        project_header_layout.setContentsMargins(5, 5, 5, 5)

        self.project_header_label = QLabel("Project Details Window")
        self.project_header_label.setFont(QFont("Arial", 10, QFont.Bold))
        project_close_btn = QPushButton("×")
        project_close_btn.setFixedSize(20, 20)
        project_close_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        project_close_btn.clicked.connect(self.close_project_details)

        project_header_layout.addWidget(self.project_header_label)
        project_header_layout.addStretch()
        project_header_layout.addWidget(project_close_btn)
        project_layout.addWidget(project_header)

        # Content area for Project Details, with scroll
        self.project_details_scroll_area = QScrollArea(self.project_panel)
        self.project_details_scroll_area.setWidgetResizable(True)
        self.project_details_scroll_area.setStyleSheet("QScrollArea { border: none; } QWidget#projectScrollContent { background-color: white; }")

        self.project_details_content_widget = QWidget()
        self.project_details_content_widget.setObjectName("projectScrollContent")
        self.project_details_content_widget_layout = QVBoxLayout(self.project_details_content_widget)
        self.project_details_content_widget_layout.setContentsMargins(10, 10, 10, 10)
        self.project_details_content_widget_layout.setSpacing(10)

        # --- General Information Section ---
        self.generalInfoGroup = QtWidgets.QGroupBox("General Information", self.project_details_content_widget)
        self.generalInfoGroup.setCheckable(True)
        self.generalInfoGroup.setChecked(False)
        self.generalInfoGroup.setStyleSheet("QGroupBox { background-color: rgb(240,230,230); border: 1px solid gray; border-radius: 5px; margin-top: 1ex; }"
                                            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; background-color: rgb(240,230,230); }"
                                            "QGroupBox::indicator { width: 13px; height: 13px; }"
                                            "QGroupBox::indicator:checked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled (1).png); }"
                                            "QGroupBox::indicator:unchecked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png); }")

        self.gridLayout_2 = QtWidgets.QFormLayout(self.generalInfoGroup)
        self.gridLayout_2.setContentsMargins(10, 20, 10, 10)
        self.gridLayout_2.setSpacing(10)

        self.label_company_name = QtWidgets.QLabel("Company Name")
        self.lineEdit_company_name = QtWidgets.QLineEdit()
        self.lineEdit_company_name.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_company_name, self.lineEdit_company_name)

        self.label_project_title = QtWidgets.QLabel("Project Title")
        self.lineEdit_project_title = QtWidgets.QLineEdit()
        self.lineEdit_project_title.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_project_title, self.lineEdit_project_title)

        self.label_project_description = QtWidgets.QLabel("Project Description")
        self.textEdit_project_description = QtWidgets.QTextEdit()
        self.textEdit_project_description.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_project_description, self.textEdit_project_description)

        self.label_valuer_name = QtWidgets.QLabel("Name of Valuer")
        self.lineEdit_valuer_name = QtWidgets.QLineEdit()
        self.lineEdit_valuer_name.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_valuer_name, self.lineEdit_valuer_name)

        self.label_job_number = QtWidgets.QLabel("Job Number")
        self.lineEdit_job_number = QtWidgets.QLineEdit()
        self.lineEdit_job_number.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_job_number, self.lineEdit_job_number)
        
        self.label_client = QtWidgets.QLabel("Client")
        self.lineEdit_client = QtWidgets.QLineEdit()
        self.lineEdit_client.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_client, self.lineEdit_client)

        self.label_country = QtWidgets.QLabel("Country")
        self.comboBox_country = QtWidgets.QComboBox()
        # Set frame to True to encourage integrated dropdown
        self.comboBox_country.setFrame(True) 
        # Add border style to make it visually clear it's a framed widget
        self.comboBox_country.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #cccccc; /* Added border */
                border-radius: 3px; /* Optional: adds slight rounding */
                padding: 1px 0px 1px 3px; /* Adjust padding for text */
            }
            QComboBox::drop-down {
                border-left: 1px solid #cccccc; /* Separator for the arrow button */
                width: 20px; /* Width of the arrow button area */
            }
            QComboBox::down-arrow {
                image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/arrow_down.png); /* Path to your down arrow icon if you have one */
                /* If you don't have a custom arrow, remove this line or replace with a default one */
            }
        """)
        countries = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
            "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
            "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
            "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)",
            "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
            "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
            "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
            "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
            "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
            "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
            "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
            "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
            "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
            "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
            "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
            "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa",
            "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
            "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
            "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
            "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
        ]
        self.comboBox_country.addItems(countries)

        self.label_base_year = QtWidgets.QLabel("Base Year")
        self.lineEdit_base_year = QtWidgets.QLineEdit()
        self.lineEdit_base_year.setStyleSheet("background-color: #ffffff")
        self.gridLayout_2.addRow(self.label_base_year, self.lineEdit_base_year)

        self.project_details_content_widget_layout.addWidget(self.generalInfoGroup)


        # --- Input Parameters Section ---
        self.inputParamsGroup = QtWidgets.QGroupBox("Input Parameters", self.project_details_content_widget)
        self.inputParamsGroup.setCheckable(True)
        self.inputParamsGroup.setChecked(False)
        self.inputParamsGroup.setStyleSheet("QGroupBox { background-color: rgb(240,230,230); border: 1px solid gray; border-radius: 5px; margin-top: 1ex; }"
                                            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; background-color: rgb(240,230,230); }"
                                            "QGroupBox::indicator { width: 13px; height: 13px; }"
                                            "QGroupBox::indicator:checked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled (1).png); }"
                                            "QGroupBox::indicator:unchecked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png); }")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.inputParamsGroup)
        self.verticalLayout_3.setContentsMargins(10, 20, 10, 10)
        self.verticalLayout_3.setSpacing(5)

        self.pushButton = QtWidgets.QPushButton("Structure Works Data")
        self.pushButton.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.verticalLayout_3.addWidget(self.pushButton)

        self.gridLayout_3_widget = QtWidgets.QWidget() # Container for Structure Works sub-buttons
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayout_3_widget)
        self.gridLayout_3.setContentsMargins(20, 0, 0, 0)

        self.pushButton_2 = QtWidgets.QPushButton("Foundation", clicked=self.openFoundationWindow)
        self.pushButton_2.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton("Super-Structure", clicked=self.openSuperStructureWindow)
        self.pushButton_3.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.gridLayout_3.addWidget(self.pushButton_3, 1, 0, 1, 1)

        self.pushButton_4 = QtWidgets.QPushButton("Sub-Structure", clicked=self.openSubStructureWindow)
        self.pushButton_4.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.gridLayout_3.addWidget(self.pushButton_4, 2, 0, 1, 1)

        self.pushButton_5 = QtWidgets.QPushButton("Miscellaneous", clicked=self.openMiscellaneousWindow)
        self.pushButton_5.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.gridLayout_3.addWidget(self.pushButton_5, 3, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.gridLayout_3_widget)


        self.pushButton_6 = QtWidgets.QPushButton("Financial Data", clicked=self.openFinancialWindow)
        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton("Carbon Emission Data")
        self.pushButton_7.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setChecked(False)
        self.verticalLayout_3.addWidget(self.pushButton_7)

        self.gridLayout_4_widget = QtWidgets.QWidget() # Container for Carbon Emission sub-buttons
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayout_4_widget)
        self.gridLayout_4.setContentsMargins(20, 0, 0, 0)

        self.pushButton_8 = QtWidgets.QPushButton("Carbon Emission Cost Data", clicked=self.openCarbonEmissionWindow)
        self.pushButton_8.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))
        self.gridLayout_4.addWidget(self.pushButton_8, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.gridLayout_4_widget)

        self.pushButton_9 = QtWidgets.QPushButton("Bridge and Traffic Data", clicked=self.openBridgeTrafficWindow)
        self.verticalLayout_3.addWidget(self.pushButton_9)

        self.pushButton_10 = QtWidgets.QPushButton("Maintenance and Repair", clicked=self.openMaintenanceWindow)
        self.verticalLayout_3.addWidget(self.pushButton_10)

        self.pushButton_11 = QtWidgets.QPushButton("Disposal and Recycling", clicked=self.openDemolitionWindow)
        self.verticalLayout_3.addWidget(self.pushButton_11)

        self.project_details_content_widget_layout.addWidget(self.inputParamsGroup)


        # --- Outputs Section ---
        self.outputsGroup = QtWidgets.QGroupBox("Outputs", self.project_details_content_widget)
        self.outputsGroup.setCheckable(True)
        self.outputsGroup.setChecked(False)
        self.outputsGroup.setStyleSheet("QGroupBox { background-color: rgb(240,230,230); border: 1px solid gray; border-radius: 5px; margin-top: 1ex; }"
                                        "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; background-color: rgb(240,230,230); }"
                                        "QGroupBox::indicator { width: 13px; height: 13px; }"
                                        "QGroupBox::indicator:checked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled (1).png); }"
                                        "QGroupBox::indicator:unchecked { image: url(C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png); }")
        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.outputsGroup)
        self.verticalLayout_4.setContentsMargins(10, 20, 10, 10)
        self.label_10 = QtWidgets.QLabel("Output content goes here.")
        self.verticalLayout_4.addWidget(self.label_10)

        self.project_details_content_widget_layout.addWidget(self.outputsGroup)
        self.project_details_content_widget_layout.addStretch(1)

        self.project_details_scroll_area.setWidget(self.project_details_content_widget)
        project_layout.addWidget(self.project_details_scroll_area)
        self.dynamic_content_stack.addWidget(self.project_panel)


        # --- Results Panel (Placeholder) ---
        self.results_panel = QWidget()
        results_layout = QVBoxLayout(self.results_panel)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_header = QWidget()
        results_header.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #e0e0e0;")
        results_header.setFixedHeight(40)
        results_header_layout = QHBoxLayout(results_header)
        results_header_layout.setContentsMargins(5, 5, 5, 5)
        self.results_header_label = QLabel("Results")
        self.results_header_label.setFont(QFont("Arial", 10, QFont.Bold))
        results_header_layout.addWidget(self.results_header_label)
        results_header_layout.addStretch()
        results_layout.addWidget(results_header)
        results_layout.addWidget(QLabel("<h2>Results content goes here.</h2><p>This panel will display analytical results.</p>", self.results_panel))
        self.dynamic_content_stack.addWidget(self.results_panel)


        # --- Compare Panel (Placeholder) ---
        self.compare_panel = QWidget()
        compare_layout = QVBoxLayout(self.compare_panel)
        compare_layout.setContentsMargins(0, 0, 0, 0)
        compare_header = QWidget()
        compare_header.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #e0e0e0;")
        compare_header.setFixedHeight(40)
        compare_header_layout = QHBoxLayout(compare_header)
        compare_header_layout.setContentsMargins(5, 5, 5, 5)
        self.compare_header_label = QLabel("Compare")
        self.compare_header_label.setFont(QFont("Arial", 10, QFont.Bold))
        compare_header_layout.addWidget(self.compare_header_label)
        compare_header_layout.addStretch()
        compare_layout.addWidget(compare_header)
        compare_layout.addWidget(QLabel("<h2>Compare different scenarios here.</h2><p>This panel will allow side-by-side comparisons.</p>", self.compare_panel))
        self.dynamic_content_stack.addWidget(self.compare_panel)


        # Add the static tutorial panel and the dynamic content stack to the main splitter
        self.content_splitter.addWidget(self.tutorials_panel)
        self.content_splitter.addWidget(self.dynamic_content_stack)

        # Set initial sizes for the splitter: Tutorials fixed, rest for dynamic content
        # These sizes will be adjusted by update_splitter_sizes based on panel visibility
        # For initial setup, we want tutorials visible and project details visible.
        # So Tutorials (300) and then the rest for the stacked widget.
        self.content_splitter.setSizes([300, self.width() - 300])


    def create_status_bar(self):
        self.statusBar = self.statusBar() # Assign status_bar to self.statusBar
        self.statusBar.setStyleSheet("background-color: #f0f0f0; border-top: 1px solid #e0e0e0;")

        # --- "Data" section at the bottom ---
        self.data_widget = QWidget()
        self.data_layout = QHBoxLayout(self.data_widget)
        self.data_layout.setContentsMargins(5, 0, 5, 0)
        self.data_layout.setSpacing(5)

        data_label = QLabel("Data")
        data_label.setFont(QFont("Arial", 9, QFont.Bold))
        self.data_layout.addWidget(data_label)

        look_up_label = QLabel("Look up:")
        self.data_layout.addWidget(look_up_label)
        self.combo_box_lookup = QComboBox()
        self.combo_box_lookup.addItems(["Carbon Data", "Maintenance Rate Data", "Recycling Data"])
        self.combo_box_lookup.setStyleSheet("background-color: white; border: 1px solid #cccccc; padding: 2px;")
        self.data_layout.addWidget(self.combo_box_lookup)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Search...")
        self.search_line_edit.setStyleSheet("background-color: white; border: 1px solid #cccccc; padding: 2px;")
        self.data_layout.addWidget(self.search_line_edit)

        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                padding: 3px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        self.data_layout.addWidget(search_button)

        self.data_layout.addStretch(1)

        self.statusBar.addPermanentWidget(self.data_widget)


    def update_tutorial_content(self):
        page_data = self.tutorial_pages[self.current_tutorial_page - 1]

        self.page_label.setText(page_data["page_number"])
        self.welcome_label.setText(page_data["title"])
        self.description_label.setText(page_data["content"])

    def tutorial_next(self):
        if self.current_tutorial_page < self.total_tutorial_pages:
            self.current_tutorial_page += 1
            self.update_tutorial_content()

    def tutorial_back(self):
        if self.current_tutorial_page > 1:
            self.current_tutorial_page -= 1
            self.update_tutorial_content()

    def close_tutorials(self):
        self.tutorials_panel.hide()
        if "Tutorials" in self.tab_buttons:
            self.tab_buttons["Tutorials"].setChecked(False)
            self.tab_buttons["Tutorials"].setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-bottom: none;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    padding: 5px 15px;
                    margin: 0px 2px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
            """)
        self.update_splitter_sizes()

    def close_project_details(self):
        # This function should probably hide the current dynamic panel and potentially
        # uncheck its associated custom tab button.
        # For simplicity, if the Project Details panel's close button is clicked,
        # it will hide the *entire* dynamic content stack and uncheck Project Details button.
        self.dynamic_content_stack.hide()

        if "Project Details" in self.tab_buttons:
            self.tab_buttons["Project Details"].setChecked(False)
            self.tab_buttons["Project Details"].setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-bottom: none;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    padding: 5px 15px;
                    margin: 0px 2px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
            """)
        self.update_splitter_sizes()


    def update_splitter_sizes(self):
        """Adjusts splitter sizes based on currently visible panels."""
        sizes = [0, 0] # Initial sizes for tutorials_panel and dynamic_content_stack

        if self.tutorials_panel.isVisible():
            sizes[0] = self.tutorials_panel.width()
        
        if self.dynamic_content_stack.isVisible():
            sizes[1] = self.content_splitter.width() - sizes[0]
        
        self.content_splitter.setSizes(sizes)


    # --- Methods for Project Details Collapsible Groups ---
    def toggle_general_info_group_content(self, group_box, checked):
        widgets_to_toggle = [
            self.label_company_name, self.lineEdit_company_name,
            self.label_project_title, self.lineEdit_project_title,
            self.label_project_description, self.textEdit_project_description,
            self.label_valuer_name, self.lineEdit_valuer_name,
            self.label_job_number, self.lineEdit_job_number,
            self.label_client, self.lineEdit_client,
            self.label_country, self.comboBox_country,
            self.label_base_year, self.lineEdit_base_year
        ]
        for widget in widgets_to_toggle:
            widget.setVisible(checked)
        self.update_group_indicator_style(group_box, checked)

    def toggle_input_params_group_content(self, group_box, checked):
        self.pushButton.setVisible(checked)
        self.pushButton_6.setVisible(checked)
        self.pushButton_7.setVisible(checked)
        self.pushButton_9.setVisible(checked)
        self.pushButton_10.setVisible(checked)
        self.pushButton_11.setVisible(checked)

        if checked:
            self.gridLayout_3_widget.setVisible(self.pushButton.isChecked())
            self.gridLayout_4_widget.setVisible(self.pushButton_7.isChecked())
        else:
            self.gridLayout_3_widget.setVisible(False)
            self.gridLayout_4_widget.setVisible(False)
        
        self.update_group_indicator_style(group_box, checked)

    def toggle_outputs_group_content(self, group_box, checked):
        self.label_10.setVisible(checked)
        self.update_group_indicator_style(group_box, checked)

    def update_group_indicator_style(self, group_box, is_checked):
        style = group_box.styleSheet()
        if is_checked:
            style = style.replace("indicator:unchecked", "indicator:checked")
        else:
            style = style.replace("indicator:checked", "indicator:unchecked")
        group_box.setStyleSheet(style)

    def toggle_sub_buttons_visibility(self, layout, toggle_button):
        is_checked = toggle_button.isChecked()
        layout.parentWidget().setVisible(is_checked) # Hide/show the container widget of the layout
        
        if is_checked:
            toggle_button.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled (1).png"))
        else:
            toggle_button.setIcon(QtGui.QIcon("C:/Users/saans/AppData/Local/Programs/Python/Python310/Lib/site-packages/qt5_applications/Qt/bin/../../../../../../../../../../Downloads/play_arrow_filled.png"))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "<untitled draft> - BICCA Studio 1.0.0"))
        
        # Custom Tab button texts
        self.tab_buttons["Tutorials"].setText(_translate("MainWindow", "Tutorials"))
        self.tab_buttons["Project Details"].setText(_translate("MainWindow", "Project Details"))
        self.tab_buttons["Results"].setText(_translate("MainWindow", "Results"))
        self.tab_buttons["Compare"].setText(_translate("MainWindow", "Compare"))

        # Headers for panels
        self.tutorials_header_label.setText(_translate("MainWindow", "Tutorials"))
        self.project_header_label.setText(_translate("MainWindow", "Project Details Window"))
        self.results_header_label.setText(_translate("MainWindow", "Results"))
        self.compare_header_label.setText(_translate("MainWindow", "Compare"))

        # Group Box Titles
        self.generalInfoGroup.setTitle(_translate("MainWindow", "General Information"))
        self.inputParamsGroup.setTitle(_translate("MainWindow", "Input Parameters"))
        self.outputsGroup.setTitle(_translate("MainWindow", "Outputs"))

        # General Information Labels and Placeholders
        self.label_company_name.setText(_translate("MainWindow", "Company Name"))
        self.lineEdit_company_name.setPlaceholderText(_translate("MainWindow", "Enter Company Name"))
        self.label_project_title.setText(_translate("MainWindow", "Project Title"))
        self.lineEdit_project_title.setPlaceholderText(_translate("MainWindow", "Enter Project Title"))
        self.label_project_description.setText(_translate("MainWindow", "Project Description"))
        self.textEdit_project_description.setPlaceholderText(_translate("MainWindow", "Enter Project Description"))
        self.label_valuer_name.setText(_translate("MainWindow", "Name of Valuer"))
        self.lineEdit_valuer_name.setPlaceholderText(_translate("MainWindow", "Enter Valuer's Name"))
        self.label_job_number.setText(_translate("MainWindow", "Job Number"))
        self.lineEdit_job_number.setPlaceholderText(_translate("MainWindow", "Enter Job Number"))
        self.label_client.setText(_translate("MainWindow", "Client"))
        self.lineEdit_client.setPlaceholderText(_translate("MainWindow", "Enter Client Name"))
        self.label_country.setText(_translate("MainWindow", "Country"))
        self.label_base_year.setText(_translate("MainWindow", "Base Year"))
        self.lineEdit_base_year.setPlaceholderText(_translate("MainWindow", "e.g., 2023"))

        # Input Parameters Buttons
        self.pushButton.setText(_translate("MainWindow", "Structure Works Data"))
        self.pushButton_3.setText(_translate("MainWindow", "Super-Structure"))
        self.pushButton_2.setText(_translate("MainWindow", "Foundation"))
        self.pushButton_4.setText(_translate("MainWindow", "Sub-Structure"))
        self.pushButton_5.setText(_translate("MainWindow", "Miscellaneous"))
        self.pushButton_6.setText(_translate("MainWindow", "Financial Data"))
        self.pushButton_7.setText(_translate("MainWindow", "Carbon Emission Data"))
        self.pushButton_8.setText(_translate("MainWindow", "Carbon Emission Cost Data"))
        self.pushButton_9.setText(_translate("MainWindow", "Bridge and Traffic Data"))
        self.pushButton_10.setText(_translate("MainWindow", "Maintenance and Repair"))
        self.pushButton_11.setText(_translate("MainWindow", "Disposal and Recycling"))

        # Outputs Label
        self.label_10.setText(_translate("MainWindow", "Output content goes here."))

        # Menu and Toolbar actions
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuReports.setTitle(_translate("MainWindow", "Reports"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionCreate_a_Copy.setText(_translate("MainWindow", "Create a Copy"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionRename.setText(_translate("MainWindow", "Rename"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionVersion_History.setText(_translate("MainWindow", "Version History"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionContact_Us.setText(_translate("MainWindow", "Contact Us"))
        self.actionFeedback.setText(_translate("MainWindow", "Feedback"))
        self.actionVideo_Tutorials.setText(_translate("MainWindow", "Video Tutorials"))
        self.actionJoin_our_Community.setText(_translate("MainWindow", "Join our Community"))

        # Data section retranslate
        self.combo_box_lookup.setItemText(0, _translate("MainWindow", "Carbon Data"))
        self.combo_box_lookup.setItemText(1, _translate("MainWindow", "Maintenance Rate Data"))
        self.combo_box_lookup.setItemText(2, _translate("MainWindow", "Recycling Data"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
