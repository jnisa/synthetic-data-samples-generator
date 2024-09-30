# unitary tests for the avro sampling functionality

import os

from unittest import TestCase

import pandas as pd

from fastavro import reader

from synthetic_data_samples_generator.utils.avro import generate_avro_file


class TestAvro(TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup test files before all tests are run"""
        cls.test_file = "test.avro"

    @classmethod
    def tearDownClass(cls):
        """Cleanup test files after all tests are run"""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_generate_avro_file(self):
        """
        Description: test the generate_avro_file function.
        """

        df = pd.DataFrame(
            {
                "name": ["John", "Jane", "Doe"],
                "age": [28, 34, 29],
                "city": ["New York", "London", "Paris"],
            }
        )

        df = df.astype(str)
        generate_avro_file(df, self.test_file)

        assert os.path.exists(self.test_file)

        with open(self.test_file, "rb") as avro_file:
            avro_reader = reader(avro_file)
            records = list(avro_reader)

        assert len(records) == 3
        assert records[0]["name"] == "John"
        assert records[0]["age"] == "28"
        assert records[0]["city"] == "New York"
