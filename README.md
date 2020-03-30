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

Without supplying additional arguments, this will validate and prune the set of sample data points included in the ``data/data_points.csv`` file, and write a new set of pruned data points to ``data/pruned_data_points``.

Data points will be pruned according to the combination of their distance and
their timestamp difference (i.e. a derived 'average speed' between data points).

Sample output:
```
$ python3 validate_route.py
INFO:root:Parsed 227 data points from file data/data_points.csv
INFO:root:Removed 6 invalid gps nodes
INFO:root:Wrote pruned GPS data to data/pruned_data_points.csv
```

The error tolerance is tunable using the ``speed_threshold`` argument, but is set to 100 'average units of speed' for the purposes of this exercise.

Note that this 'speed' metric is an arbitrarily calculated unit, with a scale that was chosen to broadly suit the input data. In a real-world system, this metric would be more carefully specified and derived from the conventions of the input data.

All aspects of the validation can be customised with the following command line arguments:

```
$ python3 validate_route.py --help
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

For example, the verbose output option includes detailed node data and reporting:

```
(gps) bash-3.2$ python3 validate_route.py -v True
INFO:root:Parsed 227 data points from file data/data_points.csv
DEBUG:root:Pruning gps nodes with an average speed threshold of 100 units
DEBUG:root:Node 1: 	speed : 8.46 	dist : 42.32 	time : 5 	51.4984, -0.1604
DEBUG:root:Node 2: 	speed : 5.96 	dist : 29.79 	time : 5 	51.4982, -0.1606
...
DEBUG:root:Node 74: 	speed : 425.21 	dist : 2551.27 	time : 6 	51.5114, -0.1756
DEBUG:root:Node 74 will be pruned
DEBUG:root:Node 75: 	speed : 9.05 	dist : 99.6 	time : 11 	51.4988, -0.1546
...
DEBUG:root:Node 91: 	speed : 0.0 	dist : 0.0 	time : 5 	51.5002, -0.1504
DEBUG:root:Node 92: 	speed : 266.28 	dist : 2662.84 	time : 10 	51.5115, -0.1745
DEBUG:root:Node 92 will be pruned
...
DEBUG:root:Node 226: 	speed : 5.19 	dist : 46.75 	time : 9 	51.5298, -0.1156
INFO:root:Removed 6 invalid gps nodes
INFO:root:Wrote pruned GPS data to data/pruned_data_points.csv
```

## Unit Tests

Use PyTest to run unit tests for the GPS classes. All tests are contained in the ``/tests`` directory of this repo.

```
$ pytest tests/
======= test session starts ==========
platform darwin -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /Users/cormacphelan/Dropbox/code/python/gps
collected 31 items

tests/test_gps_node.py ..............  [ 45%]
tests/test_gps_route.py .................   [100%]

============== 31 passed in 0.15s ===========
```

For code coverage metrics, run the ``coverage`` package, or view the pre-generated HTML report in the ``htmlcov/index.html`` file of this repo.

---

# Class DocStrings

## GpsNode Class
```python
GpsNode(self, x_pos: float = 0.0, y_pos: float = 0.0, timestamp: int = 0)
```

A single GPS node object, describing coordinates and timestamp data

#### Attributes:
* x_pos (float): x coordinate of GpsNode
* y_pos (float): y coordinate of GpsNode
* timestamp (int): timestamp representation of GpsNode

---

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

---

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
* node_list (list): A list of valid GpsNode objects

---

### prune_outlier_nodes
```python
GpsRoute.prune_outlier_nodes(speed_threshold: int = 100)
```

Prunes a route for potentially erroneous nodes.

Nodes will be pruned according to the combination of their distance and
their timestamp (average speed).

For example, given 2 nodes A and B, if they:
* are distant and have widely-separated timestamps: B IS VALID
* are distant and have narrowly-separated timestamps: B IS NOT VALID
* are close and have widely-separated timestamps: B IS VALID
* are close and have narrowly-separated timestamps: B IS VALID

The error tolerance is tunable using the ``speed_threshold`` argument, but is set to 100 'average units of speed' for the purposes of this exercise.

Note that the ``speed`` metric is an arbitrarily calculated unit, with a scale that was chosen to broadly suit the input data. In a real-world system, this metric would be more carefully specified and derived from the conventions of the input data.

#### Args:
* speed_threshold (int): Limit for valid average speeds.

#### Returns:
* integer count of nodes Removed

---

### read_nodes_from_csv
```python
GpsRoute.read_nodes_from_csv(file_path: str)
```

Parses input CSV files for valid Gps point data. Updates the
member variable GpsRoute.node_list

#### Args:
* file_path (str): Input path for data point CSV source

---

### read_nodes_from_list
```python
GpsRoute.read_nodes_from_list(input_data: list)
```

Parses a native Python list of valid GpsNode objects. Updates the
member variable GpsRoute.node_list

#### Args:
* input_data (list): A list of valid GpsNode objects
