import uuid
from app.job.JobObject import returnType
import pandas as pd

class ConditionObject:
    def __init__(self, name, forward_id, backward_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.forward_id = forward_id
        self.backward_id = backward_id

    def get_jobids(self):
        return self.forward_id, self.backward_id

    def get_combined_tss(self, jobRegistry):
        forward_job = jobRegistry[self.forward_id]
        backward_job = jobRegistry[self.backward_id]

        tss_df_forward = forward_job.get_file(returnType.TSS)
        tss_df_reverse = backward_job.get_file(returnType.TSS)

        combined = pd.concat([tss_df_forward, tss_df_reverse])

        cleaned = combined.drop_duplicates()

        return cleaned

    def get_upsetplot_df(self, jobRegistry):
        forward_job = jobRegistry[self.forward_id]
        backward_job = jobRegistry[self.backward_id]

        tss_df_forward = forward_job.get_file(returnType.TSS)
        tss_df_reverse = backward_job.get_file(returnType.TSS)

        combined = pd.concat([tss_df_forward, tss_df_reverse])

        cleaned = combined.drop_duplicates()

        master_table = forward_job.get_file(returnType.MASTERTABLE)

        rows = []
        for index, row in cleaned.iterrows():
            condition = (master_table["Pos"] == row["Pos"]) & (master_table["TSS type"] == row["TSS type"])

            if(condition.any()):
                rows += [{"Pos": row["Pos"], "TSS type": row["TSS type"], "origin": 2}]
            else:
                rows += [{"Pos": row["Pos"], "TSS type": row["TSS type"], "origin": 0}]

        for index, row in master_table.iterrows():
            condition = (cleaned["Pos"] == row["Pos"]) & (cleaned["TSS type"] == row["TSS type"])

            if(condition.any()):
                pass
            else:
                rows += [{"Pos": row["Pos"], "TSS type": row["TSS type"], "origin": 1}]

        print(rows)

        return_df = pd.DataFrame(rows)

        return return_df

