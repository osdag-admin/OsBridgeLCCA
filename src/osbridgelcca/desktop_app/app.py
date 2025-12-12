from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt
from main_template import UiMainWindow
import sys

class MyMainWindow(QMainWindow):
    """
    The main application window that uses a custom title bar.
    """
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    # Enable mnemonics (underlined shortcuts) for menu items
    QCoreApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())