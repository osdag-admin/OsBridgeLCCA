from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QIcon, QPixmap)
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QWidget, QLabel)
from PySide6.QtGui import QMouseEvent

class CustomTitleBar(QWidget):
    """
    A custom title bar widget for a frameless QMainWindow.
    It provides window dragging, minimize, maximize/restore, and close buttons
    with custom styling and SVG icons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("custom_title_bar")
        self.setFixedHeight(30)
        # Set a single stylesheet for the entire title bar and all its children
        self.setStyleSheet("""
            #custom_title_bar {
                background-color: #45913E;
            }
            #custom_title_bar QLabel {
                background-color: #45913E;
                color: white;
            }
            #custom_title_bar QPushButton {
                background-color: #45913E;
                color: white;
                border: none;
                padding: 0px;
            }
            #custom_title_bar QPushButton:hover {
                background-color: #55a04c;
            }
            #custom_title_bar QPushButton:pressed {
                background-color: #3d7936;
            }
            #custom_title_bar QPushButton#close_button:hover {
                background-color: #E81123;
            }
            #custom_title_bar QPushButton#close_button:pressed {
                background-color: #F1707A;
            }
        """)

        # Main layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Left: Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(30, 30)
        self.icon_label.setStyleSheet("padding: 5px;")
        # self.icon_label.setPixmap(QPixmap("resources/osdag_logo.svg").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.icon_label)

        # Middle: Title (centered)
        self.title_label = QLabel("My Custom App")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.title_label, 1)  # Add stretch factor of 1 to center the title

        # Right: Control Buttons
        self.btn_size = QSize(46, 30)

        # Helper function to create a styled button
        def create_button(icon_svg, is_close=False):
            btn = QPushButton()
            btn.setFixedSize(self.btn_size)
            btn.setIcon(QIcon(QPixmap.fromImage(QPixmap(icon_svg).toImage())))
            btn.setIconSize(QSize(14, 14))
            if is_close:
                btn.setObjectName("close_button")
            return btn

        # Control buttons
        self.minimize_button = create_button("resources/window_minimize.svg")
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.layout.addWidget(self.minimize_button)

        self.maximize_button = create_button("resources/window_maximize.svg")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.maximize_button)

        self.close_button = create_button("resources/window_close.svg", is_close=True)
        self.close_button.clicked.connect(self.parent_window.close)
        self.layout.addWidget(self.close_button)

        self.start_pos = None
        self.start_geometry = None

    def set_maximize_icon(self):
        self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap("resources/window_maximize.svg").toImage())))

    def set_restore_icon(self):
        self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap("resources/window_restore.svg").toImage())))

    def toggle_maximize_restore(self):
        """Toggles between maximized and normal window states and updates the icon."""
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.set_maximize_icon()
        else:
            self.parent_window.showMaximized()
            self.set_restore_icon()

    # --- Window Dragging Functionality ---
    def mousePressEvent(self, event: QMouseEvent):
        """Records initial position for dragging."""
        if event.button() == Qt.LeftButton and not self.parent_window.isMaximized():
            self.start_pos = event.globalPosition().toPoint()
            self.start_geometry = self.parent_window.geometry()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Moves the window based on mouse movement."""
        if event.buttons() == Qt.LeftButton and self.start_pos and not self.parent_window.isMaximized():
            delta = event.globalPosition().toPoint() - self.start_pos
            new_x = self.start_geometry.x() + delta.x()
            new_y = self.start_geometry.y() + delta.y()
            self.parent_window.move(new_x, new_y)
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Resets dragging state."""
        if not self.parent_window.isMaximized():
            self.start_pos = None
            self.start_geometry = None
        event.accept()
