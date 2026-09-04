from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal
from tasks import TaskWidget
from resources import ResourceManager

# Class for creating a TaskList creates a vertical layout in which tasks are placed
# This is then placed inside the scroll are in the frontend.
class TaskList(QWidget):

    # Signals to the log of the frontend. Might not be strictly necessary but keeps it connected.
    log = Signal(str)
    error = Signal(str)
    eta = Signal(float)
    finished = Signal(bool)
    cpu = Signal(int)
    memory = Signal(int)

    # Constructor
    def __init__(self):
        super().__init__()
        
        # Create VBoxLayout and addStretch for later use.
        self.layout = QVBoxLayout(self)
        self.layout.addStretch()

        self.manager = ResourceManager()

        # Helper variables which help name new tasks and check if they're still running
        self.task_count = 0
        self.tasks = []

        # CPU and memory signals need to be connected (to be re-emitted) here since they are needed in the initialization of the tasklist.
        self.manager.cpu.connect(self.cpu)
        self.manager.memory.connect(self.memory)
    
    # Method for adding tasks and doing related activities
    def add_task(self):
        # Add task and add one to count and task to task list.
        self.task_count += 1
        self.task = TaskWidget(f"Task {self.task_count}")
        self.tasks.append(self.task)

        # The following signals are connected to the resource manager each time a new task is added (for the added task)
        # The finished signal doesn't need to emit the boolean, only the task that is finished.
        self.task.finished.connect(lambda _, task=self.task: self.manager.when_task_finished(task))

        # The CPU and memory signals need to emit the value and the task.
        self.task.cpu.connect(lambda value, task=self.task: self.manager.update_task_cpu(task, value))
        self.task.memory.connect(lambda value, task=self.task: self.manager.update_task_memory(task, value))

        # Call the resource manager's add task method to add task properly. Then configure task (layout and signals).
        self.manager.add_task(self.task)
        self.configure_task()
    
    # Method for adding TaskWidget to layuot and connecting its signals
    def configure_task(self):
        # Add the widget by inserting it to the top.
        self.layout.insertWidget(self.layout.count() - 1, self.task)

        # Connect signals.
        # - Log signal is sent to frontend
        # - Also in the case of an error
        # - Eta signal updates eta and re-emits
        # - Finished signal also needs to update eta for it to reach 0
        # - Finished signal is also re-emitted

        self.task.log.connect(self.log)
        self.task.error.connect(self.error)
        self.task.eta.connect(self.update_eta)
        self.task.eta.connect(self.eta)
        self.task.finished.connect(self.update_eta)
        self.task.finished.connect(self.finished)
        

    # Method for updating the frontend ETA calculator
    def update_eta(self):
        
        # Define total variable and a list of running tasks (list of self.tasks tasks which are running)
        total = 0
        running_tasks = [task for task in self.tasks if task.running]

        # If there are running tasks, set the total amount to the highest amount of time left.
        # This is found with a max value of a list comprehension that finds the tasks' current_eta property
        if running_tasks:
            try:
                total = max(task.current_eta for task in running_tasks if task.current_eta > 0)
            except ValueError:
                total = 0

        # Display the total value.
        self.task.eta_label.setText(f"{total:.2f} s")
        return f"{total:.2f} s"
    
    # Method for calling the stopping of all workers from the TaskWidget class.
    # If there are no active workers, skips functionality so it can be called safely.
    def exit_press(self):
        try:
            self.task.destroy_workers()
        except:
            pass