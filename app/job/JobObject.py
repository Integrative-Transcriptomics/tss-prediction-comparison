import uuid
from app.job.JobStatus import JobStatus
from app.job.NotReadyException import NotReadyException
from app.prediction.tssPredictor import tss_predictor_sklearn
import app.prediction.OperationsOnWiggle as ops


class JobObject:
    def __init__(self, filepaths, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.status = JobStatus.NOT_STARTED
        self.paths = filepaths
        self.return_object = {}

    def get_return_object(self):
        if self.status == JobStatus.FINISHED:

            return self.return_object
        else:
            raise NotReadyException("Job is not done yet")

    def process(self):
        dataframe_to_predict = ops.parse_for_prediction(self.paths)
        self.return_object = tss_predictor_sklearn(dataframe_to_predict)
        self.status = JobStatus.FINISHED
