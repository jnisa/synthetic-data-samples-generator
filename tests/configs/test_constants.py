# unitary tests that will be performed on the constants.py file

from unittest import TestCase

from synthetic_data_samples_generator.configs.constants import FileType


class TestFileType(TestCase):

    def test_file_type_values(self):
        """
        Description: Test the values of the FileType enum.
        """

        self.assertEqual(FileType.CSV.value, "csv")
        self.assertEqual(FileType.JSON.value, "json")
        self.assertEqual(FileType.PARQUET.value, "parquet")
        self.assertEqual(FileType.GEOJSON.value, "geojson")
        self.assertEqual(FileType.AVRO.value, "avro")
        self.assertEqual(FileType.TURTLE.value, "turtle")

    def test_file_type_members(self):
        """
        Description: Test the members of the FileType enum.
        """

        self.assertEqual(len(FileType), 6)
        self.assertIn(FileType.CSV, FileType)
        self.assertIn(FileType.JSON, FileType)
        self.assertIn(FileType.PARQUET, FileType)
        self.assertIn(FileType.GEOJSON, FileType)
        self.assertIn(FileType.AVRO, FileType)
        self.assertIn(FileType.TURTLE, FileType)

    def test_file_type_uniqueness(self):
        """
        Description: Test the uniqueness of the FileType enum.
        """

        values = [member.value for member in FileType]
        self.assertEqual(len(values), len(set(values)))
