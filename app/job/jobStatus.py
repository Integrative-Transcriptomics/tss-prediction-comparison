from enum import Enum

# list of all file ending we want to allow the user to upload
class jobStatus(Enum):
    NOT_STARTED = "Not started"
    RUNNING = "Running"
    FINISHED = "Finished"
    FAILED = "Failed"