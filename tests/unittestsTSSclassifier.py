import unittest
import pandas as pd
from app import TSSclassifier as cl
from app import GFFParser as ps


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.tss_fw_list = [400, 1005, 20100, 21100, 12523]
        self.tss_rv_list = [1005, 26695, 1670, 26696, 32000]
        self.gff_df = ps.parse_gff_to_df("test_files/NC_004703.gff")
        self.confidence_list = [0.9, 0.7, 0.65, 0.8, 0.9]
        self.classification_fw = pd.DataFrame({
            "Pos": [400, 400, 1005, 20100, 21100, 12523, 12523],
            "TSS type": ["iTSS", "pTSS/sTSS", "asTSS", "orphan", "asTSS", "iTSS", "pTSS/sTSS"],
            "confidence": [0.9, 0.9, 0.7, 0.65, 0.8, 0.9, 0.9],
            "gene name": ["BT_RS24095", "BT_RS24100", "BT_RS24105", None, "BT_RS24225", "BT_RS24155", "BT_RS24160"],
            "distance": [0, 0, 780, 2012, 1012, 0, 0]})

        self.classification_rv = pd.DataFrame({
            "Pos": [1005, 26695, 1670, 26696, 32000],
            "TSS type": ["asTSS", "iTSS", "orphan", "pTSS/sTSS", "asTSS"],
            "confidence": [0.9, 0.7, 0.65, 0.8, 0.9],
            "gene name": ["BT_RS24100", "BT_RS24255", None, "BT_RS24255", "BT_RS24295"],
            "distance": [None, 0, 201, 1, 638]})

        self.mastertable = pd.DataFrame({
            "Pos": [1005, 26700, 1670, 26691, 405, 20100, 12520, 22000],
            "Strand": ["-", "-", "-", "-", "+", "+", "+", "+"],
            "TSS type": ["iTSS", "iTSS", "orphan", "pTSS/sTSS", "iTSS", "pTSS/sTSS", "pTSS/sTSS", "asTSS"]
        })

    def test_classify(self):
        pd.testing.assert_frame_equal(cl.classify(self.gff_df, self.tss_fw_list, self.confidence_list, False),
                                      self.classification_fw)

        pd.testing.assert_frame_equal(cl.classify(self.gff_df, self.tss_rv_list, self.confidence_list, True),
                                      self.classification_rv)

    def test_find_common_tss(self):
        expected_fw = pd.DataFrame({
            "Pos": [12520, 405],
            "TSS type": ["pTSS/sTSS", "iTSS"],
            "confidence": [0.9, 0.9],
            "gene name": ["BT_RS24160", "BT_RS24095"],
            "distance": [0, 0]
        })
        expected_rv = pd.DataFrame({
            "Pos": [26691, 1670, 26700],
            "TSS type": ["pTSS/sTSS", "orphan", "iTSS"],
            "confidence": [0.8, 0.65, 0.7],
            "gene name": ["BT_RS24255", None, "BT_RS24255"],
            "distance": [1.0, 201.0, 0.0]
        })
        print(cl.find_common_tss(self.classification_fw, self.mastertable, False))
        print(cl.find_common_tss(self.classification_rv, self.mastertable, True))
        pd.testing.assert_frame_equal(cl.find_common_tss(self.classification_fw, self.mastertable, False), expected_fw)
        pd.testing.assert_frame_equal(cl.find_common_tss(self.classification_rv, self.mastertable, True), expected_rv)


if __name__ == '__main__':
    unittest.main()
