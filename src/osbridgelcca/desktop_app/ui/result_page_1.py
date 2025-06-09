import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QSplitter, QFrame, QSizePolicy, QAction, QToolBar, QStackedWidget,
    QDockWidget, QScrollArea, QMenu, QLineEdit, QGroupBox
)
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap


class CloseableTabWidget(QTabWidget):
    """Custom tab widget with closeable tabs"""
    
    def __init__(self, parent=None):
        super(CloseableTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.setDocumentMode(True)
        self.setMovable(True)
        
    def closeTab(self, index):
        """Close the tab at the given index"""
        # Don't actually remove tabs in this demo
        print(f"Close tab requested for tab index {index}")


class TreePanel(QWidget):
    """Project details tree panel implementation"""
    
    def __init__(self, parent=None):
        super(TreePanel, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header
        header = QFrame()
        header.setFrameShape(QFrame.StyledPanel)
        # Updated header background color to match the image (light brown/beige)
        header.setStyleSheet("background-color: #F5EFE6;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        title_label = QLabel("Project Details Window")
        title_label.setStyleSheet("color: #333333; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: #555555;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #000000;
            }
        """)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # Create tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: none;
                background-color: #F5EFE0;  /* Beige background to match image */
            }
            QTreeWidget::item {
                height: 24px;
            }
            QTreeWidget::item:selected {
                background-color: #E6F2E6;
                color: #000000;
            }
            QTreeWidget::item:has-children {
                font-weight: bold;
                color: #333333;
            }
        """)
        
        # Input Parameters section
        input_params = QTreeWidgetItem(["Input Parameters"])
        input_params.setIcon(0, QIcon.fromTheme("folder", self.getDefaultIcon()))
        input_params.setBackground(0, QColor("#F5EFE0"))  # Set background for Input Parameters
        input_params.setForeground(0, QColor("#333333"))  # Dark text color
        self.tree.addTopLevelItem(input_params)
        
        # Structure Works Data
        structure_works = QTreeWidgetItem(["Structure Works Data"])
        structure_works.setIcon(0, QIcon.fromTheme("folder", self.getDefaultIcon()))
        structure_works.setForeground(0, QColor("#333333"))  # Dark text color
        input_params.addChild(structure_works)
        
        structure_works.addChild(self.createItem("Financial Data"))
        structure_works.addChild(self.createItem("Carbon Emission Data"))
        structure_works.addChild(self.createItem("Bridge and Traffic Data"))
        structure_works.addChild(self.createItem("Maintenance and Repair"))
        structure_works.addChild(self.createItem("Demolition and Recycling"))
        
        # Direct children of Input Parameters
        input_params.addChild(self.createItem("Carbon Emission Data"))
        input_params.addChild(self.createItem("Bridge and Traffic Data"))
        input_params.addChild(self.createItem("Maintenance and Repair"))
        input_params.addChild(self.createItem("Demolition and Recycling"))
        
        # Output section
        output = QTreeWidgetItem(["Output"])
        output.setIcon(0, QIcon.fromTheme("folder", self.getDefaultIcon()))
        output.setBackground(0, QColor("#F5EFE0"))  # Set background for Output
        output.setForeground(0, QColor("#333333"))  # Dark text color
        self.tree.addTopLevelItem(output)
        
        # Output items
        output_items = [
            "Initial Construction Cost",
            "Initial Carbon Emission Cost",
            "Time Cost",
            "Traffic User Cost",
            "Carbon Emission due to Re-routing",
            "Periodic Maintenance Costs",
            "Maintenance Emission Costs",
            "Routine Inspection Costs",
            "Repair & Rehabilitation Costs",
            "Reconstruction Costs",
            "Demolition & Disposal Cost",
            "Recycling Cost",
            "Total Life-Cycle Cost"
        ]
        
        for item_text in output_items:
            item = self.createItem(item_text, is_document=True)
            output.addChild(item)
        
        # Expand input params by default
        input_params.setExpanded(True)
        structure_works.setExpanded(True)
        output.setExpanded(True)
        
        layout.addWidget(self.tree)
        
    def createItem(self, text, is_document=False):
        """Create a tree item with the appropriate icon"""
        item = QTreeWidgetItem([text])
        if is_document:
            # Document icon for output items
            item.setIcon(0, QIcon.fromTheme("text-x-generic", self.getDocumentIcon()))
        else:
            # Default folder icon
            item.setIcon(0, QIcon.fromTheme("folder", self.getDefaultIcon()))
        return item
    
    def getDefaultIcon(self):
        """Return a default folder icon"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(0, 0, 0, 0))
        return QIcon(pixmap)
    
    def getDocumentIcon(self):
        """Return a default document icon"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(0, 0, 0, 0))
        return QIcon(pixmap)


class DataWindowPanel(QWidget):
    """Data Window Panel Implementation"""
    
    def __init__(self, parent=None):
        super(DataWindowPanel, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Placeholder for chart area - upper section
        chart_placeholder = QWidget()
        chart_placeholder.setMinimumHeight(300)
        chart_placeholder.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CCCCCC;")
        
        placeholder_text = QLabel("Life-Cycle Costs for 50 years\n\nVisualization area for donut charts")
        placeholder_text.setAlignment(Qt.AlignCenter)
        chart_layout = QVBoxLayout(chart_placeholder)
        chart_layout.addWidget(placeholder_text)
        
        layout.addWidget(chart_placeholder)
        
        # Create legend
        legend_frame = QFrame()
        legend_frame.setFrameShape(QFrame.StyledPanel)
        legend_frame.setMaximumHeight(50)
        legend_frame.setStyleSheet("background-color: #F5F5F5; border: 1px solid #DDDDDD;")
        
        legend_layout = QHBoxLayout(legend_frame)
        
        legend_items = [
            ("Initial Stage", "#000000"),
            ("Use Stage", "#006400"),
            ("End-of-Life Stage", "#8B4513"),
            ("Beyond-Life Stage", "#90EE90")
        ]
        
        for text, color in legend_items:
            color_box = QFrame()
            color_box.setFixedSize(16, 16)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            
            label = QLabel(text)
            
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.addWidget(color_box)
            item_layout.addWidget(label)
            
            legend_layout.addLayout(item_layout)
        
        legend_layout.addStretch()
        layout.addWidget(legend_frame)
        
        # Placeholder for horizontal bar chart - lower section
        barchart_placeholder = QWidget()
        barchart_placeholder.setMinimumHeight(300)
        barchart_placeholder.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CCCCCC;")
        
        barchart_text = QLabel("Horizontal bar chart area showing breakdown of life-cycle costs")
        barchart_text.setAlignment(Qt.AlignCenter)
        barchart_layout = QVBoxLayout(barchart_placeholder)
        barchart_layout.addWidget(barchart_text)
        
        layout.addWidget(barchart_placeholder)
        
        # Total cost display
        total_frame = QFrame()
        total_layout = QHBoxLayout(total_frame)
        total_layout.setContentsMargins(5, 5, 5, 5)
        
        total_layout.addStretch()
        
        total_label = QLabel("Total Life-Cycle Cost:")
        total_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        total_layout.addWidget(total_label)
        
        total_value = QLabel("259.15 Lakh")
        total_value.setStyleSheet("font-weight: bold; font-size: 12px;")
        total_layout.addWidget(total_value)
        
        layout.addWidget(total_frame)
        
        # Download and view options
        options_frame = QFrame()
        options_layout = QVBoxLayout(options_frame)
        
        download_layout = QHBoxLayout()
        download_layout.addWidget(QPushButton("Download as PNG"))
        download_layout.addWidget(QPushButton("Download as JPG"))
        download_layout.addWidget(QPushButton("Download as PDF"))
        options_layout.addLayout(download_layout)
        
        view_layout = QHBoxLayout()
        view_layout.addWidget(QPushButton("View as Pie Chart"))
        view_layout.addWidget(QPushButton("View as Table"))
        options_layout.addLayout(view_layout)
        
        layout.addWidget(options_frame)
        
        # Navigation buttons
        nav_frame = QFrame()
        nav_layout = QHBoxLayout(nav_frame)
        
        nav_layout.addStretch()
        
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Next")
        next_btn.setFixedWidth(100)
        nav_layout.addWidget(next_btn)
        
        layout.addWidget(nav_frame)


class ResultsWindowPanel(QWidget):
    """Results Window Panel Implementation"""
    
    def __init__(self, parent=None):
        super(ResultsWindowPanel, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tabbed widget for Economic, Social, Environmental costs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        
        # Economic cost tab
        economic_tab = QWidget()
        economic_layout = QVBoxLayout(economic_tab)
        
        cost_title = QLabel("Economic cost distribution across various stages for bridges for 50 years")
        cost_title.setAlignment(Qt.AlignCenter)
        economic_layout.addWidget(cost_title)
        
        chart_placeholder = QWidget()
        chart_placeholder.setMinimumHeight(300)
        chart_placeholder.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CCCCCC;")
        
        chart_text = QLabel("Economic cost distribution donut chart")
        chart_text.setAlignment(Qt.AlignCenter)
        chart_layout = QVBoxLayout(chart_placeholder)
        chart_layout.addWidget(chart_text)
        
        economic_layout.addWidget(chart_placeholder)
        
        # Download options
        dl_layout = QHBoxLayout()
        dl_layout.addWidget(QPushButton("Download as PNG"))
        dl_layout.addWidget(QPushButton("Download as JPG"))
        dl_layout.addWidget(QPushButton("Download as PDF"))
        economic_layout.addLayout(dl_layout)
        
        # View options
        view_layout = QHBoxLayout()
        view_layout.addWidget(QPushButton("View as Pie Chart"))
        view_layout.addWidget(QPushButton("View as Table"))
        economic_layout.addLayout(view_layout)
        
        tabs.addTab(economic_tab, "Economic Cost")
        
        # Social cost tab
        social_tab = QWidget()
        social_layout = QVBoxLayout(social_tab)
        social_layout.addWidget(QLabel("Social cost distribution across stages for PSC bridges for 50 years"))
        social_layout.addWidget(QWidget())  # Placeholder for chart
        tabs.addTab(social_tab, "Social Cost")
        
        # Environmental cost tab
        env_tab = QWidget()
        env_layout = QVBoxLayout(env_tab)
        env_layout.addWidget(QLabel("Environmental cost distribution across stages for PSC bridges for 50 years"))
        env_layout.addWidget(QWidget())  # Placeholder for chart
        tabs.addTab(env_tab, "Environmental Cost")
        
        layout.addWidget(tabs)


class BLCCAStudio(QMainWindow):
    """Main BLCCA Studio application window"""
    
    def __init__(self):
        super(BLCCAStudio, self).__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle("BLCCA Studio 1.0.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.createMenuBar()
        
        # Create toolbar
        self.createToolBar()
        
        # Create tab bar for main navigation
        self.createTopTabBar()
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Project Details
        project_panel = TreePanel()
        project_panel.setMinimumWidth(250)
        project_panel.setMaximumWidth(400)
        # Add styling to match the left panel color
        project_panel.setStyleSheet("background-color: #F5EFE0;")
        splitter.addWidget(project_panel)
        
        # Right side panel container
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Create tab widget for Data Window and Results Window
        right_tabs = CloseableTabWidget()
        
        # Data Window tab
        data_tab = QScrollArea()
        data_tab.setWidgetResizable(True)
        data_tab.setWidget(DataWindowPanel())
        right_tabs.addTab(data_tab, "Data Window")
        
        # Results Window tab
        results_tab = QScrollArea()
        results_tab.setWidgetResizable(True)
        results_tab.setWidget(ResultsWindowPanel())
        right_tabs.addTab(results_tab, "Results Window")
        
        right_layout.addWidget(right_tabs)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes - left panel gets 1/4, right gets 3/4
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QTabWidget::pane {
                border: 1px solid #C0C0C0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                border: 1px solid #C0C0C0;
                border-bottom: none;
                min-width: 8ex;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
            QPushButton {
                background-color: #F0F0F0;
                border: 1px solid #C0C0C0;
                border-radius: 3px;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QSplitter::handle {
                background-color: #C0C0C0;
            }
            QTreeWidget {
                border: none;
            }
        """)
    
    def createMenuBar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.createAction('New', 'Create a new project'))
        fileMenu.addAction(self.createAction('Open', 'Open an existing project'))
        fileMenu.addAction(self.createAction('Save', 'Save the current project'))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAction('Exit', 'Exit the application'))
        
        # Home menu
        homeMenu = menubar.addMenu('Home')
        
        # Reports menu
        reportsMenu = menubar.addMenu('Reports')
        
        # Help menu
        helpMenu = menubar.addMenu('Help')
    
    def createToolBar(self):
        """Create the application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        
        # Add blank placeholder icons for demonstration
        homeAction = self.createAction('', 'Home')
        fileAction = self.createAction('', 'Files')
        docAction = self.createAction('', 'Documents')
        
        toolbar.addAction(homeAction)
        toolbar.addAction(fileAction)
        toolbar.addAction(docAction)
        
        self.addToolBar(toolbar)
    
    def createTopTabBar(self):
        """Create the top tab bar for main navigation"""
        tabBar = QTabWidget()
        tabBar.setDocumentMode(True)
        tabBar.setTabPosition(QTabWidget.North)
        
        # Create more centered navigation tabs with proper styling
        tabBar.setStyleSheet("""
            QTabBar {
                alignment: center;
            }
            QTabBar::tab {
                padding: 4px 16px;
                margin: 0;
                background-color: #F0F0F0;
                border: 1px solid #D0D0D0;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
        """)
        
        # Create the tabs
        tabBar.addTab(QWidget(), "Windows")
        tabBar.addTab(QWidget(), "Tutorials")
        tabBar.addTab(QWidget(), "Project Details")
        tabBar.addTab(QWidget(), "Results")
        tabBar.addTab(QWidget(), "Compare")
        
        # Add tab bar below the toolbar with centered alignment
        tabBarContainer = QWidget()
        layout = QHBoxLayout(tabBarContainer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)  # Center the tab widget in the container
        layout.addWidget(tabBar)
        
        # Create a dock widget to hold the tab bar
        dock = QDockWidget("", self)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setWidget(tabBarContainer)
        dock.setTitleBarWidget(QWidget())  # Hide the title bar
        
        self.addDockWidget(Qt.TopDockWidgetArea, dock)
    
    def createAction(self, text, statusTip):
        """Create a QAction with the given text and status tip"""
        action = QAction(text, self)
        action.setStatusTip(statusTip)
        return action


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BLCCAStudio()
    window.show()
    sys.exit(app.exec_())