from PySide6.QtCore import QObject, Signal, Slot
import time

# Some signals to be used by widgets
# Could be defined in the Worker class but they can also be separated like this.

class WorkerSignals(QObject):
    progress = Signal(int)
    finished = Signal(bool)
    error = Signal(str)
    log = Signal(str)
    eta = Signal(float)
    cpu = Signal(int)
    memory = Signal(int)

# Class for creating worker objects for tasks to be run. Each task is run by its own Worker object.

class Worker(QObject):
    
    # Constructor with the parameters name (defined by order)
    # and CPU and memory requirements (defined randomly) and the time of one step (also defined randomly).
    def __init__(self, name, cpu_req, memory_req, timer):
        super().__init__()
        
        # Create properties according to parameters.
        self.name = name
        self.cpu_requirement = cpu_req
        self.memory_requirement = memory_req
        self.timer = timer
        # Store cpu in temp to allow resetting after pause.
        self.temp = cpu_req

        # Signals are handily in one place like this.
        self.signals = WorkerSignals()
        # Helper variables
        self._running = True
        self._paused = False

    # Method for cancelling the running of the worker
    def stop(self):
        self._running = False
    
    # Pause and resume for controlling the running of tasks and the cpu required. Memory is still used.
    def pause(self):
        self._paused = True
        self.cpu_requirement = 0
    
    def resume(self):
        self._paused = False
        self.cpu_requirement = self.temp

    # This method runs the tasks.
    @Slot()
    def run(self):

        # Get the start time to be used later
        start_time = time.time()

        # Emitting signal to be used in the log
        print(f"Starting {self.name} with timer set to {round(self.timer, 2)}")
        self.signals.log.emit(f"{self.name} started.\n")

        # Completion is True by default and is changed to False if task is cancelled or runs into an error.
        completed = True

        # Index from 0 to 100
        try:
            for i in range(101):
                # If worker is stopped, change completion value and emit the time remaining and cpu and memory requirements to be 0.
                if not self._running:
                    completed = False
                    self.signals.eta.emit(0)
                    self.signals.cpu.emit(0)
                    self.signals.memory.emit(0)
                    break
                # If worker is paused, check for cancellation and wait for resuming.
                while self._paused:
                    time.sleep(0.01)
                    if not self._running:
                        break

                # Wait for step time
                time.sleep(self.timer)

                # Emit progress signal (easy-to-understand progress is signal in percentage (0-100))
                self.signals.progress.emit(i)
                # Also emit the CPU and memory usage signals.
                self.signals.cpu.emit(self.cpu_requirement)
                self.signals.memory.emit(self.memory_requirement)

                # If there is progress, the eta value can be emitted.
                if i > 0:
                    # Create the ETA value as follows
                    elapsed = time.time() - start_time
                    progress_ratio = i/100

                    eta_value = (elapsed / progress_ratio) * (1 - progress_ratio)
                    # If the task is paused, determining the ETA value is impossible so don't emit if paused.
                    if not self._paused:
                        self.signals.eta.emit(eta_value)

        # Emit error signal if task runs into errors.
        except Exception as e:
            self.signals.error.emit(str(e))
            completed = False
            # Also emit ETA, CPU and memory as 0.
            self.signals.eta.emit(0)
            self.signals.cpu.emit(0)
            self.signals.memory.emit(0)

        # When task is complete, emit log -> finished and finished signal.
        finally:
            self.signals.log.emit(f"{self.name} finished.\n")
            self.signals.finished.emit(completed)
            # Also emit CPU and memory as 0.
            self.signals.cpu.emit(0)
            self.signals.memory.emit(0)
        