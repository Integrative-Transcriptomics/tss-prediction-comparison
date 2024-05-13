import uuid
import sys
sys.path.append("..")
from .JobStatus import JobStatus
from .NotReadyException import NotReadyException
from prediction.tssPredictor import tss_predictor


class JobObject:
    def __init__(self, filepath, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.status = JobStatus.NOT_STARTED
        self.path = filepath
        self.return_object = {}

    def get_return_object(self):
        if self.status == JobStatus.FINISHED:

            return self.return_object
        else:
            raise NotReadyException("Job is not done yet")

    def process(self):
        self.return_object = tss_predictor(self.path)
        self.status = JobStatus.FINISHED
