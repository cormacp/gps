from ..gps import GpsRoute, GpsNode
import os
import pytest

class TestReadRouteFromList(object):
    def setup(self):
        self.valid_input_list = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728]
        ]
        self.invalid_input_list_char = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,"a"]
        ]
        self.invalid_input_list_dimension = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824]
        ]
        self.route = GpsRoute()

    def test_valid_list_input(self):
        self.route.read_nodes_from_list(self.valid_input_list)
        assert isinstance(self.route.node_list, list)
        assert len(self.route.node_list) == 3
        for node in self.route.node_list:
            assert isinstance(node, GpsNode)
            assert hasattr(node, "x_pos")
            assert hasattr(node, "y_pos")
            assert hasattr(node, "timestamp")

    def test_invalid_list_input(self):
        with pytest.raises(ValueError):
            self.route.read_nodes_from_list(self.invalid_input_list_char)

    def test_invalid_list_dimension(self):
        with pytest.raises(ValueError):
            self.route.read_nodes_from_list(self.invalid_input_list_dimension)

    def test_empty_list_input(self):
        self.route.read_nodes_from_list([])
        assert isinstance(self.route.node_list, list)
        assert len(self.route.node_list) == 0


class TestReadRouteFromCSV(object):
    def setup(self):
        self.csv_path = os.path.join(
            os.path.dirname(__file__), '../data/data_points.csv'
        )
        self.corrupt_csv_path = os.path.join(
            os.path.dirname(__file__), '../data/sample_corrupt_data_points.csv'
        )
        self.invalid_csv_path = "no_such.csv"
        self.route = GpsRoute()

    def test_valid_input_csv(self):
        self.route.read_nodes_from_csv(self.csv_path)
        assert isinstance(self.route.node_list, list)
        assert len(self.route.node_list) == 227
        for node in self.route.node_list:
            assert isinstance(node, GpsNode)
            assert hasattr(node, "x_pos")
            assert hasattr(node, "y_pos")
            assert hasattr(node, "timestamp")

    def test_invalid_input_csv(self):
        with pytest.raises(FileNotFoundError):
            self.route.read_nodes_from_csv(self.invalid_csv_path)

    def test_corrupt_input_csv(self):
        with pytest.raises(ValueError):
            self.route.read_nodes_from_csv(self.corrupt_csv_path)


class TestRoutePruning(object):
    def setup(self):
        self.route_0_errors = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728],
            [51.49804155,-0.1605367034,1326378733],
            [51.49769948,-0.1604581217,1326378738],
            [51.49733998,-0.1606820971,1326378743]
        ]
        self.route_1_error = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728],
            [53.49804155,-10.1605367034,1326378733],
            [51.49769948,-0.1604581217,1326378738],
            [51.49733998,-0.1606820971,1326378743]
        ]
        self.route_3_errors = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728],
            [53.49804155,-10.1605367034,1326378733],
            [51.49769948,-0.1604581217,1326378738],
            [53.49804155,-10.1605367034,1326378739],
            [55.49733998,-0.3606820971,1326378743],
            [51.49733998,-0.1606820971,1326378744]
        ]
        self.route_duplicate_timestamp = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728],
            [51.49804155,-0.1605367034,1326378733],
            [51.49804152,-0.1605367032,1326378733],
            [51.49769948,-0.1604581217,1326378738],
            [51.49733998,-0.1606820971,1326378743]
        ]
        self.stationary_route = [
            [51.49588258,-0.1637460713,1326378984],
            [51.49588258,-0.1637460713,1326378993],
            [51.49588258,-0.1637460713,1326379002]
        ]
        self.route_consecutive_errors = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [53.49820502,-10.1606269428,1326378728],
            [54.49804155,-12.1605367034,1326378733],
            [56.49769948,-60.1604581217,1326378738],
            [51.49733998,-0.1606820971,1326378743]
        ]
        self.route_wide_error_range = [
            [51.49780976,-0.1542154569,1326379255],
            [51.49800006,-0.1539555201,1326379260],
            [51.49815136,-0.1537985061,1326379265],
            [51.5113867,-0.1756095886,1326379271],
            [51.49880463,-0.1545503467,1326379276],
            [51.49908125,-0.1548237447,1326379280],
            [51.49944104,-0.1547229289,1326379285]
        ]
        self.route = GpsRoute()

    def test_perfect_route(self):
        self.route.read_nodes_from_list(self.route_0_errors)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0
        assert len(self.route.node_list) == initial_route_length

    def test_route_1_error(self):
        self.route.read_nodes_from_list(self.route_1_error)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 1
        assert len(self.route.node_list) == initial_route_length - 1

        # Validate with a 2nd pass
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0

    def test_route_3_errors(self):
        self.route.read_nodes_from_list(self.route_3_errors)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 3
        assert len(self.route.node_list) == initial_route_length - 3

        # Validate with a 2nd pass
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0

    def test_route_duplicate_timestamp(self):
        self.route.read_nodes_from_list(self.route_duplicate_timestamp)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 1
        assert len(self.route.node_list) == initial_route_length - 1

        # Validate with a 2nd pass
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0

    def test_stationary_route(self):
        self.route.read_nodes_from_list(self.stationary_route)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0
        assert len(self.route.node_list) == initial_route_length

    def test_route_consecutive_errors(self):
        self.route.read_nodes_from_list(self.route_consecutive_errors)
        initial_route_length = len(self.route.node_list)
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 3
        assert len(self.route.node_list) == initial_route_length - 3

        # Validate with a 2nd pass
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == 0

    def test_low_threshold(self):
        self.route.read_nodes_from_list(self.route_wide_error_range)
        initial_route_length = len(self.route.node_list)
        speed_threshold = 7
        removal_count = self.route.prune_outlier_nodes(speed_threshold)
        assert removal_count == 4
        assert len(self.route.node_list) == initial_route_length - 4

    def test_high_threshold(self):
        self.route.read_nodes_from_list(self.route_wide_error_range)
        initial_route_length = len(self.route.node_list)
        speed_threshold = 400
        removal_count = self.route.prune_outlier_nodes(speed_threshold)
        assert removal_count == 1
        assert len(self.route.node_list) == initial_route_length - 1

    def test_too_short_route(self):
        self.route.read_nodes_from_list([[1,2,3]])
        removal_count = self.route.prune_outlier_nodes()
        assert removal_count == None

class TestWriteCSV(object):
    def setup(self):
        self.valid_input_list = [
            [51.49871493,-0.1601177991,1326378718],
            [51.49840586,-0.1604068824,1326378723],
            [51.49820502,-0.1606269428,1326378728]
        ]
        self.route = GpsRoute()
        self.route.read_nodes_from_list(self.valid_input_list)
        self.output_csv_path = os.path.join(
            os.path.dirname(__file__), '../data/test_output.csv'
        )

    def test_valid_output_path(self):
        self.route.write_to_csv(self.output_csv_path)
        assert os.path.isfile(self.output_csv_path)
        os.remove(self.output_csv_path)
        assert not os.path.isfile(self.output_csv_path)
