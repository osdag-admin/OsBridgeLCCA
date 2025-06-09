import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTreeWidget, QTreeWidgetItem, QTabWidget, 
                            QFrame, QSplitter, QToolBar, QAction, QMenu, QMenuBar)
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF

class DonutChart(QWidget):
    def __init__(self, title, subtitle, values, colors, labels, parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.values = values  # List of percentage values
        self.colors = colors  # List of colors for each segment
        self.labels = labels  # List of labels for the legend
        self.setMinimumSize(180, 180)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw title and subtitle
        titleFont = QFont("Arial", 8)
        titleFont.setBold(True)
        painter.setFont(titleFont)
        painter.drawText(int(10), int(15), self.title)
        
        subtitleFont = QFont("Arial", 7)
        painter.setFont(subtitleFont)
        painter.drawText(int(10), int(30), self.subtitle)
        
        # Draw donut chart
        rect = QRectF(10, 40, self.width()-20, self.height()-60)
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2
        
        # Draw pie segments
        startAngle = 0
        for i, value in enumerate(self.values):
            spanAngle = value * 3.6  # Convert percentage to degrees (percentage * 360 / 100)
            
            painter.setPen(QPen(QColor(self.colors[i]), 1))
            painter.setBrush(QBrush(QColor(self.colors[i])))
            
            # Create a path for the donut segment
            path = QPainterPath()
            path.moveTo(center)
            path.arcTo(rect, startAngle, spanAngle)
            painter.drawPath(path)
            
            startAngle += spanAngle

        # Draw inner circle to create donut hole
        painter.setPen(QPen(Qt.white))
        painter.setBrush(QBrush(Qt.white))
        inner_rect = QRectF(center.x() - radius * 0.6, center.y() - radius * 0.6, radius * 1.2, radius * 1.2)
        painter.drawEllipse(inner_rect)

class PieChart(QWidget):
    def __init__(self, title, data, parent=None):
        super().__init__(parent)
        self.title = title
        self.data = data  # List of tuples (label, value, color, percentage)
        self.setMinimumSize(400, 250)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw title
        titleFont = QFont("Arial", 8)
        titleFont.setBold(True)
        painter.setFont(titleFont)
        painter.drawText(int(10), int(15), self.title)
        
        # Draw pie chart
        rect = QRectF(10, 25, self.width()/2 - 20, self.height() - 40)
        
        startAngle = 0
        for label, value, color, percentage in self.data:
            spanAngle = percentage * 3.6  # Convert to degrees
            
            painter.setPen(QPen(QColor(color), 1))
            painter.setBrush(QBrush(QColor(color)))
            painter.drawPie(rect, int(startAngle * 16), int(spanAngle * 16))  # Qt uses 16ths of a degree
            
            startAngle += spanAngle
        
        # Draw legend items on the right side
        legendX = self.width()/2 + 10
        legendY = 30
        
        for label, value, color, percentage in self.data:
            # Draw color square
            colorRect = QRectF(legendX, legendY, 10, 10)
            painter.setPen(QPen(QColor(color), 1))
            painter.setBrush(QBrush(QColor(color)))
            painter.drawRect(colorRect)
            
            # Draw label and percentage
            textFont = QFont("Arial", 7)
            painter.setFont(textFont)
            text = f"{label}: {percentage}%"
            painter.drawText(int(legendX + 15), int(legendY + 9), text)
            
            # Draw value in parentheses
            if value:
                valueText = f"({value} LaBRs)"
                painter.drawText(int(legendX + 15), int(legendY + 22), valueText)
            
            legendY += 30

class BCCStudioUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window title and size
        self.setWindowTitle("<untitled-draft> - BLCCA Studio 1.0.0")
        self.resize(900, 700)
        
        # Create menu bar with green background like in the reference image
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #4a9948; color: white;")
        
        fileMenu = menubar.addMenu('File')
        homeMenu = menubar.addMenu('Home')
        reportsMenu = menubar.addMenu('Reports')
        helpMenu = menubar.addMenu('Help')
        
        # Create toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #f9f9f9;")
        self.addToolBar(toolbar)
        
        # Add toolbar buttons (file operations)
        newAction = QAction(QIcon(), "", self)
        openAction = QAction(QIcon(), "", self)
        saveAction = QAction(QIcon(), "", self)
        
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        
        # Create tab bar
        tabBar = QWidget()
        tabBarLayout = QHBoxLayout(tabBar)
        tabBarLayout.setContentsMargins(0, 2, 0, 2)
        tabBarLayout.setSpacing(2)
        
        # Add stretch at the beginning to center the tabs
        tabBarLayout.addStretch()
        
        tabs = ["Windows", "Tutorials", "Project Details", "Results", "Compare"]
        
        for tab in tabs:
            tabButton = QPushButton(tab)
            tabButton.setStyleSheet("background-color: #e0e0e0; border: 1px solid #ccc; border-bottom: none; padding: 5px 10px; border-radius: 3px 3px 0 0;")
            tabBarLayout.addWidget(tabButton)
        
        # Add stretch at the end to center the tabs
        tabBarLayout.addStretch()
        
        # Create main content area
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        
        mainLayout.addWidget(tabBar)
        
        # Create content area with windows (not using splitter to better match reference)
        contentArea = QWidget()
        contentLayout = QHBoxLayout(contentArea)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(5)
        
        # Create left panel (Project Details Window)
        leftPanel = QWidget()
        leftPanel.setFixedWidth(180)  # Fixed width to match reference
        leftPanel.setStyleSheet("background-color: #f0e6e6;")  # Light pink background to match reference
        leftPanelLayout = QVBoxLayout(leftPanel)
        leftPanelLayout.setContentsMargins(5, 5, 5, 5)
        
        # Project Details Header
        projectDetailsHeader = QWidget()
        projectHeaderLayout = QHBoxLayout(projectDetailsHeader)
        projectHeaderLayout.setContentsMargins(0, 0, 0, 0)
        
        projectTitle = QLabel("Project Details Window")
        projectTitle.setStyleSheet("font-size: 10px;")
        closeBtn = QPushButton("×")
        closeBtn.setFixedSize(15, 15)
        closeBtn.setStyleSheet("background-color: transparent; border: none;")
        
        projectHeaderLayout.addWidget(projectTitle)
        projectHeaderLayout.addWidget(closeBtn)
        
        leftPanelLayout.addWidget(projectDetailsHeader)
        
        # Project tree view
        treeWidget = QTreeWidget()
        treeWidget.setHeaderHidden(True)
        treeWidget.setStyleSheet("background-color: transparent; border: none;")
        
        # Input Parameters section
        inputParams = QTreeWidgetItem(treeWidget, ["Input Parameters"])
        inputParams.setExpanded(True)
        
        # Add items with icons
        structureWorks = QTreeWidgetItem(inputParams, ["Structure Works Data"])
        financialData = QTreeWidgetItem(inputParams, ["Financial Data"])
        carbonData = QTreeWidgetItem(inputParams, ["Carbon Emission Data"])
        bridgeData = QTreeWidgetItem(inputParams, ["Bridge and Traffic Data"])
        maintenanceData = QTreeWidgetItem(inputParams, ["Maintenance and Repair"])
        demolitionData = QTreeWidgetItem(inputParams, ["Demolition and Recycling"])
        
        # Output section
        outputSection = QTreeWidgetItem(treeWidget, ["Output"])
        outputSection.setExpanded(True)
        
        # Output items with colored icons (using stylesheet)
        initialCost = QTreeWidgetItem(outputSection, ["Initial Construction Cost"])
        initialCarbonCost = QTreeWidgetItem(outputSection, ["Initial Carbon Emission Cost"])
        timeCost = QTreeWidgetItem(outputSection, ["Time Cost"])
        userDelayItem = QTreeWidgetItem(outputSection, ["User Delay Cost"])
        carbonEmissionItem = QTreeWidgetItem(outputSection, ["Carbon Emission due to Re-Routing"])
        periodicItem = QTreeWidgetItem(outputSection, ["Periodic Maintenance Costs"])
        maintenanceEmissionItem = QTreeWidgetItem(outputSection, ["Maintenance Emission Costs"])
        routineItem = QTreeWidgetItem(outputSection, ["Routine Inspection Costs"])
        repairItem = QTreeWidgetItem(outputSection, ["Repair & Rehabilitation Costs"])
        reconstructionItem = QTreeWidgetItem(outputSection, ["Reconstruction Costs"])
        demolitonItem = QTreeWidgetItem(outputSection, ["Demolition & Disposal Cost"])
        recyclingItem = QTreeWidgetItem(outputSection, ["Recycling Credit"])
        totalItem = QTreeWidgetItem(outputSection, ["Total Life-Cycle Cost"])
        
        # Style the tree items to match reference (add colored squares to the left)
        for item in [initialCost, initialCarbonCost, timeCost, userDelayItem, carbonEmissionItem, 
                    periodicItem, maintenanceEmissionItem, routineItem, repairItem,
                    reconstructionItem, demolitonItem, recyclingItem, totalItem]:
            item.setForeground(0, QColor("#009900"))  # Green text to match reference
        
        treeWidget.expandAll()
        leftPanelLayout.addWidget(treeWidget)
        
        # Create right content area with windows
        rightContent = QWidget()
        rightLayout = QVBoxLayout(rightContent)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        
        # Create tabbed windows area
        tabbedWindows = QWidget()
        tabbedWindowsLayout = QHBoxLayout(tabbedWindows)
        tabbedWindowsLayout.setContentsMargins(0, 0, 0, 0)
        tabbedWindowsLayout.setSpacing(0)
        
        # Data Window tab
        dataWindowTab = QWidget()
        dataWindowTab.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        dataWindowTabLayout = QHBoxLayout(dataWindowTab)
        dataWindowTabLayout.setContentsMargins(5, 5, 5, 5)
        dataWindowTabLayout.setSpacing(0)
        
        dataTabLabel = QLabel("Data Window")
        dataTabLabel.setStyleSheet("font-size: 10px;")
        dataTabClose = QPushButton("×")
        dataTabClose.setFixedSize(15, 15)
        dataTabClose.setStyleSheet("background-color: transparent; border: none;")
        
        dataWindowTabLayout.addWidget(dataTabLabel)
        dataWindowTabLayout.addStretch()
        dataWindowTabLayout.addWidget(dataTabClose)
        
        # Results Window tab
        resultsWindowTab = QWidget()
        resultsWindowTab.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        resultsWindowTabLayout = QHBoxLayout(resultsWindowTab)
        resultsWindowTabLayout.setContentsMargins(5, 5, 5, 5)
        resultsWindowTabLayout.setSpacing(0)
        
        resultsTabLabel = QLabel("Results Window")
        resultsTabLabel.setStyleSheet("font-size: 10px;")
        resultsTabClose = QPushButton("×")
        resultsTabClose.setFixedSize(15, 15)
        resultsTabClose.setStyleSheet("background-color: transparent; border: none;")
        
        resultsWindowTabLayout.addWidget(resultsTabLabel)
        resultsWindowTabLayout.addStretch()
        resultsWindowTabLayout.addWidget(resultsTabClose)
        
        # Each tab should be relatively narrow like in the reference image
        dataWindowTab.setFixedWidth(140)
        resultsWindowTab.setFixedWidth(140)
        
        tabbedWindowsLayout.addWidget(dataWindowTab)
        tabbedWindowsLayout.addWidget(resultsWindowTab)
        tabbedWindowsLayout.addStretch()
        
        # Windows content
        windowsContent = QWidget()
        windowsLayout = QVBoxLayout(windowsContent)
        windowsLayout.setContentsMargins(0, 0, 0, 0)
        windowsLayout.setSpacing(5)  # Reduce spacing between items
        
        # Data window content
        dataWindow = QWidget()
        dataWindow.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")
        dataWindowLayout = QVBoxLayout(dataWindow)
        dataWindowLayout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Create donut chart container
        chartContainer = QWidget()
        chartLayout = QHBoxLayout(chartContainer)
        chartLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        chartLayout.setSpacing(5)  # Reduce spacing
        
        # Create three donut charts
        economicChart = DonutChart(
            "Economic cost distribution across various stages for lifetime of 50 years",
            "Initial Stage Economic Cost: 28.4%, 84.15 LaBRs",
            [28.4, 45.6, 26.0],
            ["#1a3c5a", "#4d79a4", "#a67d3b"],
            ["Initial Stage", "Mid Stage", "End-of-Life Stage"]
        )
        
        socialChart = DonutChart(
            "Social cost distribution across stages for PCC bridges for 50 years",
            "Initial Stage Social Cost: 54.32%",
            [54.32, 45.68, 0, 0],
            ["#1a3c5a", "#4d79a4", "#a67d3b", "#d0b981"],
            ["Initial Stage", "Mid Stage", "End-of-Life Stage", "Beyond-Life Stage"]
        )
        
        environmentalChart = DonutChart(
            "Environmental cost distribution across stages for PCC bridges for 50 years",
            "Initial Stage Environmental Cost: 18.88%",
            [18.88, 74.85, 6.28, 0],
            ["#1a3c5a", "#196d4a", "#a67d3b", "#d0b981"],
            ["Initial Stage", "Mid Stage", "End-of-Life Stage", "Beyond-Life Stage"]
        )
        
        chartLayout.addWidget(economicChart)
        chartLayout.addWidget(socialChart)
        chartLayout.addWidget(environmentalChart)
        
        dataWindowLayout.addWidget(chartContainer)
        
        # Legend for charts
        legendWidget = QWidget()
        legendLayout = QHBoxLayout(legendWidget)
        
        legendItems = [
            ("Initial Stage", "#1a3c5a"),
            ("Mid Stage", "#4d79a4"),
            ("End-of-Life Stage", "#a67d3b"),
            ("Beyond-Life Stage", "#d0b981")
        ]
        
        for text, color in legendItems:
            legendItemWidget = QWidget()
            legendItemLayout = QHBoxLayout(legendItemWidget)
            
            colorBox = QLabel()
            colorBox.setFixedSize(15, 15)
            colorBox.setStyleSheet(f"background-color: {color};")
            
            textLabel = QLabel(text)
            textLabel.setStyleSheet("font-size: 10px;")
            
            legendItemLayout.addWidget(colorBox)
            legendItemLayout.addWidget(textLabel)
            
            legendLayout.addWidget(legendItemWidget)
        
        dataWindowLayout.addWidget(legendWidget)
        
        # Results window
        resultsWindow = QWidget()
        resultsWindow.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")
        resultsWindowLayout = QVBoxLayout(resultsWindow)
        resultsWindowLayout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Life-Cycle Costs pie chart
        pieChartData = [
            ("Initial Construction Cost", "81.93", "#e67300", 23.7),
            ("Initial Carbon Emission Cost", "9.87", "#7d33a3", 3.3),
            ("User Delay Cost", "139.93", "#f39c12", 45.6),
            ("Carbon Emission due to Re-Routing", "19.69", "#34495e", 11.5),
            ("Periodic Maintenance Costs", "1.44", "#16a085", 0.4),
            ("Maintenance Emission Cost", "10.86", "#2980b9", 6.4),
            ("Routine Inspection Cost", "1.91", "#8e44ad", 3.5),
            ("Repair & Rehabilitation Cost", "2.93", "#2c3e50", 0.85),
            ("Demolition & Disposal Cost", "0.71", "#bdc3c7", 0.3)
        ]
        
        lifeCyclePieChart = PieChart("Life-Cycle Costs for 50 years", pieChartData)
        resultsWindowLayout.addWidget(lifeCyclePieChart)
        
        # Stack data and results windows - 
        dataWindow.setMaximumHeight(1000)  # Adjust height to match reference
        resultsWindow.setMaximumHeight(500)  # Adjust height to match reference
        
        # Stack data and results windows
        windowsLayout.addWidget(dataWindow)
        windowsLayout.addWidget(resultsWindow)
        
        # Add tab header and content to main right layout
        rightLayout.addWidget(tabbedWindows)
        rightLayout.addWidget(windowsContent)
        
        # Add buttons at bottom
        buttonRow = QWidget()
        buttonRowLayout = QHBoxLayout(buttonRow)
        buttonRowLayout.setContentsMargins(0, 10, 0, 0)
        
        buttonRowLayout.addStretch()
        backButton = QPushButton("Back")
        backButton.setStyleSheet("padding: 5px 15px;")
        nextButton = QPushButton("Next")
        nextButton.setStyleSheet("padding: 5px 15px;")
        buttonRowLayout.addWidget(backButton)
        buttonRowLayout.addWidget(nextButton)
        
        rightLayout.addWidget(buttonRow)
        
        # Add panels to content area
        contentLayout.addWidget(leftPanel)
        contentLayout.addWidget(rightContent)
        
        mainLayout.addWidget(contentArea)
        
        # Show the UI
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set global styles
    app.setStyle("Fusion")
    
    # Set green header and other global styles
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f4f4f4;
        }
        QMenuBar {
            background-color: #4a9948;
            color: white;
        }
        QToolBar {
            border-bottom: 1px solid #ddd;
        }
        QSplitter::handle {
            background-color: #cccccc;
        }
    """)
    
    ex = BCCStudioUI()
    sys.exit(app.exec_())