import app.MasterTableParser as mtp
import pandas as pd
import unittest
import sys
sys.path.append('../')



class MyTestCase(unittest.TestCase):

    def setUp(self):
        })

    def test_parse_master_table_to_df(self):
        df = mtp.parse_master_table_to_df(file_path)
        pd.testing.assert_frame_equal(df, self.df)