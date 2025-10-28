from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, 
                               QLabel, QMessageBox)
from PySide6.QtCore import Qt, Signal
import os

class CustomTabWidget(QWidget):
    """Combined widget that contains both tab bar and tab functionality"""
    tab_close_requested = Signal(int)
    
    def __init__(self, parent):
        super().__init__(None)
        self.parent = parent
        self.tab_counter = 0
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        
        # Connect signals
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tab_widget)
    
    def apply_styles(self):
        """Apply custom styles to the widget"""        
        # Build absolute path for close button image
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            close_img_path = os.path.join(base_dir, "..", "resources", "close.png")
            close_img_path = os.path.normpath(close_img_path)
            close_img_url = close_img_path.replace("\\", "/")  # for Windows compatibility
        except:
            close_img_url = ""  # Fallback if image not found

        style = f"""
            CustomTabWidget {{
                background-color: transparent;
            }}
            QTabWidget::pane {{
                border: none;
                background-color: transparent;
            }}
            QTabBar::tab {{
                background-color: #FDEFEF;
                border-top: 1px solid #E0E0E0;
                border-left: 1px solid #E0E0E0;
                border-right: 1px solid #E0E0E0;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
                min-width: 80px;
            }}
            QTabBar::tab:selected {{
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                color: #000000;
            }}
            QTabBar::tab:hover {{
                background-color: #F0E6E6;
                border-color: #808080;
            }}
            QTabBar::tab:selected:hover {{
                background-color: #F0E6E6;
                border-color: #808080;
            }}
            QTabBar::tab:pressed {{
                background-color: #FFF3F3;
                border-color: #606060;
            }}
            QTabBar::tab:selected:pressed {{
                background-color: #FFF3F3;
                border-color: #606060;
            }}
            QTabBar::close-button {{
                subcontrol-position: right;
                width: 13px;
                height: 13px;
                margin-right: 6px;
                border: 1px solid #ff5252;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }}
            QTabBar::close-button:hover {{
                border-color: #f44336;
            }}
        """
        
        # If image exists, use it; otherwise use colored button
        if close_img_url and os.path.exists(close_img_url.replace("file:///", "")):
            style = style.replace(
                """QTabBar::close-button {
                subcontrol-position: right;
                width: 13px;
                height: 13px;
                margin-right: 6px;
                border: 1px solid #ff5252;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }""",
                f"""QTabBar::close-button {{
                image: url({close_img_url});
                subcontrol-position: right;
                width: 13px;
                height: 13px;
                margin-right: 6px;
                background: transparent;
                border: none;
            }}"""
            )
        
        self.setStyleSheet(style)
    
    def addWidget(self, widget, title):
        """Add a new tab with the given widget and title"""
        if not widget:
            return -1
            
        self.tab_counter += 1
        if not title:
            title = f"Tab {self.tab_counter}"
        
        # Add the tab
        index = self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(index)
        return index
    
    def activate_tab(self, index):
        """Activate the tab at the specified index."""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
        else:
            print(f"Warning: Invalid tab index: {index}. Must be between 0 and {self.tab_widget.count() - 1}.")
    
    def add_new_tab(self, widget=None, title=None):
        """Add a new tab (alternative method name for compatibility)"""
        if widget is None:
            # Create a default widget if none provided
            widget = QWidget()
            layout = QVBoxLayout(widget)
            label = QLabel(f"Content for {title or f'Tab {self.tab_counter + 1}'}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
        
        return self.addWidget(widget, title)
    
    def close_tab(self, index):
        """Close a tab at the given index"""
        if index < 0 or index >= self.tab_widget.count():
            return False
            
        if self.tab_widget.count() <= 1:
            QMessageBox.information(
                self, 
                'Close Tab', 
                'This is the last tab. Do you want to close it?',
                QMessageBox.StandardButton.Ok
            )
            return False
        
        # get title
        widget_name = self.tab_widget.tabText(index)
        
        # Fix: Check if key exists before deleting
        if widget_name in self.parent.active_tab_widgets:
            del self.parent.active_tab_widgets[widget_name]

        # Update indices for remaining tabs
        for tab in list(self.parent.active_tab_widgets.keys()):
            if self.parent.active_tab_widgets[tab] > index:
                self.parent.active_tab_widgets[tab] -= 1
        
        self.tab_widget.removeTab(index)
        self.tab_close_requested.emit(index)
        return True
    
    def removeTab(self, index):
        """Remove tab at given index"""
        self.tab_widget.removeTab(index)
    
    def setCurrentIndex(self, index):
        """Set the current active tab"""
        self.tab_widget.setCurrentIndex(index)
    
    def currentIndex(self):
        """Get the current active tab index"""
        return self.tab_widget.currentIndex()
    
    def count(self):
        """Get the number of tabs"""
        return self.tab_widget.count()
    
    def widget(self, index):
        """Get widget at given index"""
        return self.tab_widget.widget(index)
    
    def setTabText(self, index, text):
        """Set text for tab at given index"""
        self.tab_widget.setTabText(index, text)
    
    def tabText(self, index):
        """Get text for tab at given index"""
        return self.tab_widget.tabText(index)
