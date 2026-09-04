from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QScrollArea, QLabel, QPushButton, QTextEdit, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from tasklist import TaskList
from styles import Styles

# A QMainWindow class to hold the graphical elements inside

class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        super().__init__()
        # Name of the window created by running main.py
        self.setWindowTitle("My Task Manager")

        # Create a "panel" and add a layout.
        # Can be any layout since only one widget is added.
        self.panel = QWidget()
        self.layout = QGridLayout()

        # Set the widget and layout to be used.
        self.setCentralWidget(self.panel)

        self.panel.setLayout(self.layout)

        # Create UI elements
        self.UI = MainUI()
        self.layout.addWidget(self.UI, 0, 0)

# A QWidget class to create widgets and layouts
# Holds all of the graphical elements inside.

class MainUI(QWidget):
    
    # Constructor
    def __init__(self):
        super().__init__()

        # Create some layouts. Many are used to achieve desired layout structure.
        self.layout = QGridLayout(self)

        self.util_layout = QGridLayout()
        
        self.eta_layout = QVBoxLayout()

        # Create the scroll area and the tasklist object. "Place" the tasklist into the scroll area.
        self.scroll_area = QScrollArea()
        self.tasklist = TaskList()
        self.scroll_area.setWidget(self.tasklist)
        self.scroll_area.setWidgetResizable(True)
        
        # Call the setup methods.
        self.create_widgets()
        self.set_layouts()
        self.connection()
        
    # Method for connecting signals

    def connection(self):
        
        # Connect buttons to corresponding methods
        self.add_button.clicked.connect(self.tasklist.add_task)
        self.exitbutton.clicked.connect(self.exit_app)
        self.log_clear_button.clicked.connect(self.log_box.clear)

        # Connect tasklist signals to corresponding methods
        self.tasklist.log.connect(self.update_log)
        self.tasklist.error.connect(self.update_log)
        self.tasklist.eta.connect(self.update_eta)
        self.tasklist.finished.connect(self.update_eta)
        self.tasklist.cpu.connect(self.update_cpu_usage)
        self.tasklist.memory.connect(self.update_memory_usage)
    
    # Method for creating and setting styles of widgets
    def create_widgets(self):

        # Create and set up labels.
        self.task_info_label = QLabel("Add tasks by pressing the button here.")
        self.task_info_label.setFixedHeight(40)
        self.task_info_label.setStyleSheet(Styles.taskinfo)
        self.eta_info_label = QLabel("Estimated time left:")
        self.eta_info_label.setFixedHeight(40)
        self.eta_info_label.setStyleSheet(Styles.info)
        self.eta_label = QLabel("")
        self.eta_label.setFixedHeight(40)
        self.eta_label.setStyleSheet(Styles.eta)
        self.log_label = QLabel("Log window")
        self.log_label.setFixedHeight(40)
        self.log_label.setStyleSheet(Styles.info)
        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_label.setFixedHeight(40)
        self.cpu_label.setStyleSheet(Styles.info)
        self.memory_label = QLabel("Memory Usage:")
        self.memory_label.setFixedHeight(40)
        self.memory_label.setStyleSheet(Styles.info)

        # Create and set up buttons.
        self.add_button = QPushButton("Add task")
        self.add_button.setFixedHeight(40)
        self.add_button.setStyleSheet(Styles.addtask)
        self.log_clear_button = QPushButton("Clear log")
        self.log_clear_button.setFixedHeight(42)
        self.log_clear_button.setStyleSheet(Styles.clearlog)
        self.exitbutton = QPushButton("Exit")
        self.exitbutton.setFixedHeight(42)
        self.exitbutton.setStyleSheet(Styles.exit)

        # Create and set up progress bars for monitoring the resources
        # and a log box for logging task starts and ends.
        self.cpu_usage = QProgressBar()
        self.memory_usage = QProgressBar()
        
        self.log_box = QTextEdit()
        self.log_box.setFixedHeight(100)
    
    # The following two methods update the on screen value for the CPU and memory resources.
    # These are called via a signal.
    def update_cpu_usage(self, usage):
        self.cpu_usage.setValue(usage)
    
    def update_memory_usage(self, mem):
        self.memory_usage.setValue(mem)

    # Method for showing desired message in log box
    def update_log(self, msg):
        # New messages start from the top.
        cursor = self.log_box.textCursor()
        cursor.movePosition(QTextCursor.Start)
        # Write
        cursor.insertText(msg)

        # Call limit
        self.log_limit()
    
    # Method for updating the on screen ETA value
    def update_eta(self):
        self.eta_label.setText(self.tasklist.update_eta())
    
    # Method for limiting the log to 50 lines.
    def log_limit(self):
        max_lines = 50
        
        # As long as the console is longer than 50 lines
        # remove the last line. 
        while self.log_box.document().blockCount() > max_lines:
            cursor = self.log_box.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.movePosition(QTextCursor.Up, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    # Kill threads and exit app.
    def exit_app(self):
        self.tasklist.exit_press()
        QApplication.quit()

    # Layouts for this class
    def set_layouts(self):

        # Widgets in the util_layout on the left side of the layout
        self.util_layout.addWidget(self.task_info_label, 0, 0, alignment = Qt.AlignTop)
        self.util_layout.addWidget(self.add_button, 0, 1, alignment = Qt.AlignTop)
        self.util_layout.addWidget(self.log_label, 1, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.log_box, 2, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.log_clear_button, 3, 0, alignment=Qt.AlignTop)

        self.util_layout.addWidget(self.cpu_label, 4, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.cpu_usage, 5, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.memory_label, 6, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.memory_usage, 7, 0, alignment=Qt.AlignTop)
        self.util_layout.addWidget(self.exitbutton, 8, 0, alignment=Qt.AlignTop)
        
        # Widgets in the eta_layout in the middle of the screen
        self.eta_layout.addWidget(self.eta_info_label, 0, alignment=Qt.AlignTop)
        self.eta_layout.addWidget(self.eta_label, 1, alignment=Qt.AlignTop)

        self.util_layout.addLayout(self.eta_layout, 2, 1)

        # Add layouts to main layout.
        self.layout.addLayout(self.util_layout, 0, 0)
        self.layout.addWidget(self.scroll_area, 0, 2)

        # Set row stretches to prevent graphical elements from scaling vertically to keep clarity.
        self.util_layout.setRowStretch(0, 0)
        self.util_layout.setRowStretch(1, 0)
        self.util_layout.setRowStretch(2, 0)
        self.util_layout.setRowStretch(3, 0)
        self.util_layout.setRowStretch(4, 0)
        self.util_layout.setRowStretch(5, 0)
        self.util_layout.setRowStretch(6, 0)
        self.util_layout.setRowStretch(7, 0)
        self.util_layout.setRowStretch(8, 0)
        self.util_layout.setRowStretch(9, 10)

        # Set main layout column stretches to prevent widgets in the specified layouts from scaling horizontally
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(2,6)