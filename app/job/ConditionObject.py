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

    def get_combined_common(self, jobRegistry):
        forward_job = jobRegistry[self.forward_id]
        backward_job = jobRegistry[self.backward_id]

        tss_df_forward = forward_job.get_file(returnType.COMMON)
        tss_df_reverse = backward_job.get_file(returnType.COMMON)

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

        return_df = pd.DataFrame(rows)

        return_df['is_duplicate'] = return_df.duplicated('Pos', keep=False)

        priority1_mask = return_df['origin'] == 2 # prioritize common TSS first
        priority2_mask = return_df['TSS type'] == "pTSS/sTSS" # second priority pTSS
        priority3_mask = return_df['TSS type'] == "asTSS" # third priority asTSS

        #filter based upon priority masks

        # Rows with duplicates and high priority
        priority1_rows = return_df[priority1_mask & return_df['is_duplicate']]

        # Rows with duplicates but not priority1
        priority2_rows = return_df[priority2_mask & ~priority1_mask & return_df['is_duplicate']]

        # Rows with duplicates but not priority2
        priority3_rows = return_df[ priority3_mask & ~priority2_mask & ~priority1_mask & return_df['is_duplicate']]

        # Rows with no duplicates
        priority4_rows = return_df[~return_df['is_duplicate']]

        #recombine
        filtered_df = pd.concat([priority1_rows, priority2_rows, priority3_rows, priority4_rows]).drop_duplicates()
        filtered_df = filtered_df.drop(columns=['is_duplicate'])

        return filtered_df

