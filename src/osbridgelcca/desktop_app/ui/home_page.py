import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTreeWidget, 
                            QTreeWidgetItem, QTabBar, QFrame, QSplitter, 
                            QToolBar, QAction, QGroupBox, QMenu, QLineEdit,
                            QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

class BICCAStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("<untitled draft> - BICCA Studio 1.0.0")
        self.setGeometry(100, 100, 950, 650)
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
        
        # Add status bar with Data button
        self.create_status_bar()
        
        # Initially hide dropdown menus
        self.file_menu_widget.hide()
        self.help_menu_widget.hide()
        
        # Update tutorial content to first page
        self.update_tutorial_content()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
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
        
        # Custom styled menu bar items
        file_action = QAction("File", self)
        file_action.setFont(QFont("Arial", 10, QFont.Bold))
        file_action.triggered.connect(self.toggle_file_menu)
        menubar.addAction(file_action)
        
        home_action = QAction("Home", self)
        home_action.setFont(QFont("Arial", 10, QFont.Bold))
        menubar.addAction(home_action)
        
        reports_action = QAction("Reports", self)
        reports_action.setFont(QFont("Arial", 10, QFont.Bold))
        menubar.addAction(reports_action)
        
        help_action = QAction("Help", self)
        help_action.setFont(QFont("Arial", 10, QFont.Bold))
        help_action.triggered.connect(self.toggle_help_menu)
        menubar.addAction(help_action)
        
        # Create File dropdown menu widget
        self.file_menu_widget = QWidget(self)
        self.file_menu_widget.setGeometry(68, 58, 330, 500)  # Position under File menu
        self.file_menu_widget.setStyleSheet("background-color: white; border: 1px solid #cccccc;")
        file_menu_layout = QVBoxLayout(self.file_menu_widget)
        file_menu_layout.setContentsMargins(0, 0, 0, 0)
        file_menu_layout.setSpacing(0)
        
        # File menu options based on Image 1
        file_options = [
            ("New", "⊕"),
            ("Open", "📁"),
            ("Save", "💾"),
            ("Save As...", "📄"),
            ("Create a copy", "📑"),
            ("Print", "🖨️"),
            ("Rename", "📝"),
            ("Export", "📤"),
            ("Version History", "🔄"),
            ("Info", "ℹ️")
        ]
        
        for option_text, icon_text in file_options:
            option_widget = QWidget()
            option_layout = QHBoxLayout(option_widget)
            option_layout.setContentsMargins(20, 10, 10, 10)
            
            icon_label = QLabel(icon_text)
            icon_label.setFixedWidth(30)
            option_layout.addWidget(icon_label)
            
            label = QLabel(option_text)
            label.setFont(QFont("Arial", 10))
            option_layout.addWidget(label)
            
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #e0e0e0;")
            
            file_menu_layout.addWidget(option_widget)
            
            # Add separator except after the last item
            if option_text != "Info":
                file_menu_layout.addWidget(separator)
        
        # Create Help dropdown menu widget
        self.help_menu_widget = QWidget(self)
        self.help_menu_widget.setGeometry(718, 58, 330, 200)  # Position under Help menu
        self.help_menu_widget.setStyleSheet("background-color: white; border: 1px solid #cccccc;")
        help_menu_layout = QVBoxLayout(self.help_menu_widget)
        help_menu_layout.setContentsMargins(0, 0, 0, 0)
        help_menu_layout.setSpacing(0)
        
        # Help menu options based on Image 2
        help_options = [
            ("Contact us", "📧"),
            ("Feedback", "💬"),
            ("Video Tutorials", "🎦"),
            ("Join our Community", "👥")
        ]
        
        for option_text, icon_text in help_options:
            option_widget = QWidget()
            option_layout = QHBoxLayout(option_widget)
            option_layout.setContentsMargins(20, 10, 10, 10)
            
            icon_label = QLabel(icon_text)
            icon_label.setFixedWidth(30)
            option_layout.addWidget(icon_label)
            
            label = QLabel(option_text)
            label.setFont(QFont("Arial", 10))
            option_layout.addWidget(label)
            
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #e0e0e0;")
            
            help_menu_layout.addWidget(option_widget)
            
            # Add separator except after the last item
            if option_text != "Join our Community":
                help_menu_layout.addWidget(separator)
    
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
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        
        # Add buttons to toolbar
        doc_btn = QAction(QIcon(), "", self)
        folder_btn = QAction(QIcon(), "", self)
        print_btn = QAction(QIcon(), "", self)
        
        # Use small colored squares as placeholders for icons
        doc_btn_widget = QWidget()
        doc_btn_layout = QVBoxLayout(doc_btn_widget)
        doc_btn_layout.setContentsMargins(5, 5, 5, 5)
        doc_icon = QLabel()
        doc_icon.setFixedSize(20, 20)
        doc_icon.setStyleSheet("background-color: #EEEEEE; border: 1px solid #CCCCCC;")
        doc_btn_layout.addWidget(doc_icon)
        
        folder_btn_widget = QWidget()
        folder_btn_layout = QVBoxLayout(folder_btn_widget)
        folder_btn_layout.setContentsMargins(5, 5, 5, 5)
        folder_icon = QLabel()
        folder_icon.setFixedSize(20, 20)
        folder_icon.setStyleSheet("background-color: #3A75C4; border: 1px solid #2A65B4;")
        folder_btn_layout.addWidget(folder_icon)
        
        print_btn_widget = QWidget()
        print_btn_layout = QVBoxLayout(print_btn_widget)
        print_btn_layout.setContentsMargins(5, 5, 5, 5)
        print_icon = QLabel()
        print_icon.setFixedSize(20, 20)
        print_icon.setStyleSheet("background-color: #DDDDDD; border: 1px solid #AAAAAA;")
        print_btn_layout.addWidget(print_icon)
        
        toolbar.addWidget(doc_btn_widget)
        toolbar.addWidget(folder_btn_widget)
        toolbar.addWidget(print_btn_widget)
        
        self.addToolBar(toolbar)
    
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
        
        # Right spacer to push content to center
        container_layout.addStretch(1)
        
        window_tabs_container.setFixedHeight(40)
        self.main_layout.addWidget(window_tabs_container)
    
    def create_content_area(self):
        content_widget = QSplitter(Qt.Horizontal)
        
        # Left side - Tutorials panel
        tutorials_panel = QWidget()
        tutorials_layout = QVBoxLayout(tutorials_panel)
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
        project_panel = QWidget()
        project_layout = QVBoxLayout(project_panel)
        project_layout.setContentsMargins(0, 0, 0, 0)
        
        # Project header
        project_header = QWidget()
        project_header.setStyleSheet("background-color: #f0f0f0;")
        project_header_layout = QHBoxLayout(project_header)
        project_header_layout.setContentsMargins(5, 5, 5, 5)
        
        project_label = QLabel("Project Details Window")
        project_close_btn = QPushButton("×")
        project_close_btn.setFixedSize(20, 20)
        project_close_btn.setStyleSheet("border: none;")
        project_close_btn.clicked.connect(self.close_project_details)
        
        project_header_layout.addWidget(project_label)
        project_header_layout.addStretch()
        project_header_layout.addWidget(project_close_btn)
        
        # Create collapsible sections
        project_content = QWidget()
        project_content_layout = QVBoxLayout(project_content)
        project_content_layout.setContentsMargins(10, 10, 10, 10)
        
        # General Information section (expanded with form fields)
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
        
        general_info_header = QLabel("▼ General Information")  # Down arrow for expanded section
        general_info_header.setStyleSheet("font-weight: bold;")
        general_info_layout.addWidget(general_info_header)
        
        # Form fields for General Information as shown in the image
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # Company Name field
        company_layout = QHBoxLayout()
        company_label = QLabel("Company Name")
        company_label.setFixedWidth(150)
        company_edit = QLineEdit()
        company_layout.addWidget(company_label)
        company_layout.addWidget(company_edit)
        
        # Project Title field
        title_layout = QHBoxLayout()
        title_label = QLabel("Project Title")
        title_label.setFixedWidth(150)
        title_edit = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_edit)
        
        # Project Description field
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Project Description")
        desc_label.setFixedWidth(150)
        desc_edit = QLineEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(desc_edit)
        
        # Name of Valuer field with dropdown
        valuer_layout = QHBoxLayout()
        valuer_label = QLabel("Name of Valuer")
        valuer_label.setFixedWidth(150)
        valuer_combo = QComboBox()
        valuer_combo.addItem("India")
        valuer_layout.addWidget(valuer_label)
        valuer_layout.addWidget(valuer_combo)
        
        # Job Number field
        job_layout = QHBoxLayout()
        job_label = QLabel("Job Number")
        job_label.setFixedWidth(150)
        job_edit = QLineEdit()
        job_layout.addWidget(job_label)
        job_layout.addWidget(job_edit)
        
        # Client field
        client_layout = QHBoxLayout()
        client_label = QLabel("Client")
        client_label.setFixedWidth(150)
        client_edit = QLineEdit()
        client_layout.addWidget(client_label)
        client_layout.addWidget(client_edit)
        
        # Country field
        country_layout = QHBoxLayout()
        country_label = QLabel("Country")
        country_label.setFixedWidth(150)
        country_edit = QLineEdit()
        country_layout.addWidget(country_label)
        country_layout.addWidget(country_edit)
        
        # Base Year field
        year_layout = QHBoxLayout()
        year_label = QLabel("Base Year")
        year_label.setFixedWidth(150)
        year_edit = QLineEdit()
        year_layout.addWidget(year_label)
        year_layout.addWidget(year_edit)
        
        # Add all form fields to the layout
        form_layout.addLayout(company_layout)
        form_layout.addLayout(title_layout)
        form_layout.addLayout(desc_layout)
        form_layout.addLayout(valuer_layout)
        form_layout.addLayout(job_layout)
        form_layout.addLayout(client_layout)
        form_layout.addLayout(country_layout)
        form_layout.addLayout(year_layout)
        
        general_info_layout.addLayout(form_layout)
        
        # Input Parameters section (collapsed)
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
        
        input_params_header = QLabel("► Input Parameters")  # Right arrow for collapsed section
        input_params_header.setStyleSheet("font-weight: bold;")
        input_params_layout.addWidget(input_params_header)
        
        # Outputs section (collapsed)
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
        
        outputs_header = QLabel("► Outputs")  # Right arrow for collapsed section
        outputs_header.setStyleSheet("font-weight: bold;")
        outputs_layout.addWidget(outputs_header)
        
        # Add all sections to the project content
        project_content_layout.addWidget(general_info_box)
        project_content_layout.addWidget(input_params_box)
        project_content_layout.addWidget(outputs_box)
        
        project_layout.addWidget(project_header)
        project_layout.addWidget(project_content)
        project_layout.addStretch()
        
        # Add both panels to the splitter
        content_widget.addWidget(tutorials_panel)
        content_widget.addWidget(project_panel)
        
        # Set relative sizes: tutorial panel smaller than project panel
        content_widget.setSizes([200, 750])
        
        self.main_layout.addWidget(content_widget)
    
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BICCAStudio()
    window.show()
    sys.exit(app.exec_())