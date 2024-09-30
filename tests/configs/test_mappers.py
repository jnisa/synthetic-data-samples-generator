# test for the mappers.py file

from unittest import TestCase

from synthetic_data_samples_generator.configs.mappers import TypeMapping


class TestTypeMapping(TestCase):

    def test_type_mapping(self):
        """
        Description: when the TypeMapping class is instantiated, it should have the following attributes:
        """

        mapping = TypeMapping()

        self.assertEqual(mapping.int64, "int")
        self.assertEqual(mapping.float64, "float")
        self.assertEqual(mapping.bool, "boolean")
        self.assertEqual(mapping.object, "string")
        self.assertEqual(mapping.datetime64_ns, "string")

    def test_get(self):
        """
        Description: when the get method is called, it should return the corresponding rdflib type.
        """

        mapping = TypeMapping()

        self.assertEqual(mapping.get("int64"), "int")
        self.assertEqual(mapping.get("float64"), "float")
        self.assertEqual(mapping.get("bool"), "boolean")
