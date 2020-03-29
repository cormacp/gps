from ..gps import GpsNode
import pytest


class TestNodeDistance(object):
    def test_default_init(self):
        node_1 = GpsNode()
        assert node_1.x_pos == 0
        assert node_1.y_pos == 0
        assert node_1.timestamp == 0

    def test_valid_init(self):
        node_1 = GpsNode(1.0, 2.0, 12345)
        assert node_1.x_pos == 1
        assert node_1.y_pos == 2
        assert node_1.timestamp == 12345

    def test_invalid_inits(self):
        with pytest.raises(ValueError):
            GpsNode("not_a_coordinate", 2.0, 1234)

        with pytest.raises(ValueError):
            GpsNode(1.0, "not_a_coordinate", 1234)

        with pytest.raises(ValueError):
            GpsNode(1.0, 2.0, "not_a_timestamp")

    def test_zero_distance(self):
        node_1 = GpsNode(1.0, 2.0, 12345)
        node_2 = GpsNode(1.0, 2.0, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 0

    def test_positive_distance(self):
        node_1 = GpsNode(1.0, 2.0, 12345)
        node_2 = GpsNode(1.0, 4.0, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 2

    def test_negative_distance(self):
        node_1 = GpsNode(1.0, 4.0, 12345)
        node_2 = GpsNode(1.0, 1.0, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 3

    def test_diagonal_positive_distance(self):
        node_1 = GpsNode(4, 8, 12345)
        node_2 = GpsNode(8, 11, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 5

    def test_diagonal_negative_distance(self):
        node_1 = GpsNode(6, 2, 12345)
        node_2 = GpsNode(2, -1, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 5

    def test_zero_crossing_distance(self):
        node_1 = GpsNode(1.0, -2.0, 12345)
        node_2 = GpsNode(1.0, 3.0, 6789)
        assert node_1.get_distance(node_2.x_pos, node_2.y_pos) == 5


class TestNodeTimeDiff(object):
    def test_positive_time_difference(self):
        node_1 = GpsNode(1.0, 2.0, 1326378718)
        node_2 = GpsNode(11.0, 3.0, 1326378723)
        assert node_1.get_time_difference(node_2.timestamp) == 5

    def test_negative_time_difference(self):
        node_1 = GpsNode(1.0, 2.0, 1326378723)
        node_2 = GpsNode(11.0, 3.0, 1326378718)
        assert node_1.get_time_difference(node_2.timestamp) == -5

    def test_zero_time_difference(self):
        node_1 = GpsNode(1.0, 2.0, 1326378718)
        node_2 = GpsNode(11.0, 3.0, 1326378718)
        assert node_1.get_time_difference(node_2.timestamp) == 0


class TestNodeRepresentations(object):
    def setup(self):
        self.node = GpsNode(1, 2, 3)

    def test_repr(self):
        assert self.node.__repr__() == '{x_pos:1, y_pos=2, timestamp=3}'

    def test_str(self):
        assert self.node.__str__() == 'GpsNode(x_pos=1, y_pos=2, timestamp=3)'
