import unittest
import pandas as pd
from app import GFFParser as ps

class MyTestCase(unittest.TestCase):
    def test_parse_gff_to_df(self):
        result = ps.parse_gff_to_df("test_files/NC_004703.gff").head()
        expected_result = pd.DataFrame({
            "seqid": ["NC_004703.1"] * 5,
            "source": ["RefSeq"] * 5,
            "type": ["gene"] * 5,
            "start": [1, 447, 1077, 1785, 2747],
            "end": [528, 1004, 1469, 2471, 3787],
            "score": ["."] * 5,
            "strand": ["+", "+", "-", "+", "-"],
            "phase": ["."] * 5,
            "attributes": [ "ID=gene-BT_RS24095;Name=BT_RS24095;gbkey=Gene;gene_biotype=protein_coding;locus_tag=BT_RS24095;old_locus_tag=BT_p548201",
                            "ID=gene-BT_RS24100;Name=BT_RS24100;gbkey=Gene;gene_biotype=protein_coding;locus_tag=BT_RS24100;old_locus_tag=BT_p548202",
                            "ID=gene-BT_RS24105;Name=BT_RS24105;gbkey=Gene;gene_biotype=protein_coding;locus_tag=BT_RS24105;old_locus_tag=BT_p548203",
                            "ID=gene-BT_RS24110;Name=BT_RS24110;gbkey=Gene;gene_biotype=protein_coding;locus_tag=BT_RS24110;old_locus_tag=BT_p548204",
                            "ID=gene-BT_RS24115;Name=BT_RS24115;gbkey=Gene;gene_biotype=protein_coding;locus_tag=BT_RS24115;old_locus_tag=BT_p548205"]
        })

        pd.testing.assert_frame_equal(result, expected_result)


if __name__ == '__main__':
    unittest.main()
