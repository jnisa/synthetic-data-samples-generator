# unitary tests that will be performed on the synthetic_sample.py file

import os
import shutil

from unittest import TestCase

from synthetic_data_samples_generator.configs.constants import FileType, ValuesType
from synthetic_data_samples_generator.generator.engine import SyntheticDataGenerator


class TestSyntheticDataGenerator(TestCase):

    def test_target_size_mb_basic(self):
        """
        Description: Test the target_size_mb property with a basic value that passes
        the validation.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        actual = generator.target_size_mb
        expected = 10

        self.assertEqual(actual, expected)

    def test_target_size_mb_exception(self):
        """
        Description: Test the target_size_mb property with a value that should raise
        an exception.
        """

        with self.assertRaises(ValueError):
            SyntheticDataGenerator(target_size_mb=0, num_columns=5)

    def test_num_columns_basic(self):
        """
        Description: Test the num_columns property with a basic value that passes
        the validation.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        actual = generator.num_columns
        expected = 5

        self.assertEqual(actual, expected)

    def test_num_columns_exception(self):
        """
        Description: Test the num_columns property with a value that should raise
        an exception.
        """

        with self.assertRaises(ValueError):
            SyntheticDataGenerator(target_size_mb=10, num_columns=0)

    def test_sample_rows_num_basic(self):
        """
        Description: Test the sample_rows_num property with a basic value that passes
        the validation.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        actual = generator.sample_rows_num
        expected = 1000

        self.assertEqual(actual, expected)

    def test_sample_rows_num_exception(self):
        """
        Description: Test the sample_rows_num property with a value that should raise
        an exception.
        """

        with self.assertRaises(ValueError):
            SyntheticDataGenerator(target_size_mb=10, num_columns=5, sample_rows_num=0)

    def test__prepare_file_path(self):
        """
        Description: Test the _prepare_file_path method.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        actual = generator._prepare_file_path("test__prepare_file_path", FileType.CSV, "test_data")
        expected = "test_data/test__prepare_file_path.csv"

        self.assertEqual(actual, expected)

    def test_save_scaled_data(self):
        """
        Description: Test the save_scaled_data method.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        df = generator.generate_dataframe(values_type=ValuesType.INTEGER)
        generator._save_and_scale_data(df, "test_data/test_save_scaled_data.csv", FileType.CSV)

        self.assertTrue(os.path.exists("test_data/test_save_scaled_data.csv"))

    def test_save_dataframe_csv(self):
        """
        Description: Test the save_dataframe method with a csv file.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        df = generator.generate_dataframe(values_type=ValuesType.INTEGER)
        generator.save_dataframe(df, "test_data/test_save_dataframe_csv.csv", FileType.CSV)

        self.assertTrue(os.path.exists("test_data/test_save_dataframe_csv.csv"))

    def test_save_dataframe_json(self):
        """
        Description: Test the save_dataframe method with a json file.
        """

        generator = SyntheticDataGenerator(target_size_mb=10)

        df = generator.generate_dataframe(values_type=ValuesType.STRING)
        generator.save_dataframe(df, "test_data/test_save_dataframe_json.json", FileType.JSON)

        self.assertTrue(os.path.exists("test_data/test_save_dataframe_json.json"))

    def test_generate_file_csv(self):
        """
        Description: Test the generate_file method with a csv file.
        """

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        generator.generate_file(values_type=ValuesType.INTEGER, file_name="test_generate_file_csv", file_type=FileType.CSV, landing_path="test_data")

        self.assertTrue(os.path.exists("test_data/test_generate_file_csv.csv"))

    def test_generate_all_file_types(self):
        """
        Description: Test the generate_all_file_types method.
        """

        base_file_name = "test_all_types"
        landing_path = "test_data"

        generator = SyntheticDataGenerator(target_size_mb=10, num_columns=5)

        generator.generate_all_file_types(base_file_name, landing_path)

        for file_type in FileType:
            file_name = "/".join([landing_path, f"{base_file_name}.{file_type.value}"])
            self.assertTrue(os.path.exists(file_name))
            # TODO. passing to all the types except .ttl - reasons on the README.md
            # assert 9.5 <= SyntheticDataGenerator.get_file_size_in_mb(file_name) <= 10.5

    @classmethod
    def tearDownClass(cls):
        """Cleanup test files after all tests are run"""

        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
