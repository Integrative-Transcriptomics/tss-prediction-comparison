import uuid
from app.job.JobStatus import JobStatus
from app.job.JobExceptions import NotReadyException
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


class ConditionNotFoundException(Exception):
    """Custom exception in case self.condition_name of JobObject is not found in MasterTable of JobObject."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class JobObject:
    def __init__(self,
                 filepaths,
                 name,
                 condition_name,
                 master_table_path=None,
                 gff_path=None,
                 is_reverse_strand=False):

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
        self.condition_name = condition_name  # upload_file in server.py needs to be adjusted

    def get_file(self, type):
        if self.status == JobStatus.FINISHED:

            if (type == returnType.TSS):
                return self.classified_tss

            if (type == returnType.COMMON):
                return self.common_tss

            if (type == returnType.MASTERTABLE):
                return self.master_table

            else:
                raise Exception("Unknown filetype")
        else:
            raise NotReadyException("Job is not done yet")

    def get_processed_df(self):
        if (self.processedDF is not None):
            return self.processedDF
        else:
            raise NotReadyException("Computing the mean df is not done yet")

    def process(self):
        dataframe_to_predict, median_df = ops.parse_for_prediction(self.paths, self.is_reverse_strand)
        self.processedDF = median_df
        tss_list, confidence_list = tss_predictor_sklearn(dataframe_to_predict)

        try:
            gff_df = ps.parse_gff_to_df(self.gff_path)
            self.classified_tss = cs.classify(gff_df, tss_list, confidence_list, self.is_reverse_strand)
            self.common_tss = self.__compute_common_tss()
        except (ConditionNotFoundException, cs.GffFormatException) as e:
            self.status = JobStatus.FAILED
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        else:
            self.status = JobStatus.FINISHED

    def __compute_common_tss(self):
        """
        Computes common TSS of this and corresponding TSS of master_table.
        :return: common TSS
        """
        conditions_of_master_table = mtp.parse_master_table(self.master_table_path)
        try:
            self.master_table = conditions_of_master_table[self.condition_name]
        except KeyError as e:
            raise ConditionNotFoundException(
                "condition_name of JobObject: " + self.condition_name + " does not exist in provided MasterTable") from e
        else:
            common_tss = cs.find_common_tss(self.classified_tss, self.master_table, self.is_reverse_strand)

            return common_tss
