from PySide6.QtCore import QObject, Signal
from styles import Styles

# Class for managing resources and task queue
class ResourceManager(QObject):

    # Signals to be emitted back to UI
    cpu = Signal(int)
    memory = Signal(int)

    # Constructor
    def __init__(self):
        super().__init__()

        # Helper variables for max and current values for CPU and memory
        self.max_cpu = 100
        self.max_memory = 100

        self.used_cpu = 0
        self.used_memory = 0

        # Create task queue and a list of currently running tasks.
        self.queue = []
        self.running_tasks = []

        # Create sets of tasks' CPU and memory requirements.
        self.task_cpu = {}
        self.task_memory = {}

    # Following methods are for updating a specific task's CPU and memory
    def update_task_cpu(self, task, value):
        self.task_cpu[task] = value
        self.try_task_start()

    def update_task_memory(self, task, value):
        self.task_memory[task] = value
        self.try_task_start()

    # Method for checking whether task given as parameter can run
    # @return boolean value, whether task can run
    def can_task_run(self, task):
        return (
        self.used_cpu + task.worker.cpu_requirement <= self.max_cpu
        and self.used_memory + task.worker.memory_requirement <= self.max_memory
    )
    
    # Methods for allocating or releasing CPU and memory and emitting those values
    def allocate(self, task):
        
        self.used_cpu += task.worker.cpu_requirement
        self.used_memory += task.worker.memory_requirement

        self.cpu.emit(self.used_cpu)
        self.memory.emit(self.used_memory)
    
    def release(self, task):

        self.used_cpu -= task.worker.cpu_requirement
        self.used_memory -= task.worker.memory_requirement

        self.cpu.emit(self.used_cpu)
        self.memory.emit(self.used_memory)
    
    # Method for adding a task given as parameter to the queue and calling method for trying to start a task
    def add_task(self, task):
        self.queue.append(task)
        self.try_task_start()
    
    # Method for trying to start a task from the task queue
    def try_task_start(self):
        # Goes through queue
        for task in self.queue[:]:
            # If the task can run, do required actions to make it start and update values accordingly.
            if self.can_task_run(task):
                self.allocate(task)
                task.start_worker()
                self.running_tasks.append(task)
                self.queue.remove(task)
                task.status.setText("Running...")
                task.status.setStyleSheet(Styles.running)
            # If the task can't run, set it to queue and update values accordingly.
            else:
                task.queued = True
                task.status.setText("Queued")
                task.status.setStyleSheet(Styles.queued)
    
    # Method for actions when a task finishes
    def when_task_finished(self, task):
        
        # Release the memory and remove from running tasks.
        self.release(task)
        if task in self.running_tasks:
            self.running_tasks.remove(task)

        # Remove CPU and memory values from sets
        self.task_cpu.pop(task, None)
        self.task_memory.pop(task, None)

        # Try to start another task.
        self.try_task_start()