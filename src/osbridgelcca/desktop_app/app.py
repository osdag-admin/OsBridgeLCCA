import sys
import csv
import json
from PyQt5 import QtWidgets
from ui.input_form import save_general_info
from ui.project_details_windows.ProjectDetails_BridgeANDTrafficData_Window import Ui_BridgeTraffic_Dialog
from ui.project_details_windows.ProjectDetails_Foundation_Window import Ui_Foundation_Dialog
from ui.project_details_windows.ProjectDetails_CarbonEmissionData_Window import Ui_CarbonEmission_Dialog
from ui.project_details_windows.ProjectDetails_DemolitionANDRecyclingData_Window import Ui_Demolition_Dialog
from ui.project_details_windows.ProjectDetails_FinancialData_Window import Ui_FinancialData_Dialog
from ui.project_details_windows.ProjectDetails_MaintenanceANDRepairData_Window import Ui_Maintenance_Dialog
from ui.project_details_windows.ProjectDetails_Miscellaneous_Window import Ui_Miscellaneous_Dialog
from ui.project_details_windows.ProjectDetails_SubStructure_Window import Ui_SubStructure_Dialog
from ui.project_details_windows.ProjectDetails_SuperStructure_Window import Ui_SuperStructure_Dialog
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTreeWidget, 
                            QTreeWidgetItem, QTabBar, QFrame, QSplitter, 
                            QToolBar, QAction, QGroupBox, QMenu, QLineEdit,
                            QComboBox, QMessageBox, QGridLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class BICCAStudio(QMainWindow):
    def openBridgeTrafficWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_BridgeTraffic_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openFoundationWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Foundation_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openCarbonEmissionWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_CarbonEmission_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openDemolitionWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Demolition_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openFinancialWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_FinancialData_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openMaintenanceWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Maintenance_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openMiscellaneousWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Miscellaneous_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openSubStructureWindow(self):   
        self.window = QtWidgets.QDialog()
        self.ui = Ui_SubStructure_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def openSuperStructureWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_SuperStructure_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("<untitled draft> - BICCA Studio 1.0.0")
        self.setGeometry(100, 40, 1440, 900)
        self.setStyleSheet("background-color: #f5f5f5;")
        
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
        
        # Create the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create menu bar with dropdown menus
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create window tabs
        self.create_window_tabs()
        
        # Create main content area
        self.create_content_area()
        self.show_tutorials_only()  # Show only tutorials at launch
        
        # Add status bar with Data button
        self.create_status_bar()
        
        # Initially hide dropdown menus
        self.file_menu_widget = QWidget(self)
        self.file_menu_widget.hide()
        self.help_menu_widget = QWidget(self)
        self.help_menu_widget.hide()
        
        # Update tutorial content to first page
        self.update_tutorial_content()
        
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setObjectName("menubar")
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #4C9141;
                color: white;
            }
            QMenuBar::item {
                background-color: white;
                color: black;
                padding: 5px 25px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
        """)

        # File menu
        self.menuFile = QMenu("File", self)
        self.menuFile.setObjectName("menuFile")
        menubar.addMenu(self.menuFile)

        # Home menu
        self.menuHome = QMenu("Home", self)
        self.menuHome.setObjectName("menuHome")
        menubar.addMenu(self.menuHome)

        # Reports menu
        self.menuReports = QMenu("Reports", self)
        self.menuReports.setObjectName("menuReports")
        menubar.addMenu(self.menuReports)

        # Help menu
        self.menuHelp = QMenu("Help", self)
        self.menuHelp.setObjectName("menuHelp")
        menubar.addMenu(self.menuHelp)

        # Actions with icons (update icon paths as needed)
        from PyQt5.QtGui import QIcon, QPixmap

        def icon(path):
            return QIcon(QPixmap(path))

        self.actionNew = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Vector.png"), "New", self)
        self.actionOpen = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Vector (1).png"), "Open", self)
        self.actionSave = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _save action floppy_.png"), "Save", self)
        self.actionSave_As = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _document save as template_.png"), "Save As...", self)
        self.actionCreate_a_Copy = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _file copy_.png"), "Create a Copy", self)
        self.actionPrint = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Vector (2).png"), "Print", self)
        self.actionRename = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Vector (3).png"), "Rename", self)
        self.actionExport = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Export.png"), "Export", self)
        self.actionVersion_History = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Vector (4).png"), "Version History", self)
        self.actionInfo = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Alert Circle.png"), "Info", self)
        self.actionContact_Us = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Contact.png"), "Contact Us", self)
        self.actionFeedback = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _Person Feedback_.png"), "Feedback", self)
        self.actionVideo_Tutorials = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _youtube_.png"), "Video Tutorials", self)
        self.actionJoin_our_Community = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/🦆 icon _People Community_.png"), "Join our Community", self)
        self.actionEdit = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/08b7798a84ffe0528bdec7dc8efe8fb1c89f77ae.png"), "Edit", self)
        self.actionFile = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Icon.png"), "File", self)
        self.actionOpen_File = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/78ff94ca74c504343b797700f5d515a40ab72143.png"), "Open File", self)

        # Add actions to File menu
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionCreate_a_Copy)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionRename)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionVersion_History)
        self.menuFile.addAction(self.actionInfo)

        # Add actions to Help menu
        self.menuHelp.addAction(self.actionContact_Us)
        self.menuHelp.addAction(self.actionFeedback)
        self.menuHelp.addAction(self.actionVideo_Tutorials)
        self.menuHelp.addAction(self.actionJoin_our_Community)

        # Optionally, add actions to toolbar if you want
        # self.addToolBar(Qt.LeftToolBarArea, QToolBar(self)).addAction(self.actionEdit)
        # self.addToolBar(Qt.LeftToolBarArea, QToolBar(self)).addAction(self.actionFile)
        # self.addToolBar(Qt.LeftToolBarArea, QToolBar(self)).addAction(self.actionOpen_File)
    
    def toggle_file_menu(self):
        # Close help menu if it's open
        self.help_menu_widget.hide()
        
        # Toggle file menu
        if self.file_menu_widget.isVisible():
            self.file_menu_widget.hide()
        else:
            self.file_menu_widget.show()
            self.file_menu_widget.raise_()
    
    def toggle_help_menu(self):
        # Close file menu if it's open
        self.file_menu_widget.hide()
        
        # Toggle help menu
        if self.help_menu_widget.isVisible():
            self.help_menu_widget.hide()
        else:
            self.help_menu_widget.show()
            self.help_menu_widget.raise_()
    
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        # Use the same icons as in MainWindow.py (update paths if needed)
        from PyQt5.QtGui import QIcon, QPixmap

        def icon(path):
            return QIcon(QPixmap(path))

        self.actionEdit = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/08b7798a84ffe0528bdec7dc8efe8fb1c89f77ae.png"), "Edit", self)
        self.actionFile = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/Icon.png"), "File", self)
        self.actionOpen_File = QAction(icon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/78ff94ca74c504343b797700f5d515a40ab72143.png"), "Open File", self)

        toolbar.addAction(self.actionEdit)
        toolbar.addAction(self.actionFile)
        toolbar.addAction(self.actionOpen_File)
        toolbar.addSeparator()
    
    def create_window_tabs(self):
        # Create a container widget for better alignment
        window_tabs_container = QWidget()
        container_layout = QHBoxLayout(window_tabs_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left spacer to push content to center
        container_layout.addStretch(1)
        
        # Windows label with better spacing
        windows_label = QLabel("Windows:")
        windows_label.setStyleSheet("padding: 5px 10px 5px 0px;")
        container_layout.addWidget(windows_label)
        
        # Store tab buttons for later use
        self.tab_buttons = {}

        # Create tab buttons with better spacing
        tabs = ["Tutorials", "Project Details", "Results", "Compare"]
        for i, tab_name in enumerate(tabs):
            tab_btn = QPushButton(tab_name)
            tab_btn.setStyleSheet("""
                QPushButton {
                    background-color: #EEEEEE;
                    border: 1px solid #CCCCCC;
                    padding: 5px 10px;
                    margin: 0px 2px;
                }
                QPushButton:pressed {
                    background-color: #DDDDDD;
                }
            """)
            container_layout.addWidget(tab_btn)
            self.tab_buttons[tab_name] = tab_btn
            # Connect each tab to its handler
            if tab_name == "Tutorials":
                tab_btn.clicked.connect(self.show_tutorials_only)
            elif tab_name == "Project Details":
                tab_btn.clicked.connect(self.show_project_details)
            # Results and Compare can be connected later

        # Right spacer to push content to center
        container_layout.addStretch(1)
        
        window_tabs_container.setFixedHeight(40)
        self.main_layout.addWidget(window_tabs_container)
    
    def show_tutorials_only(self):
        # Hide project details panel
        self.project_panel.setVisible(False)
        # Set tutorials panel max width to 771
        self.tutorials_panel.setMaximumWidth(771)
        # Center the tutorials panel in the main window
        self.splitter.setSizes([1, 0])
        # Optionally, expand tutorials to fill available space
        self.tutorials_panel.setMinimumWidth(0)
        self.tutorials_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

    def show_project_details(self):
        # Show both panels
        self.project_panel.setVisible(True)
        # Restore tutorials panel max width to 244
        self.tutorials_panel.setMaximumWidth(244)
        self.tutorials_panel.setMinimumWidth(0)
        self.tutorials_panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # Reset splitter sizes for normal layout
        self.splitter.setSizes([200, 750])
    
    def create_content_area(self):
        def get_country_name(filename = "src//osbridgelcca//desktop_app//assets//country_abbreviations.csv"):
            country_names_lst = []

            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skiping header row
                for row in reader:
                    country_names_lst.append(row[1])
            return country_names_lst
    
        def get_base_year(filename = "src//osbridgelcca//desktop_app//assets//years_2000_to_2025.csv"):
            base_years_lst = []

            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skiping header row
                for row in reader:
                    base_years_lst.append(row[0])
            return base_years_lst
        

        self.splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Tutorials panel
        self.tutorials_panel = QWidget()
        self.tutorials_panel.setMaximumWidth(771)  # Start with max 771 for launch
        tutorials_layout = QVBoxLayout(self.tutorials_panel)
        tutorials_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tutorial header
        tutorials_header = QWidget()
        tutorials_header.setStyleSheet("background-color: #f0e6e6;")
        tutorials_header_layout = QHBoxLayout(tutorials_header)
        tutorials_header_layout.setContentsMargins(5, 5, 5, 5)
        
        tutorials_label = QLabel("Tutorials")
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("border: none;")
        close_btn.clicked.connect(self.close_tutorials)
        
        tutorials_header_layout.addWidget(tutorials_label)
        tutorials_header_layout.addStretch()
        tutorials_header_layout.addWidget(close_btn)
        
        # Tutorial content with light pink background
        self.tutorials_content = QWidget()
        self.tutorials_content.setStyleSheet("background-color: #f9f0f0;")
        self.tutorials_content_layout = QVBoxLayout(self.tutorials_content)
        
        # Create labels that will be updated dynamically
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("font-weight: bold; padding: 5px; border-bottom: 1px solid #ddd;")
        
        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-weight: bold; padding: 10px; border-bottom: 1px solid #ddd;")
        
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("padding: 10px;")
        
        self.tutorials_content_layout.addWidget(self.page_label)
        self.tutorials_content_layout.addWidget(self.welcome_label)
        self.tutorials_content_layout.addWidget(self.description_label)
        self.tutorials_content_layout.addStretch()
        
        # Tutorial navigation buttons
        nav_buttons = QWidget()
        nav_buttons.setStyleSheet("background-color: #f9f0f0;")
        nav_layout = QHBoxLayout(nav_buttons)
        nav_layout.setContentsMargins(10, 5, 10, 5)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 5px 15px;
                border-radius: 3px;
            }
        """)
        back_btn.clicked.connect(self.tutorial_back)
        
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 5px 15px;
                border-radius: 3px;
            }
        """)
        next_btn.clicked.connect(self.tutorial_next)
        
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)
        
        tutorials_layout.addWidget(tutorials_header)
        tutorials_layout.addWidget(self.tutorials_content)
        tutorials_layout.addWidget(nav_buttons)
        
        # Right side - Project Details panel
        self.project_panel = QWidget()
        self.project_panel.setMaximumWidth(771)
        project_layout = QVBoxLayout(self.project_panel)
        project_layout.setContentsMargins(0, 0, 0, 0)
        
        # Project header
        project_header = QWidget()
        project_header.setStyleSheet("background-color: #f0f0f0;")
        project_header_layout = QHBoxLayout(project_header)
        project_header_layout.setContentsMargins(5, 5, 5, 5)
        
        project_label = QLabel("Project Details Window")
        project_close_btn = QPushButton("×")
        project_close_btn.setFixedSize(20, 20)
        project_close_btn.setStyleSheet("font-weight: bold; border: none;")
        project_close_btn.clicked.connect(self.close_project_details)
        
        project_header_layout.addWidget(project_label)
        project_header_layout.addStretch()
        project_header_layout.addWidget(project_close_btn)
        
        # Create collapsible sections
        project_content = QWidget()
        project_content_layout = QVBoxLayout(project_content)
        project_content_layout.setContentsMargins(10, 10, 10, 10)
        
        # General Information section (collapsible)
        general_info_box = QGroupBox()
        general_info_box.setStyleSheet("""
            QGroupBox {
                background-color: #f0e6e6;
                border-radius: 3px;
                margin-bottom: 5px;
            }
        """)
        general_info_layout = QVBoxLayout(general_info_box)
        general_info_layout.setContentsMargins(10, 10, 10, 10)
        
        # Collapsible header
        self.general_info_btn = QPushButton("► General Information")
        self.general_info_btn.setCheckable(True)
        self.general_info_btn.setChecked(False)
        self.general_info_btn.setStyleSheet("font-weight: bold; text-align: left; background: none; border: none;")
        general_info_layout.addWidget(self.general_info_btn)

        # Content widget
        self.general_info_content = QWidget()
        self.general_info_content.setStyleSheet("background-color: #fff9f9;")
        form_layout = QGridLayout(self.general_info_content)
        form_layout.setSpacing(10)

        # Company Name
        company_label = QLabel("Company Name")
        company_label.setFixedWidth(150)
        company_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        company_edit = QLineEdit()
        company_edit.setFixedWidth(483)
        company_edit.setFixedHeight(25)
        company_edit.setStyleSheet("background-color: #ffffff;")

        # Project Title
        title_label = QLabel("Project Title")
        title_label.setFixedWidth(150)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_edit = QLineEdit()
        title_edit.setFixedWidth(483)
        title_edit.setFixedHeight(25)
        title_edit.setStyleSheet("background-color: #ffffff;")

        # Project Description
        desc_label = QLabel("Project Description")
        desc_label.setFixedWidth(150)
        desc_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        desc_edit = QLineEdit()
        desc_edit.setFixedWidth(483)
        desc_edit.setFixedHeight(125)
        desc_edit.setStyleSheet("background-color: #ffffff;")

        # Name of Valuer
        valuer_label = QLabel("Name of Valuer")
        valuer_label.setFixedWidth(150)
        valuer_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        valuer_combo = QComboBox()
        valuer_combo.setFixedWidth(164)
        valuer_combo.setFixedHeight(19)
        valuer_combo.setStyleSheet("background-color: #ffffff;")
        for valuer in get_country_name():
            valuer_combo.addItem(valuer)

        # Job Number
        job_label = QLabel("Job Number")
        job_label.setFixedWidth(150)
        job_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        job_edit = QLineEdit()
        job_edit.setFixedWidth(164)
        job_edit.setFixedHeight(19)
        job_edit.setStyleSheet("background-color: #ffffff;")

        # Client
        client_label = QLabel("Client")
        client_label.setFixedWidth(150)
        client_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        client_edit = QLineEdit()
        client_edit.setFixedWidth(164)
        client_edit.setFixedHeight(19)
        client_edit.setStyleSheet("background-color: #ffffff;")

        # Country
        country_label = QLabel("Country")
        country_label.setFixedWidth(150)
        country_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        country_combo = QComboBox()
        country_combo.setFixedWidth(164)
        country_combo.setFixedHeight(19)
        country_combo.setStyleSheet("background-color: #ffffff;")
        for country in get_country_name():
            country_combo.addItem(country)

        # Base Year
        year_label = QLabel("Base Year")
        year_label.setFixedWidth(150)
        year_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        year_combo = QComboBox()
        year_combo.setFixedWidth(164)
        year_combo.setFixedHeight(19)
        year_combo.setStyleSheet("background-color: #ffffff;")
        for year in get_base_year():
            year_combo.addItem(year)

        # Add widgets to grid layout (row, column)
        form_layout.addWidget(company_label, 0, 0)
        form_layout.addWidget(company_edit, 0, 1)
        form_layout.addWidget(title_label, 1, 0)
        form_layout.addWidget(title_edit, 1, 1)
        form_layout.addWidget(desc_label, 2, 0)
        form_layout.addWidget(desc_edit, 2, 1)
        form_layout.addWidget(valuer_label, 3, 0)
        form_layout.addWidget(valuer_combo, 3, 1)
        form_layout.addWidget(job_label, 4, 0)
        form_layout.addWidget(job_edit, 4, 1)
        form_layout.addWidget(client_label, 5, 0)
        form_layout.addWidget(client_edit, 5, 1)
        form_layout.addWidget(country_label, 6, 0)
        form_layout.addWidget(country_combo, 6, 1)
        form_layout.addWidget(year_label, 7, 0)
        form_layout.addWidget(year_combo, 7, 1)

        # Add Save button
        save_btn = QPushButton("Save General Info")
        save_btn.setStyleSheet("background-color: #4C9141; color: white; font-weight: bold; padding: 6px 18px;")
        form_layout.addWidget(save_btn)

        # Store references to the input widgets for later access
        self.company_edit = company_edit
        self.title_edit = title_edit
        self.desc_edit = desc_edit
        self.valuer_combo = valuer_combo
        self.job_edit = job_edit
        self.client_edit = client_edit
        self.country_combo = country_combo
        self.year_combo = year_combo

        # Connect the save button
        save_btn.clicked.connect(self.save_general_info_data)
        
        general_info_layout.addWidget(self.general_info_content)

        def toggle_general_info_content(checked):
            self.general_info_content.setVisible(checked)
            self.general_info_btn.setText("▼ General Information" if checked else "► General Information")
        self.general_info_btn.toggled.connect(toggle_general_info_content)

        self.general_info_content.setVisible(False)
        
        # Input Parameters section (collapsible)
        input_params_box = QGroupBox()
        input_params_box.setStyleSheet("""
            QGroupBox {
                background-color: #f0e6e6;
                border-radius: 3px;
                margin-bottom: 5px;
            }
        """)
        input_params_layout = QVBoxLayout(input_params_box)
        input_params_layout.setContentsMargins(10, 10, 10, 10)
        
        self.input_params_btn = QPushButton("► Input Parameters")
        self.input_params_btn.setCheckable(True)
        self.input_params_btn.setChecked(False)
        self.input_params_btn.setStyleSheet("font-weight: bold; text-align: left; background: none; border: none;")
        input_params_layout.addWidget(self.input_params_btn)

        self.input_params_content = QWidget()
        self.input_params_content.setStyleSheet("background-color: rgb(240, 230, 230);")
        input_params_content_layout = QVBoxLayout(self.input_params_content)
        input_params_content_layout.setSpacing(10)

        # --- Begin: Copied from MainWindow.py's self.widget_5 ---

        # Structure Works Data (collapsible)
        structure_box = QGroupBox()
        structure_box.setStyleSheet("background-color: rgb(240,230,230); margin-bottom: 5px;")
        structure_layout = QVBoxLayout(structure_box)
        structure_layout.setContentsMargins(5, 5, 5, 5)

        self.structure_btn = QPushButton("► Structure Works Data")
        self.structure_btn.setCheckable(True)
        self.structure_btn.setChecked(False)
        self.structure_btn.setStyleSheet("text-align: left; background: none; border: none;")
        structure_layout.addWidget(self.structure_btn)

        self.structure_content = QWidget()
        structure_content_layout = QVBoxLayout(self.structure_content)
        structure_content_layout.setSpacing(6)

        # Foundation
        foundation_btn = QPushButton(" Foundation")
        foundation_btn.setIcon(QIcon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/play_arrow_filled.png"))
        foundation_btn.setStyleSheet("text-align: left;")
        foundation_btn.clicked.connect(self.openFoundationWindow)
        structure_content_layout.addWidget(foundation_btn)

        # Super-Structure
        superstructure_btn = QPushButton(" Super-Structure")
        superstructure_btn.setIcon(QIcon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/play_arrow_filled.png"))
        superstructure_btn.setStyleSheet("text-align: left;")
        superstructure_btn.clicked.connect(self.openSuperStructureWindow)
        structure_content_layout.addWidget(superstructure_btn)

        # Sub-Structure
        substructure_btn = QPushButton(" Sub-Structure")
        substructure_btn.setIcon(QIcon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/play_arrow_filled.png"))
        substructure_btn.setStyleSheet("text-align: left;")
        substructure_btn.clicked.connect(self.openSubStructureWindow)
        structure_content_layout.addWidget(substructure_btn)

        # Miscellaneous
        misc_btn = QPushButton(" Miscellaneous")
        misc_btn.setIcon(QIcon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/play_arrow_filled.png"))
        misc_btn.setStyleSheet("text-align: left;")
        misc_btn.clicked.connect(self.openMiscellaneousWindow)
        structure_content_layout.addWidget(misc_btn)

        self.structure_content.setVisible(False)
        structure_layout.addWidget(self.structure_content)

        def toggle_structure_content(checked):
            self.structure_content.setVisible(checked)
            self.structure_btn.setText("▼ Structure Works Data" if checked else "► Structure Works Data")
        self.structure_btn.toggled.connect(toggle_structure_content)

        self.input_params_content.setVisible(False)
        input_params_content_layout.addWidget(structure_box)

        # Financial Data
        financial_btn = QPushButton("► Financial Data")
        financial_btn.setStyleSheet("text-align: left;")
        financial_btn.clicked.connect(self.openFinancialWindow)
        input_params_content_layout.addWidget(financial_btn)

        # Carbon Emission Data (collapsible)
        carbon_box = QGroupBox()
        carbon_box.setStyleSheet("background-color: rgb(240,230,230); margin-bottom: 5px;")
        carbon_layout = QVBoxLayout(carbon_box)
        carbon_layout.setContentsMargins(5, 5, 5, 5)

        self.carbon_btn = QPushButton("► Carbon Emission Data")
        self.carbon_btn.setCheckable(True)
        self.carbon_btn.setChecked(False)
        self.carbon_btn.setStyleSheet(" text-align: left; background: none; border: none;")
        carbon_layout.addWidget(self.carbon_btn)

        self.carbon_content = QWidget()
        carbon_content_layout = QVBoxLayout(self.carbon_content)
        carbon_content_layout.setSpacing(6)

        carbon_cost_btn = QPushButton(" Carbon Emission Cost Data")
        carbon_cost_btn.setIcon(QIcon("src/osbridgelcca/desktop_app/assets/MainWindow_icons/play_arrow_filled.png"))
        carbon_cost_btn.setStyleSheet("text-align: left;")
        carbon_cost_btn.clicked.connect(self.openCarbonEmissionWindow)
        carbon_content_layout.addWidget(carbon_cost_btn)

        self.carbon_content.setVisible(False)
        carbon_layout.addWidget(self.carbon_content)

        def toggle_carbon_content(checked):
            self.carbon_content.setVisible(checked)
            self.carbon_btn.setText("▼ Carbon Emission Data" if checked else "► Carbon Emission Data")
        self.carbon_btn.toggled.connect(toggle_carbon_content)

        input_params_content_layout.addWidget(carbon_box)

        # Bridge and Traffic Data
        bridge_btn = QPushButton("► Bridge and Traffic Data")
        bridge_btn.setStyleSheet("text-align: left;")
        bridge_btn.clicked.connect(self.openBridgeTrafficWindow)
        input_params_content_layout.addWidget(bridge_btn)

        # Maintenance and Repair
        maintenance_btn = QPushButton("► Maintenance and Repair")
        maintenance_btn.setStyleSheet("text-align: left;")
        maintenance_btn.clicked.connect(self.openMaintenanceWindow)
        input_params_content_layout.addWidget(maintenance_btn)

        # Disposal and Recycling
        demolition_btn = QPushButton("► Disposal and Recycling")
        demolition_btn.setStyleSheet("text-align: left;")
        demolition_btn.clicked.connect(self.openDemolitionWindow)
        input_params_content_layout.addWidget(demolition_btn)

        self.input_params_content.setVisible(False)
        input_params_layout.addWidget(self.input_params_content)

        
        def toggle_input_params_content(checked):
            self.input_params_content.setVisible(checked)
            self.input_params_btn.setText("▼ Input Parameters" if checked else "► Input Parameters")
        self.input_params_btn.toggled.connect(toggle_input_params_content)
        
        # Outputs section (collapsible)
        outputs_box = QGroupBox()
        outputs_box.setStyleSheet("""
            QGroupBox {
                background-color: #f0e6e6;
                border-radius: 3px;
                margin-bottom: 5px;
            }
        """)
        outputs_layout = QVBoxLayout(outputs_box)
        outputs_layout.setContentsMargins(10, 10, 10, 10)
        
        self.outputs_btn = QPushButton("► Outputs")
        self.outputs_btn.setCheckable(True)
        self.outputs_btn.setChecked(False)
        self.outputs_btn.setStyleSheet("font-weight: bold; text-align: left; background: none; border: none;")
        outputs_layout.addWidget(self.outputs_btn)

        self.outputs_content = QWidget()
        outputs_content_layout = QVBoxLayout(self.outputs_content)
        outputs_content_layout.setSpacing(10)
        # Add your outputs widgets here, e.g.:
        outputs_content_layout.addWidget(QLabel("Outputs fields go here..."))
        self.outputs_content.setVisible(False)
        outputs_layout.addWidget(self.outputs_content)

        def toggle_outputs_content(checked):
            self.outputs_content.setVisible(checked)
            self.outputs_btn.setText("▼ Outputs" if checked else "► Outputs")
        self.outputs_btn.toggled.connect(toggle_outputs_content)
        
        # Add all sections to the project content
        project_content_layout.addWidget(general_info_box)
        project_content_layout.addWidget(input_params_box)
        project_content_layout.addWidget(outputs_box)
        
        project_layout.addWidget(project_header)
        project_layout.addWidget(project_content)
        project_layout.addStretch()
        
        # Add both panels to the splitter
        self.splitter.addWidget(self.tutorials_panel)
        self.splitter.addWidget(self.project_panel)
        self.main_layout.addWidget(self.splitter)
    
    def create_status_bar(self):
        status_bar = self.statusBar()
        
        data_btn = QPushButton("▲ Data")
        data_btn.setStyleSheet("padding: 5px 15px;")
        
        status_bar.addPermanentWidget(data_btn)
    
    def update_tutorial_content(self):
        # Get current page data
        page_data = self.tutorial_pages[self.current_tutorial_page - 1]
        
        # Update the tutorial content
        self.page_label.setText(page_data["page_number"])
        self.welcome_label.setText(page_data["title"])
        self.description_label.setText(page_data["content"])
    
    def tutorial_next(self):
        if self.current_tutorial_page < self.total_tutorial_pages:
            self.current_tutorial_page += 1
            self.update_tutorial_content()
        elif self.current_tutorial_page == self.total_tutorial_pages:
            # Simulate clicking the Project Details tab button
            if "Project Details" in self.tab_buttons:
                self.tab_buttons["Project Details"].click()
    
    def tutorial_back(self):
        if self.current_tutorial_page > 1:
            self.current_tutorial_page -= 1
            self.update_tutorial_content()
    
    def close_tutorials(self):
        # Hide the tutorials panel (in a real app, you might want to remove or collapse it)
        self.sender().parent().parent().hide()
    
    def close_project_details(self):
        # Hide the project details panel
        self.sender().parent().parent().hide()
    
    def mousePressEvent(self, event):
        # Hide menus when clicking outside
        if self.file_menu_widget.isVisible() and not self.file_menu_widget.geometry().contains(event.pos()):
            self.file_menu_widget.hide()
        
        if self.help_menu_widget.isVisible() and not self.help_menu_widget.geometry().contains(event.pos()):
            self.help_menu_widget.hide()
        
        super().mousePressEvent(event)

    def save_general_info_data(self):
        data = {
            "company_name": self.company_edit.text(),
            "project_title": self.title_edit.text(),
            "project_description": self.desc_edit.text(),
            "name_of_valuer": self.valuer_combo.currentText(),
            "job_number": self.job_edit.text(),
            "client": self.client_edit.text(),
            "country": self.country_combo.currentText(),
            "base_year": self.year_combo.currentText(),
        }
        save_general_info(data)
        QMessageBox.information(self, "Success", "Data has been saved.")
        # self.confirm_button.setEnabled(False)

    def closeEvent(self, event):
        # Clearing the general_info.json file
        filename = "src//osbridgelcca//desktop_app//assets//general_info.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        super().closeEvent(event)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BICCAStudio()
    window.show()
    sys.exit(app.exec_())
#Sampel code for a PyQt5 desktop application given by the user
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from desktop_app.logic.controller import Controller


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OsBridgeLCCA - Desktop App")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.run_button = QPushButton("Run LCCA Analysis")
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_analysis(self):
        """Trigger analysis when button is clicked."""
        controller = Controller()
        controller.run_calculations()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
'''