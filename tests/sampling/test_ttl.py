# unitary tests for the ttl sampling

from unittest import TestCase
from unittest.mock import patch, Mock
from rdflib import Graph
from rdflib import Literal
from rdflib import RDF
from rdflib import URIRef
from rdflib import BNode

from rdflib.namespace import FOAF

from synthetic_data_samples_generator.sampling.ttl import TTLSampling
from synthetic_data_samples_generator.utils.triples import generate_unique_values


class TestTTL(TestCase):

    def test_check_triples_lst_basic(self):
        """
        Description: when the list of triples is valid, the function should return True
        """

        sampling = TTLSampling()

        triples_test_set = [
            (URIRef("John"), RDF.type, FOAF.Person),
            (URIRef("John"), RDF.type, FOAF.Person),
            (URIRef("John"), RDF.type, Literal("John Doe")),
            (URIRef("John"), RDF.type, Literal("Johnny")),
            (URIRef("John"), RDF.type, BNode()),
            (URIRef("John"), RDF.type, BNode()),
        ]

        self.assertTrue(sampling._check_triples_lst(triples_test_set))

    def test_check_triples_lst_exception(self):
        """
        Description: when the list of triples is not valid, the function should raise an exception
        """

        sampling = TTLSampling()

        triples_test_set = [
            ("test_name_1", "test_predicate_1", "test_object_1"),
            ("test_name_2", "test_predicate_2", "test_object_2"),
            ("test_name_3", "test_predicate_3", "test_object_3"),
        ]

        with self.assertRaises(Exception):
            sampling._check_triples_lst(triples_test_set)

    def test_scale_ttl_file(self):
        """
        Description: when the ttl file is scaled, the size of the file should be the target size
        """

        sampling = TTLSampling()

        test_current_size_mb = 1
        test_target_size_mb = 2

        actual = sampling.scale_ttl_file(Graph(), test_current_size_mb, test_target_size_mb)
        expected = Graph()
        for triple in generate_unique_values(int(test_target_size_mb // test_current_size_mb)):
            expected.add(triple)

        self.assertEqual(len(actual), len(expected))

    def test_sample_ttl_file(self):
        """
        Description: when sample_ttl_file is called with a number of triples, it should return a graph
        containing triples similar to the custom sample.
        """

        sampling = TTLSampling()

        actual = sampling.sample_ttl_file(10)

        expected = Graph()
        for triple in generate_unique_values(10):
            expected.add(triple)

        self.assertEqual(len(actual), len(expected))

    @patch("rdflib.Graph.parse")
    def test_load_ttl_file(self, mock_parse):
        """
        Description: when the load_ttl_file method is called, it should return a graph with the triples from the file.
        """

        mock_graph = Graph()
        mock_graph.add((URIRef("http://example.org/person1"), FOAF.name, Literal("Alice")))
        mock_graph.add((URIRef("http://example.org/person2"), FOAF.name, Literal("Bob")))

        mock_parse.return_value = mock_graph

        sampling = TTLSampling()
        actual = sampling.load_ttl_file("tests/sampling/test_data/test_input.ttl")

        mock_parse.assert_called_once_with("tests/sampling/test_data/test_input.ttl", format="turtle")

        self.assertEqual(len(actual), len(mock_graph))
        for triple in mock_graph:
            self.assertIn(triple, actual)
