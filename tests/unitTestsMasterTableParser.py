import unittest
import pandas as pd
import app.MasterTableParser as p
path_to_test_folder = "test_files/"


class MyTestCase(unittest.TestCase):


    def setUp(self):

        # correct data for test1
        self.df_infected_test1 = pd.DataFrame({
            "Pos": [1],
            "Strand": ["+"],
            "TSS type": ["Orphan"]
        })

        self.df_uninfected_test1 = pd.DataFrame({
            "Pos": [2],
            "Strand": ["+"],
            "TSS type": ["Secondary"]
        })

        self.dict_test1 = {"infected": self.df_infected_test1,
                           "uninfected": self.df_uninfected_test1}


        # correct data for test2
        self.df_infected_test2 = pd.DataFrame({
            "Pos": [442, 507],
            "Strand": ["+", "-"],
            "TSS type": ["Primary", "Antisense"]
        })

        self.df_uninfected_test2 = pd.DataFrame({
            "Pos": [507],
            "Strand": ["-"],
            "TSS type": ["Antisense"]
        })

        self.dict_test2 = {"infected": self.df_infected_test2,
                           "uninfected": self.df_uninfected_test2}


    def test1_parse_MasterTable_to_dict(self):
        dict = p.parse_master_table(path_to_test_folder + "TestFile1MasterTable.tsv")
        for cond in self.dict_test1:
            pd.testing.assert_frame_equal(dict[cond], self.dict_test1[cond])


    def test2_parse_MasterTable_to_dict(self):
        dict = p.parse_master_table(path_to_test_folder + "TestFile2MasterTable.tsv")
        for cond in self.dict_test2:
            pd.testing.assert_frame_equal(dict[cond], self.dict_test2[cond])