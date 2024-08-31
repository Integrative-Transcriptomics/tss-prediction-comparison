import unittest
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
import app.prediction.OperationsOnWiggle as ops
file_path = 'test_files\\test.wig'


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "region": ["MT"] * 5,
            "position": [1, 2, 3, 4, 5],
            "value": [520.0, 536.0, 553.0, None, 568.0]
        })

        self.df2 = pd.DataFrame({
            "region": ["MT"] * 6,
            "position": [1, 2, 3, 4, 5, 6],
            "value": [521.0, 550.0, 553.0, 557.0, 563.0, 600]
        })

        self.df3 = pd.DataFrame({
            "region": ["MT"] * 6,
            "position": [1, 2, 3, 4, 5, 6],
            "value": [20.0, 500.0, 1553.0, 1557.0, 1563.0, 1600]
        })

    def test_parse_wiggle_to_DataFrame(self):
        df = ops.parse_wiggle_to_DataFrame(file_path)
        pd.testing.assert_frame_equal(df, self.df)

    def test_add_x_to_values(self):
        result_df = ops.add_x_to_values(self.df.copy(), 2, 1, 5)
        expected_values = [522.0, 538.0, 555.0, np.nan, 570.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.add_x_to_values(self.df.copy(), 2, 3, 5)
        expected_values = [520.0, 536.0, 555.0, np.nan, 570.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_sub_x_to_values(self):
        result_df = ops.sub_x_to_values(self.df.copy(), 10, 2, 4)
        expected_values = [520.0, 526.0, 543.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.sub_x_to_values(self.df.copy(), 10, 1, 5)
        expected_values = [510.0, 526.0, 543.0, np.nan, 558.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_mult_x_to_values(self):
        result_df = ops.mult_x_to_values(self.df.copy(), 0.5, 1, 2)
        expected_values = [260.0, 268.0, 553.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.mult_x_to_values(self.df.copy(), 3, 1, 5)
        expected_values = [1560.0, 1608.0, 1659.0, np.nan, 1704.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_div_x_to_values(self):
        result_df = ops.div_x_to_values(self.df.copy(), 0.5, 1, 5)
        expected_values = [1040.0, 1072.0, 1106.0, np.nan, 1136.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

        result_df = ops.div_x_to_values(self.df.copy(), 2, 1, 1)
        expected_values = [260.0, 536.0, 553.0, np.nan, 568.0]
        np.testing.assert_array_equal(list(result_df["value"]), expected_values)

    def test_median_of_values(self):
        self.assertEqual(ops.median_of_values(self.df), 544.5)
        self.assertEqual(ops.median_of_values(self.df, 1, 3), 536)

    def test_quantil_of_values(self):
        self.assertEqual(ops.quantil_of_values(self.df, 0.5), 544.5)
        self.assertEqual(ops.quantil_of_values(self.df, 0.25), 532.0)

    def test_mean_of_values(self):
        self.assertEqual(ops.mean_of_values(self.df), 544.25)
        self.assertEqual(ops.mean_of_values(self.df, 3, 5), 560.5)

    def test_std_of_values(self):
        self.assertAlmostEqual(ops.std_of_values(self.df), 18.00520758)

    def test_add_values_of_multiple_df(self):
        expected_result = pd.DataFrame({
            "region": ["MT"] * 6,
            "position": [1, 2, 3, 4, 5, 6],
            "value": [1041.0, 1086.0, 1106.0, 557.0, 1131.0, 600]
        })

        result = ops.add_values_of_multiple_df([self.df, self.df2])
        pd.testing.assert_frame_equal(result, expected_result)

    def test_median_of_multiple_df(self):
        expected_result = pd.DataFrame({
            "region": ["MT"] * 6,
            "position": [1, 2, 3, 4, 5, 6],
            "value": [520.0, 536.0, 553.0, 557.0, 568.0, 600]
        })

        df4 = pd.DataFrame({
            "region": ["MT"] * 4,
            "position": [3, 4, 5, 6],
            "value": [553.0, 557.0, 568.0, 600]
        })

        df5 = pd.DataFrame({
            "region": ["MT"] * 4,
            "position": [5, 6, 7, 8],
            "value": [520.0, 536.0, 553.0, 557.0]
        })

        expected_result_for_df4_and_df5 = pd.DataFrame({
            "region": ["MT"] * 8,
            "position": [1, 2, 3, 4, 5, 6, 7, 8],
            "value": [0, 0, 276.5, 278.5, 544, 568, 276.5, 278.5]
        })

        result = ops.median_of_multiple_df([self.df, self.df2, self.df3])
        result2 = ops.median_of_multiple_df([df4, df5])
        pd.testing.assert_frame_equal(result, expected_result)
        pd.testing.assert_frame_equal(result2, expected_result_for_df4_and_df5)

    def test_get_max_values_of_multiple_df(self):
        expected_result = pd.DataFrame({
            "region": ["MT"] * 6,
            "position": [1, 2, 3, 4, 5, 6],
            "value": [521.0, 550.0, 1553.0, 1557.0, 1563.0, 1600]
        })

        result = ops.get_max_values_of_multiple_df([self.df, self.df2, self.df3])
        pd.testing.assert_frame_equal(result, expected_result)

    def test_mean_absolute_deviation(self):
        expected_result = 6.5

        result = ops.mean_absolute_deviation(self.df2)
        self.assertEqual(expected_result, result)

    def test_zscore(self):
        expected_result = pd.DataFrame({'first gradient': {0: 29.0, 1: 16.0, 2: 3.5, 3: 5.0, 4: 21.5, 5: 37.0},
                            'second gradient': {0: -13.0, 1: -12.75, 2: -5.5, 3: 9.0, 4: 16.0, 5: 15.5}})

        result = ops.gradients(self.df2)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_previous(self):
        expected_result = pd.Series({0: 0.0, 1: 521.0, 2: 550.0, 3: 553.0, 4: 557.0, 5: 563.0}, name="previous")

        result = ops.previous(self.df2)
        pd.testing.assert_series_equal(result, expected_result)

    def test_parse_for_prediction(self):
        expected_result = pd.DataFrame({'value': {4: 568.0},
         'zscore': {4: 1.2689006466784243},
         'first gradient': {4: 568.0},
         'second gradient': {4: 560.5},
         'previous': {4: 0.0}})

        result, median_df = ops.parse_for_prediction([file_path])
        pd.testing.assert_frame_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()
