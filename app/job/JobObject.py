import uuid
from app.job.JobStatus import JobStatus
from app.job.JobExceptions import NotReadyException, NotSuppliedException
from app.prediction.tssPredictor import tss_predictor_sklearn
import app.prediction.OperationsOnWiggle as ops
from app import TSSclassifier as cs
from app import GFFParser as ps
from app import MasterTableParser as mtp
from enum import Enum

class returnType(Enum):
    TSS = "tss"
    MASTERTABLE = "master table"
    COMMON = "common"

class JobObject:
    def __init__(self, filepaths, name, master_table_path = None, gff_path = None, is_reverse_strand = False ):
        self.name = name
        self.id = str(uuid.uuid4())
        self.processedDF = None
        self.status = JobStatus.NOT_STARTED
        self.paths = filepaths
        self.is_reverse_strand = is_reverse_strand
        self.master_table_path = master_table_path
        self.gff_path = gff_path
        self.classified_tss = None
        self.common_tss = None
        self.master_table = None

    def get_file(self, type):
        if self.status == JobStatus.FINISHED:

            if(type == returnType.TSS):
                return self.classified_tss
            if(type == returnType.COMMON):
                if(self.common_tss is None):
                    raise NotSuppliedException("The Master Table or gff file was not supplied")
                else:
                    return self.common_tss
            if(type == returnType.MASTERTABLE):
                if(self.master_table is None):
                    raise NotSuppliedException("The Master Table was not supplied")
                else:
                    return self.master_table
            else:
                raise Exception("Unknown filetype")
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

        if(not self.gff_path is None):
            gff_df = ps.parse_gff_to_df(self.gff_path)
            #ToDO include confidence values in df
            self.classified_tss = cs.classify(gff_df, tss_list, self.is_reverse_strand)
        if(not self.master_table_path is None):
            self.master_table = mtp.parse_master_table_to_df(self.master_table_path)
            self.common_tss = cs.find_common_tss(self.classified_tss, self.master_table)

        self.status = JobStatus.FINISHED
