import unittest
import app.prediction.OperationsOnWiggle

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here



    def test_add_x(self):
        wiggle = os.path.relpath('test_files\\test.wig')
        df = app.prediction.OperationsOnWiggle.parse_wiggle_to_DataFrame(wiggle)
        self.assertEqual(app.prediction.OperationsOnWiggle.add_x(df, 1, 0, len(df['value'])), )

    wiggle = os.path.relpath('..\\..\\tests\\test_files\\test.wig')
    df = parse_wiggle_to_DataFrame(wiggle)
    print(df)
    df1 = add_x(df, 1, 0, len(df['value']))
    print(df1)


if __name__ == '__main__':
    unittest.main()
