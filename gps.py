import csv
import logging
import math


class GpsNode:
    def __init__(self, x_pos: float = 0.0, y_pos: float = 0.0, timestamp: int = 0):
        """
        Args:
            x_pos (float): x coordinate of GpsNode
            y_pos (float): y coordinate of GpsNode
            timestamp (int): timestamp representation of GpsNode
        """
        if (
            not isinstance(x_pos, (float, complex, int)) or
            not isinstance(y_pos, (float, complex, int)) or
            not isinstance(timestamp, (float, complex, int))
        ):
            raise ValueError()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.timestamp = int(timestamp)

    def get_distance(self, dest_x: float, dest_y: float) -> float:
        """
        Uses cartesian formula to obtain the distance to a destination point:
            sqrt((x2-x1)^2 + (y2-y1))^2

        Args:
            dest_x (float): x coordinate of destination point
            dest_y (float): y coordinate of destination point

        Returns:
            float: distance from the GpsNode to the destination point
        """
        x_diff = dest_x - self.x_pos
        y_diff = dest_y - self.y_pos
        node_distance = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))
        return node_distance

    def get_time_difference(self, dest_timestamp: int) -> int:
        """
        Obtain the timestamp difference to a destination point

        Args:
            dest_timestamp (int): timestamp of destination GpsNode

        Returns:
            int: time difference between the GpsNode and the destination point
        """
        time_diff = dest_timestamp - self.timestamp
        return time_diff

    def __repr__(self):
        str_obj = f"{{x_pos:{self.x_pos}, y_pos={self.y_pos}, timestamp={self.timestamp}}}"
        return str_obj

    def __str__(self):
        str_obj = f"GpsNode(x_pos={self.x_pos}, y_pos={self.y_pos}, timestamp={self.timestamp})"
        return str_obj


class GpsRoute:
    def __init__(self, node_list: list = []):
        self.node_list = node_list

    def read_nodes_from_csv(self, file_path: str) -> bool:
        """
        Parses input CSV files for valid Gps point data. Updates the
        member variable GpsRoute.node_list

        Args:
            file_path (str): Input path for data point CSV source
        """
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            node_data = list(reader)
        nodes = []
        for node in node_data:
            if len(node) != 3:
                raise ValueError()
            nodes.append(GpsNode(float(node[0]), float(node[1]), int(node[2])))
        self.node_list = nodes

    def read_nodes_from_list(self, input_data: list) -> bool:
        """
        Parses a native Python list of valid GpsNode objects. Updates the
        member variable GpsRoute.node_list

        Args:
            input_data (list): A list of valid GpsNode objects
        """
        nodes = []
        for node in input_data:
            if len(node) != 3:
                raise ValueError()
            nodes.append(GpsNode(node[0], node[1], node[2]))
        self.node_list = nodes

    def write_to_csv(self, file_path: str = "output.csv"):
        with open(file_path, 'w') as file:
            for node in self.node_list:
                data_row = f"{str(node.x_pos)},{str(node.y_pos)},{str(node.timestamp)}"
                file.write(data_row)
                file.write('\n')

    def prune_outlier_nodes(self, speed_threshold: int = 100) -> int:
        """
        Prune a route for potentially erroneous nodes.
        Nodes will be pruned according to the combination of their distance and
        their timestamp (average speed).
        For example, given 2 nodes A and B, if they:
            - are distant and have widely-separated timestamps: B IS VALID
            - are distant and have narrowly-separated timestamps: B IS NOT VALID
            - are close and have widely-separated timestamps: B IS VALID
            - are close and have narrowly-separated timestamps: B IS VALID

        Args:
            speed_threshold (int): Limit for valid average speeds.

        returns
            integer count of nodes removed
        """
        logging.debug(f"Pruning gps nodes with an average speed threshold of {speed_threshold} units")

        initial_length = len(self.node_list)
        removal_count = 0

        # No pruning is possible with less than 2 route nodes
        if initial_length < 2:
            return None

        nodes_for_pruning = []
        window = 1  # tracks width of comparison window (varies when invalid nodes are detected)

        # Iterate nodes, determine if each average speed exceeds the threshold
        for i in range(1, len(self.node_list)):
            time_diff = self.node_list[i-window].get_time_difference(
                self.node_list[i].timestamp)
            if time_diff == 0:
                nodes_for_pruning.append(i)
                logging.debug(f"Node {i} will be pruned\n")
                window += 1
            else:
                distance = self.node_list[i-window].get_distance(
                    self.node_list[i].x_pos, self.node_list[i].y_pos)
                distance = round(distance*100000, 2)    # linear scaling for readability
                avg_speed = round(distance/time_diff, 2)
                logging.debug(f"Node {i}: \tspeed : {avg_speed} \tdist : {distance} \ttime : {time_diff} \t{round(self.node_list[i].x_pos, 4)}, {round(self.node_list[i].y_pos, 4)} ")
                if avg_speed > speed_threshold:
                    nodes_for_pruning.append(i)
                    logging.debug(f"Node {i} will be pruned\n")
                    window += 1
                else:
                    window = 1

        nodes_for_pruning.sort(reverse=True)
        for node_idx in nodes_for_pruning:
            self.node_list.pop(node_idx)
        removal_count = initial_length - len(self.node_list)
        return removal_count

    def __repr__(self):
        str_obj = f"{{data point count:{len(self.node_list)}}}"
        return str_obj

    def __str__(self):
        str_obj = f"GpsRoute(data point count={len(self.node_list)})"
        return str_obj
