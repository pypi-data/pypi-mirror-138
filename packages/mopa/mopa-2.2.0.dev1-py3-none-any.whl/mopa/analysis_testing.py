"""Testing library for analysis.py"""

import unittest

import pandas as pd
import pandas.testing as pd_testing

import analysis


class AnalysisLib(unittest.TestCase):
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_get_nondomintated_default(self):
        # Setup
        df_test = pd.DataFrame(
            {'A': [3, 2, 2], 'B': [3, 1, 2], 'C': [3, 2, 1]}
        )
        df_expect = pd.DataFrame({'A': [2, 2], 'B': [1, 2], 'C': [2, 1]})

        # Run
        df_result = analysis.get_nondomintated(
            df_test,
            objs=['A', 'B', 'C'],
        )

        # Check equal
        self.assertEqual(df_expect, df_result)

    def test_get_nondomintated_max(self):
        # Setup
        df_test = pd.DataFrame(
            {'A': [2, 2, 1], 'B': [3, 3, 1], 'C': [3, 2, 1]}
        )
        df_expect = pd.DataFrame({'A': [2, 1], 'B': [3, 1], 'C': [3, 1]})

        # Run
        df_result = analysis.get_nondomintated(
            df_test,
            objs=['A', 'B', 'C'],
            max_objs=['C']
        )

        # Check equal
        self.assertEqual(df_expect, df_result)

    def test_get_native_robust_metric(self):
        # Setup
        df_test = pd.DataFrame({'A': [1, 1, 2, 2], 'B': [3, 4, 5, 6]})
        df_expect = pd.DataFrame(
            {
                'A': [1, 1, 2, 2],
                'B': [3, 4, 5, 6],
                'max_B': [4, 4, 6, 6]
            }
        )

        # Run
        df_result = analysis.get_native_robust_metrics(
            df=df_test,
            dec_labs=['A'],
            obj_labs=['B'],
            robust_types=['max']
        )

        # Check equal
        self.assertEqual(df_expect, df_result)

    def test_combine_device_df_different_columns(self):
        # Setup
        df_list_test = [
            pd.DataFrame({'A': [1, 1], 'B': [2, 2]}),
            pd.DataFrame({'A': [3, 3], 'C': [4, 4]})
        ]

        # Test
        with self.assertRaises(ValueError):
            analysis.combine_device_df(df_list_test, ['foo', 'bar'])


if __name__ == '__main__':
    unittest.main()
