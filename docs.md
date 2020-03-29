# GPS

A set of classes for reading, validating and pruning GPS point data

## GpsNode
```python
GpsNode(self, x_pos: float = 0.0, y_pos: float = 0.0, timestamp: int = 0)
```

A single GPS node object

#### Attributes:
* x_pos (float): x coordinate of GpsNode
* y_pos (float): y coordinate of GpsNode
* timestamp (int): timestamp representation of GpsNode


### get_distance
```python
GpsNode.get_distance(dest_x: float, dest_y: float)
```

Uses cartesian formula to obtain the distance to a destination point:
    sqrt((x2-x1)^2 + (y2-y1))^2

#### Args:
* dest_x (float): x coordinate of destination point
* dest_y (float): y coordinate of destination point

#### Returns:
* float: distance from the GpsNode to the destination point


### get_time_difference
```python
GpsNode.get_time_difference(dest_timestamp: int)
```

Obtain the timestamp difference to a destination point

#### Args:
* dest_timestamp (int): timestamp of destination GpsNode

#### Returns:
* int: time difference between the GpsNode and the destination point


## GpsRoute
```python
GpsRoute(self, node_list: list = [])
```

A GPS route object, comprising multiple GpsNode objects

#### Attributes:
* node_list (node_list): A list of valid GpsNode objects


### read_nodes_from_csv
```python
GpsRoute.read_nodes_from_csv(file_path: str)
```

Parses input CSV files for valid Gps point data. Updates the
member variable GpsRoute.node_list

#### Args:
* file_path (str): Input path for data point CSV source


### read_nodes_from_list
```python
GpsRoute.read_nodes_from_list(input_data: list)
```

Parses a native Python list of valid GpsNode objects. Updates the
member variable GpsRoute.node_list

#### Args:
* input_data (list): A list of valid GpsNode objects


### prune_outlier_nodes
```python
GpsRoute.prune_outlier_nodes(speed_threshold: int = 100)
```

Prunes a route for potentially erroneous nodes.
Nodes will be pruned according to the combination of their distance and
their timestamp (average speed).
For example, given 2 nodes A and B, if they:
    - are distant and have widely-separated timestamps: B IS VALID
    - are distant and have narrowly-separated timestamps: B IS NOT VALID
    - are close and have widely-separated timestamps: B IS VALID
    - are close and have narrowly-separated timestamps: B IS VALID

#### Args:
* speed_threshold (int): Limit for valid average speeds.

#### Returns:
* integer count of nodes removed
