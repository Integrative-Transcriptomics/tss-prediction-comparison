import unittest
import app.prediction.OperationsOnWiggle as ops
import pandas as pd
import numpy as np

file_path = 'test_files\\test.wig'


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "region": ["MT"] * 5,
            "position": [1, 2, 3, 4, 5],
            "value": [520.0, 536.0, 553.0, None, 568.0]
        })

    def test_parse_wiggle_to_DataFrame(self):
        df = ops.parse_wiggle_to_DataFrame(file_path)
        pd.testing.assert_frame_equal(df, self.df)

    def test_add_x(self):
        result_df = ops.add_x(self.df.copy(), 2, 1, 5)
        expected_values = [522.0, 538.0, 555.0, np.nan, 570.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.add_x(self.df.copy(), 2, 3, 5)
        expected_values = [520.0, 536.0, 555.0, np.nan, 570.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_sub_x(self):
        result_df = ops.sub_x(self.df.copy(), 10, 2, 4)
        expected_values = [520.0, 526.0, 543.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.sub_x(self.df.copy(), 10, 1, 5)
        expected_values = [510.0, 526.0, 543.0, np.nan, 558.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_mult_x(self):
        result_df = ops.mult_x(self.df.copy(), 0.5, 1, 2)
        expected_values = [260.0, 268.0, 553.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.mult_x(self.df.copy(), 3, 1, 5)
        expected_values = [1560.0, 1608.0, 1659.0, np.nan, 1704.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_div_x(self):
        result_df = ops.div_x(self.df.copy(), 0.5, 1, 5)
        expected_values = [1040.0, 1072.0, 1106.0, np.nan, 1136.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.div_x(self.df.copy(), 2, 1, 1)
        expected_values = [260.0, 536.0, 553.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_median(self):
        self.assertEqual(ops.median(self.df), 544.5)
        self.assertEqual(ops.median(self.df, 1, 3), 536)

    def test_quantil(self):
        self.assertEqual(ops.quantil(self.df, 0.5), 544.5)
        self.assertEqual(ops.quantil(self.df, 0.25), 532.0)

    def test_mean(self):
        self.assertEqual(ops.mean(self.df), 544.25)
        self.assertEqual(ops.mean(self.df, 3, 5), 560.5)

    def test_std(self):
        self.assertAlmostEqual(ops.std(self.df), 18.00520758)


if __name__ == '__main__':
    unittest.main()
