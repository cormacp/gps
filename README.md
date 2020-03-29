# GPS

A set of classes for reading, validating and pruning GPS point data

## Installation
No additional packages or utilities are required to run the route validation script and import the GPS classes.

However, if you wish to run additional tools against these classes (e.g. measure test coverage, generate docs, validate style), a Pipfile has been included to resolve requirements, and can be used as follows:

```
cd <project_dir>
pipenv shell
pipenv install --dev
```

## Running

To validate a set of data points, just run the entrypoint script, which imports all GPS classes:

```
cd <project_dir>
python3 validate_route.py
```

Without supplying additional arguments, this will validate and prune the set of sample data points included in the ``data/data_points.csv`` file, and write a new set of pruned data points to ``data/pruned_data_points``

Sample output:
```
python3 validate_route.py
INFO:root:Parsed 227 data points from file data/data_points.csv
INFO:root:Removed 6 invalid gps nodes
INFO:root:Wrote pruned GPS data to data/pruned_data_points.csv
```

However, all aspects of the validation can be customised with the following command line arguments:

```
usage: validate_route.py [-h] [-f SOURCE_DATA] [-v VERBOSE_MODE]
                         [-o OUTPUT_FILE] [-t THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  -f SOURCE_DATA, --file SOURCE_DATA
                        source data point file
  -v VERBOSE_MODE, --verbose VERBOSE_MODE
                        set verbose logging
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        data point output path
  -t THRESHOLD, --threshold THRESHOLD
                        threshold avg. speed for data point pruning
```

## Unit Tests

---

# Class DocStrings

---

## GpsNode Class
```python
GpsNode(self, x_pos: float = 0.0, y_pos: float = 0.0, timestamp: int = 0)
```

A single GPS node object, describing coordinates and timestamp data

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

---

## GpsRoute Class
```python
GpsRoute(self, node_list: list = [])
```

A GPS route object, comprising multiple GpsNode objects

#### Attributes:
* node_list (node_list): A list of valid GpsNode objects


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
* integer count of nodes Removed


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
