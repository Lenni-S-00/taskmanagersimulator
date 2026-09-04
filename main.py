# A GUI application made to be a task manager simulator
# Using PySide6 for frontend and functionality
# App is run as a QApplication
# Default windowsize is 800x600

from PySide6.QtWidgets import QApplication
from frontend import MainWindow

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.resize(800,600)
    window.show()
    app.exec()