# script dedicated to test auxiliar methods

from unittest import TestCase

import pandas as pd

from synthetic_data_samples_generator.utils.pandas import dataframe_multiplier


class TestAuxiliars(TestCase):

    def setUp(self):
        """
        Setup the resources that will be used in the tests.
        """

        self.df_sample = pd.DataFrame(
            {
                "col_1": [1, 2, 3, 4],
                "col_2": [4, 5, 6, 7],
                "col_3": [7, 8, 9, 10],
                "col_4": [10, 11, 12, 13],
            }
        )

    def test_dataframe_multiplier_augmentation(self):
        """
        Description: when the scalling factor is higher than 1.
        """

        df = dataframe_multiplier(self.df_sample, 1, 2)

        actual = df.shape[0]
        expected = 8

        self.assertEqual(actual, expected)

    def test_dataframe_multiplier_reduction(self):
        """
        Description: when the scalling factor is lower than 1.
        """

        df = dataframe_multiplier(self.df_sample, 1, 0.5)

        actual = df.shape[0]
        expected = 2

        self.assertEqual(actual, expected)
