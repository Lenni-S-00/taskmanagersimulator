from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QProgressBar
from PySide6.QtCore import QThread, Signal
from workers import Worker
from styles import Styles

import random

# Class for creating task widget objects that have the running task and metrics inside
class TaskWidget(QWidget):

    # Signals to be emitted forward
    log = Signal(str)
    eta = Signal(float)
    finished = Signal(bool)
    error = Signal(str)
    cpu = Signal(int)
    memory = Signal(int)

    # Constructor with parameter name to be given the task
    def __init__(self, name):
        super().__init__()

        # Set name variable to be set to the worker.
        self.name = name

        # Create other variables.
        self.current_eta = 0
        self.running = False
        self.queued = False

        # Create and set layouts of the task's graphical widget.
        self.toplayout = QGridLayout()
        self.tasklayout = QGridLayout()
        self.barlayout = QGridLayout()

        self.setLayout(self.toplayout)

        # Call methods for creating properties.
        self.create_widgets()
        self.create_utils()

    # Method for widget creation
    def create_widgets(self):

        # Create labels for the task's name and status and a progress bar for its progress.
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet(Styles.tasks)

        self.status = QLabel("Running...")
        self.status.setStyleSheet(Styles.running)
        self.eta_label = QLabel("")
        
        self.progress = QProgressBar()

        # Create necessary buttons for the task.
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(Styles.taskcancel)
        self.resume_button = QPushButton("Resume")
        self.resume_button.setStyleSheet(Styles.taskresume)
        self.pause_button = QPushButton("Pause")
        self.pause_button.setStyleSheet(Styles.taskpause)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet(Styles.taskdelete)
    
    # Method for creating other parts (other than the widgets)
    def create_utils(self):

        # Create thread (important for concurrency).
        # This is where the worker (and the task) will be run in.
        self.thread = QThread()

        # Define other properties.
        self.set_layouts()
        self.def_workers()
        self.buttoncontrol()

    # Method for defining worker-related properties
    def def_workers(self):
        # Helper list
        self.workers = []
        
        # Set random memory requirement and timer for worker step (with fitting values).
        mem_req = random.randint(10, 40)
        timer = random.uniform(0.01, 0.1)
        # CPU usage correlates to timer value
        cpu_req = timer*400

        # Create the Worker itself and move it to thread
        self.worker = Worker(self.name, cpu_req, mem_req, timer)
        self.worker.moveToThread(self.thread)
        
        # Call the worker signals to be connected correctly.
        self.worker_signals()

    # Method for setting up worker signals
    def worker_signals(self):
        
        # Run the worker's run method upon creation.
        self.thread.started.connect(self.worker.run)

        # Connect progress signal to helper method.
        self.worker.signals.progress.connect(self.update_progress)

        # Connect finished signal to be re-emitted (to have the effect shown by frontend),
        # and connect it to quit and delete the task properly.
        self.worker.signals.finished.connect(self.finished)
        self.worker.signals.finished.connect(self.finish)
        self.worker.signals.finished.connect(self.thread.quit)
        self.worker.signals.finished.connect(self.worker.deleteLater)
        self.worker.signals.finished.connect(self.thread.deleteLater)

        # Re-emit log signals and print possible error in console for debugging purposes.
        self.worker.signals.log.connect(self.log)
        self.worker.signals.error.connect(self.error)
        self.worker.signals.error.connect(self.error_message)

        # ETA is updated per task and also re-emitted to possibly be shown as the longest ETA.
        self.worker.signals.eta.connect(self.eta)
        self.worker.signals.eta.connect(self.update_eta)
        
        # Re-emit CPU and memory requirements.
        self.worker.signals.cpu.connect(self.cpu)
        self.worker.signals.memory.connect(self.memory)
    
    # Method for starting the worker.
    # Called by other objects upon task creation.
    def start_worker(self):

        self.thread.start()
        self.workers.append(self.worker)
    
    # Method for connecting button signals
    def buttoncontrol(self):

        self.cancel_button.clicked.connect(self.cancel)
        self.resume_button.clicked.connect(self.resume_press)
        self.pause_button.clicked.connect(self.pause_press)
        # Delete button is added when task is complete/cancelled.
        self.delete_button.clicked.connect(lambda: self.setParent(None))
        self.delete_button.clicked.connect(self.deleteLater)
    
    # Set widgets and layouts to layouts
    def set_layouts(self):
        
        self.tasklayout.addWidget(self.name_label, 0, 0)
        self.tasklayout.addWidget(self.status, 0, 1)
        self.tasklayout.addWidget(self.eta_label, 0, 2)

        self.tasklayout.addWidget(self.cancel_button, 1, 2)
        self.tasklayout.addWidget(self.pause_button, 1, 1)
        self.tasklayout.addWidget(self.resume_button, 1, 0)

        # Layout setup
        self.barlayout.addWidget(self.progress, 0, 0)
        self.toplayout.addLayout(self.tasklayout, 0, 0)
        self.toplayout.addLayout(self.barlayout, 1, 0)
        
    # Set progress bar value to correspond progress.
    def update_progress(self, value):
        self.progress.setValue(value)
        if self.workers:
            self.running = True

    # Set ETA value to correspond ETA. Also set the label accordingly.
    def update_eta(self, eta):
        self.current_eta = eta
        self.eta_label.setText(f"{eta:.2f} s")

    # Print error
    def error_message(self, error):
        print(error)

    # Handle pause and resume clicks accordingly
    def pause_press(self):
        self.status.setText("Paused")
        self.status.setStyleSheet(Styles.paused)
        self.worker.pause()

    def resume_press(self):
        self.status.setText("Running...")
        self.status.setStyleSheet(Styles.running)
        self.worker.resume()

    # Handle cancel clicks to stop the task and update UI.
    def cancel(self):
        print(f"{self.worker} stopped.")
        self.status.setText("Cancelled")
        self.status.setStyleSheet(Styles.cancelled)
        self.worker.stop()
        # Call task ending helper
        self.when_ended()
    
    # Method for handling task finishing, update UI
    def finish(self, completed):
        if completed == True:
            self.status.setText("Ready")
            self.status.setStyleSheet(Styles.ready)
        else:
            print("Not finished.")
        # Call task ending helper
        self.when_ended()

    # Show delete button when task finished.
    # Hide other buttons.
    def when_ended(self):
        self.cancel_button.setVisible(False)
        self.resume_button.setVisible(False)
        self.pause_button.setVisible(False)
        self.eta_label.setVisible(False)
        self.tasklayout.addWidget(self.delete_button, 1, 2)

    # Method for stopping workers upon exiting the app to prevent errors
    def destroy_workers(self):
        for worker in self.workers:
            worker.stop()