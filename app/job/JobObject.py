import uuid
from app.job.JobStatus import JobStatus
from app.job.NotReadyException import NotReadyException
from app.prediction.tssPredictor import tss_predictor_sklearn
import app.prediction.OperationsOnWiggle as ops
from app import TSSclassifier as cs

class JobObject:
    def __init__(self, filepaths, name, master_table = None, gff_data_frame = None, is_reverse_strand = False ):
        self.name = name
        self.id = str(uuid.uuid4())
        self.processedDF = None
        self.status = JobStatus.NOT_STARTED
        self.paths = filepaths
        self.is_reverse_strand = is_reverse_strand
        self.master_table = master_table
        self.gff_data_frame = gff_data_frame
        self.classified_tss = None
        self.common_tss = None

    def get_return_object(self):
        if self.status == JobStatus.FINISHED:

            return self.return_object
        else:
            raise NotReadyException("Job is not done yet")

    def get_processed_df(self):
        if(self.processedDF is not None):
            return self.processedDF
        else:
            raise NotReadyException("Computing the mean df is not done yet")
    def process(self):
        dataframe_to_predict, median_df = ops.parse_for_prediction(self.paths, self.is_reverse_strand)
        self.processedDF = median_df
        tss_list, confidence_list = tss_predictor_sklearn(dataframe_to_predict)

        if(not self.gff_data_frame is None):
            self.classified_tss = cs.classify(self.gff_data_frame, tss_list, self.is_reverse_strand)
        if(not self.master_table is None):
            self.common_tss = cs.find_common_tss(self.classified_tss, self.master_table)

        self.status = JobStatus.FINISHED
