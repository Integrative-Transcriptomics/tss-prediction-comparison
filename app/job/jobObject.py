from .jobStatus import jobStatus
from .NotReadyException import NotReadyException
import sys
sys.path.append("..")
from prediction.tssPredictor import tssPredictor

import uuid

class jobObject:
    def __init__(self, filepath, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.status = jobStatus.NOT_STARTED
        self.path = filepath
        self.return_object = {}

    def getReturnObject(self):
        if(self.status == jobStatus.FINISHED):

            return self.return_object
        else:
            raise NotReadyException("Job is not done yet")

    def process(self):
        self.return_object = tssPredictor(self.path)
        self.status = jobStatus.FINISHED


