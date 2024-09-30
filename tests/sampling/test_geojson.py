# unitary tests for the geojson sampling functionality

from unittest import TestCase
from unittest.mock import patch

import geopandas as gpd
from geopandas import GeoDataFrame

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon
from shapely.geometry import GeometryCollection

from synthetic_data_samples_generator.configs.constants import GeometryTypes
from synthetic_data_samples_generator.sampling.geojson import GeoJSONSampling


class TestGeoJSONSampling(TestCase):

    def setUp(self):
        self.geojson_sampling = GeoJSONSampling()
        self.assertInRange = lambda val, lim_inf, lim_sup: lim_inf <= val <= lim_sup

    def test_create_point_record(self):
        """
        Description: Test the creation of point records.
        """

        point_record = self.geojson_sampling._create_point_record()

        self.assertIsInstance(point_record, Point)
        self.assertInRange(point_record.x, -180, 180)
        self.assertInRange(point_record.y, -180, 180)

    def test_create_linestring_record(self):
        """
        Description: Test the creation of linestring records.
        """

        linestring_record = self.geojson_sampling._create_linestring_record()

        self.assertIsInstance(linestring_record, LineString)
        self.assertEqual(len(linestring_record.coords), 2)

        for coord in linestring_record.coords:
            self.assertInRange(coord[0], -180, 180)
            self.assertInRange(coord[1], -90, 90)

    def test_create_polygon_record(self):
        """
        Description: Test the creation of polygon records.
        """

        polygon_record = self.geojson_sampling._create_polygon_record()

        self.assertIsInstance(polygon_record, Polygon)
        self.assertEqual(len(polygon_record.exterior.coords), 6)

        for coord in polygon_record.exterior.coords:
            self.assertInRange(coord[0], -180, 180)
            self.assertInRange(coord[1], -90, 90)

    def test_create_multipoint_record(self):
        """
        Description: Test the creation of multipoint records.
        """

        multipoint_record = self.geojson_sampling._create_multipoint_record()

        self.assertIsInstance(multipoint_record, MultiPoint)
        self.assertEqual(len(multipoint_record.geoms), 3)

        for point in multipoint_record.geoms:
            self.assertIsInstance(point, Point)
            self.assertInRange(point.x, -180, 180)
            self.assertInRange(point.y, -90, 90)

    def test_create_multilinestring_record(self):
        """
        Description: Test the creation of multilinestring records.
        """

        multilinestring_record = self.geojson_sampling._create_multilinestring_record()

        self.assertIsInstance(multilinestring_record, MultiLineString)
        self.assertEqual(len(multilinestring_record.geoms), 3)

        for linestring in multilinestring_record.geoms:
            self.assertIsInstance(linestring, LineString)
            self.assertEqual(len(linestring.coords), 2)
            self.assertInRange(list(linestring.coords)[0][0], -180, 180)
            self.assertInRange(list(linestring.coords)[0][1], -90, 90)
            self.assertInRange(list(linestring.coords)[1][0], -180, 180)
            self.assertInRange(list(linestring.coords)[1][1], -90, 90)

    def test_create_multipolygon_record(self):
        """
        Description: Test the creation of multipolygon records.
        """

        multipolygon_record = self.geojson_sampling._create_multipolygon_record()

        self.assertIsInstance(multipolygon_record, MultiPolygon)
        self.assertEqual(len(multipolygon_record.geoms), 3)

        for polygon in multipolygon_record.geoms:
            self.assertIsInstance(polygon, Polygon)
            self.assertEqual(len(polygon.exterior.coords), 6)
            for x, y in polygon.exterior.coords:
                self.assertInRange(x, -180, 180)
                self.assertInRange(y, -90, 90)

    def test_create_geometrycollection_record(self):
        """
        Description: Test the creation of geometrycollection records.
        """

        geometrycollection_record = self.geojson_sampling._create_geometrycollection_record()

        self.assertIsInstance(geometrycollection_record, GeometryCollection)
        self.assertEqual(len(geometrycollection_record.geoms), 3)

        for geom in geometrycollection_record.geoms:
            self.assertIsInstance(geom, (Point, LineString, Polygon))

    def test_generate_sample_basic(self):
        """
        Description: Test the generation of a sample of records.
        """

        sample = self.geojson_sampling.generate_sample()

        self.assertIsInstance(sample, GeoDataFrame)
        self.assertEqual(len(sample), 7)

        for geom in sample.geometry:
            self.assertIsInstance(
                geom,
                (
                    Point,
                    LineString,
                    Polygon,
                    MultiPoint,
                    MultiLineString,
                    MultiPolygon,
                    GeometryCollection,
                ),
            )

    @patch("geopandas.read_file")
    def test_load_file(self, mock_read_file):
        """
        Description: Test the loading of a file.
        """

        mock_gdf = gpd.GeoDataFrame({"geometry": [Point(0, 0), Point(1, 1)], "attribute": ["A", "B"]})

        mock_read_file.return_value = mock_gdf

        file_path = "tests/sampling/test_data/test_input.geojson"
        sample = self.geojson_sampling.load_file(file_path)

        mock_read_file.assert_called_once_with(file_path)

        self.assertIs(sample, mock_gdf)
        self.assertIsInstance(sample, GeoDataFrame)
        self.assertEqual(len(sample), 2)
        self.assertEqual(list(sample.columns), ["geometry", "attribute"])
